using DBHTab.Models;
using DBHTab.ViewModels;
using DBHTab.Views;
using Newtonsoft.Json.Linq;
using System.IO;

namespace DBHTab.Commands
{
    public class LoadRegressionResultCommand : CommandBase
    {
        #region Field Variables

        private RegressionOptionViewModel _regressionOptionViewModel;
        private RegressionOptionPopupView _optionView;

        #endregion

        #region Initialize

        public LoadRegressionResultCommand(RegressionOptionViewModel regressionOptionViewModel, RegressionOptionPopupView viewOption)
        {
            _regressionOptionViewModel = regressionOptionViewModel;
            _optionView = viewOption;
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
            if (parameter.Length != 8)
            {
                return false;
            }
            IEnumerable<ColumnInfo> indepColumns = parameter[1] as IEnumerable<ColumnInfo>;
            IEnumerable<ColumnInfo> depColumns = parameter[2] as IEnumerable<ColumnInfo>;
            if (indepColumns == null || depColumns == null)
                return false;
            if (indepColumns.Count() == 0 || depColumns.Count() > 1)
                return false;

            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            IEnumerable<ColumnInfo> indepColumns = parameter[1] as IEnumerable<ColumnInfo>;
            IEnumerable<ColumnInfo> depColumns = parameter[2] as IEnumerable<ColumnInfo>;
            int selectionMethodIndex = (int)parameter[3];
            int scalerMethodIndex = (int)parameter[4];
            int imputeMethodIndex = (int)parameter[5];
            bool isSplit = (bool)parameter[6];
            int testRatio = (int)parameter[7];

            string? selectionMethod = ConvertToSelectionMethod(selectionMethodIndex);
            string? scalerMethod = ConvertToScalerMethod(scalerMethodIndex);
            string? imputeMethod = ConvertToImputeMethod(imputeMethodIndex);
            float testRatioF = testRatio / 100.0f;
            LoadRegressionDir(projectDir, indepColumns, depColumns, selectionMethod, scalerMethod, imputeMethod, isSplit, testRatioF);
        }

        #endregion

        #region Private Methods

        private string? ConvertToSelectionMethod(int methodIndex)
        {
            string? selectionMethod = null;
            switch (methodIndex)
            {
                case 0:
                    selectionMethod = null;
                    break;
                case 1:
                    selectionMethod = "forward";
                    break;
                case 2:
                    selectionMethod = "backward";
                    break;
                case 3:
                    selectionMethod = "stepwise";
                    break;
            }
            return selectionMethod;
        }

        private string? ConvertToScalerMethod(int methodIndex)
        {
            string? scalerMethod = null;
            switch (methodIndex)
            {
                case 0:
                    scalerMethod = null;
                    break;
                case 1:
                    scalerMethod = "standard";
                    break;
                case 2:
                    scalerMethod = "minmax";
                    break;
                case 3:
                    scalerMethod = "maxabs";
                    break;
                case 4:
                    scalerMethod = "robust";
                    break;
            }
            return scalerMethod;
        }

        private string? ConvertToImputeMethod(int methodIndex)
        {
            string? imputeMethod = null;
            switch (methodIndex)
            {
                case 0:
                    imputeMethod = "remove";
                    break;
                case 1:
                    imputeMethod = "mean";
                    break;
                case 2:
                    imputeMethod = "median";
                    break;
                case 3:
                    imputeMethod = "mode";
                    break;
                case 4:
                    imputeMethod = "linear";
                    break;
            }
            return imputeMethod;
        }

        private async void LoadRegressionDir(
            string? projectDir,
            IEnumerable<ColumnInfo>? indepColumns, IEnumerable<ColumnInfo>? depColumns,
            string? selectionMethod, string? scalerMethod, string? imputeMethod,
            bool isSplit, float testRatio)
        {
            _regressionOptionViewModel.SetProgressSpinner(true, "회귀분석 진행중...");
            string regDir = await HttpRequest.PostRegressionResult(projectDir, indepColumns, depColumns,
                selectionMethod, scalerMethod, imputeMethod, isSplit, testRatio);
            _regressionOptionViewModel.SetProgressSpinner(false);

            if (Path.Exists(regDir))
            {
                string infoPath = Path.Combine(regDir, "Info.json");
                if (!File.Exists(infoPath))
                    return;

                string json = File.ReadAllText(infoPath);
                var jObj = JObject.Parse(json);
                _regressionOptionViewModel.RegressionDir = regDir;
                _regressionOptionViewModel.ModelType = jObj["ModelType"].ToString();
                _optionView.Close();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
