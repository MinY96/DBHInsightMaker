using DBHTab.UserControls;
using Newtonsoft.Json.Linq;
using System.Data;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;

namespace DBHTab.Pages
{
    /// <summary>
    /// RegModelPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegModelPage : ModernWpf.Controls.Page
    {
        #region Field Variables
        #endregion

        #region Initialize

        public RegModelPage(string pageDir)
        {
            InitializeComponent();
            LoadModelInfo(pageDir);
        }

        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        private void LoadModelInfo(string folderPath)
        {
            string infoPath = Path.Combine(folderPath, "Info.json");
            if (!File.Exists(infoPath)) return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            // 모델 타입 & 회귀식
            ModelTypeText.Text = $"회귀 모델 타입: {jObj["model_type"]}";
            EquationText.Text = $"회귀식: {jObj["equation"]}";

            // 성능 지표 → DataGrid
            var perf = jObj["model_performance"]?.ToObject<Dictionary<string, object>>();
            //var nameDic = jObj["name_dic"]?.ToObject<Dictionary<string, string>>();

            if (perf != null)
            {
                var table = new DataTable();
                table.Columns.Add("Metric");
                table.Columns.Add("Value");

                foreach (var kv in perf)
                {
                    table.Rows.Add(kv.Key, kv.Value);
                }
                PerformanceGrid.ItemsSource = table.DefaultView;
            }

            // 계수 상세 → DataGrid
            var coefList = jObj["coeff_info"]?.ToObject<List<Dictionary<string, object>>>();
            if (coefList != null && coefList.Count > 0)
            {
                var table = new DataTable();
                foreach (var key in coefList[0].Keys)
                    table.Columns.Add(key);

                foreach (var coef in coefList)
                {
                    var dr = table.NewRow();
                    foreach (var kv in coef)
                        dr[kv.Key] = kv.Value ?? "";
                    table.Rows.Add(dr);
                }
                CoefGrid.ItemsSource = table.DefaultView;
            }

            var plotInfo = jObj["plot_info"] as JObject;
            grdPlot.Children.Clear();
            grdPlot.ColumnDefinitions.Clear();
            // Regression plots
            bool hasRegressionPlots =
                plotInfo.ContainsKey("predict_scatter_img") &&
                plotInfo.ContainsKey("predict_box_img") &&
                plotInfo.ContainsKey("predict_order_img");
            if (hasRegressionPlots)
            {
                grdPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                var imgPath = plotInfo["predict_scatter_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치(산점도)";
                    control.ChartPath = "predict_scatter.png";
                    control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 0);
                    grdPlot.Children.Add(control);
                }

                imgPath = plotInfo["predict_box_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치(Box Plot)";
                    control.ChartPath = "predict_box.png";
                    control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 1);
                    grdPlot.Children.Add(control);
                }

                imgPath = plotInfo["predict_order_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치";
                    control.ChartPath = "predict_order.png";
                    control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 2);
                    grdPlot.Children.Add(control);
                }
            }
            else
            {
                grdPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });

                var imgPath = plotInfo["confusion_matrix_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "혼동 행렬";
                    control.ChartPath = "confusion_matrix.png";
                    control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 0);
                    grdPlot.Children.Add(control);
                }

                imgPath = plotInfo["roc_curve_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "AUC-ROC Curve";
                    control.ChartPath = "roc_curve.png";
                    control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 1);
                    grdPlot.Children.Add(control);
                }
            }
            //if (plotInfo != null)
            //{
            //    // 회귀용 차트
            //    if (plotInfo["predict_scatter_img"] != null)
            //    {
            //        LoadImage(plotInfo["predict_scatter_img"].ToString(), ScatterImage);
            //        ScatterTab.Visibility = Visibility.Visible;
            //    }
            //    if (plotInfo["predict_box_img"] != null)
            //    {
            //        LoadImage(plotInfo["predict_box_img"].ToString(), BoxImage);
            //        BoxTab.Visibility = Visibility.Visible;
            //    }
            //    if (plotInfo["predict_order_img"] != null)
            //    {
            //        LoadImage(plotInfo["predict_order_img"].ToString(), OrderImage);
            //        OrderTab.Visibility = Visibility.Visible;
            //    }

            //    // 분류용 차트
            //    if (plotInfo["confusion_matrix_img"] != null)
            //    {
            //        LoadImage(plotInfo["confusion_matrix_img"].ToString(), ConfusionImage);
            //        ConfusionTab.Visibility = Visibility.Visible;
            //    }
            //    if (plotInfo["roc_curve_img"] != null)
            //    {
            //        LoadImage(plotInfo["roc_curve_img"].ToString(), RocImage);
            //        RocTab.Visibility = Visibility.Visible;
            //    }
            //}
        }

        private void LoadImage(string path, Image control)
        {
            if (!string.IsNullOrEmpty(path) && File.Exists(path))
            {
                control.Source = new BitmapImage(new System.Uri(path));
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
