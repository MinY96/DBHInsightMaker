using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class ChartColumnOption : INotifyPropertyChanged
    {
        private string _column;
        private string _linestyle = "auto";
        private string _marker = "auto";
        private string _label = "auto";
        private string _color = "#000000";
        private int _lineWidth = 1;
        private int _markersize = 1;
        private bool _isSecondAxis = false;

        public string Column
        {
            get { return _column; }
            set { _column = value;  OnPropertyChanged(); }
        }        

        public string LineStyle
        {
            get { return _linestyle; }
            set { _linestyle = value; OnPropertyChanged(); }
        }

        public int LineWidth
        {
            get { return _lineWidth; }
            set { _lineWidth = value; OnPropertyChanged(); }
        }

        public string Marker
        {
            get { return _marker; }
            set { _marker = value; OnPropertyChanged(); }
        }

        public int MarkerSize
        {
            get { return _markersize; }
            set { _markersize = value; OnPropertyChanged(); }
        }
        public string Color
        {
            get { return _color; }
            set { _color = value; OnPropertyChanged(); }
        }

        public string Label
        {
            get { return _label; }
            set { _label = value; OnPropertyChanged(); }
        }

        public bool IsSecondaryAxis
        {
            get { return _isSecondAxis; }
            set { _isSecondAxis = value; OnPropertyChanged(); }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        public void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
