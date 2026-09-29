using DBHTab.Models;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;

namespace DBHTab.ViewModels
{
    public class RegLogisticTestPageModel : ViewModelBase
    {
        #region Field Variables

        private LogisticRegModelInfo? _logisticModelInfo;
        private LogisticRegModelInfo? _testResult;
        private DataView? _coefTable;
        private DataView? _regTable;
        private BitmapImage? _rocCurveImg;
        private BitmapImage? _prCurveImg;
        private BitmapImage? _rocCMImg;
        private BitmapImage? _prCMImg;

        #endregion

        #region Initialize

        public RegLogisticTestPageModel(string pageDir)
        {
            LoadLogisticModelInfo(pageDir);
        }

        #endregion

        #region Properties

        public LogisticRegModelInfo? LogisticModelInfo
        {
            get { return _logisticModelInfo; }
            set { _logisticModelInfo = value; OnPropertyChanged(); }
        }

        public LogisticRegModelInfo? TestResult
        {
            get { return _testResult; }
            set { _testResult = value; OnPropertyChanged(); }
        }

        public DataView? CoefTable
        {
            get { return _coefTable; }
            set { _coefTable = value; OnPropertyChanged(); }
        }

        public DataView? RegTable
        {
            get { return _regTable; }
            set { _regTable = value; OnPropertyChanged(); }
        }

        public BitmapImage? ROCCurveImg
        {
            get { return _rocCurveImg; }
            set { _rocCurveImg = value; OnPropertyChanged(); }
        }

        public BitmapImage? PRCurveImg
        {
            get { return _prCurveImg; }
            set { _prCurveImg = value; OnPropertyChanged(); }
        }

        public BitmapImage? ROCConfusionMatrixImg
        {
            get { return _rocCMImg; }
            set { _rocCMImg = value; OnPropertyChanged(); }
        }

        public BitmapImage? PRConfusionMatrixImg
        {
            get { return _prCMImg; }
            set { _prCMImg = value; OnPropertyChanged(); }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods

        private void LoadLogisticModelInfo(string pageDir)
        {
            string infoPath = Path.Combine(pageDir, "Info.json");
            if (!File.Exists(infoPath))
                return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            LogisticRegModelInfo logisticModelInfo = new LogisticRegModelInfo();

            // Model Info
            var modelInfo = jObj["model_info"] as JObject;
            ParseAndAssignValue(modelInfo, "model_type", logisticModelInfo, "ModelType", typeof(string));
            ParseAndAssignValue(modelInfo, "equation", logisticModelInfo, "RegEquation", typeof(string));
            ParseAndAssignValue(modelInfo, "n", logisticModelInfo, "DataSize", typeof(int));
            ParseAndAssignValue(modelInfo, "k", logisticModelInfo, "IndepValCount", typeof(int));
            ParseAndAssignValue(modelInfo, "llr-statistic", logisticModelInfo, "Statistic", typeof(double));
            ParseAndAssignValue(modelInfo, "p-value", logisticModelInfo, "PValue", typeof(double));
            ParseAndAssignValue(modelInfo, "llf", logisticModelInfo, "LLF", typeof(double));
            ParseAndAssignValue(modelInfo, "aic", logisticModelInfo, "AIC", typeof(double));
            ParseAndAssignValue(modelInfo, "bic", logisticModelInfo, "BIC", typeof(double));

            LogisticModelInfo = logisticModelInfo;

            LogisticRegModelInfo testResult = new LogisticRegModelInfo();

            // Model Fit Metrics
            var testSetInfo = jObj["test_set"] as JObject;
            ParseAndAssignValue(testSetInfo, "test_ratio", testResult, "DataRatio", typeof(double));
            ParseAndAssignValue(testSetInfo, "test_size", testResult, "DataSize", typeof(int));

            // Test Performance Metrics
            var performMetrics = jObj["performance_metrics"] as JObject;
            var rocInfo = performMetrics["roc"] as JObject;
            testResult.ROCMetrics = ParseAsClassificationMetrics(rocInfo);
            var prInfo = performMetrics["pr"] as JObject;
            testResult.PRMetrics = ParseAsClassificationMetrics(prInfo);

            TestResult = testResult;

            // DataTable
            ParseAsDataTableAssignValue(jObj, "coef_table", "CoefTable");
            ParseAsDataTableAssignValue(jObj, "reg_table", "RegTable");

            // Plot Info
            ParseAndAssignValue(rocInfo, "roc_curve_img", "ROCCurveImg", typeof(string));
            ParseAndAssignValue(rocInfo, "roc_confusion_matrix_img", "ROCConfusionMatrixImg", typeof(string));
            ParseAndAssignValue(prInfo, "pr_curve_img", "PRCurveImg", typeof(string));
            ParseAndAssignValue(prInfo, "pr_confusion_matrix_img", "PRConfusionMatrixImg", typeof(string));
        }

        private ClassificationMetrics ParseAsClassificationMetrics(JObject clfInfo)
        {
            var mtricsInfo = clfInfo["metrics"] as JObject;
            ClassificationMetrics result = new ClassificationMetrics();
            ParseAndAssignValue(clfInfo, "threshold", result, "Threshold", typeof(double));
            ParseAndAssignValue(clfInfo, "auc", result, "AUC", typeof(double));
            ParseAndAssignValue(mtricsInfo, "tn", result, "TN", typeof(int));
            ParseAndAssignValue(mtricsInfo, "tp", result, "TP", typeof(int));
            ParseAndAssignValue(mtricsInfo, "fn", result, "FN", typeof(int));
            ParseAndAssignValue(mtricsInfo, "fp", result, "FP", typeof(int));
            ParseAndAssignValue(mtricsInfo, "accuracy", result, "Accuracy", typeof(double));
            ParseAndAssignValue(mtricsInfo, "recall", result, "Recall", typeof(double));
            ParseAndAssignValue(mtricsInfo, "precision", result, "Precision", typeof(double));
            ParseAndAssignValue(mtricsInfo, "specificity", result, "Specificity", typeof(double));
            ParseAndAssignValue(mtricsInfo, "fpr", result, "FPR", typeof(double));
            ParseAndAssignValue(mtricsInfo, "npv", result, "NPV", typeof(double));
            ParseAndAssignValue(mtricsInfo, "f1_score", result, "F1Score", typeof(double));
            return result;
        }

        private void ParseAsDataTableAssignValue(JObject pageInfo, string key, string propertyName)
        {
            if (pageInfo == null)
                return;

            if (pageInfo.TryGetValue(key, out JToken value))
            {
                var tableList = value.ToObject<List<Dictionary<string, object>>>();
                if (tableList != null && tableList.Count > 0)
                {
                    var table = new DataTable();
                    foreach (var column in tableList[0].Keys)
                        table.Columns.Add(column);

                    foreach (var coef in tableList)
                    {
                        var dr = table.NewRow();
                        foreach (var kv in coef)
                        {
                            if (kv.Value is double doublevalue)
                            {
                                dr[kv.Key] = doublevalue.ToString("N4");
                            }
                            else if (kv.Value is int intValue)
                            {
                                dr[kv.Key] = intValue.ToString("N0"); // N0 포맷 적용
                            }
                            else
                            {
                                dr[kv.Key] = kv.Value ?? "";
                            }
                        }
                        table.Rows.Add(dr);
                    }

                    var propertyInfo = this.GetType().GetProperty(propertyName);
                    if (propertyInfo != null && propertyInfo.CanWrite)
                    {
                        propertyInfo.SetValue(this, table.DefaultView);
                    }
                }
            }
        }

        private void ParseAndAssignValue(JObject pageInfo, string key, string propertyName, Type targetType)
        {
            if (pageInfo == null)
                return;

            if (pageInfo.TryGetValue(key, out JToken value))
            {
                object parsedValue = null;
                if (value.Type == JTokenType.Null)
                {
                    parsedValue = null;
                }
                else
                {
                    if (targetType == typeof(int))
                        parsedValue = value.ToObject<int>();
                    else if (targetType == typeof(double))
                        parsedValue = value.ToObject<double>();
                    else if (targetType == typeof(string))
                        parsedValue = value.ToObject<string>();
                    else
                        throw new ArgumentException("Unsupported target type");

                }
                var propertyInfo = this.GetType().GetProperty(propertyName);
                if (propertyInfo != null && propertyInfo.CanWrite)
                {
                    if (propertyInfo.PropertyType == typeof(BitmapImage))
                    {
                        parsedValue = new BitmapImage(new Uri((string)parsedValue));
                    }
                    propertyInfo.SetValue(this, parsedValue);
                }
            }
        }

        private void ParseAndAssignValue(JObject pageInfo, string key, object targetClass, string propertyName, Type targetType)
        {
            if (pageInfo == null)
                return;

            if (pageInfo.TryGetValue(key, out JToken value))
            {
                object parsedValue = null;
                if (value.Type == JTokenType.Null)
                {
                    parsedValue = null;
                }
                else
                {
                    if (targetType == typeof(int))
                        parsedValue = value.ToObject<int>();
                    else if (targetType == typeof(double))
                        parsedValue = value.ToObject<double>();
                    else if (targetType == typeof(string))
                        parsedValue = value.ToObject<string>();
                    else
                        throw new ArgumentException("Unsupported target type");

                }
                var propertyInfo = targetClass.GetType().GetProperty(propertyName);
                if (propertyInfo != null && propertyInfo.CanWrite)
                {
                    propertyInfo.SetValue(targetClass, parsedValue);
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
