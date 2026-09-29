# pylint: disable=W0718, E1101
"""
상관 분석
"""
from typing import Dict, List
import math
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from eda_manager.chart.chart_helper import formatter_kmb, close_pyplot,\
    save_chart_to_bytes, save_chart_to_file
from fonts import get_project_font

FONT_GOTHIC_PATH, FONT_DREAM_PATH = get_project_font()

matplotlib.use("agg")
DBGOTHIC = fm.FontProperties(fname=FONT_GOTHIC_PATH)
DBDREAM = fm.FontProperties(fname=FONT_DREAM_PATH, size=15, weight='bold')
fm.fontManager.addfont(FONT_GOTHIC_PATH)
fm.fontManager.addfont(FONT_DREAM_PATH)

plt.rcParams['font.family'] = DBGOTHIC.get_name()
plt.rcParams['axes.unicode_minus'] = False

class CorrelationAnalyze():
    """ 상관 분석 클래스 """
    def __init__(self, df: pd.DataFrame, columns: List[Dict[str, object]], corr_method: str):
        self.sample = df[[col['Column'] for col in columns]].copy(deep=True)
        self.columns = columns
        self.corr_method = corr_method
        self.corr_result = None
        for ord_col in [col['Column'] for col in columns if col['ColumnChar']=='Ordinal']:
            self.sample[ord_col] = self.sample[ord_col].cat.codes

    def result(self):
        """ 상관 분석 결과 """
        self.corr_result = self.correlation_detail_info()
        result = {}
        chart_result = {}
        chart_result[f'상관 계수 Matrix({self.corr_method.capitalize()})'] = self.coefficient_matrix()
        chart_result['산점도 행렬'] = self.scatter_matrix()
        result['Charts'] = [
            {'ChartName':k, 'ImageBase64':v, 'ChartFileName':k}
            for k,v in chart_result.items() if v is not None]
        result['Results'] = self.corr_result
        return result

    def result_with_save(self, corr_matrix_path: str, scatter_matrix_path: str):
        """ 상관 분석 결과 (저장)"""
        result = {}
        plot_info = {}
        plot_info['corr_matrix_img'] = None
        plot_info['scatter_matrix_img'] = None
        self.corr_result = self.correlation_detail_info()
        if self.coefficient_matrix(save_file=True, save_path=corr_matrix_path):
            plot_info['corr_matrix_img'] = corr_matrix_path
        if self.scatter_matrix(save_file=True, save_path=scatter_matrix_path):
            plot_info['scatter_matrix_img'] = scatter_matrix_path
        col_dic = {
            'Column1': '표본 1',
            'Column2': '표본 2',
            'SampleCount': 'N',
            'Coefficient': '상관계수',
            'ConfidenceIntervalLower': '95% 신뢰하한',
            'ConfidenceIntervalUpper': '95% 신뢰상한',
            'PValue': 'p-value',
            'CorrelationLevel': '상관 관계'
        }
        result['Results'] = pd.DataFrame(self.corr_result).rename(columns=col_dic)
        result['plot_info'] = plot_info
        return result

    def coefficient_confidence_interval(self, n: int, r: float, corr_method: str='pearson'):
        """ 상관 계수 신뢰 구간

        Args:
            n (int): 관측치 수
            r (float): 표본 상관 계수 추정치
            corr_method (str, optional): 상관 계수 Type. Defaults to 'pearson'.
        """
        z_base, z_diff, z_025 = 0, 0, 1.96
        if corr_method == 'pearson':
            z_base = 0.5*(math.log(1+r)-math.log(1-r))
            z_diff = z_025/math.sqrt(n-3)
        else:
            se = math.sqrt((1+math.pow(r,2)/2)/(n-3))
            z_base = 0.5*(math.log(1+r)-math.log(1-r))
            z_diff = z_025*se
        z_l, z_u = z_base - z_diff, z_base + z_diff
        lower = (math.exp(2*z_l)-1)/(math.exp(2*z_l)+1)
        upper = (math.exp(2*z_u)-1)/(math.exp(2*z_u)+1)
        return lower, upper

    def judge_correlation_level(self, coeff: float):
        """ 상관 관계 정도 판정

        Args:
            coeff (float): 상관 계수
        """
        if -1<=coeff<-0.7:
            return '강한 음의 상관관계'
        elif -0.7<=coeff<-0.3:
            return '약한 음의 상관관계'
        elif -0.3<=coeff<0.3:
            return '상관관계 없음'
        elif 0.3<=coeff<0.7:
            return '약한 양의 상관관계'
        elif 0.7<=coeff<=1.0:
            return '강한 양의 상관관계'
        return None

    def correlation_detail_info(self) -> List[Dict[str, object]]:
        """ 상관 관계 상세 분석

        Args:
            df_sample (pd.DataFrame): 샘플 데이터
            columns (List[str]): 변수 리스트
            corr_method (str): 상관 계수 Type

        Returns:
            List[Dict[str, object]]: 결과
        """
        corr_result = []
        for col1, col2 in combinations([col['Column'] for col in self.columns], 2):
            sample = self.sample[[col1, col2]].dropna()
            n = len(sample)
            if n<4:
                corr_result.append(
                    {
                        'Column1': str(col1),
                        'Column2': str(col2),
                        'SampleCount': n,
                        'Coefficient': None,
                        'ConfidenceIntervalLower': None,
                        'ConfidenceIntervalUpper': None,
                        'PValue': None,
                        'CorrelationLevel': None
                    }
                )
            corr, p_val = None, None
            if self.corr_method == 'pearson':
                corr, p_val = pearsonr(sample[col1], sample[col2])
            else:
                corr, p_val = spearmanr(sample[col1], sample[col2])
            ci_l, ci_u = self.coefficient_confidence_interval(n, corr, self.corr_method)
            level = self.judge_correlation_level(corr)
            corr_result.append(
                {
                    'Column1': str(col1),
                    'Column2': str(col2),
                    'SampleCount': n,
                    'Coefficient': float(corr),
                    'ConfidenceIntervalLower': float(ci_l),
                    'ConfidenceIntervalUpper': float(ci_u),
                    'PValue': float(p_val),
                    'CorrelationLevel': level
                }
            )
        return corr_result

    def overwrite_corr_value(self, x, y, ax=None, **kws):
        """ 산점도 행렬 위에 값 표시 """
        ax = ax or plt.gca()
        x_col_nm = x.name.split('(Rank)')[0] if x.name.endswith('(Rank)') else x.name
        y_col_nm = y.name.split('(Rank)')[0] if y.name.endswith('(Rank)') else y.name
        col = [col for col in self.corr_result if
               (col['Column1']==x_col_nm)
               and (col['Column2']==y_col_nm)][0]
        corr = col['Coefficient']
        p_val = col['PValue']
        ax.annotate(f'$r = {corr ** 2:.2f}$\np-value: ${p_val:.2f}$',
                    xy=(.05, .95), xycoords=ax.transAxes, fontsize=8,
                    color='darkred', backgroundcolor='#FFFFFF99', ha='left', va='top')
        if abs(corr)>=0.7:
            ax.set_facecolor('0.8')
        ax.grid(True, linestyle='--', alpha=0.5)
        min_val, max_val = ax.get_ylim()
        if max_val - min_val > 1_000:
            ax.yaxis.set_major_formatter(FuncFormatter(formatter_kmb))
        min_val, max_val = ax.get_xlim()
        if max_val - min_val > 1_000:
            ax.xaxis.set_major_formatter(FuncFormatter(formatter_kmb))

    def coefficient_matrix(self, save_file: bool=False, save_path: str=None):
        """ 상관 계수 행렬 차트 반환 """
        img = None
        is_save = False
        try:
            df_corr = self.sample.corr(method=self.corr_method)
            mask = np.zeros_like(df_corr, dtype=np.bool)
            mask[np.triu_indices_from(mask)] = True
            fig, ax = plt.subplots(figsize=(7, 7))
            sns.heatmap(df_corr,
                        cmap='RdYlBu_r',
                        annot=True,
                        mask=mask,
                        linewidths=.5,
                        fmt='.3f',
                        cbar_kws={'shrink':.5},
                        ax=ax,
                        vmin=-1, vmax=1)
            ax.set_title(f'쌍별 비교 {self.corr_method.capitalize()} 상관 계수',
                        fontdict=dict(fontsize=15, fontweight='bold', fontproperties=DBDREAM))
            ax.set_xlabel('표본 1', fontdict=dict(fontweight='bold'))
            ax.set_ylabel('표본 2', fontdict=dict(fontweight='bold'))
            fig.tight_layout()
            if not save_file:
                img = save_chart_to_bytes(fig)
            else:
                is_save = save_chart_to_file(fig, save_path)
        except Exception as e:
            print(e)
        close_pyplot()
        if not save_file:
            return img
        return is_save

    def scatter_matrix(self, save_file: bool=False, save_path: str=None):
        """ 산점도 행렬 반환 """
        img = None
        is_save = False
        try:
            ordinals = [col['Column'] for col in self.columns if col['ColumnChar']=='Ordinal']
            g = sns.pairplot(self.sample.rename(columns={col:f'{col}(Rank)' for col in ordinals}),
                            corner=True)
            g.map_lower(self.overwrite_corr_value)
            g.fig.suptitle("산점도 행렬", fontsize=20)
            if not save_file:
                img = save_chart_to_bytes(g)
            else:
                is_save = save_chart_to_file(g, save_path)
        except Exception as e:
            print(e)
        close_pyplot()
        if not save_file:
            return img
        return is_save
