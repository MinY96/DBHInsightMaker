using System.ComponentModel;

namespace DBHTab.Models
{
    public class ProjectInfo : INotifyPropertyChanged
    {
        #region Field Variables
        #endregion

        #region Initialize
        #endregion

        #region Properties

        public string ProjectName { get; set; } = default!;
        public string ProjectDesc { get; set; } = default!;
        public string ProjectDir { get; set; } = default!;
        public DateTime CreateTime { get; set; } = default(DateTime)!;
        public bool IsLoadData { get; set; } = false;
        public string FileName { get; set; } = default!;
        public string FileExtension { get; set; } = default!;
        public string SheetName { get; set; } = default!;
        public float FileSize { get; set; } = default!;
        public int Rows { get; set; } = default!;
        public int Cols { get; set; } = default!;

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
