# pylint: disable=W0718, E1101, C0413, C0103, C0321, C0301
"""
예측 결과 분석
"""

from typing import List
import numpy as np
import pandas as pd

class PredictAnalyzer:
    """ Test 분석 클래스 """
    def __init__(self, page_dir: str, task_type: str, y: pd.Series, y_pred: pd.Series,
                 y_prob: np.ndarray=None, class_names: List[str]=None,
                 test_ratio: float=None):
        """
        Parameters
        ----------
        page_dir: str
            페이지 정보 저장 경로
        task_type : str
            "regression" or "classifier"
        y : array-like
            실제 값
        y_pred : array-like
            예측 값
        y_prob : array-like, optional
            분류일 경우 확률 (predict_proba 결과)
        class_names : list, optional
            분류일 경우 클래스 이름 리스트
        """
        self.page_dir = page_dir
        self.task_type = task_type
        self.y = np.array(y)
        self.y_pred = np.array(y_pred)
        self.y_prob = y_prob
        self.class_names = class_names
        self.test_ratio = test_ratio
        self.test_size = len(y)
