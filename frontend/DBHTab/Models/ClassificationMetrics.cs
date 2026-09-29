using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class ClassificationMetrics : INotifyPropertyChanged
    {
        public int TN { get; set; }
        public int TP { get; set; }
        public int FN { get; set; }
        public int FP { get; set; }
        public double Threshold { get; set; }
        public double AUC { get; set; }
        public double Accuracy { get; set; }
        public double Recall { get; set; }
        public double Precision { get; set; }
        public double F1Score { get; set; }
        public double Specificity { get; set; }
        public double FPR { get; set; }
        public double NPV { get; set; }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
