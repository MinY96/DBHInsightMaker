using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class FileTypeToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                bool isCsv = (bool)value;
                if (isCsv)
                {
                    return Visibility.Hidden;
                }
                return Visibility.Visible;
            }
            return Visibility.Visible;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
