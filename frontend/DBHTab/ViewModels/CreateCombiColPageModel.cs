using DBHTab.Models;
using DBHTab.Pages;

namespace DBHTab.ViewModels
{
    public class CreateCombiColPageModel : CreateColumnPageModelBase
    {
        #region Field Variables

        private CreateNewColumnPopupViewModel _popupViewModel;
        private ColumnInfo _selectedColumnFirst;
        private ColumnInfo _selectedColumnSecond;
        private IList<ColumnInfo> _numColumns;
        private IList<ColumnInfo> _catColumns;
        private IList<ColumnInfo> _dtColumns;
        private CalcInfo _calc;
        private string _subType;
        private string _timeDeltaType = "year";

        public CreateCombiColPageModel()
        {

        }

        #endregion

        #region Initialize
        #endregion

        #region Properties

        public IList<ColumnInfo> NumericalColumns
        {
            get { return _numColumns; }
            set { _numColumns = value; OnPropertyChanged(); }
        }

        public IList<ColumnInfo> CategoricalColumns
        {
            get { return _catColumns; }
            set { _catColumns = value; OnPropertyChanged(); }
        }

        public IList<ColumnInfo> DateTimeColumns
        {
            get { return _dtColumns; }
            set { _dtColumns = value; OnPropertyChanged(); }
        }

        public ColumnInfo SelectedColumnFirst
        {
            get { return _selectedColumnFirst; }
            set
            {
                _selectedColumnFirst = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public ColumnInfo SelectedColumnSecond
        {
            get { return _selectedColumnSecond; }
            set
            {
                _selectedColumnSecond = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public CalcInfo Calc
        {
            get { return _calc; }
            set
            {
                _calc = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string SubType
        {
            get { return _subType; }
            set { _subType = value; }
        }

        public string TimeDeltaType
        {
            get { return _timeDeltaType; }
            set { _timeDeltaType = value; }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public override Dictionary<string, object> Payload()
        {
            return new Dictionary<string, object>
            {
                {"MainType","Combi" },
                {"SubType",SubType},
                {"ColumnFirst",SelectedColumnFirst.Column},
                {"ColumnSecond",SelectedColumnSecond.Column},
                {"Symbol",Calc.Tag},
                {"TimeDeltaType",TimeDeltaType},
            };
        }

        public void UpdateData(CreateNewColumnPopupViewModel? createNewColumnPopupViewModel)
        {
            _popupViewModel = createNewColumnPopupViewModel;
            NumericalColumns = _popupViewModel.NumericalColumns;
            CategoricalColumns = _popupViewModel.CategoricalColumns;
            DateTimeColumns = _popupViewModel.DateTimeColumns;
        }

        #endregion

        #region Private Methods

        private void CheckCompletePayload()
        {
            IsCompleteOption = false;
            if (SelectedColumnFirst != null & Calc != null & SelectedColumnSecond != null)
            {
                IsCompleteOption = true;
            }
            if (_popupViewModel != null)
            {
                _popupViewModel.IsCompleteOption = IsCompleteOption;
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
