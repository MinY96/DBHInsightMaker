using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ChartOptionStringToNullableDoubleConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
            {
                return null;
            }
            var s = value.ToString()?.Trim();

            if (string.IsNullOrEmpty(s) || s.Equals("auto", StringComparison.OrdinalIgnoreCase))
            {
                return null;
            }

            if (double.TryParse(s, NumberStyles.Any, culture, out var d))
                return (double?)d;

            if (double.TryParse(s, NumberStyles.Any, CultureInfo.InvariantCulture, out var d2))
                return (double?)d2;

            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null || value == DependencyProperty.UnsetValue)
                return "auto";

            double? d = null;

            if (value is double dd)
                d = dd;
            else if (value is double?)
                d = (double?)value;

            if (value is string s)
                return s;

            if (parameter is string format && !string.IsNullOrWhiteSpace(format))
                return d.Value.ToString(format, CultureInfo.InvariantCulture);

            return d.Value.ToString(CultureInfo.InvariantCulture);
        }
    }
}
