# pylint: disable=W0718, E1101, C0413, C0103, C0321, C0301
"""
회귀 분석 모델 정보
"""

from typing import Dict
import os
import numpy as np
import pandas as pd
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             root_mean_squared_error, mean_absolute_percentage_error,
                             roc_curve, precision_recall_curve, auc, confusion_matrix)
from eda_manager.analyze.data_analyze import Preprocessor, PredictAnalyzer
from eda_manager.analyze.data_analyze.chart_creator import (plot_roc_curve, plot_pr_curve, plot_confusion_matrix,
                                                            plot_predict_scatter, plot_predict_box, plot_predict_order,
                                                            plot_reg_result_by_indep_var)
from helper import dict_to_json

class RegressionResult:
    """ 회귀 분석 결과 클래스
    """
    def __init__(self):
        self.n = 0 # 표본 크기
        self.k = 0 # 독립변수 개수
        self.equation = None
        self.model = None
        self.model_type = None
        self.y = None
        self.y_pred = None
        self.llf = None
        self.aic = None
        self.bic = None
        self.statistic = None
        self.p_value = None

class LinearRegressionResult(RegressionResult):
    """ 선형 회귀 분석 결과 클래스
    """
    def __init__(self, page_dir: str, reg_info: Dict[str, object]):
        super().__init__()
        self.model_type = 'Linear Regression(선형 회귀)'
        self.page_dir = page_dir
        self.n = reg_info['model_info']['n']
        self.k = reg_info['model_info']['k']
        self.indep_vars = reg_info['variables']
        self.statistic = reg_info['model_info']['statistic']
        self.p_value = reg_info['model_info']['p_value']
        self.X = reg_info['x']
        self.y = reg_info['y']
        self.y_pred = reg_info['y_pred']
        self.equation = f"{reg_info['dep_var']} = " + ' + '.join([f"[{row['Coef']:.2f}]*"+unit
                                             for unit, row in
                                             reg_info['coef_table'].iterrows()])
        self.llf = reg_info['metrics']['llf']
        self.aic = reg_info['metrics']['aic']
        self.bic = reg_info['metrics']['bic']
        self.coef_table = reg_info['coef_table'].reset_index(names='Coef Name').to_dict('records')
        self.sst = 0
        self.ssr = 0
        self.sse = 0
        self.r2 = 0
        self.r2_adj = 0
        self.mae = 0
        self.mse = 0
        self.rmse = 0
        self.mape = 0
        self.mpe = 0

    def _update_metrics(self):
        self.sst = float(np.sum((self.y-np.mean(self.y))**2))
        self.sse = float(np.sum((self.y-self.y_pred)**2))
        self.ssr = self.sst - self.sse

        self.r2 = self.ssr / self.sst
        self.r2_adj = 1 - (1-self.r2)*(len(self.y)-1)/(len(self.y)-self.k-1)
        self.mae = float(mean_absolute_error(self.y, self.y_pred))
        self.mse = float(mean_squared_error(self.y, self.y_pred))
        self.rmse = float(root_mean_squared_error(self.y, self.y_pred))
        self.mape = float(mean_absolute_percentage_error(self.y, self.y_pred))
        self.mpe = float(np.mean((self.y-self.y_pred)/self.y))

    def save_model_result(self):
        """모델 결과 저장 메소드"""
        self._update_metrics()
        df_linear = pd.concat([self.y, self.y_pred], axis=1).reset_index(drop=True)
        df_linear['residual'] = df_linear['y']-df_linear['y_pred']
        df_linear = df_linear.rename(columns={
            'y': '실제값(y)',
            'y_pred': '예측값(y^)',
            'residual': '잔차(y-y^)'
        })
        plot_info = {}
        pred_sactter_plot_path = os.path.join(self.page_dir, 'predict_scatter.png')
        pred_box_plot_path = os.path.join(self.page_dir, 'predict_box.png')
        pred_plot_path = os.path.join(self.page_dir, 'predict_order.png')
        reg_by_indep_plot_path = os.path.join(self.page_dir, 'regression_by_indep_vars.png')
        if plot_predict_scatter(self.y, self.y_pred, pred_sactter_plot_path):
            plot_info['predict_scatter_img'] = pred_sactter_plot_path
        if plot_predict_box(self.y, self.y_pred, pred_box_plot_path):
            plot_info['predict_box_img'] = pred_box_plot_path
        if plot_predict_order(self.y, self.y_pred, pred_plot_path):
            plot_info['predict_order_img'] = pred_plot_path
        if plot_reg_result_by_indep_var(self.X, self.y, self.indep_vars, self.coef_table, reg_by_indep_plot_path):
            plot_info['regression_by_indep_var_img'] = reg_by_indep_plot_path
        info = {
            'model_info': {
                'model_type': self.model_type,
                'equation': self.equation,
                'n': self.n,
                'k': self.k
            },
            'model_fit_metrics': {
                'sst': self.sst,
                'ssr': self.ssr,
                'sse': self.sse,
                'r2': self.r2,
                'r2_adj': self.r2_adj,
                'f-statistic': self.statistic,
                'p-value': self.p_value
            },
            'inform_criteria': {
                'llf': self.llf,
                'aic': self.aic,
                'bic': self.bic
            },
            'performance_metrics': {
                'mae': self.mae,
                'mse': self.mse,
                'rmse': self.rmse,
                'mape': self.mape,
                'mpe': self.mpe
            },
            'coef_table': self.coef_table,
            'reg_table': df_linear.to_dict('records'),
            'plot_info': plot_info
        }
        info_path = os.path.join(self.page_dir, 'info.json')
        is_save = dict_to_json(info, info_path)
        return is_save

    def save_model_predict_result(self, pred_info: PredictAnalyzer):
        """모델 테스트 결과 저장 메소드"""
        self._update_metrics()
        model_info = {
            'model_type': self.model_type,
            'equation': self.equation,
            'n': self.n,
            'k': self.k,
            'f-statistic': self.statistic,
            'p-value': self.p_value,
            'r2': self.r2,
            'r2_adj': self.r2_adj,
            'llf': self.llf,
            'aic': self.aic,
            'bic': self.bic
        }
        self.y, self.y_pred = pd.Series(pred_info.y, name='y'), pd.Series(pred_info.y_pred, name='y_pred')
        self._update_metrics()
        df_linear = pd.concat([self.y, self.y_pred], axis=1).reset_index(drop=True)
        df_linear['residual'] = df_linear['y']-df_linear['y_pred']
        df_linear = df_linear.rename(columns={
            'y': '실제값(y)',
            'y_pred': '예측값(y^)',
            'residual': '잔차(y-y^)'
        })
        plot_info = {}
        pred_sactter_plot_path = os.path.join(self.page_dir, 'predict_scatter.png')
        pred_box_plot_path = os.path.join(self.page_dir, 'predict_box.png')
        pred_plot_path = os.path.join(self.page_dir, 'predict_order.png')
        if plot_predict_scatter(self.y, self.y_pred, pred_sactter_plot_path):
            plot_info['predict_scatter_img'] = pred_sactter_plot_path
        if plot_predict_box(self.y, self.y_pred, pred_box_plot_path):
            plot_info['predict_box_img'] = pred_box_plot_path
        if plot_predict_order(self.y, self.y_pred, pred_plot_path):
            plot_info['predict_order_img'] = pred_plot_path
        info = {
            'model_info': model_info,
            'test_set': {
                'test_ratio': pred_info.test_ratio,
                'test_size': pred_info.test_size
            },
            'test_performance_metrics': {
                'sst': self.sst,
                'ssr': self.ssr,
                'sse': self.sse,
                'r2': self.r2,
                'r2_adj': self.r2_adj,
                'mae': self.mae,
                'mse': self.mse,
                'rmse': self.rmse,
                'mape': self.mape,
                'mpe': self.mpe
            },
            'reg_table': df_linear.to_dict('records'),
            'plot_info': plot_info
        }
        info_path = os.path.join(self.page_dir, 'info.json')
        is_save = dict_to_json(info, info_path)
        return is_save

class LogisticRegressionResult(RegressionResult):
    """ 로지스틱 회귀 분석 결과 클래스
    """
    def __init__(self, page_dir: str, reg_info: Dict[str, object], prep: Preprocessor):
        super().__init__()
        self.model_type = 'Logistic Regression(로지스틱 회귀)'
        self.prep = prep
        self.page_dir = page_dir
        self.n = reg_info['model_info']['n']
        self.k = reg_info['model_info']['k']
        self.indep_vars = reg_info['variables']
        self.statistic = reg_info['model_info']['statistic']
        self.p_value = reg_info['model_info']['p_value']
        self.X = reg_info['x']
        self.y = reg_info['y']
        self.y_proba = reg_info['y_proba']
        self.pos_label = int(self.y.unique().max())
        try:
            self.equation = f"{reg_info['dep_var']} = " + ' + '.join([f"[{row['Coef']:.2f}]*"+unit
                                             for unit, row in
                                             reg_info['coef_table'].iterrows()])
            self.coef_table = reg_info['coef_table']\
                .reset_index(names='Coef Name').to_dict('records')
        except Exception as e:
            print(e)
            self.equation = reg_info['equation']
            self.coef_table = reg_info['coef_table']
        self.llf = reg_info['metrics']['llf']
        self.aic = reg_info['metrics']['aic']
        self.bic = reg_info['metrics']['bic']
        self.clf_metrics = {}

    def _update_metrics(self):
        self.clf_metrics['roc'] = self.update_roc_curve_metrics()
        self.clf_metrics['pr'] = self.update_pr_curve_metrics()

    def update_roc_curve_metrics(self):
        """ ROC Curve 기준 평가 지표 """
        fpr, tpr, thresholds = roc_curve(self.y, self.y_proba, pos_label=self.pos_label)
        roc_auc = auc(fpr, tpr)
        distances = np.sqrt((1-tpr)**2 + (fpr)**2)
        optimal_idx = np.argmin(distances)

        opt_thr = thresholds[optimal_idx]
        opt_fpr, opt_tpr = fpr[optimal_idx], tpr[optimal_idx]
        y_pred = (self.y_proba >= opt_thr).astype(int)
        y_pred.name = 'y_pred_roc'
        clf_info = {
            'threshold': opt_thr,
            'y_pred': y_pred,
            'auc': roc_auc,
            'metrics': self.update_clf_metrics(self.y, y_pred)
        }
        roc_curve_plot_path = os.path.join(self.page_dir, 'roc_curve.png')
        confusion_matrix_plot_path = os.path.join(self.page_dir, 'roc_confusion_matrix.png')
        if plot_roc_curve(fpr, tpr, roc_auc, self.pos_label, opt_fpr, opt_tpr, opt_thr, roc_curve_plot_path):
            clf_info['roc_curve_img'] = roc_curve_plot_path
        class_names = None
        if self.prep.y_was_encoded:
            class_names = list(map(str, np.unique(self.prep.inverse_transform_y(self.y))))
        if plot_confusion_matrix(self.y, y_pred, class_names, confusion_matrix_plot_path):
            clf_info['roc_confusion_matrix_img'] = confusion_matrix_plot_path
        return clf_info

    def update_pr_curve_metrics(self):
        """PR Curve 기준 성능 지표"""
        precisions, recalls, thresholds = precision_recall_curve(self.y, self.y_proba, pos_label=self.pos_label)
        pr_auc = auc(recalls, precisions)
        f1_scores = 2*precisions*recalls/(precisions+recalls)
        optimal_idx = np.argmax(f1_scores)
        opt_thr = thresholds[optimal_idx]
        opt_precision, opt_recall = precisions[optimal_idx], recalls[optimal_idx]
        opt_f1_score = f1_scores[optimal_idx]
        y_pred = (self.y_proba >= opt_thr).astype(int)
        y_pred.name = 'y_pred_pr'
        clf_info = {
            'threshold': opt_thr,
            'y_pred': y_pred,
            'auc': pr_auc,
            'metrics': self.update_clf_metrics(self.y, y_pred)
        }
        pr_curve_plot_path = os.path.join(self.page_dir, 'pr_curve.png')
        confusion_matrix_plot_path = os.path.join(self.page_dir, 'pr_confusion_matrix.png')
        if plot_pr_curve(precisions, recalls, f1_scores, pr_auc,
                         self.pos_label, opt_recall, opt_precision,
                         opt_f1_score, opt_thr, pr_curve_plot_path):
            clf_info['pr_curve_img'] = pr_curve_plot_path
        class_names = None
        if self.prep.y_was_encoded:
            class_names = list(map(str, np.unique(self.prep.inverse_transform_y(self.y))))
        if plot_confusion_matrix(self.y, y_pred, class_names, confusion_matrix_plot_path):
            clf_info['pr_confusion_matrix_img'] = confusion_matrix_plot_path
        return clf_info

    def update_clf_metrics(self, y: pd.Series, y_pred: pd.Series):
        """ 분류 모델 평가지표 """
        tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel().tolist()
        accuracy = (tp+tn)/(tp+tn+fp+fn) if (tp+tn+fp+fn) > 0 else None
        recall = tp/(tp+fn) if (tp+fn) > 0 else None
        precision = tp/(tp+fp) if (tp+fp) > 0 else None
        specificity = tn/(tn+fp) if (tn+fp) > 0 else None
        fpr = 1 - specificity
        npv = tn/(tn+fn) if (tn+fn) > 0 else None
        f1_score = 2*precision*recall/(precision+recall) if all([recall, precision]) else None
        return {
            'tn': tn,
            'fp': fp,
            'fn': fn,
            'tp': tp,
            'accuracy': accuracy,
            'recall': recall,
            'precision': precision,
            'specificity': specificity,
            'fpr': fpr,
            'npv': npv,
            'f1_score': f1_score
        }

    def save_model_result(self):
        """모델 결과 저장 메소드"""
        self._update_metrics()
        df_logit = pd.concat([self.y,
                              self.y_proba,
                              self.clf_metrics['roc']['y_pred'],
                              self.clf_metrics['pr']['y_pred']], axis=1).reset_index(drop=True)
        if self.prep.y_was_encoded:
            y = pd.Series(self.prep.inverse_transform_y(self.y), index=self.y.index)
            y_pred_roc = pd.Series(self.prep.inverse_transform_y(self.clf_metrics['roc']['y_pred']), index=self.y.index)
            y_pred_pr = pd.Series(self.prep.inverse_transform_y(self.clf_metrics['pr']['y_pred']), index=self.y.index)
            y.name = 'y'
            y_pred_roc.name = 'y_pred_roc'
            y_pred_pr.name = 'y_pred_pr'
        else:
            y = self.y
            y_pred_roc = self.clf_metrics['roc']['y_pred']
            y_pred_pr = self.clf_metrics['pr']['y_pred']
        df_logit = pd.concat([y, self.y_proba, y_pred_roc, y_pred_pr], axis=1).reset_index(drop=True)
        df_logit = df_logit.rename(columns={
            'y': '실제값(y)',
            'y_proba': '예측 확률(0~1)',
            'y_pred_roc': f'예측값(ROC Curve, 기준:{self.clf_metrics['roc']['threshold']:.2f})',
            'y_pred_pr': f'예측값(PR Curve, 기준:{self.clf_metrics['pr']['threshold']:.2f})'
        })
        clf_metrics = {}
        for curve, curve_info in self.clf_metrics.items():
            clf_metrics[curve] = {k:v for k,v in curve_info.items() if k!='y_pred'}
        info = {
            'model_info': {
                'model_type': self.model_type,
                'equation': self.equation,
                'n': self.n,
                'k': self.k
            },
            'model_fit_metrics': {
                'llr-statistic': self.statistic,
                'p-value': self.p_value
            },
            'inform_criteria': {
                'llf': self.llf,
                'aic': self.aic,
                'bic': self.bic
            },
            'performance_metrics': clf_metrics,
            'coef_table': self.coef_table,
            'reg_table': df_logit.to_dict('records'),
        }
        info_path = os.path.join(self.page_dir, 'info.json')
        is_save = dict_to_json(info, info_path)
        return is_save

    def save_model_predict_result(self, pred_info: PredictAnalyzer):
        """모델 테스트 결과 저장 메소드"""
        # self._update_metrics()
        model_info = {
            'model_type': self.model_type,
            'equation': self.equation,
            'n': self.n,
            'k': self.k,
            'llr-statistic': self.statistic,
            'p-value': self.p_value,
            'llf': self.llf,
            'aic': self.aic,
            'bic': self.bic
        }
        self.y, self.y_proba = pd.Series(pred_info.y, name='y'), pd.Series(pred_info.y_prob, name='y_proba')
        self._update_metrics()
        df_logit = pd.concat([self.y,
                              self.y_proba,
                              self.clf_metrics['roc']['y_pred'],
                              self.clf_metrics['pr']['y_pred']], axis=1).reset_index(drop=True)
        if self.prep.y_was_encoded:
            y = pd.Series(self.prep.inverse_transform_y(self.y), index=self.y.index)
            y_pred_roc = pd.Series(self.prep.inverse_transform_y(self.clf_metrics['roc']['y_pred']), index=self.y.index)
            y_pred_pr = pd.Series(self.prep.inverse_transform_y(self.clf_metrics['pr']['y_pred']), index=self.y.index)
            y.name = 'y'
            y_pred_roc.name = 'y_pred_roc'
            y_pred_pr.name = 'y_pred_pr'
        else:
            y = self.y
            y_pred_roc = self.clf_metrics['roc']['y_pred']
            y_pred_pr = self.clf_metrics['pr']['y_pred']
        df_logit = pd.concat([y, self.y_proba, y_pred_roc, y_pred_pr], axis=1).reset_index(drop=True)
        df_logit = df_logit.rename(columns={
            'y': '실제값(y)',
            'y_proba': '예측 확률(0~1)',
            'y_pred_roc': f'예측값(ROC Curve, 기준:{self.clf_metrics['roc']['threshold']:.2f})',
            'y_pred_pr': f'예측값(PR Curve, 기준:{self.clf_metrics['pr']['threshold']:.2f})'
        })
        clf_metrics = {}
        for curve, curve_info in self.clf_metrics.items():
            clf_metrics[curve] = {k:v for k,v in curve_info.items() if k!='y_pred'}
        info = {
            'model_info': model_info,
            'test_set': {
                'test_ratio': pred_info.test_ratio,
                'test_size': pred_info.test_size
            },
            'performance_metrics': clf_metrics,            
            'reg_table': df_logit.to_dict('records'),
        }
        info_path = os.path.join(self.page_dir, 'info.json')
        is_save = dict_to_json(info, info_path)
        return is_save
