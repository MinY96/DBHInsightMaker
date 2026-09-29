using DBHTab.ViewModels;
using System.Windows.Navigation;

namespace DBHTab.Pages
{
    /// <summary>
    /// CreateOutlierColPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateOutlierColPage : ModernWpf.Controls.Page
    {
        public CreateOutlierColPage()
        {
            InitializeComponent();
            this.DataContext = new CreateOutlierColPageModel();
            InitCalcOption();
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            CreateNewColumnPopupViewModel createNewColumnPopupViewModel = e.ExtraData as CreateNewColumnPopupViewModel;
            ((CreateOutlierColPageModel)this.DataContext).UpdateData(createNewColumnPopupViewModel);
        }

        private void InitCalcOption()
        {
            cmbReplaceOutlierMethod.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="공백", Description="공백(N/A)으로 대체", Tag="na" },
                new CalcInfo { Symbol="평균", Description="평균으로 대체", Tag="mean" },
                new CalcInfo { Symbol="중앙값", Description="중앙값으로 대체", Tag="median" },
                new CalcInfo { Symbol="이전 값", Description="이상치 이전 값으로 대체", Tag="prev" },
                new CalcInfo { Symbol="이후 값", Description="이상치 다음 값으로 대체", Tag="next" },
                new CalcInfo { Symbol="최빈값", Description="가장 많이 발생한 값으로 대체", Tag="mode" },
                new CalcInfo { Symbol="선형 보간", Description="이상치 전,후 값 선형 보간값으로 대체", Tag="linear" },
                new CalcInfo { Symbol="지정 값", Description="지정한 값으로 대체", Tag="fix" },
            };
        }

        private void rdoOutlierType_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            var model = (CreateOutlierColPageModel)this.DataContext;
            model.SelectedColumn = null;
            int selectedIndex = ((ModernWpf.Controls.RadioButtons)sender).SelectedIndex;
            if (selectedIndex == 0)
                model.SubType = "Sigma";
            else if (selectedIndex == 1)
                model.SubType = "IQR";
        }
    }
}
