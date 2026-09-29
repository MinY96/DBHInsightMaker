using DBHTab.Pages;
using DBHTab.ViewModels;

namespace DBHTab.Views
{
    /// <summary>
    /// CreateNewColumnPopupView.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class CreateNewColumnPopupView
    {
        public CreateNewColumnPopupView(string projectDir, IEnumerable<Models.ColumnInfo> columns, ProjectMainView mainView)
        {
            InitializeComponent();
            this.DataContext = new CreateNewColumnPopupViewModel(projectDir, columns, mainView);
        }

        private void nvCreateColumnOption_SelectionChanged(ModernWpf.Controls.NavigationView sender, ModernWpf.Controls.NavigationViewSelectionChangedEventArgs args)
        {
            var selectedItem = (ModernWpf.Controls.NavigationViewItem)args.SelectedItem;
            string pageName = (string)selectedItem.Tag;
            if (pageName == "CreateRandomCol")
            {
                contentFrameCreateCol.Navigate(typeof(CreateRandomColPage), (CreateNewColumnPopupViewModel)this.DataContext);
            }
            else if (pageName == "CreateCalcCol")
            {
                contentFrameCreateCol.Navigate(typeof(CreateCalcColPage), (CreateNewColumnPopupViewModel)this.DataContext);
            }
            else if (pageName == "CreateCombiCol")
            {
                contentFrameCreateCol.Navigate(typeof(CreateCombiColPage), (CreateNewColumnPopupViewModel)this.DataContext);
            }
            else if (pageName == "CreateOutlierCol")
            {
                contentFrameCreateCol.Navigate(typeof(CreateOutlierColPage), (CreateNewColumnPopupViewModel)this.DataContext);
            }
            else if (pageName == "CreateConvertCol")
            {
                contentFrameCreateCol.Navigate(typeof(CreateConvertColPage), (CreateNewColumnPopupViewModel)this.DataContext);
            }
        }

        //private void CreateNewData_PrimaryButtonClick(ModernWpf.Controls.ContentDialog sender, ModernWpf.Controls.ContentDialogButtonClickEventArgs args)
        //{
        //    string newColName = ((CreateNewColumnPopupViewModel)this.DataContext).NewColumnName;
        //    var currentPage = contentFrameCreateCol.Content;
        //    if (currentPage != null)
        //    {
        //        var model = ((ModernWpf.Controls.Page)currentPage).DataContext as CreateColumnPageModelBase;
        //        if (model != null)
        //        {
        //            if (model.IsCompleteOption)
        //            {
        //                var options = model.Payload();
        //            }
        //        }
        //    }
        //}
    }
}
