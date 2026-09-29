using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class RelativeChartPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private RelativeChartPopupView _relativeChartPopupView;
        private string _projectName;
        private string _projectDir;
        private bool _isLoad = false;
        private string _loadMsg = string.Empty;
        IList<ColumnInfo> _columns;
        private ColumnInfo _columnXaxis;
        private ColumnInfo _columnYaxis;
        private ColumnInfo _columnZaxis;
        private ColumnInfo _columnGroup;
        IList<ChartInfo> _charts;

        #endregion

        #region Initialize

        public RelativeChartPopupViewModel(RelativeChartPopupView relativeChartPopupView, string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            _relativeChartPopupView = relativeChartPopupView;
            _projectName = projectName;
            _projectDir = projectDir;
            _columns = new List<ColumnInfo>(columns);
            UpdateComboboxItemState();
            LoadRelativeChartCommand = new LoadRelativeChartCommand(this);
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

        public string LoadingMessage
        {
            get { return _loadMsg; }
            set
            {
                _loadMsg = value;
                OnPropertyChanged();
            }
        }

        public IList<ColumnInfo> ColumnLists
        {
            get { return _columns; }
            set
            {
                _columns = value;
                OnPropertyChanged();
            }
        }

        public ColumnInfo ColumnXaxis
        {
            get { return _columnXaxis; }
            set
            {
                _columnXaxis = value;
                OnPropertyChanged();
            }
        }

        public ColumnInfo ColumnYaxis
        {
            get { return _columnYaxis; }
            set
            {
                _columnYaxis = value;
                OnPropertyChanged();
            }
        }

        public ColumnInfo ColumnZaxis
        {
            get { return _columnZaxis; }
            set
            {
                _columnZaxis = value;
                OnPropertyChanged();
            }
        }

        public ColumnInfo ColumnGroup
        {
            get { return _columnGroup; }
            set
            {
                _columnGroup = value;
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

        public ICommand LoadRelativeChartCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        public void SetCharts(IEnumerable<ChartInfo> chartInfos)
        {
            Charts = new List<ChartInfo>(chartInfos);
        }

        #endregion

        #region Private Methods

        private void UpdateComboboxItemState()
        {
            foreach (var column in ColumnLists)
            {
                column.IsEnabled = true;
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
