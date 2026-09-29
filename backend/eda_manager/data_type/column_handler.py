# pylint: disable=W0718
"""
Data 가공 및 조회
"""

from typing import Dict, List
import os
import pandas as pd
from eda_manager.data_type import summarize_dataframe
from helper import read_json_to_dict, save_file_info

def load_column_init_data(project_dir: str, col_nm: str) -> Dict[str, object]:
    """ 컬럼 초기 50개 Data 반환

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 컬럼 명

    Returns:
        Dict[str, object]: 컬럼 데이터
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    result, error = None, None
    try:
        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        col_info = [info for info in col_infos if info['Column']==col_nm][0]
        result = list(map(str, df[col_info['Column']].dropna()))[:50]
    except Exception as e:
        error = str(e)
    return result, error

def load_column_unique_data(project_dir: str, col_nm: str) -> Dict[str, object]:
    """ 컬럼 고유값 리스트 반환

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 컬럼 명

    Returns:
        Dict[str, object]: 컬럼 고유값 리스트
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    result, error = None, None
    try:
        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        col_info = [info for info in col_infos if info['Column']==col_nm][0]
        result = sorted(list(map(str, df[col_info['Column']].dropna().unique())))
    except Exception as e:
        error = str(e)
    return result, error

def convert_column_type(project_dir: str, col_nm: str,
                        convert_dtype: str, datetime_format: str=None, orders: List[str]=None,
                        save_mode: bool=False):
    """ 컬럼 타입 변환

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 컬럼 명
        convert_dtype (str): 변환할 타입
        datetime_format (str, optional): DateTime 변환 포맷. Defaults to None.
        orders (List[str], optional): Ordinal 순서 리스트. Defaults to None.
        save_mode (bool, optional): 저장 모드 여부. Defaults to False.
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    file_info_path = os.path.join(project_dir, 'file_info.json')
    result, error = None, None
    convert_data = None
    try:
        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        col_info = [info for info in col_infos if info['Column']==col_nm][0]
        col_nm = col_info['Column']
        if convert_dtype == 'DateTime':
            convert_data = pd.to_datetime(df[col_nm], format=datetime_format)
        elif convert_dtype == 'Ordinal':
            convert_data = df[col_nm].astype('str').astype('category')
            convert_data = convert_data.cat.set_categories(orders, ordered=True)
        elif convert_dtype == 'Nominal':
            convert_data = df[col_nm].astype('category')
            convert_data = convert_data.cat.as_unordered()
        elif convert_dtype == 'Discrete':
            convert_data = df[col_nm].astype(int)
        elif convert_dtype == 'Continuous':
            convert_data = df[col_nm].astype(float)
    except Exception as e:
        error = str(e)
        return result, error
    if not save_mode:
        result = list(map(str, convert_data.dropna()))[:50]
        return result, error
    try:
        # from project_manager.file_handler import save_file_info
        df[col_nm] = convert_data
        col_infos = summarize_dataframe(df)
        file_info = read_json_to_dict(file_info_path)
        save_file_info(df, file_info, col_infos, project_dir)
        return True, None
    except Exception as e:
        return False, str(e)

def remove_column(project_dir: str, col_nm: str) -> bool:
    """ 프로젝트 내 컬럼 제거

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 제거할 컬럼

    Returns:
        bool: 정상 제거 여부
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    file_info_path = os.path.join(project_dir, 'file_info.json')
    try:
        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        col_info = [info for info in col_infos if info['Column']==col_nm][0]
        col_nm = col_info['Column']
        df = df.drop(columns=[col_nm])
        col_infos = summarize_dataframe(df)
        file_info = read_json_to_dict(file_info_path)
        save_file_info(df, file_info, col_infos, project_dir)
        return True, None
    except Exception as e:
        return False, str(e)
