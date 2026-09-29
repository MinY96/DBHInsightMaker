using DBHTab.Models;
using Microsoft.Win32;
using System.Windows;

namespace DBHTab.Commands
{
    public class SaveDataToExcelCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public SaveDataToExcelCommand()
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
            if (parameter[0] == DependencyProperty.UnsetValue || parameter[1] == DependencyProperty.UnsetValue || parameter[2] == DependencyProperty.UnsetValue)
            {
                return false;
            }
            string projectDir = parameter[0] as string;
            bool isRaw = (bool)parameter[1];
            IEnumerable<ColumnInfo>? columns = parameter[2] as IEnumerable<ColumnInfo>;
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
            bool isRaw = (bool)parameter[1];
            SaveDataToExcelAsync(projectDir, isRaw);
        }

        #endregion

        #region Private Methods

        private async Task SaveDataToExcelAsync(string projectDir, bool isRaw)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Excel file (*.xlsx)|*.xlsx";
            if (saveFileDialog.ShowDialog() == true)
            {
                bool isRemove = await HttpRequest.PostSaveAsExcel(projectDir, saveFileDialog.FileName, isRaw);
                if (isRemove)
                {
                    await ModernWpf.MessageBox.ShowAsync("Excel 파일이 저장되었습니다.");
                }
                else
                {
                    await ModernWpf.MessageBox.ShowAsync("파일 저장 에러", "에러", MessageBoxButton.OK, MessageBoxImage.Error, MessageBoxResult.OK);
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
