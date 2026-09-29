using DBHTab.Models;
using DBHTab.ViewModels;
using DBHTab.Views;

namespace DBHTab.Commands
{
    public class PopupConvertTypeCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public PopupConvertTypeCommand()
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
            var parameter = (object[])parameters;
            if (parameter == null)
            {
                return false;
            }
            if (parameter.Length != 3)
            {
                return false;
            }
            string projectDir = parameter[0] as string;
            ColumnInfo? selectedColumn = parameter[1] as ColumnInfo;
            if (string.IsNullOrEmpty(projectDir) | selectedColumn == null)
            {
                return false;
            }
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            ColumnInfo selectedColumn = (ColumnInfo)parameter[1];
            ProjectMainView mainView = (ProjectMainView)parameter[2];
            ShowConvertType(projectDir, selectedColumn, mainView);
        }

        #endregion

        #region Private Methods

        private async void ShowConvertType(string? projectDir, ColumnInfo? selectedColumn, ProjectMainView mainView)
        {
            IEnumerable<string> colData = await HttpRequest.PostColumnDataInit(projectDir, selectedColumn);
            var createPopup = new ConvertDataTypePopupView(projectDir, selectedColumn, colData);
            bool? result = createPopup.ShowDialog();
            if (result == true)
            {
                await ((ProjectMainViewModel)mainView.DataContext).InitDataInfoAsync();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
