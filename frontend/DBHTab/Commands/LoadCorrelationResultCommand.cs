using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;

namespace DBHTab.Commands
{
    public class LoadCorrelationResultCommand : CommandBase
    {
        #region Field Variables

        private CorrelationAnalysisViewModel _correlationAnalysisViewModel;

        #endregion

        #region Initialize

        public LoadCorrelationResultCommand(CorrelationAnalysisViewModel correlationAnalysisViewModel)
        {
            _correlationAnalysisViewModel = correlationAnalysisViewModel;
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
            bool? isPearson = parameter[1] as bool?;
            IEnumerable<ColumnInfo> columns = parameter[2] as IEnumerable<ColumnInfo>;
            if (string.IsNullOrEmpty(projectDir) ||
                isPearson == null ||
                columns == null)
            {
                return false;
            }
            var checkedColumns = columns.Where(c => c.IsChecked).ToList();
            if (checkedColumns.Count < 2)
                return false;
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            bool isPearson = (bool)parameter[1];
            string corrMethod = isPearson ? "pearson" : "spearman";
            IEnumerable<ColumnInfo> columns = parameter[2] as IEnumerable<ColumnInfo>;
            var checkedColumns = columns.Where(c => c.IsChecked).ToList();
            LoadChartS(projectDir, corrMethod, checkedColumns);
        }

        #endregion

        #region Private Methods

        private async void LoadChartS(string? projectDir, string corrMethod, IEnumerable<ColumnInfo>? columns)
        {
            if (corrMethod == "pearson")
            {
                if (columns.Any(c => c.ColumnType == "Categorical"))
                {
                    ModernWpf.MessageBox.Show("(Pearson) 범주형 변수가 포함되어 있습니다.", "변수 재설정 필요", MessageBoxButton.OK);
                    return;
                }
            }
            _correlationAnalysisViewModel.SetProgressSpinner(true, "상관분석 진행중...");
            Dictionary<string, object> result = await HttpRequest.PostCorrResult(projectDir, corrMethod, columns);
            string corrTitle = "상관분석: " + string.Join(", ", columns.Select(c => c.Column));
            _correlationAnalysisViewModel.UpdateCorrResult(corrTitle, result);
            _correlationAnalysisViewModel.SetProgressSpinner(false);
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
