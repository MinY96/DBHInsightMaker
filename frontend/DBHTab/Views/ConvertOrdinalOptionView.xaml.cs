using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;

namespace DBHTab.Views
{
    /// <summary>
    /// ConvertOrdinalOptionView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ConvertOrdinalOptionView
    {
        public ConvertOrdinalOptionView(IEnumerable<UniqueData> uniqueData)
        {
            InitializeComponent();
            this.DataContext = new ConvertOrdinalOptionViewModel(uniqueData);
        }

        private void btnMoveTop_Click(object sender, RoutedEventArgs e)
        {
            if (grdOrder.SelectedItem != null)
            {
                UniqueData? selectedItem = grdOrder.SelectedItem as UniqueData;
                ((ConvertOrdinalOptionViewModel)this.DataContext).MoveToTop(selectedItem);
            }
        }

        private void btnMoveUp_Click(object sender, RoutedEventArgs e)
        {
            if (grdOrder.SelectedItem != null)
            {
                UniqueData? selectedItem = grdOrder.SelectedItem as UniqueData;
                ((ConvertOrdinalOptionViewModel)this.DataContext).MoveUp(selectedItem);
            }
        }

        private void btnMoveDown_Click(object sender, RoutedEventArgs e)
        {
            if (grdOrder.SelectedItem != null)
            {
                UniqueData? selectedItem = grdOrder.SelectedItem as UniqueData;
                ((ConvertOrdinalOptionViewModel)this.DataContext).MoveDown(selectedItem);
            }
        }

        private void btnMoveBottom_Click(object sender, RoutedEventArgs e)
        {
            if (grdOrder.SelectedItem != null)
            {
                UniqueData? selectedItem = grdOrder.SelectedItem as UniqueData;
                ((ConvertOrdinalOptionViewModel)this.DataContext).MoveToBottom(selectedItem);
            }
        }
    }
}
