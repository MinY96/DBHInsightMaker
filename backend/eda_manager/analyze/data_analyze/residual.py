"""
회귀분석 잔차분석 클래스
"""

import os
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from eda_manager.analyze.data_analyze.chart_creator import _set_chart_title, _set_chart_x_label

class ResidualAnalyzer:
    def __init__(self, y, y_pred, model_type, model, output_dir):
        self.y = y
        self.y_pred = y_pred
        self.model_type = model_type.lower()
        self.model = model
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # residuals
        self.residuals = y - y_pred

        # chart meta storage
        self.charts_info = []

        # 차트 후보 목록 정의
        self.chart_definitions = [
            {
                "name": "Residual vs Fitted",
                "method": self.plot_residual_vs_fitted,
                "valid_models": ["linear", "logit"],
                "explanation": "적합치(Fitted values)에 따른 잔차의 분포를 시각화합니다.",
                "insight": (
                    "이 그래프는 모형의 선형성(linearity)과 등분산성(homoscedasticity)을 "
                    "검토하는 데 유용합니다. 잔차가 0을 중심으로 무작위로 흩어져 있으면 모형이 잘 맞는다는 의미입니다."
                ),
                "check": (
                    "잔차가 곡선 패턴을 보이면 선형성이 위배된 것이고, 깔때기 모양으로 퍼지면 등분산성이 깨진 것입니다. "
                    "이 경우 변수 변환(Box-Cox 등)이나 비선형 모형 고려가 필요합니다."
                )
            },
            {
                "name": "Residual vs Order",
                "method": self.plot_residual_vs_order,
                "valid_models": ["linear", "logit", "multilogit"],
                "explanation": "관측 순서(또는 시간)에 따른 잔차 변화를 보여줍니다.",
                "insight": (
                    "데이터가 시간 순서나 수집 순서에 따라 자기상관(autocorrelation)을 가지는지 확인할 수 있습니다. "
                    "잔차가 무작위로 분포하면 독립성 가정이 충족된 것이고, 주기적 패턴이나 추세가 있으면 독립성 위배입니다."
                ),
                "check": (
                    "잔차가 특정 구간에서만 크거나 파동처럼 반복되는 경우가 있는지 확인해야 합니다. "
                    "자기상관이 의심되면 Durbin-Watson 검정이나 ARIMA 기반 접근이 필요합니다."
                )
            },
            {
                "name": "Histogram of Residual",
                "method": self.plot_histogram,
                "valid_models": ["linear"],
                "explanation": "잔차 분포를 히스토그램으로 나타내어 정규성 여부를 확인합니다.",
                "insight": (
                    "선형회귀에서는 잔차가 정규분포를 따른다고 가정합니다. "
                    "히스토그램이 종 모양(Bell-shape)에 가까울수록 정규성이 충족된 것입니다."
                ),
                "check": (
                    "히스토그램이 한쪽으로 치우치거나 꼬리가 두껍다면 정규성이 위배된 것입니다. "
                    "이 경우 변수 변환이나 로버스트 회귀를 고려해야 합니다."
                )
            },
            {
                "name": "Q-Q Plot of Residual",
                "method": self.plot_qqplot,
                "valid_models": ["linear"],
                "explanation": "잔차 분위수와 정규분포 분위수를 비교하는 Q-Q Plot입니다.",
                "insight": (
                    "잔차가 직선을 잘 따르면 정규성을 만족합니다. "
                    "꼬리 부분이 위/아래로 크게 벗어나면 Heavy tail 또는 Light tail 분포를 의미합니다."
                ),
                "check": (
                    "잔차 점들이 대각선 직선에서 심하게 벗어나지 않는지 확인합니다. "
                    "특히 꼬리 부분에서 일관되게 벗어나면 정규성 위배를 시사합니다."
                )
            },
            {
                "name": "Scale-Location",
                "method": self.plot_scale_location,
                "valid_models": ["linear"],
                "explanation": "적합값 대비 표준화 잔차의 분산(Scale-Location)을 보여줍니다.",
                "insight": (
                    "잔차 분산이 적합값 전 구간에서 일정한지 확인할 수 있습니다. "
                    "이상적인 경우 점들이 수평 띠처럼 일정하게 퍼져야 합니다."
                ),
                "check": (
                    "점들이 깔때기 모양으로 넓어지거나 좁아지는 패턴이 있는지 확인합니다. "
                    "등분산성이 깨졌다면 가중치 회귀(Weighted Regression)나 변수 변환이 필요합니다."
                )
            },
            {
                "name": "Cook’s Distance vs Order",
                "method": self.plot_cooks_distance,
                "valid_models": ["linear", "logit", "multilogit"],
                "explanation": "각 관측치의 Cook’s Distance를 순서대로 나타낸 그래프입니다.",
                "insight": (
                    "Cook’s Distance는 특정 관측치가 회귀계수 추정에 미치는 영향력을 나타냅니다. "
                    "값이 큰 관측치는 모형에 과도한 영향을 줄 수 있습니다."
                ),
                "check": (
                    "일반적으로 Cook’s D > 4/n이면 영향력이 큰 점으로 간주합니다. "
                    "이런 점은 데이터 오류나 특이 케이스일 수 있으므로 검토가 필요합니다."
                )
            },
            {
                "name": "Leverage vs Cook’s Distance",
                "method": self.plot_leverage_cooks,
                "valid_models": ["linear", "logit", "multilogit"],
                "explanation": "레버리지(Leverage)와 Cook’s Distance의 관계를 보여줍니다.",
                "insight": (
                    "레버리지가 큰 점은 독립변수 공간에서 극단적인 위치에 있는 관측치입니다. "
                    "Cook’s Distance도 크다면 고영향점(High Influence Point)으로 모형을 심각하게 왜곡할 수 있습니다."
                ),
                "check": (
                    "대부분의 점은 중앙에 분포해야 하며, 멀리 떨어진 점이 없는지 확인해야 합니다. "
                    "고영향점은 제거 또는 별도 모형 적용을 고려해야 합니다."
                )
            }
        ]

    def run(self):
        for chart in self.chart_definitions:
            if self.model_type in chart["valid_models"]:
                fig = chart["method"]()
                filename = f"{chart['name'].lower().replace(' ', '_').replace('’','')}.png"
                filepath = os.path.join(self.output_dir, filename)
                fig.savefig(filepath, dpi=120, bbox_inches="tight")
                plt.close(fig)

                self.charts_info.append({
                    "name": chart["name"],
                    "path": filepath,
                    "explanation": chart["explanation"],
                    "insight": chart["insight"],
                    "check": chart["check"]
                })

        # JSON 저장
        with open(os.path.join(self.output_dir, "info.json"), "w", encoding="utf-8") as f:
            json.dump(self.charts_info, f, ensure_ascii=False, indent=2)

    # ------------------- 차트 구현부 -------------------
    def plot_residual_vs_fitted(self):
        fig, ax = plt.subplots()
        ax.scatter(self.y_pred, self.residuals, alpha=0.7)
        ax.axhline(0, color="red", linestyle="--")
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "적합치", is_tick_set=False)
        ax.set_ylabel("잔차")
        _set_chart_title(ax, "잔차 대 적합치")
        return fig

    def plot_residual_vs_order(self):
        fig, ax = plt.subplots()
        sns.lineplot(x=range(len(self.residuals)), y=self.residuals, marker="o", ax=ax)
        ax.axhline(0, color="red", linestyle="--")
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "관측 순서", is_tick_set=False)
        ax.set_ylabel("잔차")
        _set_chart_title(ax, "잔차 대 순서")
        return fig

    def plot_histogram(self):
        fig, ax = plt.subplots()
        ax.hist(self.residuals, bins=20, edgecolor="black")
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "잔차", is_tick_set=False)
        ax.set_ylabel("빈도")
        _set_chart_title(ax, "잔차 히스토그램")
        return fig

    def plot_qqplot(self):
        fig, ax = plt.subplots()
        sm.qqplot(self.residuals, line="45", ax=ax)
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_title(ax, "잔차 Q-Q Plot")
        return fig

    def plot_scale_location(self):
        fitted = self.y_pred
        std_resid = self.residuals / np.std(self.residuals)
        fig, ax = plt.subplots()
        ax.scatter(fitted, np.sqrt(np.abs(std_resid)), alpha=0.7)
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "적합치", is_tick_set=False)
        ax.set_ylabel("√(|표준화된 잔차|)")
        _set_chart_title(ax, "Scale - Location")
        return fig

    def plot_cooks_distance(self):
        infl = self.model.get_influence()
        cooks_d = infl.cooks_distance[0]
        fig, ax = plt.subplots()
        ax.stem(np.arange(len(cooks_d)), cooks_d, basefmt=" ")
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "관측 순서", is_tick_set=False)
        ax.set_ylabel("Cook’s Distance")
        _set_chart_title(ax, "Cook’s Distance 대 순서")
        return fig

    def plot_leverage_cooks(self):
        infl = self.model.get_influence()
        leverage = infl.hat_matrix_diag
        cooks_d = infl.cooks_distance[0]
        fig, ax = plt.subplots()
        ax.scatter(leverage, cooks_d, alpha=0.7)
        ax.grid(True, linestyle='--', alpha=0.5)
        _set_chart_x_label(ax, "Leverage", is_tick_set=False)
        ax.set_ylabel("Cook’s Distance")
        _set_chart_title(ax, "Leverage 대 Cook’s Distance")
        return fig
