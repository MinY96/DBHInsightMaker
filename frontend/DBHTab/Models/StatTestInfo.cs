using System.ComponentModel;

namespace DBHTab.Models
{
    public class StatTestInfo
    {
        #region Field Variables
        #endregion

        #region Initialize
        #endregion

        #region Properties

        public string Method { get; set; } = default!;
        public string Purpose { get; set; } = default!;
        public string BestCase { get; set; } = default!;
        public string Strength { get; set; } = default!;
        public string Weakness { get; set; } = default!;
        public List<StatTestResultInfo> Results { get; set; } = default!;

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
