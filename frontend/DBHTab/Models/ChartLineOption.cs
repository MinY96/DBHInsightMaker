using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class ChartLineOption : INotifyPropertyChanged
    {
        private string _axis;
        private string _kind;
        private string _linestyle;
        private string _color = "#000000";
        private string _text = string.Empty;
        private string _textAlignVertical = "center";
        private string _textAlignHorizontal = "center";
        private string _customDateTime;
        private int _lineWidth = 1;
        private int _textRotation = 0;
        private double? _customValue;
        private bool _isCustomValueDouble = true;

        public string Axis
        {
            get { return _axis; }
            set { _axis = value;  OnPropertyChanged(); }
        }

        public string Kind
        {
            get { return _kind; }
            set { _kind = value; OnPropertyChanged(); }
        }

        public int LineWidth
        {
            get { return _lineWidth; }
            set { _lineWidth = value; OnPropertyChanged(); }
        }

        public string LineStyle
        {
            get { return _linestyle; }
            set { _linestyle = value; OnPropertyChanged(); }
        }

        public string Color
        {
            get { return _color; }
            set { _color = value; OnPropertyChanged(); }
        }

        public string Text
        {
            get { return _text; }
            set { _text = value; OnPropertyChanged(); }
        }

        public string TextAlignVertical
        {
            get { return _textAlignVertical; }
            set { _textAlignVertical = value; OnPropertyChanged(); }
        }

        public string TextAlignHorizontal
        {
            get { return _textAlignHorizontal; }
            set { _textAlignHorizontal = value; OnPropertyChanged(); }
        }

        public int TextRotation
        {
            get { return _textRotation; }
            set { _textRotation = value; OnPropertyChanged(); }
        }

        public double? CustomValue
        {
            get { return _customValue; }
            set { _customValue = value; OnPropertyChanged(); }
        }

        public string CustomDateTime
        {
            get { return _customDateTime; }
            set { _customDateTime = value; OnPropertyChanged(); }
        }

        public bool IsCustomValueDouble
        {
            get { return _isCustomValueDouble; }
            set { _isCustomValueDouble = value; OnPropertyChanged(); }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        public void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
