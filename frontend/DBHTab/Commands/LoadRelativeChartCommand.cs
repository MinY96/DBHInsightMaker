using DBHTab.Models;
using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class LoadRelativeChartCommand : CommandBase
    {
        #region Field Variables

        private RelativeChartPopupViewModel _relativeChartPopupViewModel;

        #endregion

        #region Initialize

        public LoadRelativeChartCommand(RelativeChartPopupViewModel relativeChartPopupViewModel)
        {
            _relativeChartPopupViewModel = relativeChartPopupViewModel;
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
            if (parameter.Length != 5)
            {
                return false;
            }
            string projectDir = parameter[0] as string;
            ColumnInfo? colXaxis = parameter[1] as ColumnInfo;
            ColumnInfo? colYaxis = parameter[2] as ColumnInfo;
            ColumnInfo? colZaxis = parameter[3] as ColumnInfo;
            ColumnInfo? colGroup = parameter[4] as ColumnInfo;
            //if (string.IsNullOrEmpty(projectDir) ||
            //    colXaxis == null ||
            //    colYaxis == null)
            //{
            //    return false;
            //}
            if (string.IsNullOrEmpty(projectDir))
            {
                return false;
            }
            if (!CheckColumnCount(colXaxis, colYaxis, colZaxis, colGroup))
            {
                return false;
            }
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            ColumnInfo colXaxis = parameter[1] as ColumnInfo;
            ColumnInfo colYaxis = parameter[2] as ColumnInfo;
            ColumnInfo? colZaxis = parameter[3] as ColumnInfo;
            ColumnInfo? colGroup = parameter[4] as ColumnInfo;
            LoadChartS(projectDir, colXaxis, colYaxis, colZaxis, colGroup);
        }

        #endregion

        #region Private Methods

        private async void LoadChartS(string projectDir, ColumnInfo colXaxis, ColumnInfo colYaxis, ColumnInfo? colZaxis, ColumnInfo? colGroup)
        {
            _relativeChartPopupViewModel.SetProgressSpinner(true, "Chart 로드중...");
            IEnumerable<ChartInfo> chartInfos = await HttpRequest.PostRelativeChart(projectDir, colXaxis, colYaxis, colZaxis, colGroup);
            if (chartInfos != null)
                _relativeChartPopupViewModel.SetCharts(chartInfos);
            _relativeChartPopupViewModel.SetProgressSpinner(false);
        }

        private bool CheckColumnCount(object colX, object colY, object colZ, object colG)
        {
            int nullCount = 0;
            if (colX == null) nullCount++;
            if (colY == null) nullCount++;
            if (colZ == null) nullCount++;
            if (colG == null) nullCount++;

            return nullCount < 3;
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
