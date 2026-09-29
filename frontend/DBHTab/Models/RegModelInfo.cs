using DBHTab.Commands;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace DBHTab.Models
{
    public class RegModelInfo : INotifyPropertyChanged
    {
        #region Field Variables
        #endregion

        #region Initialize

        public RegModelInfo()
        {

        }

        #endregion

        #region Properties

        public string ModelType { get; set; } = string.Empty;
        public string RegEquation { get; set; } = string.Empty;
        public int DataSize { get; set; } = default!;
        public double DataRatio { get; set; } = default!;
        public int IndepValCount { get; set; } = default!;
        public double Statistic { get; set; } = default!;
        public double PValue { get; set; } = default!;
        public double LLF { get; set; } = default!;
        public double AIC { get; set; } = default!;
        public double BIC { get; set; } = default!;

        #endregion

        #region Commands

        #endregion

        #region Public Events

        public event PropertyChangedEventHandler? PropertyChanged;

        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion
    }
}
