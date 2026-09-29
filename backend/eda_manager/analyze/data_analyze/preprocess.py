# pylint: disable=W0718, E1101, C0413, C0103, C0321, C0301
"""
회귀분석 전처리 클래스
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, OneHotEncoder

class Preprocessor:
    """ 회귀분석 진행 전 데이터 전처리 클래스  """
    def __init__(self, num_cols=None, cat_cols=None, scaler="standard", impute="remove", drop_first=True):
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.scaler_type = scaler
        self.impute = impute
        self.drop_first = drop_first

        # 스케일러 선택
        if scaler == "standard":
            self.scaler = StandardScaler()
        elif scaler == "minmax":
            self.scaler = MinMaxScaler()
        elif scaler == "robust":
            self.scaler = RobustScaler()
        elif scaler == "maxabs":
            self.scaler = MaxAbsScaler()
        elif scaler is None:
            self.scaler = None
        else:
            raise ValueError("Unsupported scaler. Use 'standard', 'minmax', 'robust', or None.")

        self.ohe = OneHotEncoder(drop="first" if drop_first else None, sparse_output=False)
        self.group_map = {}
        self.fitted = False

        # y 변환용
        self.label_encoder = None
        self.y_was_encoded = False

    def _impute(self, X: pd.DataFrame):
        X = X.replace([np.inf, -np.inf], np.nan)
        if self.impute == "remove":
            return X.dropna()
        elif self.impute == "mean":
            return X.fillna(X.mean())
        elif self.impute == "median":
            return X.fillna(X.median())
        elif self.impute == "mode":
            return X.fillna(X.mode().iloc[0])
        elif self.impute == "linear":
            return X.interpolate(method="linear").fillna(method="bfill").fillna(method="ffill")
        else:
            raise ValueError("Unsupported impute option.")

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        """ Train Data 전처리 """
        X = self._impute(X)
        y = y[X.index]

        if self.num_cols and self.scaler:
            self.scaler.fit(X[self.num_cols])

        if self.cat_cols:
            self.ohe.fit(X[self.cat_cols])
            for c in self.cat_cols:
                cols = [col for col in self.ohe.get_feature_names_out() if col.startswith(c)]
                self.group_map[c] = cols

        if y is not None:
            if y.dtype == "O" or y.dtype.name == "category":  # 문자열 또는 카테고리
                self.label_encoder = LabelEncoder()
                self.label_encoder.fit(y)
                self.y_was_encoded = True

        self.fitted = True
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series = None):
        """ fit된 전처리 메소드로 Train Set 변환 """
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fit before transform.")
        X = self._impute(X)
        y = y[X.index]
        dfs = []

        if self.num_cols:
            if self.scaler:
                X_num = pd.DataFrame(self.scaler.transform(X[self.num_cols]),
                                     columns=self.num_cols, index=X.index)
            else:
                X_num = X[self.num_cols].copy()
            dfs.append(X_num)

        if self.cat_cols:
            X_cat = pd.DataFrame(self.ohe.transform(X[self.cat_cols]),
                                 columns=self.ohe.get_feature_names_out(self.cat_cols),
                                 index=X.index)
            dfs.append(X_cat)

        X_out = pd.concat(dfs, axis=1)

        if y is not None and self.label_encoder:
            y_out = self.label_encoder.transform(y)
            if len(np.unique(y)) <= 2:
                y_out = pd.Series(y_out, index=y.index)
            # logit일 때랑 mutli일때 비교
            
        else:
            y_out = y

        return X_out, y_out

    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None):
        """ Fit, Transform 한번에 진행 """
        self.fit(X, y)
        return self.transform(X, y)

    def inverse_transform_y(self, y_encoded):
        """숫자형 라벨을 원래 문자열 라벨로 복원"""
        if self.label_encoder:
            return self.label_encoder.inverse_transform(y_encoded)
        else:
            return y_encoded
