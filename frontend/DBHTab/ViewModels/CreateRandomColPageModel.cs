namespace DBHTab.ViewModels
{
    public class CreateRandomColPageModel : CreateColumnPageModelBase
    {
        #region Field Variables

        private double? _minValue = double.NaN;
        private double? _maxValue = double.NaN;
        private double? _meanValue = 0.00;
        private double? _stdValue = 1.00;
        private bool _isInteger = true;
        private bool _nomalDist = false;
        private CreateNewColumnPopupViewModel _popupViewModel;

        public CreateRandomColPageModel()
        {

        }

        #endregion

        #region Initialize
        #endregion

        #region Properties

        public double? MinValue
        {
            get { return _minValue; }
            set
            {
                _minValue = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public double? MaxValue
        {
            get { return _maxValue; }
            set
            {
                _maxValue = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public double? MeanValue
        {
            get { return _meanValue; }
            set
            {
                _meanValue = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public double? StdValue
        {
            get { return _stdValue; }
            set
            {
                _stdValue = value;
                CheckCompletePayload();
                OnPropertyChanged();
            }
        }

        public bool IsInteger
        {
            get { return _isInteger; }
            set
            {
                _isInteger = value;
                OnPropertyChanged();
            }
        }

        public bool SetNormalDist
        {
            get { return _nomalDist; }
            set
            {
                _nomalDist = value;
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
                {"MainType","Random" },
                {"SubType",string.Empty},
                {"MinValue",MinValue},
                {"MaxValue",MaxValue},
                {"IsInteger",IsInteger},
                {"SetNormalDist",SetNormalDist},
                {"MeanValue",MeanValue},
                {"StdValue",StdValue},
            };
        }

        public void UpdateData(CreateNewColumnPopupViewModel? createNewColumnPopupViewModel)
        {
            _popupViewModel = createNewColumnPopupViewModel;
        }

        #endregion

        #region Private Methods

        private void CheckCompletePayload()
        {
            if (MinValue != null & MaxValue != null & !double.IsNaN((double)MinValue) & !double.IsNaN((double)MaxValue) & MinValue < MaxValue)
            {
                if (SetNormalDist)
                {
                    if (MeanValue == null | StdValue == null)
                        IsCompleteOption = false;
                    else if (double.IsNaN((double)MeanValue) || double.IsNaN((double)StdValue))
                    {
                        IsCompleteOption = false;
                    }
                    else if (MinValue > MeanValue || MaxValue < MeanValue)
                    {
                        IsCompleteOption = false;
                    }
                    else
                    {
                        IsCompleteOption = true;
                    }
                }
                else
                {
                    IsCompleteOption = true;
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
