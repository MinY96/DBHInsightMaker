using DBHTab.Commands;
using System.ComponentModel;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace DBHTab.Models
{
    public class ChartInfo
    {
        #region Field Variables
        #endregion

        #region Initialize

        public ChartInfo()
        {
            SaveChartImageCommand = new SaveChartImageCommand();
        }

        #endregion

        #region Properties

        public string ChartName { get; set; } = default!;
        public string ChartDesc { get; set; } = default!;
        public string ChartFileName { get; set; } = default!;
        public string ImageBase64 { get; set; } = default!;
        public byte[] ChartImage { get; set; } = default!;
        public BitmapImage ChartBitmapImage { get; set; }

        #endregion

        #region Commands

        public ICommand SaveChartImageCommand { get; set; }


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
