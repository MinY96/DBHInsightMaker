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
    public class ChartOptionStringToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return null;

            var s = value.ToString()?.Trim();

            if (string.IsNullOrEmpty(s) || s.Equals("auto", StringComparison.OrdinalIgnoreCase))
                return null;

            try
            {
                string red = s.Substring(1, 2);
                string green = s.Substring(3, 2);
                string blue = s.Substring(5, 2);
                string alpha = s.Substring(7, 2);
                var colorObj = ColorConverter.ConvertFromString($"#{alpha}{red}{green}{blue}");
                if (colorObj is Color c)
                    return c;
            }
            catch
            {

            }
            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value == null)
                return "auto";
            if (value is Color c)
            {
                string argb = c.ToString();
                string alpha = argb.Substring(1, 2);
                string red = argb.Substring(3, 2);
                string green = argb.Substring(5, 2);
                string blue = argb.Substring(7, 2);
                return $"#{red}{green}{blue}{alpha}";
            }
            return "auto";
        }
    }
}
