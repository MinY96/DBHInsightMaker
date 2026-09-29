using DBHTab.UserControls;
using Newtonsoft.Json;
using System.IO;

namespace DBHTab.Pages
{
    public class ResidualChartInfo
    {
        public string name { get; set; }
        public string path { get; set; }
        public string explanation { get; set; }
        public string insight { get; set; }
        public string check { get; set; }
    }
    /// <summary>
    /// RegResidualPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegResidualPage : ModernWpf.Controls.Page
    {
        #region Field Variables

        private List<ResidualChartInfo> residualCharts;

        #endregion

        #region Initialize

        public RegResidualPage(string pageDir)
        {
            InitializeComponent();
            LoadResidualInfo(pageDir);
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
        private void LoadResidualInfo(string folderPath)
        {
            string infoPath = Path.Combine(folderPath, "Info.json");
            if (!File.Exists(infoPath)) return;

            string json = File.ReadAllText(infoPath);
            residualCharts = JsonConvert.DeserializeObject<List<ResidualChartInfo>>(json);

            //ResidualGrid.ItemsSource = residualCharts;

            //// 첫 번째 차트를 기본 선택
            //if (residualCharts.Count > 0)
            //{
            //    ResidualGrid.SelectedIndex = 0;
            //    ShowImage(residualCharts[0].path);
            //}
            foreach (ResidualChartInfo item in residualCharts)
            {
                ucExplainChartViewer control = null;
                string chartName = string.Empty;
                if (item.name == "Residual vs Fitted")
                {
                    control = cvFitted;
                    chartName = "Residual_Fitted.png";
                }
                else if (item.name == "Residual vs Order")
                {
                    control = cvOrder;
                    chartName = "Residual_Order.png";
                }
                else if (item.name == "Histogram of Residual")
                {
                    control = cvHist;
                    chartName = "Residual_Histogram.png";
                }
                else if (item.name == "Q-Q Plot of Residual")
                {
                    control = cvQq;
                    chartName = "Residual_QQ_Plot.png";
                }
                else if (item.name == "Scale-Location")
                {
                    control = cvScale;
                    chartName = "Scale_Location.png";
                }
                else if (item.name == "Cook’s Distance vs Order")
                {
                    control = cvCooks;
                    chartName = "CooksD_Order.png";
                }
                else if (item.name == "Leverage vs Cook’s Distance")
                {
                    control = cvLeverage;
                    chartName = "Leverage_CooksD.png";
                }
                control.ChartName = item.name;
                control.ChartPath = chartName;
                control.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(item.path));
                control.Explain = item.explanation;
                control.Insight = item.insight;
                control.CheckPoint = item.check;
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
