using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace DBHTab.Models
{
    public class ChartOption : INotifyPropertyChanged
    {
        #region Field Variables
        
        private string _value;
        private ObservableCollection<ChartLineOption> _lines;
        private ObservableCollection<ChartColumnOption> _addedColumns;

        #endregion

        #region Properties
        public string Key { get; set; }
        public string Type { get; set; }
        public string Name { get; set; }
        public string Control {  get; set; }
        public List<string> Option { get; set; }
        public int? Min { get; set; }
        public int? Max { get; set; }
        public double? MinDouble { get; set; }
        public double? MaxDouble { get; set; }
        public int? Paddingleft { get; set; } = 0;
        public Thickness ControlPadding { get; set; }
        public string Value
        {
            get {  return _value; }
            set
            {
                if (_value != value)
                {
                    _value = value;
                    OnPropertyChanged(nameof(Value));
                }
            }
        }

        public ObservableCollection<ChartLineOption> LinesOption
        { 
            get { return _lines; }
            set
            {
                if (_lines != value)
                {
                    _lines = value;
                    OnPropertyChanged(nameof(LinesOption));
                }
            }
        }

        public ObservableCollection<ChartColumnOption> AddedColumnOptions
        {
            get { return _addedColumns; }
            set
            {
                if (_addedColumns != value)
                {
                    _addedColumns = value;
                    OnPropertyChanged(nameof(AddedColumnOptions));
                }
            }
        }

        #endregion

        #region Public Events

        public event PropertyChangedEventHandler? PropertyChanged;

        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion
    }

    public class ChartOptionsResponse
    {
        public string ChartGroup { get; set; }
        public string ChartType { get; set; }
        public string Description { get; set; }
        public List<ChartOption> Options { get; set; }
    }
}
