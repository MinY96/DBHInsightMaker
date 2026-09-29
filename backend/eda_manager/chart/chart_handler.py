# pylint: disable=W0718, C0415
"""
차트 처리 메소드
"""

from typing import Dict, List, Tuple
import os
import matplotlib
from eda_manager.chart.single import column_charts
from eda_manager.chart.relative import relative_charts
from eda_manager.chart.custom.custom_dict import decode_ui_chart_opiton
from helper import read_json_to_dict

matplotlib.use("agg")

def select_column_info(col_infos: List[Dict[str, object]], col_nm: str):
    """ 일치하는 컬럼 정보 반환

    Args:
        col_infos (List[Dict[str, object]]): 컬럼 정보 리스트
        col_nm (str): 조회할 컬럼 명
    """
    if col_nm is None:
        return None
    for col_info in col_infos:
        if col_info['Column'] == col_nm:
            return col_info
    return None

def get_column_charts(
    project_dir: str, col: str) -> List[Dict[str, object]]:
    """ 선택한 컬럼의 타입에 해당하는 차트 생성 """
    result, error = None, None
    column_info_path = os.path.join(project_dir, "column_info.json")
    col_infos = read_json_to_dict(column_info_path)
    col_info = select_column_info(col_infos, col)
    try:
        result = column_charts(project_dir, col_info)
    except Exception as e:
        print(e)
        error = '지원되지 않는 컬럼 조합입니다.'
    return result, error

def get_relative_chart(
    project_dir: str, col_x: str, col_y: str, col_z: str, col_g: str) -> List[Dict[str, object]]:
    """ 선택한 컬럼 조합에 해당하는 관계형 차트 생성 """
    result, error = None, None
    column_info_path = os.path.join(project_dir, "column_info.json")
    col_infos = read_json_to_dict(column_info_path)
    col_x_info = select_column_info(col_infos, col_x)
    col_y_info = select_column_info(col_infos, col_y)
    col_z_info = select_column_info(col_infos, col_z)
    col_g_info = select_column_info(col_infos, col_g)
    try:
        result = relative_charts(project_dir, col_x_info, col_y_info, col_z_info, col_g_info)
    except Exception as e:
        print(e)
        error = '지원되지 않는 컬럼 조합입니다.'
    return result, error

def convert_chart_option_type(key: str, value: str,
                              value_type: str, special_ops: List[Tuple[str, object]]=None):
    """ 옵션 타입 변환

    Args:
        value (str): string 형식의 값
        value_type (str): 기존 타입
    """
    if special_ops is not None:
        for special_key,  special_val in special_ops:
            if (key == special_key) & (special_val is not None):
                return special_val
    if value == "auto":
        return "auto"
    match value_type:
        case "string":
            return value
        case "int":
            return int(value)
        case "bool":
            return value in [True, 'true', 'True', 1]
    return value

def get_custom_chart(
    project_dir: str, chart_group: str, chart_type: str,
    options: List[Dict[str, str]], chart_nm: str="CustomChart"):
    """ 커스텀 차트 생성

    Args:
        project_dir (str): 프로젝트 경로
        chart_group (str): 차트 그룹명
        chart_type (str): 차트 타입
        options (List[Dict[str, str]]): 옵션 리스트
    """
    result, error = None, None
    try:
        options = {ops["key"]:convert_chart_option_type(ops["key"], ops["value"],
                                            ops["type"], [("lines", ops.get("lines", None)),
                                                          ("y_nums", ops.get("columns", None))])
                   for ops in options}
        options.update({"project_dir": project_dir})
        img_type = "png"
        if "gif" in options:
            img_type = "png" if options["gif"] in ["auto", False] else "gif"
        dec_option = decode_ui_chart_opiton(chart_group, chart_type, options)
        chart_func = None
        match chart_group:
            case "scatter":
                from eda_manager.chart.custom.chart_group import scatter
                match chart_type:
                    case "num_num":
                        chart_func = scatter.num_num_chart
                    case "num_num_by_cat":
                        chart_func = scatter.num_num_by_cat_chart
                    case "num_num_num":
                        chart_func = scatter.num_num_num_chart
                    case "num_num_num_by_cat":
                        chart_func = scatter.num_num_num_by_cat_chart
                    case "num_num_num_stem":
                        chart_func = scatter.stem_num_num_num_chart
                    case "num_num_num_stem_by_cat":
                        chart_func = scatter.stem_num_num_num_by_cat_chart
            case "line":
                from eda_manager.chart.custom.chart_group import line
                match chart_type:
                    case "index_num":
                        chart_func = line.index_num_chart
                    case "index_nums":
                        chart_func = line.index_nums_chart
                    case "index_num_cat":
                        chart_func = line.index_num_cat_chart
                    case "dt_num":
                        chart_func = line.dt_num_chart
                    case "dt_nums":
                        chart_func = line.dt_nums_chart
                    case "dt_num_cat":
                        chart_func = line.dt_num_cat_chart
            case "bar":
                from eda_manager.chart.custom.chart_group import bar
                match chart_type:
                    case "pareto":
                        chart_func = bar.pareto
                    case "count":
                        chart_func = bar.count
                    case "count_cat":
                        chart_func = bar.count_cat
                    case "bar_cat_num":
                        chart_func = bar.bar_cat_num
                    case "bar_cat_num_cat":
                        chart_func = bar.bar_cat_num_cat
            case "box":
                from eda_manager.chart.custom.chart_group import box
                match chart_type:
                    case "num":
                        dec_option.update({"cat": None, "g_cat": None,
                                           "large_g_cat": None, "gap": "auto"})
                    case "num_cat":
                        dec_option.update({"g_cat": None, "large_g_cat": None, "gap": "auto"})
                    case "num_cat_cat":
                        dec_option.update({"color": "auto"})
                chart_func = box.box
            case "point":
                from eda_manager.chart.custom.chart_group import point
                match chart_type:
                    case "num":
                        dec_option.update({"cat": None, "g_cat": None, "large_g_cat": None})
                    case "num_cat":
                        dec_option.update({"g_cat": None, "large_g_cat": None})
                    case "num_cat_cat":
                        dec_option.update({"color": "auto"})
                chart_func = point.point
            case "dist":
                from eda_manager.chart.custom.chart_group import distribution
                match chart_type:
                    case "dist_num":
                        chart_func = distribution.dist_num
                    case "dist_num_cat":
                        chart_func = distribution.dist_num_cat
                    case "dist_num_num":
                        chart_func = distribution.dist_num_num
                    case "dist_num_num_cat":
                        chart_func = distribution.dist_num_num_cat
                    case "dist_cat_cat_num":
                        chart_func = distribution.dist_cat_cat_num
            case "proportion":
                from eda_manager.chart.custom.chart_group import proportion
                match chart_type:
                    case "pie":
                        chart_func = proportion.pie_chart
                    case "wordcloud":
                        chart_func = proportion.wordcloud_chart
                    case "waffle":
                        chart_func = proportion.waffle_chart
                    case "treemap":
                        chart_func = proportion.treemap_chart
                    case "mosaic":
                        chart_func = proportion.mosaic_chart
            case "timeseries":
                from eda_manager.chart.custom.chart_group import timeseries
                match chart_type:
                    case "dist_dt":
                        chart_func = timeseries.dist_datetime
        img_bytes = chart_func(**dec_option)
        result = {
            "ChartName": chart_nm,
            "ImageBase64": img_bytes,
            "ChartFileName": f"{chart_group}-{chart_type}.{img_type}"
        }
    except Exception as e:
        error = str(e)
    return result, error
