using DBHTab.Models;
using DBHTab.Views;

namespace DBHTab.ViewModels
{
    public class ColumnChartPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private bool _isLoad = false;
        private string _loadMsg = string.Empty;
        string _projectDir = string.Empty;
        ColumnChartPopupView _columnChartPopupView;
        ColumnInfo _columnInfo;
        IList<ChartInfo> _charts;

        #endregion

        #region Initialize

        public ColumnChartPopupViewModel(ColumnChartPopupView columnChartPopupView, string projectDir, ColumnInfo columnInfo)
        {
            _columnChartPopupView = columnChartPopupView;
            _projectDir = projectDir;
            _columnInfo = columnInfo;
            LoadCharts();
        }

        #endregion

        #region Properties        

        public string ProjectDir
        {
            get { return _projectDir; }
            set { _projectDir = value; }
        }

        public string ColumnName
        {
            get { return _columnInfo.Column; }
        }

        public string ColumnType
        {
            get { return _columnInfo.ColumnType; }
        }

        public string ColumnChar
        {
            get { return _columnInfo.ColumnChar; }
        }

        public bool IsLoad
        {
            get { return _isLoad; }
            set
            {
                _isLoad = value;
                OnPropertyChanged();
            }
        }

        public string LoadingMessage
        {
            get { return _loadMsg; }
            set
            {
                _loadMsg = value;
                OnPropertyChanged();
            }
        }

        public IList<ChartInfo> Charts
        {
            get { return _charts; }
            set
            {
                _charts = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods

        private async void LoadCharts()
        {
            SetProgressSpinner(true, "Chart 로드중...");
            IEnumerable<ChartInfo> chartInfos = await HttpRequest.PostColumnCharts(ProjectDir, _columnInfo);
            Charts = new List<ChartInfo>(chartInfos);
            SetProgressSpinner(false);
        }

        private void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
