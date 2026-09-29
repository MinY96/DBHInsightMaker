using DBHTab.Models;
using DBHTab.ViewModels;
using Microsoft.Win32;
using System.Collections.ObjectModel;

namespace DBHTab.Commands
{
    public class SetFilePathCommand : CommandBase
    {
        #region Field Variables

        private LoadDataPopupViewModel _loadDataPopupViewModel;

        #endregion

        #region Initialize

        public SetFilePathCommand(LoadDataPopupViewModel loadDataPopupViewModel)
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

        public override bool CanExecute(object? parameter)
        {
            return true;
        }

        public override void Execute(object? parameter)
        {
            bool isCsv = (bool)parameter;
            SetFilePathAsync(isCsv);
        }

        #endregion

        #region Private Methods

        private async Task SetFilePathAsync(bool isCsv)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            string title = isCsv ? "CSV 파일 선택" : "Excel 파일 선택";
            string filter = isCsv ? "CSV Files (*.csv)|*.csv" : "Excel Files|*.xls;*.xlsx;*.xlsm|All Files|*.*";
            openFileDialog.Filter = filter;
            openFileDialog.Title = title;
            if (openFileDialog.ShowDialog() == true)
            {
                string selectedFilePath = openFileDialog.FileName;
                if (!isCsv)
                {
                    IEnumerable<string> sheets = await HttpRequest.GetExcelSheetsAsync(selectedFilePath);
                    _loadDataPopupViewModel.SheetS = new ObservableCollection<string>(sheets);

                }
                _loadDataPopupViewModel.SetFilePath(selectedFilePath);
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
