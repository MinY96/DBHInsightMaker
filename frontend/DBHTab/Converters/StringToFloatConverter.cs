using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class StringToFloatConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return null;
            try
            {
                double fValue = (double)value;
                return fValue.ToString("F2");
            }
            catch
            {
                return null;
            }
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return null;
            try
            {
                double fValue = (double)value;
                return fValue.ToString("F2");
            }
            catch
            {
                return null;
            }
        }
    }
}
