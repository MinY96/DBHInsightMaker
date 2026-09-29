using DBHTab.Models;
using DBHTab.ViewModels;
using System;
using System.Collections.Generic;
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
using System.Windows.Shapes;

namespace DBHTab.Views
{
    /// <summary>
    /// CustomChartView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CustomChartView : Window
    {
        public CustomChartView(string projectName, string projectDir, IEnumerable<ColumnInfo> columns)
        {
            InitializeComponent();
            this.DataContext = new CustomChartViewModel(this, projectName, projectDir, columns);
        }
    }
}
