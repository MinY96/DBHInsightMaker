using DBHTab.ViewModels;
using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ContentToOptionCheckConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return false;
            try
            {
                var model = ((ModernWpf.Controls.Page)value).DataContext as CreateColumnPageModelBase;
                return model.IsCompleteOption;
            }
            catch { return false; }
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
