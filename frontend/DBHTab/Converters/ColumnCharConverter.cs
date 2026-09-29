using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ColumnCharConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value != null)
            {
                string columChar = (string)value;
                if (columChar == "Discrete")
                    return "이산형";
                if (columChar == "Continuous")
                    return "연속형";
                if (columChar == "Nominal")
                    return "명목형";
                if (columChar == "Ordinal")
                    return "순서형";
                if (columChar == "DateTime")
                    return "DateTime";

                return string.Empty;
            }
            return string.Empty;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
