using Newtonsoft.Json.Linq;
using System.Data;
using System.IO;
using System.Windows;
using System.Windows.Media;

namespace DBHTab.Pages
{
    /// <summary>
    /// RegSelectionPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegSelectionPage : ModernWpf.Controls.Page
    {
        #region Field Variables                        

        #endregion

        #region Initialize

        public RegSelectionPage(string pageDir)
        {
            InitializeComponent();
            LoadSelectionInfo(pageDir);
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

        private void LoadSelectionInfo(string pageDir)
        {
            string infoPath = Path.Combine(pageDir, "Info.json");
            if (!File.Exists(infoPath)) return;

            string json = File.ReadAllText(infoPath);
            var jObj = JObject.Parse(json);

            SelectionMethodText.Text = jObj["selection_method"].ToString();
            IndepVarsList.ItemsSource = jObj["indep_vars"]?.ToObject<List<string>>();

            var hist = jObj["selection_hist"]?.ToObject<List<Dictionary<string, object>>>();
            if (hist != null)
            {
                var table = new DataTable();
                foreach (var key in hist[0].Keys) table.Columns.Add(key);
                foreach (var row in hist)
                {
                    var dr = table.NewRow();
                    foreach (var kv in row) dr[kv.Key] = kv.Value ?? "";
                    table.Rows.Add(dr);
                }
                SelectionHistGrid.ItemsSource = table.DefaultView;

                SelectionHistGrid.LoadingRow += (s, e) =>
                {
                    var row = (DataRowView)e.Row.Item;
                    if (row["best"].ToString() == "☆")
                    {
                        e.Row.Background = Brushes.LightGoldenrodYellow;
                        e.Row.FontWeight = FontWeights.Bold;
                    }
                };
            }

            var imgPath = jObj["selection_hist_img"]?.ToString();
            if (File.Exists(imgPath))
            {
                cvHistory.ChartPath = "selection_hist.png";
                cvHistory.ChartImage = new System.Windows.Media.Imaging.BitmapImage(new System.Uri(imgPath));
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
