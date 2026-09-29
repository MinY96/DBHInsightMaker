using DBHTab.ViewModels;

namespace DBHTab.Views
{
    /// <summary>
    /// LoadDataPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class LoadDataPopupView
    {
        public LoadDataPopupView(ProjectMainViewModel projectMainViewModel)
        {
            InitializeComponent();
            DataContext = new LoadDataPopupViewModel(projectMainViewModel);
        }
    }
}
