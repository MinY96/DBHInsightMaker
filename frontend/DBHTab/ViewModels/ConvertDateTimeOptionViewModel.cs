using System.Collections.ObjectModel;

namespace DBHTab.ViewModels
{
    public class DateTimeFormatCode
    {
        public string Code { get; set; }
        public string Meaning { get; set; }
        public string Example { get; set; }
    }

    public class DateTimeFormat
    {
        public string Format { get; set; }
        public string Example { get; set; }
    }

    public class ConvertDateTimeOptionViewModel : ViewModelBase
    {
        #region Field Variables

        private ObservableCollection<DateTimeFormatCode> _codeSamples;
        private IList<DateTimeFormat> _originFormat;
        private string _sample;
        private string _selectedFormat;
        private bool _isSelectFormat = false;

        #endregion

        #region Initialize

        public ConvertDateTimeOptionViewModel(string sample)
        {
            _sample = sample;
            LoadSampleCodeData();
            LoadOriginFormat();
        }

        #endregion

        #region Properties

        public ObservableCollection<DateTimeFormatCode> CodeSamples
        {
            get { return _codeSamples; }
            set
            {
                _codeSamples = value;
                OnPropertyChanged();
            }
        }

        public IList<DateTimeFormat> OriginFormats
        {
            get { return _originFormat; }
            set
            {
                _originFormat = value;
                OnPropertyChanged();
            }
        }

        public string Sample
        {
            get { return _sample; }
            set
            {
                _sample = value;
                OnPropertyChanged();
            }
        }

        public string SelectedFormat
        {
            get { return _selectedFormat; }
            set
            {
                _selectedFormat = value;
                IsSelectFormat = !string.IsNullOrEmpty(value);
                OnPropertyChanged();
            }
        }

        public bool IsSelectFormat
        {
            get { return _isSelectFormat; }
            set
            {
                _isSelectFormat = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void UpdateFormat(bool isOrigin, string selectedFormat)
        {
            if (isOrigin)
            {
                SelectedFormat = selectedFormat;
            }
        }

        #endregion

        #region Private Methods

        private void LoadSampleCodeData()
        {
            var samples = new List<DateTimeFormatCode>
            {
                new DateTimeFormatCode {Code="%a", Meaning="요일(약자)", Example="Sun, Mon, Sat"},
                new DateTimeFormatCode {Code="%A", Meaning="요일(전체)", Example="Sunday, Monday"},
                new DateTimeFormatCode {Code="%w", Meaning="요일(숫자) - Sun:0, Mon:1,…", Example="0, 1, …, 6"},
                new DateTimeFormatCode {Code="%d", Meaning="월의 일(2자리)", Example="01, 02, …, 31"},
                new DateTimeFormatCode {Code="%b", Meaning="월(약자)", Example="Jan, Feb, …, Dec"},
                new DateTimeFormatCode {Code="%B", Meaning="월(전체)", Example="January, February"},
                new DateTimeFormatCode {Code="%m", Meaning="월(2자리)",   Example="01, 02, …, 12"},
                new DateTimeFormatCode {Code="%y", Meaning="연도(2자리)", Example="99, 23, 25"},
                new DateTimeFormatCode {Code="%Y", Meaning="연도(전체)", Example="1999, 2023, 2025"},
                new DateTimeFormatCode {Code="%H", Meaning="시각(24시간 - 2자리)", Example="00, 01, …, 23"},
                new DateTimeFormatCode {Code="%h", Meaning="시각(12시간 - 2자리)", Example="01, 02, …, 12"},
                new DateTimeFormatCode {Code="%p", Meaning="AM or PM", Example="AM, PM"},
                new DateTimeFormatCode {Code="%M", Meaning="분(2자리)", Example="00, 01, …, 59"},
                new DateTimeFormatCode {Code="%S", Meaning="초(2자리)", Example="00, 01, …, 59"},
                new DateTimeFormatCode {Code="%f", Meaning="밀리초(6자리)", Example="000000, …, 999999"},
                new DateTimeFormatCode {Code="%j", Meaning="연도의 일(3자리)", Example="001, 002, …, 366"},
                new DateTimeFormatCode {Code="%U", Meaning="주차(일요일 시작 기준)", Example="00, 01, …, 53"},
                new DateTimeFormatCode {Code="%W", Meaning="주차(월요일 시작 기준)", Example="00, 01, …, 53"},
            };
            CodeSamples = new ObservableCollection<DateTimeFormatCode>(samples);
        }

        private void LoadOriginFormat()
        {
            var sample = new List<DateTimeFormat>
            {
                new DateTimeFormat { Format="%Y-%m-%d", Example="2025-08-27" },
                new DateTimeFormat { Format="%Y-%m-%d %H:%M:%S", Example="2025-08-27 08:15:00" },
                new DateTimeFormat { Format="%Y-%m-%d %H:%M:%S.%f", Example="2025-08-27 08:15:13.003026" },
                new DateTimeFormat { Format="%m/%d/%Y", Example="08/27/2025" },
                new DateTimeFormat { Format="%m/%d/%y", Example="08/27/25" },
                new DateTimeFormat { Format="%d/%m/%Y", Example="27/08/2025" },
                new DateTimeFormat { Format="%Y.%m.%d", Example="2025.08.27" },
                new DateTimeFormat { Format="%a, %d %b %Y %H:%M:%S", Example="Wed, 27 Aug 2025 08:15:00" },
                new DateTimeFormat { Format="%a %d %b %Y, %I:%M%p", Example="Wed 27 Aug 2025, 08:15AM" },
                new DateTimeFormat { Format="%Y WW%W", Example="2025 WW35" },
                new DateTimeFormat { Format="%Y년 %m월 %d일", Example="2025년 08월 27일" },
            };
            OriginFormats = sample;
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
