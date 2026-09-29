using DBHTab.Models;
using DBHTab.ViewModels;

namespace DBHTab.Commands
{
    public class CreateNewColumnCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public CreateNewColumnCommand()
        {

        }

        #endregion

        #region Properties
        #endregion

        #region Commands
        #endregion

        #region Public Events
        #endregion

        #region Public Methods

        public override bool CanExecute(object? parameters)
        {
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            string newColumnName = parameter[1] as string;
            var currentPage = parameter[2];
            CreateNewColumnPopupViewModel mainModel = parameter[3] as CreateNewColumnPopupViewModel;
            if (currentPage != null)
            {
                var pageModel = ((ModernWpf.Controls.Page)currentPage).DataContext as CreateColumnPageModelBase;
                if (pageModel != null)
                {
                    if (pageModel.IsCompleteOption)
                    {
                        var options = pageModel.Payload();
                        options["ProjectDir"] = projectDir;
                        options["NewColumnName"] = newColumnName;
                        CreateColumn(options, mainModel);
                    }
                }
            }
        }

        #endregion

        #region Private Methods

        private async void CreateColumn(Dictionary<string, object> options, CreateNewColumnPopupViewModel? mainModel)
        {
            mainModel.UpdateMainViewProgressState(true, "신규 컬럼 생성중...");
            bool isCreate = await HttpRequest.PostCreateColumn(options);
            mainModel.UpdateMainViewProgressState(false, "");
            if (isCreate)
            {
                mainModel.UpdateMainViewProject();
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
