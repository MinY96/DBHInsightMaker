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
    public partial class AddColumnOption : UserControl
    {
        public AddColumnOption()
        {
            InitializeComponent();
        }

        public ObservableCollection<ChartColumnOption> AddedColumns
        {
            get => (ObservableCollection<ChartColumnOption>)GetValue(AddedColumnsProperty);
            set => SetValue(AddedColumnsProperty, value);
        }
        public static readonly DependencyProperty AddedColumnsProperty =
            DependencyProperty.Register(
                name: nameof(AddedColumns),
                propertyType: typeof(ObservableCollection<ChartColumnOption>),
                ownerType: typeof(AddColumnOption),
                new PropertyMetadata(null));

        public List<string> Columns
        {
            get => (List<string>)GetValue(ColumnsProperty);
            set => SetValue(ColumnsProperty, value);
        }
        public static readonly DependencyProperty ColumnsProperty = 
            DependencyProperty.Register(
                name: nameof(Columns),
                propertyType: typeof(List<string>),
                ownerType: typeof(AddColumnOption),
                new PropertyMetadata(null));

        private void AddColumn_Click(object sender, RoutedEventArgs e)
        {
            if (AddedColumns == null)
            {
                AddedColumns = new ObservableCollection<ChartColumnOption>();
            }
            AddedColumns.Add(new ChartColumnOption());
        }

        private void RemoveColumn_Click(object sender, RoutedEventArgs e)
        {
            if (AddedColumns == null)
            {
                return;
            }
            if (sender is Button btn && btn.DataContext is ChartColumnOption column)
            {
                if (AddedColumns.Contains(column))
                    AddedColumns.Remove(column);
            }
        }
    }
}
