using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class ConvertDataTypePopupViewModel : ViewModelBase
    {
        #region Field Variables

        private ConvertDataTypePopupView _convertDataTypePopupView;
        private ColumnInfo _columnInfo;
        private ObservableCollection<string> _beforeData;
        private ObservableCollection<string> _afterData;
        private IEnumerable<string> _orderInfo;
        private string _projectDir;
        private string _loadMsg = string.Empty;
        private string _dtFormat = string.Empty;
        private bool _isLoad = false;
        private bool _enableNominal = false;
        private bool _enableOrdinal = false;
        private bool _enableContinuous = false;
        private bool _enableDiscrete = false;
        private bool _enableDateTime = false;
        private bool _saveMode = false;

        #endregion

        #region Initialize

        public ConvertDataTypePopupViewModel(ConvertDataTypePopupView convertDataTypePopupView,
            string projectDir, ColumnInfo columnInfo, IEnumerable<string> columnData)
        {
            _convertDataTypePopupView = convertDataTypePopupView;
            _projectDir = projectDir;
            _columnInfo = columnInfo;
            _beforeData = new ObservableCollection<string>(columnData);
            ConvertDataTypeCommand = new ConvertDataTypeCommand(this);
            InitButtonEnable(columnInfo.ColumnChar);
        }

        #endregion

        #region Properties

        public string ProjectDir
        {
            get { return _projectDir; }
            set { _projectDir = value; }
        }

        public string ColumnName
        {
            get { return (_columnInfo != null) ? _columnInfo.Column : string.Empty; }
        }

        public string ColumnChar
        {
            get { return _columnInfo.ColumnChar; }
        }

        public string ConvertTo { get; set; }

        public bool IsLoad
        {
            get { return _isLoad; }
            set
            {
                _isLoad = value;
                OnPropertyChanged();
            }
        }

        public string LoadingMessage
        {
            get { return _loadMsg; }
            set
            {
                _loadMsg = value;
                OnPropertyChanged();
            }
        }

        public string DateTimeFormat
        {
            get { return _dtFormat; }
            set
            {
                _dtFormat = value;
                OnPropertyChanged();
            }
        }

        public int UniqueCount
        {
            get { return _columnInfo.UniqueCount; }
        }

        public IEnumerable<string> OrderInfo
        {
            get { return _orderInfo; }
            set
            {
                _orderInfo = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<string> BeforeData
        {
            get { return _beforeData; }
            set
            {
                _beforeData = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<string> AfterData
        {
            get { return _afterData; }
            set
            {
                _afterData = value;
                SaveMode = (value != null) ? true : false;
                OnPropertyChanged();
            }
        }

        public bool EnableNominal
        {
            get { return _enableNominal; }
            set { _enableNominal = value; OnPropertyChanged(); }
        }

        public bool EnableOrdinal
        {
            get { return _enableOrdinal; }
            set { _enableOrdinal = value; OnPropertyChanged(); }
        }

        public bool EnableContinuous
        {
            get { return _enableContinuous; }
            set { _enableContinuous = value; OnPropertyChanged(); }
        }

        public bool EnableDiscrete
        {
            get { return _enableDiscrete; }
            set { _enableDiscrete = value; OnPropertyChanged(); }
        }

        public bool EnableDateTime
        {
            get { return _enableDateTime; }
            set { _enableDateTime = value; OnPropertyChanged(); }
        }

        public bool SaveMode
        {
            get { return _saveMode; }
            set { _saveMode = value; OnPropertyChanged(); }
        }

        #endregion

        #region Commands

        public ICommand ConvertDataTypeCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void SetProgressSpinner(bool isProgress, string progressMessage = "")
        {
            IsLoad = isProgress;
            LoadingMessage = progressMessage;
        }

        public void ViewConvertDataType()
        {
            SaveMode = false;
            ConvertDataTypeCommand.Execute(this);
        }

        public void UpdateProjectMainView()
        {
            _convertDataTypePopupView.DialogResult = true;
            _convertDataTypePopupView.Close();
        }

        #endregion

        #region Private Methods

        private void InitButtonEnable(string columnChar)
        {
            switch (columnChar)
            {
                case "Continuous":
                    EnableDiscrete = true;
                    EnableNominal = true;
                    break;
                case "Discrete":
                    EnableContinuous = true;
                    EnableNominal = true;
                    EnableOrdinal = true;
                    break;
                case "Nominal":
                    EnableContinuous = true;
                    EnableDiscrete = true;
                    EnableOrdinal = true;
                    EnableDateTime = true;
                    break;
                case "Ordinal":
                    EnableDiscrete = true;
                    EnableNominal = true;
                    break;
                case "DateTime":
                    EnableNominal = true;
                    break;
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
