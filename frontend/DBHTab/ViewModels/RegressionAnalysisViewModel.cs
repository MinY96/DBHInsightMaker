namespace DBHTab.ViewModels
{
    public class RegressionAnalysisViewModel : ViewModelBase
    {
        #region Field Variables

        string _projectName;
        string _regressionDir;

        #endregion

        #region Initialize

        public RegressionAnalysisViewModel(string projectName, string regressionDir)
        {
            _projectName = projectName;
            _regressionDir = regressionDir;
        }

        #endregion

        #region Properties

        public string ProjectName
        {
            get { return _projectName; }
        }

        public string RegressionDir
        {
            get { return _regressionDir; }
        }

        #endregion

        #region Commands
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
