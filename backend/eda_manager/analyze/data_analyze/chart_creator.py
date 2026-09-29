"""
Data Analysis 내 차트 생성 헬퍼
"""

from typing import Dict, List
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.pyplot import Axes
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    RocCurveDisplay, PrecisionRecallDisplay    
)
from eda_manager.chart.chart_helper import formatter_kmb, close_pyplot, save_chart_to_file
from fonts import get_project_font

FONT_GOTHIC_PATH, FONT_DREAM_PATH = get_project_font()

matplotlib.use("agg")
DBGOTHIC = fm.FontProperties(fname=FONT_GOTHIC_PATH)
DBDREAM = fm.FontProperties(fname=FONT_DREAM_PATH, size=15, weight='bold')
fm.fontManager.addfont(FONT_GOTHIC_PATH)
fm.fontManager.addfont(FONT_DREAM_PATH)

plt.rcParams['font.family'] = DBGOTHIC.get_name()
plt.rcParams['axes.unicode_minus'] = False

def _set_chart_title(ax: Axes, title: str):
    """ 차트 제목 설정

    Args:
        ax (Axes): axis
        chart_nm (str): 차트 종류
    """
    ax.set_title(label=title, fontdict=dict(fontproperties=DBDREAM))

def _set_chart_x_label(ax: Axes, x_label: str, is_tick_set: bool=True):
    """ 차트 x축 라벨 설정

    Args:
        ax (Axes): axis
        value_cnt (int): 값 개수
    """
    ax.set_xlabel(x_label, fontdict=dict(fontweight='bold'))
    if is_tick_set:
        xticks = ax.get_xticks()
        if len(xticks) > 15:
            step = len(xticks) // 15
            ax.set_xticks(xticks[::step])
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        else:
            ax.set_xticks(xticks)

def _set_axis_kmb_formatter(ax: Axes):
    """ X, Y축 kml 포맷 적용 """
    min_val, max_val = ax.get_ylim()
    if max_val - min_val > 1_000:
        ax.yaxis.set_major_formatter(FuncFormatter(formatter_kmb))
    min_val, max_val = ax.get_xlim()
    if max_val - min_val > 1_000:
        ax.xaxis.set_major_formatter(FuncFormatter(formatter_kmb))

# ---------- plotting (노란 ⭐ + 정수 tick + post-best 표시) ----------
def plot_aic_history(df_hist: pd.DataFrame, save_path: str):
    """ 변수 선택 히스토리 시각화 """
    is_save = False
    try:
        metric = 'aic'
        if metric not in df_hist.columns:
            raise ValueError(f"'{metric}' 기록이 없습니다.")

        y = df_hist[metric].astype(float)
        x = np.arange(1, len(y)+1)

        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(x, y, marker="o")

        # 최적 지점
        if metric in ["aic","logloss","rmse"]:
            best_pos = int(np.argmin(y.values))
        else:
            best_pos = int(np.argmax(y.values))
        best_x = x[best_pos]
        best_y = y.iloc[best_pos]

        # 노란 별 + 값 주석
        ax.scatter(best_x, best_y, color="gold", marker="*", s=250,
                edgecolor="black", zorder=5, label="best")
        label_txt = f"step={best_x}, {metric}={best_y:.4f}"
        ax.annotate(label_txt, (best_x, best_y), textcoords="offset points", xytext=(0,10),
                        ha="center", fontsize=10, color="black", weight="bold")

        # 마지막 점이 post-best-*이면 회색 X로 구분
        if len(y) >= 2:
            last_action = df_hist.iloc[-1]["action"]
            if isinstance(last_action, str) and last_action == 'stop':
                ax.scatter(x[-1], y.iloc[-1], marker="X", s=80, color="gray", zorder=4)

        _set_chart_title(ax, f"{metric.upper()} by step")
        ax.set_xticks(np.arange(1, len(y)+1, 1))  # 정수 tick 강제
        _set_chart_x_label(ax, 'Step')
        ax.set_ylabel(metric.upper())
        _set_axis_kmb_formatter(ax)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_vif_score(df_coeff: pd.DataFrame, save_path: str):
    """ 독립변수 VIF 점수 시각화 """
    is_save = False
    try:
        vif = df_coeff['VIF'].sort_values(ascending=True).dropna()
        colors = ['#a6cee3' if value < 10 else '#1f78b4' for value in vif]
        hatches = ['' if value < 10 else '//' for value in vif]
        fig, ax = plt.subplots()
        bars = ax.barh(vif.index, vif, color=colors)
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)
        ax.bar_label(bars, fmt=lambda x: f"{x:,.2f}")
        ax.axvline(10, 0, 1, linestyle='--', c='red')
        ax.text(10, 0, ' 10 →')
        ax.set_xlabel('VIF Score')
        _set_chart_title(ax, f"독립변수 VIF Score")
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_predict_scatter(y: pd.Series, y_pred: pd.Series, save_path: str):
    """ 실제값 vs 예측값 시각화(scatter)"""
    is_save = False
    try:
        fig, ax = plt.subplots(figsize=(16,9))
        ax.scatter(y, y_pred, alpha=0.8)
        _set_chart_title(ax, "실제값 vs 예측값(산점도)")
        _set_chart_x_label(ax, '실제값(y)', is_tick_set=False)
        ax.set_ylabel('예측값(y^)')
        _set_axis_kmb_formatter(ax)
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_predict_box(y: pd.Series, y_pred: pd.Series, save_path: str):
    """ 실제값 vs 예측값 시각화(scatter)"""
    is_save = False
    try:
        df_predict = pd.concat([pd.Series(y, name='y'), pd.Series(y_pred, name='y_pred')], axis=1)
        fig, ax = plt.subplots(figsize=(16,9))
        sns.boxplot(df_predict.sort_values('y'), x='y', y='y_pred', fill=False, ax=ax)
        _set_chart_title(ax, "실제값 vs 예측값(Box Plot)")
        _set_chart_x_label(ax, '실제값(y)')
        ax.set_ylabel('예측값(y^)')
        _set_axis_kmb_formatter(ax)
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_predict_order(y: pd.Series, y_pred: pd.Series, save_path: str):
    """ 실제값 vs 예측값 시각화 """
    is_save = False
    try:
        fig, ax = plt.subplots(figsize=(16,5))
        ax.plot(range(len(y)), y, 'o--', label='실제값(y)', alpha=0.7)
        ax.plot(range(len(y_pred)), y_pred, 'o--', label='예측값(y^)', alpha=0.7)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        _set_chart_title(ax, "실제값 vs 예측값")
        _set_chart_x_label(ax, '실제값(y)')
        ax.set_ylabel('예측값(y^)')
        _set_axis_kmb_formatter(ax)
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_reg_result_by_indep_var(
    X: pd.DataFrame, y: pd.Series,
    vars: List[str], coef_table: List[Dict[str,object]], save_path: str):
    """ 독립 변수 별 회귀식 시각화 """
    is_save = False
    try:
        n_col = 3
        n_row = len(vars) // n_col
        h = 3*n_row
        fig, ax = plt.subplots(ncols=n_col, nrows=n_row, figsize=(10,h), sharey=True)
        for i, var in enumerate(vars):
            i_col = i % n_col
            i_row = i // n_col
            idx = vars.index(var)
            coef_values = [0 for _ in range(len(vars))]
            const_info = [coef_info['Coef'] for coef_info
                          in coef_table if coef_info['Coef Name']=='const']
            const = const_info.pop() if len(const_info)>0 else 0
            coef = [coef_info['Coef'] for coef_info in coef_table
                    if coef_info['Coef Name']==var].pop()
            coef_values[idx] = coef
            var_x_data = X[var]
            var_fit_data = const + coef * var_x_data
            ax[i_row, i_col].plot(var_x_data, var_fit_data,
                                  c='r', label=f'y^ = [{const:.2f}] + [{coef:.2f}]{var}')
            ax[i_row, i_col].scatter(var_x_data, y, label='y', alpha=.5)
            ax[i_row, i_col].set_title(var)
            ax[i_row, i_col].legend()
            _set_axis_kmb_formatter(ax[i_row, i_col])
        fig.suptitle('독립변수 별 회귀식', fontdict=dict(fontproperties=DBDREAM))
        fig.tight_layout()
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_confusion_matrix(y: pd.Series, y_pred: pd.Series, class_nms: List[str], save_path: str):
    """ 분류 결과 혼동행렬 """
    is_save = False
    try:
        cm = confusion_matrix(y, y_pred)
        fig, ax = plt.subplots()
        # disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_nms, ax=ax)
        ConfusionMatrixDisplay.from_predictions(y_true=y, y_pred=y_pred, display_labels=class_nms, ax=ax, cmap='Blues')
        # disp.plot(cmap="Blues")
        # plt.title("Confusion Matrix")
        _set_chart_title(ax, "Confusion Matrix")
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_roc_curve(fpr: np.ndarray, tpr: np.ndarray,
                   auc_roc: float, pos_label: int,
                   opt_fpr: float, opt_tpr: float, opt_thr: float, save_path: str):
    """ ROC Curve """
    is_save = False
    try:
        fig, ax = plt.subplots()
        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc_roc, pos_label=pos_label)
        display.plot(ax=ax)
        ax.fill_between(fpr, tpr, alpha=0.2, label='AUC')
        ax.plot([0, opt_fpr], [opt_tpr]*2, color='gray', ls='--', alpha=0.4)
        ax.plot([opt_fpr]*2, [0, opt_tpr], color='gray', ls='--', alpha=0.4)
        ax.scatter([opt_fpr], [opt_tpr], c='r', label='Optimal Point', zorder=10)
        ax.annotate(text=f"임계값: {opt_thr:.2f}\n(fpr: {opt_fpr:.2f}, tpr: {opt_tpr:.2f})", 
                    xy=(opt_fpr, opt_tpr),
                    xytext=[0.6,0.4],
                    bbox=dict(boxstyle='round', pad=0.4, fc='wheat', alpha=0.4),
                    arrowprops=dict(arrowstyle='->'),
                    ha='center')
        ax.plot([0,1],[0,1], ls='--', label='Random')
        ax.legend()
        _set_chart_title(ax, "ROC Curve")
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

def plot_pr_curve(precisions: np.ndarray, recalls: np.ndarray, f1_scores: np.ndarray,
                  auc_pr: float, pos_label: int,
                  opt_recall: float, opt_precision: float, opt_f1_score, opt_thr: float,
                  save_path: str                  
                  ):
    try:
        fig, ax = plt.subplots()
        display = PrecisionRecallDisplay(precision=precisions, recall=recalls,
                                         pos_label=pos_label, average_precision=auc_pr,
                                         estimator_name='Logistic Regression')
        display.plot(ax=ax)
        ax.fill_between(recalls, precisions, alpha=0.2, label='AUC')
        ax.plot([0, opt_recall], [opt_precision]*2, color='gray', ls='--', alpha=0.4)
        ax.plot([opt_recall]*2, [0, opt_precision], color='gray', ls='--', alpha=0.4)
        ax.plot(recalls, f1_scores, label='F1 Score')
        ax.scatter([opt_recall], [opt_precision], c='r', label='Optimal Point', zorder=10)
        ax.annotate(text=f"임계값: {opt_thr:.2f} (F1 Score: {opt_f1_score:.2f})\n(Recall: {opt_recall:.2f}, Precision: {opt_precision:.2f})",
                    xy=(opt_recall, opt_precision),
                    xytext=[0.6,0.4],
                    bbox=dict(boxstyle='round', pad=0.4, fc='wheat', alpha=0.4),
                    arrowprops=dict(arrowstyle='->'),
                    ha='center')
        ax.legend(loc='lower right')
        _set_chart_title(ax, "Precision Recall Curve")
        is_save = save_chart_to_file(fig, save_path)
    except Exception as e:
        print(e)
    close_pyplot()
    return is_save

# def plot_roc_curve(y: pd.Series, y_prob: np.ndarray, save_path: str):
#     is_save = False
#     try:
#         if y_prob is not None:
#             try:
#                 if y_prob.ndim == 1 or y_prob.shape[1] == 2:  # 이진 분류
#                     y_prob_binary = y_prob[:,1] if y_prob.ndim > 1 else y_prob
#                     fpr, tpr, _ = roc_curve(y, y_prob_binary)
#                     roc_auc = auc(fpr, tpr)

#                     fig, ax = plt.subplots()
#                     ax.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
#                     ax.plot([0,1],[0,1], "k--")
#                     ax.set_xlabel("False Positive Rate")
#                     ax.set_ylabel("True Positive Rate")
#                     _set_chart_title(ax, "ROC Curve")
#                     ax.legend(loc="lower right")
#                     is_save = save_chart_to_file(fig, save_path)
#                 else:  # 다중 분류 → micro-average
#                     from sklearn.preprocessing import label_binarize
#                     y_bin = label_binarize(y, classes=np.arange(y_prob.shape[1]))
#                     fpr, tpr, _ = roc_curve(y_bin.ravel(), y_prob.ravel())
#                     roc_auc = auc(fpr, tpr)

#                     fig, ax = plt.subplots()
#                     ax.plot(fpr, tpr, label=f"micro-average ROC (AUC = {roc_auc:.2f})", color="blue")
#                     ax.plot([0,1],[0,1], "k--")
#                     ax.set_xlabel("False Positive Rate")
#                     ax.set_ylabel("True Positive Rate")
#                     _set_chart_title(ax, "Multiclass ROC Curve (micro-average)")
#                     ax.legend(loc="lower right")
#                     is_save = save_chart_to_file(fig, save_path)
#             except Exception as e:
#                 print("ROC Curve 계산 불가:", e)
#     except Exception as e:
#         print(e)
#     close_pyplot()
#     return is_save
