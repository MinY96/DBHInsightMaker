using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class ProjectMainViewModel : ViewModelBase
    {
        #region Field Variables

        private ProjectInfo _projectInfo;
        private bool _isWork = false;
        private bool _isEnableGrid = true;
        private bool _isSaveRaw = true;
        private bool _isSaveSummary = true;
        private string _rowcol = string.Empty;
        private string _workMsg = string.Empty;
        ObservableCollection<ColumnInfo> _columns = new ObservableCollection<ColumnInfo>();

        #endregion

        #region Initialize

        public ProjectMainViewModel(ProjectInfo projectInfo, ProjectMainView projectMainView)
        {
            _projectInfo = projectInfo;
            InitCommand(projectMainView);
        }

        #endregion

        #region Properties

        public string ProjectName
        {
            get { return _projectInfo.ProjectName; }
        }

        public string ProjectDesc
        {
            get { return _projectInfo.ProjectDesc; }
        }

        public string FileName
        {
            get { return _projectInfo.FileName; }
            set
            {
                _projectInfo.FileName = value;
                OnPropertyChanged();
            }
        }

        public float FileSize
        {
            get { return _projectInfo.FileSize; }
            set
            {
                _projectInfo.FileSize = value;
                OnPropertyChanged();
            }
        }

        public string RowCol
        {
            get { return _rowcol; }
            set
            {
                _rowcol = value;
                OnPropertyChanged();
            }
        }

        public string WorkingMessage
        {
            get { return _workMsg; }
            set
            {
                _workMsg = value;
                OnPropertyChanged();
            }
        }

        public DateTime CreateTime
        {
            get { return _projectInfo.CreateTime; }
        }

        public string ProjectDir
        {
            get { return _projectInfo.ProjectDir; }
        }

        public bool IsLoadData
        {
            get { return _projectInfo.IsLoadData; }
            set
            {
                _projectInfo.IsLoadData = value;
                OnPropertyChanged();
            }
        }

        public bool IsWork
        {
            get { return _isWork; }
            set
            {
                _isWork = value;
                OnPropertyChanged();
            }
        }

        public bool IsEnableMainGrid
        {
            get { return _isEnableGrid; }
            set
            {
                _isEnableGrid = value;
                OnPropertyChanged();
            }
        }

        public bool IsRaw
        {
            get { return _isSaveRaw; }
        }

        public bool IsSummary
        {
            get { return !_isSaveRaw; }
        }

        public ObservableCollection<ColumnInfo> ColumnLists
        {
            get { return _columns; }
            set
            {
                _columns = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand PopupLoadDataCommand { get; set; }
        public ICommand InitProjectDataCommand { get; set; }
        public ICommand SaveDataToExcelCommand { get; set; }
        public ICommand PopupCreateNewColumnCommand { get; set; }
        public ICommand PopupRelativeChartViewCommand { get; set; }
        public ICommand PopupCustomChartViewCommand { get; set; }
        public ICommand PopupAnalyzeCorrelationViewCommand { get; set; }
        public ICommand PopupAnalysisRegressionViewCommand { get; set; }

        #endregion

        #region Public Events

        public async Task InitDataInfoAsync()
        {
            SetProgressSpinner(true, "프로젝트 로딩...");
            if (IsLoadData)
            {
                await UpdateFileInfoAsync();
                await UpdateColumnListAsync();
            }
            SetProgressSpinner(false);
        }

        public async Task LoadDataAsync(bool isCsv, string sheetName, string filePath)
        {
            SetProgressSpinner(true, "데이터 로드중...");
            IsLoadData = await HttpRequest.PostLoadData(ProjectDir, isCsv, sheetName, filePath);
            if (IsLoadData)
            {
                await HttpRequest.PostUpdateProject(ProjectDir, null, null, null, IsLoadData);
                await UpdateFileInfoAsync();
                await UpdateColumnListAsync();
            }
            // 파일 정보 불러오기
            SetProgressSpinner(false);
        }

        #endregion

        #region Public Methods

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsWork = isProgress;
            IsEnableMainGrid = !isProgress;
            WorkingMessage = progressMessage;
        }

        #endregion

        #region Private Methods

        private void InitCommand(ProjectMainView projectMainView)
        {
            PopupLoadDataCommand = new PopupLoadDataCommand(this);
            InitProjectDataCommand = new InitProjectDataCommand(this);
            InitProjectDataCommand.Execute(this);
            PopupCreateNewColumnCommand = new PopupCreateNewColumnCommand();
            PopupRelativeChartViewCommand = new PopupRelativeChartViewCommand(projectMainView);
            PopupCustomChartViewCommand = new PopupCustomChartViewCommand(projectMainView);
            PopupAnalyzeCorrelationViewCommand = new PopupAnalyzeCorrelationViewCommand(projectMainView);
            PopupAnalysisRegressionViewCommand = new PopupAnalysisRegressionViewCommand(projectMainView);
            SaveDataToExcelCommand = new SaveDataToExcelCommand();
        }


        private async Task UpdateFileInfoAsync()
        {
            var fileInfo = await HttpRequest.PostLoadFileInfo(ProjectDir);
            string fileName = (bool)fileInfo["IsCsv"] ? (string)fileInfo["FileName"]
                : $"{(string)fileInfo["FileName"]} (Sheet명:{(string)fileInfo["SheetName"]})";
            FileName = fileName;
            FileSize = (float)fileInfo["FileSize"];
            RowCol = (string)fileInfo["RowCol"];
        }

        private async Task UpdateColumnListAsync()
        {
            IEnumerable<ColumnInfo> columnList = await HttpRequest.GetColumnListAsync(ProjectDir);
            if (columnList == null)
                return;
            ColumnLists = new ObservableCollection<ColumnInfo>(columnList);
        }

        #endregion

        #region Protected Methods
        #endregion

    }
}
