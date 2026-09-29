# pylint: disable=W0718
"""
차트 관련 헬퍼 메소드
"""
from typing import Tuple
import os
import io
import base64
from datetime import datetime
import pandas as pd
from matplotlib.pyplot import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation
from fonts import get_project_font

FONT_GOTHIC_PATH, FONT_DREAM_PATH = get_project_font()

DBGOTHIC = fm.FontProperties(fname=FONT_GOTHIC_PATH)
DBDREAM = fm.FontProperties(fname=FONT_DREAM_PATH)
fm.fontManager.addfont(FONT_GOTHIC_PATH)
fm.fontManager.addfont(FONT_DREAM_PATH)

plt.rcParams['font.family'] = DBGOTHIC.get_name()
plt.rcParams['axes.unicode_minus'] = False

def _format_scientific(x: float, decimals: int=1) -> str:
    s = f"{x:.{decimals}E}"
    mant, exp = s.split('E')
    exp = str(int(exp))
    return mant + 'E' + exp

def formatter_kmb(x: float, _):
    """ 차트 축 표기 설정 """
    if isinstance(x, str):
        return x
    if x == 0 or x == -0.0:
        return "0"
    abs_x = abs(x)
    if abs_x < 1:
        if abs_x >= 1e-2:
            s = f"{x:.2f}"
            if float(s) == 0.0:
                return "0"
            s = s.rstrip('0').rstrip('.')
            return s
        else:
            return _format_scientific(x, decimals=1)
    if abs_x < 1000:
        if abs_x.is_integer():
            return str(int(x))
        else:
            s = f"{x:.2f}"
            s = s.rstrip('0').rstrip('.')
            return s
    if abs_x >= 1e12:
        return _format_scientific(x, decimals=1)
    units = (('K', 1e3), ('M', 1e6), ('B', 1e9))
    for unit, factor in units:
        if abs_x < factor * 1000:
            scaled = x / factor
            s = f"{scaled:.2f}"
            # s = f"{scaled:.1f}"
            if '.' in s:
                s = s.rstrip('0').rstrip('.')
            return s + unit
    return _format_scientific(x, decimals=1)

def close_pyplot():
    """pyplot 종료"""
    plt.cla()
    plt.clf()
    plt.close()

def save_chart_to_file(fig: Figure, save_path: str) -> bool:
    """ 차트 파일로 저장 """
    is_save = False
    try:
        fig.savefig(save_path)
        is_save = os.path.exists(save_path)
    except Exception as e:
        print(e)
    return is_save

def save_chart_to_bytes(fig: Figure) -> str:
    """ 차트 바이트로 저장

    Args:
        fig (Figure): 차트 Figure

    Returns:
        str: img_base64
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def save_gif_chart_to_bytes(project_dir: str, ani: FuncAnimation) -> str:
    """ 차트 바이트로 저장

    Args:
        project_dir (str): 프로젝트 경로
        fig (Figure): 차트 Figure

    Returns:
        str: img_base64
    """
    temp_dir = os.path.join(project_dir, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, "animation.gif")
    ani.save(file_path, writer="pillow")
    buf = io.BytesIO()
    with open(file_path, 'rb') as f:
        buf.write(f.read())
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    # os.remove(file_path)
    return img_base64

def get_season(month: int) -> str:
    """ 월 분기 변환

    Args:
        month (int): 월

    Returns:
        str: 분기
    """
    if month in [1,2,3]:
        return 'Q1'
    elif month in [4,5,6]:
        return 'Q2'
    elif month in [7,8,9]:
        return 'Q3'
    else:
        return 'Q4'

def split_datetime(data: datetime) -> Tuple[str]:
    """ DateTime 분리 - 연/월/분기/주/일/시/분/초

    Args:
        data: datetime

    Returns:
        Tuple[str]: 분리된 시각 정보
    """
    return data.year, f"{data.strftime('%y')} {get_season(data.month)}",\
        data.strftime('%y %b'), data.strftime('%yww%W'), data.strftime('%y%m%d'),\
            data.strftime('%y%m%d%H'),data.strftime('%y%m%d %H:%M'),\
                data.strftime('%y%m%d %H:%M:%S'),

def split_prop_others(df: pd.DataFrame, cat: str, use_etc: bool=True, category_count: int=7):
    """ 비중, 기타 항목 구분 """
    series = df[cat]
    df_prop = pd.DataFrame(series.value_counts()).reset_index()
    total = df_prop["count"].sum()
    df_prop["cumsum"] = df_prop["count"].cumsum()
    df_prop["ratio"] = df_prop["count"] / total
    df_prop["cumratio"] = df_prop["cumsum"] / total
    df_others = None
    if not use_etc:
        return df_prop, df_others

    # 1. 카테고리수 7개로 맞춤
    if len(df_prop)>category_count:
        df_others = df_prop[6:].copy(deep=True).reset_index(drop=True)[[cat, "count", "ratio"]]
        other_sum = df_prop[6:]["count"].sum()
        df_prop = df_prop[:7]
        df_prop.loc[6, cat] = "기타"
        df_prop.loc[6, "count"] = other_sum
        df_prop["cumsum"] = df_prop["count"].cumsum()
        df_prop["ratio"] = df_prop["count"] / total
        df_prop["cumratio"] = df_prop["cumsum"] / total

    # 2. 1% 미만 항목 기타로 조정
    small_props = df_prop[df_prop["ratio"]<0.01]
    if len(small_props)>0:
        if len(df_prop[df_prop[cat]=="기타"]) == 0:
            df_prop = pd.concat(
                [
                    df_prop,
                    pd.DataFrame([{cat: "기타", "count":0,
                                   "cumsum":0, "ratio": 0.0, "cumratio": 0.0}])
                ],
                ignore_index=True)
        for row_index, row in small_props.iterrows():
            row_count = int(row["count"])
            row_ratio = float(row["ratio"])
            row_para = row[cat]
            df_prop.loc[df_prop[cat]=="기타", "count"] += row_count
            if df_others is not None:
                df_others = pd.concat(
                    [
                        df_others,
                        pd.DataFrame([{cat: row_para,
                                       "count": row_count, "ratio": row_ratio}])
                    ],
                    ignore_index=True
                )
            else:
                df_others = pd.DataFrame([{cat: row_para,
                                           "count": row_count, "ratio": row_ratio}])
            df_prop.drop(row_index, inplace=True)

    # 3. 누적 비율 95% 이상인 항목 기타로 조정
    outers = df_prop[df_prop[df_prop["cumratio"]>0.95].first_valid_index()+1:]
    small_props = outers[outers[cat]!="기타"]
    if len(small_props)>0:
        if len(df_prop[df_prop[cat]=="기타"]) == 0:
            df_prop = pd.concat(
                [
                    df_prop,
                    pd.DataFrame([{cat: "기타", "count":0,
                                   "cumsum":0, "ratio": 0.0, "cumratio": 0.0}])
                ],
                ignore_index=True)
        for row_index, row in small_props.iterrows():
            row_count = int(row["count"])
            row_ratio = float(row["ratio"])
            row_para = row[cat]
            df_prop.loc[df_prop[cat]=="기타", "count"] += row_count
            if df_others is not None:
                df_others = pd.concat(
                    [
                        df_others,
                        pd.DataFrame([{cat: row_para,
                                       "count": row_count, "ratio": row_ratio}])
                    ],
                    ignore_index=True
                )
            else:
                df_others = pd.DataFrame([{cat: row_para,
                                           "count": row_count, "ratio": row_ratio}])
            df_prop.drop(row_index, inplace=True)

    df_prop.reset_index(drop=True, inplace=True)
    df_prop["cumsum"] = df_prop["count"].cumsum()
    df_prop["ratio"] = df_prop["count"] / total
    df_prop["cumratio"] = df_prop["cumsum"] / total
    if df_others is not None:
        df_others = df_others.sort_values("count", ascending=False).reset_index(drop=True)
    return df_prop, df_others

def allocate_key_value(custom_dict: dict, key: str, value: object) -> dict:
    """ 딕셔너리에 값이 None이 아니면 입력받은 key로 할당 """
    if value is not None:
        custom_dict[key] = value
    return custom_dict

def common_option(
    chart_nm: str=None, chart_nm_font_size: int=None,
    x_axis_nm: str=None, y_axis_nm: str=None, z_axis_nm: str=None, axis_font_size: int=None,
    y_axis2_nm: str=None,
    group_nm: str=None,
    x_axis_rotate: int=None, y_axis_rotate: int=None, z_axis_rotate: int=None,
    y_axis2_rotate: int=None,
    x_axis_lim_min: float=None, x_axis_lim_max: float=None,
    x_axis_lim_min_dt: datetime=None, x_axis_lim_max_dt: datetime=None,
    y_axis_lim_min: float=None, y_axis_lim_max: float=None,
    x_size: int=None, y_size: int=None):
    """ 차트 기본 옵션 """
    option = {}
    option = allocate_key_value(option, "chart_nm", chart_nm)
    option = allocate_key_value(option, "chart_nm_font_size", chart_nm_font_size)
    option = allocate_key_value(option, "x_axis_nm", x_axis_nm)
    option = allocate_key_value(option, "y_axis_nm", y_axis_nm)
    option = allocate_key_value(option, "y_axis2_nm", y_axis2_nm)
    option = allocate_key_value(option, "z_axis_nm", z_axis_nm)
    option = allocate_key_value(option, "axis_font_size", axis_font_size)
    option = allocate_key_value(option, "group_nm", group_nm)
    option = allocate_key_value(option, "x_axis_rotate", x_axis_rotate)
    option = allocate_key_value(option, "y_axis_rotate", y_axis_rotate)
    option = allocate_key_value(option, "y_axis2_rotate", y_axis2_rotate)
    option = allocate_key_value(option, "z_axis_rotate", z_axis_rotate)
    option = allocate_key_value(option, "x_axis_lim_min", x_axis_lim_min)
    option = allocate_key_value(option, "x_axis_lim_max", x_axis_lim_max)
    option = allocate_key_value(option, "x_axis_lim_min_dt", x_axis_lim_min_dt)
    option = allocate_key_value(option, "x_axis_lim_max_dt", x_axis_lim_max_dt)
    option = allocate_key_value(option, "y_axis_lim_min", y_axis_lim_min)
    option = allocate_key_value(option, "y_axis_lim_max", y_axis_lim_max)
    option = allocate_key_value(option, "x_size", x_size)
    option = allocate_key_value(option, "y_size", y_size)
    return option

def init_figure_axes(size_x, size_y, dimension="2d", ncols=0, sharey=False, sharex=False):
    """ Figure, Axes 초기화 """
    fig, ax = None, None
    if (size_x=="auto") and (size_y=="auto"):
        if dimension == "3d":
            fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),
                                   layout="constrained")
        elif ncols>0:
            fig, ax = plt.subplots(layout='constrained', ncols=ncols, sharey=sharey, sharex=sharex)
        else:
            fig, ax = plt.subplots(layout='constrained', sharey=sharey, sharex=sharex)
    elif size_x=="auto":
        if dimension == "3d":
            fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),
                                   figsize=(size_y, size_y),
                                   layout="constrained")
        elif ncols>0:
            fig, ax = plt.subplots(figsize=(size_y, size_y), layout='constrained',
                                   ncols=ncols, sharey=sharey, sharex=sharex)
        else:
            fig, ax = plt.subplots(figsize=(size_y, size_y), layout='constrained',
                                   sharey=sharey, sharex=sharex)
    elif size_y=="auto":
        if dimension == "3d":
            fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),
                                   figsize=(size_x, size_x),
                                   layout="constrained")
        elif ncols>0:
            fig, ax = plt.subplots(figsize=(size_x, size_x), layout='constrained',
                                   ncols=ncols, sharey=sharey, sharex=sharex)
        else:
            fig, ax = plt.subplots(figsize=(size_x, size_x), layout='constrained',
                                   sharey=sharey, sharex=sharex)
    else:
        if dimension == "3d":
            fig, ax = plt.subplots(subplot_kw=dict(projection="3d"),
                                   figsize=(size_x, size_y),
                                   layout="constrained")
        elif ncols>0:
            fig, ax = plt.subplots(figsize=(size_x, size_y), layout='constrained',
                                   ncols=ncols, sharey=sharey, sharex=sharex)
        else:
            fig, ax = plt.subplots(figsize=(size_x, size_y), layout='constrained',
                                   sharey=sharey, sharex=sharex)
    return fig, ax

def update_chart_y_axis(ax, y_title: str, y_title_font_size: int,
                        rotate_label: bool=False, rotate: int=0):
    """ Y축 업데이트 """
    ax.set_ylabel(y_title, fontdict=dict(fontsize=y_title_font_size, fontweight='bold'))
    if rotate_label:
        ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), rotation=rotate, ha='center')
    ax.yaxis.set_major_formatter(FuncFormatter(formatter_kmb))

def update_chart_with_common_option(ax, auto_title: str, column_info: dict, common: dict,
                                    is_x_dt: bool=False, is_y_dt: bool=False,
                                    pass_title: bool=False):
    """ 생성한 차트 내 기본 옵션 설정 """
    # 그리드 설정
    ax.grid(True, linestyle='--', alpha=.5)
    axis_tick_font = "Malgun Gothic" # sans-serif, Malgun Gothic
    chart_nm_font_size = common.get("chart_nm_font_size", 15)
    chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size
    axis_font_size = common.get("axis_font_size", 12)
    axis_font_size = 12 if axis_font_size=="auto" else axis_font_size

    # 1. 차트 제목 설정
    if (not pass_title) and ("chart_nm" in common):
        chart_nm = common.get("chart_nm", None)
        chart_nm = auto_title if chart_nm=="auto" else chart_nm
        ax.set_title(chart_nm, fontdict=dict(fontsize=chart_nm_font_size,
            fontweight='bold', fontproperties=DBDREAM))

    # 2. X축 제목 설정
    if "x_axis_nm" in common:
        x_title = common.get("x_axis_nm", None)
        x_title = column_info["x_axis"] if x_title=="auto" else x_title
        ax.set_xlabel(x_title, fontdict=dict(fontsize=axis_font_size,
            fontweight='bold', fontproperties=DBGOTHIC))

    # 3. Y축 제목 설정
    if "y_axis_nm" in common:
        y_title = common.get("y_axis_nm", None)
        y_title = column_info["y_axis"] if y_title=="auto" else y_title
        ax.set_ylabel(y_title, fontdict=dict(fontsize=axis_font_size,
            fontweight='bold', fontproperties=DBGOTHIC))

    # 4. Z축 제목 설정
    if "z_axis_nm" in common:
        z_title = common.get("z_axis_nm", None)
        z_title = column_info["z_axis"] if z_title=="auto" else z_title
        ax.set_zlabel(z_title, fontdict=dict(fontsize=axis_font_size,
            fontweight='bold', fontproperties=DBGOTHIC))

    # 5. X축 범위 설정
    if ("x_axis_lim_min" in common) & ("x_axis_lim_max" in common):
        x_min, x_max = common.get("x_axis_lim_min", None), common.get("x_axis_lim_max", None)
        if x_min != "auto" and x_max != "auto":
            ax.set_xlim(float(x_min), float(x_max))
        elif x_min != "auto":
            ax.set_xlim(left=float(x_min))
        elif x_max != "auto":
            ax.set_xlim(right=float(x_max))

    # 5-1. X축 시계열 범위 설정
    if ("x_axis_lim_min_dt" in common) & ("x_axis_lim_max_dt" in common):
        x_min, x_max = common.get("x_axis_lim_min_dt", None), common.get("x_axis_lim_max_dt", None)
        if (x_min is not None and x_min != "auto") and (x_max is not None and x_max != "auto"):
            ax.set_xlim(datetime.strptime(x_min, "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime(x_max, "%Y-%m-%d %H:%M:%S"))
        elif (x_min is not None and x_min != "auto"):
            ax.set_xlim(left=datetime.strptime(x_min, "%Y-%m-%d %H:%M:%S"))
        elif (x_max is not None and x_max != "auto"):
            ax.set_xlim(right=datetime.strptime(x_max, "%Y-%m-%d %H:%M:%S"))

    # 6. Y축 범위 설정
    if ("y_axis_lim_min" in common) & ("y_axis_lim_max" in common):
        y_min, y_max = common.get("y_axis_lim_min", None), common.get("y_axis_lim_max", None)
        if y_min != "auto" and y_max != "auto":
            ax.set_ylim(float(y_min), float(y_max))
        elif y_min != "auto":
            ax.set_ylim(bottom=float(y_min))
        elif y_max != "auto":
            ax.set_ylim(top=float(y_max))

    # 7. X축 라벨 설정
    if "x_axis_rotate" in common:
        x_angle = common.get("x_axis_rotate", None)
        x_angle = 0 if x_angle == "auto" else x_angle
        ax.set_xticklabels(ax.get_xticklabels(), rotation=x_angle,
                           ha='center', family=axis_tick_font)
        if not is_x_dt:
            ax.xaxis.set_major_formatter(FuncFormatter(formatter_kmb))

    # 8. Y축 라벨 설정
    if "y_axis_rotate" in common:
        y_angle = common.get("y_axis_rotate", None)
        y_angle = 0 if y_angle == "auto" else y_angle
        ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), rotation=y_angle,
                      ha='right', family=axis_tick_font)
        if not is_y_dt:
            ax.yaxis.set_major_formatter(FuncFormatter(formatter_kmb))

    # 9. Z축 라벨 설정
    if "z_axis_rotate" in common:
        z_angle = common.get("z_axis_rotate", None)
        z_angle = 0 if z_angle == "auto" else z_angle
        ax.set_zticks(ax.get_zticks(), ax.get_zticklabels(), rotation=z_angle,
                      ha='center', family=axis_tick_font)
        ax.zaxis.set_major_formatter(FuncFormatter(formatter_kmb))
