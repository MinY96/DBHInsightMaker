using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class InitProjectDataCommand : CommandBase
    {
        #region Field Variables

        private ProjectMainViewModel _projectMainViewModel;

        #endregion

        #region Initialize

        public InitProjectDataCommand(ProjectMainViewModel projectMainViewModel)
        {
            _projectMainViewModel = projectMainViewModel;
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
            InitProjectDataInfo();
        }

        #endregion

        #region Private Methods

        private async void InitProjectDataInfo()
        {
            await _projectMainViewModel.InitDataInfoAsync();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
