# pylint: disable=W0718
"""
파일 처리 관련 메소드
"""
from typing import Dict
import os
import json
import numpy as np
import pandas as pd

def safe_default(o):
    if o is None:
        return None
    if isinstance(o, float):
        if np.isnan(o) or np.isinf(o):  # NaN, inf 체크
            return None
    return o

def dict_to_json(info: Dict[str, object], save_file_path: str) -> bool:
    """ 딕셔너리 json 파일 저장

    Args:
        info (Dict[str, object]): 정보 담긴 딕셔너리
        save_file_path (str): json 파일 경로

    Returns:
        bool: 파일 정상 저장 여부
    """
    try:
        with open(save_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(info, json_file, ensure_ascii=False, indent=4, default=safe_default)
        return True
    except Exception as e:
        print(e)
    return False

def read_json_to_dict(json_file_path: str) -> Dict[str, object]:
    """_summary_

    Args:
        json_file_path (str): _description_

    Returns:
        Dict[str, object]: 파일 정보 반환
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            info = json.load(json_file)
        return info
    except Exception as e:
        print(e)
    return None

def save_file_info(df: pd.DataFrame,
                   file_info: Dict[str, object], col_info: Dict[str, object],
                   project_dir: str, sheet_nm: str=None):
    """ 프로젝트 폴더에 Data 저장

    Args:
        df (pd.DataFrame): 파일 Read 결과
        file_info (Dict[str, object]): 파일 정보
        col_info (Dict[str, object]): 컬럼 별 유형
        project_dir (str): 프로젝트 경로
        sheet_nm (str): Excel 파일 시트 명
    """
    file_info['SheetName'] = sheet_nm
    file_info['Rows'] = df.shape[0]
    file_info['Cols'] = df.shape[1]
    data_path = os.path.join(project_dir, 'data.pkl')
    file_info_path = os.path.join(project_dir, 'file_info.json')
    col_info_path = os.path.join(project_dir, 'column_info.json')
    df.to_pickle(data_path)
    dict_to_json(file_info, file_info_path)
    dict_to_json(col_info, col_info_path)
