using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.RightsManagement;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace DBHTab.Models
{
    public class OptionTemplateSelector : DataTemplateSelector
    {
        public DataTemplate TextBoxTemplate { get; set; }
        public DataTemplate ComboBoxTemplate { get; set; }
        public DataTemplate CheckBoxTemplate { get; set; }
        public DataTemplate IntegerUpDownTemplate { get; set; }
        public DataTemplate DoubleUpDownTemplate { get; set; }
        public DataTemplate DateTimePickerTemplate { get; set; }
        public DataTemplate ColorPickerTemplate { get; set; }
        public DataTemplate LinesTemplate { get; set; }
        public DataTemplate AddColumnTemplate { get; set; }
        public override DataTemplate SelectTemplate(object item, DependencyObject container)
        {
            if (item is ChartOption opt)
            {
                return opt.Control switch
                {
                    "ComboBox" => ComboBoxTemplate,
                    "CheckBox" => CheckBoxTemplate,
                    "IntegerUpDown" => IntegerUpDownTemplate,
                    "DoubleUpDown" => DoubleUpDownTemplate,
                    "DateTimePicker" => DateTimePickerTemplate,
                    "ColorPicker" => ColorPickerTemplate,
                    "TextBox" => TextBoxTemplate,
                    "LinesOption" => LinesTemplate,
                    "AddColumnOption" => AddColumnTemplate,
                    _ => TextBoxTemplate,
                };
            }
            return base.SelectTemplate(item, container);
        }
    }
}
