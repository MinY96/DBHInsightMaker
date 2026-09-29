using DBHTab.ViewModels;
using System.Windows;
using System.Windows.Controls;

namespace DBHTab.Views
{
    /// <summary>
    /// ConvertDateTimeOptionView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ConvertDateTimeOptionView
    {
        public ConvertDateTimeOptionView(string sample)
        {
            InitializeComponent();
            DataContext = new ConvertDateTimeOptionViewModel(sample);
        }

        private void OriginFormat_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            bool isOrigin = cmbOriginFormat.IsEnabled;
            string selectedFormat = ((DateTimeFormat)cmbOriginFormat.SelectedItem).Format;
            ((ConvertDateTimeOptionViewModel)this.DataContext).UpdateFormat(isOrigin, selectedFormat);
        }

        private void OriginFormat_EnabledChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            if (cmbOriginFormat.SelectedItem != null)
            {
                bool isOrigin = cmbOriginFormat.IsEnabled;
                string selectedFormat = string.Empty;
                if (isOrigin)
                {
                    selectedFormat = ((DateTimeFormat)cmbOriginFormat.SelectedItem).Format;
                    ((ConvertDateTimeOptionViewModel)this.DataContext).UpdateFormat(isOrigin, selectedFormat);
                }
                else
                {
                    if (string.IsNullOrEmpty(txtUserFormat.Text))
                    {
                        ((ConvertDateTimeOptionViewModel)this.DataContext).UpdateFormat(true, string.Empty);
                    }
                }
            }
        }
    }
}
