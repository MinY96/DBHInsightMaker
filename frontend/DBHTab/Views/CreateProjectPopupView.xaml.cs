using DBHTab.ViewModels;
using System.Text.RegularExpressions;

namespace DBHTab.Views
{
    /// <summary>
    /// CreateProjectPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateProjectPopupView
    {
        public CreateProjectPopupView()
        {
            InitializeComponent();
            DataContext = new CreateProjectPopupViewModel();
        }

        private void TextBox_PreviewTextInput(object sender, System.Windows.Input.TextCompositionEventArgs e)
        {
            // 파일 및 폴더 이름에 사용할 수 없는 문자 목록
            string invalidChars = @"<>:""/\|?*";
            Regex regex = new Regex($"[{Regex.Escape(invalidChars)}]");

            // 입력된 텍스트가 유효한지 확인
            e.Handled = regex.IsMatch(e.Text);
        }
    }
}
