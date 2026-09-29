using Microsoft.Win32;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Media.Imaging;

namespace DBHTab.Commands
{
    public class SaveChartImageCommand : CommandBase
    {
        #region Field Variables
        #endregion

        #region Initialize

        public SaveChartImageCommand()
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
            var parameter = (object[])parameters;
            if (parameter == null)
                return false;
            if (parameter[0] == DependencyProperty.UnsetValue ||
                parameter[1] == DependencyProperty.UnsetValue)
                return false;
            string? chartFileName = (string?)parameter[0];
            if ((parameter[1] is not byte[]) && (parameter[1] is not BitmapImage))
            {
                return false;
            }
            if (string.IsNullOrEmpty(chartFileName) || parameter[1] == null)
            {
                return false;
            }

            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string chartFileName = parameter[0] as string;
            object chartImg = parameter[1];
            SaveChartImage(chartFileName, chartImg);
        }

        #endregion

        #region Private Methods

        private void SaveChartImage(string chartFileName, object chartImg)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.FileName = chartFileName;
            saveFileDialog.Filter = "PNG file (*.png)|*.png";
            string imgType = chartFileName.EndsWith(".png") ? "PNG" : "GIF";

            if (saveFileDialog.ShowDialog() == true)
            {
                try
                {
                    if (chartImg is byte[] byteArray)
                    {
                        // chartImg가 byte[]인 경우
                        File.WriteAllBytes(saveFileDialog.FileName, byteArray);
                    }
                    else if (chartImg is BitmapImage bitmapImage)
                    {
                        // chartImg가 BitmapImage인 경우
                        if (imgType=="PNG")
                        {
                            using (FileStream stream = new FileStream(saveFileDialog.FileName, FileMode.Create))
                            {
                                PngBitmapEncoder encoder = new PngBitmapEncoder();
                                encoder.Frames.Add(BitmapFrame.Create(bitmapImage));
                                encoder.Save(stream);                            
                            }
                        }
                        else if (imgType=="GIF")
                        {
                            File.Copy(bitmapImage.UriSource.LocalPath, saveFileDialog.FileName, true);
                        }
                    }
                    else
                    {
                        throw new InvalidOperationException("Unsupported image type.");
                    }

                    ModernWpf.MessageBox.Show($"{imgType} 파일이 저장되었습니다.");
                }
                catch (Exception e)
                {
                    ModernWpf.MessageBox.Show("파일 저장 에러: " + e.Message, "에러", MessageBoxButton.OK, MessageBoxImage.Error, MessageBoxResult.OK);
                }
            }
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
