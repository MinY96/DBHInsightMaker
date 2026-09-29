using DBHTab.Commands;
using DBHTab.Models;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace DBHTab.UserControls
{
    /// <summary>
    /// ucChartViewer.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ucChartViewer : UserControl, INotifyPropertyChanged
    {
        #region Field Variables

        private ChartInfo _currentChartInfo;
        private int _currentIndex = -1;
        private string _pageInfo = "-";

        #endregion

        #region Initialize

        public ucChartViewer()
        {
            InitializeComponent();
            SaveChartImageCommand = new SaveChartImageCommand();
        }

        #endregion

        #region Properties

        public IList<ChartInfo> ChartInfos
        {
            get => (IList<ChartInfo>)GetValue(ChartInfosProperty);
            set => SetValue(ChartInfosProperty, value);
        }

        public static readonly DependencyProperty ChartInfosProperty = DependencyProperty.Register(
            nameof(ChartInfos),
            typeof(IList<ChartInfo>),
            typeof(ucChartViewer),
            new PropertyMetadata(null, ChartInfos_Changed));

        public int CurrentIndex
        {
            get { return _currentIndex; }
            set
            {
                _currentIndex = value;
                UpdateCurrentChartInfo();
                OnPropertyChanged();
            }
        }

        public string PageInfo
        {
            get { return _pageInfo; }
            set
            {
                _pageInfo = value;
                OnPropertyChanged();
            }
        }

        public ChartInfo CurrentChartInfo
        {
            get => _currentChartInfo;
            set
            {
                _currentChartInfo = value;
                OnPropertyChanged();
            }
        }

        #endregion

        #region Commands

        public ICommand SaveChartImageCommand { get; set; }

        #endregion

        #region Public Events

        public event PropertyChangedEventHandler? PropertyChanged;

        #endregion

        #region Public Methods

        public void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion

        #region Private Methods

        private void ChartFileName_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            // 파일 및 폴더 이름에 사용할 수 없는 문자 목록
            string invalidChars = @"<>:""/\|?*";
            Regex regex = new Regex($"[{Regex.Escape(invalidChars)}]");

            // 입력된 텍스트가 유효한지 확인
            e.Handled = regex.IsMatch(e.Text);
        }

        private static void ChartInfos_Changed(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            if (d is ucChartViewer chartViewer)
            {
                if (e.NewValue is IList<ChartInfo> chartInfo)
                {
                    chartViewer.CurrentIndex = 0;
                }
            }
        }

        private void btnPrev_Click(object sender, RoutedEventArgs e)
        {
            Prev();
        }

        private void btnNext_Click(object sender, RoutedEventArgs e)
        {
            Next();
        }

        private void Next()
        {
            if (ChartInfos == null)
                return;
            if (_currentIndex < ChartInfos.Count - 1)
            {
                _currentIndex++;
                UpdateCurrentChartInfo();
            }
        }

        private void Prev()
        {
            if (ChartInfos == null)
                return;
            if (_currentIndex > 0)
            {
                _currentIndex--;
                UpdateCurrentChartInfo();
            }
        }

        private void UpdateCurrentChartInfo()
        {
            btnPrev.IsEnabled = true;
            btnNext.IsEnabled = true;
            if (_currentIndex == 0)
                btnPrev.IsEnabled = false;
            else if (_currentIndex == ChartInfos.Count - 1)
                btnNext.IsEnabled = false;
            CurrentChartInfo = ChartInfos[_currentIndex];
            PageInfo = $"{_currentIndex + 1} / {ChartInfos.Count}";
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
