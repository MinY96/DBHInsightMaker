using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class CorrelationAnalysisViewModel : ViewModelBase
    {
        #region Field Variables

        private CorrelationAnalysisView _correlationAnalysisView;
        string _projectName;
        string _projectDir;
        private bool _isLoad = false;
        private bool _isPearson = true;
        private string _corrTitle = "상관분석";
        private string _loadMsg = string.Empty;
        private string _corrMethod = string.Empty;
        private string _corrMatrixPlotChartName = string.Empty;
        private string _scatterMatrixChartName = string.Empty;
        private byte[] _corrMatrixPlot;
        private byte[] _scatterMatrixPlot;
        ObservableCollection<ColumnInfo> _columnInfos;
        ObservableCollection<CorrResult> _corrResult;

        #endregion

        #region Initialize

        public CorrelationAnalysisViewModel(CorrelationAnalysisView correlationAnalysisView, string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            _correlationAnalysisView = correlationAnalysisView;
            _projectName = projectName;
            _projectDir = projectDir;
            _columnInfos = new ObservableCollection<ColumnInfo>(columns);
            LoadCorrelationResultCommand = new LoadCorrelationResultCommand(this);
            SaveChartImageCommand = new SaveChartImageCommand();
        }

        #endregion

        #region Properties

        public string ProjectName
        {
            get { return _projectName; }
        }

        public string ProjectDir
        {
            get { return _projectDir; }
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

        public string CorrTitle
        {
            get { return _corrTitle; }
            set
            {
                _corrTitle = value;
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

        public bool IsPearson
        {
            get { return _isPearson; }
            set
            {
                _isPearson = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<ColumnInfo> ColumnList
        {
            get { return _columnInfos; }
            set
            {
                _columnInfos = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<CorrResult>? CorrResult
        {
            get { return _corrResult; }
            set
            {
                _corrResult = value;
                OnPropertyChanged();
            }
        }

        public byte[] CorrMatrixPlot
        {
            get { return _corrMatrixPlot; }
            set
            {
                _corrMatrixPlot = value;
                OnPropertyChanged();
            }
        }

        public byte[] ScatterMatrixPlot
        {
            get { return _scatterMatrixPlot; }
            set
            {
                _scatterMatrixPlot = value;
                OnPropertyChanged();
            }
        }

        public string CorrMatrixChartname
        {
            get { return _corrMatrixPlotChartName; }
            set
            {
                _corrMatrixPlotChartName = value;
                OnPropertyChanged();
            }
        }

        public string ScatterMatrixChartName
        {
            get { return _scatterMatrixChartName; }
            set
            {
                _scatterMatrixChartName = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand LoadCorrelationResultCommand { get; set; }
        public ICommand SaveChartImageCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        public void UpdateCorrResult(string corrTitle, Dictionary<string, object> result)
        {
            CorrTitle = corrTitle;
            foreach (ChartInfo chart in (IEnumerable<ChartInfo>)result["Chart"])
            {
                if (chart.ChartName.StartsWith("상관 계수"))
                {
                    CorrMatrixPlot = chart.ChartImage;
                    CorrMatrixChartname = chart.ChartFileName;
                }
                else if (chart.ChartName == "산점도 행렬")
                {
                    ScatterMatrixPlot = chart.ChartImage;
                    ScatterMatrixChartName = chart.ChartFileName;
                }
            }
            CorrResult = new ObservableCollection<CorrResult>((IEnumerable<CorrResult>)result["Result"]);
        }

        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods
        #endregion
    }
}
