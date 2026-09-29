using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class AnalyzeStateConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                bool isWork = (bool)value;
                return !isWork;
            }
            return false;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
