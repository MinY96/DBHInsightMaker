# pylint: disable=W0718, E1101, C0413, C0103, C0321, C0301
"""
회귀 분석
"""

from typing import List, Dict, Optional

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# statsmodels
import statsmodels.api as sm
from statsmodels.tools import add_constant
from statsmodels.tools.sm_exceptions import PerfectSeparationError
from statsmodels.stats.outliers_influence import variance_inflation_factor

# sklearn (다항 로지스틱/리플)
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import log_loss

# ---------- utils ----------
def _aic_from_loglik(ll: float, k: int) -> float:
    return 2 * k - 2 * ll

def _bic_from_loglik(l1: float, k: int, n: int) -> float:
    return np.log(n) * k - 2 * l1

def _loglik_gaussian(y: np.ndarray, yhat: np.ndarray) -> float:
    n = len(y)
    resid = y - yhat
    rss = float(np.dot(resid, resid))
    sigma2 = rss / max(n, 1)
    return -0.5 * n * (np.log(2 * np.pi * sigma2) + 1)

def _loglik_multinomial(y: np.ndarray, proba: np.ndarray) -> float:
    n = len(y)
    idx = (np.arange(n), y.astype(int))
    p = np.clip(proba[idx], 1e-15, 1.0)
    return float(np.sum(np.log(p)))

def _compute_vif(X_design: pd.DataFrame) -> pd.Series:
    """
    const를 제외한 설계행렬에서 각 컬럼의 VIF 계산.
    반환: index=컬럼명, value=VIF (const는 NaN)
    """
    if "const" in X_design.columns:
        X_ = X_design.drop(columns=["const"]).copy()
    else:
        X_ = X_design.copy()

    if X_.shape[1] <= 1:
        # 피처가 1개 이하면 VIF 의미가 희박하므로 NaN으로 채움
        out = pd.Series({c: np.nan for c in X_design.columns})
        return out

    arr = X_.to_numpy()
    cols = X_.columns.tolist()
    vifs = []
    for i in range(arr.shape[1]):
        try:
            vifs.append(variance_inflation_factor(arr, i))
        except Exception:
            vifs.append(np.nan)

    out = pd.Series(vifs, index=cols)
    if "const" in X_design.columns:
        out = pd.concat([pd.Series({"const": np.nan}), out])
    return out.reindex(X_design.columns)


# ---------- main ----------
class VariableSelector:
    """
    전처리/공선성 프루닝 없이, 그룹 단위(add/drop) 변수선택을 수행하는 슬림 버전.
    - method: "forward" | "backward" | "stepwise"
    - model_type: "auto" | "linear" | "logit" | "multilogit"
    - group_map: {그룹라벨: [더미열들]} (미지정 열은 자동으로 '단일 유닛')
    - track_all_trials: True면 각 step에서 모든 후보 시도의 지표도 기록
    - select(record_post_best=True): 최적 다음 차수(post-best) 1스텝을 히스토리에 기록(차트 꺾임 표시)
    - plot_history: 노란 ⭐(최적점) + 수치 주석 + 정수 x축 + post-best 표식
    - 반환 info:
        * variables (실제 사용된 열 리스트)
        * selected_units (그룹/단일 유닛 라벨)
        * coef_table (선형/이항: VIF 열 포함, 다항: 별도 info['vif'])
        * 성능: (linear) rmse, r2, adj_r2 / (logit, multilogit) accuracy, logloss
        * predictions DF: (linear) y, y_pred / (logit) y, y_pred, y_proba / (multi) y, y_pred, y_proba_max
    """
    def __init__(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        method: str = "stepwise",
        model_type: str = "auto",
        *,
        group_map: Optional[Dict[str, List[str]]] = None,
        regularize_fallback: bool = True,
        max_iter: int = 1000,
        random_state: int = 42,
        track_all_trials: bool = False
    ):
        self.method = method
        self.model_type = model_type
        self.group_map = group_map or {}
        self.regularize_fallback = regularize_fallback
        self.max_iter = max_iter
        self.random_state = random_state
        self.track_all_trials = track_all_trials

        # 입력 유효성 (전처리 완료 가정)
        self.X_in = X.copy()
        self.y = pd.Series(y).copy()
        if self.X_in.isna().any().any() or pd.isna(self.y).any():
            raise ValueError("X/y에 결측치가 있습니다. 전처리 후 다시 시도하세요.")
        if np.isinf(self.X_in.to_numpy()).any():
            raise ValueError("X에 Inf 값이 있습니다. 전처리 후 다시 시도하세요.")

        # 디자인 행렬
        self.X = add_constant(self.X_in, has_constant="add")

        # 모델 타입 자동
        if self.model_type == "auto":
            if pd.api.types.is_numeric_dtype(self.y) and self.y.nunique() > 10:
                self.model_type = "linear"
            elif self.y.nunique() == 2:
                self.model_type = "logit"
            else:
                self.model_type = "multilogit"

        # ---- 그룹 유닛 구성 ----
        all_cols = list(self.X_in.columns)
        grouped_cols = set(c for cols in self.group_map.values() for c in cols)
        # group_map 검증
        not_in_X = grouped_cols - set(all_cols)
        if not_in_X:
            raise ValueError(f"group_map에 X에 없는 열이 포함되어 있습니다: {sorted(not_in_X)[:5]} ...")

        # 동일 열이 여러 그룹에 들어간 경우 방지
        owner = {}
        for g, cols in self.group_map.items():
            for c in cols:
                if c in owner and owner[c] != g:
                    raise ValueError(f"열 '{c}'가 여러 그룹에 중복 배정: '{owner[c]}' vs '{g}'")
                owner[c] = g

        # 유닛 맵: 그룹 + 단일
        self.units_map: Dict[str, List[str]] = {}
        for g, cols in self.group_map.items():
            if cols:
                self.units_map[g] = list(cols)
        for c in all_cols:
            if c not in grouped_cols:
                self.units_map[c] = [c]

        # 히스토리 저장
        self.history_: List[Dict] = []

    # --------- fitters ---------
    def _fit_linear(self, X: pd.DataFrame, y: pd.Series):
        try:
            res = sm.OLS(y, X, missing="raise").fit()
            y_pred = res.predict(X)
            llf = float(res.llf)
            aic = float(res.aic)
            bic = float(res.bic)
            n = len(y)
            k = len(res.params)
            coef_table = res.summary2().tables[1].copy()
            vif = _compute_vif(X)
            coef_table["VIF"] = vif.reindex(coef_table.index).values
            return {
                "model": res,
                "n": n,
                "k": k,
                "y_pred": y_pred,
                "llf": llf,
                "aic": aic,
                "bic": bic,
                "coef_table": coef_table,
                "statistic": float(res.fvalue),
                "p_value": float(res.f_pvalue),
                "regularized": False
            }
        except np.linalg.LinAlgError:
            if not self.regularize_fallback:
                raise
            # Ridge 폴백
            ridge = Ridge(alpha=1e-3, random_state=self.random_state)
            Xn = X.drop(columns=["const"]).to_numpy()
            ridge.fit(Xn, y.to_numpy())
            y_pred = ridge.predict(Xn)
            llf = _loglik_gaussian(y.to_numpy(), y_pred)
            k = X.shape[1]
            n = len(y)
            aic = _aic_from_loglik(llf, k)
            bic = _bic_from_loglik(llf, k, n)
            coef = np.concatenate([[ridge.intercept_], ridge.coef_])
            coef_table = pd.DataFrame({"Coef.": coef}, index=["const"] + list(X.columns.drop("const")))
            return {
                "model": ridge,
                "n": n,
                "k": k,
                "y_pred": y_pred,
                "llf": llf,
                "aic": aic,
                "bic": bic,
                "coef_table": coef_table,
                "statistic": None,
                "p_value": None,
                "regularized": True
            }

    def _fit_logit_binary(self, X: pd.DataFrame, y: pd.Series):
        try:
            try:
                res = sm.Logit(y, X).fit(disp=0, method="lbfgs", maxiter=self.max_iter)
            except (PerfectSeparationError, np.linalg.LinAlgError, ValueError):
                if not self.regularize_fallback:
                    raise
                res = sm.Logit(y, X).fit_regularized(alpha=1e-3, L1_wt=0.0, maxiter=self.max_iter)
            proba = res.predict(X).clip(1e-15, 1-1e-15)
            llf = float(res.llf)
            aic = float(res.aic)
            bic = float(res.bic)
            n = len(y)
            k = len(res.params)
            coef_table = res.summary2().tables[1].copy()
            vif = _compute_vif(X)
            coef_table["VIF"] = vif.reindex(coef_table.index).values
            return {
                "model": res,
                "n": n,
                "k": k,
                "y_proba": proba,
                "llf": llf,
                "aic": aic,
                "bic": bic,
                "coef_table": coef_table,
                "statistic": float(res.llr),
                "p_value": float(res.llr_pvalue),
                "regularized": False
            }
        except Exception as e:
            print(f"statsmodels Logit failed: {e}")
            clf = LogisticRegression(
                penalty="l2", solver="lbfgs", max_iter=self.max_iter, random_state=self.random_state
            )
            clf.fit(X, y.to_numpy())
            proba = clf.predict_proba(X)
            llf = _loglik_multinomial(y.to_numpy(), proba)
            n = len(y)
            K = len(np.unique(y))
            p = X.shape[1]
            k = (K - 1) * (p + 1)
            aic = _aic_from_loglik(llf, k)
            bic = _bic_from_loglik(llf, k, n)
            vif_series = _compute_vif(X)  # 별도 제공
            coef_table = pd.DataFrame({"VIF":[]})
            coef_table["VIF"] = vif_series
            return {
                "model": clf,
                "n": n,
                "k": k,
                "y_proba": proba,
                "llf": llf,
                "aic": aic,
                "bic": bic,
                "coef_table": coef_table,
                "statistic": float(res.llr),
                "p_value": float(res.llr_pvalue),
                "regularized": True
            }

    def _fit_multilogit(self, X: pd.DataFrame, y: pd.Series):
        Xn = X.drop(columns=["const"]).to_numpy()
        
        # 🔹 case 1: feature가 없을 때 (intercept-only model)
        if Xn.shape[1] == 0:
            value_counts = y.value_counts(normalize=True).sort_index()
            classes = np.unique(y)
            
            # 모든 샘플에 대해 클래스별 확률 = 데이터 분포
            proba = np.tile(value_counts.values, (len(y), 1))
            llf = _loglik_multinomial(y.to_numpy(), proba)
            k = len(classes) - 1   # intercept 수
            n = Xn.shape[0]
            aic = _aic_from_loglik(llf, k)
            bic = _bic_from_loglik(llf, k, n)
            
            # coef_table: intercept-only → class별 확률만 표시
            coef_table = pd.DataFrame([value_counts.values],
                                    columns=[f"class={cls}" for cls in classes],
                                    index=["intercept"])
            
            pred = np.repeat(value_counts.idxmax(), len(y))
            logloss_val = float(log_loss(y, proba))
            
            return {
                "model": None,
                "n": n,
                "k": k,
                "aic": aic,
                "bic": bic,
                "llf": llf,
                "coef_table": coef_table,
                "logloss": logloss_val,
                "y_proba": None,
                "y_pred": pred,
                "regularized": False,
            }
        
        # 🔹 case 2: feature가 하나 이상 있을 때 (원래 코드)
        clf = LogisticRegression(
            penalty="l2", solver="lbfgs", multi_class="multinomial",
            max_iter=self.max_iter, random_state=self.random_state
        )
        clf.fit(Xn, y.to_numpy())
        proba = clf.predict_proba(Xn)
        pred = clf.predict(Xn)
        llf = _loglik_multinomial(y.to_numpy(), proba)
        # K = len(np.unique(y))
        # p = Xn.shape[1]
        # k = (K - 1) * (p + 1)
        k = clf.coef_.size + 1 # coef의 크기 + 절편
        n = Xn.shape[0]
        aic = _aic_from_loglik(llf, k)
        bic = _bic_from_loglik(llf, k, n)

        rows = []
        for i, cls in enumerate(clf.classes_):
            rows.append(pd.Series(
                np.concatenate([clf.intercept_[i:i+1], clf.coef_[i]]),
                index=["const"] + list(X.columns.drop("const")),
                name=f"class={cls}"
            ))
        coef_table = pd.DataFrame(rows)

        logloss_val = float(log_loss(y, proba))
        # acc = float(accuracy_score(y, pred))
        # vif_series = _compute_vif(X)  # 별도 제공

        # pred_df = pd.DataFrame({
        #     "y": y.values,
        #     "y_pred": pred,
        #     "y_proba_max": proba.max(axis=1)
        # }, index=y.index)

        return {
            "model": clf,
            "n": n,
            "k": k,
            "aic": aic,
            "bic": bic,
            "llf": bic,
            "coef_table": coef_table,
            "logloss": logloss_val,
            # "accuracy": acc,
            # "vif": vif_series,
            # "pred_df": pred_df,
            "y_proba": proba,
            "y_pred": pred,
            "regularized": True,
        }

    def _fit_any(self, X: pd.DataFrame, y: pd.Series):
        if self.model_type == "linear":
            return self._fit_linear(X, y)
        elif self.model_type == "logit":
            return self._fit_logit_binary(X, y)
        elif self.model_type == "multilogit":
            return self._fit_multilogit(X, y)
        else:
            raise ValueError("unsupported model_type")

    # ---------- helpers ----------
    def _expand_units(self, unit_labels: List[str]) -> List[str]:
        """그룹/단일 유닛 라벨 리스트 -> 실제 열 이름 리스트(원래 X 컬럼 순서 보존)"""
        want_cols = set()
        for u in unit_labels:
            want_cols.update(self.units_map[u])
        return [c for c in self.X_in.columns if c in want_cols]

    def _record_history(self, step_idx: int, action: str,
                        unit_labels: List[str], fit_res: Dict, trial: bool=False):
        rec = {
            "step": step_idx,
            "action": action,                 # 예: forward-add:day, backward-drop:smoker
            "selected_units": list(unit_labels),
            "variables": self._expand_units(unit_labels),
            "aic": float(fit_res["aic"])
        }
        if self.model_type == "linear":
            rec.update({"rmse": fit_res.get("rmse"), "r2": fit_res.get("r2"), "adj_r2": fit_res.get("adj_r2")})
        else:
            rec.update({"logloss": fit_res.get("logloss"), "accuracy": fit_res.get("accuracy")})
        if trial and not self.track_all_trials:
            return
        self.history_.append(rec)

    def get_history_df(self) -> pd.DataFrame:
        """ 변수선택 히스토리 반환 """
        if not self.history_:
            return pd.DataFrame()
        df = pd.DataFrame(self.history_)
        cols = ["step","action","variables","aic","bic"]
        df_hist = df[[c for c in cols if c in df.columns]].copy()
        df_hist.loc[len(df_hist)-1, 'action'] = 'stop'
        df_hist['best'] = ''
        df_hist.loc[len(df_hist)-2, 'best'] = '☆'
        df_hist['variables'] = df_hist['variables'].astype(str)
        return df_hist

    # ---------- selection (group-aware, best snapshot + post-best 기록) ----------
    def select(self, record_post_best: bool = True) -> Dict:
        """ 선택한 옵션에 해당하는 변수 선택 진행 """
        units_all = list(self.units_map.keys())
        selected_units: List[str] = []
        candidates_units: List[str] = units_all.copy()

        best_aic = np.inf
        best_fit: Optional[Dict] = None
        best_units: List[str] = []
        step_idx = 0

        def fit_units(units: List[str]):
            cols = self._expand_units(units)
            Xsub = self.X[["const"] + cols]
            return self._fit_any(Xsub, self.y)

        # post-best 1스텝 기록(차트 꺾임 위해)
        def _record_post_best_forward():
            nonlocal step_idx
            if not candidates_units: return
            trials = []
            for u in candidates_units:
                fit = fit_units(selected_units + [u])
                trials.append((fit["aic"], u, fit))
            _, u_next, fit_next = sorted(trials, key=lambda x: x[0])[0]
            step_idx += 1
            self._record_history(step_idx, f"post-best-add:{u_next}",
                                 selected_units + [u_next], fit_next, trial=False)

        def _record_post_best_backward():
            nonlocal step_idx
            if not selected_units: return
            trials = []
            for u in selected_units:
                cols_units = [x for x in selected_units if x != u]
                fit = fit_units(cols_units)
                trials.append((fit["aic"], u, fit, cols_units))
            _, u_next, fit_next, cols_units = sorted(trials, key=lambda x: x[0])[0]
            step_idx += 1
            self._record_history(step_idx, f"post-best-drop:{u_next}", cols_units, fit_next, trial=False)

        def _record_post_best_stepwise():
            nonlocal step_idx
            trials = []
            for u in candidates_units:
                trials.append(("add", u, fit_units(selected_units + [u])))
            for u in selected_units:
                cols_units = [x for x in selected_units if x != u]
                trials.append(("drop", u, fit_units(cols_units)))
            if not trials: return
            act, u, fit_next = sorted(trials, key=lambda t: t[2]["aic"])[0]
            new_units = (selected_units + [u]) if act == "add" else [x for x in selected_units if x != u]
            step_idx += 1
            self._record_history(step_idx, f"post-best-{act}:{u}", new_units, fit_next, trial=False)

        # forward/backward/stepwise 본체
        if self.method is None:
            selected_units = units_all.copy()
            candidates_units = []
            base = fit_units(selected_units) if selected_units else fit_units([])
            best_aic, best_fit = base["aic"], base
            best_units = selected_units.copy()
            step_idx += 1
            self._record_history(step_idx, "start-full", selected_units, base, trial=False)
        if self.method == "forward":
            improved = True
            while improved and candidates_units:
                improved = False
                trials = []
                for u in list(candidates_units):
                    fit = fit_units(selected_units + [u])
                    trials.append((fit["aic"], u, fit))
                    self._record_history(step_idx, f"trial-add:{u}",
                                         selected_units + [u], fit, trial=True)
                if trials:
                    trials.sort(key=lambda x: x[0])
                    aic_new, u_new, fit_new = trials[0]
                    if aic_new + 1e-8 < best_aic:
                        best_aic, best_fit = aic_new, fit_new
                        selected_units.append(u_new); candidates_units.remove(u_new)
                        best_units = selected_units.copy()
                        step_idx += 1
                        self._record_history(step_idx, f"forward-add:{u_new}",
                                             selected_units, fit_new, trial=False)
                        improved = True
            if record_post_best: _record_post_best_forward()

        elif self.method == "backward":
            selected_units = units_all.copy()
            candidates_units = []
            base = fit_units(selected_units) if selected_units else fit_units([])
            best_aic, best_fit = base["aic"], base
            best_units = selected_units.copy()
            step_idx += 1
            self._record_history(step_idx, "start-full", selected_units, base, trial=False)

            improved = True
            while improved and selected_units:
                improved = False
                trials = []
                for u in list(selected_units):
                    cols_units = [x for x in selected_units if x != u]
                    fit = fit_units(cols_units)
                    trials.append((fit["aic"], u, fit, cols_units))
                    self._record_history(step_idx, f"trial-drop:{u}", cols_units, fit, trial=True)
                trials.sort(key=lambda x: x[0])
                aic_new, u_drop, fit_new, cols_units = trials[0]
                if aic_new + 1e-8 < best_aic:
                    best_aic, best_fit = aic_new, fit_new
                    selected_units = cols_units
                    candidates_units.append(u_drop)
                    best_units = selected_units.copy()
                    step_idx += 1
                    self._record_history(step_idx, f"backward-drop:{u_drop}",
                                         selected_units, fit_new, trial=False)
                    improved = True
            if record_post_best: _record_post_best_backward()

        else:  # stepwise
            improved = True
            while improved:
                improved = False
                # forward
                f_trials = []
                for u in list(candidates_units):
                    fit = fit_units(selected_units + [u])
                    f_trials.append((fit["aic"], u, fit))
                    self._record_history(step_idx, f"trial-add:{u}",
                                         selected_units + [u], fit, trial=True)
                if f_trials:
                    f_trials.sort(key=lambda x: x[0])
                    faic, fu, ffit = f_trials[0]
                    if faic + 1e-8 < best_aic:
                        best_aic, best_fit = faic, ffit
                        selected_units.append(fu); candidates_units.remove(fu)
                        best_units = selected_units.copy()
                        step_idx += 1
                        self._record_history(step_idx, f"forward-add:{fu}",
                                             selected_units, ffit, trial=False)
                        improved = True

                # backward
                b_trials = []
                for u in list(selected_units):
                    cols_units = [x for x in selected_units if x != u]
                    fit = fit_units(cols_units)
                    b_trials.append((fit["aic"], u, fit, cols_units))
                    self._record_history(step_idx, f"trial-drop:{u}", cols_units, fit, trial=True)
                if b_trials:
                    b_trials.sort(key=lambda x: x[0])
                    baic, bu, bfit, cols_units = b_trials[0]
                    if baic + 1e-8 < best_aic:
                        best_aic, best_fit = baic, bfit
                        selected_units = cols_units
                        candidates_units.append(bu)
                        best_units = selected_units.copy()
                        step_idx += 1
                        self._record_history(step_idx, f"backward-drop:{bu}",
                                             selected_units, bfit, trial=False)
                        improved = True
            if record_post_best: _record_post_best_stepwise()

        # 최종(최적 조합)
        if best_fit is None:
            best_fit = fit_units(best_units)

        cols_final = self._expand_units(best_units)
        if self.model_type == "linear":
            self.y.name = 'y'
            best_fit['y_pred'].name = 'y_pred'
            return {
                "model": best_fit["model"],
                "model_type": self.model_type,
                "variables": cols_final,
                "equation": f"y ~ {' + '.join(cols_final) if cols_final else '1 (intercept only)'}",
                "x": self.X,
                "y": self.y,
                "y_pred": best_fit['y_pred'],
                "model_info": {
                    "n": best_fit["n"],
                    "k": best_fit["k"],
                    "statistic": best_fit["statistic"],
                    "p_value": best_fit["p_value"]
                },
                "coef_table": best_fit["coef_table"].rename(columns={
                    "[0.025":"95% 신뢰하한",
                    "0.975]":"95% 신뢰상한",
                    "Coef.": "Coef",
                    "Std.Err.": "Std Err"
                }),
                "metrics": {
                    "llf": best_fit["llf"],
                    "aic": best_fit["aic"],
                    "bic": best_fit["bic"]
                }
            }
        elif self.model_type == "logit":
            self.y.name = 'y'
            best_fit['y_proba'].name = 'y_proba'
            return {
                "model": best_fit["model"],
                "model_type": self.model_type,
                "variables": cols_final,
                "equation": f"y ~ {' + '.join(cols_final) if cols_final else '1 (intercept only)'}",
                "x": self.X,
                "y": self.y,
                "y_proba": best_fit['y_proba'],
                "model_info": {
                    "n": best_fit["n"],
                    "k": best_fit["k"],
                    "statistic": best_fit.get("statistic", None),
                    "p_value": best_fit.get("p_value", None)
                },
                "coef_table": best_fit["coef_table"].rename(columns={
                    "[0.025":"95% 신뢰하한",
                    "0.975]":"95% 신뢰상한",
                    "Coef.": "Coef",
                    "Std.Err.": "Std Err"
                }),
                "metrics": {
                    "llf": best_fit["llf"],
                    "aic": best_fit["aic"],
                    "bic": best_fit["bic"]
                }
            }
        elif self.model_type == "multilogit":
            self.y.name = 'y'
            return {
                "model": best_fit["model"],
                "model_type": self.model_type,
                "variables": cols_final,
                "equation": f"y ~ {' + '.join(cols_final) if cols_final else '1 (intercept only)'}",
                "x": self.X,
                "y": self.y,
                "y_proba": pd.DataFrame(best_fit['y_proba']),
                "y_pred": pd.Series(best_fit['y_pred'], name='y_pred'),
                "model_info": {
                    "n": best_fit["n"],
                    "k": best_fit["k"],
                    "logloss": best_fit["logloss"]
                },
                "coef_table": best_fit["coef_table"],
                "metrics": {
                    "llf": best_fit["llf"],
                    "aic": best_fit["aic"],
                    "bic": best_fit["bic"]
                }
            }
            
        # info = {
        #     "model_type": self.model_type,
        #     "selected_units": best_units,
        #     "variables": cols_final,
        #     "aic": float(best_fit["aic"]),
        #     "equation_units": f"y ~ {' + '.join(best_units) if best_units else '1 (intercept only)'}",
        #     "equation": f"y ~ {' + '.join(cols_final) if cols_final else '1 (intercept only)'}",
        #     "coef_table": best_fit["coef_table"].rename(columns={
        #         "[0.025":"95% 신뢰하한",
        #         "0.975]":"95% 신뢰상한",
        #         "Coef.": "Coef",
        #         "Std.Err.": "Std Err"
        #     }),
        #     "log_likelihood": float(best_fit["llf"]),
        #     "notes": []
        # }
        # if self.model_type == "linear":
        #     info.update({"rmse": best_fit.get("rmse"),
        #                  "r2": best_fit.get("r2"),
        #                  "adj_r2": best_fit.get("adj_r2"),
        #                  "p_value": best_fit.get("f_pvalue", "")})
        # else:
        #     info.update({"logloss": best_fit.get("logloss"),
        #                  "accuracy": best_fit.get("accuracy"),
        #                  "p_value": best_fit.get("llr_pvalue", ""),
        #                  "adj_r2": best_fit.get("adj_r2", "")})
        # if self.model_type == "multilogit" and "vif" in best_fit:
        #     info["vif"] = best_fit["vif"]
        # info["predictions"] = best_fit.get("pred_df")
        # info["multi_pred_proba"] = best_fit.get("multi_proba", None)
        # self.final_info_ = info
        # self.final_fit_ = best_fit["model"]
        # self.final_cols_ = ["const"] + cols_final
        # self.final_units_ = best_units
        # return info
