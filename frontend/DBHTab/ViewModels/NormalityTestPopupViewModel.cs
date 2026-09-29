using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class NormalityTestPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private int _selectedMethodIndex = 0;
        private bool _isLoad = false;
        private string _loadMsg = string.Empty;
        private string _bestCase = string.Empty;
        private string _strength = string.Empty;
        private string _weakness = string.Empty;
        private string _result = string.Empty;
        private string _detail = string.Empty;
        private string _qqPlotChartName = string.Empty;
        private string _distPlotChartName = string.Empty;
        private byte[] _qqPlot;
        private byte[] _distPlot;
        string _projectDir = string.Empty;
        NormalityTestPopupView _nomalityTestView;
        ColumnInfo _columnInfo;
        IEnumerable<StatTestInfo> _statTestInfos;

        #endregion

        #region Initialize

        public NormalityTestPopupViewModel(NormalityTestPopupView nomalityTestView, string projectDir, ColumnInfo columnInfo)
        {
            _nomalityTestView = nomalityTestView;
            _projectDir = projectDir;
            _columnInfo = columnInfo;
            LoadTestResult();
            InitCommand();
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

        public string? Mean
        {
            get { return _columnInfo.Mean; }
        }

        public string? Std
        {
            get { return _columnInfo.Std; }
        }

        public int DataCount
        {
            get { return _columnInfo.DataCount; }
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

        public byte[] QQPlot
        {
            get { return _qqPlot; }
            set
            {
                _qqPlot = value;
                OnPropertyChanged();
            }
        }

        public byte[] DistPlot
        {
            get { return _distPlot; }
            set
            {
                _distPlot = value;
                OnPropertyChanged();
            }
        }

        public string QQPlotChartName
        {
            get { return _qqPlotChartName; }
            set
            {
                _qqPlotChartName = value;
                OnPropertyChanged();
            }
        }

        public string DistPlotChartName
        {
            get { return _distPlotChartName; }
            set
            {
                _distPlotChartName = value;
                OnPropertyChanged();
            }
        }

        public int SelectedMethodIndex
        {
            get { return _selectedMethodIndex; }
            set
            {
                _selectedMethodIndex = value;
                OnPropertyChanged();
            }
        }
        public string BestCase
        {
            get { return _bestCase; }
            set
            {
                _bestCase = value;
                OnPropertyChanged();
            }
        }

        public string Strength
        {
            get { return _strength; }
            set
            {
                _strength = value;
                OnPropertyChanged();
            }
        }

        public string Weakness
        {
            get { return _weakness; }
            set
            {
                _weakness = value;
                OnPropertyChanged();
            }
        }

        public string Result
        {
            get { return _result; }
            set
            {
                _result = value;
                OnPropertyChanged();
            }
        }

        public string Detail
        {
            get { return _detail; }
            set
            {
                _detail = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand SaveChartImageCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void UpdateResult()
        {
            if (_statTestInfos != null & SelectedMethodIndex >= 0)
            {
                StatTestInfo resultInfo = _statTestInfos.ToList()[SelectedMethodIndex];
                BestCase = resultInfo.BestCase;
                Strength = resultInfo.Strength;
                Weakness = resultInfo.Weakness;
                string sigLevel = (string)((System.Windows.Controls.ComboBoxItem)_nomalityTestView.cmbSignificanceLevel.SelectedItem).Content;
                float fSigLevel = float.Parse(sigLevel);
                var result = resultInfo.Results.FirstOrDefault(x => x.SignificanceLevel == fSigLevel);
                if (result != null)
                {
                    Result = result.Result;
                    Detail = result.Detail;
                }
            }
        }

        #endregion

        #region Private Methods

        private async void LoadTestResult()
        {
            SetProgressSpinner(true, "정규성 검정 결과 로드중...");
            Dictionary<string, object> result = await HttpRequest.PostNomalityTestResult(ProjectDir, _columnInfo);
            _statTestInfos = (IEnumerable<StatTestInfo>)result["Test"];
            foreach (ChartInfo chart in (IEnumerable<ChartInfo>)result["Chart"])
            {
                if (chart.ChartName == "QQ-Plot")
                {
                    QQPlot = chart.ChartImage;
                    QQPlotChartName = chart.ChartFileName;
                }
                else if (chart.ChartName == "Distribution")
                {
                    DistPlot = chart.ChartImage;
                    DistPlotChartName = chart.ChartFileName;
                }
            }
            UpdateResult();
            SetProgressSpinner(false);
        }

        private void InitCommand()
        {
            SaveChartImageCommand = new SaveChartImageCommand();
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
