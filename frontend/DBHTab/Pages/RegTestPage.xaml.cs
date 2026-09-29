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
    /// RegTestPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegTestPage : ModernWpf.Controls.Page
    {
        #region Field Variables
        #endregion

        #region Initialize

        public RegTestPage(string pageDir)
        {
            InitializeComponent();
            LoadTestInfo(pageDir);
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
        private void LoadTestInfo(string folderPath)
        {
            string infoPath = Path.Combine(folderPath, "Info.json");
            if (!File.Exists(infoPath)) return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            // 성능 지표 → DataGrid
            var perf = jObj["model_performance"]?.ToObject<Dictionary<string, object>>();

            if (perf != null)
            {
                var table = new DataTable();
                table.Columns.Add("Metric");
                table.Columns.Add("Value");

                foreach (var kv in perf)
                {
                    table.Rows.Add(kv.Key, kv.Value);
                }
                testPerformanceGrid.ItemsSource = table.DefaultView;
            }

            // 테스트 결과 → DataGrid
            var coefList = jObj["predict_result"]?.ToObject<List<Dictionary<string, object>>>();
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
                testResultGrid.ItemsSource = table.DefaultView;
            }

            // 차트 로드
            var plotInfo = jObj["plot_info"] as JObject;
            grdTestPlot.Children.Clear();
            grdTestPlot.ColumnDefinitions.Clear();
            // Regression plots
            bool hasRegressionPlots =
                plotInfo.ContainsKey("predict_scatter_img") &&
                plotInfo.ContainsKey("predict_box_img") &&
                plotInfo.ContainsKey("predict_order_img");
            if (hasRegressionPlots)
            {
                grdTestPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdTestPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdTestPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                var imgPath = plotInfo["predict_scatter_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치(산점도)";
                    control.ChartPath = "predict_scatter.png";
                    control.ChartImage = new BitmapImage(new Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 0);
                    grdTestPlot.Children.Add(control);
                }

                imgPath = plotInfo["predict_box_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치(Box Plot)";
                    control.ChartPath = "predict_box.png";
                    control.ChartImage = new BitmapImage(new Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 1);
                    grdTestPlot.Children.Add(control);
                }

                imgPath = plotInfo["predict_order_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "관측치 대 적합치";
                    control.ChartPath = "predict_order.png";
                    control.ChartImage = new BitmapImage(new Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 2);
                    grdTestPlot.Children.Add(control);
                }
            }
            else
            {
                grdTestPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
                grdTestPlot.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });

                var imgPath = plotInfo["confusion_matrix_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "혼동 행렬";
                    control.ChartPath = "confusion_matrix.png";
                    control.ChartImage = new BitmapImage(new Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 0);
                    grdTestPlot.Children.Add(control);
                }

                imgPath = plotInfo["roc_curve_img"]?.ToString();
                if (imgPath != null)
                {
                    var control = new usSingleChartViewer();
                    control.ChartName = "AUC-ROC Curve";
                    control.ChartPath = "roc_curve.png";
                    control.ChartImage = new BitmapImage(new Uri(imgPath));
                    Grid.SetRow(control, 0);
                    Grid.SetColumn(control, 1);
                    grdTestPlot.Children.Add(control);
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
