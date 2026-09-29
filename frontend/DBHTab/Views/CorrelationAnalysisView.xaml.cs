using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;
using System.Windows.Controls;

namespace DBHTab.Views
{
    /// <summary>
    /// CorrelationAnalysisView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CorrelationAnalysisView : Window
    {
        public CorrelationAnalysisView(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            InitializeComponent();
            var filteredColumns = columns.Where(c => (c.ColumnChar != "Nominal") && (c.ColumnChar != "DateTime"));
            this.DataContext = new CorrelationAnalysisViewModel(this, projectName, projectDir, filteredColumns);
        }

        private void SampleGrid_GotFocused(object sender, RoutedEventArgs e)
        {
            DataGridCell cell = e.OriginalSource as DataGridCell;
            if (cell != null && cell.Column is DataGridCheckBoxColumn)
            {
                grdCorrVar.BeginEdit();
                CheckBox chkBox = cell.Content as CheckBox;
                if (chkBox != null)
                {
                    chkBox.IsChecked = !chkBox.IsChecked;
                    rdoCorrMethod.Focus();
                }
            }
        }
    }
}
