using DBHTab.ViewModels;
using System.Windows.Navigation;

namespace DBHTab.Pages
{
    /// <summary>
    /// CreateRandomColPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateRandomColPage : ModernWpf.Controls.Page
    {
        public CreateRandomColPage()
        {
            InitializeComponent();
            this.DataContext = new CreateRandomColPageModel();
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            CreateNewColumnPopupViewModel createNewColumnPopupViewModel = e.ExtraData as CreateNewColumnPopupViewModel;
            ((CreateRandomColPageModel)this.DataContext).UpdateData(createNewColumnPopupViewModel);
        }
    }
}
