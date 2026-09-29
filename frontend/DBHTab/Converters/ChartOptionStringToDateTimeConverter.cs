using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;
using System.Windows.Media;

namespace DBHTab.Converters
{
    public class ChartOptionStringToDateTimeConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return null;

            var s = value.ToString()?.Trim();

            if (string.IsNullOrEmpty(s) || s.Equals("auto", StringComparison.OrdinalIgnoreCase))
                return null;

            if (parameter is string format && !string.IsNullOrWhiteSpace(format))
            {
                if (DateTime.TryParseExact(s, format, culture, DateTimeStyles.None, out var dtExact))
                    return (DateTime?)dtExact;
            }

            if (DateTime.TryParse(s, culture, DateTimeStyles.AssumeLocal, out var dt))
                return (DateTime?)dt;

            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return null;
            DateTime? dt = null;

            if (value is DateTime d)
                dt = d;
            else if (value is DateTime?)
                dt = (DateTime?)value;

            if (dt == null)
                return null;

            if (parameter is string format && !string.IsNullOrWhiteSpace(format))
                return dt.Value.ToString(format, culture);

            return dt.Value.ToString("yyyy-MM-dd HH:mm:ss", culture);
        }
    }
}
