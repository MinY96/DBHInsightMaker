using System.ComponentModel;

namespace DBHTab.Models
{
    public class StatTestResultInfo
    {
        #region Field Variables
        #endregion

        #region Initialize
        #endregion

        #region Properties

        public string Result { get; set; } = default!;
        public string Detail { get; set; } = default!;
        public float SignificanceLevel { get; set; } = default!;

        #endregion

        #region Commands
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
