# pylint: disable=W0718
"""
Data 변환
"""

from typing import Dict, List
import os
import pandas as pd
from eda_manager.data_type import summarize_dataframe
from eda_manager.preprocess import Converter
from helper import read_json_to_dict, save_file_info

def create_new_column(payload: Dict[str, object]):
    """ 옵션 별 컬럼 생성 로직 분기

    Args:
        payload (Dict[str, object]): 컬럼 생성 옵션
    """
    project_dir = payload.get('ProjectDir', None)
    data_path = os.path.join(project_dir, 'data.pkl')
    file_info_path = os.path.join(project_dir, 'file_info.json')

    df = pd.read_pickle(data_path)
    new_col_nm = payload.get('NewColumnName', None)
    main_type = payload.get('MainType', None)
    new_data = None
    data_size = len(df)
    payload.update({'DataSize':data_size})
    try:
        match main_type:
            case 'Random':
                new_data = to_dataframe_series(create_random_data(payload), new_col_nm)
            case 'Calc':
                new_data = to_dataframe_series(create_calc_data(df, payload), new_col_nm)
            case 'Combi':
                new_data = to_dataframe_series(create_combi_data(df, payload), new_col_nm)
            case 'Outlier':
                new_data = to_dataframe_series(create_outlier_data(df, payload), new_col_nm)
            case 'Convert':
                new_data = to_dataframe_series(create_convert_data(df, payload), new_col_nm)
    except ValueError as e:
        return False, str(e)
    df = pd.concat([df, new_data], axis=1)
    col_infos = summarize_dataframe(df)
    file_info = read_json_to_dict(file_info_path)
    save_file_info(df, file_info, col_infos, project_dir)
    return True, None

def to_dataframe_series(data: List[object], col_nm: str):
    """ List Series로 변환 """
    return pd.Series(data, name=col_nm)

def create_random_data(payload: Dict[str, object]) -> List[float]:
    """ 난수 생성

    Args:
        payload (Dict[str, object]): 옵션

    Returns:
        List[float]: 생성된 난수 리스트
    """
    data_size = payload.get('DataSize', None)
    min_val = payload.get('MinValue', None)
    max_val = payload.get('MaxValue', None)
    is_integer = payload.get('IsInteger', None)
    is_norm = payload.get('SetNormalDist', None)
    mean_val = payload.get('MeanValue', None)
    std_val = payload.get('StdValue', None)
    if is_norm & is_integer:
        return Converter.random_interger_norm_data(data_size, min_val, max_val, mean_val, std_val)
    elif is_norm & (not is_integer):
        return Converter.random_float_norm_data(data_size, min_val, max_val, mean_val, std_val)
    elif (not is_norm) & is_integer:
        return Converter.random_integer_data(data_size, min_val, max_val)
    elif (not is_norm) & (not is_integer):
        return Converter.random_float_data(data_size, min_val, max_val)

def create_calc_data(df: pd.DataFrame, payload: Dict[str, object]) -> List[float]:
    """ 연산 데이터 생성

    Args:
        df (pd.DataFrame): 원본 데이터
        payload (Dict[str, object]): 옵션

    Returns:
        List[float]: 생성된 연산 데이터 리스트
    """
    col_type = payload.get('SubType', None)
    col_nm = payload.get('Column', None)
    col_data = df[col_nm]
    calc_type = payload.get('Symbol', None)
    if col_type == 'Numerical':
        calc_value = payload.get('Value', None)
        return Converter.calc_numerical_data(col_data, calc_type, calc_value)
    elif col_type == 'Categorical':
        if calc_type in ['upper', 'lower', 'capital', 'strip']:
            return Converter.calc_categorical_data(col_data, calc_type)
        elif calc_type == 'split':
            split_text = payload.get('SplitText', None)
            split_order = payload.get('SplitOrder', None)
            return Converter.calc_categorical_data_split(col_data, split_text, split_order)
        elif calc_type == 'replace':
            rpl_old = payload.get('ReplaceOld', None)
            rpl_new = payload.get('ReplaceNew', None)
            return Converter.calc_categorical_data_replace(col_data, rpl_old, rpl_new)
        elif calc_type == 'concat':
            concat_text = payload.get('ConcatenateText', None)
            is_prev = payload.get('ConcatenateOnPrev', None)
            return Converter.calc_categorical_data_concatenate(col_data, concat_text, is_prev)
    elif col_type == 'Function':
        return Converter.calc_function_data(col_data, calc_type)

def create_combi_data(df: pd.DataFrame, payload: Dict[str, object]) -> List[float]:
    """ 변수 조합 데이터 생성

    Args:
        df (pd.DataFrame): 원본 데이터
        payload (Dict[str, object]): 옵션

    Returns:
        List[float]: 생성된 변수 조합 데이터 리스트
    """
    col_type = payload.get('SubType', None)
    col_first_nm = payload.get('ColumnFirst', None)
    col_second_nm = payload.get('ColumnSecond', None)
    col_first, col_second = df[col_first_nm], df[col_second_nm]
    operation = payload.get('Symbol', None)
    if col_type == 'Numerical':
        return Converter.combi_numerical_data(col_first, col_second, operation)
    elif col_type == 'Categorical':
        return Converter.combi_categorical_data(col_first, col_second, operation)
    elif col_type == 'DateTime':
        timedelta_type = payload.get('TimeDeltaType', None)
        return Converter.combi_datetime_data(col_first, col_second, operation, timedelta_type)

def create_outlier_data(df: pd.DataFrame, payload: dict[str, object]) -> List[float]:
    """ 이상치 대체 데이터 생성

    Args:
        df (pd.DataFrame): 원본 데이터
        payload (Dict[str, object]): 옵션

    Returns:
        List[float]: 생성된 이상치 대체 데이터 리스트
    """
    col_type = payload.get('SubType', None)
    col_nm = payload.get('Column', None)
    col_data = df[col_nm]
    method = payload.get('ReplaceMethod', None)
    rep_value = payload.get('ReplaceValue', None)
    outlier_mask = None
    if col_type == 'Sigma':
        mean, sigma = float(payload.get('Mean', None)), float(payload.get('Std', None))
        sigma_level = float(payload.get('SigmaLevel', None))
        outlier_mask = Converter.outlier_sigma_data(col_data, mean, sigma, sigma_level)
    elif col_type == 'IQR':
        q1, q3 = float(payload.get('Q1', None)), float(payload.get('Q3', None))
        outlier_mask = Converter.outlier_iqr_data(col_data, q1, q3)
    return Converter.outlier_replace_data(col_data, outlier_mask, method, rep_value)

def create_convert_data(df: pd.DataFrame, payload: dict[str, object]) -> List[float]:
    """ 데이터 변환

    Args:
        df (pd.DataFrame): 원본 데이터
        payload (Dict[str, object]): 옵션

    Returns:
        List[float]: 변환된 데이터 리스트
    """
    col_type = payload.get('SubType', None)
    col_nm = payload.get('Column', None)
    col_data = df[col_nm]
    method = payload.get('ConvertMethod', None)
    if col_type == 'NormalDist':
        return Converter.transform_data(col_data, method)
    elif col_type == 'Scaler':
        return Converter.scaler_data(col_data, method)
