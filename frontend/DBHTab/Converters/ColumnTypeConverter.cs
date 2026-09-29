using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ColumnTypeConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                string columnType = ((string)value == "Numerical") ? "수치형" : "범주형";
                return columnType;
            }
            return string.Empty;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
