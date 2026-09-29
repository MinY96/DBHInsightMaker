using DBHTab.Models;
using DBHTab.Views;

namespace DBHTab.Commands
{
    public class PopupNormalityTestCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public PopupNormalityTestCommand()
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
            if (parameter.Length != 2)
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
            ShowNomalityTest(projectDir, selectedColumn);
        }

        #endregion

        #region Private Methods

        private async void ShowNomalityTest(string? projectDir, ColumnInfo? selectedColumn)
        {

            var createPopup = new NormalityTestPopupView(projectDir, selectedColumn);
            createPopup.Show();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
