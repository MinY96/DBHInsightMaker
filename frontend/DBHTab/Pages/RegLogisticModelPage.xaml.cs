using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DBHTab.ViewModels;
using DBHTab.Views;
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
    /// RegLogisticModelPage.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RegLogisticModelPage : ModernWpf.Controls.Page
    {
        public RegLogisticModelPage(string pageDir)
        {
            InitializeComponent();
            this.DataContext = new RegLogisticModelPageModel(pageDir);
        }

        private void LogisticDesc_Clicked(object sender, RoutedEventArgs e)
        {
            BitmapImage bitmap = new BitmapImage(new Uri("pack://application:,,,/Resources/classification_confusion_matrix.png"));
            Window owner = Window.GetWindow(this);
            GlossaryView popup = new GlossaryView(" Confusion Matrix 정의", bitmap)
            {
                Owner = owner,
            };
            popup.ShowDialog();
        }

        private void Logictic_Metrics_Clicked(object sender, RoutedEventArgs e)
        {            
            BitmapImage bitmap = new BitmapImage(new Uri("pack://application:,,,/Resources/classification_metrics.png"));
            Window owner = Window.GetWindow(this);
            GlossaryView popup = new GlossaryView("로지스틱 회귀 모델 평가 지표", bitmap)
            {
                Owner = owner
            };
            popup.ShowDialog();
        }
    }
}
