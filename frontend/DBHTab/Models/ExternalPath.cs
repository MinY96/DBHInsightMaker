using System.IO;
using System.IO.Compression;

namespace DBHTab.Models
{
    public static class ExternalPath
    {
        public static string GetBaseDir()
        {
            return AppDomain.CurrentDomain.BaseDirectory;
        }

        private static string GetZipPath()
            => Path.Combine(GetBaseDir(), "External", "app.zip");

        private static string GetExtractPath()
            => Path.Combine(GetBaseDir(), "External", "app");

        public static string EnsureExtractedApiExe()
        {
            string zipPath = GetZipPath();
            string extractDir = GetExtractPath();

            // zip 파일이 바뀌면 새로 풀기
            string markerFile = Path.Combine(extractDir, "version.marker");
            bool needExtract = true;

            if (File.Exists(markerFile))
            {
                var oldHash = File.ReadAllText(markerFile);
                var newHash = File.GetLastWriteTimeUtc(zipPath).Ticks.ToString();
                if (oldHash == newHash)
                {
                    needExtract = false;
                }
            }
            if (needExtract)
            {
                if (Directory.Exists(extractDir))
                    Directory.Delete(extractDir, true);
                Directory.CreateDirectory(extractDir);
                ZipFile.ExtractToDirectory(zipPath, extractDir);
                File.WriteAllText(markerFile, File.GetLastWriteTimeUtc(zipPath).Ticks.ToString());
            }
            return Path.Combine(extractDir, "app.exe");
        }

        public static string GetPyApiExe()
            => Path.Combine(GetBaseDir(), "External", "app", "app.exe");
    }
}
