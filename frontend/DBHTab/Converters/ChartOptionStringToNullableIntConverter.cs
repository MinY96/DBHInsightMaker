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
    public class ChartOptionStringToNullableIntConverter : IValueConverter
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

            if (int.TryParse(s, out var result))
                return result;

            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return "auto";
            if (value is int i)
                return i.ToString();
            if (value is int?)
            {
                var n = (int?) value;
                return n.HasValue ? n.Value.ToString() : "auto";
            }
            return "auto";
        }
    }
}
