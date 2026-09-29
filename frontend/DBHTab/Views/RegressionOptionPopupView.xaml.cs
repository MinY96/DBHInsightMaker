using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;
using System.Windows.Input;

namespace DBHTab.Views
{
    /// <summary>
    /// RegressionOptionPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegressionOptionPopupView : Window
    {
        public RegressionOptionPopupView(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            InitializeComponent();
            this.DataContext = new RegressionOptionViewModel(this, projectName, projectDir, columns);
        }

        private void btnMoveForward_Click(object sender, RoutedEventArgs e)
        {
            var selectedItems = lvSourceColumns.SelectedItems.Cast<ColumnInfo>().ToList();
            ((RegressionOptionViewModel)this.DataContext).MoveForwardColumns(selectedItems);
        }

        private void btnMoveBackward_Click(object sender, RoutedEventArgs e)
        {
            var selectedIndep = lvIndepColumns.SelectedItems.Cast<ColumnInfo>().ToList();
            var selectedDep = lvDepColumns.SelectedItems.Cast<ColumnInfo>().ToList();
            ((RegressionOptionViewModel)this.DataContext).MoveBackwardColumns(selectedIndep, selectedDep);
        }

        private void lvRegHistory_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (lvRegHistory.SelectedItem is RegressionProject regProject)
            {
                ((RegressionOptionViewModel)this.DataContext).OpenRegressionResult(regProject);
            }
        }
    }
}
