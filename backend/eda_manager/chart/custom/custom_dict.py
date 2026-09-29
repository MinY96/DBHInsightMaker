# pylint: disable=W0718
"""
관계형 차트 관련 집합
"""
from enum import Enum
from eda_manager.chart.chart_helper import common_option

class OptionType(Enum):
    """ 차트 옵션 타입 클래스 """
    STRING = "string"
    INT = "int"
    DOUBLE = "double"
    DATETIME = "datetime"
    BOOL = "bool"
    USERCONTROL = "usercontrol"

class OptionControl(Enum):
    """ 차트 옵션 컨트롤 클래스 """
    TEXTBOX = "TextBox"
    INTUPDOWN = "IntegerUpDown"
    DOUBLEUPDOWN = "DoubleUpDown"
    DATETIME = "DateTimePicker"
    COMBOBOX = "ComboBox"
    COLOR = "ColorPicker"
    CHECKBOX = "CheckBox"
    LINES = "LinesOption"
    ADDCOLUMN = "AddColumnOption"

def chart_desc_dict(chart_group, chart_type):
    """차트 정보 한글 변환"""
    if chart_group == "scatter":
        match chart_type:
            case "num_num":
                return "산점도 [x축: 수치, y축: 수치]"
            case "num_num_by_cat":
                return "범주형 변수 기준 그룹화된 산점도 [x축: 수치, y축: 수치]"
            case "num_num_num":
                return "3d 산점도 [x축: 수치, y축: 수치, z축: 수치]"
            case "num_num_num_stem":
                return "투영선이 있는 3d 산점도 [x축: 수치, y축: 수치, z축: 수치]"
            case "num_num_num_by_cat":
                return "범주형 변수 기준 그룹화된 3d 산점도 [x축: 수치, y축: 수치, z축: 수치]"
            case "num_num_num_stem_by_cat":
                return "범주형 변수 기준 그룹화된 투영선이 있는 3d 산점도 [x축: 수치, y축: 수치, z축: 수치]"
    if chart_group == "line":
        match chart_type:
            case "index_num":
                return "라인 차트 [x축: 인덱스, y축: 수치]"
            case "index_nums":
                return "라인 차트 [x축: 인덱스, y축: 수치 N개]"
            case "index_num_cat":
                return "범주형 변수 기준 라인 차트 [x축: 인덱스, y축: 수치]"
            case "dt_num":
                return "라인 차트 [x축: 시계열, y축: 수치]"
            case "dt_nums":
                return "라인 차트 [x축: 시계열, y축: 수치 N개]"
            case "dt_num_cat":
                return "범주형 변수 기준 라인 차트 [x축: 시계열, y축: 수치]"
    if chart_group == "bar":
        match chart_type:
            case "pareto":
                return "파레토 차트"
            case "count":
                return "분포형(빈도/백분위/비율) 바 차트 [x/y축: 범주]"
            case "count_cat":
                return "분포형(빈도/백분위/비율) 그룹/누적형 바 차트 [x/y축: 범주, 그룹(대그룹): 범주]"
            case "bar_cat_num":
                return "기술통계 요약 바 차트 [x/y축: 범주, 값: 수치]"
            case "bar_cat_num_cat":
                return "기술통계 요약 그룹/누적형 바 차트 [x/y축: 범주, 값: 수치, 그룹(대그룹): 범주]"
    if chart_group == "box":
        match chart_type:
            case "num":
                return "박스형 차트 [x/y축: 수치]"
            case "num_cat":
                return "범주형 변수 기준 박스형 차트 [x/y축: 수치, 그룹: 범주]"
            case "num_cat_cat":
                return "범주형 변수 기준 박스형 차트 [x/y축: 수치, 그룹(대그룹): 범주]"
    if chart_group == "point":
        match chart_type:
            case "num":
                return "포인트 차트 [x/y축: 수치]"
            case "num_cat":
                return "범주형 변수 기준 포인트 차트 [x/y축: 수치, 그룹: 범주]"
            case "num_cat_cat":
                return "범주형 변수 기준 포인트 차트 [x/y축: 수치, 그룹(대그룹): 범주]"
    if chart_group == "dist":
        match chart_type:
            case "dist_num":
                return "분포형 차트 [x/y축: 수치]"
            case "dist_num_cat":
                return "범주형 변수 기준 분포형 차트 [x/y축: 수치, 그룹(대그룹): 범주]"
            case "dist_num_num":
                return "두 수치형 변수 간 관계형 차트 [x축: 수치, y축: 수치]"
            case "dist_num_num_cat":
                return "범주형 변수 기준 두 수치형 변수 간 관계형 차트 [x축: 수치, y축: 수치, 그룹(대그룹): 범주]"
            case "dist_cat_cat_num":
                return "두 범주형 변수 간 관계 요약 차트 [x축: 범주, y축: 범주, 값: 수치-요약]"
    if chart_group == "proportion":
        match chart_type:
            case "pie":
                return "범주별 비율을 전체 대비 관점에서 직관적으로 시각화"
            case "wordcloud":
                return "범주의 상대적 빈도나 중요도를 시각적 강조로 빠르게 파악"
            case "waffle":
                return "전체를 기준 단위로 나누어 범주 비중을 직관적으로 체감"
            case "treemap":
                return "범주 간 비중과 계층 구조를 동시에 면적 기반으로 표현"
            case "mosaic":
                return "범주 간 비중 면적 구조로 표현"
    if chart_group == "timeseries":
        match chart_type:
            case "dist_dt":
                return "DateTime 타입 별 히스토그램"

def chart_option(opt_type: OptionType, name: str, control: OptionControl,
                 min_val=None, max_val=None, min_double_val=None, max_double_val=None,
                 option=None, padding_left=0):
    """ 차트 옵션 생성기 """
    return {
        "type": opt_type.value,
        "name": name,
        "control": control.value,
        "min": min_val,
        "max": max_val,
        "mindouble": min_double_val,
        "maxdouble": max_double_val,
        "option": option,
        "paddingleft": padding_left
    }

chart_option_ui = {
    "chart_nm": chart_option(OptionType.STRING, "차트 제목", OptionControl.TEXTBOX),
    "chart_nm_font_size": chart_option(OptionType.INT, "차트 제목 폰트 크기", OptionControl.INTUPDOWN, 1),
    "axis_font_size": chart_option(OptionType.INT, "축 제목 폰트 크기", OptionControl.INTUPDOWN, 1),
    "x_axis_nm": chart_option(OptionType.STRING, "X축 제목", OptionControl.TEXTBOX),
    "y_axis_nm": chart_option(OptionType.STRING, "Y축 제목", OptionControl.TEXTBOX),
    "y_axis2_nm": chart_option(OptionType.STRING, "Y(보조)축 제목", OptionControl.TEXTBOX),
    "z_axis_nm": chart_option(OptionType.STRING, "Z축 제목", OptionControl.TEXTBOX),

    "group_nm": chart_option(OptionType.STRING, "그룹 컬럼", OptionControl.TEXTBOX),

    "x_axis_rotate": chart_option(OptionType.INT, "X축 라벨 회전", OptionControl.INTUPDOWN, -364, 364),
    "y_axis_rotate": chart_option(OptionType.INT, "Y축 라벨 회전", OptionControl.INTUPDOWN, -364, 364),
    "y_axis2_rotate": chart_option(OptionType.INT, "Y(보조)축 라벨 회전", OptionControl.INTUPDOWN,
                                   -364, 364),
    "z_axis_rotate": chart_option(OptionType.INT, "Z축 라벨 회전", OptionControl.INTUPDOWN, -364, 364),

    "ncol": chart_option(OptionType.INT, "컬럼 수", OptionControl.INTUPDOWN, 1, 25),
    "nrow": chart_option(OptionType.INT, "행 수", OptionControl.INTUPDOWN, 1, 25),
    "scale_type": chart_option(OptionType.STRING, "차트 스케일 옵션", OptionControl.COMBOBOX,
                               option=["nearest", "floor", "ceil"]),

    "x_axis_lim_min": chart_option(OptionType.DOUBLE, "X축 범위(최소)", OptionControl.DOUBLEUPDOWN),
    "x_axis_lim_max": chart_option(OptionType.DOUBLE, "X축 범위(최대)", OptionControl.DOUBLEUPDOWN),
    "y_axis_lim_min": chart_option(OptionType.DOUBLE, "Y축 범위(최소)", OptionControl.DOUBLEUPDOWN),
    "y_axis_lim_max": chart_option(OptionType.DOUBLE, "Y축 범위(최대)", OptionControl.DOUBLEUPDOWN),
    "gap": chart_option(OptionType.DOUBLE, "동일 그룹간 간격", OptionControl.DOUBLEUPDOWN,
                        min_double_val=0.0, max_double_val=1.0),
    "x_axis_lim_min_dt": chart_option(OptionType.DATETIME, "X축 범위(최소)", OptionControl.DATETIME),
    "x_axis_lim_max_dt": chart_option(OptionType.DATETIME, "X축 범위(최대)", OptionControl.DATETIME),

    "x_size": chart_option(OptionType.INT, "차트 사이즈(가로: 인치)", OptionControl.INTUPDOWN, 1, 20),
    "y_size": chart_option(OptionType.INT, "차트 사이즈(세로: 인치)", OptionControl.INTUPDOWN, 1, 20),

    "num": chart_option(OptionType.STRING, "수치형 컬럼 - 필수선택", OptionControl.COMBOBOX),
    "x_num": chart_option(OptionType.STRING, "X축 컬럼(수치형) - 필수선택", OptionControl.COMBOBOX),
    "x_cat": chart_option(OptionType.STRING, "X축 컬럼(범주형) - 필수선택", OptionControl.COMBOBOX),
    "y_num": chart_option(OptionType.STRING, "Y축 컬럼(수치형) - 필수선택", OptionControl.COMBOBOX),
    "y_cat": chart_option(OptionType.STRING, "Y축 컬럼(범주형) - 필수선택", OptionControl.COMBOBOX),
    "z_num": chart_option(OptionType.STRING, "Z축 컬럼(수치형) - 필수선택", OptionControl.COMBOBOX),

    "cat": chart_option(OptionType.STRING, "범주형 컬럼 - 필수선택", OptionControl.COMBOBOX),
    "g_cat": chart_option(OptionType.STRING, "그룹 컬럼(범주형) - 필수선택", OptionControl.COMBOBOX),
    "large_g_cat": chart_option(OptionType.STRING, "그룹 컬럼(범주형, 대분류)", OptionControl.COMBOBOX),
    "x_dt": chart_option(OptionType.STRING, "X축 컬럼(DateTime) - 필수선택", OptionControl.COMBOBOX),
    "dt": chart_option(OptionType.STRING, "DateTime 컬럼 - 필수선택", OptionControl.COMBOBOX),

    "y_nums": chart_option(OptionType.USERCONTROL, "Y축 컬럼(수치형 N개) - 필수선택", OptionControl.ADDCOLUMN),

    "box_kind": chart_option(OptionType.STRING, "박스 타입", OptionControl.COMBOBOX,
                             option=["box", "violin", "boxen"]),
    "dist_kind": chart_option(OptionType.STRING, "분포 타입", OptionControl.COMBOBOX,
                             option=["hist", "kde"]),
    "point_kind": chart_option(OptionType.STRING, "포인트 타입", OptionControl.COMBOBOX,
                             option=["strip", "swarm"]),
    "fill": chart_option(OptionType.BOOL, "채우기 여부", OptionControl.CHECKBOX),
    "orient": chart_option(OptionType.STRING, "차트 방향", OptionControl.COMBOBOX, option=["x", "y"]),
    "stat": chart_option(OptionType.STRING, "집계 타입", OptionControl.COMBOBOX,
                         option=["count", "percent", "proportion"]),
    "estimator": chart_option(OptionType.STRING, "집계 함수", OptionControl.COMBOBOX,
                              option=["평균", "합계", "최대", "최소", "중앙값", "표준편차"]),
    "show_label": chart_option(OptionType.BOOL, "라벨 표시", OptionControl.CHECKBOX),
    "show_val": chart_option(OptionType.BOOL, "값 표시", OptionControl.CHECKBOX),
    "label_pos": chart_option(OptionType.STRING, "라벨 표시 위치", OptionControl.COMBOBOX,
                         option=["center", "edge"]),
    "color": chart_option(OptionType.STRING, "차트 색상", OptionControl.COLOR),
    "line_color": chart_option(OptionType.STRING, "라인 색상", OptionControl.COLOR),
    "bar_color": chart_option(OptionType.STRING, "바 색상", OptionControl.COLOR),
    "marker": chart_option(OptionType.STRING, "마커 모양", OptionControl.COMBOBOX,
                           option=[".", "o", "s", "p", "*", "D", "d"]),
    "marker_size": chart_option(OptionType.INT, "마커 크기", OptionControl.INTUPDOWN, 1, 300),

    "line_style": chart_option(OptionType.STRING, "라인 스타일", OptionControl.COMBOBOX,
                               option=["-", "--", ":", "-."]),
    "line_width": chart_option(OptionType.INT, "라인 너비", OptionControl.INTUPDOWN),

    "kde": chart_option(OptionType.BOOL, "KDE 표시", OptionControl.CHECKBOX),
    "log_scale": chart_option(OptionType.BOOL, "축 스케일링(로그)", OptionControl.CHECKBOX),
    "x_log_scale": chart_option(OptionType.BOOL, "X축 스케일링(로그)", OptionControl.CHECKBOX),
    "y_log_scale": chart_option(OptionType.BOOL, "Y축 스케일링(로그)", OptionControl.CHECKBOX),
    "reg_line": chart_option(OptionType.BOOL, "회귀선 표시", OptionControl.CHECKBOX),
    "reg_line_color": chart_option(OptionType.STRING, "회귀선 색상",
                                   OptionControl.COLOR, padding_left=15),

    "legend_pos": chart_option(OptionType.STRING, "범주 표시 위치", OptionControl.COMBOBOX,
                               option=["best", "upper left", "upper right", "upper center",
                              "lower left", "lower right", "lower center"]),
    "stem_line_color": chart_option(OptionType.STRING, "투영선 색상", OptionControl.COLOR),
    "stem_axis": chart_option(OptionType.STRING, "투영 기준 축", OptionControl.COMBOBOX, 
                              option=["x", "y", "z"]),

    "gif": chart_option(OptionType.BOOL, "GIF 파일 여부", OptionControl.CHECKBOX),
    "rotate_axis": chart_option(OptionType.STRING, "회전 축", OptionControl.COMBOBOX,
                                option=["vertical", "horizontal"], padding_left=15),

    "use_etc": chart_option(OptionType.BOOL, "기타 항목 사용", OptionControl.CHECKBOX),
    "show_etc_detail": chart_option(OptionType.BOOL, "기타 세부내용 표시", OptionControl.CHECKBOX),
    "group_type": chart_option(OptionType.STRING, "그룹 시각화 타입", OptionControl.COMBOBOX,
                               option=["grouped", "stacked"]),

    "lines": chart_option(OptionType.USERCONTROL, "수평/수직선 표시", OptionControl.LINES)
}

init_chart_option = {
    "scatter": {
        "num_num": {
            "x_num": None, "y_num": None,
            "color": "auto", "marker": "auto", "marker_size": "auto",
            "reg_line": "auto", "reg_line_color": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_num_by_cat": {
            "x_num": None, "y_num": None, "g_cat": None,
            "marker_size": "auto",
            "reg_line": "auto",
            "legend_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_num_num": {
            "x_num": None, "y_num": None, "z_num": None,
            "color": "auto", "marker": "auto", "marker_size": "auto",
            "gif": "false", "rotate_axis": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", z_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", z_axis_rotate="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_num_num_stem": {
            "x_num": None, "y_num": None, "z_num": None,
            "color": "auto", "marker": "auto", "marker_size": "auto",
            "stem_line_color": "auto", "stem_axis": "auto",
            "gif": "false", "rotate_axis": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", z_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", z_axis_rotate="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_num_num_by_cat": {
            "x_num": None, "y_num": None, "z_num": None, "g_cat": None,
            "legend_pos": "auto",
            "marker": "auto", "marker_size": "auto",
            "gif": "false", "rotate_axis": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", z_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", z_axis_rotate="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_num_num_stem_by_cat": {
            "x_num": None, "y_num": None, "z_num": None, "g_cat": None,
            "legend_pos": "auto",
            "marker": "auto", "marker_size": "auto",
            "stem_axis": "auto",
            "gif": "false", "rotate_axis": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", z_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", z_axis_rotate="auto",
                x_size="auto", y_size="auto"
            )
        },
    },
    "bar": {
        "pareto": {
            "cat": None,
            "bar_color": None, "line_color": "auto",
            "use_etc": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_size="auto", y_size="auto", axis_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                x_axis_rotate="auto"
            )
        },
        "count": {
            "cat": None,
            "orient": "auto",
            "color": "auto",
            "stat": "auto",
            "show_label": "auto",
            "label_pos": "auto",
            "use_etc": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "count_cat": {
            "cat": "auto", "g_cat": None, "large_g_cat": None,
            "orient": "auto",
            "stat": "auto",
            "group_type": "auto",
            "show_label": "auto",
            "label_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "bar_cat_num": {
            "cat": None, "num": None,
            "orient": "auto",
            "estimator": "auto",
            "color": "auto",
            "show_label": "auto", "label_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto")
        },
        "bar_cat_num_cat": {
            "cat": None, "num": None, "g_cat": None, "large_g_cat": None,
            "orient": "auto", "estimator": "auto",
            "group_type": "auto",
            "show_label": "auto", "label_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto")
        }
    },
    "line": {
        "index_num": {
            "y_num": None,
            "color": "auto", "line_style": "auto", "line_width": "auto",
            "marker": "auto", "marker_size": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        },
        "index_nums": {
            "y_nums": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", y_axis2_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", y_axis2_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        },
        "index_num_cat": {
            "y_num": None, "g_cat": None,
            "line_width": "auto",
            "marker_size": "auto",
            "legend_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        },
        "dt_num": {
            "x_dt": None, "y_num": None,
            "color": "auto", "line_style": "auto", "line_width": "auto",
            "marker": "auto", "marker_size": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min_dt="auto", x_axis_lim_max_dt="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        },
        "dt_num_cat": {
            "x_dt": None, "y_num": None, "g_cat": None,
            "line_width": "auto",
            "marker_size": "auto",
            "legend_pos": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min_dt="auto", x_axis_lim_max_dt="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        },
        "dt_nums": {
            "x_dt": None, "y_nums": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto", y_axis2_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto", y_axis2_rotate="auto",
                x_axis_lim_min_dt="auto", x_axis_lim_max_dt="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            ),
            "lines": "auto",
        }
    },
    "box": {
        "num_cat_cat": {
            "cat": None, "num": None, "g_cat": None, "large_g_cat": None,
            "orient": "auto", "fill": "auto",
            "gap": "auto", "line_width": "auto", "line_color": "auto",
            "box_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_cat": {
            "cat": None, "num": None,
            "orient": "auto", "color": "auto", "fill": "auto",
            "line_width": "auto", "line_color": "auto",
            "box_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num": {
            "num": None,
            "orient": "auto", "color": "auto", "fill": "auto",
            "line_width": "auto", "line_color": "auto",
            "box_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        }
    },
    "point": {
        "num_cat_cat": {
            "cat": None, "num": None, "g_cat": None, "large_g_cat": None,
            "orient": "auto", "point_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num_cat": {
            "cat": None, "num": None,
            "orient": "auto", "color": "auto", "point_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "num": {
            "num": None, "orient": "auto", "color": "auto",
            "point_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        }
    },
    "dist": {
        "dist_num": {
            "num": None,
            "orient": "auto", "color": "auto", "fill": "auto",
            "kde": "auto", "log_scale": "auto",
            "dist_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "dist_num_cat": {
            "num": None, "g_cat": None, "large_g_cat": None,
            "orient": "auto", "fill": "auto",
            "kde": "auto", "log_scale": "auto",
            "dist_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "dist_num_num": {
            "x_num": None, "y_num": None,
            "color": "auto", "fill": "auto",
            "x_log_scale": "auto", "y_log_scale": "auto",
            "dist_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "dist_num_num_cat": {
            "x_num": None, "y_num": None, "g_cat": None, "large_g_cat": None,
            "fill": "auto",
            "x_log_scale": "auto", "y_log_scale": "auto",
            "dist_kind": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        },
        "dist_cat_cat_num": {
            "x_cat": None, "y_cat": None, "num": None,
            "estimator": "auto", "show_val": "true",
            "line_width": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_axis_rotate="auto", y_axis_rotate="auto",
                x_axis_lim_min="auto", x_axis_lim_max="auto",
                y_axis_lim_min="auto", y_axis_lim_max="auto",
                x_size="auto", y_size="auto"
            )
        }
    },
    "proportion": {
        "pie": {
            "cat": None,
            "use_etc": "true", "show_etc_detail": "true",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                axis_font_size="auto",
                x_size="auto", y_size="auto"
            )
        },
        "wordcloud": {
            "cat": None,
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_size="auto", y_size="auto"
            )
        },
        "waffle": {
            "cat": None,
            "use_etc": "false",
            "nrow": "auto", "ncol": "auto",
            "scale_type": "auto",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_size="auto", y_size="auto"
            )
        },
        "treemap": {
            "cat": None,
            "use_etc": "false",
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_size="auto", y_size="auto"
            )
        },
        "mosaic": {
            "x_cat": None, "y_cat": None,
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                x_axis_nm="auto", y_axis_nm="auto",
                axis_font_size="auto",
                x_size="auto", y_size="auto"
            )
        },
    },
    "timeseries": {
        "dist_dt": {
            "dt": None,
            "common_option": common_option(
                chart_nm="auto", chart_nm_font_size="auto",
                axis_font_size="auto",
                x_axis_rotate="auto"
            )
        },
    }
}

def encode_ui_chart_option(chart_group: str, chart_type: str):
    """ Chart 생성 옵션을 UI용 정보로 인코딩 """
    ops = init_chart_option[chart_group][chart_type]
    ui_option = {}
    for para, value in ops.items():
        if para == "common_option":
            for common_para, common_value in value.items():
                item = chart_option_ui.get(common_para, None)
                item.update({"value": common_value})
                ui_option[common_para] = item
        else:
            item = chart_option_ui.get(para, None)
            item.update({"value": value})
            ui_option[para] = item
    return ui_option

def select_ui_chart_option(chart_group: str, chart_type: str):
    """ Chart 생성 옵션을 UI용 정보로 인코딩 """
    result, err = None, None
    try:
        ops = init_chart_option[chart_group][chart_type]
        ui_option = []
        for para, value in ops.items():
            if para == "common_option":
                for common_para, common_value in value.items():
                    item = chart_option_ui.get(common_para, None)
                    item.update({"key": common_para, "value": common_value})
                    ui_option.append(item)
            else:
                item = chart_option_ui.get(para, None)
                item.update({"key": para, "value": value})
                ui_option.append(item)
        result = {
            "ChartGroup": chart_group,
            "ChartType": chart_type,
            "Description": chart_desc_dict(chart_group, chart_type),
            "Options": ui_option
        }
    except Exception as e:
        err = str(e)
    return result, err

def decode_ui_chart_opiton(chart_group: str, chart_type: str, option: dict):
    """ UI에서 전달받은 Chart 생성 옵션을 디코딩 """
    keys = list(init_chart_option[chart_group][chart_type].keys())
    keys.append("project_dir")
    common = {}
    remove_keys = []
    for key, value in option.items():
        if key not in keys:
            remove_keys.append(key)
            common[key] = value
    option.update({"common_option": common})
    option = {k:v for k,v in option.items() if k not in remove_keys}
    return option
