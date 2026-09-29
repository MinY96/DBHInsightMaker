using System.Globalization;
using System.Windows.Data;

namespace DBHTab.Converters
{
    public class ComboBoxItemEnabledConverter : IMultiValueConverter
    {
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            var currentItem = values[0];
            var selectedItem1 = values[1];
            var selectedItem2 = values[2];
            var selectedItem3 = values[3];
            var selectedItem4 = values[4];

            if (currentItem == null) return true;
            if (Equals(currentItem, selectedItem1) ||
                Equals(currentItem, selectedItem2) ||
                Equals(currentItem, selectedItem3) ||
                Equals(currentItem, selectedItem4))
                return false;
            return true;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
