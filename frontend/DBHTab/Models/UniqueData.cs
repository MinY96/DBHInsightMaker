using System.ComponentModel;

namespace DBHTab.Models
{
    public class UniqueData : INotifyPropertyChanged
    {
        private string _value;
        private int _rank = 1;

        public string Value
        {
            get => _value;
            set
            {
                _value = value;
                OnPropertyChanged(nameof(Value));
            }
        }

        public int Rank
        {
            get => _rank;
            set
            {
                _rank = value;
                OnPropertyChanged(nameof(Rank));
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
