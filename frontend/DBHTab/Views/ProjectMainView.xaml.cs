using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;

namespace DBHTab.Views
{
    /// <summary>
    /// ProjectMainView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class ProjectMainView : Window
    {
        public ProjectMainView(ProjectInfo projectInfo)
        {
            InitializeComponent();
            DataContext = new ProjectMainViewModel(projectInfo, this);
        }
    }
}
