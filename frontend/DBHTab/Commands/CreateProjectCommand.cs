using DBHTab.Models;
using DBHTab.ViewModels;
using System.IO;
using System.Windows;

namespace DBHTab.Commands
{
    public class CreateProjectCommand : CommandBase
    {
        #region Field Variables

        private CreateProjectPopupViewModel _createProjectPopupViewModel;

        #endregion

        #region Initialize

        public CreateProjectCommand(CreateProjectPopupViewModel createProjectPopupViewModel)
        {
            _createProjectPopupViewModel = createProjectPopupViewModel;
        }

        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public override bool CanExecute(object? parameter)
        {
            string projectName = (string)parameter;
            if (string.IsNullOrEmpty(projectName))
            {
                return false;
            }
            return true;
        }

        public override void Execute(object? parameter)
        {
            string projectName = (string)parameter;
            string projectDesc = _createProjectPopupViewModel.ProjectDesc;
            CreateProject(projectName, projectDesc);
        }

        #endregion

        #region Private Methods

        private async void CreateProject(string? projectName, string projectDesc)
        {
            var userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            string projectParenteDir = Path.Combine(userPath, "insightmaker_project");
            bool result = await HttpRequest.PostCreateProject(projectParenteDir, projectName, projectDesc);
            if (result)
            {
                ModernWpf.MessageBox.Show($"{projectName} 프로젝트를 생성하였습니다", "Project 생성", MessageBoxButton.OK);
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
