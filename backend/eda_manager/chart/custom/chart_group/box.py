# pylint: disable=W0613, W0718, E1101
"""
박스형 차트 생성기
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from eda_manager.chart.chart_helper import (update_chart_with_common_option,
                                            save_chart_to_bytes,
                                            close_pyplot, DBDREAM)

def box(
    project_dir: str,
    cat: str, num: str, g_cat: str, large_g_cat: str,
    orient: str,
    color: str, fill: bool, gap: float,
    line_width: int, line_color: str,
    box_kind: str,
    common_option: dict):
    """ 박스형 차트 : 통합 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        if cat is not None:
            df = df.dropna(subset=[cat])
            df[cat] = df[cat].astype(str)
        orient = "y" if orient=="auto" else orient
        box_kind = "box" if box_kind=="auto" else box_kind
        auto_title = None
        x_axis_auto_title = None
        y_axis_auto_title = None
        is_x_cat = orient=="y"
        is_pass_title = False

        options = {"data": df, "kind": box_kind, "fill": fill}
        if color != "auto":
            options.update({"color": color})
        if line_color != "auto":
            options.update({"linecolor": line_color})
        if line_width != "auto":
            options.update({"linewidth": line_width})
        if cat is not None:
            auto_title = f"{box_kind.capitalize()} 차트 - {cat} vs {num}"
            options.update({"x": num if orient=="x" else cat,
                            "y": cat if orient=="x" else num})
            x_axis_auto_title = cat if orient=="y" else num
            y_axis_auto_title = num if orient=="y" else cat
            if g_cat is not None:
                auto_title += f"(by {g_cat})"
                options.update({"hue": g_cat})
                if (box_kind == "violin") and (len(df[g_cat].dropna().unique())%2==0):
                    options.update({"split": True})
                if gap != "auto":
                    options.update({"gap": float(gap)})
                if large_g_cat is not None:
                    is_pass_title = True
                    auto_title += f", 대분류:{large_g_cat}"
                    options.update({"col": large_g_cat})
        else:
            auto_title = f"{box_kind.capitalize()} 차트 - {num}"
            if color != "auto":
                options.update({"color": color})
            if orient == "x":
                options.update({"x": num})
                x_axis_auto_title = num
                y_axis_auto_title = None
            else:
                options.update({"y": num})
                x_axis_auto_title = None
                y_axis_auto_title = num

        g = sns.catplot(**options)
        def update_axes(data, **kws):
            ax = plt.gca()

            update_chart_with_common_option(
                ax, auto_title,
                {"x_axis":x_axis_auto_title, "y_axis":y_axis_auto_title},
                common_option,
                is_x_dt=is_x_cat, is_y_dt=not is_x_cat, pass_title=is_pass_title)
        if is_pass_title:
            g.fig.suptitle(auto_title,
                           fontdict=dict(fontsize=15, fontweight='bold', fontproperties=DBDREAM))
        g.map_dataframe(update_axes)
        img = save_chart_to_bytes(g)
    except Exception as e:
        print(e)
    close_pyplot()
    return img
