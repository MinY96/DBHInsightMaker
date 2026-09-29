# pylint: disable=W0718
"""
Project 처리 메소드
"""

from typing import Dict, List
import os
import shutil
from datetime import datetime
from helper import dict_to_json, read_json_to_dict

def project_infos(project_parent_dir: str) -> List[Dict[str, object]]:
    """ 프로젝트 저장 경로 내 프로젝트 정보 리스트 반환

    Args:
        project_parent_dir (str): 프로젝트 저장 경로

    Returns:
        List[Dict[str, object]]: 프로젝트 정보 리스트
    """
    infos = []
    try:
        for project in os.listdir(project_parent_dir):
            project_dir = os.path.join(project_parent_dir, project)
            project_info_file = os.path.join(project_dir, 'info.json')
            if os.path.exists(project_info_file):
                info = read_json_to_dict(project_info_file)
                infos.append(info)
        return infos, None
    except Exception as e:
        return None, str(e)

def create_project(project_parent_dir: str, name: str, desc: str) -> bool:
    """ 프로젝트 생성

    Args:
        project_parent_dir (str): 프로젝트 저장 경로
        name (str): 프로젝트 명
        desc (str): 프로젝트 설명

    Returns:
        bool: 프로젝트 정상 생성 여부
    """
    project_dir = os.path.join(project_parent_dir, name)
    error = f'{name} 프로젝트가 이미 존재합니다.'
    if not os.path.exists(project_dir):
        try:
            os.makedirs(project_dir)
            info = {
                'ProjectName': name,
                'ProjectDesc': desc,
                'ProjectDir': project_dir,
                'CreateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'IsLoadData': False
            }
            file_path = os.path.join(project_dir, 'info.json')
            dict_to_json(info, file_path)
            return True, None
        except Exception as e:
            error = str(e)
    return False, error

def delete_project(project_nm: str, project_dir: str) -> bool:
    """ 프로젝트 삭제

    Args:
        project_nm (str): 프로젝트 명
        project_dir (str): 프로젝트 경로

    Returns:
        bool: 프로젝트 정상 삭제 여부
    """
    error = ''
    if os.path.exists(project_dir):
        try:
            shutil.rmtree(project_dir)
            return True, None
        except Exception as e:
            error = str(e)
    return False, f'{project_nm}-{error}'

def update_project_info(project_dir: str, update_info: Dict[str, bool]) -> bool:
    """ 프로젝트 정보 업데이트

    Args:
        project_dir (str): 프로젝트 경로
        update_info (Dict[str, bool]): 업데이트할 정보

    Returns:
        bool: 정상 업데이트 여부
    """
    file_path = os.path.join(project_dir, 'info.json')
    project_info = None
    if os.path.exists(file_path):
        try:
            project_info = read_json_to_dict(file_path)
            for k, update_value in update_info.items():
                project_info[k] = update_value
            dict_to_json(project_info, file_path)
            return True, None
        except Exception as e:
            return False, str(e)
    return False, '프로젝트 파일이 존재하지 않습니다.'
