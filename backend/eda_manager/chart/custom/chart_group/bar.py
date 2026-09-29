# pylint: disable=W0718, W0613, E1101, C0104, C3001
"""
Bar(바 차트) 차트 생성기
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from eda_manager.chart.chart_helper import (init_figure_axes,
                                            split_prop_others,
                                            update_chart_with_common_option,
                                            update_chart_y_axis,
                                            save_chart_to_bytes,
                                            close_pyplot, DBDREAM, DBGOTHIC)

def pareto(project_dir: str, cat: str, common_option: dict,
           bar_color: str, line_color: str,
           use_etc: bool=False):
    """ 바차트 : Paretor 차트 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        use_etc = False if use_etc=="auto" else use_etc
        auto_title = f"Pareto Chart - {cat}"
        df = pd.read_pickle(data_path)
        df[cat] = df[cat].astype(str)
        df_cnt_info = pd.DataFrame(df[cat].value_counts()).reset_index()
        if use_etc and len(df_cnt_info)>20:
            etc_cnt = df_cnt_info.iloc[20:]["count"].sum()
            df_cnt_info = pd.concat([df_cnt_info.iloc[:20],
                                     pd.DataFrame([{cat: "기타", "count": etc_cnt}])])
        df_cnt_info["cumsum"] = df_cnt_info["count"].cumsum()
        df_cnt_info["cumratio"] = df_cnt_info["cumsum"]/df_cnt_info["count"].sum()*100

        size_x, size_y = common_option['x_size'], common_option['y_size']
        axis_font_size = common_option["axis_font_size"]
        axis_font_size = 12 if axis_font_size=="auto" else axis_font_size
        line_color = line_color if line_color!="auto" else "orange"
        fig, ax = init_figure_axes(size_x, size_y)

        # 1. 개별 막대 그래프
        options = {"data": df_cnt_info, "x": cat, "y": "count", "ax": ax}
        if bar_color != "auto":
            options.update({"color": bar_color})
        sns.barplot(**options)
        for container in ax.containers:
            ax.bar_label(container, label_type="edge", fmt="{:,.0f}")

        # 2. 누적 비율 산점도
        ax2 = ax.twinx()
        options = {"data": df_cnt_info, "x": cat, "y": "cumratio", "ax": ax2,
                   "color":line_color, "marker": "o"}
        sns.lineplot(**options)
        for x,y in zip(df_cnt_info[cat], df_cnt_info["cumratio"]):
            ax2.annotate(f"{y:.1f}%", (x,y), textcoords="offset points", xytext=(0,5), ha="center")

        update_chart_with_common_option(ax, auto_title, {"x_axis":cat, "y_axis":"개수"},
                                        common_option, is_x_dt=True)
        update_chart_y_axis(ax2, "누적 비율(%)", axis_font_size)
        ax.set_axisbelow(True)
        ax2.set_axisbelow(True)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def count(
    project_dir: str,
    cat: str,
    orient: str, stat: str,
    color: str,
    show_label: bool, label_pos: str,
    common_option: dict,
    use_etc: bool=False):
    """ 바차트 : (빈도) 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    use_etc = False if use_etc=="auto" else use_etc
    try:
        auto_title = f"바 차트(빈도) - {cat}"
        df = pd.read_pickle(data_path)
        if use_etc and len(df[cat].unique())>20:
            _, df_other = split_prop_others(df, cat, category_count=20)
            df_other = df_other.rename(columns={cat: "name"})
            df.loc[df[cat].isin(df_other["name"].tolist()), cat] = "기타"
        orient = "x" if orient=="auto" else orient
        show_label = False if show_label=="auto" else show_label
        stat = "count" if stat=="auto" else stat
        label_pos = "edge" if label_pos=="auto" else label_pos
        label_fmt = None
        auto_axis_title = None
        match stat:
            case "count":
                auto_axis_title = "Count"
                label_fmt = lambda v: f"{v:,.0f}"
            case "percent":
                auto_axis_title = "Percent"
                label_fmt = lambda v: f"{v:,.2f}%"
            case "proportion":
                auto_axis_title = "Proportion"
                label_fmt = lambda v: f"{v:,.2f}"
            case "probability":
                auto_axis_title = "Probablility"
                label_fmt = lambda v: f"{v:,.2f}"

        options = {"data": df, "stat": stat}
        if orient == "x":
            options.update({"x": cat})
        else:
            options.update({"y": cat})
        if color != "auto":
            options.update({"color": color})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        options.update({"ax": ax})
        sns.countplot(**options)
        if show_label:
            for container in ax.containers:
                labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                ax.bar_label(container, label_type=label_pos, labels=labels)
        update_chart_with_common_option(
            ax, auto_title,
            {"x_axis": auto_axis_title if orient!="x" else cat,
             "y_axis": auto_axis_title if orient!="y" else cat},
            common_option, is_x_dt=orient=="x", is_y_dt=orient=="y")
        ax.set_axisbelow(True)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def count_cat(
    project_dir: str,
    cat: str, g_cat: str, large_g_cat: str,
    orient: str, stat: str,
    group_type: str,
    show_label: bool, label_pos: str,
    common_option: dict):
    """ 바차트 : (빈도) 범주형 Group by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        auto_title = f"바 차트(빈도) - {cat}(by {g_cat})"
        df = pd.read_pickle(data_path)

        orient = "x" if orient=="auto" else orient
        large_g_cat = None if large_g_cat=="auto" else large_g_cat
        group_type = "grouped" if group_type=="auto" else group_type
        show_label = False if show_label=="auto" else show_label
        stat = "count" if stat=="auto" else stat
        label_pos = "edge" if label_pos=="auto" else label_pos
        label_fmt = None
        auto_axis_title = None
        match stat:
            case "count":
                auto_axis_title = "Count"
                label_fmt = lambda v: f"{v:,.0f}"
            case "percent":
                auto_axis_title = "Percent"
                label_fmt = lambda v: f"{v:,.2f}%"
            case "proportion":
                auto_axis_title = "Proportion"
                label_fmt = lambda v: f"{v:,.2f}"
            case "probability":
                auto_axis_title = "Probablility"
                label_fmt = lambda v: f"{v:,.2f}"

        options = {"data": df, "stat": stat, "hue": g_cat}
        if group_type == "stacked":
            options.update({"multiple": "stack", "shrink": .8})
        if orient == "x":
            options.update({"x": cat})
        else:
            options.update({"y": cat})
        if large_g_cat is not None:
            def show_text_label(data, **kws):
                ax = plt.gca()
                if show_label:
                    for container in ax.containers:
                        labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                        ax.bar_label(container, label_type=label_pos, labels=labels)
                update_chart_with_common_option(
                    ax, auto_title,
                    {"x_axis": auto_axis_title if orient!="x" else cat,
                    "y_axis": auto_axis_title if orient!="y" else cat},
                    {k:v for k,v in common_option.items()
                     if k not in ["chart_nm"]}, is_x_dt=orient=="x", is_y_dt=orient=="y")
                ax.set_axisbelow(True)
            options.update({"col": large_g_cat})
            if group_type == "grouped":
                options.update({"kind": "count"})
                g = sns.catplot(**options)
            else:
                options.update({"kind": "hist"})
                g = sns.displot(**options)
            g.map_dataframe(show_text_label)
            g.fig.suptitle(auto_title+f", 대분류:{large_g_cat}", y=1.05)
            img = save_chart_to_bytes(g)
        else:
            size_x, size_y = common_option['x_size'], common_option['y_size']
            fig, ax = init_figure_axes(size_x, size_y)
            options.update({"ax": ax})
            if group_type == "grouped":
                sns.countplot(**options)
            else:
                sns.histplot(**options)
            if show_label:
                for container in ax.containers:
                    labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                    ax.bar_label(container, label_type=label_pos, labels=labels)
            update_chart_with_common_option(
                ax, auto_title,
                {"x_axis": auto_axis_title if orient!="x" else cat,
                "y_axis": auto_axis_title if orient!="y" else cat},
                common_option, is_x_dt=orient=="x", is_y_dt=orient=="y")
            ax.set_axisbelow(True)
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def bar_cat_num(
    project_dir: str,
    cat: str, num: str,
    orient: str, estimator: str,
    color: str,
    show_label: bool, label_pos: str,
    common_option: dict):
    """ 바차트 : 범주형 vs 수치형(요약) """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)

        orient = "y" if orient=="auto" else orient
        show_label = False if show_label=="auto" else show_label
        estimator = "평균" if estimator=="auto" else estimator
        auto_title = f"바 차트 - {cat} vs {num}({estimator})"
        label_pos = "edge" if label_pos=="auto" else label_pos
        agg_func = None
        auto_axis_title = None
        label_fmt = lambda v: f"{v:,.2f}"
        match estimator:
            case "평균":
                auto_axis_title = f"{num}(평균)"
                agg_func = np.nanmean
            case "합계":
                auto_axis_title = f"{num}(합계)"
                agg_func = np.nansum
            case "최대":
                auto_axis_title = f"{num}(최대)"
                agg_func = np.nanmax
            case "최소":
                auto_axis_title = f"{num}(최소)"
                agg_func = np.nanmin
            case "중앙값":
                auto_axis_title = f"{num}(중앙값)"
                agg_func = np.nanmedian
            case "표준편차":
                auto_axis_title = f"{num}(표준편차)"
                agg_func = np.nanstd

        options = {"data": df, "estimator": agg_func}
        if orient == "y":
            options.update({"x": cat, "y": num})
        else:
            options.update({"x": num, "y": cat, "orient": "y"})
        if color != "auto":
            options.update({"color": color})

        size_x, size_y = common_option['x_size'], common_option['y_size']
        fig, ax = init_figure_axes(size_x, size_y)
        options.update({"ax": ax})
        sns.barplot(**options)
        if show_label:
            for container in ax.containers:
                labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                ax.bar_label(container, label_type=label_pos, labels=labels)
        update_chart_with_common_option(
            ax, auto_title,
            {"x_axis": auto_axis_title if orient!="y" else cat,
             "y_axis": cat if orient!="y" else auto_axis_title},
            common_option, orient!="x", orient=="x")
        ax.set_axisbelow(True)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def bar_cat_num_cat(
    project_dir: str,
    cat: str, num: str, g_cat: str, large_g_cat: str,
    orient: str, estimator: str,
    group_type: str,
    show_label: bool, label_pos: str,
    common_option: dict):
    """ 바차트 : 범주형 vs 수치형(요약) by 범주형 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)

        group_type = "grouped" if group_type=="auto" else group_type
        orient = "y" if orient=="auto" else orient
        show_label = False if show_label=="auto" else show_label
        estimator = "평균" if estimator=="auto" else estimator
        auto_title = f"바 차트 - {cat} vs {num}({estimator}) by {g_cat}"
        label_pos = "edge" if label_pos=="auto" else label_pos
        agg_func = None
        auto_axis_title = None
        label_fmt = lambda v: f"{v:,.2f}"
        size_x, size_y = common_option['x_size'], common_option['y_size']
        match estimator:
            case "평균":
                auto_axis_title = f"{num}(평균)"
                agg_func = np.nanmean
            case "합계":
                auto_axis_title = f"{num}(합계)"
                agg_func = np.nansum
            case "최대":
                auto_axis_title = f"{num}(최대)"
                agg_func = np.nanmax
            case "최소":
                auto_axis_title = f"{num}(최소)"
                agg_func = np.nanmin
            case "중앙값":
                auto_axis_title = f"{num}(중앙값)"
                agg_func = np.nanmedian
            case "표준편차":
                auto_axis_title = f"{num}(표준편차)"
                agg_func = np.nanstd
        if group_type == "grouped":
            options = {"data": df, "estimator": agg_func, "hue":g_cat, "errorbar": None}
            if orient == "y":
                options.update({"x": cat, "y": num})
            else:
                options.update({"x": num, "y": cat, "orient": "y"})
            if large_g_cat is not None:
                def show_text_label(data, **kws):
                    ax = plt.gca()
                    if show_label:
                        for container in ax.containers:
                            labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                            ax.bar_label(container, label_type=label_pos, labels=labels)
                    update_chart_with_common_option(
                        ax, auto_title,
                        {"x_axis": auto_axis_title if orient!="y" else cat,
                         "y_axis": cat if orient!="y" else auto_axis_title},
                        {k:v for k,v in common_option.items()
                        if k not in ["chart_nm"]}, is_x_dt=orient=="x", is_y_dt=orient=="y")
                    ax.set_axisbelow(True)
                options.update({"col": large_g_cat, "kind": "bar"})
                g = sns.catplot(**options)
                g.map_dataframe(show_text_label)
                g.fig.suptitle(auto_title+f", 대분류:{large_g_cat}", y=1.05,
                               fontdict=dict(fontsize=15, fontweight='bold',
                                             fontproperties=DBDREAM))
                img = save_chart_to_bytes(g)

            size_x, size_y = common_option['x_size'], common_option['y_size']
            fig, ax = init_figure_axes(size_x, size_y)
            options.update({"ax": ax})
            sns.barplot(**options)
            if show_label:
                for container in ax.containers:
                    labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                    ax.bar_label(container, label_type=label_pos, labels=labels)
            update_chart_with_common_option(
                ax, auto_title,
                {"x_axis": auto_axis_title if orient!="y" else cat,
                "y_axis": cat if orient!="y" else auto_axis_title},
                common_option, orient!="x", orient=="x")
            ax.set_axisbelow(True)
            img = save_chart_to_bytes(fig)
        else:
            plt.style.use("seaborn-v0_8")
            if large_g_cat is not None:
                uniques = sorted(df[large_g_cat].unique())
                fig, ax = init_figure_axes(size_x, size_y, ncols=len(uniques), sharey=True)
                for i, l_g_col in enumerate(uniques):
                    agg = (
                        df[df[large_g_cat]==l_g_col]
                        .groupby([cat, g_cat])[num]
                        .apply(agg_func)
                        .unstack(fill_value=0)
                    )
                    bar = None
                    for col in agg.columns:
                        if orient == "y":
                            ax[i].bar(
                                agg.index,
                                agg[col],
                                bottom = bar,
                                label=col if i==0 else None,
                            )
                        else:
                            ax[i].barh(
                                agg.index,
                                agg[col],
                                left = bar,
                                label=col if i==0 else None,
                            )
                        bar = agg[col] if bar is None else bar + agg[col]
                        if show_label:
                            for container in ax[i].containers:
                                labels = [label_fmt(v) if v!=0 else ''
                                          for v in container.datavalues]
                                ax.bar_label(container, label_type=label_pos, labels=labels)
                        ax[i].set_title(f"{large_g_cat} = {l_g_col}",
                                        fontdict=dict(fontweight='bold', fontproperties=DBGOTHIC))
                        ax[i].set_xlabel(cat if orient=="y" else auto_axis_title,
                                         fontdict=dict(fontweight='bold', fontproperties=DBGOTHIC))
                        if i == 0:
                            ax[i].set_ylabel(auto_axis_title if orient=="y" else cat,
                                             fontdict=dict(fontweight='bold',
                                                           fontproperties=DBGOTHIC))
                        ax[i].grid(True, linestyle='--', alpha=.5)
                fig.legend(title=g_cat)
                fig.suptitle(auto_title + f", 대분류: {large_g_cat}",
                             fontdict=dict(fontsize=15, fontweight='bold', fontproperties=DBDREAM))
            else:
                agg = (
                    df
                    .groupby([cat, g_cat])[num]
                    .apply(agg_func)
                    .unstack(fill_value=0)
                )
                fig, ax = init_figure_axes(size_x, size_y)
                bar = None
                for col in agg.columns:
                    if orient == "y":
                        ax.bar(agg.index, agg[col], bottom = bar, label=col)
                    else:
                        ax.barh(agg.index, agg[col], left = bar, label=col)

                    bar = agg[col] if bar is None else bar + agg[col]
                    if show_label:
                        for container in ax.containers:
                            labels = [label_fmt(v) if v!=0 else '' for v in container.datavalues]
                            ax.bar_label(container, label_type=label_pos, labels=labels)
                ax.set_xlabel(cat if orient=="y" else auto_axis_title,
                              fontdict=dict(fontweight='bold', fontproperties=DBGOTHIC))
                ax.set_ylabel(auto_axis_title if orient=="y" else cat,
                              fontdict=dict(fontweight='bold', fontproperties=DBGOTHIC))
                ax.set_title(auto_title, fontdict=dict(fontsize=15, fontweight='bold',
                                                       fontproperties=DBDREAM))
                ax.grid(True, linestyle='--', alpha=.5)
                ax.legend(title=g_cat)
            img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
