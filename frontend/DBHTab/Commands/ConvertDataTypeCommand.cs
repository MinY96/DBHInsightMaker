using DBHTab.Models;
using DBHTab.ViewModels;
using System.Collections.ObjectModel;

namespace DBHTab.Commands
{
    public class ConvertDataTypeCommand : CommandBase
    {
        #region Field Variables

        private ConvertDataTypePopupViewModel _convertDataTypePopupViewModel;

        #endregion

        #region Initialize

        public ConvertDataTypeCommand(ConvertDataTypePopupViewModel convertDataTypePopupViewModel)
        {
            _convertDataTypePopupViewModel = convertDataTypePopupViewModel;
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
            if (parameter == null)
                return false;

            bool saveMode = (bool)parameter;
            return saveMode;
        }

        public override void Execute(object? parameter)
        {
            string projectDir = _convertDataTypePopupViewModel.ProjectDir;
            string columnName = _convertDataTypePopupViewModel.ColumnName;
            string convertTo = _convertDataTypePopupViewModel.ConvertTo;
            string datetimeFormat = _convertDataTypePopupViewModel.DateTimeFormat;
            IEnumerable<string> orders = _convertDataTypePopupViewModel.OrderInfo;
            bool saveMode = _convertDataTypePopupViewModel.SaveMode;
            ConvertDataType(projectDir, columnName, convertTo, datetimeFormat, orders, saveMode);
        }

        #endregion

        #region Private Methods

        private async void ConvertDataType(string projectDir, string columnName, string convertTo, string datetimeFormat, IEnumerable<string> orders, bool saveMode)
        {
            _convertDataTypePopupViewModel.SetProgressSpinner(true, $"{convertTo} (으)로 변환 중...");
            if (saveMode)
            {
                bool isConvert = await HttpRequest.PostConvertType(projectDir, columnName, convertTo, datetimeFormat, orders);
                if (isConvert)
                {
                    _convertDataTypePopupViewModel.UpdateProjectMainView();
                }
            }
            else
            {
                IEnumerable<string>? convertData = await HttpRequest.PostConvertTypeTest(
                    projectDir, columnName, convertTo, datetimeFormat, orders);
                if (convertData != null)
                    _convertDataTypePopupViewModel.AfterData = new ObservableCollection<string>(convertData);
            }
            _convertDataTypePopupViewModel.SetProgressSpinner(false);
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
