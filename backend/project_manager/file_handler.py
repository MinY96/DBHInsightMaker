# pylint: disable=W0718
"""
File 처리 메소드
"""

from typing import Dict
import os
import pandas as pd
from eda_manager.data_type import summarize_dataframe
from helper import read_json_to_dict, save_file_info

def get_file_info(file_path: str) -> Dict[str, object]:
    """ 파일 세부 정보 반환

    Args:
        file_path (str): 파일 경로

    Returns:
        Dict[str, object]: 파일 세부 정보
    """
    file_info = {
        'FileName': None,
        'FileExtension': None,
        'FileSize': None,        
    }
    try:
        file_info['FileName'] = os.path.basename(file_path)
        file_info['FileExtension'] = file_path.split('.')[-1].lower()
        file_info['FileSize'] = os.path.getsize(file_path)/1_000_000
        return file_info
    except Exception as e:
        print(e)
    return file_info

def load_file_info(project_dir: str) -> Dict[str, object]:
    """ 파일 세부 정보 로드

    Args:
        project_dir (str): 프로젝트 경로

    Returns:
        Dict[str, object]: 파일 세부 정보
    """
    file_path = os.path.join(project_dir, 'file_info.json')
    if os.path.exists(file_path):
        try:
            file_info = read_json_to_dict(file_path)
            return file_info, None
        except Exception as e:
            return None, str(e)
    return None, '파일 정보가 존재하지 않습니다.'

def load_column_info(project_dir: str) -> Dict[str, object]:
    """ 데이터 유형 세부 정보 로드

    Args:
        project_dir (str): 프로젝트 경로

    Returns:
        Dict[str, object]: 데이터 유형 세부 정보
    """
    file_path = os.path.join(project_dir, 'column_info.json')
    if os.path.exists(file_path):
        try:
            col_info = read_json_to_dict(file_path)
            return col_info, None
        except Exception as e:
            return None, str(e)
    return None, '파일 정보가 존재하지 않습니다.'

def load_csv_file(project_dir: str, file_path: str) -> bool:
    """ csv 파일 로드

    Args:
        project_dir (str): 프로젝트 경로
        file_path (str): 업로드할 파일 경로

    Returns:
        bool: 업로드 정상 여부
    """
    if os.path.exists(file_path):
        try:
            file_info = get_file_info(file_path)
            df = pd.read_csv(file_path)
            col_info = summarize_dataframe(df)
            save_file_info(df, file_info, col_info, project_dir)
            return True, None
        except Exception as e:
            return False, str(e)
    return False, '업로드할 파일이 존재하지 않습니다.'

def load_excel_file(project_dir: str, file_path: str, sheet_nm: str) -> bool:
    """ Excel 파일 로드

    Args:
        project_dir (str): 프로젝트 경로
        file_path (str): 업로드할 파일 경로
        sheet_nm (str): 시트 명

    Returns:
        bool: 업로드 정상 여부
    """
    if os.path.exists(file_path):
        try:
            file_info = get_file_info(file_path)
            df = None
            match file_info['FileExtension']:
                case 'xls':
                    df = pd.read_excel(file_path, sheet_name=sheet_nm, engine='xlrd')
                case 'xlsx':
                    df = pd.read_excel(file_path, sheet_name=sheet_nm, engine='openpyxl')
                case 'xlsm':
                    df = pd.read_excel(file_path, sheet_name=sheet_nm, engine='openpyxl')
            col_info = summarize_dataframe(df)
            save_file_info(df, file_info, col_info, project_dir, sheet_nm)
            return True, None
        except Exception as e:
            return False, str(e)
    return False, '업로드할 파일이 존재하지 않습니다.'

def load_excel_sheets(file_path: str):
    """ Excel 파일 내 존재하는 Sheet 명 리스트 반환

    Args:
        file_path (str): Excel 파일 경로
    """
    if os.path.exists(file_path):
        result, error = None, None
        try:
            xls = pd.ExcelFile(file_path)
            result = xls.sheet_names
        except Exception as e:
            error = str(e)
        return result, error
    return None, 'Excel 파일이 존재하지 않습니다.'

def save_data_as_excel(project_dir: str, save_path: str) -> bool:
    """ Excel 파일 로드

    Args:
        project_dir (str): 프로젝트 경로
        file_path (str): 업로드할 파일 경로

    Returns:
        bool: 정상 저장 여부
    """
    if os.path.exists(project_dir):
        data_path = os.path.join(project_dir, 'data.pkl')
        # column_info_path = os.path.join(project_dir, 'column_info.json')
        result, error = False, None
        try:
            df = pd.read_pickle(data_path)
            df.to_excel(save_path, index=False)
            result = os.path.exists(save_path)
        except Exception as e:
            error = str(e)
        return result, error
    return False, '해당 프로젝트 폴더가 존재하지 않습니다.'

def save_summary_as_excel(project_dir: str, save_path: str) -> bool:
    """ Excel 파일 로드

    Args:
        project_dir (str): 프로젝트 경로
        file_path (str): 업로드할 파일 경로

    Returns:
        bool: 정상 저장 여부
    """
    if os.path.exists(project_dir):
        column_info_path = os.path.join(project_dir, 'column_info.json')
        result, error = False, None
        try:
            col_infos = read_json_to_dict(column_info_path)
            rename_dic = {
                'DataCount':int,
                'MissingCount': int,
                'MissingRatio': float,
                'UniqueCount': int
            }
            df_summary = pd.DataFrame(col_infos).astype(rename_dic)
            df_summary.to_excel(save_path, index=False)
            result = os.path.exists(save_path)
        except Exception as e:
            error = str(e)
        return result, error
    return False, '해당 프로젝트 폴더가 존재하지 않습니다.'
