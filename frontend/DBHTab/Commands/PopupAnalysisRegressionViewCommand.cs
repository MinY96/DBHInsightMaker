using DBHTab.Models;
using DBHTab.ViewModels;
using DBHTab.Views;

namespace DBHTab.Commands
{
    public class PopupAnalysisRegressionViewCommand : CommandBase
    {
        #region Field Variables

        private ProjectMainView owner;

        #endregion

        #region Initialize

        public PopupAnalysisRegressionViewCommand(ProjectMainView projectMainView)
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
            ShowRegression(projectName, projectDir, columns);
        }

        #endregion

        #region Private Methods

        private async void ShowRegression(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            var regOptionView = new RegressionOptionPopupView(projectName, projectDir, columns);
            RegressionOptionViewModel regOptionModel = regOptionView.DataContext as RegressionOptionViewModel;
            regOptionView.Owner = owner;
            regOptionView.ShowDialog();
            string regDir = regOptionModel.RegressionDir;
            string regType = regOptionModel.ModelType;
            if (!string.IsNullOrEmpty(regDir))
            {
                var regAnalysisView = new RegressionAnalysisView(projectName, regDir, regType);
                regAnalysisView.Show();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
