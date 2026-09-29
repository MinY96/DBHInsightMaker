# pylint: disable=W0718
"""
Data 타입 및 Summary 조회
"""

from typing import Dict, List
import pandas as pd

def summarize_dataframe(df: pd.DataFrame) -> List[Dict[str, object]]:
    """ DataFrame의 기존 정보 및 기초통계량 반환

    Args:
        df (pd.DataFrame): 데이터 프레임

    Returns:
        List[Dict[str, object]]: 컬럼 별 데이터 단위 정보 / 통계량 반환
    """
    result = []

    for col in df.columns:
        col_data = df[col]
        dtype = col_data.dtype

        col_type, col_char = 'Categorical', 'Nominal'
        # Column Type & Character
        if pd.api.types.is_object_dtype(dtype):
            col_type = 'Categorical'
            col_char = 'Nominal'
        elif isinstance(dtype, pd.CategoricalDtype):
            col_type = 'Categorical'
            if dtype.ordered:
                col_char = 'Ordinal'
            else:
                col_char = 'Nominal'
        elif pd.api.types.is_integer_dtype(dtype):
            col_type = 'Numerical'
            col_char = 'Discrete'
        elif pd.api.types.is_float_dtype(dtype):
            col_type = 'Numerical'
            col_char = 'Continuous'
        elif pd.api.types.is_datetime64_dtype(dtype):
            col_type = 'Numerical'
            col_char = 'DateTime'

        # Basic counts
        data_count = col_data.count()
        missing_count = col_data.isna().sum()
        missing_ratio = missing_count / len(df)

        # Stats
        mean = std = min_val = q1 = median = q3 = max_val = None
        if col_type == 'Numerical':
            if col_char in ['Continuous', 'Discrete']:
                t_format = ',.4f' if col_char=='Continuous' else ',.0f'
                mean = f"{col_data.mean():{t_format}}"
                std = f"{col_data.std():{t_format}}"
                min_val = f"{col_data.min():{t_format}}"
                q1 = f"{col_data.quantile(0.25):{t_format}}"
                median = f"{col_data.median():{t_format}}"
                q3 = f"{col_data.quantile(0.75):{t_format}}"
                max_val = f"{col_data.max():{t_format}}"
            elif col_char == 'DateTime':
                default_format = '%Y-%m-%d %H:%M:%S'
                mean = col_data.mean().strftime(default_format)
                std = None
                min_val = col_data.min().strftime(default_format)
                q1 = col_data.quantile(0.25).strftime(default_format)
                median = col_data.median().strftime(default_format)
                q3 = col_data.quantile(0.75).strftime(default_format)
                max_val = col_data.max().strftime(default_format)
        elif col_char == 'Ordinal':
            mean = std = q1 = median = q3 = None
            min_val = col_data.min()
            max_val = col_data.max()

        # Mode (최빈값)
        mode_val = None
        try:
            mode_series = col_data.mode()
            if not mode_series.empty:
                mode_val = str(mode_series.iloc[0])
        except Exception as e:
            print(e)

        unique_count = int(col_data.nunique())

        result.append({
            'Column': col,
            'ColumnType': col_type,
            'ColumnChar': col_char,
            'DataCount': int(data_count),
            'MissingCount': int(missing_count),
            'MissingRatio': float(missing_ratio),
            'Mean': mean,
            'Std': std,
            'Min': min_val,
            'Q1': q1,
            'Median': median,
            'Q3': q3,
            'Max': max_val,
            'Mode': mode_val,
            'UniqueCount': unique_count
        })
    return result
