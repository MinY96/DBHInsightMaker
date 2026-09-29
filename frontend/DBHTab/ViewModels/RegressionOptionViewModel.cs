using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using Newtonsoft.Json;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class RegressionProject
    {
        public string RegressionDir { get; set; } = default!;
        public string CreateTime { get; set; } = default!;
        public string ModelType { get; set; } = default!;
        public string DepVar { get; set; } = default!;
        public string Selection { get; set; } = default!;
        public string Scaler { get; set; } = default!;
        public string Impute { get; set; } = default!;
        public string TestRatio { get; set; } = default!;
        public string OptionDetail { get; set; } = default!;
    }

    public class RegressionOptionViewModel : ViewModelBase
    {
        #region Field Variables

        private string _projectName;
        private string _projectDir;
        private string _regressionDir = string.Empty;
        private string _loadMsg = string.Empty;
        private string _modelType = string.Empty;
        private bool _isLoad = false;
        private bool _isIndep = true;
        private bool _isSplit = false;
        private int _selectionMethodIndex = 0;
        private int _scalerMethodIndex = 0;
        private int _imputeMethodIndex = 0;
        private int _testRatio = 0;
        private ObservableCollection<ColumnInfo> _columns = new ObservableCollection<ColumnInfo>();
        private ObservableCollection<ColumnInfo> _indepColumns = new ObservableCollection<ColumnInfo>();
        private ObservableCollection<ColumnInfo> _depColums = new ObservableCollection<ColumnInfo>();
        private ObservableCollection<RegressionProject> _regProjects = new ObservableCollection<RegressionProject>();
        private RegressionOptionPopupView _viewOption;

        #endregion

        #region Initialize

        public RegressionOptionViewModel(RegressionOptionPopupView viewOption, string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            _viewOption = viewOption;
            _projectName = projectName;
            _projectDir = projectDir;
            _columns = new ObservableCollection<ColumnInfo>(columns.OrderBy(x => x.Column));
            LoadRegressionHistory(projectDir);
            LoadRegressionResultCommand = new LoadRegressionResultCommand(this, viewOption);
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

        public string RegressionDir
        {
            get { return _regressionDir; }
            set { _regressionDir = value; }
        }

        public string ModelType
        {
            get { return _modelType; }
            set { _modelType = value; }
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

        public bool IsLoad
        {
            get { return _isLoad; }
            set
            {
                _isLoad = value;
                OnPropertyChanged();
            }
        }

        public bool IsIndep
        {
            get { return _isIndep; }
            set
            {
                _isIndep = value;
                OnPropertyChanged();
            }
        }

        public bool IsSplit
        {
            get { return _isSplit; }
            set
            {
                _isSplit = value;
                OnPropertyChanged();
            }
        }

        public int SelectionMethodIndex
        {
            get { return _selectionMethodIndex; }
            set
            {
                _selectionMethodIndex = value;
                OnPropertyChanged();
            }
        }

        public int ScalerMethodIndex
        {
            get { return _scalerMethodIndex; }
            set
            {
                _scalerMethodIndex = value;
                OnPropertyChanged();
            }
        }

        public int ImputeMethodIndex
        {
            get { return _imputeMethodIndex; }
            set
            {
                _imputeMethodIndex = value;
                OnPropertyChanged();
            }
        }

        public int TestRatio
        {
            get { return _testRatio; }
            set
            {
                _testRatio = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<ColumnInfo> Columns
        {
            get { return _columns; }
            set
            {
                _columns = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(ColumnsCount));
            }
        }

        public int ColumnsCount => Columns.Count;

        public ObservableCollection<ColumnInfo> IndepColumns
        {
            get { return _indepColumns; }
            set
            {
                _indepColumns = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(IndepColumnsCount));
            }
        }

        public int IndepColumnsCount => IndepColumns.Count;

        public ObservableCollection<ColumnInfo> DepColumns
        {
            get { return _depColums; }
            set
            {
                _depColums = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(DepColumnsCount));
            }
        }

        public int DepColumnsCount => DepColumns.Count;

        public ObservableCollection<RegressionProject> RegressionProjects
        {
            get { return _regProjects; }
            set
            {
                _regProjects = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(RegressionProjectsCount));
            }
        }

        public int RegressionProjectsCount => RegressionProjects.Count;

        #endregion

        #region Commands

        public ICommand LoadRegressionResultCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void MoveForwardColumns(List<ColumnInfo> selectedItems)
        {
            foreach (var item in selectedItems)
            {
                Columns.Remove(item);
                OnPropertyChanged(nameof(ColumnsCount));
                if (IsIndep)
                {
                    if ((item.UniqueCount > 5) & (item.ColumnType != "Numerical"))
                    {
                        ModernWpf.MessageBox.Show("독립 변수에 고유값이 5개 이상인 범주형 변수를 넣을 수 없습니다.", "경고", MessageBoxButton.OK, MessageBoxImage.Warning);
                        Columns.Add(item);
                        OnPropertyChanged(nameof(ColumnsCount));
                    }
                    else
                    {
                        IndepColumns.Add(item);
                        OnPropertyChanged(nameof(IndepColumnsCount));
                    }
                }
                else
                {
                    if (DepColumns.Count >= 1)
                    {
                        ModernWpf.MessageBox.Show("종속 변수에는 이미 변수가 지정되어 있습니다.", "경고", MessageBoxButton.OK, MessageBoxImage.Warning);
                        Columns.Add(item);
                        OnPropertyChanged(nameof(ColumnsCount));
                    }
                    else
                    {
                        DepColumns.Add(item);
                        OnPropertyChanged(nameof(DepColumnsCount));
                    }
                }
            }
            Columns = new ObservableCollection<ColumnInfo>(Columns.OrderBy(x => x.Column));
            DepColumns = new ObservableCollection<ColumnInfo>(DepColumns.OrderBy(x => x.Column));
            IndepColumns = new ObservableCollection<ColumnInfo>(IndepColumns.OrderBy(x => x.Column));
        }

        public void MoveBackwardColumns(List<ColumnInfo> selectedIndep, List<ColumnInfo> selectedDep)
        {
            if (IsIndep)
            {
                foreach (var item in selectedIndep)
                {
                    IndepColumns.Remove(item);
                    Columns.Add(item);
                    OnPropertyChanged(nameof(IndepColumnsCount));
                    OnPropertyChanged(nameof(ColumnsCount));
                }
            }
            else
            {
                foreach (var item in selectedDep)
                {
                    DepColumns.Remove(item);
                    Columns.Add(item);
                    OnPropertyChanged(nameof(DepColumnsCount));
                    OnPropertyChanged(nameof(ColumnsCount));
                }
            }
            Columns = new ObservableCollection<ColumnInfo>(Columns.OrderBy(x => x.Column));
        }

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        public void OpenRegressionResult(RegressionProject regProject)
        {
            RegressionDir = regProject.RegressionDir;
            ModelType = regProject.ModelType;
            _viewOption.Close();
        }

        #endregion

        #region Private Methods

        private void LoadRegressionHistory(string projectDir)
        {
            string projectAnalyzeDir = System.IO.Path.Combine(projectDir, "analyze");
            string regProjectsDir = System.IO.Path.Combine(projectAnalyzeDir, "regression");

            var projects = new ObservableCollection<RegressionProject>();
            if (Path.Exists(regProjectsDir))
            {
                var directories = Directory.GetDirectories(regProjectsDir);
                foreach (var directory in directories)
                {
                    var jsonFilePath = System.IO.Path.Combine(directory, "info.json");
                    if (File.Exists(jsonFilePath))
                    {
                        var jsonContent = File.ReadAllText(jsonFilePath);
                        var project = JsonConvert.DeserializeObject<RegressionProject>(jsonContent);
                        if (project != null)
                        {
                            string detailOption = GetDetailProjectOption(project);
                            project.OptionDetail = detailOption;
                            projects.Add(project);
                        }
                    }
                }
            }

            RegressionProjects = projects;
        }

        private string GetDetailProjectOption(RegressionProject project)
        {
            string detail = string.Empty;
            List<string> temp = new List<string>();
            if (!string.IsNullOrEmpty(project.Selection))
                temp.Add(ConvertToSelectionMethod(project.Selection));
            if (!string.IsNullOrEmpty(project.Scaler))
                temp.Add(ConvertToScalerMethod(project.Scaler));
            if (!string.IsNullOrEmpty(project.Impute))
                temp.Add(ConvertToImputeMethod(project.Impute));
            if (!string.IsNullOrEmpty(project.TestRatio))
                temp.Add(project.TestRatio);
            detail = String.Join(" / ", temp);
            return detail;
        }

        private string ConvertToSelectionMethod(string method)
        {
            string selectionMethod = string.Empty;
            switch (method)
            {
                case "forward":
                    selectionMethod = "전진 선택법";
                    break;
                case "backward":
                    selectionMethod = "후진 제거법";
                    break;
                case "stepwise":
                    selectionMethod = "Step-Wise";
                    break;
            }
            return selectionMethod;
        }

        private string ConvertToScalerMethod(string method)
        {
            string scalerMethod = string.Empty;
            switch (method)
            {
                case "standard":
                    scalerMethod = "Standard";
                    break;
                case "minmax":
                    scalerMethod = "Min-Max";
                    break;
                case "maxabs":
                    scalerMethod = "Max-Abs";
                    break;
                case "robust":
                    scalerMethod = "Robust";
                    break;
            }
            return scalerMethod;
        }

        private string ConvertToImputeMethod(string method)
        {
            string imputeMethod = string.Empty;
            switch (method)
            {
                case "remove":
                    imputeMethod = "제거";
                    break;
                case "mean":
                    imputeMethod = "평균";
                    break;
                case "median":
                    imputeMethod = "중앙값";
                    break;
                case "mode":
                    imputeMethod = "최빈값";
                    break;
                case "linear":
                    imputeMethod = "선형";
                    break;
            }
            return imputeMethod;
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
