# pylint: disable=W0613, W0718, E1101
"""
분포형 차트 생성기
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
from eda_manager.chart.chart_helper import (
    init_figure_axes,
    update_chart_with_common_option,
    save_chart_to_bytes,
    close_pyplot, DBDREAM)
from project_manager import read_json_to_dict

def qq_plot(project_dir: str, num: str,
            common_option: dict):
    """ QQ Plot 생성 """
    img = None
    data_path = os.path.join(project_dir, "data.pkl")
    col_info_path = os.path.join(project_dir, "column_info.json")
    try:
        df = pd.read_pickle(data_path)
        data = df[num].dropna()
        col_infos = read_json_to_dict(col_info_path)
        col_info = [info for info in col_infos if info['Column']==num][0]
        mean = float(col_info['Mean'].replace(',',''))
        std = float(col_info['Std'].replace(',',''))
        # target 설정 및 정렬
        target = np.array(data)
        target = np.sort(target)
        # Outlier 판정
        outlier_mask = np.abs(target - mean) > 3*std
        # 분위수 위치 계산
        n = len(target)
        p = (np.arange(1, n+1) - 0.5)/n # plotting position formula
        # 정규분포의 이론적 분위수
        theorotical_q = norm.ppf(p, loc=mean, scale=std)
        auto_title = f'{num} - QQ Plot'
        auto_x_label = f'정규 분포(μ={mean:.2f}, σ={std:.2f}) 의 분위수'
        auto_y_label = f'정렬된 {num}'

        # QQ Plot 생성
        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        ax.scatter(theorotical_q[~outlier_mask], target[~outlier_mask],
                edgecolors='blue', facecolor='none', linewidths=1)
        ax.plot(theorotical_q, theorotical_q, 'r--', label='y = x (Perfect Fit)')
        ax.scatter(theorotical_q[outlier_mask], target[outlier_mask], marker='x',
                s=60, c='gray', label='Outliers (3σ)')
        ax.legend(loc='upper left')
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":auto_x_label, "y_axis":auto_y_label},
                                        common_option)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dist_num(
    project_dir: str, num: str, orient: str,
    color: str,
    fill: bool, kde: bool, log_scale: bool,
    dist_kind: str,
    common_option: dict):
    """ 분포형 차트 : 수치 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        orient = "y" if orient=="auto" else orient
        dist_kind = "hist" if dist_kind=="auto" else dist_kind
        kde = False if kde=="auto" else kde
        log_scale = False if log_scale=="auto" else log_scale
        fill = True if fill=="auto" else fill
        options = {
            "data": df, "fill": fill, "kind": dist_kind
        }
        has_non_positive = (df[num]<0).any()
        if log_scale and not has_non_positive:
            options.update({"log_scale": log_scale})
        if dist_kind == "hist":
            options.update({"kde": kde})
        if orient == "x":
            options.update({"y": num})
        else:
            options.update({"x": num})
        if color!="auto":
            options.update({"color": color})

        auto_title = f"히스토그램 - {num}" if dist_kind=="hist" else f"KDE Plot - {num}"
        auto_axis_title = "Count" if dist_kind=="hist" else "Density"
        x_axis_auto_title = num if orient=="y" else auto_axis_title
        y_axis_auto_title = auto_axis_title if orient=="y" else num

        g = sns.displot(**options)
        def update_axes(data, **kws):
            ax = plt.gca()
            update_chart_with_common_option(
                ax, auto_title,
                {"x_axis":x_axis_auto_title, "y_axis":y_axis_auto_title},
                common_option)
            if has_non_positive:
                if orient=="x":
                    ax.set_yscale("symlog", linthresh=1.0)
                else:
                    ax.set_xscale("symlog", linthresh=1.0)
        g.map_dataframe(update_axes)
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dist_num_cat(
    project_dir: str,
    num: str, g_cat: str, large_g_cat: str, orient: str,
    fill: bool, kde: bool, log_scale: bool,
    dist_kind: str,
    common_option: dict):
    """ 분포형 차트 : 수치 Group by 범주 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        is_pass_title = False
        df = pd.read_pickle(data_path)
        df = df.dropna(subset=[num, g_cat])
        orient = "y" if orient=="auto" else orient
        dist_kind = "hist" if dist_kind=="auto" else dist_kind
        kde = False if kde=="auto" else kde
        log_scale = False if log_scale=="auto" else log_scale
        fill = True if fill=="auto" else fill
        options = {
            "data": df, "fill": fill,
            "kind": dist_kind, "hue": g_cat
        }
        auto_title = f"히스토그램 - {num} by {g_cat}" if dist_kind=="hist"\
            else f"KDE Plot - {num} by {g_cat}"
        has_non_positive = (df[num]<0).any()
        if log_scale and not has_non_positive:
            if (df[num]==0).any():
                df[num] = df[num].replace(0, 1e-6)
            options.update({"log_scale": log_scale})
        if large_g_cat is not None:
            is_pass_title = True
            auto_title += f", 대분류:{large_g_cat}"
            options.update({"col": large_g_cat})
        if dist_kind == "hist":
            options.update({"kde": kde})
        if orient == "x":
            options.update({"y": num})
        else:
            options.update({"x": num})

        auto_axis_title = "Count" if dist_kind=="hist" else "Density"
        x_axis_auto_title = num if orient=="y" else auto_axis_title
        y_axis_auto_title = auto_axis_title if orient=="y" else num

        g = sns.displot(**options)
        def update_axes(data, **kws):
            ax = plt.gca()
            update_chart_with_common_option(
                        ax, auto_title,
                        {"x_axis":x_axis_auto_title, "y_axis":y_axis_auto_title},
                        common_option,
                        pass_title=is_pass_title)
            if has_non_positive:
                if orient=="x":
                    ax.set_yscale("symlog", linthresh=1.0)
                else:
                    ax.set_xscale("symlog", linthresh=1.0)
        if is_pass_title:
            g.fig.suptitle(auto_title,
                fontdict=dict(fontsize=15, fontweight='bold', fontproperties=DBDREAM))
        g.map_dataframe(update_axes)
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dist_num_num(
    project_dir: str,
    x_num: str, y_num: str,
    color: str, fill: bool,
    x_log_scale: bool, y_log_scale: bool,
    dist_kind: str,
    common_option: dict):
    """ 분포형 차트 : 수치 vs 수치 (히트맵/등고선) """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        dist_kind = "hist" if dist_kind=="auto" else dist_kind
        fill = True if fill=="auto" else fill
        x_log_scale = False if x_log_scale=="auto" else x_log_scale
        y_log_scale = False if y_log_scale=="auto" else y_log_scale
        options = {
            "data": df, "x": x_num, "y": y_num,
            "kind": dist_kind, "cbar": True,
            "cbar_kws": {"format": "%.0f" 
                         if dist_kind=="hist" else "%.2E"}
        }
        has_non_positive = (df[x_num]<0).any() or (df[y_num]<0).any()
        if (x_log_scale or y_log_scale) and not has_non_positive:
            options.update({"log_scale": (x_log_scale, y_log_scale)})
            if x_log_scale and (df[x_num]==0).any():
                df[x_num] = df[x_num].replace(0, 1e-6)
            if y_log_scale and (df[y_num]==0).any():
                df[y_num] = df[y_num].replace(0, 1e-6)
        if dist_kind != "hist":
            options.update({"fill": fill})
        if color!="auto":
            options.update({"color": color})

        auto_title = f"히트맵(빈도) - {x_num} vs {y_num}"\
            if dist_kind=="hist"\
                else f"등고선도(밀도) - {x_num} vs {y_num}"

        g = sns.displot(**options)
        def update_axes(data, **kws):
            ax = plt.gca()
            update_chart_with_common_option(
                        ax, auto_title,
                        {"x_axis":x_num, "y_axis":y_num},
                        common_option)
            if has_non_positive:
                if x_log_scale:
                    ax.set_yscale("symlog", linthresh=1.0)
                if y_log_scale:
                    ax.set_xscale("symlog", linthresh=1.0)
        g.map_dataframe(update_axes)
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dist_num_num_cat(
    project_dir: str,
    x_num: str, y_num: str, g_cat: str, large_g_cat: str,
    fill: bool,
    x_log_scale: bool, y_log_scale: bool,
    dist_kind: str,
    common_option: dict):
    """ 분포형 차트 : 수치 vs 수치 (히트맵/등고선) Group by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        is_pass_title = False
        df = pd.read_pickle(data_path)
        dist_kind = "hist" if dist_kind=="auto" else dist_kind
        fill = True if fill=="auto" else fill
        x_log_scale = False if x_log_scale=="auto" else x_log_scale
        y_log_scale = False if y_log_scale=="auto" else y_log_scale
        options = {
            "data": df, "x": x_num, "y": y_num, "hue": g_cat,
            "kind": dist_kind
        }

        auto_title = f"히트맵(빈도) - {x_num} vs {y_num} by {g_cat}"\
            if dist_kind=="hist"\
                else f"등고선도(밀도) - {x_num} vs {y_num} by {g_cat}"

        has_non_positive = (df[x_num]<0).any() or (df[y_num]<0).any()
        if (x_log_scale or y_log_scale) and not has_non_positive:
            options.update({"log_scale": (x_log_scale, y_log_scale)})
            if x_log_scale and (df[x_num]==0).any():
                df[x_num] = df[x_num].replace(0, 1e-6)
            if y_log_scale and (df[y_num]==0).any():
                df[y_num] = df[y_num].replace(0, 1e-6)
        if dist_kind != "hist":
            options.update({"fill": fill})
        if large_g_cat is not None:
            is_pass_title = True
            auto_title += f", 대분류:{large_g_cat}"
            options.update({"col": large_g_cat})

        g = sns.displot(**options)
        def update_axes(data, **kws):
            ax = plt.gca()
            update_chart_with_common_option(
                        ax, auto_title,
                        {"x_axis":x_num, "y_axis":y_num},
                        common_option,
                        pass_title=is_pass_title)
            if has_non_positive:
                if x_log_scale:
                    ax.set_yscale("symlog", linthresh=1.0)
                if y_log_scale:
                    ax.set_xscale("symlog", linthresh=1.0)
        if is_pass_title:
            g.fig.suptitle(auto_title,
                fontdict=dict(fontsize=15, fontweight='bold', fontproperties=DBDREAM))
        g.map_dataframe(update_axes)
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def dist_cat_cat_num(
    project_dir: str,
    x_cat: str, y_cat: str, num: str,
    estimator: str,
    show_val: bool, line_width: int,
    common_option: dict):
    """ 분포형 차트 : 범주 vs 범주 히트맵 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        df = df.dropna(subset=[x_cat, y_cat])
        df[[x_cat, y_cat]] = df[[x_cat, y_cat]].astype(str)
        estimator = "평균" if estimator=="auto" else estimator
        show_val = True if show_val=="auto" else show_val
        auto_title = f"히트맵 {x_cat} vs {y_cat}\n값: {num}-{estimator}"

        match estimator:
            case "평균":
                agg_func = np.nanmean
            case "합계":
                agg_func = np.nansum
            case "최대":
                agg_func = np.nanmax
            case "최소":
                agg_func = np.nanmin
            case "중앙값":
                agg_func = np.nanmedian
            case "표준편차":
                agg_func = np.nanstd

        pivot_df = df.pivot_table(
            index=y_cat,
            columns=x_cat,
            values=num,
            aggfunc=agg_func
        )

        options = {
            "data": pivot_df, "annot": show_val,
            "fmt": ".1f"
        }
        if line_width!="auto":
            line_width = line_width/10.0
            options.update({"linewidth": line_width})
        fig, ax = init_figure_axes("auto", "auto")
        options.update({"ax": ax})
        sns.heatmap(**options)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis": x_cat, "y_axis": y_cat },
                                        is_x_dt = True, is_y_dt = True,
                                        common = common_option)
        ax.grid(None)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
