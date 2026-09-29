# pylint: disable=W0718, E1101, C0121
"""
Scatter(산점도) 차트 생성기
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
from eda_manager.chart.chart_helper import (init_figure_axes,
                                            update_chart_with_common_option,
                                            save_chart_to_bytes, save_gif_chart_to_bytes,
                                            close_pyplot)

def num_num_chart(
    project_dir: str,
    x_num: str, y_num: str,
    color: str,
    marker: str, marker_size: int,
    reg_line: bool, reg_line_color: str,
    common_option: dict):
    """ 산점도 : 수치형 vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"산점도 - {x_num} vs {y_num}"
        options = {"data": pd.read_pickle(data_path), "x": x_num, "y": y_num}
        if color!="auto":
            options.update({"color": color})
        if marker!="auto":
            options.update({"marker": marker})
        if marker_size!="auto":
            if reg_line==True:
                options.update({"scatter_kws":dict(s=marker_size)})
            else:
                options.update({"s":marker_size})
        if (reg_line==True) and (reg_line_color!="auto"):
            options.update({"line_kws":dict(color=reg_line_color)})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        if reg_line==True:
            sns.regplot(**options)
        else:
            sns.scatterplot(**options)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num}, common_option)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def num_num_by_cat_chart(
    project_dir: str,
    x_num: str, y_num: str, g_cat: str,
    marker_size: int,
    legend_pos: str,
    reg_line: bool,
    common_option: dict):
    """ 산점도 : 수치형 vs 수치형 by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    fig, g = None, None
    try:
        auto_title = f"산점도 - {x_num} vs {y_num}"
        df = pd.read_pickle(data_path)
        options = {"data": df, "x": x_num, "y": y_num, "hue": g_cat}

        size_x, size_y = common_option['x_size'], common_option['y_size']
        if reg_line==True:
            if (size_x!="auto") and (size_y!="auto"):
                options.update({"legend": False, "height": size_y, "aspect": size_x/size_y})
            elif size_x!="auto":
                options.update({"legend": False, "height": size_x, "aspect": 1})
            elif size_y!="auto":
                options.update({"legend": False, "height": size_y, "aspect": 1.5})
            else:
                options.update({"legend": False})
            scatter_kws, line_kws = {}, {}
            if marker_size!="auto":
                scatter_kws.update({"s": marker_size})
            if len(scatter_kws)>0:
                options.update({"scatter_kws": scatter_kws})
            if len(line_kws)>0:
                options.update({"line_kws": line_kws})
            g = sns.lmplot(**options)
            ax = plt.gca()
        else:
            fig, ax = init_figure_axes(size_x, size_y)
            if len(df[g_cat].unique())<10:
                options.update({"style": g_cat})
            options.update({"style": g_cat})
            if marker_size!="auto":
                options.update({"s":marker_size})
            sns.scatterplot(**options)
        if legend_pos != "auto":
            ax.legend(title=g_cat, loc=legend_pos)
        else:
            ax.legend(title=g_cat)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num}, common_option)
        if g is None:
            img = save_chart_to_bytes(fig)
        else:
            img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def num_num_num_chart(
    project_dir: str,
    x_num: str, y_num: str, z_num: str,
    color: str,
    marker: str, marker_size: int,
    gif: bool, rotate_axis: str,
    common_option: dict):
    """ 산점도 : 수치형 vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        gif = False if gif=="auto" else gif
        df = pd.read_pickle(data_path)[[x_num, y_num, z_num]]
        auto_title = f"산점도 - {x_num} vs {y_num} vs {x_num}"
        options = {
            "xs": df[x_num].values,
            "ys": df[y_num].values,
            "zs": df[z_num].values,
        }
        if color!="auto":
            options.update({"c": color})
        if marker!="auto":
            options.update({"marker": marker})
        if marker_size!="auto":
            options.update({"s":marker_size})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y, dimension="3d")
        ax.scatter(**options)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num, "z_axis":z_num},
                                        common_option)
        ax.set_box_aspect(None, zoom=0.9)
        if gif:
            rotate_axis = "vertical" if rotate_axis == "auto" else rotate_axis
            def update(num):
                if rotate_axis == "vertical":
                    ax.view_init(elev=30, azim=num) # 수직 회전
                else:
                    ax.view_init(elev=num, azim=30) # 수평 회전
                return ax
            ani = FuncAnimation(fig, update, frames=np.arange(0,360,1), interval=50)
            img = save_gif_chart_to_bytes(project_dir, ani)
        else:
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def num_num_num_by_cat_chart(
    project_dir: str,
    x_num: str, y_num: str, z_num: str, g_cat: str,
    marker: str, marker_size: int,
    gif: bool, rotate_axis: str,
    legend_pos: str,
    common_option: dict):
    """ 산점도 : 수치형 vs 수치형 vs 수치형 by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        gif = False if gif=="auto" else gif
        df = pd.read_pickle(data_path)[[x_num, y_num, z_num, g_cat]]
        auto_title = f"산점도 - {x_num} vs {y_num} vs {x_num} (by {g_cat})"
        group_size = len(df[g_cat].unique())
        if group_size<=10:
            cmap = plt.get_cmap("tab10")
        elif group_size<=20:
            cmap = plt.get_cmap("tab20")
        else:
            cmap = plt.cm.viridis
            cmap = cmap(np.linspace(0, 1, group_size))
            cmap = [tuple(color) for color in cmap]
        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y, dimension="3d")
        for i, (group, data) in enumerate(df.groupby(g_cat)):
            options = {
                "xs": data[x_num].values,
                "ys": data[y_num].values,
                "zs": data[z_num].values,
                "c": cmap(i) if group_size<=20 else cmap[i],
                "label": group
            }
            if marker!="auto":
                options.update({"marker": marker})
            if marker_size!="auto":
                options.update({"s": marker_size})
            ax.scatter(**options)
        if legend_pos != "auto":
            ax.legend(title=g_cat, loc=legend_pos)
        else:
            ax.legend(title=g_cat)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num, "z_axis":z_num},
                                        common_option)
        ax.set_box_aspect(None, zoom=0.9)
        if gif:
            rotate_axis = "vertical" if rotate_axis == "auto" else rotate_axis
            def update(num):
                if rotate_axis == "vertical":
                    ax.view_init(elev=30, azim=num) # 수직 회전
                else:
                    ax.view_init(elev=num, azim=30) # 수평 회전
                return ax
            ani = FuncAnimation(fig, update, frames=np.arange(0,360,1), interval=50)
            img = save_gif_chart_to_bytes(project_dir, ani)
        else:
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def stem_num_num_num_chart(
    project_dir: str,
    x_num: str, y_num: str, z_num: str,
    color: str,
    marker: str, marker_size: int,
    stem_line_color: str, stem_axis: str,
    gif: bool, rotate_axis: str,
    common_option: dict):
    """ 산점도(Stem) : 수치형 vs 수치형 vs 수치형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        gif = False if gif=="auto" else gif
        stem_axis = "z" if stem_axis=="auto" else stem_axis
        df = pd.read_pickle(data_path)[[x_num, y_num, z_num]]
        auto_title = f"산점도 - {x_num} vs {y_num} vs {x_num} ({stem_axis.upper()}축 투영)"
        options = {
            "x": df[x_num].values,
            "y": df[y_num].values,
            "z": df[z_num].values,
        }
        if marker!="auto":
            options.update({"markerfmt": marker})
        if stem_axis!="auto":
            options.update({"orientation": stem_axis})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y, "3d")
        markerline, stemline, baseline = ax.stem(**options)
        markerline.set_markerfacecolor("none")
        plt.setp(baseline, linewidth=1)
        if marker_size!="auto":
            markerline.set_markersize(marker_size)
        if color!="auto":
            markerline.set_markeredgecolor(color)
        if stem_line_color!="auto":
            plt.setp(stemline, color=stem_line_color, linewidth=1)
            plt.setp(baseline, color=stem_line_color, linewidth=1)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num, "z_axis":z_num},
                                        common_option)
        ax.set_box_aspect(None, zoom=0.9)
        if gif:
            rotate_axis = "vertical" if rotate_axis == "auto" else rotate_axis
            def update(num):
                if rotate_axis == "vertical":
                    ax.view_init(elev=30, azim=num) # 수직 회전
                else:
                    ax.view_init(elev=num, azim=30) # 수평 회전
                return ax
            ani = FuncAnimation(fig, update, frames=np.arange(0,360,1), interval=50)
            img = save_gif_chart_to_bytes(project_dir, ani)
        else:
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def stem_num_num_num_by_cat_chart(
    project_dir: str,
    x_num: str, y_num: str, z_num: str, g_cat: str,
    marker: str, marker_size: int,
    stem_axis: str,
    gif: bool, rotate_axis: str,
    legend_pos: str,
    common_option: dict):
    """ 산점도 : 수치형 vs 수치형 vs 수치형 by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        gif = False if gif=="auto" else gif
        stem_axis = "z" if stem_axis=="auto" else stem_axis
        df = pd.read_pickle(data_path)[[x_num, y_num, z_num, g_cat]]
        auto_title = f"산점도 - {x_num} vs {y_num} vs {x_num} ({stem_axis.upper()}축 투영, by {g_cat})"
        group_size = len(df[g_cat].unique())
        if group_size<=10:
            cmap = plt.get_cmap("tab10")
        elif group_size<=20:
            cmap = plt.get_cmap("tab20")
        else:
            cmap = plt.cm.viridis
            cmap = cmap(np.linspace(0, 1, group_size))
            cmap = [tuple(color) for color in cmap]
        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y, dimension="3d")
        for i, (group, data) in enumerate(df.groupby(g_cat)):
            options = {
                "x": data[x_num].values,
                "y": data[y_num].values,
                "z": data[z_num].values,
                "label": group
            }
            color = list(cmap(i)) if group_size<=20 else list(cmap[i])
            color[3] = 0.8
            color = tuple(color)
            if marker!="auto":
                options.update({"markerfmt": marker})
            if stem_axis!="auto":
                options.update({"orientation": stem_axis})
            markerline, stemline, baseline = ax.stem(**options)
            markerline.set_markerfacecolor("none")
            plt.setp(baseline, linewidth=1)
            markerline.set_markeredgecolor(color)
            if marker_size!="auto":
                markerline.set_markersize(marker_size)
            plt.setp(stemline, color=color, linewidth=1)
            plt.setp(baseline, color=color, linewidth=1)
        if legend_pos != "auto":
            ax.legend(title=g_cat, loc=legend_pos)
        else:
            ax.legend(title=g_cat)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_num, "y_axis":y_num, "z_axis":z_num},
                                        common_option)
        ax.set_box_aspect(None, zoom=0.9)
        if gif:
            rotate_axis = "vertical" if rotate_axis == "auto" else rotate_axis
            def update(num):
                if rotate_axis == "vertical":
                    ax.view_init(elev=30, azim=num) # 수직 회전
                else:
                    ax.view_init(elev=num, azim=30) # 수평 회전
                return ax
            ani = FuncAnimation(fig, update, frames=np.arange(0,360,1), interval=50)
            img = save_gif_chart_to_bytes(project_dir, ani)
        else:
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
