using DBHTab.Models;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
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


namespace DBHTab.UserControls
{
    /// <summary>
    /// LinesOption.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class LinesOption : UserControl
    {
        public LinesOption()
        {
            InitializeComponent();
        }

        public ObservableCollection<ChartLineOption> Lines
        {
            get => (ObservableCollection<ChartLineOption>)GetValue(LinesProperty);
            set => SetValue(LinesProperty, value);
        }
        public static readonly DependencyProperty LinesProperty =
            DependencyProperty.Register(
                name: nameof(Lines),
                propertyType: typeof(ObservableCollection<ChartLineOption>),
                ownerType: typeof(LinesOption),
                new PropertyMetadata(null));

        private void AddLine_Click(object sender, RoutedEventArgs e)
        {
            if (Lines == null)
            {
                //return;
                Lines = new ObservableCollection<ChartLineOption>();
            }
            Lines.Add(new ChartLineOption());
        }

        private void RemoveButton_Click(object sender, RoutedEventArgs e)
        {
            if (Lines == null)
            {
                return;
            }
            if (sender is Button btn && btn.DataContext is ChartLineOption line)
            {
                if (Lines.Contains(line))
                    Lines.Remove(line);
            }
        }
    }
}
