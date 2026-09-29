using System.Windows;

namespace DBHTab.Manager
{
    public class ProjectWindowManager
    {
        #region Field Variables

        private int _openProjectCount = 0;
        private const int MaxProjects = 3;

        #endregion

        #region Initialize
        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events

        public bool TryOpenProjectWindow(Func<Window> createWindow)
        {
            if (_openProjectCount < MaxProjects)
            {
                _openProjectCount++;
                var projectWindow = createWindow();
                projectWindow.Closed += (s, e) => _openProjectCount--;
                projectWindow.Show();
                return true;
            }
            else
            {
                ModernWpf.MessageBox.Show($"최대 {MaxProjects}개의 프로젝트 창만 열 수 있습니다.", "경고", MessageBoxButton.OK, MessageBoxImage.Warning);
                return false;
            }
        }

        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods
        #endregion
    }
}
