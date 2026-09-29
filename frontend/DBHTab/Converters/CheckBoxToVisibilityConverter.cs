using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class CheckBoxToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                bool isCheck = (bool)value;
                if (isCheck)
                {
                    return Visibility.Visible;
                }
                return Visibility.Hidden;
            }
            return Visibility.Visible;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
