# pylint: disable=W0718, W0719, E1101, C0415
"""
관계형 차트 생성기
"""
from typing import Dict, List
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

def get_relative_charts(project_dir, chart_group, chart_type, options, para_list):
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

def matching_parameters_by_chart_group_type(
    chart_group: str, chart_type: str, col_info: Dict[str, str]):
    """ 차트 그룹, 타입에 해당하는 옵션/파라미터 매칭 """
    col_order = ''.join(col_info.keys())
    para_list = None
    if col_order == "yg" and chart_group == "bar" and chart_type == "count_cat":
        y, g = col_info["y"], col_info["g"]
        para_list = {
            "Grouped Bar Chart(Count)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "stat": "count"},
            "Grouped Bar Chart(Percent)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "stat": "percent"},
            "Grouped Bar Chart(Proportion)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "stat": "proportion"},
            "Stacked Bar Chart(Count)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "stat": "count"},
            "Stacked Bar Chart(Percent)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "stat": "percent"},
            "Stacked Bar Chart(Proportion)": {"cat": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "stat": "proportion"},
        }
    elif col_order == "yg" and chart_group == "dist" and chart_type == "dist_num_cat":
        y, g = col_info["y"], col_info["g"]
        para_list = {
            "Histogram": {"num": y, "g_cat": g, "orient": "x",
            "fill": True, "dist_kind": "hist", "kde": True},
            "KDE Plot": {"num": y, "g_cat": g, "orient": "x",
            "fill": True, "dist_kind": "kde"},
        }
    elif col_order == "yg" and chart_group == "line" and chart_type == "index_num_cat":
        y, g = col_info["y"], col_info["g"]
        para_list = {
            "Line Chart": {"y_num": y, "g_cat": g},
        }
    elif col_order == "xg" and chart_group == "bar" and chart_type == "count_cat":
        x, g = col_info["x"], col_info["g"]
        para_list = {
            "Grouped Bar Chart(Count)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "grouped", "show_label": True,
             "label_pos": "edge", "stat": "count"},
            "Grouped Bar Chart(Percent)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "grouped", "show_label": True,
             "label_pos": "edge", "stat": "percent"},
            "Grouped Bar Chart(Proportion)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "grouped", "show_label": True,
             "label_pos": "edge", "stat": "proportion"},
            "Stacked Bar Chart(Count)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "stacked", "show_label": True,
             "label_pos": "center", "stat": "count"},
            "Stacked Bar Chart(Percent)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "stacked", "show_label": True,
             "label_pos": "center", "stat": "percent"},
            "Stacked Bar Chart(Proportion)": {"cat": x, "g_cat": g, "orient": "x",
            "group_type": "stacked", "show_label": True,
             "label_pos": "center", "stat": "proportion"},
        }
    elif col_order == "xy" and chart_group == "bar" and chart_type == "bar_cat_num":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Bar Chart(Avg)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "평균"},
            "Bar Chart(Sum)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "합계"},
            "Bar Chart(Max)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "최대"},
            "Bar Chart(Min)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "최소"},
            "Bar Chart(Med)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "중앙값"},
            "Bar Chart(Std)": {"cat": x, "num": y, "orient": "y",
            "show_label": True, "label_pos": "edge", "estimator": "표준편차"},
        }
    elif col_order == "xy" and chart_group == "box" and chart_type == "num_cat":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Grouped Box Plot": {"cat": x, "num": y, "box_kind": "box"},
            "Grouped Violin Plot": {"cat": x, "num": y, "box_kind": "violin"},
            "Grouped Boxen Plot": {"cat": x, "num": y, "box_kind": "boxen"},
        }
    elif col_order == "xy" and chart_group == "point" and chart_type == "num_cat":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Grouped Strip Plot": {"cat": x, "num": y, "point_kind": "strip"},
            "Grouped Swarm Plot": {"cat": x, "num": y, "point_kind": "swarm"},
        }
    elif col_order == "xyg" and chart_group == "bar" and chart_type == "bar_cat_num_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "Grouped Bar Chart(Avg)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "평균"},
            "Grouped Bar Chart(Sum)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "합계"},
            "Grouped Bar Chart(Max)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "최대"},
            "Grouped Bar Chart(Min)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "최소"},
            "Grouped Bar Chart(Med)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "중앙값"},
            "Grouped Bar Chart(Std)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "grouped", "show_label": True,
            "label_pos": "edge", "estimator": "표준편차"},
            "Stacked Bar Chart(Avg)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "평균"},
            "Stacked Bar Chart(Sum)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "합계"},
            "Stacked Bar Chart(Max)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "최대"},
            "Stacked Bar Chart(Min)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "최소"},
            "Stacked Bar Chart(Med)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "중앙값"},
            "Stacked Bar Chart(Std)": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "group_type": "stacked", "show_label": True,
            "label_pos": "center", "estimator": "표준편차"}
        }
    elif col_order == "xyg" and chart_group == "box" and chart_type == "num_cat_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "다중 Grouped Box Plot": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "box_kind": "box"},
            "다중 Grouped Violin Plot": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "box_kind": "violin"},
            "다중 Grouped Boxen Plot": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "box_kind": "boxen"},
        }
    elif col_order == "xyg" and chart_group == "point" and chart_type == "num_cat_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "다중 Grouped Strip Plot": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "point_kind": "strip"},
            "다중 Grouped Swarm Plot": {"cat": x, "num": y, "g_cat": g,
            "orient": "y", "point_kind": "swarm"},
        }
    elif col_order == "xg" and chart_group == "dist" and chart_type == "dist_num_cat":
        x, g = col_info["x"], col_info["g"]
        para_list = {
            "Histogram": {"num": x, "g_cat": g, "orient": "y",
            "fill": True, "dist_kind": "hist", "kde": True},
            "KDE Plot": {"num": x, "g_cat": g, "orient": "y",
            "fill": True, "dist_kind": "kde"},
        }
    elif col_order == "yx" and chart_group == "bar" and chart_type == "bar_cat_num":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Bar Chart(Avg)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "평균"},
            "Bar Chart(Sum)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "합계"},
            "Bar Chart(Max)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "최대"},
            "Bar Chart(Min)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "최소"},
            "Bar Chart(Med)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "중앙값"},
            "Bar Chart(Std)": {"cat": y, "num": x, "orient": "x",
            "show_label": True, "label_pos": "edge", "estimator": "표준편차"},
        }
    elif col_order == "yx" and chart_group == "box" and chart_type == "num_cat":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Grouped Box Plot": {"cat": y, "num": x, "orient": "x", "box_kind": "box"},
            "Grouped Violin Plot": {"cat": y, "num": x, "orient": "x", "box_kind": "violin"},
            "Grouped Boxen Plot": {"cat": y, "num": x, "orient": "x", "box_kind": "boxen"},
        }
    elif col_order == "yx" and chart_group == "point" and chart_type == "num_cat":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Grouped Strip Plot": {"cat": y, "num": x, "orient": "x", "point_kind": "strip"},
            "Grouped Swarm Plot": {"cat": y, "num": x, "orient": "x", "point_kind": "swarm"},
        }
    elif col_order == "yxg" and chart_group == "bar" and chart_type == "bar_cat_num_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "Grouped Bar Chart(Avg)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "평균"},
            "Grouped Bar Chart(Sum)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "합계"},
            "Grouped Bar Chart(Max)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "최대"},
            "Grouped Bar Chart(Min)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "최소"},
            "Grouped Bar Chart(Med)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "중앙값"},
            "Grouped Bar Chart(Std)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "grouped",
              "show_label": True, "label_pos": "edge", "estimator": "표준편차"},
            "Stacked Bar Chart(Avg)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "평균"},
            "Stacked Bar Chart(Sum)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "합계"},
            "Stacked Bar Chart(Max)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "최대"},
            "Stacked Bar Chart(Min)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "최소"},
            "Stacked Bar Chart(Med)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "중앙값"},
            "Stacked Bar Chart(Std)": {"cat": y, "num": x, "g_cat": g,
             "orient": "x", "group_type": "stacked",
              "show_label": True, "label_pos": "center", "estimator": "표준편차"}
        }
    elif col_order == "yxg" and chart_group == "box" and chart_type == "num_cat_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "다중 Grouped Box Plot": {"cat": y, "num": x, "g_cat": g,
            "orient": "x", "box_kind": "box"},
            "다중 Grouped Violin Plot": {"cat": y, "num": x, "g_cat": g,
            "orient": "x", "box_kind": "violin"},
            "다중 Grouped Boxen Plot": {"cat": y, "num": x, "g_cat": g,
            "orient": "x", "box_kind": "boxen"},
        }
    elif col_order == "yxg" and chart_group == "point" and chart_type == "num_cat_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "다중 Grouped Strip Plot": {"cat": y, "num": x, "g_cat": g,
            "orient": "x", "point_kind": "strip"},
            "다중 Grouped Swarm Plot": {"cat": y, "num": x, "g_cat": g,
            "orient": "x", "point_kind": "swarm"},
        }
    elif col_order == "xy" and chart_group == "scatter" and chart_type == "num_num":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Scatter Plot": {"x_num": x, "y_num": y},
            "Scatter Plot with Regression": {"x_num": x, "y_num": y, "reg_line": True},
        }
    elif col_order == "xy" and chart_group == "dist" and chart_type == "dist_num_num":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Heat Map": {"x_num": x, "y_num": y, "dist_kind": "hist"},
            "Heat Map(KDE)": {"x_num": x, "y_num": y, "dist_kind": "kde"},
        }
    elif col_order == "xyg" and chart_group == "scatter" and chart_type == "num_num_by_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "Grouped Scatter Plot": {"x_num": x, "y_num": y, "g_cat": g},
            "Grouped Scatter Plot with Regression": {"x_num": x, "y_num": y, "g_cat": g,
                                                     "reg_line": True},
        }
    elif col_order == "xyg" and chart_group == "dist" and chart_type == "dist_num_num_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "Grouped Heat Map": {"x_num": x, "y_num": y, "g_cat": g, "dist_kind": "hist"},
            "Grouped Heat Map(KDE)": {"x_num": x, "y_num": y, "g_cat": g, "dist_kind": "kde"},
        }
    elif col_order == "xyz" and chart_group == "scatter" and chart_type == "num_num_num":
        x, y, z = col_info["x"], col_info["y"], col_info["z"]
        para_list = {
            "3D Scatter Plot": {"x_num": x, "y_num": y, "z_num": z},
        }
    elif col_order == "xyz" and chart_group == "scatter" and chart_type == "num_num_num_stem":
        x, y, z = col_info["x"], col_info["y"], col_info["z"]
        para_list = {
            "3D Scatter Plot(Projection: X-axis)": {"x_num": x, "y_num": y, "z_num": z,
            "stem_axis": "x"},
            "3D Scatter Plot(Projection: Y-axis)": {"x_num": x, "y_num": y, "z_num": z,
            "stem_axis": "y"},
            "3D Scatter Plot(Projection: Z-axis)": {"x_num": x, "y_num": y, "z_num": z,
            "stem_axis": "z"},
        }
    elif col_order == "xyzg" and chart_group == "scatter" and chart_type == "num_num_num_by_cat":
        x, y, z, g = col_info["x"], col_info["y"], col_info["z"], col_info["g"]
        para_list = {
            "Grouped 3D Scatter Plot": {"x_num": x, "y_num": y, "z_num": z, "g_cat": g},
        }
    elif col_order == "xyzg" and chart_group == "scatter" and\
        chart_type == "num_num_num_stem_by_cat":
        x, y, z, g = col_info["x"], col_info["y"], col_info["z"], col_info["g"]
        para_list = {
            "Grouped 3D Scatter Plot(Projection: X-axis)":
            {"x_num": x, "y_num": y, "z_num": z, "g_cat": g, "stem_axis": "x"},
            "Grouped 3D Scatter Plot(Projection: Y-axis)":
            {"x_num": x, "y_num": y, "z_num": z, "g_cat": g, "stem_axis": "y"},
            "Grouped 3D Scatter Plot(Projection: Z-axis)":
            {"x_num": x, "y_num": y, "z_num": z, "g_cat": g, "stem_axis": "z"},
        }
    elif col_order == "xy" and chart_group == "line" and chart_type == "dt_num":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Time Series": {"x_dt": x, "y_num": y},
        }
    elif col_order == "xyg" and chart_group == "line" and chart_type == "dt_num_cat":
        x, y, g = col_info["x"], col_info["y"], col_info["g"]
        para_list = {
            "Grouped Time Series": {"x_dt": x, "y_num": y, "g_cat": g},
        }
    elif col_order == "xy" and chart_group == "proportion" and chart_type == "mosaic":
        x, y = col_info["x"], col_info["y"]
        para_list = {
            "Mosaic Plot": {"x_cat": x, "y_cat": y}
        }

    options, _ = select_ui_chart_option(chart_group, chart_type)
    options = options["Options"]
    return options, para_list

def apply_relative_charts(project_dir: str, chart_group: str,
                          chart_type: str, col_info: Dict[str, str]):
    """ 관련 파라미터 조회 후 관계형 차트 반환 프로세스 """
    options, para_list = matching_parameters_by_chart_group_type(chart_group, chart_type, col_info)
    return get_relative_charts(project_dir, chart_group, chart_type, options, para_list)

def relative_charts(
    project_dir: str,
    x_col_info: Dict[str, object],
    y_col_info: Dict[str, object],
    z_col_info: Dict[str, object],
    g_col_info: Dict[str, object]) -> List[Dict[str, object]]:
    """ 입력받은 컬럼 조합에 해당하는 차트 리스트 반환 """
    x_col, x_type, x_char = get_column_type(x_col_info)
    y_col, y_type, _ = get_column_type(y_col_info)
    z_col, z_type, _ = get_column_type(z_col_info)
    g_col, g_type, _ = get_column_type(g_col_info)
    not_null_cnt = len([c_type for c_type in [x_type, y_type, z_type, g_type]
                        if c_type is not None])
    results = []
    chart_group, chart_type = None, None
    # case 1(yg) - y: 범주 , group: 범주
    if (not_null_cnt==2) and is_categorical(y_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "bar", "count_cat", {"y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 2(yg) - y: 수치, group: 범주
    elif (not_null_cnt==2) and is_numerical(y_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "dist", "dist_num_cat", {"y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "line", "index_num_cat", {"y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 3(xg) - x: 범주, group: 범주
    elif (not_null_cnt==2) and is_categorical(x_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "bar", "count_cat", {"x":x_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 4(xy) - x: 범주, y: 수치
    elif (not_null_cnt==2) and is_categorical(x_type) and is_numerical(y_type):
        chart_group, chart_type, col_info = "bar", "bar_cat_num", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "box", "num_cat", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "point", "num_cat", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 5(xyg) - x: 범주, y: 수치, g: 범주
    elif (not_null_cnt==3) and is_categorical(x_type) and is_numerical(y_type)\
        and is_categorical(g_type):
        chart_group, chart_type, col_info = "bar", "bar_cat_num_cat",\
            {"x":x_col, "y":y_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "box", "num_cat_cat",\
            {"x":x_col, "y":y_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "point", "num_cat_cat",\
            {"x":x_col, "y":y_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 6(xg) - x: 수치, g: 범주
    elif (not_null_cnt==2) and is_numerical(x_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "dist", "dist_num_cat", {"x":x_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 7(yx) - x: 수치, y: 범주
    elif (not_null_cnt==2) and is_numerical(x_type) and is_categorical(y_type):
        chart_group, chart_type, col_info = "bar", "bar_cat_num", {"y":y_col, "x":x_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "box", "num_cat", {"y":y_col, "x":x_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "point", "num_cat", {"y":y_col, "x":x_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 8(yxg) - x: 수치, y: 범주, g: 범주
    elif (not_null_cnt==3) and is_numerical(x_type) and is_categorical(y_type)\
        and is_categorical(g_type):
        chart_group, chart_type, col_info = "bar", "bar_cat_num_cat",\
            {"y":y_col, "x":x_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "box", "num_cat_cat", {"y":y_col, "x":x_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "point", "num_cat_cat",\
            {"y":y_col, "x":x_col, "g": g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 9(xy) - x: 수치, y: 수치
    elif (not_null_cnt==2) and is_numerical(x_type) and is_numerical(y_type):
        chart_group, chart_type, col_info = "scatter", "num_num", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "dist", "dist_num_num", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 10(xyg) - x: 수치, y: 수치, g: 범주
    elif (not_null_cnt==3) and is_numerical(x_type) and is_numerical(y_type)\
        and is_categorical(g_type):
        chart_group, chart_type, col_info = "scatter", "num_num_by_cat",\
            {"x":x_col, "y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "dist", "dist_num_num_cat",\
            {"x":x_col, "y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 11(xyz) - x: 수치, y: 수치, z: 수치
    elif (not_null_cnt==3) and is_numerical(x_type) and is_numerical(y_type)\
        and is_numerical(z_type):
        chart_group, chart_type, col_info = "scatter", "num_num_num",\
            {"x":x_col, "y":y_col, "z":z_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "scatter", "num_num_num_stem",\
            {"x":x_col, "y":y_col, "z":z_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 12(xyzg) - x: 수치, y: 수치, z: 수치, g: 범주
    elif (not_null_cnt==4) and is_numerical(x_type) and is_numerical(y_type)\
        and is_numerical(z_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "scatter", "num_num_num_by_cat",\
            {"x":x_col, "y":y_col, "z":z_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
        chart_group, chart_type, col_info = "scatter", "num_num_num_stem_by_cat",\
            {"x":x_col, "y":y_col, "z":z_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 13 - x: DateTime, y: 수치
    elif (not_null_cnt==2) and is_numerical(x_type) and is_datetime(x_char)\
        and is_numerical(y_type):
        chart_group, chart_type, col_info = "line", "dt_num", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 14 - x: DateTime, y: 수치, g: 범주
    elif (not_null_cnt==3) and is_numerical(x_type) and is_datetime(x_char)\
        and is_numerical(y_type) and is_categorical(g_type):
        chart_group, chart_type, col_info = "line", "dt_num_cat", {"x":x_col, "y":y_col, "g":g_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    # case 15(xy) - x: 범주, y: 범주
    elif (not_null_cnt==2) and is_categorical(x_type) and is_categorical(y_type):
        chart_group, chart_type, col_info = "proportion", "mosaic", {"x":x_col, "y":y_col}
        results += apply_relative_charts(project_dir, chart_group, chart_type, col_info)
    if len(results) > 0:
        return results
    raise Exception
