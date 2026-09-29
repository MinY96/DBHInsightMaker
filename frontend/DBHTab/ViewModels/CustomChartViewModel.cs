using DBHTab.Commands;
using DBHTab.Models;
using DBHTab.Views;
using System.Collections.ObjectModel;
using System.IO;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace DBHTab.ViewModels
{
    public class CustomChartViewModel : ViewModelBase
    {
        #region Field Variables

        private CustomChartView _customChartView;
        private string _projectName;
        private string _projectDir;
        private bool _isLoad = false;
        private bool _isLoadingOptions;
        private bool _isCreatingChart;
        private string _loadMsg = string.Empty;
        private string _chartGroup = string.Empty;
        private string _chartType = string.Empty;
        private string _chartHeader = string.Empty;
        private string _chartDesc = string.Empty;
        private string _customChartPath = string.Empty;
        private string _disabledReason = string.Empty;
        private IList<ColumnInfo> _columns;
        BitmapImage _sampleChart;
        BitmapImage _creationChart;

        #endregion

        #region Initialize

        public CustomChartViewModel(CustomChartView view, string projectName, string projectDir, IEnumerable<Models.ColumnInfo> columns)
        {
            _customChartView = view;
            _projectName = projectName;
            _projectDir = projectDir;
            _columns  = new List<ColumnInfo>(columns);
            InitChartNodes();
            LoadCustomChartCommand = new LoadCustomChartCommand(this);
        }

        #endregion

        #region Properties

        public string ProjectName
        {
            get { return _projectName; }
        }

        public string ProjectDir
        {
            get { return _projectDir; }
        }

        public bool IsLoad
        {
            get { return _isLoad; }
            set
            {
                _isLoad = value;
                OnPropertyChanged();
            }
        }

        public bool IsLoadingOptions
        {
            get { return _isLoadingOptions; }
            set
            {
                _isLoadingOptions = value;
                OnPropertyChanged();
            }
        }

        public bool IsCreatingChart
        {
            get { return _isCreatingChart; }
            set
            {
                _isCreatingChart = value;
                OnPropertyChanged();
            }
        }

        public string DisabledReason
        {
            get { return _disabledReason; }
            set
            {
                _disabledReason = value;
                OnPropertyChanged();
            }
        }

        public string LoadingMessage
        {
            get { return _loadMsg; }
            set
            {
                _loadMsg = value;
                OnPropertyChanged();
            }
        }

        public string SelectedChartGroup
        {
            get { return _chartGroup; }
            set
            {
                _chartGroup = value;
                OnPropertyChanged();
            }
        }

        public string SelectedChartType
        {
            get { return _chartType; }
            set
            {
                _chartType = value;
                OnPropertyChanged();
            }
        }

        public string SelectedChartHeader
        {
            get { return _chartHeader; }
            set
            {
                _chartHeader = value;
                OnPropertyChanged();
            }
        }

        public string SelectedChartDesc
        {
            get { return _chartDesc; }
            set
            {
                _chartDesc = value;
                OnPropertyChanged();
            }
        }

        public string CustomChartPath
        {
            get { return _customChartPath; }
            set
            {
                _customChartPath = value;
                OnPropertyChanged();
            }
        }

        public IList<ColumnInfo> ColumnLists
        {
            get { return _columns; }
            set
            {
                _columns = value;
                OnPropertyChanged();
            }
        }

        public BitmapImage SampleChart
        {
            get { return _sampleChart; }
            set
            {
                _sampleChart = value;
                OnPropertyChanged();
            }
        }

        public BitmapImage CreationChart
        {
            get { return _creationChart; }
            set
            {
                _creationChart = value;
                OnPropertyChanged();
            }
        }

        public ObservableCollection<ChartOption> Options { get; } = new ObservableCollection<ChartOption>();
        public ObservableCollection<ChartNode> ChartNodes { get; } = new ObservableCollection<ChartNode>();

        #endregion

        #region Commands

        public ICommand TreeItemSelectedCommand { get; set; }
        public ICommand LoadCustomChartCommand { get; set; }

        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public void ShowDisabledReason(string reason)
        {
            DisabledReason = reason;
        }

        public void UpdateCustomChart(ChartInfo customChart)
        {
            if (customChart != null)
            {
                CustomChartPath = customChart.ChartFileName;
                if (customChart.ChartBitmapImage != null)
                {
                    CreationChart = customChart.ChartBitmapImage;
                }
                else
                {
                    BitmapImage image = new BitmapImage();
                    image.BeginInit();
                    image.StreamSource = new MemoryStream(customChart.ChartImage);
                    image.EndInit();
                    image.Freeze();
                    CreationChart = image;
                }
                IsCreatingChart = false;
            }
        }

        #endregion

        #region Private Methods

        private void AddChildNode(ChartNode targetNode, string header, string groupTag, string typeTag)
        {
            targetNode.Children.Add(new ChartNode
            {
                Header = header,
                GroupTag = groupTag,
                TypeTag = typeTag
            });
        }

        private void InitChartNodes()
        {
            var scatterNode = new ChartNode 
            { 
                Header="산점도 - 6",
                GroupTag = "scatter",
                TypeTag = null
            };
            AddChildNode(scatterNode, "산점도", "scatter", "num_num");
            AddChildNode(scatterNode, "그룹 별 산점도", "scatter", "num_num_by_cat");
            AddChildNode(scatterNode, "3d 산점도", "scatter", "num_num_num");
            AddChildNode(scatterNode, "3d 산점도 with 투영선", "scatter", "num_num_num_stem");
            AddChildNode(scatterNode, "그룹 별 3d 산점도", "scatter", "num_num_num_by_cat");
            AddChildNode(scatterNode, "그룹 별 3d 산점도 with 투영선", "scatter", "num_num_num_stem_by_cat");
            ChartNodes.Add(scatterNode);

            var lineNode = new ChartNode
            {
                Header = "라인 차트 - 6",
                GroupTag = "line",
                TypeTag = null
            };
            AddChildNode(lineNode, "라인 차트(인덱스 기준)", "line", "index_num");
            AddChildNode(lineNode, "범주 별 라인 차트(인덱스 기준)", "line", "index_num_cat");
            AddChildNode(lineNode, "다변량 라인 차트(인덱스 기준)", "line", "index_nums");
            AddChildNode(lineNode, "라인 차트(DateTime 기준)", "line", "dt_num");
            AddChildNode(lineNode, "범주 별 라인 차트(DateTime 기준)", "line", "dt_num_cat");
            AddChildNode(lineNode, "다변량 라인 차트(DateTime 기준)", "line", "dt_nums");
            ChartNodes.Add(lineNode);

            var barNode = new ChartNode
            {
                Header = "바 차트 - 5",
                GroupTag = "bar",
                TypeTag = null
            };
            AddChildNode(barNode, "파레토 차트", "bar", "pareto");
            AddChildNode(barNode, "범주 별 바 차트(빈도/백분위/비율)", "bar", "count");
            AddChildNode(barNode, "그룹/누적형 바 차트(빈도/백분위/비율)", "bar", "count_cat");
            AddChildNode(barNode, "범주 별 바 차트(수치 요약 - 통계량)", "bar", "bar_cat_num");
            AddChildNode(barNode, "그룹/누적형 바 차트(수치 요약 - 통계량)", "bar", "bar_cat_num_cat");
            ChartNodes.Add(barNode);

            var boxNode = new ChartNode
            {
                Header = "Box형 차트 - 3",
                GroupTag = "box",
                TypeTag = null
            };
            AddChildNode(boxNode, "Box/Violin/Boxen 차트", "box", "num");
            AddChildNode(boxNode, "범주 별 Box/Violin/Boxen 차트", "box", "num_cat");
            AddChildNode(boxNode, "범주 x 그룹 별 Box/Violin/Boxen 차트", "box", "num_cat_cat");
            ChartNodes.Add(boxNode);

            var pointNode = new ChartNode
            {
                Header = "Point형 차트 - 3",
                GroupTag = "point",
                TypeTag = null
            };
            AddChildNode(pointNode, "Strip/Swarm 차트", "point", "num");
            AddChildNode(pointNode, "범주 별 Strip/Swarm 차트", "point", "num_cat");
            AddChildNode(pointNode, "범주 x 그룹 별 Strip/Swarm 차트", "point", "num_cat_cat");
            ChartNodes.Add(pointNode);

            var distNode = new ChartNode
            {
                Header = "분포(관계)형 차트 - 5",
                GroupTag = "dist",
                TypeTag = null
            };
            AddChildNode(distNode, "히스토그램/KDE 차트", "dist", "dist_num");
            AddChildNode(distNode, "범주 x 그룹 별 히스토그램/KDE 차트", "dist", "dist_num_cat");
            AddChildNode(distNode, "히트맵/등고선(수치형 관계 시각화)", "dist", "dist_num_num");
            AddChildNode(distNode, "범주 x 그룹 별 히트맵/등고선(수치형 관계 시각화)", "dist", "dist_num_num_cat");
            AddChildNode(distNode, "히트맵(범주형 관계 요약 시각화)", "dist", "dist_cat_cat_num");
            ChartNodes.Add(distNode);

            var proportionNode = new ChartNode
            {
                Header = "빈도/비중/비율 시각화 차트 - 5",
                GroupTag = "proportion",
                TypeTag = null
            };
            AddChildNode(proportionNode, "파이(Pie) 차트", "proportion", "pie");
            AddChildNode(proportionNode, "Word Cloud(워드 클라우드)", "proportion", "wordcloud");
            AddChildNode(proportionNode, "와플(Waffle) 차트", "proportion", "waffle");
            AddChildNode(proportionNode, "트리맵(TreeMap) 차트", "proportion", "treemap");
            AddChildNode(proportionNode, "모자이크(Mosaic) 차트", "proportion", "mosaic");
            ChartNodes.Add(proportionNode);

            TreeItemSelectedCommand = new RelayCommand<ChartNode>(OnTreeItemSelected);
        }

        private async void OnTreeItemSelected(ChartNode node)
        {
            if (node == null)
                return;

            if (string.IsNullOrEmpty(node.TypeTag))
            {
                Options.Clear();
                SelectedChartGroup = null;
                SelectedChartType = null;
                SelectedChartDesc = string.Empty;
                SampleChart = null;
                return;
            }

            SelectedChartGroup = node.GroupTag;
            SelectedChartType = node.TypeTag;
            SelectedChartHeader = node.Header;
            SelectedChartDesc = string.Empty;
            CreationChart = null;
            CustomChartPath = null;
            string stringChartName = $"{node.GroupTag}-{node.TypeTag}";
            //string stringChartName = "scatter-num_num_by_cat";
            try
            {
                SampleChart = new BitmapImage(new Uri($"pack://application:,,,/Resources/{stringChartName}.png")) 
                {
                    DecodePixelWidth = 500,
                    DecodePixelHeight = 300,
                };
            }
            catch (Exception ex)
            {
            }

            try
            {
                IsLoadingOptions = true;
                var optionResponses = await HttpRequest.PostChartOptionsAsync(node.GroupTag, node.TypeTag);
                SelectedChartDesc = optionResponses.Description;
                Options.Clear();
                foreach (var opt in optionResponses.Options)
                {
                    opt.ControlPadding = new System.Windows.Thickness((double)opt.Paddingleft, 0,0,0);
                    if (new[] { "num", "x_num", "y_num", "z_num", "g_num", "y_nums" }.Contains(opt.Key))
                    {
                        opt.Option = ColumnLists.Where(
                            c => (c.ColumnChar != "Nominal") && (c.ColumnChar != "DateTime")
                            ).Select(c => c.Column).ToList(); ;
                    }
                    else if (new[] {"cat", "x_cat", "y_cat", "z_cat", "g_cat" }.Contains(opt.Key))
                    {
                        opt.Option = ColumnLists.Where(
                            c => (c.ColumnType == "Categorical") || 
                            ((c.ColumnChar == "Discrete") && (c.UniqueCount<20)))
                            .Select(c=>c.Column).ToList();
                    }
                    else if (new[] { "large_g_cat" }.Contains(opt.Key))
                    {
                        opt.Option = ColumnLists.Where(
                            c => (c.ColumnType == "Categorical") ||
                            ((c.ColumnChar == "Discrete") && (c.UniqueCount <= 5)))
                            .Select(c => c.Column).ToList();
                    }
                    else if (new[] { "x_dt", "y_dt" }.Contains(opt.Key))
                    {
                        opt.Option = ColumnLists.Where(
                            c => (c.ColumnChar == "DateTime"))
                            .Select(c => c.Column).ToList(); ;
                    }
                    else if (opt.Key == "fill")
                    {
                        opt.Value = "true";
                    }
                    Options.Add(opt);
                }
            }
            catch
            {

            }
            IsLoadingOptions = false;
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
