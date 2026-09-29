using DBHTab.Models;
using DBHTab.ViewModels;
using ModernWpf.Controls;
using System.Windows;
using System.Windows.Controls;

namespace DBHTab.Views
{
    /// <summary>
    /// ConvertDataTypePopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ConvertDataTypePopupView : Window
    {
        public ConvertDataTypePopupView(string projectDir, ColumnInfo columnInfo, IEnumerable<string> columnData)
        {
            InitializeComponent();
            this.DataContext = new ConvertDataTypePopupViewModel(this, projectDir, columnInfo, columnData);
        }

        private async void ConvertToDateTime_Click(object sender, RoutedEventArgs e)
        {
            ConvertDataTypePopupViewModel model = ((ConvertDataTypePopupViewModel)this.DataContext);
            string sample = model.BeforeData.First();
            var popup = new ConvertDateTimeOptionView(sample);
            var result = await popup.ShowAsync();

            if (result == ContentDialogResult.Primary)
            {
                model.DateTimeFormat = ((ConvertDateTimeOptionViewModel)popup.DataContext).SelectedFormat;
                model.ConvertTo = "DateTime";
                model.ViewConvertDataType();
            }
        }

        private async void ConvertToOrdinal_Click(object sender, RoutedEventArgs e)
        {
            ConvertDataTypePopupViewModel model = ((ConvertDataTypePopupViewModel)this.DataContext);
            IEnumerable<UniqueData> uniqueData = await HttpRequest.PostColumnUnique(model.ProjectDir, model.ColumnName);

            var popup = new ConvertOrdinalOptionView(uniqueData);
            var result = await popup.ShowAsync();

            if (result == ContentDialogResult.Primary)
            {
                model.OrderInfo = (((ConvertOrdinalOptionViewModel)popup.DataContext).OrderInfo).Select(x => x.Value);
                model.ConvertTo = "Ordinal";
                model.ViewConvertDataType();
            }
        }

        private void ConvertType_Click(object sender, RoutedEventArgs e)
        {
            string content = ((Button)sender).Content.ToString();
            if (ModernWpf.MessageBox.Show($"데이터 Type을 {content}(으)로 변경하시겠습니까?", "데이터 타입 변환", MessageBoxButton.YesNo) == MessageBoxResult.No)
                return;
            ConvertDataTypePopupViewModel model = ((ConvertDataTypePopupViewModel)this.DataContext);
            string convertType = "Continuous";
            if (content == "이산형")
                convertType = "Discrete";
            else if (content == "명목형")
                convertType = "Nominal";
            model.ConvertTo = convertType;
            model.ViewConvertDataType();
        }
    }
}
