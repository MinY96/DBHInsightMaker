using DBHTab.ViewModels;
using System.Windows.Controls;
using System.Windows.Navigation;

namespace DBHTab.Pages
{
    /// <summary>
    /// CreateRandomColPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public class CalcInfo
    {
        public string Symbol { get; set; } = string.Empty;
        public string Tag { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
    }

    public partial class CreateCalcColPage : ModernWpf.Controls.Page
    {
        #region Field Variables                
        #endregion

        #region Initialize

        public CreateCalcColPage()
        {
            InitializeComponent();
            this.DataContext = new CreateCalcColPageModel();
            InitCalcOption();
        }

        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events      
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods

        private void InitCalcOption()
        {
            cmbNumericalOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="+", Description="덧셈", Tag="add"},
                new CalcInfo { Symbol="-", Description="뺄셈", Tag="subtract"},
                new CalcInfo { Symbol="×", Description="곱셈", Tag="multiply" },
                new CalcInfo { Symbol="÷", Description="나눗셈", Tag="devide" },
                new CalcInfo { Symbol="n제곱", Description="거듭제곱", Tag="power"},
            };
            cmbCategoricalOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="Upper", Description="대문자화", Tag="upper"},
                new CalcInfo { Symbol="Lower", Description="소문자화", Tag="lower"},
                new CalcInfo { Symbol="Capitalize", Description="첫글자 대문자", Tag="capital"},
                new CalcInfo { Symbol="Strip", Description="양쪽 공백 제거", Tag="strip"},
                new CalcInfo { Symbol="Split", Description="문자열 자르기", Tag="split"},
                new CalcInfo { Symbol="Replace", Description="문자열 대체", Tag="replace"},
                new CalcInfo { Symbol="Concatenate", Description="문자열 붙이기", Tag="concat"},
            };
            cmbFunctionOption.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="Abs", Description="절대값 함수", Tag="abs"},
                new CalcInfo { Symbol="Sqrt", Description="제곱근 함수", Tag="root"},
                new CalcInfo { Symbol="Log", Description="로그 함수", Tag="log"},
                new CalcInfo { Symbol="Exp", Description="지수 함수", Tag="exp"},
                new CalcInfo { Symbol="Sin", Description="Sin 함수", Tag="sin"},
                new CalcInfo { Symbol="Cos", Description="Cos 함수", Tag="cos"},
            };
        }

        #endregion

        #region Protected Methods

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            CreateNewColumnPopupViewModel createNewColumnPopupViewModel = e.ExtraData as CreateNewColumnPopupViewModel;
            ((CreateCalcColPageModel)this.DataContext).UpdateData(createNewColumnPopupViewModel);
        }

        #endregion

        private void rdoCalcType_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            var model = (CreateCalcColPageModel)this.DataContext;
            model.SelectedColumn = null;
            model.Calc = null;
            int selectedIndex = ((ModernWpf.Controls.RadioButtons)sender).SelectedIndex;
            if (selectedIndex == 0)
                model.SubType = "Numerical";
            else if (selectedIndex == 1)
                model.SubType = "Categorical";
            else if (selectedIndex == 2)
                model.SubType = "Function";
        }
    }
}
