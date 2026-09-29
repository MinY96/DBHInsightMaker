# pylint: disable=W0718
"""
Data 변환 클래스
"""

import random
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler

class Converter:
    """데이터 변환, 생성 관련 메소드 집합"""

    @classmethod
    def random_integer_data(cls, data_size: int, min_val: int, max_val: int):
        """ 정수 타입 난수 생성 """
        min_val, max_val = int(min_val), int(max_val)
        return [random.randint(min_val, max_val) for _ in range(data_size)]

    @classmethod
    def random_float_data(cls, data_size: int, min_val: float, max_val: float):
        """ 실수 타입 난수 생성 """
        return [random.uniform(min_val, max_val) for _ in range(data_size)]

    @classmethod
    def random_interger_norm_data(cls, data_size: int, min_val: int, max_val: int,
                                  mean_val: float, std_val: float):
        """ 정수 타입 정규 분포 만족하는 난수 생성 """
        min_val, max_val = int(min_val), int(max_val)
        random_data = np.random.normal(mean_val, std_val, data_size)
        random_data = np.clip(np.round(random_data).astype(int), min_val, max_val)
        return random_data.tolist()

    @classmethod
    def random_float_norm_data(cls, data_size:  int, min_val: float, max_val: float,
                               mean_val: float, std_val: float):
        """ 실수 타입 정규 분포 만족하는 난수 생성 """
        random_data = np.random.normal(mean_val, std_val, data_size)
        random_data = np.clip(random_data, min_val, max_val)
        return random_data.tolist()

    @classmethod
    def calc_numerical_data(cls, data: pd.Series, operation: str, operand: float):
        """ 수치형 데이터 연산 """
        if operation == 'add':
            return (data + operand).tolist()
        elif operation == 'subtract':
            return (data - operand).tolist()
        elif operation == 'multiply':
            return (data * operand).tolist()
        elif operation == 'devide':
            if operand == 0:
                raise ValueError("Division by zero is not allowed.")
            return (data / operand).tolist()
        elif operation == 'power':
            return (data ** operand).tolist()
        raise ValueError(f"Unsupported operation: {operation}")

    @classmethod
    def calc_categorical_data(cls, data: pd.Series, operation: str):
        """ 범주형 데이터 연산 """
        if operation == 'upper':
            return (data.str.upper()).tolist()
        elif operation == 'lower':
            return (data.str.lower()).tolist()
        elif operation == 'capital':
            return (data.str.capitalize()).tolist()
        elif operation == 'strip':
            return (data.str.strip()).tolist()
        raise ValueError(f"Unsupported operation for categorical data: {operation}")

    @classmethod
    def calc_categorical_data_split(cls, data: pd.Series, split_text: str, split_order: int):
        """ 범주형 데이터 분할 후 특정 부분 추출 """
        return data.str.split(split_text, expand=True)[split_order-1].tolist()

    @classmethod
    def calc_categorical_data_replace(cls, data: pd.Series, old: str, new: str):
        """ 범주형 데이터 특정 문자열 치환 """
        return data.str.replace(old, new).tolist()

    @classmethod
    def calc_categorical_data_concatenate(cls, data: pd.Series, concat_text: str, is_prev: bool):
        """ 범주형 데이터 특정 문자열 연결 """
        if is_prev:
            return (concat_text + data).tolist()
        return (data + concat_text).tolist()

    @classmethod
    def calc_function_data(cls, data: pd.Series, func: str):
        """ 수치형 데이터 함수 연산 """
        if func == 'abs':
            return np.abs(data).to_list()
        elif func == 'root':
            return np.sqrt(data).to_list()
        elif func == 'log':
            return np.log(data).to_list()
        elif func == 'exp':
            return np.exp(data).to_list()
        elif func == 'sin':
            return np.sin(data).to_list()
        elif func == 'cos':
            return np.cos(data).to_list()
        raise ValueError(f"Unsupported function for numerical data: {func}")

    @classmethod
    def combi_numerical_data(cls, data_first: pd.Series, data_second: pd.Series, operation: str):
        """ 수치형 변수 조합 """
        if operation == 'add':
            return (data_first + data_second).to_list()
        elif operation == 'subtract':
            return (data_first - data_second).tolist()
        elif operation == 'multiply':
            return (data_first * data_second).tolist()
        elif operation == 'devide':
            return (data_first / data_second).tolist()
        elif operation == 'min':
            return np.min([data_first, data_second], axis=0).tolist()
        elif operation == 'max':
            return np.max([data_first, data_second], axis=0).tolist()
        raise ValueError(f"Unsupported operation: {operation}")

    @classmethod
    def combi_categorical_data(cls, data_first: pd.Series, data_second: pd.Series, operation: str):
        """ 범주형 변수 조합 """
        if operation == 'concat':
            return (data_first + data_second).to_list()
        raise ValueError(f"Unsupported operation: {operation}")

    @classmethod
    def combi_datetime_data(cls, dt_first: pd.Series, dt_second: pd.Series,
                            operation: str, timedelta_type: str):
        """ 범주형 변수 조합 """
        if operation == 'diff':
            total_seconds = (dt_first - dt_second).dt.total_seconds()
            match timedelta_type:
                case 'year':
                    return (total_seconds // (365*24*60*60)).to_list()
                case 'month':
                    return (total_seconds // (30*24*60*60)).to_list()
                case 'day':
                    return (total_seconds // (24*60*60)).to_list()
                case 'hour':
                    return (total_seconds // (60*60)).to_list()
                case 'minute':
                    return (total_seconds // 60).to_list()
                case 'second':
                    return (total_seconds).to_list()
        raise ValueError(f"Unsupported operation: {operation}")

    @classmethod
    def outlier_sigma_data(cls, data: pd.Series, mean_val: float,
                           sigma_val: float, sigma_level: float):
        """ Sigma 기준 이상치 판정 """
        return (data>mean_val+sigma_level*sigma_val) | (data<mean_val-sigma_level*sigma_val)

    @classmethod
    def outlier_iqr_data(cls, data: pd.Series, q1: float, q3: float):
        """ IQR 기준 이상치 판정 """
        iqr = q3 - q1
        return (data>q3+1.5*iqr) | (data<q1-1.5*iqr)

    @classmethod
    def outlier_replace_data(cls, data: pd.Series, outlier_mask: pd.Series,
                             method: str, rep_value: float):
        """ 이상치 판정 값 대체 """
        na_mask = data.isna()
        if method in ['na', 'mean', 'median', 'mode', 'fix']:
            rep_value = float(rep_value) if method!='공백' else None
            temp = data.copy(deep=True)
            temp.loc[outlier_mask] = rep_value
            return temp.to_list()
        elif method == 'prev':
            data = data.mask(outlier_mask).ffill().bfill()
            data.loc[na_mask] = None
            return data.to_list()
        elif method == 'next':
            data = data.mask(outlier_mask).bfill().ffill()
            data.loc[na_mask] = None
            return data.to_list()
        elif method == 'linear':
            data.mask(outlier_mask).interpolate(method='linear', limit_direction='both')
            data.loc[na_mask] = None
            return data.to_list()

    @classmethod
    def transform_data(cls, data: pd.Series, method: str):
        """ 데이터 변환 """
        if method == 'log':
            if (data <= 0).any():
                raise ValueError("Log transformation requires all values > 0.")
            return np.log(data)
        elif method == 'sqrt':
            if (data < 0).any():
                raise ValueError("Square root transformation requires all values >= 0.")
            return np.sqrt(data)
        elif method == 'reciprocal':
            if (data == 0).any():
                raise ValueError("Reciprocal transformation requires no zeros.")
            return 1 / data
        elif method == 'boxcox':
            if (data <= 0).any():
                raise ValueError("Box-Cox requires all values > 0.")
            transformed, _ = stats.boxcox(data)
            return pd.Series(transformed, index=data.index)
        elif method == 'yeojohnson':
            transformed, _ = stats.yeojohnson(data)
            return pd.Series(transformed, index=data.index)
        raise ValueError(f"Unsupported transformation method: {method}")

    @classmethod
    def scaler_data(cls, data: pd.Series, method: str):
        """ 데이터 변환 """
        scaler = None
        if method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'standard':
            scaler = StandardScaler()
        elif method == 'maxabs':
            scaler = MaxAbsScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        transformed = scaler.fit_transform(pd.DataFrame(data))
        return transformed.ravel().tolist()
