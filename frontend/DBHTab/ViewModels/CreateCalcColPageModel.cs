using DBHTab.Models;
using DBHTab.Pages;

namespace DBHTab.ViewModels
{
    public class CreateCalcColPageModel : CreateColumnPageModelBase
    {
        #region Field Variables

        private CreateNewColumnPopupViewModel _popupViewModel;
        private ColumnInfo _selectedColumn;
        private IList<ColumnInfo> _numColumns;
        private IList<ColumnInfo> _catColumns;
        private CalcInfo _calc;
        private double? _calcValue = double.NaN;
        private string _subType;
        private string _splitText;
        private int? _splitOrder = 1;
        private string _replaceOld;
        private string _replaceNew;
        private string _concatenateText;
        private bool _concatenateOnPrev = true;

        public CreateCalcColPageModel()
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

        public double? CalcValue
        {
            get { return _calcValue; }
            set
            {
                _calcValue = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string SubType
        {
            get { return _subType; }
            set { _subType = value; }
        }

        public string SplitText
        {
            get { return _splitText; }
            set
            {
                _splitText = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public int? SplitOrder
        {
            get { return _splitOrder; }
            set
            {
                _splitOrder = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string ReplaceOld
        {
            get { return _replaceOld; }
            set
            {
                _replaceOld = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string ReplaceNew
        {
            get { return _replaceNew; }
            set
            {
                _replaceNew = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public string ConcatenateText
        {
            get { return _concatenateText; }
            set
            {
                _concatenateText = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public bool ConcatenateOnPrev
        {
            get { return _concatenateOnPrev; }
            set { _concatenateOnPrev = value; OnPropertyChanged(); }
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
                {"MainType", "Calc"},
                {"SubType", SubType},
                {"Column", SelectedColumn.Column},
                {"Symbol", Calc.Tag},
                {"Value", CalcValue},
                {"SplitText", SplitText},
                {"SplitOrder", SplitOrder},
                {"ReplaceOld", ReplaceOld},
                {"ReplaceNew", ReplaceNew},
                {"ConcatenateText", ConcatenateText},
                {"ConcatenateOnPrev", ConcatenateOnPrev},
            };
        }

        public void UpdateData(CreateNewColumnPopupViewModel? createNewColumnPopupViewModel)
        {
            _popupViewModel = createNewColumnPopupViewModel;
            NumericalColumns = _popupViewModel.NumericalColumns;
            CategoricalColumns = _popupViewModel.CategoricalColumns;
        }

        #endregion

        #region Private Methods

        private void CheckCompletePayload()
        {
            IsCompleteOption = false;
            if (SelectedColumn != null & Calc != null)
            {
                if (SubType == "Numerical" & CalcValue != null & !double.IsNaN((double)CalcValue))
                {
                    IsCompleteOption = true;
                }
                else if (SubType == "Categorical")
                {
                    var specialSymbols = new[] { "Split", "Replace", "Concatenate" };
                    if (Calc.Symbol == "Split" & !string.IsNullOrEmpty(SplitText) & SplitOrder != null)
                    {
                        IsCompleteOption = true;
                    }
                    else if (Calc.Symbol == "Replace" & !string.IsNullOrEmpty(ReplaceOld) & !string.IsNullOrEmpty(ReplaceNew))
                    {
                        IsCompleteOption = true;
                    }
                    else if (Calc.Symbol == "Concatenate" & !string.IsNullOrEmpty(ConcatenateText))
                    {
                        IsCompleteOption = true;
                    }
                    else if (!specialSymbols.Contains(Calc.Symbol))
                    {
                        IsCompleteOption = true;
                    }
                }
                else if (SubType == "Function")
                {
                    IsCompleteOption = true;
                }
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
