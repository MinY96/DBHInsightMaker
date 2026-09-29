using DBHTab.Models;
using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class LoadDataCommand : CommandBase
    {
        #region Field Variables

        private LoadDataPopupViewModel _loadDataPopupViewModel;

        #endregion

        #region Initialize

        public LoadDataCommand(LoadDataPopupViewModel loadDataPopupViewModel)
        {
            _loadDataPopupViewModel = loadDataPopupViewModel;
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
            //var parameter = (object[])parameters;
            //if (parameter == null)
            //{
            //    return false;
            //}
            //if (parameter.Length != 3)
            //{
            //    return false;
            //}
            //bool? isCsv = parameter[0] as bool?;
            //string filePath = parameter[1] as string;
            //string sheetName = parameter[2] as string;

            //if (string.IsNullOrEmpty(filePath) || filePath=="-")
            //{
            //    return false;
            //}
            //if (!(bool)isCsv & string.IsNullOrEmpty(sheetName))
            //{
            //    return false;
            //}
            return true;
        }

        public override void Execute(object? parameter)
        {
            LoadData();
        }

        #endregion

        #region Private Methods

        private void LoadData()
        {
            _loadDataPopupViewModel.LoadData();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
