
using DBHTab.Models;
using DBHTab.Pages;

namespace DBHTab.ViewModels
{
    public class CreateConvertColPageModel : CreateColumnPageModelBase
    {
        #region Field Variables

        private CreateNewColumnPopupViewModel _popupViewModel;
        private ColumnInfo _selectedColumn;
        private IList<ColumnInfo> _numColumns;
        private CalcInfo _calc;
        private string _subType;

        public CreateConvertColPageModel()
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

        public ColumnInfo SelectedColumn
        {
            get { return _selectedColumn; }
            set
            {
                _selectedColumn = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string SubType
        {
            get { return _subType; }
            set { _subType = value; }
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
                {"MainType","Convert" },
                {"SubType",SubType},
                {"Column",SelectedColumn.Column},
                {"ConvertMethod",Calc.Tag},
            };
        }

        public void UpdateData(CreateNewColumnPopupViewModel? createNewColumnPopupViewModel)
        {
            _popupViewModel = createNewColumnPopupViewModel;
            NumericalColumns = _popupViewModel.NumericalColumns;
        }

        #endregion

        #region Private Methods

        private void CheckCompletePayload()
        {
            if (SelectedColumn != null & Calc != null)
            {
                IsCompleteOption = true;
            }
            else
            {
                IsCompleteOption = false;
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
