using DBHTab.Models;
using DBHTab.ViewModels;
using DBHTab.Views;
using System.Windows;

namespace DBHTab.Commands
{
    public class PopupDeleteColumnCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public PopupDeleteColumnCommand()
        {

        }

        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public override bool CanExecute(object? parameters)
        {
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            ColumnInfo selectedColumn = (ColumnInfo)parameter[1];
            ProjectMainView mainView = (ProjectMainView)parameter[2];
            RemoveColumn(projectDir, selectedColumn, mainView);
        }

        #endregion

        #region Private Methods

        private async void RemoveColumn(string? projectDir, ColumnInfo? selectedColumn, ProjectMainView mainView)
        {
            if (ModernWpf.MessageBox.Show($"{selectedColumn.Column}(을)를 제거하시겠습니까?", "데이터 제거", MessageBoxButton.YesNo) == MessageBoxResult.No)
                return;
            bool isRemove = await HttpRequest.PostRemoveColumn(projectDir, selectedColumn);
            if (isRemove)
            {
                await ((ProjectMainViewModel)mainView.DataContext).InitDataInfoAsync();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
