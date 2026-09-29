# pylint: disable=W0718, C0103, C0415
"""
통계 검정 메소드
"""
from typing import Dict, List
import os
import shutil
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from eda_manager.analyze.data_analyze import (CorrelationAnalyze, Preprocessor,
                                              VariableSelector, ResidualAnalyzer,
                                              PredictAnalyzer,
                                              LinearRegressionResult, LogisticRegressionResult)
from helper import read_json_to_dict, dict_to_json

def convert_number_expression(value) -> str:
    """ 값을 표에서 읽기 수월한 형식으로 변경 """
    if isinstance(value, int):
        return f"{value:,}"
    elif isinstance(value, float):
        if (abs(value) < 0.0001) | (abs(value) > 1_000_000):
            return f"{value:.2e}"
        else:
            return f"{value:,.2f}"
    return value

def get_correlation_result(
    project_dir: str, columns: List[str], corr_method: str) -> Dict[str, object]:
    """ 프로젝트 폴더 내 선택한 컬럼 상관 분석 진행

    Args:
        project_dir (str): 프로젝트 경로
        col_nm (str): 컬럼 리스트
        corr_method (str): 상관 분석 Type

    Returns:
        Dict[str, object]: 상관 분석 결과
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    result, error = None, None
    try:
        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        col_infos = [info for info in col_infos if info['Column'] in columns]
        corr = CorrelationAnalyze(df, col_infos, corr_method)
        result = corr.result()
    except Exception as e:
        error = str(e)
    return result, error

def get_regression_result_test(
    reg_project_dir: str,
    X: pd.DataFrame,
    y: pd.Series,
    num_cols: List[str],
    cat_cols: List[str],
    selection_method: str=None,
    scaler: str=None, impute: str='remove', test_ratio: float=None) -> str:
    """ 프로젝트 내 선택한 컬럼 회귀분석 진행

    Args:
        project_dir (str): 프로젝트 경로
        indp_vars (List[str]): 독립변수 리스트
        dep_var (str): 종속변수
        selection_method (str, optional): 변수선택 기법. Defaults to None.
        scaler (str, optional): 스케일러 기법. Defaults to None.
        impute (str, optional): 결측치 처리 기법. Defaults to None.
        test_ratio (float, optional): Test Set 비율. Defaults to None.

    Returns:
        str: 회귀분석 결과 저장 경로
    """
    result, error = None, None
    do_test = test_ratio is not None
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=test_ratio, random_state=42)
        prep = Preprocessor(num_cols=num_cols, cat_cols=cat_cols, scaler=scaler, impute=impute)
        X_train_proc, y_train_enc = prep.fit_transform(X_train, y_train)
        X_test_proc, y_test_enc = prep.transform(X_test, y_test)
        sel = None
        if len(cat_cols)>0:
            sel = VariableSelector(X_train_proc, y_train_enc, method=selection_method,
                                   model_type="auto", group_map=prep.group_map)
        else:
            sel = VariableSelector(X_train_proc, y_train_enc, method=selection_method,
                                   model_type="auto")
        res = sel.select()
        model_type = None
        y_pred_test, y_test_proba, class_names = None, None, None
        if res['model_type'] == 'linear':
            model_type = 'Linear Regression'
            x_test_sel = sm.add_constant(X_test_proc[res['variables']])
            model = res["model"]
            y_pred_test = model.predict(x_test_sel).values
            y_test_enc = y_test_enc.values
        elif res['model_type'] == 'logit':
            model_type = 'Logistic Regression'
            x_test_sel = sm.add_constant(X_test_proc[res['variables']])
            model = res["model"]
            y_test_proba = model.predict(x_test_sel).values
            y_pred_test = (y_test_proba >= 0.5).astype(int)
            y_test_enc = y_test_enc.values
            if prep.y_was_encoded:
                class_names = list(map(str, np.unique(prep.inverse_transform_y(y_pred_test))))
        else:
            model_type = 'MultiNomial Logistic Regression'
            X_test_sel = X_test_proc[res["variables"]]
            model = res["model"]
            y_pred_test = model.predict(X_test_sel)
            y_test_proba = model.predict_proba(X_test_sel)
            class_names = list(map(str, np.unique(prep.inverse_transform_y(y_pred_test))))
        pred_task = 'regression' if model_type == 'Linear Regression' else 'classifier'
        pred = PredictAnalyzer(reg_project_dir, pred_task, y_test_enc,
                               y_pred_test, y_test_proba, class_names, test_ratio)
        result = save_regression_result_test(reg_project_dir, prep, sel, res, pred, model_type)

        info = {
            'RegressionDir': reg_project_dir,
            'CreateTime': datetime.strptime(os.path.basename(reg_project_dir),
                                            '%y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S'),
            'ModelType': model_type,
            'DepVar': "y",
            'Selection': selection_method if selection_method is not None else '',
            'Scaler': scaler if scaler is not None else '',
            'Impute': impute if impute is not None else '',
            'TestRatio': f'{test_ratio:.0%}' if do_test else '' 
        }
        info_path = os.path.join(reg_project_dir, 'info.json')
        dict_to_json(info, info_path)
    except Exception as e:
        error = str(e)
    return result, error

def get_regression_result(
    project_dir: str, indep_vars: List[str], dep_var: str,
    selection_method: str=None,
    scaler: str=None, impute: str='remove', test_ratio: float=None) -> str:
    """ 프로젝트 내 선택한 컬럼 회귀분석 진행

    Args:
        project_dir (str): 프로젝트 경로
        indp_vars (List[str]): 독립변수 리스트
        dep_var (str): 종속변수
        selection_method (str, optional): 변수선택 기법. Defaults to None.
        scaler (str, optional): 스케일러 기법. Defaults to None.
        impute (str, optional): 결측치 처리 기법. Defaults to None.
        test_ratio (float, optional): Test Set 비율. Defaults to None.

    Returns:
        str: 회귀분석 결과 저장 경로
    """
    data_path = os.path.join(project_dir, 'data.pkl')
    column_info_path = os.path.join(project_dir, 'column_info.json')
    result, error = None, None
    do_test = test_ratio is not None
    is_mix = False
    pred = None
    try:
        reg_key = datetime.now().strftime('%y%m%d%H%M%S')
        reg_project_dir = _check_regression_project_dir(project_dir, reg_key)

        df = pd.read_pickle(data_path)
        col_infos = read_json_to_dict(column_info_path)
        num_vars = [col['Column'] for col in col_infos
                    if (col['ColumnType']=='Numerical') and (col['Column'] in indep_vars)]
        cat_vars = [col['Column'] for col in col_infos
                    if (col['ColumnType']=='Categorical') and (col['Column'] in indep_vars)]
        cat_vars = cat_vars if len(cat_vars)>0 else None
        is_mix = cat_vars is not None
        y_col = [col for col in col_infos if col['Column']==dep_var][0]
        y_var = y_col['Column']
        model_type = 'Linear Regression'
        if (y_col['ColumnType'] == 'Numerical') and (y_col['UniqueCount'] > 10):
            model_type = 'Linear Regression'
        elif y_col['UniqueCount']==2:
            model_type = 'Logistic Regression'
        else:
            model_type = 'MultiNomial Logistic Regression'

        df = df.dropna(subset=[y_var]).reset_index(drop=True)
        prep = Preprocessor(num_cols=num_vars, cat_cols=cat_vars, scaler=scaler, impute=impute)
        X_train = df[num_vars + (cat_vars if cat_vars is not None else [])]
        y_train = df[y_var]
        if do_test:
            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train,
                                                            test_size=test_ratio, random_state=42)
        X_train_proc, y_train_enc = prep.fit_transform(X_train, y_train)
        if do_test:
            X_test_proc, y_test_enc = prep.transform(X_test, y_test)

        sel = None
        if is_mix:
            sel = VariableSelector(X_train_proc, y_train_enc, method=selection_method,
                                   model_type="auto", group_map=prep.group_map)
        else:
            sel = VariableSelector(X_train_proc, y_train_enc, method=selection_method,
                                   model_type="auto")
        res = sel.select()
        res['dep_var'] = dep_var
        if do_test:
            y_pred_test, y_test_proba, class_names = None, None, None
            if res['model_type'] == 'linear':
                model_type = 'Linear Regression'
                x_test_sel = sm.add_constant(X_test_proc[res['variables']])
                model = res["model"]
                y_pred_test = model.predict(x_test_sel).values
                y_test_enc = y_test_enc.values
            elif res['model_type'] == 'logit':
                model_type = 'Logistic Regression'
                x_test_sel = sm.add_constant(X_test_proc[res['variables']])
                model = res["model"]
                y_test_proba = model.predict(x_test_sel).values
                y_pred_test = (y_test_proba >= 0.5).astype(int)
                y_test_enc = y_test_enc.values
                if prep.y_was_encoded:
                    class_names = list(map(str, np.unique(prep.inverse_transform_y(y_pred_test))))
            else:
                X_test_sel = X_test_proc[res["variables"]]
                model = res["model"]
                y_pred_test = model.predict(X_test_sel)
                y_test_proba = model.predict_proba(X_test_sel)
                class_names = list(map(str, np.unique(prep.inverse_transform_y(y_pred_test))))
            pred_task = 'regression' if model_type == 'Linear Regression' else 'classifier'
            pred = PredictAnalyzer(reg_project_dir, pred_task, y_test_enc,
                                   y_pred_test, y_test_proba, class_names, test_ratio)
        is_save = save_regression_result(reg_project_dir, prep, sel, res, pred, model_type)
        if is_save:
            result = reg_project_dir
            info = {
                'RegressionDir': reg_project_dir,
                'CreateTime': datetime.strptime(os.path.basename(reg_project_dir),
                                                '%y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S'),
                'ModelType': model_type,
                'DepVar': dep_var if dep_var is not None else '',
                'Selection': selection_method if selection_method is not None else '',
                'Scaler': scaler if scaler is not None else '',
                'Impute': impute if impute is not None else '',
                'TestRatio': f'{test_ratio:.0%}' if do_test else '' 
            }
            info_path = os.path.join(reg_project_dir, 'info.json')
            dict_to_json(info, info_path)
        else:
            result = None
    except Exception as e:
        error = str(e)
        result = None
        shutil.rmtree(reg_project_dir)
    return result, error

def _clear_directory_items(dir_path: str):
    """ 폴더 내 파일, 폴더 제거 """
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        # 폴더 내의 모든 항목을 순회
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            # 파일이면 삭제, 폴더이면 재귀적으로 삭제
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

def _check_regression_project_dir(project_dir: str, reg_key: str) -> str:
    """ 회귀분석 결과 저장 폴더 반환 """
    analyze_dir = os.path.join(project_dir, 'analyze')
    reg_dir = os.path.join(analyze_dir, 'regression')
    if not os.path.exists(analyze_dir):
        os.makedirs(analyze_dir)
    if not os.path.exists(reg_dir):
        os.makedirs(reg_dir)
    reg_project_dir = os.path.join(reg_dir, reg_key)
    if not os.path.exists(reg_project_dir):
        os.makedirs(reg_project_dir)
    for page in ['1_selection', '2_corr', '3_model', '4_residual', '5_test']:
        page_dir = os.path.join(reg_project_dir, page)
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)
        else:
            _clear_directory_items(page_dir)
    return reg_project_dir

def save_regression_result(reg_project_dir: str,
                           prep: Preprocessor, selector: VariableSelector,
                           sel_result: Dict[str, object], pred_info: PredictAnalyzer,
                           model_type: str):
    """ 회귀분석 결과물 저장 """
    is_save = False
    try:
        for page_key in ['1_selection', '2_corr', '3_model', '4_residual', '5_test']:
            if (page_key == '1_selection') and (selector.method is None):
                continue
            if (page_key == '4_residual') and (sel_result['model_type'] in ['logit', 'multilogit']):
                continue
            page_dir = os.path.join(reg_project_dir, page_key)
            page_info_path = os.path.join(page_dir, 'info.json')
            page_info = {}
            page_info['model_type'] = model_type
            match page_key:
                case '1_selection':
                    save_reg_selection_result(page_dir, page_info_path,
                                              page_info, selector, sel_result)
                case '2_corr':
                    save_reg_corr_result(page_dir, page_info_path, page_info, selector, sel_result)
                case '3_model':
                    page_info['model_type'] = model_type
                    save_reg_model_result(page_dir, page_info, prep, sel_result)
                case '4_residual':
                    save_reg_residual_result(page_dir, selector, sel_result)
                case '5_test':
                    save_reg_test_result(page_dir, page_info_path, page_info, prep, pred_info, sel_result)
        is_save = True
    except Exception as e:
        print(e)
        is_save = False
    return is_save

def save_regression_result_test(reg_project_dir: str,
                                prep: Preprocessor, selector: VariableSelector,
                                sel_result: Dict[str, object], pred_info: PredictAnalyzer,
                                model_type: str):
    """ 회귀분석 결과물 저장 """
    if os.path.exists(reg_project_dir):
        for page_key in ['1_selection', '2_corr', '3_model', '4_residual', '5_test']:
            page_dir = os.path.join(reg_project_dir, page_key)
            _clear_directory_items(page_dir)
    for page_key in ['1_selection', '2_corr', '3_model', '4_residual', '5_test']:
        if (page_key == '1_selection') and (selector.method is None):
            continue
        if (page_key == '4_residual') and (sel_result['model_type'] in ['logit', 'multilogit']):
            continue
        page_dir = os.path.join(reg_project_dir, page_key)
        page_info_path = os.path.join(page_dir, 'info.json')
        page_info = {}
        page_info['model_type'] = model_type
        match page_key:
            case '1_selection':
                save_reg_selection_result(page_dir, page_info_path, page_info, selector, sel_result)
            case '2_corr':
                save_reg_corr_result(page_dir, page_info_path, page_info, selector, sel_result)
            case '3_model':
                save_reg_model_result(page_dir, page_info, prep, sel_result)
            case '4_residual':
                save_reg_residual_result(page_dir, selector, sel_result)
            case '5_test':
                save_reg_test_result(page_dir, page_info_path, page_info, prep, pred_info, sel_result)
    return reg_project_dir

def save_reg_selection_result(page_dir: str, page_info_path: str, page_info: Dict[str, object],
                              selector: VariableSelector, sel_result: Dict[str, object]):
    """ 회귀분석 변수 선택 결과 저장 """
    from eda_manager.analyze.data_analyze.chart_creator import plot_aic_history
    def selection_method_converter(method: str):
        match method:
            case 'forward':
                return '전진 선택'
            case 'backward':
                return '후진 제거'
            case 'stepwise':
                return 'StepWise'
        return '-'
    is_save = False
    try:
        page_info['indep_vars'] = sel_result['variables']
        page_info['selection_method'] = selection_method_converter(selector.method)
        col_dic = {
            'step': 'Step',
            'action': 'Action',
            'variables': 'Variables',
            'aic': 'AIC',
            'bic': 'BIC',
            'best': 'Best'
        }
        page_info['selection_hist'] = selector.get_history_df().\
            rename(columns=col_dic).map(convert_number_expression).to_dict('records')
        page_info['selection_hist_img'] = None
        hist_plot_nm = 'selection_history.png'
        plot_save_path = os.path.join(page_dir, hist_plot_nm)
        if plot_aic_history(selector.get_history_df(), plot_save_path):
            page_info['selection_hist_img'] = plot_save_path
        is_save = dict_to_json(page_info, page_info_path)
    except Exception as e:
        print(e)
    return is_save

def save_reg_corr_result(page_dir: str, page_info_path: str, page_info: Dict[str, object],
                         selector: VariableSelector, sel_result: Dict[str, object]):
    """ 독립변수 상관분석 결과 저장 """
    from eda_manager.analyze.data_analyze.chart_creator import plot_vif_score
    is_save = False
    try:
        df = selector.X_in[sel_result['variables']].copy()
        column_infos = [{'Column':col, 'ColumnChar':'Continuous'} for col in df.columns]
        corr = CorrelationAnalyze(df, column_infos, 'pearson')
        page_info = corr.result_with_save(os.path.join(page_dir, 'corr_matrix.png'),
                                        os.path.join(page_dir, 'scatter_matrix.png'))
        page_info['Results'] = page_info['Results'].map(convert_number_expression).to_dict('records')
        vif_score_plot_path = os.path.join(page_dir, 'vif_score.png')
        if plot_vif_score(sel_result['coef_table'], vif_score_plot_path):
            page_info['plot_info']['vif_score_img'] = vif_score_plot_path
        is_save = dict_to_json(page_info, page_info_path)
    except Exception as e:
        print(e)
    return is_save

def save_reg_model_result(page_dir: str, page_info: Dict[str, object],
                          prep: Preprocessor, sel_result: Dict[str, object]):
    """ 회귀모델 정보 저장 """
    is_save = False
    try:
        if page_info['model_type'] == 'Linear Regression':
            lr = LinearRegressionResult(page_dir, sel_result)
            is_save = lr.save_model_result()
        elif page_info['model_type'] == 'Logistic Regression':
            lr = LogisticRegressionResult(page_dir, sel_result, prep)
            is_save = lr.save_model_result()
            
        # page_info['equation'] = 'y = ' + ' + '.join([f"[{row['Coef']:.2f}]*"+unit for
        #                             unit, row in sel_result['coef_table'].iterrows()])\
        #                             if page_info['model_type'] != 'MultiNomial Logistic Regression'\
        #                             else sel_result['equation']
        # model_performance = {
        #     'AIC': sel_result.get('aic', None),
        #     'Adjusted R²': sel_result.get('adj_r2', None),
        #     'RMSE': sel_result.get('rmse', None),
        #     'p-value': sel_result.get('p_value', None),
        #     'R²': sel_result.get('r2', None),
        #     'Log Likelihood': sel_result.get('log_likelihood', None),
        #     'Log Loss': sel_result.get('logloss', None),
        #     'Accuracy': sel_result.get('accuarcy', None)
        # }
        # page_info['model_performance'] = model_performance
        # page_info['coeff_info'] = sel_result['coef_table']\
        #     .reset_index(names='Coef Name').map(convert_number_expression).to_dict('records')
        # df_predict = sel_result['predictions']

        # proba = None
        # class_names = None
        # if page_info['model_type'] == 'Logistic Regression':
        #     proba = df_predict['y_proba']
        # elif page_info['model_type'] == 'MultiNomial Logistic Regression':
        #     proba = sel_result['multi_pred_proba']
        #     class_names = list(map(str, np.unique(prep.inverse_transform_y(df_predict['y']))))
        # pred_task = 'regression' if page_info['model_type'] == 'Linear Regression' else 'classifier'

        # pred = PredictAnalyzer(page_dir, pred_task,
        #                        df_predict['y'], df_predict['y_pred'], proba, class_names)
        # pred_info = pred.analyze()
        # page_info['model_performance'].update(pred_info['model_performance'])
        # page_info['model_performance'] = {k:convert_number_expression(v) for k,v
        #                      in page_info['model_performance'].items()
        #                      if v is not None and v!=""}
        # page_info['plot_info'] = pred_info['plot_info']
        # is_save = dict_to_json(page_info, page_info_path)
    except Exception as e:
        print(e)
    return is_save

def save_reg_residual_result(page_dir: str, selector: VariableSelector,
                             sel_result: Dict[str, object]):
    """ 잔차 분석 결과 저장 """
    is_save = False
    try:
        analyzer = ResidualAnalyzer(
            y=sel_result['y'],
            y_pred=sel_result['y_pred'],
            model_type=sel_result['model_type'],
            model=sel_result['model'],
            output_dir=page_dir
        )
        analyzer.run()
        is_save = True
    except Exception as e:
        print(e)
    return is_save

def save_reg_test_result(page_dir: str, page_info_path: str, page_info: Dict[str, object],
                         prep: Preprocessor, pred_info: PredictAnalyzer, sel_result: Dict[str, object]):
                        #  pred_info: PredictAnalyzer, df_predict: pd.DataFrame):
    """ 테스트셋 분석 결과 저장 """
    is_save = False
    try:
        if page_info['model_type'] == 'Linear Regression':
            lr = LinearRegressionResult(page_dir, sel_result)
            is_save = lr.save_model_predict_result(pred_info)
        elif page_info['model_type'] == 'Logistic Regression':
            lr = LogisticRegressionResult(page_dir, sel_result, prep)
            is_save = lr.save_model_predict_result(pred_info)
        # pred_info.page_dir = page_dir
        # page_info.update(pred_info.analyze())
        # page_info['predict_result'] = df_predict.rename(
        #     columns={
        #         'y': 'Y',
        #         'y_pred': 'Y^',
        #         'y_proba': 'Y Prob',
        #         'y_proba_max': 'Y Prob Max'
        #     }).map(convert_number_expression).to_dict('records')
        # is_save = dict_to_json(page_info, page_info_path)
    except Exception as e:
        print(e)
    return is_save
