using DBHTab.ViewModels;
using DBHTab.Views;
using System.Windows;

namespace DBHTab.Commands
{
    public class PopupLoadDataCommand : CommandBase
    {
        #region Field Variables

        private ProjectMainViewModel _projectMainViewModel;

        #endregion

        #region Initialize

        public PopupLoadDataCommand(ProjectMainViewModel projectMainViewModel)
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
            bool isLoadData = (bool)parameter;
            LoadData(isLoadData);
        }

        #endregion

        #region Private Methods
        private void LoadData(bool isLoadData)
        {
            if (isLoadData)
            {
                if (ModernWpf.MessageBox.Show("데이터를 새로 로드하시겠습니까?", "데이터 로드", MessageBoxButton.YesNo) == MessageBoxResult.No)
                    return;
            }
            LoadDataPopupView loadDataPopupView = new LoadDataPopupView(_projectMainViewModel);
            loadDataPopupView.ShowAsync();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
