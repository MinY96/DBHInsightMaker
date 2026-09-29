# pylint: disable=W0718, E1101
"""
정규성 검정
"""
from typing import Dict
import os
import numpy as np
import pandas as pd
from scipy.stats import shapiro, kstest, anderson
from eda_manager.chart.chart_helper import common_option
from eda_manager.chart.custom.chart_group.distribution import qq_plot, dist_num

class NormalityTest():
    """ 정규성 검정 클래스

    Args:
        col_info (Dict[str, object]): 컬럼 정보
        df (pd.DataFrame): 데이터
    """

    def __init__(self, project_dir: str, col_info: Dict[str, object], col_nm: str):
        self.project_dir = project_dir
        self.col_info = col_info
        self.col_nm = col_nm
        self.figsize_x = 7
        self.figsize_y = 7

    def result(self):
        """ 정규성 검정 결과 """
        data_path = os.path.join(self.project_dir, 'data.pkl')
        df = pd.read_pickle(data_path)
        data = df[self.col_nm].dropna()
        result = {}
        chart_result = {}
        chart_result['QQ-Plot'] = qq_plot(
            self.project_dir, self.col_nm,
            common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_size=self.figsize_x, y_size=self.figsize_y
        ))
        chart_result['Distribution'] = dist_num(
            self.project_dir, self.col_nm, orient="auto", color="auto",
            fill="auto", kde=True, dist_kind="hist", log_scale="auto",
            common_option=common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size=self.figsize_x, y_size=self.figsize_y
            ))
        result['Charts'] = [
            {'ChartName':k, 'ImageBase64':v, 'ChartFileName':f"{self.col_nm}-{k}"}
            for k,v in chart_result.items() if v is not None]
        result['Results'] = [
            self.shapiro_wilk_test(data),
            self.kolmogorov_smirnov_test(data),
            self.anderson_darling_test(data)]
        return result

    def test_result_by_p_value(
        self, p_value: float, significance_level: float) -> Dict[str, object]:
        """ p-value 기반 정규성 결과 판정

        Args:
            p_value (float): p-value
            significance_level (float): 유의 수준

        Returns:
            Dict[str, object]: 판정 결과
        """
        if p_value <= significance_level:
            return {
                'SignificanceLevel': significance_level,
                'Result': f'{self.col_nm} 은 정규 분포를 따르지 않는다.',
                'Detail': f'p-value ({p_value:.4f}) ≤ α ({significance_level:.2f}) 이므로, 귀무가설(H0) 기각'
            }
        return {
            'SignificanceLevel': significance_level,
            'Result': f'{self.col_nm} 은 정규 분포를 따른다.',
            'Detail': f'p-value ({p_value:.4f}) > α ({significance_level:.2f}) 이므로, 귀무가설(H0) 채택'
        }

    def test_result_by_stat(
        self, stat: float, threshold: float, significance_level: float) -> Dict[str, object]:
        """ 통계량 기반 정규성 결과 판정

        Args:
            stat (float): 통계량
            threshold (float): 임계값
            significance_level (float): 유의수준

        Returns:
            Dict[str, object]: 판정 결과
        """
        p_value = 0.05 if significance_level==5. else 0.01
        if stat < threshold:
            return {
                'SignificanceLevel': p_value,
                'Result': f'{self.col_nm} 은 정규 분포를 따른다.',
                'Detail': (f'p-value가 {significance_level:.1f}%일 때, '
                           f'통계량 ({stat:.4f}) < 임계값 ({threshold:.4f}) 이므로, 귀무가설(H0) 채택')
            }
        return {
            'SignificanceLevel': p_value,
            'Result': f'{self.col_nm} 은 정규 분포를 따르지 않는다.',
            'Detail': (f'p-value가 {significance_level:.1f}%일 때, '
                       f'통계량 ({stat:.4f}) ≥ 임계값 ({threshold:.4f}) 이므로, 귀무가설(H0) 기각')
        }

    def shapiro_wilk_test(self, data) -> Dict[str, object]:
        """ Shapiro-Wilk 검정 결과 반환

        Returns:
            Dict[str, object]: 정규성 검정 결과
        """
        data = np.array(data)
        _, p = shapiro(data)
        return {
            'Method': 'Shapiro Wilk',
            'Purpose': 'Normality Test',
            'BestCase': '샘플 크기가 작거나 중간 규모인 경우',
            'Strength': '작은 표본에서 높은 검정력',
            'Weakness': '큰 데이터셋에서는 매우 민감',
            'Results': [
                self.test_result_by_p_value(p, 0.01),
                self.test_result_by_p_value(p, 0.05)
            ]
        }

    def kolmogorov_smirnov_test(self, data) -> Dict[str, object]:
        """ Kolmogorov-Smirnov 검정 결과 반환

        Returns:
            Dict[str, object]: 정규성 검정 결과
        """
        data = np.array(data)
        mean = float(self.col_info['Mean'].replace(',',''))
        std = float(self.col_info['Std'].replace(',',''))
        _, p = kstest(data, 'norm', args=(mean, std))
        return {
            'Method': 'Kolmogorov-Smirnov',
            'Purpose': 'Normality Test',
            'BestCase': '분포 전체를 단수하게 비교할 때, 평균/표준편차가 이미 알려진 경우',
            'Strength': '표본 크기에 제한 없음',
            'Weakness': '검정 정밀도 낮음',
            'Results': [
                self.test_result_by_p_value(p, 0.01),
                self.test_result_by_p_value(p, 0.05)
            ]
        }

    def anderson_darling_test(self, data) -> Dict[str, object]:
        """ Anderson-Darling 검정 결과 반환

        Returns:
            Dict[str, object]: 정규성 검정 결과
        """
        data = np.array(data)
        stat = anderson(data, dist='norm')
        return {
            'Method': 'Anderson-Darling',
            'Purpose': 'Normality Test',
            'BestCase': '꼬리 부분이 중요한 경우',
            'Strength': '정규성뿐 아니라 꼬리 적합성까지 민감하게 포착',
            'Weakness': '표본이 적으면 불안정',
            'Results': [
                self.test_result_by_stat(
                    stat.statistic, stat.critical_values[-1], stat.significance_level[-1]),
                self.test_result_by_stat(
                    stat.statistic, stat.critical_values[2], stat.significance_level[2])
            ]
        }
