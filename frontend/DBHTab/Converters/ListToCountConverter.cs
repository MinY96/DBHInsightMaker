using System.Collections;
using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ListToCountConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                return ((ICollection)value).Count;
            }
            return 0;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
