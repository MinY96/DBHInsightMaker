using DBHTab.ViewModels;
using System.Windows.Navigation;

namespace DBHTab.Pages
{
    /// <summary>
    /// CreateConvertColPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateConvertColPage : ModernWpf.Controls.Page
    {
        public CreateConvertColPage()
        {
            InitializeComponent();
            this.DataContext = new CreateConvertColPageModel();
            InitCalcOption();
        }

        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            base.OnNavigatedTo(e);
            CreateNewColumnPopupViewModel createNewColumnPopupViewModel = e.ExtraData as CreateNewColumnPopupViewModel;
            ((CreateConvertColPageModel)this.DataContext).UpdateData(createNewColumnPopupViewModel);
        }

        private void InitCalcOption()
        {
            cmbNormalizeConverter.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="Box-Cox 변환", Description="(양수 데이터) 비대칭적인 분포를 정규분포에 가깝게 변환", Tag="boxcox" },
                new CalcInfo { Symbol="Yeo-Jonson 변환", Description="음수를 포함한 데이터 정규 분포 변환 기법", Tag="yeojohnson" },
                new CalcInfo { Symbol="로그 변환", Tag="log",
                    Description="(양수 데이터-비율/지수적으로 증가하는 데이터) 분포가 오른쪽으로 치우쳐 있을 때 효과적" },
                new CalcInfo { Symbol="제곱근 변환", Tag="sqrt", Description="(양수 데이터-카운트 데이터) 분포가 오른쪽으로 치우쳐 있을 때 효과적" },
                new CalcInfo { Symbol="역수 변환", Tag="reciprocal", Description="(양수 데이터) 분포가 왼쪽으로 치우쳐 있을 때 효과적" },
            };
            cmbScalerConverter.ItemsSource = new List<CalcInfo>
            {
                new CalcInfo { Symbol="Min-Max Scaler", Description="모든 데이터를 0~1 사이로 변환", Tag="minmax" },
                new CalcInfo { Symbol="Standard Scaler", Description="Z-Score 표준화 (평균 0, 분산 1)", Tag="standard" },
                new CalcInfo { Symbol="MaxAbs Scaler", Description="최대 절대값 기준 스케일링 (최대절대값 → 1)", Tag="maxabs" },
                new CalcInfo { Symbol="Robust Saler", Description="중앙값과 IQR을 사용한 스케일링, 이상치 영향 최소화", Tag="robust" },
            };
        }

        private void rdoConvertType_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            var model = (CreateConvertColPageModel)this.DataContext;
            model.SelectedColumn = null;
            model.Calc = null;
            int selectedIndex = ((ModernWpf.Controls.RadioButtons)sender).SelectedIndex;
            if (selectedIndex == 0)
                model.SubType = "NormalDist";
            else if (selectedIndex == 1)
                model.SubType = "Scaler";
        }
    }
}
