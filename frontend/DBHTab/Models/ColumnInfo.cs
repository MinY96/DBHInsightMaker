using DBHTab.Commands;
using System.ComponentModel;
using System.Windows.Input;

namespace DBHTab.Models
{
    public class ColumnInfo : INotifyPropertyChanged
    {
        #region Field Variables
        #endregion

        #region Initialize

        public ColumnInfo()
        {
            PopupColumnChartCommand = new PopupColumnChartCommand();
            PopupNomalityTestCommand = new PopupNormalityTestCommand();
            PopupConvertTypeCommand = new PopupConvertTypeCommand();
            PopupDeleteColumnCommand = new PopupDeleteColumnCommand();
        }

        #endregion

        #region Properties

        public string Column { get; set; } = default!;
        public string ColumnType { get; set; } = default!;
        public string ColumnChar { get; set; } = default!;
        public int DataCount { get; set; } = default!;
        public int MissingCount { get; set; } = default!;
        public float? MissingRatio { get; set; }
        public string? Mean { get; set; }
        public string? Std { get; set; }
        public string? Min { get; set; }
        public string? Max { get; set; }
        public string? Median { get; set; }
        public string? Q1 { get; set; }
        public string? Q3 { get; set; }
        public string Mode { get; set; } = default!;
        public int UniqueCount { get; set; } = default!;
        public bool IsEnabled { get; set; } = true;
        public bool IsChecked { get; set; } = false;

        #endregion

        #region Commands
        public ICommand PopupColumnChartCommand { get; set; }
        public ICommand PopupNomalityTestCommand { get; set; }
        public ICommand PopupConvertTypeCommand { get; set; }
        public ICommand PopupDeleteColumnCommand { get; set; }

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
}
