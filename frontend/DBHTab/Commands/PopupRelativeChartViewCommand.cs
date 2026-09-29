using DBHTab.Models;
using DBHTab.Views;

namespace DBHTab.Commands
{
    public class PopupRelativeChartViewCommand : CommandBase
    {
        #region Field Variables

        private ProjectMainView owner;

        #endregion

        #region Initialize

        public PopupRelativeChartViewCommand(ProjectMainView projectMainView)
        {
            owner = projectMainView;
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
            string projectName = parameter[0] as string;
            string projectDir = parameter[1] as string;
            IEnumerable<ColumnInfo>? columns = parameter[2] as IEnumerable<ColumnInfo>;
            if (string.IsNullOrEmpty(projectDir) | columns == null)
            {
                return false;
            }
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectName = parameter[0] as string;
            string projectDir = parameter[1] as string;
            IEnumerable<ColumnInfo> columns = parameter[2] as IEnumerable<ColumnInfo>;
            ShowRelativeChart(projectName, projectDir, columns);
        }

        #endregion

        #region Private Methods

        private async void ShowRelativeChart(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {

            var chartPopupView = new RelativeChartPopupView(projectName, projectDir, columns);
            chartPopupView.Owner = owner;
            chartPopupView.Show();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
