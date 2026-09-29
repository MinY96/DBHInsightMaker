# pylint: disable=W0718, W0719, E1101, C0415
"""
Data 타입 별 차트 생성기
"""
from typing import List, Dict
from eda_manager.chart.custom.custom_dict import select_ui_chart_option

def get_column_type(col_info: Dict[str, object]):
    """ 컬럼 타입 반환

    Args:
        col_info (Dict[str, object]): 컬럼 정보

    Returns:
        string: 컬럼 타입
    """
    if col_info is not None:
        return col_info['Column'], col_info['ColumnType'], col_info['ColumnChar']
    return None, None, None

def is_numerical(col_type: str) -> bool:
    """컬럼 타입이 수치형인지 확인"""
    return col_type == 'Numerical'

def is_categorical(col_type: str) -> bool:
    """컬럼 타입이 범주형인지 확인"""
    return col_type == 'Categorical'

def is_datetime(col_type: str) -> bool:
    """컬럼 타입이 DateTime인지 확인"""
    return col_type == 'DateTime'

def matching_parameters_by_chart_group_type(
    chart_group: str, chart_type: str, col_nm: str):
    """ 차트 그룹, 타입에 해당하는 옵션/파라미터 매칭 """
    para_list = None
    if chart_group == "bar" and chart_type == "count":
        para_list = {
            "세로 바 차트(Count)": {"cat": col_nm, "orient": "y", "stat": "count",
                               "show_label": True, "use_etc": True},
            "세로 바 차트(Percent)": {"cat": col_nm, "orient": "y", "stat": "percent",
                                 "show_label": True, "use_etc": True}
        }
    elif chart_group == "bar" and chart_type == "pareto":
        para_list = {
            "파레토 차트": {"cat": col_nm, "use_etc": True}
        }
    elif chart_group == "proportion" and chart_type == "pie":
        para_list = {
            "파이 차트": {"cat": col_nm, "use_etc": True, "show_etc_detail": False},
            "파이 차트(기타 상세)": {"cat": col_nm, "use_etc": True, "show_etc_detail": True}
        }
    elif chart_group == "proportion" and chart_type == "treemap":
        para_list = {
            "트리 맵": {"cat": col_nm, "use_etc": True},
        }
    elif chart_group == "proportion" and chart_type == "waffle":
        para_list = {
            "와플 차트": {"cat": col_nm, "use_etc": True, "scale_type": "nearest"},
        }
    elif chart_group == "proportion" and chart_type == "wordcloud":
        para_list = {
            "WordCloud": {"cat": col_nm},
        }
    elif chart_group == "box" and chart_type == "num":
        para_list = {
            "Box 차트": {"num": col_nm, "orient": "y", "box_kind": "box"},
            "Violin 차트": {"num": col_nm, "orient": "y", "box_kind": "violin"},
            "Boxen 차트": {"num": col_nm, "orient": "y", "box_kind": "boxen"},
        }
    elif chart_group == "dist" and chart_type == "dist_num":
        para_list = {
            "KDE 차트": {"num": col_nm, "orient": "y", "dist_kind": "kde"},
            "히스토그램": {"num": col_nm, "orient": "y", "dist_kind": "hist"},
            "히스토그램 + KDE": {"num": col_nm, "orient": "y", "dist_kind": "hist", "kde": True},
        }
    elif chart_group == "line" and chart_type == "index_num":
        para_list = {
            "라인 차트(인덱스 기준)": {"y_num": col_nm},
        }
    elif chart_group == "point" and chart_type == "num":
        para_list = {
            "Strip 차트": {"num": col_nm, "orient": "y", "point_kind": "strip"},
            "Swarm 차트": {"num": col_nm, "orient": "y", "point_kind": "swarm"},
        }
    elif chart_group == "timeseries" and chart_type == "dist_dt":
        para_list = {
            "DateTime 타입 별 분포": {"dt": col_nm}
        }
    options, _ = select_ui_chart_option(chart_group, chart_type)
    options = options["Options"]
    return options, para_list

def get_column_charts(project_dir, chart_group, chart_type, options, para_list):
    """ 조건에 부합하는 차트 생성 """
    from eda_manager.chart.chart_handler import get_custom_chart
    results = []
    for chart_nm, para in para_list.items():
        chart_option = options.copy()
        for ops in chart_option:
            if ops["key"] in para:
                update_value = para[ops["key"]]
                ops["value"] = update_value
        result, _ = get_custom_chart(project_dir, chart_group, chart_type,
                                     chart_option, chart_nm=chart_nm)
        results.append(result)
    return results

def apply_custom_charts(project_dir: str, chart_group: str, chart_type: str, col_nm: str):
    """ 관련 파라미터 조회 후 관계형 차트 반환 프로세스 """
    options, para_list = matching_parameters_by_chart_group_type(chart_group, chart_type, col_nm)
    return get_column_charts(project_dir, chart_group, chart_type, options, para_list)

def column_charts(project_dir: str, col_info: Dict[str, object]) -> List[Dict[str, object]]:
    """ 입력받은 컬럼 타입에 해당하는 차트 리스트 반환 """
    results = []
    col_nm, col_type, col_char = get_column_type(col_info)
    # case 1 - 수치형/DateTime
    if is_numerical(col_type) and is_datetime(col_char):
        chart_group, chart_type = "timeseries", "dist_dt"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
    # case 2 - 수치형
    elif is_numerical(col_type):
        chart_group, chart_type = "line", "index_num"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "dist", "dist_num"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "box", "num"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "point", "num"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
    # case 3 - 범주형
    elif is_categorical(col_type):
        chart_group, chart_type = "proportion", "pie"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "proportion", "treemap"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "proportion", "waffle"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "proportion", "wordcloud"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "bar", "pareto"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
        chart_group, chart_type = "bar", "count"
        results += apply_custom_charts(project_dir, chart_group, chart_type, col_nm)
    if len(results) > 0:
        return results
    raise Exception

# class NumericalChart():
#     """ 수치형 데이터 시각화 클래스

#     Args:
#         col_info (Dict[str, object]): 컬럼 정보
#         df (pd.DataFrame): 데이터
#     """
#     def __init__(self, col_info: Dict[str, object], df: pd.DataFrame):
#         self.col_info = col_info
#         self.col_nm = col_info['Column']
#         self.data = df[col_info['Column']].dropna()
#         self.figsize_x = 10
#         self.figsize_y = 6

#     def charts(self, col_char: str) -> Dict[str, object]:
#         """ 수치형 차트 결과 반환
#         Args:
#             col_char (str): 컬럼 타입
#         Returns:
#             Dict[str, object]: 차트 결과
#         """
#         result = {}
#         if col_char == 'Discrete':
#             result['Box Plot'] = self.box_plot()
#         elif col_char == 'Continuous':
#             result['Box Plot'] = self.box_plot()
#         return [{'ChartName':k,
#                 'ImageBase64':v,
#                 'ChartFileName':f"{self.col_nm}-{k}"}
#                 for k,v in result.items()
#                 if v is not None]

#     def set_chart_title(self, ax: Axes, chart_nm: str):
#         """ 차트 제목 설정

#         Args:
#             ax (Axes): axis
#             chart_nm (str): 차트 종류
#         """
#         ax.set_title(label=f'{self.col_nm} - {chart_nm}',
#             fontdict=dict(fontproperties=DBDREAM))

#     def set_chart_x_label(self, ax: Axes, value_cnt: int):
#         """ 차트 x축 라벨 설정

#         Args:
#             ax (Axes): axis
#             value_cnt (int): 값 개수
#         """
#         ax.set_xlabel(self.col_nm, fontdict=dict(fontweight='bold'))
#         if value_cnt>10:
#             for tick in ax.get_xticklabels():
#                 tick.set_rotation(45)

#     def set_chart_y_label(self, ax: Axes):
#         """ 차트 y축 라벨 설정

#         Args:
#             ax (Axes): axis
#         """
#         y_min = float(self.col_info['Min'].replace(',',''))
#         y_max = float(self.col_info['Max'].replace(',',''))
#         if y_max - y_min > 1_000:
#             ax.yaxis.set_major_formatter(FuncFormatter(formatter_kmb))

#     def box_plot(self):
#         """ Box Plot 생성 """
#         img = None
#         try:
#             mean = float(self.col_info['Mean'].replace(',',''))
#             median = float(self.col_info['Median'].replace(',',''))
#             q1 = float(self.col_info['Q1'].replace(',',''))
#             q3 = float(self.col_info['Q3'].replace(',',''))
#             meanlineprops = dict(linestyle='--', linewidth=1, color='#ffcc00')
#             fig, ax = plt.subplots(figsize=(self.figsize_x,self.figsize_y))
#             box = ax.boxplot(self.data,
#                              notch=True, patch_artist=True,
#                              showmeans=True, meanline=True,
#                              meanprops=meanlineprops)
#             num_fliers = len(box["fliers"][0].get_ydata())
#             for element in box["boxes"]:
#                 element.set(color="black", linewidth=1, facecolor="#0099ff")
#             for element in box["medians"]:
#                 element.set(color="#ffcc00", linewidth=1)
#             for element in box["whiskers"]:
#                 element.set(color="black", linewidth=1)
#             for element in box["caps"]:
#                 element.set(color="black", linewidth=1)
#             for element in box["fliers"]:
#                 element.set(marker="o", markeredgecolor="firebrick", markersize=3)
#             self.set_chart_title(ax, 'Box Plot')
#             ax.set_xticks([1], [self.col_nm])
#             ax.set_xticklabels([self.col_nm], fontdict=dict(fontweight='bold'))
#             self.set_chart_y_label(ax)
#             ax.legend(handles=
#                 [
#                     Line2D([0], [0], color="#ffcc00", ls="--", lw=2, label=f"평균: {mean: ,.1f}"),
#                     Line2D([0], [0], color="#ffcc00", ls="-", lw=2, label=f"중앙값: {median: ,.1f}"),
#                     Line2D([0], [0], color="black", ls="-", lw=2, label=f"Q1(25%): {q1: ,.1f}"),
#                     Line2D([0], [0], color="black", ls="-", lw=2, label=f"Q3(75%): {q3: ,.1f}"),
#                     Line2D([0], [0], marker="o", color="w", markerfacecolor="w",
#                            markeredgecolor="firebrick", markersize=10,
#                            label=f"이상치: {num_fliers: ,}개"),
#                 ]
#             )
#             ax.grid(True, linestyle='--', alpha=.5)
#             fig.tight_layout()
#             img = save_chart_to_bytes(fig)
#         except Exception as e:
#             print(e)
#         close_pyplot()
#         return img
