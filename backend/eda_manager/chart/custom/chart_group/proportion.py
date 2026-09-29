# pylint: disable=W0613, W0718, E1101, C2801
"""
빈도,비중 요약 차트 생성기
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mtick
import seaborn as sns
import squarify
from wordcloud import WordCloud
from pywaffle import Waffle
from statsmodels.graphics.mosaicplot import mosaic
from eda_manager.chart.chart_helper import (
    init_figure_axes, split_prop_others,
    save_chart_to_bytes, update_chart_with_common_option,
    close_pyplot, DBDREAM, FONT_GOTHIC_PATH)

def pie_chart(
    project_dir: str,
    cat: str,
    use_etc: bool, show_etc_detail: bool,
    common_option: dict):
    """ 파이차트 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        df[cat] = df[cat].dropna().astype(str)
        auto_title = f"Pie 차트 - {cat}"
        use_etc = True if use_etc=="auto" else use_etc
        if len(df[cat].unique())<7:
            use_etc = False
        df_prop, df_others = split_prop_others(df, cat, use_etc)
        colors = [
            "#4c72b0", "#dd8452", "#55a868", "#c44e52",
            "#8172b3", "#937860", "#da8bc3"
        ]
        gray_color = "#8c8c8c"
        colors = colors[:len(df_prop)]
        explodes = [0 for _ in range(len(df_prop))]
        if "기타" in df_prop[cat].values:
            colors[-1] = gray_color
            explodes[-1] = 0.05
        options = {
            "x": df_prop["ratio"],
            "colors": colors,
            "labels": [f"{row[cat]}\n({row['count']:.0f})"
                       for _,row in df_prop.iterrows()],
            "explode": explodes,
            "startangle": 90,
            "autopct": "%1.1f%%",
            "pctdistance": .7,
            "labeldistance": 1.15,
            "counterclock": False,
            "wedgeprops": dict(width=.6),
            "textprops": dict(ha="center", fontweight="bold")
        }

        size_x, size_y = common_option['x_size'], common_option['y_size']
        chart_nm = common_option.get("chart_nm", None)
        chart_nm_font_size = common_option.get("chart_nm_font_size", 15)
        chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size

        fig, ax = None, None
        if use_etc and show_etc_detail and df_others is not None:
            df_others[cat] = df_others[cat].astype(str)
            df_others = df_others[:100]
            fig, ax = init_figure_axes(size_x, size_y, ncols=2)
            ax[0].pie(**options)
            ax[0].legend(df_prop[cat], title=cat, ncol=4,
                      loc="lower center", bbox_to_anchor=(0.5, -0.23))
            chart_nm = auto_title if chart_nm=="auto" else chart_nm
            ax[0].set_title(chart_nm, fontdict=dict(fontsize=chart_nm_font_size,
                fontweight='bold', fontproperties=DBDREAM), y=1.05, pad=5)
            other_bars = ax[1].bar(df_others[cat], df_others["count"], color=gray_color)
            ax[1].bar_label(other_bars, label_type="center")
            ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=-45, ha='center')
            ax[1].grid(True, linestyle='--', alpha=.5)
            sub_ax = ax[1].twinx()
            sub_ax.plot(df_others[cat], df_others["ratio"], marker="o", color="tab:red")
            for i, ratio in enumerate(df_others["ratio"].values):
                sub_ax.text(df_others[cat].values[i], ratio,
                            f"  {ratio:.2%}", ha="left", va="center")
            sub_ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
            ax[1].set_axisbelow(True)
            ax[1].set_title(f"{cat} - 기타 상세", fontdict=dict(fontsize=chart_nm_font_size,
                fontweight='bold', fontproperties=DBDREAM), y=1.05, pad=5)
        else:
            if not show_etc_detail:
                if "기타" in df_prop[cat].values:
                    colors[-1] = gray_color
                explodes = [0 for _ in range(len(df_prop))]
                options.update({"colors": colors, "explode": explodes})
            fig, ax = init_figure_axes(size_x, size_y)
            ax.pie(**options)
            ax.legend(df_prop[cat], title=cat, ncol=4,
                      loc="lower center", bbox_to_anchor=(0.5, -0.23))
            chart_nm = auto_title if chart_nm=="auto" else chart_nm
            ax.set_title(chart_nm, fontdict=dict(fontsize=chart_nm_font_size,
                fontweight='bold', fontproperties=DBDREAM), y=1.05, pad=5)

        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def wordcloud_chart(
    project_dir: str,
    cat: str,
    common_option: dict):
    """ WordCloud """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        series = df[cat].dropna().astype(str)
        counts = series.value_counts().to_dict()
        x_size, y_size = common_option['x_size'], common_option['y_size']
        x_size = 5 if x_size=="auto" else x_size
        y_size = 5 if y_size=="auto" else y_size
        w_x_size, w_y_size = x_size * 100, y_size*100
        chart_nm = common_option.get("chart_nm", "auto")
        chart_nm_font_size = common_option.get("chart_nm_font_size", "auto")
        auto_title = f"Wordcloud - {cat}"
        chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size
        chart_nm = auto_title if chart_nm=="auto" else chart_nm
        try:
            wordcloud = WordCloud(background_color='white',
                    collocations=False,
                    width=w_x_size, height=w_y_size,
                    font_path = FONT_GOTHIC_PATH).generate_from_frequencies(counts)
        except Exception as e:
            print(e)
            # arial_font_path = fm.findfont("Arial", fallback_to_default=False)
            arial_font_path = fm.findfont("Malgun Gothic", fallback_to_default=False)
            wordcloud = WordCloud(background_color='white',
                    collocations=False,
                    width=w_x_size, height=w_y_size,
                    font_path = arial_font_path).generate_from_frequencies(counts)
        fig, ax = plt.subplots(figsize=(x_size, y_size))
        ax.imshow(wordcloud)
        ax.set_title(chart_nm, fontdict=dict(fontsize=chart_nm_font_size,
                    fontweight='bold', fontproperties=DBDREAM))
        ax.axis('off')
        fig.tight_layout()
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def waffle_chart(
    project_dir: str,
    cat: str,
    use_etc: bool,
    nrow: int, ncol: int,
    scale_type: str,
    common_option: dict):
    """ 와플 차트 생성 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    use_etc = True if use_etc=="auto" else use_etc
    try:
        df = pd.read_pickle(data_path)
        if use_etc and len(df[cat].unique())>10:
            df_prop, _ = split_prop_others(df, cat, use_etc, category_count=10)
            if len(df_prop)<10:
                df_prop = df_prop.rename(columns={cat: "name"})
            counts = {row.name: row.count for row in df_prop.itertuples()}
        else:
            series = df[cat].dropna().astype(str)
            counts = series.value_counts().to_dict()

        if len(counts)<=10:
            cmap = sns.color_palette("deep")
            colors = [cmap[i] for i,_ in enumerate(counts.items())]
        elif len(counts)<=20:
            cmap = sns.color_palette("tab20")
            colors = [cmap[i] for i,_ in enumerate(counts.items())]
        else:
            cmap = sns.color_palette("cubehelix", as_cmap=True)
            colors = [cmap(i*10) for i,_ in enumerate(counts.items())]

        auto_title = f"Waffle 차트 - {cat}"
        chart_nm = common_option.get("chart_nm", "auto")
        chart_nm_font_size = common_option.get("chart_nm_font_size", "auto")
        x_size, y_size = common_option['x_size'], common_option['y_size']
        x_size = 5 if x_size=="auto" else x_size
        y_size = 5 if y_size=="auto" else y_size
        chart_nm = auto_title if chart_nm=="auto" else chart_nm
        chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size
        nrow = 10 if nrow=="auto" else nrow
        ncol = 10 if ncol=="auto" else ncol
        scale_type = "nearest" if scale_type=="auto" else scale_type
        unique_cnt = len(counts)
        n_col = unique_cnt//8 + 1 if unique_cnt%8!=0 else unique_cnt//8

        fig = plt.figure(
            FigureClass=Waffle,
            rows=nrow,
            columns=ncol,
            values=counts,
            colors=colors,
            legend={"loc": "upper left", "bbox_to_anchor": (1, 1), "ncol": n_col},
            title={
                "label": chart_nm,
                "loc": "left",
                "fontdict": {
                    "fontsize": chart_nm_font_size,
                    "fontweight": "bold",
                    "fontproperties": DBDREAM
                }
            },
            figsize=(x_size, y_size),
            rounding_rule=scale_type,
        )
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def treemap_chart(
    project_dir: str,
    cat: str,
    use_etc: bool,
    common_option: dict
    ):
    """ 트리맵 생성 """
    img = None
    use_etc = True if use_etc=="auto" else use_etc
    data_path = os.path.join(project_dir, "data.pkl")
    try:
        df = pd.read_pickle(data_path)
        if use_etc and len(df[cat].unique())>10:
            df_prop, _ = split_prop_others(df, cat, use_etc, category_count=10)
            if len(df_prop)<10:
                df_prop = df_prop.rename(columns={cat: "name"})
            counts = {row.name: row.count for row in df_prop.itertuples()}
        else:
            series = df[cat].dropna().astype(str)
            counts = series.value_counts().to_dict()

        x_size, y_size = common_option['x_size'], common_option['y_size']
        chart_nm = common_option.get("chart_nm", "auto")
        chart_nm_font_size = common_option.get("chart_nm_font_size", "auto")
        auto_title = f"TreeMap - {cat}"
        chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size
        chart_nm = auto_title if chart_nm=="auto" else chart_nm

        if len(counts)<=10:
            cmap = sns.color_palette("deep")
            colors = [cmap[i] for i,_ in enumerate(counts.items())]
        else:
            cmap = sns.color_palette("viridis", as_cmap=True)
            colors = [cmap(i*10) for i,_ in enumerate(counts.items())]

        fig, ax = init_figure_axes(x_size, y_size)
        ax.set_axis_off()
        squarify.plot(
            sizes=[v for _,v in counts.items()],
            label=[f"{k}\n({v:,.0f})" for k,v in counts.items()],
            color=colors,
            text_kwargs={"fontweight": "bold", "color": "black"},
            pad=True,
            ax=ax
        )
        ax.set_title(chart_nm,
                    fontdict=dict(fontsize=chart_nm_font_size,
                                fontweight='bold', fontproperties=DBDREAM))
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img

def mosaic_chart(
    project_dir: str,
    x_cat: str,
    y_cat: str,
    common_option: dict
    ):
    """ 모자이크 차트 생성 """
    img = None
    data_path = os.path.join(project_dir, "data.pkl")
    try:
        df = pd.read_pickle(data_path)
        x_size, y_size = common_option['x_size'], common_option['y_size']
        chart_nm = common_option.get("chart_nm", "auto")
        chart_nm_font_size = common_option.get("chart_nm_font_size", "auto")
        auto_title = f"Mosaic - {x_cat} vs {y_cat}"
        chart_nm_font_size = 15 if chart_nm_font_size=="auto" else chart_nm_font_size
        chart_nm = auto_title if chart_nm=="auto" else chart_nm

        fig, ax = init_figure_axes(x_size, y_size)
        mosaic(df, [x_cat, y_cat], gap=.01, ax=ax)
        update_chart_with_common_option(ax, auto_title,
                                        {"x_axis":x_cat, "y_axis":y_cat}, common_option)
        img = save_chart_to_bytes(fig)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
