using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Windows.Input;

namespace DBHTab.ViewModels
{
    public class CreateNewColumnPopupViewModel : ViewModelBase
    {
        #region Field Variables

        private bool _isCompleteOption = false;
        private bool _completeOption = false;
        private string _projectDir;
        private string _newColumnName;
        private IList<ColumnInfo> _columns;
        private IList<ColumnInfo> _numericalColumns;
        private IList<ColumnInfo> _categoricalColumns;
        private IList<ColumnInfo> _dtColumns;
        private ProjectMainView _mainView;

        #endregion

        #region Initialize

        public CreateNewColumnPopupViewModel(string projectDir, IEnumerable<ColumnInfo> columns, ProjectMainView mainView)
        {
            CreateNewColumnCommand = new CreateNewColumnCommand();
            _projectDir = projectDir;
            _mainView = mainView;
            _columns = (IList<ColumnInfo>?)columns;
            _numericalColumns = columns.Where(c => c.ColumnChar == "Continuous" | c.ColumnChar == "Discrete").ToList();
            _categoricalColumns = columns.Where(c => c.ColumnChar == "Nominal").ToList();
            _dtColumns = columns.Where(c => c.ColumnChar == "DateTime").ToList();
        }

        #endregion

        #region Properties

        public string NewColumnName
        {
            get { return _newColumnName; }
            set
            {
                if (Columns.Where(x => x.Column == value).Count() > 0)
                {
                    _newColumnName = string.Empty;
                    CompleteOption = IsCompleteOption & !string.IsNullOrEmpty(_newColumnName);
                    throw new ArgumentException($"{value} 은(는) 이미 존재하는 컬럼명입니다.");
                }
                _newColumnName = value;
                CompleteOption = IsCompleteOption & !string.IsNullOrEmpty(_newColumnName);
                OnPropertyChanged();
            }
        }

        public bool IsCompleteOption
        {
            get { return _isCompleteOption; }
            set
            {
                _isCompleteOption = value;
                CompleteOption = _isCompleteOption & !string.IsNullOrEmpty(NewColumnName);
                OnPropertyChanged();
            }
        }

        public bool CompleteOption
        {
            get { return _completeOption; }
            set
            {
                _completeOption = value;
                OnPropertyChanged();
            }
        }

        public IList<ColumnInfo> Columns
        {
            get { return _columns; }
            set { _columns = value; OnPropertyChanged(); }
        }

        public IList<ColumnInfo> NumericalColumns
        {
            get { return _numericalColumns; }
            set { _numericalColumns = value; OnPropertyChanged(); }
        }

        public IList<ColumnInfo> CategoricalColumns
        {
            get { return _categoricalColumns; }
            set { _categoricalColumns = value; OnPropertyChanged(); }
        }

        public IList<ColumnInfo> DateTimeColumns
        {
            get { return _dtColumns; }
            set { _dtColumns = value; OnPropertyChanged(); }
        }

        public string ProjectDir
        {
            get { return _projectDir; }
            set { _projectDir = value; OnPropertyChanged(); }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events

        public ICommand CreateNewColumnCommand { get; set; }

        #endregion

        #region Public Methods

        public void UpdateMainViewProgressState(bool isProgress, string message)
        {
            ((ProjectMainViewModel)_mainView.DataContext).SetProgressSpinner(isProgress, message);
        }

        public async void UpdateMainViewProject()
        {
            await ((ProjectMainViewModel)_mainView.DataContext).InitDataInfoAsync();
        }

        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods
        #endregion
    }
}
