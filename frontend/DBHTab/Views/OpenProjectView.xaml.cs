using DBHTab.Manager;
using DBHTab.Models;
using DBHTab.ViewModels;
using System.Windows;

namespace DBHTab.Views
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class OpenProjectView : Window
    {
        private ProjectWindowManager _projectWindowManager;

        public OpenProjectView()
        {
            InitializeComponent();
            DataContext = new OpenProjectViewModel();
            _projectWindowManager = new ProjectWindowManager();
        }

        private void OnCreateProjectButtonClick(object sender, RoutedEventArgs e)
        {
            try
            {
                var createPopup = new CreateProjectPopupView();
                createPopup.Closed += CreatePopup_Closed;
                createPopup.ShowAsync();
            }
            catch (Exception ex)
            {

            }
        }

        private void CreatePopup_Closed(ModernWpf.Controls.ContentDialog sender, ModernWpf.Controls.ContentDialogClosedEventArgs args)
        {
            using var _ = ((OpenProjectViewModel)this.DataContext).LoadSavedProjectSAsync();
        }

        private void Project_MouseDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (ProjectListView.SelectedItem is ProjectInfo selectedProject)
            {
                _projectWindowManager.TryOpenProjectWindow(() => new ProjectMainView(selectedProject));
            }
        }
    }
}