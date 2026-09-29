using DBHTab.Models;
using DBHTab.Views;

namespace DBHTab.Commands
{
    public class PopupCreateNewColumnCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public PopupCreateNewColumnCommand()
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
            IEnumerable<ColumnInfo>? columns = parameter[1] as IEnumerable<ColumnInfo>;
            if (string.IsNullOrEmpty(projectDir) | columns == null)
            {
                return false;
            }
            if (columns.Count() < 1)
            {
                return false;
            }
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            IEnumerable<ColumnInfo>? columns = parameter[1] as IEnumerable<ColumnInfo>;
            ProjectMainView mainView = (ProjectMainView)parameter[2];
            CreateColumnAsync(projectDir, columns, mainView);
        }

        #endregion

        #region Private Methods

        private async void CreateColumnAsync(string? projectDir, IEnumerable<ColumnInfo>? columns, ProjectMainView mainView)
        {
            CreateNewColumnPopupView createColView = new CreateNewColumnPopupView(projectDir, columns, mainView);
            var result = await createColView.ShowAsync();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
