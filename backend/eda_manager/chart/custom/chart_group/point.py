# pylint: disable=W0613, W0718, E1101
"""
포인트 차트 생성기
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from eda_manager.chart.chart_helper import (update_chart_with_common_option,
                                            save_chart_to_bytes,
                                            close_pyplot, DBDREAM)

def sample_keep_outliers_iqr(
    df: pd.DataFrame,
    y: str,                  # swarmplot의 y(수치 컬럼)
    x: str | None = None,    # swarmplot의 x(그룹 컬럼) 없으면 None
    apply_over_n: int = 500,
    max_total: int = 500,    # 최종 최대 샘플 수(대략)
    iqr_k: float = 1.5,
    random_state: int = 42,
) -> pd.DataFrame:
    """ 데이터 크기가 클 경우 샘플링 : 그룹 반영 """
    n = len(df)
    if n <= apply_over_n:
        return df

    # y 결측은 제외(스웜플롯도 어차피 찍기 애매)
    work = df.loc[df[y].notna()].copy()
    def _outlier_mask_iqr(s: pd.Series) -> pd.Series:
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        lo = q1 - iqr_k * iqr
        hi = q3 + iqr_k * iqr
        return (s < lo) | (s > hi)
    if x is None:
        out_mask = _outlier_mask_iqr(work[y])
        out = work[out_mask]
        inl = work[~out_mask]
        # outlier가 너무 많으면(드물지만) 일단 전부 포함 → max_total보다 커질 수 있음
        remain = max(max_total - len(out), 0)
        if remain == 0:
            return out
        sampled_inl = inl.sample(
            n=min(remain, len(inl)),
            random_state=random_state
        )
        return pd.concat([out, sampled_inl], axis=0)

    # 그룹별 IQR로 outlier 잡기
    out_parts = []
    inl_parts = []
    for _, g in work.groupby(x, sort=False):
        m = _outlier_mask_iqr(g[y])
        out_parts.append(g[m])
        inl_parts.append(g[~m])
    out = pd.concat(out_parts, axis=0)
    inl = pd.concat(inl_parts, axis=0)
    # 그룹별로 inlier 샘플 수 배분(대략 균등)
    remain = max(max_total - len(out), 0)
    if remain == 0:
        return out

    groups = list(inl.groupby(x, sort=False))
    if not groups:
        return out
    # 그룹 수만큼 균등 할당 + 남는 건 순차적으로 1개씩
    k = len(groups)
    base = remain // k
    extra = remain % k
    sampled = []
    for i, (_, g) in enumerate(groups):
        take = base + (1 if i < extra else 0)
        if take <= 0:
            continue
        sampled.append(g.sample(n=min(take, len(g)), random_state=random_state))

    sampled_inl = pd.concat(sampled, axis=0) if sampled else inl.iloc[0:0]
    return pd.concat([out, sampled_inl], axis=0)

def point(
    project_dir: str,
    cat: str, num: str, g_cat: str, large_g_cat: str,
    orient: str, color: str, point_kind: str,
    common_option: dict):
    """ 박스형 차트 : 통합 """
    img = None
    data_path = os.path.join(project_dir, 'data.pkl')
    try:
        df = pd.read_pickle(data_path)
        if cat is not None:
            df = df.dropna(subset=[cat])
            df[cat] = df[cat].astype(str)
        if point_kind == "swarm" and len(df)>500:
            df = sample_keep_outliers_iqr(df, num, cat)
        orient = "y" if orient=="auto" else orient
        point_kind = "strip" if point_kind=="auto" else point_kind
        auto_title = None
        x_axis_auto_title = None
        y_axis_auto_title = None
        is_x_cat = orient=="y"
        is_pass_title = False

        options = {"data": df, "kind": point_kind}
        if color != "auto":
            options.update({"color": color})
        if cat is not None:
            auto_title = f"{point_kind.capitalize()} 차트 - {cat} vs {num}"
            options.update({"x": num if orient=="x" else cat,
                            "y": cat if orient=="x" else num})
            x_axis_auto_title = cat if orient=="y" else num
            y_axis_auto_title = num if orient=="y" else cat
            if g_cat is not None:
                auto_title += f"(by {g_cat})"
                options.update({"hue": g_cat})
                if large_g_cat is not None:
                    is_pass_title = True
                    auto_title += f", 대분류:{large_g_cat}"
                    options.update({"col": large_g_cat})
        else:
            auto_title = f"{point_kind.capitalize()} 차트 - {num}"
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
