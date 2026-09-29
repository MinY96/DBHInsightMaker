using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ChartOptionStringToComboBoxItemConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is null)
                return null;
            if (value is string)
                if (value == "auto")
                    return null;
                return value;
            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is null)
                return "auto";
            if (value is ComboBoxItem)
                return ((ComboBoxItem)value).Content.ToString();
            return null;
        }
    }
}
