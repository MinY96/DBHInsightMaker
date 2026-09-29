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
    public class RegLinearTestPageModel : ViewModelBase
    {
        #region Field Variables

        private LinearRegModelInfo? _lineraModelInfo;
        private LinearRegModelInfo? _testResult;
        private DataView? _coefTable;
        private DataView? _regTable;
        private BitmapImage? _predictOrderImg;
        private BitmapImage? _predictBoxImg;
        private BitmapImage? _predictScatterImg;

        #endregion

        #region Initialize

        public RegLinearTestPageModel(string pageDir)
        {
            LoadLinearModelInfo(pageDir);
        }

        #endregion

        #region Properties

        public LinearRegModelInfo? LinearModelInfo
        {
            get { return _lineraModelInfo; }
            set { _lineraModelInfo = value; OnPropertyChanged(); }
        }

        public LinearRegModelInfo? TestResult
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

        public BitmapImage? PredictOrderImg
        {
            get { return _predictOrderImg; }
            set { _predictOrderImg = value; OnPropertyChanged(); }
        }

        public BitmapImage? PredictBoxImg
        {
            get { return _predictBoxImg; }
            set { _predictBoxImg = value; OnPropertyChanged(); }
        }

        public BitmapImage? PredictScatterImg
        {
            get { return _predictScatterImg; }
            set { _predictScatterImg = value; OnPropertyChanged(); }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods

        private void LoadLinearModelInfo(string pageDir)
        {
            string infoPath = Path.Combine(pageDir, "Info.json");
            if (!File.Exists(infoPath))
                return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            LinearRegModelInfo linearModelInfo = new LinearRegModelInfo();

            // Model Info
            var modelInfo = jObj["model_info"] as JObject;
            ParseAndAssignValue(modelInfo, "model_type", linearModelInfo, "ModelType", typeof(string));
            ParseAndAssignValue(modelInfo, "equation", linearModelInfo, "RegEquation", typeof(string));
            ParseAndAssignValue(modelInfo, "n", linearModelInfo, "DataSize", typeof(int));
            ParseAndAssignValue(modelInfo, "k", linearModelInfo, "IndepValCount", typeof(int));
            ParseAndAssignValue(modelInfo, "f-statistic", linearModelInfo, "Statistic", typeof(double));
            ParseAndAssignValue(modelInfo, "p-value", linearModelInfo, "PValue", typeof(double));
            ParseAndAssignValue(modelInfo, "r2", linearModelInfo, "RSquare", typeof(double));
            ParseAndAssignValue(modelInfo, "r2_adj", linearModelInfo, "RSquareAdj", typeof(double));
            ParseAndAssignValue(modelInfo, "llf", linearModelInfo, "LLF", typeof(double));
            ParseAndAssignValue(modelInfo, "aic", linearModelInfo, "AIC", typeof(double));
            ParseAndAssignValue(modelInfo, "bic", linearModelInfo, "BIC", typeof(double));

            LinearModelInfo = linearModelInfo;

            LinearRegModelInfo testResult = new LinearRegModelInfo();

            // Model Fit Metrics
            var testSetInfo = jObj["test_set"] as JObject;
            ParseAndAssignValue(testSetInfo, "test_ratio", testResult, "DataRatio", typeof(double));
            ParseAndAssignValue(testSetInfo, "test_size", testResult, "DataSize", typeof(int));            

            // Test Performance Metrics
            var performMetrics = jObj["test_performance_metrics"] as JObject;
            ParseAndAssignValue(performMetrics, "sst", testResult, "SST", typeof(double));
            ParseAndAssignValue(performMetrics, "ssr", testResult, "SSR", typeof(double));
            ParseAndAssignValue(performMetrics, "sse", testResult, "SSE", typeof(double));
            ParseAndAssignValue(performMetrics, "r2", testResult, "RSquare", typeof(double));
            ParseAndAssignValue(performMetrics, "r2_adj", testResult, "RSquareAdj", typeof(double));
            ParseAndAssignValue(performMetrics, "mae", testResult, "MAE", typeof(double));
            ParseAndAssignValue(performMetrics, "mse", testResult, "MSE", typeof(double));
            ParseAndAssignValue(performMetrics, "rmse", testResult, "RMSE", typeof(double));
            ParseAndAssignValue(performMetrics, "mape", testResult, "MAPE", typeof(double));
            ParseAndAssignValue(performMetrics, "mpe", testResult, "MPE", typeof(double));

            TestResult = testResult;

            // DataTable
            ParseAsDataTableAssignValue(jObj, "coef_table", "CoefTable");
            ParseAsDataTableAssignValue(jObj, "reg_table", "RegTable");

            // Plot Info
            var plotInfo = jObj["plot_info"] as JObject;
            ParseAndAssignValue(plotInfo, "predict_order_img", "PredictOrderImg", typeof(string));
            ParseAndAssignValue(plotInfo, "predict_box_img", "PredictBoxImg", typeof(string));
            ParseAndAssignValue(plotInfo, "predict_scatter_img", "PredictScatterImg", typeof(string));
            ParseAndAssignValue(plotInfo, "regression_by_indep_var_img", "RegByIndepImg", typeof(string));
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
