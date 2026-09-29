using Newtonsoft.Json.Linq;
using System.Data;
using System.IO;
using System.Windows.Media;

namespace DBHTab.Pages
{
    /// <summary>
    /// RegCorrPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegCorrPage : ModernWpf.Controls.Page
    {
        #region Field Variables                
        #endregion

        #region Initialize

        public RegCorrPage(string pageDir)
        {
            InitializeComponent();
            LoadCorrInfo(pageDir);
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

        private void LoadCorrInfo(string pageDir)
        {
            string infoPath = Path.Combine(pageDir, "Info.json");
            if (!File.Exists(infoPath)) return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            // Results → DataGrid 바인딩
            var results = jObj["Results"]?.ToObject<List<Dictionary<string, object>>>();
            if (results != null)
            {
                var table = new DataTable();
                if (results.Count > 0)
                {
                    foreach (var key in results[0].Keys)
                        table.Columns.Add(key);
                }
                foreach (var row in results)
                {
                    var dr = table.NewRow();
                    foreach (var kv in row)
                        dr[kv.Key] = kv.Value ?? "";
                    table.Rows.Add(dr);
                }

                CorrResultsGrid.ItemsSource = table.DefaultView;

                // CorrelationLevel 강조 표시
                CorrResultsGrid.LoadingRow += (s, e) =>
                {
                    var row = (DataRowView)e.Row.Item;
                    string level = row["상관 관계"].ToString();

                    if (level.Contains("강한"))
                        e.Row.Background = Brushes.LightSkyBlue;
                    else if (level.Contains("약한"))
                        e.Row.Background = Brushes.LightCyan;
                };
            }

            // 이미지 로드
            var plotInfo = jObj["plot_info"];
            if (plotInfo != null)
            {
                var imgPath = plotInfo["corr_matrix_img"]?.ToString();
                if (imgPath != null)
                {
                    cvScatterMatrix.ChartPath = "corr_matrix.png";
                    cvScatterMatrix.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                }

                imgPath = plotInfo["scatter_matrix_img"]?.ToString();
                if (imgPath != null)
                {
                    cvCorrMatrix.ChartPath = "scatter_matrix.png";
                    cvCorrMatrix.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                }

                imgPath = plotInfo["vif_score_img"]?.ToString();
                if (imgPath != null)
                {
                    cvVifScore.ChartPath = "vif_score.png";
                    cvVifScore.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
