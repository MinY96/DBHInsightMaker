using DBHTab.Models;
using System.Diagnostics;
using System.IO;
using System.Windows;

namespace DBHTab
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private Process pythonProcess;

        public App()
        {
            AppDomain.CurrentDomain.UnhandledException += CurrentDomain_UnhandledException;            
        }

        private void CurrentDomain_UnhandledException(object sender, UnhandledExceptionEventArgs e)
        {
            if (pythonProcess != null && !pythonProcess.HasExited)
            {
                pythonProcess.Kill();
            }
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            killProcessByName("app");
            var exe = ExternalPath.EnsureExtractedApiExe();
            var psi = new ProcessStartInfo
            {
                FileName = exe,
                WorkingDirectory = Path.GetDirectoryName(exe),
                UseShellExecute = false,
                CreateNoWindow = true,
            };

            // 디버깅 시 주석, 게시할 때 주석 해제
            pythonProcess = Process.Start(psi);
        }

        protected override void OnExit(ExitEventArgs e)
        {
            bool isShutDownApi = HttpRequest.PostInsertUserLogs();
            base.OnExit(e);
            // 애플리케이션 종료 시 Python 프로세스 종료
            if (pythonProcess != null)
            {
                pythonProcess.CloseMainWindow();
                pythonProcess.WaitForExit(5000);

                if (!pythonProcess.HasExited)
                {
                    pythonProcess.Kill();
                    pythonProcess.WaitForExit();
                }

                pythonProcess.Dispose();
            }
        }

        private void killProcessByName(string processName)
        {
            try
            {
                Process[] processes = Process.GetProcessesByName(processName);

                foreach (var process in processes)
                {
                    process.Kill();
                    process.WaitForExit();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void RemovePastApiDir()
        {
            var userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            string localTempDir = Path.Combine(userPath, "AppData\\Local\\Temp");
            DirectoryInfo dirLocalTemp = new DirectoryInfo(localTempDir);
            if (dirLocalTemp.Exists)
            {
                var directories = Directory.GetDirectories(localTempDir, "_MEI*");
                foreach (var directory in directories)
                {
                    // Python 실행파일 압축 해제 폴더 삭제
                    Directory.Delete(directory, true);
                }
            }
        }
    }

}
