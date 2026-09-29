using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class DateTimeToStringConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                DateTime dtCreateDate = (DateTime)value;
                string formattedDate = dtCreateDate.ToString("yyyy-MM-dd");
                return formattedDate;
            }
            return string.Empty;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
