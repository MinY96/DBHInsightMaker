using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;
using System.Windows.Controls;

namespace DBHTab.Views
{
    /// <summary>
    /// NormalityTestPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class NormalityTestPopupView : Window
    {
        public NormalityTestPopupView(string projectDir, ColumnInfo columnInfo)
        {
            InitializeComponent();
            this.DataContext = new NormalityTestPopupViewModel(this, projectDir, columnInfo);
        }

        private void NormalityMethod_Changed(object sender, SelectionChangedEventArgs e)
        {
            ((NormalityTestPopupViewModel)this.DataContext).UpdateResult();
        }

        private void cmbSignificanceLevel_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (this.DataContext != null)
            {
                ((NormalityTestPopupViewModel)this.DataContext).UpdateResult();
            }
        }
    }
}
