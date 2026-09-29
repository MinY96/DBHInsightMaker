using DBHTab.ViewModels;
using System.Windows.Navigation;

namespace DBHTab.Pages
{
    /// <summary>
    /// CreateCombiColPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateCombiColPage : ModernWpf.Controls.Page
    {
        public CreateCombiColPage()
        {
            InitializeComponent();
            this.DataContext = new CreateCombiColPageModel();
            InitCalcOption();
        }

        private void InitCalcOption()
        {
            cmbNumericalCombiOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="+", Description="덧셈", Tag="add" },
                new CalcInfo { Symbol="-", Description="뺄셈", Tag="subtract" },
                new CalcInfo { Symbol="×", Description="곱셈", Tag="multiply" },
                new CalcInfo { Symbol="÷", Description="나눗셈", Tag="devide" },
                new CalcInfo { Symbol="Min", Description="둘 중 작은 값", Tag="min" },
                new CalcInfo { Symbol="Max", Description="둘 중 큰 값", Tag="max" },
            };
            cmbCategoricalCombiOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="Concatenate", Description="문자열 붙이기", Tag="concat" },
            };
            cmbDateTimeCombiOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="차이", Description="시간 차이", Tag="diff" },
            };
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            CreateNewColumnPopupViewModel createNewColumnPopupViewModel = e.ExtraData as CreateNewColumnPopupViewModel;
            ((CreateCombiColPageModel)this.DataContext).UpdateData(createNewColumnPopupViewModel);
        }

        private void rdoCombiType_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            var model = (CreateCombiColPageModel)this.DataContext;
            model.SelectedColumnFirst = null;
            model.SelectedColumnSecond = null;
            model.Calc = null;
            int selectedIndex = ((ModernWpf.Controls.RadioButtons)sender).SelectedIndex;
            if (selectedIndex == 0)
                model.SubType = "Numerical";
            else if (selectedIndex == 1)
                model.SubType = "Categorical";
            else if (selectedIndex == 2)
                model.SubType = "DateTime";
        }

        private void rdoTimeDeltaType_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            var model = (CreateCombiColPageModel)this.DataContext;
            int selectedIndex = ((ModernWpf.Controls.RadioButtons)sender).SelectedIndex;
            if (selectedIndex == 0)
                model.TimeDeltaType = "year";
            else if (selectedIndex == 1)
                model.TimeDeltaType = "month";
            else if (selectedIndex == 2)
                model.TimeDeltaType = "day";
            else if (selectedIndex == 3)
                model.TimeDeltaType = "hour";
            else if (selectedIndex == 4)
                model.TimeDeltaType = "minute";
            else if (selectedIndex == 5)
                model.TimeDeltaType = "second";
        }
    }
}
