# pylint: disable=W0718
"""
InsightMaker API
"""

import os
from datetime import datetime
import threading
from typing import Dict
from flask import Flask, jsonify, request
from project_manager import (project_infos, create_project, delete_project, update_project_info,
                             load_csv_file, load_excel_file, load_excel_sheets,
                             load_file_info, load_column_info,
                             save_data_as_excel, save_summary_as_excel)
from eda_manager import (load_column_init_data, load_column_unique_data,
                         convert_column_type, remove_column,
                         get_column_charts,
                         get_normality_result, get_relative_chart,
                         get_correlation_result, get_regression_result,
                         create_new_column, get_custom_chart)
from eda_manager.chart.custom.custom_dict import select_ui_chart_option
from database_manager import PostgreSQL

route_counts = {}
lock = threading.Lock()
USER_ID = os.path.basename(os.path.expanduser("~"))
LOG_FILE = 'route_counts.log'

def initialize():
    """ Route 사용 초기화 """
    global route_counts
    # 로그 파일 초기화
    with open(LOG_FILE, 'w') as f:
        pass
    route_counts = {}

app = Flask(__name__)
with app.app_context():
    # 애플리케이션 시작 시 한 번 실행될 코드
    initialize()

def load_counts():
    """ Route 카운팅 정보 로드 """
    counts = {}
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                route, count = line.strip().split(",")
                counts[route] = int(count)
    except FileNotFoundError:
        pass
    return counts

def save_counts():
    """ Route 카운팅 정보 저장 """
    with open(LOG_FILE, 'w') as f:
        for route, count in route_counts.items():
            f.write(f"{route},{count}\n")

def count_route(route_nm: str):
    """ Route 카운트 증가 """
    with lock:
        route_counts[route_nm] = route_counts.get(route_nm, 0) + 1
        save_counts()

def result_format(result: object, error: str) -> Dict[str, object]:
    """ API 요청 반환 포맷

    Args:
        result (object): 요청 결과
        error (str): 에러 사항

    Returns:
        Dict[str, object]: _description_
    """
    return_format = {
        'result': result,
        'error': error
    }
    return jsonify(return_format), 200

@app.route('/insightmaker/is_open', methods=['GET'])
def check_is_open():
    """ api 실행 여부 확인 """
    return result_format(True, None)

@app.route('/insightmaker/project/project_list', methods=['POST'])
def get_project_list():
    """ 저장된 Project 정보 반환 """
    data = request.get_json()
    project_parent_dir = data.get('ProjectParentDir', None)
    infos = project_infos(project_parent_dir)
    return result_format(*infos)

@app.route('/insightmaker/project/save_raw_data', methods=['POST'])
def post_save_raw_data_as_excel():
    """ 원본 데이터 엑셀 다운로드 """
    count_route("project-save_raw_data")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    save_path = data.get('SavePath', None)
    infos = save_data_as_excel(project_dir, save_path)
    return result_format(*infos)

@app.route('/insightmaker/project/save_summary_data', methods=['POST'])
def post_save_summary_data_as_excel():
    """ 컬럼 요약 데이터 엑셀 다운로드 """
    count_route("project-save_summary_data")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    save_path = data.get('SavePath', None)
    infos = save_summary_as_excel(project_dir, save_path)
    return result_format(*infos)

@app.route('/insightmaker/project/create_project', methods=['POST'])
def post_create_project():
    """ 전달받은 정보로 프로젝트 생성 후 결과 반환 """
    count_route("project-create_project")
    data = request.get_json()
    project_parent_dir = data.get('ProjectParentDir', None)
    project_name = data.get('ProjectName', None)
    project_desc = data.get('ProjectDesc', None)
    infos = create_project(project_parent_dir, project_name, project_desc)
    return result_format(*infos)

@app.route('/insightmaker/project/delete_project', methods=['POST'])
def post_delete_project():
    """ 전달받은 정보의 프로젝트 삭제 후 결과 반환 """
    data = request.get_json()
    project_name = data.get('ProjectName', None)
    project_dir = data.get('ProjectDir', None)
    infos = delete_project(project_name, project_dir)
    return result_format(*infos)

@app.route('/insightmaker/project/update_project', methods=['POST'])
def post_update_project():
    """ 수정된 사항 프로젝트 정보에 업데이트 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    update_info = {
        k:data.get(k, None) for k
        in ['ProjectName', 'ProjectDesc', 'CreateTime', 'IsLoadData']
        if data.get(k,None) is not None
    }
    infos = update_project_info(project_dir, update_info)
    return result_format(*infos)

@app.route('/insightmaker/project/load_data', methods=['POST'])
def post_load_data():
    """ 선택한 파일 업로드 후 결과 반환 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    is_csv = data.get('IsCsv', None)
    sheet_nm = data.get('SheetName', None)
    file_path = data.get('FilePath', None)
    infos = load_csv_file(project_dir, file_path)\
        if is_csv else load_excel_file(project_dir, file_path, sheet_nm)
    return result_format(*infos)

@app.route('/insightmaker/project/load_data/sheet', methods=['POST'])
def post_load_excel_sheets():
    """ 선택한 Excel 파일의 Sheet 명 리스트 반환 """
    data = request.get_json()
    excel_file_path = data.get('ExcelFilePath', None)
    infos = load_excel_sheets(excel_file_path)
    return result_format(*infos)

@app.route('/insightmaker/project/file_info', methods=['POST'])
def post_load_file_info():
    """ 업로드한 파일의 상세정보 반환 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    infos = load_file_info(project_dir)
    return result_format(*infos)

@app.route('/insightmaker/project/column_info', methods=['POST'])
def post_load_column_info():
    """ 업로드한 파일의 컬럼 별 상세정보 반환 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    infos = load_column_info(project_dir)
    return result_format(*infos)

@app.route('/insightmaker/project/remove_column', methods=['POST'])
def post_remove_column():
    """ 데이터 내 컬럼 제거 """
    count_route("project-remove_column")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    infos = remove_column(project_dir, col_nm)
    return result_format(*infos)

@app.route('/insightmaker/project/create_column', methods=['POST'])
def post_create_column():
    """ 데이터 신규 컬럼 추가 """
    count_route("project-create_column")
    data = request.get_json()
    infos = create_new_column(data)
    return result_format(*infos)

@app.route('/insightmaker/project/column_data_init', methods=['POST'])
def post_load_column_data_init():
    """ 선택한 컬럼에 대한 초기 50개 Data 반환 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    infos = load_column_init_data(project_dir, col_nm)
    return result_format(*infos)

@app.route('/insightmaker/project/column_unique_data', methods=['POST'])
def post_load_column_unique_value():
    """ 선택한 컬럼에 대한 고유값 리스트 반환 """
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    infos = load_column_unique_data(project_dir, col_nm)
    return result_format(*infos)

@app.route('/insightmaker/project/convert_column_type', methods=['POST'])
def post_load_converted_column_value():
    """ 컬럼 타입 변환 """
    count_route("project-convert_column_type")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    convert_dtype = data.get('ConvertTo', None)
    datetime_format = data.get('DateTimeFormat', None)
    orders = data.get('OrderInfo', None)
    save_mode = data.get('SaveMode', None)
    infos = convert_column_type(project_dir, col_nm, convert_dtype,
                                datetime_format, orders, save_mode)
    return result_format(*infos)

@app.route('/insightmaker/eda/chart/single', methods=['POST'])
def post_load_column_charts():
    """ 선택한 컬럼에 대한 차트 반환 """
    count_route("eda-show_single_chart")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    infos = get_column_charts(project_dir, col_nm)
    return result_format(*infos)

@app.route('/insightmaker/eda/chart/relative', methods=['POST'])
def post_load_relative_column_charts():
    """ 관계형 차트 반환 """
    count_route("eda-show_relative_chart")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_x = data.get('ColumnX', None)
    col_y = data.get('ColumnY', None)
    col_z = data.get('ColumnZ', None)
    col_v = data.get('ColumnGroup', None)
    infos = get_relative_chart(project_dir, col_x, col_y, col_z, col_v)
    return result_format(*infos)

@app.route('/insightmaker/eda/chart/chart_option', methods=['POST'])
def post_load_chart_options():
    """ 선택한 차트의 옵션 반환 """
    data = request.get_json()
    chart_group = data.get('ChartGroup', None)
    chart_type = data.get('ChartType', None)
    infos = select_ui_chart_option(chart_group, chart_type)
    return result_format(*infos)

@app.route('/insightmaker/eda/chart/custom_chart', methods=['POST'])
def post_load_custom_chart():
    """ 커스텀 차트 반환 """
    count_route("eda-show_custom_chart")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    chart_group = data.get('ChartGroup', None)
    chart_type = data.get('ChartType', None)
    options = data.get('Options', None)
    infos = get_custom_chart(project_dir, chart_group, chart_type, options)
    return result_format(*infos)

@app.route('/insightmaker/eda/stat_test/normality', methods=['POST'])
def post_load_normality_info():
    """ 선택한 컬럼에 대한 정규성 검정 결과 반환 """
    count_route("eda-normality_test")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    col_nm = data.get('Column', None)
    infos = get_normality_result(project_dir, col_nm)
    return result_format(*infos)

@app.route('/insightmaker/eda/analyze/correlation', methods=['POST'])
def post_load_correlation_info():
    """ 선택한 컬럼에 대한 상관분석 결과 반환 """
    count_route("analyze-correlation")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    columns = data.get('Columns', None)
    corr_type = data.get('CorrMethod', None)
    infos = get_correlation_result(project_dir, columns, corr_type)
    return result_format(*infos)

@app.route('/insightmaker/eda/analyze/regression', methods=['POST'])
def post_load_regression_info():
    """ 선택한 옵션에 대한 회귀분석 진행 및 결과 폴더 반환 """
    count_route("analyze-regression")
    data = request.get_json()
    project_dir = data.get('ProjectDir', None)
    indep_vars = data.get('IndepVars', None)
    dep_var = data.get('DepVar', None)
    selection_method = data.get('SelectionMethod', None)
    scaler_method = data.get('ScalerMethod', None)
    impute_method = data.get('ImputeMethod', None)
    is_test = data.get('IsSplit', None)
    test_ratio = data.get('TestRatio', None)
    if not is_test:
        test_ratio = None
    infos = get_regression_result(project_dir, indep_vars, dep_var,
                                  selection_method, scaler_method, impute_method, test_ratio)
    return result_format(*infos)

@app.route('/insightmaker/insert_user_logs', methods=['POST'])
def post_insert_user_logs():
    """ 사용자 사용 로그 업데이트 """
    current_date = datetime.now().strftime("%Y-%m-%d")
    query = "INSERT INTO user_logs (event_time, user_id, main_cat_id, sub_cat_id, counts) VALUES "
    for log, count in load_counts().items():
        main, sub = log.strip().split("-")
        query += f"('{current_date}', '{USER_ID}', '{main}', '{sub}', {count}),"
    if query.endswith(","):
        query = query[:-1]
    query += """ ON CONFLICT (event_time, user_id, main_cat_id, sub_cat_id)
    DO UPDATE SET counts = user_logs.counts + EXCLUDED.counts"""
    db = PostgreSQL("10.145.249.210", "postgres", 5432, "dbh")
    is_insert = db.execute("insightmaker", query)
    return result_format(is_insert, None)

if __name__ == '__main__':
    app.run(host='localhost', port=5050)
