using DBHTab.Models;
using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class IsOpenApiCommand : CommandBase
    {
        #region Field Variables

        OpenProjectViewModel _openProjectViewModel;

        #endregion

        #region Initialize

        public IsOpenApiCommand(OpenProjectViewModel openProjectViewModel)
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
            CheckApiIsOpen();
        }

        #endregion

        #region Private Methods

        private async void CheckApiIsOpen()
        {
            bool isOpenApi = await HttpRequest.CheckOpenApi();
            if (isOpenApi)
            {
                _openProjectViewModel.SetProgressSpinner(false);
                using var _ = _openProjectViewModel.LoadSavedProjectSAsync();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
