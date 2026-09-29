using DBHTab.Pages;
using DBHTab.ViewModels;
using ModernWpf.Controls;
using System.IO;

namespace DBHTab.Views
{
    /// <summary>
    /// RegressionAnalysisView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegressionAnalysisView
    {
        private string _regressionDir = string.Empty;
        private string _projectName = string.Empty;
        private string _regressionType = string.Empty;

        public RegressionAnalysisView(string projectName, string regressionDir, string regType)
        {
            _regressionDir = regressionDir;
            _projectName = projectName;
            _regressionType = regType;
            InitializeComponent();
            InitMenuState();
            this.DataContext = new RegressionAnalysisViewModel(projectName, regressionDir);
        }

        private void InitMenuState()
        {
            SetMenuState(regSelectionPage);
            SetMenuState(regCorrPage);
            SetMenuState(regModelPage);
            SetMenuState(regResidualPage);
            SetMenuState(regTestPage);
        }

        private void SetMenuState(NavigationViewItem item)
        {
            string pageDir = Path.Combine(_regressionDir, item.Tag.ToString());
            string infoPath = Path.Combine(pageDir, "info.json");
            item.IsEnabled = File.Exists(infoPath);
        }

        private void nvRegressionView_SelectionChanged(NavigationView sender, NavigationViewSelectionChangedEventArgs args)
        {
            if (args.SelectedItem is NavigationViewItem selectedItem)
            {
                string pageDir = Path.Combine(_regressionDir, selectedItem.Tag.ToString());

                switch (selectedItem.Tag)
                {
                    case "1_selection":
                        contentFrameRegression.Navigate(new RegSelectionPage(pageDir));
                        break;
                    case "2_corr":
                        contentFrameRegression.Navigate(new RegCorrPage(pageDir));
                        break;
                    case "3_model":
                        //contentFrameRegression.Navigate(new RegModelPage(pageDir));
                        if (_regressionType == "Linear Regression")
                            contentFrameRegression.Navigate(new RegLinearModelPage(pageDir));
                        else if (_regressionType == "Logistic Regression")
                            contentFrameRegression.Navigate(new RegLogisticModelPage(pageDir));
                        break;
                    case "4_residual":
                        contentFrameRegression.Navigate(new RegResidualPage(pageDir));
                        break;
                    case "5_test":
                        //contentFrameRegression.Navigate(new RegTestPage(pageDir));
                        if (_regressionType == "Linear Regression")
                            contentFrameRegression.Navigate(new RegLinearTestPage(pageDir));
                        else if (_regressionType == "Logistic Regression")                            
                            contentFrameRegression.Navigate(new RegLogisticTestPage(pageDir));
                        break;
                }
            }
        }

        public string ProjectName
        {
            get { return _projectName; }
            set { _projectName = value; }
        }
    }
}
