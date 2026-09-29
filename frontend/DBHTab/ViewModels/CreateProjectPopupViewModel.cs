using DBHTab.Commands;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class CreateProjectPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private string _projectName = string.Empty;
        private string _projectDesc = string.Empty;
        private bool _isProjectName = false;

        #endregion

        #region Initialize

        public CreateProjectPopupViewModel()
        {
            InitCommands();
        }

        #endregion

        #region Properties

        public string ProjectName
        {
            get { return _projectName; }
            set
            {
                _projectName = value;
                IsProjectName = !string.IsNullOrEmpty(value);
                OnPropertyChanged();
            }
        }

        public string ProjectDesc
        {
            get { return _projectDesc; }
            set
            {
                _projectDesc = value;
                OnPropertyChanged();
            }
        }

        public bool IsProjectName
        {
            get { return _isProjectName; }
            set
            {
                _isProjectName = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand CreateProjectCommand { get; set; }
        public ICommand UpdateProjectViewCommand { get; set; }

        #endregion

        #region Public Methods
        #endregion

        #region Private Methods

        private void InitCommands()
        {
            CreateProjectCommand = new CreateProjectCommand(this);
        }

        #endregion
    }
}
