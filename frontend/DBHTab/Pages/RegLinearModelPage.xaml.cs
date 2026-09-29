using DBHTab.UserControls;
using DBHTab.ViewModels;
using DBHTab.Views;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace DBHTab.Pages
{
    /// <summary>
    /// RegLinearModelPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegLinearModelPage : ModernWpf.Controls.Page
    {
        #region Field Variables
        #endregion

        #region Initialize

        public RegLinearModelPage(string pageDir)
        {
            InitializeComponent();
            this.DataContext = new RegLinearModelPageModel(pageDir);
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
        #endregion

        #region Protected Methods
        #endregion

        private void RegDescribe_Button_Click(object sender, RoutedEventArgs e)
        {
            Window owner = Window.GetWindow(this);
            BitmapImage bitmap = new BitmapImage(new Uri("pack://application:,,,/Resources/regression_describe.png"));
            GlossaryView popup = new GlossaryView("선형 회귀 모델", bitmap)
            {
                Owner = owner
            };
            popup.ShowDialog();
        }

        private void RegMetrics_Button_Click(object sender, RoutedEventArgs e)
        {
            Window owner = Window.GetWindow(this);
            BitmapImage bitmap = new BitmapImage(new Uri("pack://application:,,,/Resources/regression_metrics.png"));
            GlossaryView popup = new GlossaryView("회귀 모델 지표 설명", bitmap)
            {
                Owner = owner
            };
            popup.ShowDialog();
        }
    }
}
