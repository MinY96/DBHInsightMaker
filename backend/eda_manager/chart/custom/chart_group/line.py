# pylint: disable=W0718, E1101
"""
Line(라인) 차트 생성기
"""
from typing import Dict, List
import os
from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from eda_manager.chart.chart_helper import (init_figure_axes,
                                            update_chart_with_common_option,
                                            save_chart_to_bytes,
                                            update_chart_y_axis,
                                            close_pyplot)

def update_axes_lines(ax, line_options: List[Dict[str, object]], y_data: pd.Series):
    """ 차트 내 수직/수평선 추가

    Args:
        ax (_type_): 차트
        line_options (List[Dict[str, object]]): 선 옵션 리스트
    """
    try:
        if not isinstance(line_options, list):
            return
        if line_options == "auto":
            return
        line_ops = None
        for ops in line_options:
            line_ops = {
                "color": ops["linecolor"],
                "linestyle": ops["linestyle"],
                "linewidth": int(ops["linewidth"])
            }
            value = None
            values = None
            text, text_va, text_ha = ops["text"], ops["text_va"], ops["text_ha"]
            text_rotate = int(ops["text_rotate"])
            text_x_pos, text_y_pos = 0, 0
            match ops["axis"]:
                case "수평":
                    mean, sigma = np.nanmean(y_data), np.nanstd(y_data)
                    match ops["kind"]:
                        case "최대값":
                            value = np.nanmax(y_data)
                        case "최소값":
                            value = np.nanmin(y_data)
                        case "평균값":
                            value = mean
                        case "중앙값":
                            value = np.nanmedian(y_data)
                        case "μ+1σ":
                            value = mean + sigma
                        case "μ+2σ":
                            value = mean + 2*sigma
                        case "μ+3σ":
                            value = mean + 3*sigma
                        case "μ-1σ":
                            value = mean - sigma
                        case "μ-2σ":
                            value = mean - 2*sigma
                        case "μ-3σ":
                            value = mean - 3*sigma
                        case "사용자 지정":
                            value = float(ops["custom_value"]) if ops["is_custom_double"]\
                                else datetime.strptime(ops["custom_dt"], "%Y-%m-%d %H:%M:%S")
                    line_ops.update({"y": value})
                    ax.axhline(**line_ops)
                    if (text is not None) & (text != ""):
                        match text_ha:
                            case "left":
                                text_x_pos = 0
                            case "center":
                                text_x_pos = len(y_data)//2
                            case "right":
                                text_x_pos = len(y_data)-1
                        if text_va == "bottom":
                            text_va = "top"
                        elif text_va == "top":
                            text_va = "bottom"
                        ax.text(text_x_pos, value, text,
                                ha=text_ha, va=text_va, rotation=text_rotate)
                case "수직":
                    match ops["kind"]:
                        case "최대값 인덱스(최초)":
                            value = np.nanargmax(y_data)
                        case "최대값 인덱스(전체)":
                            max_val = np.nanmax(y_data)
                            values = y_data[y_data==max_val].index.tolist()
                        case "최소값 인덱스(최초)":
                            value = np.nanargmin(y_data)
                        case "최소값 인덱스(전체)":
                            min_val = np.nanmin(y_data)
                            values = y_data[y_data==min_val].index.tolist()
                        case "사용자 지정":
                            value = float(ops["custom_value"]) if ops["is_custom_double"]\
                                else datetime.strptime(ops["custom_dt"], "%Y-%m-%d %H:%M:%S")
                    if value is not None:
                        line_ops.update({"x": value})
                        ax.axvline(**line_ops)
                    else:
                        for id_val in values:
                            value = id_val
                            line_ops.update({"x": id_val})
                            ax.axvline(**line_ops)
                    if (text is not None) & (text != ""):
                        match text_va:
                            case "bottom":
                                text_y_pos = np.nanmin(y_data)
                            case "center":
                                text_y_pos = np.nanmedian(y_data)
                            case "top":
                                text_y_pos = np.nanmax(y_data)
                        if text_ha == "left":
                            text_ha = "right"
                        elif text_ha == "right":
                            text_ha = "left"
                        ax.text(value, text_y_pos, text,
                                ha=text_ha, va=text_va, rotation=text_rotate)
    except Exception as e:
        print(e)
        return

def index_num_chart(
    project_dir: str,
    y_num: str,
    color: str, line_style: str, line_width: int,
    marker: str, marker_size: int,
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : 인덱스 vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"라인 차트 - 인덱스 vs {y_num}"
        df = pd.read_pickle(data_path)
        df.index.name = "Index"
        options = {"data": df, "x": "Index", "y": y_num}
        if color!="auto":
            options.update({"color": color})
        if line_style!="auto":
            options.update({"linestyle": line_style})
        if line_width!="auto":
            options.update({"linewidth": line_width})
        if marker!="auto":
            options.update({"marker": marker})
        if marker_size!="auto":
            options.update({"markersize": marker_size})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        sns.lineplot(**options)
        update_axes_lines(ax, lines, df[y_num])
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":"Index", "y_axis":y_num}, common_option)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def index_nums_chart(
    project_dir: str,
    y_nums: List[Dict[str, str]],
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : 인덱스 vs 수치형(N개) """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        is_unique_y_axis = len(np.unique([y_num["is_secondary_axis"] for y_num in y_nums]))==1
        if is_unique_y_axis:
            for y_num in y_nums:
                y_num["is_secondary_axis"] = False

        data_path = os.path.join(project_dir, 'data.pkl')
        df = pd.read_pickle(data_path)
        df.index.name = "Index"
        auto_title = f"라인 차트 - 인덱스 vs ({", ".join([y_num["column"] for y_num in y_nums])})"

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)

        y_axis_nm = common_option["y_axis_nm"]
        if y_axis_nm == "auto":
            y_axis_nm = "주축"
        for y_num in [y_num for y_num in y_nums if not y_num["is_secondary_axis"]]:
            column = y_num["column"]
            line_style, line_width = y_num["linestyle"], y_num["linewidth"]
            line_color = y_num["linecolor"]
            marker, marker_size = y_num["marker"], y_num["marker_size"]
            label = y_num["label"] if y_num["label"]!="auto" else y_num["column"]
            options = {"data": df, "x": "Index", "y":column, "label": label, "ax": ax}
            if line_color != "auto":
                options.update({"color": line_color})
            if line_style != "auto":
                options.update({"linestyle": line_style})
            if line_width != "auto":
                options.update({"linewidth": line_width})
            if marker != "auto":
                options.update({"marker": marker})
            if marker_size != "auto":
                options.update({"markersize": marker_size})
            sns.lineplot(**options)
            update_axes_lines(ax, lines, df[column])
        if not is_unique_y_axis:
            ax.legend(loc="upper left", title=y_axis_nm)
        else:
            ax.legend(loc="upper left")
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":"Index", "y_axis":"주축"}, common_option)

        if not is_unique_y_axis:
            ax2 = ax.twinx()
            y_axis2_nm = common_option["y_axis2_nm"]
            axis_font_size = common_option["axis_font_size"]
            axis_font_size = 12 if axis_font_size=="auto" else axis_font_size
            if y_axis2_nm == "auto":
                y_axis2_nm = "보조축"
            is_y_axis2_rotate = False
            y_axis2_rotate = common_option["y_axis2_rotate"]
            is_y_axis2_rotate = y_axis2_rotate != "auto"
            for y_num in [y_num for y_num in y_nums if y_num["is_secondary_axis"]]:
                column = y_num["column"]
                line_style, line_width = y_num["linestyle"], y_num["linewidth"]
                line_color = y_num["linecolor"]
                marker, marker_size = y_num["marker"], y_num["marker_size"]
                label = y_num["label"] if y_num["label"]!="auto" else y_num["column"]
                options = {"data": df, "x": "Index", "y":column, "label": label, "ax": ax2}
                if line_color != "auto":
                    options.update({"color": line_color})
                if line_style != "auto":
                    options.update({"linestyle": line_style})
                if line_width != "auto":
                    options.update({"linewidth": line_width})
                if marker != "auto":
                    options.update({"marker": marker})
                if marker_size != "auto":
                    options.update({"markersize": marker_size})
                sns.lineplot(**options)
                update_axes_lines(ax2, lines, df[column])
            update_chart_y_axis(ax2, y_axis2_nm, axis_font_size,
                                rotate_label=is_y_axis2_rotate, rotate=y_axis2_rotate)
            ax2.legend(loc="upper right", title=y_axis2_nm)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def index_num_cat_chart(
    project_dir: str,
    y_num: str, g_cat: str,
    line_width: int, marker_size: int, legend_pos: str,
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : 인덱스 vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"라인 차트 - 인덱스 vs {y_num}(by {g_cat})"
        df = pd.read_pickle(data_path)
        df.index.name = "Index"
        options = {"data": df, "x": "Index", "y": y_num,
                   "hue": g_cat, "markers": True }
        if len(df[g_cat].unique())<10:
            options.update({"style": g_cat})
        if line_width!="auto":
            options.update({"linewidth": line_width})
        if marker_size!="auto":
            options.update({"markersize": marker_size})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        sns.lineplot(**options)
        update_axes_lines(ax, lines, df[y_num])
        update_chart_with_common_option(ax, auto_title,
                                    {"x_axis":"Index", "y_axis":y_num}, common_option)
        if legend_pos != "auto":
            ax.legend(title=g_cat, loc=legend_pos)
        else:
            ax.legend(title=g_cat)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dt_num_chart(
    project_dir: str,
    x_dt: str, y_num: str,
    color: str, line_style: str, line_width: int,
    marker: str, marker_size: int,
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : DateTime vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"라인 차트 - {x_dt} vs {y_num}"
        df = pd.read_pickle(data_path)
        options = {"data": df, "x": x_dt, "y": y_num}
        if color!="auto":
            options.update({"color": color})
        if line_style!="auto":
            options.update({"linestyle": line_style})
        if line_width!="auto":
            options.update({"linewidth": line_width})
        if marker!="auto":
            options.update({"marker": marker})
        if marker_size!="auto":
            options.update({"markersize": marker_size})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        sns.lineplot(**options)
        update_axes_lines(ax, lines, df[y_num])
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_dt, "y_axis":y_num},
                                        common_option, is_x_dt=True)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dt_nums_chart(
    project_dir: str,
    x_dt: str, y_nums: List[Dict[str, str]],
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : DateTime vs 수치형(N개) """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        is_unique_y_axis = len(np.unique([y_num["is_secondary_axis"] for y_num in y_nums]))==1
        if is_unique_y_axis:
            for y_num in y_nums:
                y_num["is_secondary_axis"] = False

        data_path = os.path.join(project_dir, 'data.pkl')
        df = pd.read_pickle(data_path)
        auto_title = f"라인 차트 - {x_dt} vs ({", ".join([y_num["column"] for y_num in y_nums])})"

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)

        y_axis_nm = common_option["y_axis_nm"]
        if y_axis_nm == "auto":
            y_axis_nm = "주축"
        for y_num in [y_num for y_num in y_nums if not y_num["is_secondary_axis"]]:
            column = y_num["column"]
            line_style, line_width = y_num["linestyle"], y_num["linewidth"]
            line_color = y_num["linecolor"]
            marker, marker_size = y_num["marker"], y_num["marker_size"]
            label = y_num["label"] if y_num["label"]!="auto" else y_num["column"]
            options = {"data": df, "x": x_dt, "y":column, "label": label, "ax": ax}
            if line_color != "auto":
                options.update({"color": line_color})
            if line_style != "auto":
                options.update({"linestyle": line_style})
            if line_width != "auto":
                options.update({"linewidth": line_width})
            if marker != "auto":
                options.update({"marker": marker})
            if marker_size != "auto":
                options.update({"markersize": marker_size})
            sns.lineplot(**options)
            update_axes_lines(ax, lines, df[column])
        if not is_unique_y_axis:
            ax.legend(loc="upper left", title=y_axis_nm)
        else:
            ax.legend(loc="upper left")
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_dt, "y_axis":"주축"}, common_option,
                                        is_x_dt=True)

        if not is_unique_y_axis:
            ax2 = ax.twinx()
            y_axis2_nm = common_option["y_axis2_nm"]
            if y_axis2_nm == "auto":
                y_axis2_nm = "보조축"
            axis_font_size = common_option["axis_font_size"]
            axis_font_size = 12 if axis_font_size=="auto" else axis_font_size
            is_y_axis2_rotate = False
            y_axis2_rotate = common_option["y_axis2_rotate"]
            is_y_axis2_rotate = y_axis2_rotate != "auto"
            for y_num in [y_num for y_num in y_nums if y_num["is_secondary_axis"]]:
                column = y_num["column"]
                line_style, line_width = y_num["linestyle"], y_num["linewidth"]
                line_color = y_num["linecolor"]
                marker, marker_size = y_num["marker"], y_num["marker_size"]
                label = y_num["label"] if y_num["label"]!="auto" else y_num["column"]
                options = {"data": df, "x": x_dt, "y":column, "label": label, "ax": ax2}
                if line_color != "auto":
                    options.update({"color": line_color})
                if line_style != "auto":
                    options.update({"linestyle": line_style})
                if line_width != "auto":
                    options.update({"linewidth": line_width})
                if marker != "auto":
                    options.update({"marker": marker})
                if marker_size != "auto":
                    options.update({"markersize": marker_size})
                sns.lineplot(**options)
                update_axes_lines(ax2, lines, df[column])
            update_chart_y_axis(ax2, y_axis2_nm, axis_font_size,
                                rotate_label=is_y_axis2_rotate, rotate=y_axis2_rotate)
            ax2.legend(loc="upper right", title=y_axis2_nm)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dt_num_cat_chart(
    project_dir: str,
    x_dt: str, y_num: str, g_cat: str,
    line_width: int, marker_size: int,
    legend_pos: str,
    lines: List[Dict[str, str]],
    common_option: dict):
    """ 라인차트 : DateTime vs 수치형 Group by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"라인 차트 - {x_dt} vs {y_num}"
        df = pd.read_pickle(data_path)
        options = {"data": df, "x": x_dt, "y": y_num,
                   "hue": g_cat, "markers": True }
        if len(df[g_cat].unique())<10:
            options.update({"style": g_cat})
        if line_width!="auto":
            options.update({"linewidth": line_width})
        if marker_size!="auto":
            options.update({"markersize": marker_size})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        sns.lineplot(**options)
        update_axes_lines(ax, lines, df[y_num])
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_dt, "y_axis":y_num},
                                        common_option, is_x_dt=True)
        if legend_pos != "auto":
            ax.legend(title=g_cat, loc=legend_pos)
        else:
            ax.legend(title=g_cat)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
