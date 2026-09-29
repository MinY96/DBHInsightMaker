using DBHTab.Commands;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class LoadDataPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private bool _isCsv = true;
        private bool _isEnableLoadFile = false;
        private string _filePath = "-";
        private string _sheetName = string.Empty;
        private ObservableCollection<string> _sheets = new ObservableCollection<string>();
        private ProjectMainViewModel _projectMainViewModel;

        #endregion

        #region Initialize

        public LoadDataPopupViewModel(ProjectMainViewModel projectMainViewModel)
        {
            _projectMainViewModel = projectMainViewModel;
            InitCommands();
        }

        #endregion

        #region Properties

        public bool IsCsv
        {
            get { return _isCsv; }
            set
            {
                _isCsv = value;
                ResetFileInfo();
                //CheckEnablePrimaryButton();
                OnPropertyChanged();
            }
        }

        public bool IsEnableLoadFile
        {
            get { return _isEnableLoadFile; }
            set
            {
                _isEnableLoadFile = value;
                OnPropertyChanged();
            }
        }

        public string FilePath
        {
            get { return _filePath; }
            set
            {
                _filePath = value;
                CheckEnablePrimaryButton();
                //IsEnableLoadFile = !string.IsNullOrEmpty(_filePath) && _filePath != "-";
                OnPropertyChanged();
            }
        }

        public string SheetName
        {
            get { return _sheetName; }
            set
            {
                _sheetName = value;
                CheckEnablePrimaryButton();
                OnPropertyChanged();
            }
        }

        public ObservableCollection<string> SheetS
        {
            get { return _sheets; }
            set
            {
                _sheets = value;
                CheckEnablePrimaryButton();
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand LoadDataCommand { get; set; }
        public ICommand SetFilePathCommand { get; set; }

        #endregion

        #region Public Methods

        public void SetFilePath(string filePath)
        {
            FilePath = filePath;
        }

        public void LoadData()
        {
            _projectMainViewModel.LoadDataAsync(IsCsv, SheetName, FilePath);
        }

        #endregion

        #region Private Methods

        private void InitCommands()
        {
            LoadDataCommand = new LoadDataCommand(this);
            SetFilePathCommand = new SetFilePathCommand(this);
        }

        private void ResetFileInfo()
        {
            SheetName = string.Empty;
            FilePath = "-";
        }

        private void CheckEnablePrimaryButton()
        {
            if (_isCsv)
            {
                if (string.IsNullOrEmpty(FilePath) | FilePath == "-")
                {
                    IsEnableLoadFile = false;
                }
                else
                {
                    IsEnableLoadFile = true;
                }
            }
            else
            {
                if (string.IsNullOrEmpty(FilePath) | FilePath == "-" | string.IsNullOrEmpty(SheetName))
                {
                    IsEnableLoadFile = false;
                }
                else
                {
                    IsEnableLoadFile = true;
                }
            }
        }

        #endregion
    }
}
