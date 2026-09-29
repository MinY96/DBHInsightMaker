using DBHTab.Commands;
using DBHTab.Models;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class OpenProjectViewModel : ViewModelBase
    {
        #region Field Variables

        private Process _edaLogicProcess;
        private bool _isOpenApi = false;
        private bool _isLoad = false;
        private string _loadMsg = string.Empty;
        string? _projectParenteDir;
        string? _filterProjectName;
        DateTime? _filterStartDate;
        DateTime? _filterEndDate;
        ObservableCollection<ProjectInfo> _projects = new ObservableCollection<ProjectInfo>();
        ObservableCollection<ProjectInfo> _filterProjects = new ObservableCollection<ProjectInfo>();

        #endregion

        #region Initialize

        public OpenProjectViewModel()
        {
            InitCommands();
            SetProjectSaveDir();
            using var _ = ExecuteApi();
            //using var _ = LoadSavedProjectSAsync();
        }

        #endregion

        #region Properties

        public ObservableCollection<ProjectInfo> Projects
        {
            get { return _projects; }
            set
            {
                _projects = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<ProjectInfo> FilteredProjects
        {
            get { return _filterProjects; }
            set
            {
                _filterProjects = value;
                OnPropertyChanged();
            }
        }

        public string? FilterProjectName
        {
            get { return _filterProjectName; }
            set
            {
                _filterProjectName = value;
                OnPropertyChanged();
                UpdateFilterdProject();
            }
        }

        public DateTime? FilterStartDate
        {
            get { return _filterStartDate; }
            set
            {
                _filterStartDate = value;
                OnPropertyChanged();
                UpdateFilterdProject();
            }
        }

        public DateTime? FilterEndDate
        {
            get { return _filterEndDate; }
            set
            {
                _filterEndDate = value;
                OnPropertyChanged();
                UpdateFilterdProject();
            }
        }

        public bool IsOpenApi
        {
            get { return _isOpenApi; }
            set
            {
                _isOpenApi = value;
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

        public string LoadingMessage
        {
            get { return _loadMsg; }
            set
            {
                _loadMsg = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand IsOpenApiCommand { get; set; }
        public ICommand LoadProjectCommand { get; set; }
        public ICommand DeleteProjectCommand { get; set; }

        #endregion

        #region Public Methods

        public void UpdateProjects(IEnumerable<ProjectInfo> projects)
        {
            if (projects != null)
            {
                var sorted = projects.OrderByDescending(p => p.CreateTime).ThenByDescending(p => p.ProjectName);
                Projects = new ObservableCollection<ProjectInfo>(sorted);
            }
            UpdateFilterdProject();
        }

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        #endregion

        #region Private Methods

        private async Task ExecuteApi()
        {
            SetProgressSpinner(true, "API를 실행중입니다...");
            IsOpenApiCommand.Execute(this);
        }

        private void InitCommands()
        {
            LoadProjectCommand = new LoadProjectCommand(this);
            DeleteProjectCommand = new DeleteProjectCommand(this);
            IsOpenApiCommand = new IsOpenApiCommand(this);
        }

        private void SetProjectSaveDir()
        {
            var userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            _projectParenteDir = Path.Combine(userPath, "insightmaker_project");
            DirectoryInfo dirProjects = new DirectoryInfo(_projectParenteDir);
            if (!dirProjects.Exists)
            {
                dirProjects.Create();
            }
        }

        public async Task LoadSavedProjectSAsync()
        {
            LoadProjectCommand.Execute(_projectParenteDir);
        }

        private void UpdateFilterdProject()
        {
            if (_filterProjectName == null && _filterStartDate == null && _filterEndDate == null)
            {
                FilteredProjects = new ObservableCollection<ProjectInfo>(_projects);
            }
            else
            {
                var filteredProjects = _projects.Where(project =>
                    (_filterProjectName == null || project.ProjectName.ToLower().Contains(_filterProjectName.ToLower())) &&
                    (_filterStartDate == null || project.CreateTime >= _filterStartDate) &&
                    (_filterEndDate == null || project.CreateTime <= _filterEndDate));
                FilteredProjects = new ObservableCollection<ProjectInfo>(filteredProjects);
            }
        }

        #endregion
    }
}
