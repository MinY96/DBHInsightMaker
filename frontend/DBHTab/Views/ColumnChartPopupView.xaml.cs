using DBHTab.Models;
using DBHTab.ViewModels;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Input;

namespace DBHTab.Views
{
    /// <summary>
    /// ColumnChartPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ColumnChartPopupView : Window
    {
        public ColumnChartPopupView(string projectDir, ColumnInfo columnInfo)
        {
            InitializeComponent();
            this.DataContext = new ColumnChartPopupViewModel(this, projectDir, columnInfo);
        }

        private void ChartFileName_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            // 파일 및 폴더 이름에 사용할 수 없는 문자 목록
            string invalidChars = @"<>:""/\|?*";
            Regex regex = new Regex($"[{Regex.Escape(invalidChars)}]");

            // 입력된 텍스트가 유효한지 확인
            e.Handled = regex.IsMatch(e.Text);
        }
    }
}
