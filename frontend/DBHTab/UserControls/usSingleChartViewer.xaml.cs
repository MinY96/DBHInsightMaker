using DBHTab.Commands;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media.Imaging;
using WpfAnimatedGif;

namespace DBHTab.UserControls
{
    /// <summary>
    /// usSingleChartViewer.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class usSingleChartViewer : UserControl
    {
        #region Field Variables
        #endregion

        #region Initialize

        public usSingleChartViewer()
        {
            InitializeComponent();
            SaveChartImageCommand = new SaveChartImageCommand();
        }

        #endregion

        #region Properties



        public string ChartName
        {
            get { return (string)GetValue(ChartNameProperty); }
            set
            {
                SetValue(ChartNameProperty, value);
            }
        }

        public static readonly DependencyProperty ChartNameProperty = DependencyProperty.Register(
            "Chartname",
            typeof(string),
            typeof(usSingleChartViewer),
            new PropertyMetadata(string.Empty));

        public string ChartPath
        {
            get { return (string)GetValue(ChartPathProperty); }
            set
            {
                SetValue(ChartPathProperty, value);
            }
        }

        public static readonly DependencyProperty ChartPathProperty = DependencyProperty.Register(
            "ChartPath",
            typeof(string),
            typeof(usSingleChartViewer),
            new PropertyMetadata(string.Empty));

        public BitmapImage ChartImage
        {
            get { return (BitmapImage)GetValue(ChartImageProperty); }
            set
            {
                SetValue(ChartImageProperty, value);
            }
        }

        public static readonly DependencyProperty ChartImageProperty = DependencyProperty.Register(
            "ChartImage",
            typeof(BitmapImage),
            typeof(usSingleChartViewer),
            new PropertyMetadata(null, OnChartImageChanged));

        #endregion

        #region Commands

        public ICommand SaveChartImageCommand { get; set; }

        #endregion

        #region Public Events


        #endregion

        #region Public Methods        

        #endregion

        #region Private Methods

        private static void OnChartImageChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var control = d as usSingleChartViewer;
            if (control != null && e.NewValue is BitmapImage newImage)
            {
                if (newImage.CanFreeze)
                {
                    newImage.Freeze();
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
