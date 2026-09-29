# pylint: disable=W0718, W0613, E1101, C0104, C3001
"""
TimeSeries 시계열 차트 생성기
"""
from typing import Tuple
import os
from datetime import datetime
import pandas as pd
import seaborn as sns
from eda_manager.chart.chart_helper import (save_chart_to_bytes, close_pyplot, DBDREAM)

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

def split_datetime(dt: datetime) -> Tuple[str]:
    """ DateTime 분리 - 연/월/분기/주/일/시/분/초

    Args:
        data: datetime

    Returns:
        Tuple[str]: 분리된 시각 정보
    """
    return dt.year, f"{dt.strftime('%y')} {get_season(dt.month)}",\
        dt.strftime('%y %b'), dt.strftime('%yww%W'), dt.strftime('%y%m%d'),\
            dt.strftime('%y%m%d%H'),dt.strftime('%y%m%d %H:%M'),\
                dt.strftime('%y%m%d %H:%M:%S'),

def dist_datetime(
    project_dir: str, dt: str,
    common_option: dict):
    """ 시계열 히스토그램 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"{dt}(DateTime) 타입 별 분포"
        chart_nm = common_option.get("chart_nm", "auto")
        chart_fs = common_option.get("chart_nm_font_size", "auto")
        chart_fs = 15 if chart_fs=="auto" else chart_fs
        axis_fs = common_option.get("axis_font_size", 12)
        axis_fs = 12 if axis_fs=="auto" else axis_fs
        x_axis_rot = common_option.get("x_axis_rotate", "auto")
        x_axis_rot = 90 if x_axis_rot=="auto" else x_axis_rot
        if chart_nm is "auto":
            chart_nm = auto_title
        df = pd.read_pickle(data_path)
        dt_cols = ['year','season','month','week','day','hour','minute','second']
        df_dt = pd.DataFrame(df.sort_values(dt, ascending=True).reset_index(drop=True))
        df_dt[dt_cols] = df_dt.apply(
            lambda x: split_datetime(x[dt]), axis=1, result_type='expand')
        draw_cols = [col for col in dt_cols
                        if (len(df_dt[col].unique())<=30 and len(df_dt[col].unique())>1)]
        df_dt = df_dt[draw_cols]

        df_dt_type = None
        for col in df_dt.columns:
            temp = pd.DataFrame(df_dt[col])
            temp = temp.rename(columns={col: "dt_value"})
            temp["dt_type"] = col
            if df_dt_type is None:
                df_dt_type = temp
            else:
                df_dt_type = pd.concat([df_dt_type, temp], axis=0)
        df_dt_type["dt_value"] = df_dt_type["dt_value"].astype(str)

        def countplot_limited_x(data, color):
            label_fmt = lambda v: f"{v:,.0f}"
            order = data["dt_value"].unique()
            ax = sns.countplot(data=data, x="dt_value", order=order, color=color)
            for container in ax.containers:
                labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                ax.bar_label(container, label_type='edge', labels=labels)
            ax.set(xlabel=None)
            ax.tick_params(axis="x", rotation=x_axis_rot)
            ax.grid(True, axis="y", linestyle='--', alpha=.5)

        g = sns.FacetGrid(df_dt_type, col="dt_type", sharex=False, sharey=False, col_wrap=3)
        g.map_dataframe(countplot_limited_x)
        g.set_titles(col_template="{col_name} 기준 분포", fontweight="bold")
        g.fig.suptitle(chart_nm,
                        fontdict=dict(fontsize=chart_fs, fontweight='bold', fontproperties=DBDREAM))
        g.set_axis_labels(y_var="Count", fontsize=axis_fs, fontproperties=DBDREAM)
        g.tight_layout()
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
