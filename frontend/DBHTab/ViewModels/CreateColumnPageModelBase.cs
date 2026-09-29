using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace DBHTab.ViewModels
{
    public class CreateColumnPageModelBase : INotifyPropertyChanged
    {
        private bool _isComplete = false;
        public event PropertyChangedEventHandler? PropertyChanged;

        public void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public bool IsCompleteOption
        {
            get { return _isComplete; }
            set
            {
                _isComplete = value;
                OnPropertyChanged();
            }
        }

        public virtual Dictionary<string, object> Payload()
        {
            return null;
        }
    }
}
