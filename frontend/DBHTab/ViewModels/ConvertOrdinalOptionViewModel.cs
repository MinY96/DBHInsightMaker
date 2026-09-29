using DBHTab.Models;
using System.Collections.ObjectModel;

namespace DBHTab.ViewModels
{
    public class ConvertOrdinalOptionViewModel : ViewModelBase
    {
        #region Field Variables

        private ObservableCollection<UniqueData> _orderInfo;

        #endregion

        #region Initialize

        public ConvertOrdinalOptionViewModel(IEnumerable<UniqueData> orderInfo)
        {
            _orderInfo = new ObservableCollection<UniqueData>(orderInfo);
            UpdateRanks();
        }

        #endregion

        #region Properties

        public ObservableCollection<UniqueData> OrderInfo
        {
            get { return _orderInfo; }
            set
            {
                _orderInfo = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void MoveToTop(UniqueData selectedItem)
        {
            if (OrderInfo != null && OrderInfo.Contains(selectedItem))
            {
                OrderInfo.Move(OrderInfo.IndexOf(selectedItem), 0);
                UpdateRanks();
            }
        }

        public void MoveUp(UniqueData selectedItem)
        {
            if (OrderInfo != null && OrderInfo.Contains(selectedItem))
            {
                int index = OrderInfo.IndexOf(selectedItem);
                if (index > 0)
                {
                    OrderInfo.Move(index, index - 1);
                    UpdateRanks();
                }
            }
        }

        public void MoveDown(UniqueData selectedItem)
        {
            if (OrderInfo != null && OrderInfo.Contains(selectedItem))
            {
                int index = OrderInfo.IndexOf(selectedItem);
                if (index < OrderInfo.Count - 1)
                {
                    OrderInfo.Move(index, index + 1);
                    UpdateRanks();
                }
            }
        }

        public void MoveToBottom(UniqueData selectedItem)
        {
            if (OrderInfo != null && OrderInfo.Contains(selectedItem))
            {
                OrderInfo.Move(OrderInfo.IndexOf(selectedItem), OrderInfo.Count - 1);
                UpdateRanks();
            }
        }

        #endregion

        #region Private Methods

        private void UpdateRanks()
        {
            if (OrderInfo != null)
            {
                for (int i = 0; i < OrderInfo.Count; i++)
                {
                    OrderInfo[i].Rank = i + 1; // Rank는 1부터 시작
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
