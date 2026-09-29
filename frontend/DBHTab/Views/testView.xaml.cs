using System.Windows;

namespace DBHTab.Views
{
    /// <summary>
    /// testView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class testView : Window
    {
        public testView()
        {
            InitializeComponent();
            LoadHtmlFile();
        }

        private async Task LoadHtmlFile()
        {
            await webBrowser.EnsureCoreWebView2Async(null);
            string FilePath = @"C:\Users\10007166\Desktop\plot.html";
            webBrowser.CoreWebView2.Navigate(new Uri(FilePath).AbsoluteUri);
        }
    }
}
