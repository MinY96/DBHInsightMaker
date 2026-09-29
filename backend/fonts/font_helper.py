# pylint: disable=W0718, E1101
"""
폰트 설정
"""
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

FONT_GOTHIC_PATH = resource_path('./fonts/DBGothicL.ttf')
FONT_DREAM_PATH = resource_path('./fonts/DBDreamB.ttf')

def get_project_font():
    """ 프로젝트 폰트 경로 반환 """
    if getattr(sys, 'frozen', False):
    # 실행파일로 실행한 경우,해당 파일을 보관한 디렉토리의 full path를 취득
        return resource_path('./fonts/DBGothicL.ttf'), resource_path('./fonts/DBDreamB.ttf')
    # 파이썬 파일로 실행한 경우,해당 파일을 보관한 디렉토리의 full path를 취득
    return os.path.abspath('./fonts/DBGothicL.ttf'),\
        os.path.abspath('./fonts/DBDreamB.ttf')
