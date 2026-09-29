using DBHTab.Models;
using DBHTab.Pages;

namespace DBHTab.ViewModels
{
    public class CreateOutlierColPageModel : CreateColumnPageModelBase
    {
        #region Field Variables

        private CreateNewColumnPopupViewModel _popupViewModel;
        private ColumnInfo _selectedColumn;
        private IList<ColumnInfo> _numColumns;
        private CalcInfo _calc;
        private string _subType;
        private int? _sigmaLevel = 3;
        private double? _replaceValue = double.NaN;

        public CreateOutlierColPageModel()
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

        public int? SigmaLevel
        {
            get { return _sigmaLevel; }
            set
            {
                _sigmaLevel = value;
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

        public double? ReplaceFixValue
        {
            get { return _replaceValue; }
            set
            {
                _replaceValue = value;
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
            string ReplaceValue = string.Empty;
            if (Calc.Symbol == "공백")
                ReplaceValue = null;
            else if (Calc.Symbol == "평균")
                ReplaceValue = SelectedColumn.Mean;
            else if (Calc.Symbol == "중앙값")
                ReplaceValue = SelectedColumn.Median;
            else if (Calc.Symbol == "최빈값")
                ReplaceValue = SelectedColumn.Mode;
            else if (Calc.Symbol == "지정 값")
                ReplaceValue = ReplaceFixValue.ToString();

            return new Dictionary<string, object>
            {
                {"MainType","Outlier" },
                {"SubType",SubType},
                {"Column",SelectedColumn.Column},
                {"Mean",SelectedColumn.Mean},
                {"Std",SelectedColumn.Std},
                {"Q1",SelectedColumn.Q1},
                {"Q3",SelectedColumn.Q3},
                {"SigmaLevel",SigmaLevel},
                {"ReplaceMethod",Calc.Tag},
                {"ReplaceValue",ReplaceValue},
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
            IsCompleteOption = true;
            if (SelectedColumn != null & Calc != null)
            {
                if (SubType == "Sigma" & SigmaLevel == null)
                {
                    IsCompleteOption = false;
                }
                if (Calc.Symbol == "지정 값" & double.IsNaN((double)ReplaceFixValue))
                {
                    IsCompleteOption = false;
                }
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
