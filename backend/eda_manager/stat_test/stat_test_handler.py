# pylint: disable=W0718
"""
통계 검정 메소드
"""
from typing import Dict
import os
from eda_manager.stat_test import NormalityTest
from helper import read_json_to_dict

def get_normality_result(
    project_dir: str, col_nm: str) -> Dict[str, object]:
    """ 프로젝트 폴더 내 선택한 컬럼 차트 생성

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 컬럼 명

    Returns:
        Dict[str, object]: 정규성 검정 결과
    """
    column_info_path = os.path.join(project_dir, 'column_info.json')
    result, error = None, None
    try:
        col_infos = read_json_to_dict(column_info_path)
        col_info = [info for info in col_infos if info['Column']==col_nm][0]
        n_test = NormalityTest(project_dir, col_info, col_nm)
        result = n_test.result()
    except Exception as e:
        error = str(e)
    return result, error
