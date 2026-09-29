using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ChartOptionStringToNullableBoolConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return false;

            var s = value.ToString()?.Trim().ToLowerInvariant();
            if (string.IsNullOrEmpty(s) || s == "auto")
                return false;
            if (s == "true" || s == "1" || s == "y" || s == "yes" || s == "True")
                return true;
            if (s == "false" || s == "0" || s == "n" || s == "no" || s == "False")
                return false;
            return false;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return "auto";

            if (value is bool b)
                return b ? "true" : "false";

            if (value is bool?)
            {
                var n = (bool?)value;
                if (!n.HasValue)
                    return "auto";

                return n.Value ? "true" : "false";
            }

            return "auto";
        }
    }
}
