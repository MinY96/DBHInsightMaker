using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;

namespace DBHTab.Commands
{
    public class DeleteProjectCommand : CommandBase
    {
        #region Field Variables

        private OpenProjectViewModel _openProjectViewModel;

        #endregion

        #region Initialize

        public DeleteProjectCommand(OpenProjectViewModel openProjectViewModel)
        {
            _openProjectViewModel = openProjectViewModel;
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
            return true;
        }

        public override void Execute(object? parameter)
        {
            ProjectInfo deleteProject = (ProjectInfo)parameter;
            DeleteProject(deleteProject);
        }

        #endregion

        #region Private Methods

        private async void DeleteProject(ProjectInfo project)
        {
            if (ModernWpf.MessageBox.Show($"{project.ProjectName} 프로젝트를 삭제하시겠습니까?",
                "Project 삭제", MessageBoxButton.YesNo) == MessageBoxResult.Yes)
            {
                bool result = await HttpRequest.PostDeleteProject(project.ProjectName, project.ProjectDir);
                if (result)
                {
                    _openProjectViewModel.LoadSavedProjectSAsync();
                    await ModernWpf.MessageBox.ShowAsync($"{project.ProjectName} 프로젝트를 정상적으로 삭제하였습니다.",
                        "Project 삭제", MessageBoxButton.OK);
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
