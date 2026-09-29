using DBHTab.Commands;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace DBHTab.UserControls
{
    /// <summary>
    /// ucExplainChartViewer.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ucExplainChartViewer : UserControl
    {
        #region Field Variables
        #endregion

        #region Initialize

        public ucExplainChartViewer()
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
            typeof(ucExplainChartViewer),
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
            typeof(ucExplainChartViewer),
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
            typeof(ucExplainChartViewer),
            new PropertyMetadata(null));

        public string Explain
        {
            get { return (string)GetValue(ExplainProperty); }
            set
            {
                SetValue(ExplainProperty, value);
            }
        }

        public static readonly DependencyProperty ExplainProperty = DependencyProperty.Register(
            "Explain",
            typeof(string),
            typeof(ucExplainChartViewer),
            new PropertyMetadata(string.Empty));

        public string Insight
        {
            get { return (string)GetValue(InsightProperty); }
            set
            {
                SetValue(InsightProperty, value);
            }
        }

        public static readonly DependencyProperty InsightProperty = DependencyProperty.Register(
            "Insight",
            typeof(string),
            typeof(ucExplainChartViewer),
            new PropertyMetadata(string.Empty));

        public string CheckPoint
        {
            get { return (string)GetValue(CheckPointProperty); }
            set
            {
                SetValue(CheckPointProperty, value);
            }
        }

        public static readonly DependencyProperty CheckPointProperty = DependencyProperty.Register(
            "CheckPoint",
            typeof(string),
            typeof(ucExplainChartViewer),
            new PropertyMetadata(string.Empty));

        #endregion

        #region Commands

        public ICommand SaveChartImageCommand { get; set; }

        #endregion

        #region Public Events


        #endregion

        #region Public Methods        

        #endregion

        #region Private Methods

        #endregion

        #region Protected Methods
        #endregion
    }
}
