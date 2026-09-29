using DBHTab.Models;
using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class LoadProjectCommand : CommandBase
    {
        #region Field Variables

        private OpenProjectViewModel _openProjectViewModel;

        #endregion

        #region Initialize

        public LoadProjectCommand(OpenProjectViewModel openProjectViewModel)
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
            var projectParentDir = (string)parameter;
            using var _ = LoadProjectsAsync(projectParentDir);
        }

        #endregion

        #region Private Methods

        private async Task LoadProjectsAsync(string? projectParentDir)
        {
            IEnumerable<ProjectInfo> projects = await HttpRequest.GetProjectListAsync(projectParentDir);
            _openProjectViewModel.UpdateProjects(projects);
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
