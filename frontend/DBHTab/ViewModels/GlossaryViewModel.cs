using DBHTab.Commands;
using DBHTab.Models;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace DBHTab.ViewModels
{
    public class GlossaryViewModel : ViewModelBase
    {
        #region Field Variables

        private string _title = string.Empty;
        BitmapImage _image;

        #endregion

        #region Initialize

        public GlossaryViewModel(string title, BitmapImage image)
        {
            _title = title;
            _image = image;
        }

        #endregion

        #region Properties

        public string Title
        {
            get { return _title; }
            set
            {
                _title = value;
                OnPropertyChanged();
            }
        }

        public BitmapImage GlossaryImg
        {
            get { return _image; }
            set
            {
                _image = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        #endregion
    }
}
