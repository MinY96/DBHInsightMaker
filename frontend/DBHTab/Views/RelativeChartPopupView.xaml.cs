using DBHTab.Models;
using DBHTab.ViewModels;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Input;

namespace DBHTab.Views
{
    /// <summary>
    /// RelativeChartPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RelativeChartPopupView : Window
    {
        public RelativeChartPopupView(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            InitializeComponent();
            this.DataContext = new RelativeChartPopupViewModel(this, projectName, projectDir, columns);
        }

        private void ChartName_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            // 파일 및 폴더 이름에 사용할 수 없는 문자 목록
            string invalidChars = @"<>:""/\|?*";
            Regex regex = new Regex($"[{Regex.Escape(invalidChars)}]");

            // 입력된 텍스트가 유효한지 확인
            e.Handled = regex.IsMatch(e.Text);
        }

        private void ClearXButton_Click(object sender, RoutedEventArgs e)
        {
            cmbXAxisColumn.SelectedItem = null;
        }

        private void ClearYButton_Click(object sender, RoutedEventArgs e)
        {
            cmbYAxisColumn.SelectedItem = null;
        }

        private void ClearZButton_Click(object sender, RoutedEventArgs e)
        {
            cmbZAxisColumn.SelectedItem = null;
        }

        private void ClearGButton_Click(object sender, RoutedEventArgs e)
        {
            cmbGroupColumn.SelectedItem = null;
        }
    }
}
