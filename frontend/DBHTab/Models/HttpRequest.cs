using DBHTab.Converters;
using System.Collections.ObjectModel;
using System.DirectoryServices.ActiveDirectory;
using System.Net.Http;
using System.Security.Policy;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Windows;
using System.Windows.Media.Imaging;

namespace DBHTab.Models
{
    public static class HttpRequest
    {
        #region Field Static Variables

        private static string _ip = "localhost";
        private static int _port = 5050;
        //private static int _timeout = 200;
        private static int _timeout = 1500;

        #endregion

        #region Public Static Methods

        public static async Task<bool> CheckOpenApi()
        {
            string? result = await GetRequestAsync("/insightmaker/is_open");
            int iMax = 20;
            while (string.IsNullOrWhiteSpace(result))
            {
                if (iMax <= 0)
                {
                    return false;
                }
                result = await GetRequestAsync("/insightmaker/is_open");
                iMax--;
            }
            return true;
        }

        public static async Task<IEnumerable<ProjectInfo>> GetProjectListAsync(string? projectParentDir)
        {
            var payload = new { ProjectParentDir = projectParentDir };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/project_list", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true,
                Converters = { new DateTimeConvertorJson() }
            };
            result = JsonSerializer.Deserialize<IEnumerable<ProjectInfo>>(JsonSerializer.Serialize(result), options);
            return (IEnumerable<ProjectInfo>)result;
        }

        public static async Task<IEnumerable<ColumnInfo>> GetColumnListAsync(string? projectDir)
        {
            var payload = new { ProjectDir = projectDir };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/column_info", payload);
            jsonResult = jsonResult.Replace("NaN", "null");
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true,
                Converters = { new DateTimeConvertorJson() }
            };
            result = JsonSerializer.Deserialize<IEnumerable<ColumnInfo>>(JsonSerializer.Serialize(result), options);
            return (IEnumerable<ColumnInfo>)result;
        }

        public static async Task<IEnumerable<ChartInfo>> PostColumnCharts(string projectDir, ColumnInfo selectedColumn)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = selectedColumn.Column,
                ColumnType = selectedColumn.ColumnType,
                ColumnChar = selectedColumn.ColumnChar
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/chart/single", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<ChartInfo>>(JsonSerializer.Serialize(result));
            foreach (ChartInfo chartInfo in (IEnumerable<ChartInfo>)result)
            {
                chartInfo.ChartImage = Convert.FromBase64String(chartInfo.ImageBase64);
            }
            return (IEnumerable<ChartInfo>)result;
        }

        public static async Task<ChartOptionsResponse> PostChartOptionsAsync(string chartGroup, string chartType)
        {
            var payload = new
            {
                ChartGroup = chartGroup,
                ChartType = chartType
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/chart/chart_option", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<ChartOptionsResponse>(
                JsonSerializer.Serialize(result),
                new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true,
                }
            );
            return (ChartOptionsResponse)result;
        }

        public static async Task<ChartInfo> PostCustomChart(string projectDir, string chartGroup, string chartType, IEnumerable<ChartOption> options)
        {
            //var line_option = options.FirstOrDefault(o => o.Key == "lines");
            //var payload = (object)null;
            //if (line_option != null && line_option.LinesOption != null)
            //{
            //    var line_options = line_option.LinesOption.Select(l => new
            //    {
            //        axis = l.Axis,
            //        kind = l.Kind,
            //        custom_value = l.CustomValue != null ? ((double)l.CustomValue).ToString("E5") : string.Empty,
            //        linestyle = l.LineStyle,
            //        linewidth = l.LineWidth,
            //        linecolor = l.Color,
            //        text = l.Text,
            //        text_va = l.TextAlignVertical,
            //        text_ha = l.TextAlignHorizontal,
            //        text_rotate = l.TextRotation
            //    }).ToList();

            //    payload = new
            //    {
            //        ProjectDir = projectDir,
            //        ChartGroup = chartGroup,
            //        ChartType = chartType,
            //        Options = options.Select(o => new
            //        {
            //            key = o.Key,
            //            value = o.Value,
            //            type = o.Type,
            //            lines = o.Key == "lines" ? line_options : null,
            //        }).ToList(),
            //    };
            //}
            //else
            //{
            //    payload = new
            //    {
            //        ProjectDir = projectDir,
            //        ChartGroup = chartGroup,
            //        ChartType = chartType,
            //        Options = options.Select(o => new
            //        {
            //            key = o.Key,
            //            value = o.Value,
            //            type = o.Type,
            //        }).ToList(),
            //    };
            //}
            var payload = new
            {
                ProjectDir = projectDir,
                ChartGroup = chartGroup,
                ChartType = chartType,
                Options = options.Select(ProcessChartOption).ToList()
            };

            string? jsonResult = await PostRequestAsync("/insightmaker/eda/chart/custom_chart", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            ChartInfo? chartInfo = JsonSerializer.Deserialize<ChartInfo>(JsonSerializer.Serialize(result));

            var gifOption = options.FirstOrDefault(o => o.Key == "gif");
            if (gifOption != null)
            {
                bool isGif;
                if (bool.TryParse(gifOption.Value, out isGif))
                {

                }
                else
                    isGif = false;
                if (isGif)
                {
                    chartInfo.ChartBitmapImage = new BitmapImage(new Uri($"{projectDir}/temp/animation.gif"));
                    return chartInfo;
                }

            }
            chartInfo.ChartImage = Convert.FromBase64String(chartInfo.ImageBase64);
            return chartInfo;
        }

        public static async Task<IEnumerable<ChartInfo>> PostRelativeChart(
            string projectDir,
            ColumnInfo colXaxis, ColumnInfo colYaxis, ColumnInfo colZaxis, ColumnInfo colGroup)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                ColumnX = (colXaxis != null) ? colXaxis.Column : null,
                ColumnY = (colYaxis != null) ? colYaxis.Column : null,
                ColumnZ = (colZaxis != null) ? colZaxis.Column : null,
                ColumnGroup = (colGroup != null) ? colGroup.Column : null
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/chart/relative", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<ChartInfo>>(JsonSerializer.Serialize(result));
            foreach (ChartInfo chartInfo in (IEnumerable<ChartInfo>)result)
            {
                chartInfo.ChartImage = Convert.FromBase64String(chartInfo.ImageBase64);
            }
            return (IEnumerable<ChartInfo>)result;
        }

        public static async Task<IEnumerable<string>> PostColumnDataInit(string projectDir, ColumnInfo selectedColumn)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = selectedColumn.Column,
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/column_data_init", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<string>>(JsonSerializer.Serialize(result));
            return (IEnumerable<string>)result;
        }

        public static async Task<IEnumerable<string>> GetExcelSheetsAsync(string excelFilePath)
        {
            var payload = new
            {
                ExcelFilePath = excelFilePath 
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/load_data/sheet", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<string>>(JsonSerializer.Serialize(result));
            return (IEnumerable<string>)result;
        }

        public static async Task<IEnumerable<string>> PostConvertTypeTest(string projectDir, string columnName, string convertTo,
            string datetimeFormat, IEnumerable<string> orders)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = columnName,
                ConvertTo = convertTo,
                DateTimeFormat = datetimeFormat,
                OrderInfo = orders,
                SaveMode = false
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/convert_column_type", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<string>>(JsonSerializer.Serialize(result));
            return (IEnumerable<string>)result;
        }        

        public static async Task<bool> PostConvertType(string projectDir, string columnName, string convertTo,
            string datetimeFormat, IEnumerable<string> orders)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = columnName,
                ConvertTo = convertTo,
                DateTimeFormat = datetimeFormat,
                OrderInfo = orders,
                SaveMode = true
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/convert_column_type", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }
            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<IEnumerable<UniqueData>> PostColumnUnique(string projectDir, string ColumName)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = ColumName,
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/column_unique_data", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<IEnumerable<string>>(JsonSerializer.Serialize(result));
            return ((IEnumerable<string>)result).Select(s => new UniqueData { Value = s });
        }

        public static async Task<Dictionary<string, object>> PostNomalityTestResult(string projectDir, ColumnInfo selectedColumn)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = selectedColumn.Column,
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/stat_test/normality", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            var resultPack = JsonSerializer.Deserialize<Dictionary<string, object>>(JsonSerializer.Serialize(result));

            var resultChart = JsonSerializer.Deserialize<IEnumerable<ChartInfo>>(JsonSerializer.Serialize(resultPack["Charts"]));
            foreach (ChartInfo chartInfo in (IEnumerable<ChartInfo>)resultChart)
            {
                chartInfo.ChartImage = Convert.FromBase64String(chartInfo.ImageBase64);
            }

            var resultTest = JsonSerializer.Deserialize<IEnumerable<StatTestInfo>>(JsonSerializer.Serialize(resultPack["Results"]));
            Dictionary<string, object> nomalityResult = new Dictionary<string, object>()
            {
                { "Chart", resultChart},
                { "Test", resultTest}
            };
            return nomalityResult;
        }

        public static async Task<Dictionary<string, object>> PostCorrResult(string projectDir, string corrMethod, IEnumerable<ColumnInfo> columns)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                CorrMethod = corrMethod,
                Columns = columns.Select(s => s.Column).ToList(),
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/analyze/correlation", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            var resultPack = JsonSerializer.Deserialize<Dictionary<string, object>>(JsonSerializer.Serialize(result));

            var resultChart = JsonSerializer.Deserialize<IEnumerable<ChartInfo>>(JsonSerializer.Serialize(resultPack["Charts"]));
            foreach (ChartInfo chartInfo in (IEnumerable<ChartInfo>)resultChart)
            {
                chartInfo.ChartImage = Convert.FromBase64String(chartInfo.ImageBase64);
            }

            var resultTest = JsonSerializer.Deserialize<IEnumerable<CorrResult>>(JsonSerializer.Serialize(resultPack["Results"]));
            Dictionary<string, object> corrResult = new Dictionary<string, object>()
            {
                { "Chart", resultChart},
                { "Result", resultTest}
            };
            return corrResult;
        }

        public static async Task<string> PostRegressionResult(string? projectDir, IEnumerable<ColumnInfo>? indepColumns, IEnumerable<ColumnInfo>? depColumns, string? selectionMethod, string? scalerMethod, string? imputeMethod, bool isSplit, float testRatio)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                IndepVars = indepColumns.Select(s => s.Column).ToList(),
                DepVar = depColumns.Select(s => s.Column).ToList()[0],
                SelectionMethod = selectionMethod,
                ScalerMethod = scalerMethod,
                ImputeMethod = imputeMethod,
                IsSplit = isSplit,
                TestRatio = testRatio
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/eda/analyze/regression", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return null;
            }
            result = JsonSerializer.Deserialize<string>(JsonSerializer.Serialize(result));
            return result.ToString();
        }

        public static async Task<bool> PostCreateProject(string? projectParentDir, string? projectName, string? projectDesc)
        {
            var payload = new
            {
                ProjectParentDir = projectParentDir,
                ProjectName = projectName,
                ProjectDesc = projectDesc
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/create_project", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostDeleteProject(string projectName, string projectDir)
        {
            var payload = new
            {
                ProjectName = projectName,
                ProjectDir = projectDir
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/delete_project", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostUpdateProject(string projectDir, string? projectName,
            DateTime? createTime, string? projectDesc, bool? isLoadData)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                ProjectName = projectName,
                ProjectDesc = projectDesc,
                CreateTime = createTime,
                IsLoadData = isLoadData
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/update_project", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostLoadData(string projectDir, bool isCsv, string sheetName, string filePath)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                IsCsv = isCsv,
                SheetName = sheetName,
                FilePath = filePath
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/load_data", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }
            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostRemoveColumn(string? projectDir, ColumnInfo selectedColumn)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                Column = selectedColumn.Column,
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/remove_column", payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostCreateColumn(Dictionary<string, object> options)
        {
            string url = "/insightmaker/project/create_column";
            string? jsonResult = await PostRequestAsync(url, options);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static async Task<bool> PostSaveAsExcel(string? projectDir, string savePath, bool isRaw)
        {
            var payload = new
            {
                ProjectDir = projectDir,
                SavePath = savePath,
            };
            string url = (isRaw) ? "/insightmaker/project/save_raw_data" : "/insightmaker/project/save_summary_data";
            string? jsonResult = await PostRequestAsync(url, payload);
            var result = GetRequestResultFormat(jsonResult);
            if (result == null)
            {
                return false;
            }

            result = JsonSerializer.Deserialize<bool>(JsonSerializer.Serialize(result));
            return (bool)result;
        }

        public static bool PostInsertUserLogs()
        {
            string url = "/insightmaker/insert_user_logs";
            try
            {
                using (HttpClient client = new HttpClient() { Timeout = TimeSpan.FromSeconds(_timeout) })
                {
                    // POST 요청
                    string urlSend = $"{GetBaserUrl()}/{url}";
                    HttpResponseMessage response = client.PostAsync(urlSend, null).GetAwaiter().GetResult();
                    return response.IsSuccessStatusCode;
                }
            }
            catch (Exception ex)
            {
                return false;
            }
        }

        public static async Task<Dictionary<string, object>> PostLoadFileInfo(string projectDir)
        {
            var payload = new
            {
                ProjectDir = projectDir,
            };
            string? jsonResult = await PostRequestAsync("/insightmaker/project/file_info", payload);
            var result = GetRequestResultFormat(jsonResult);
            result = JsonSerializer.Deserialize<ProjectInfo>(JsonSerializer.Serialize(result));
            return new Dictionary<string, object>
            {
                {"FileName",((ProjectInfo)result).FileName},
                {"IsCsv",((ProjectInfo)result).FileExtension=="csv" ? true : false},
                {"FileSize",((ProjectInfo)result).FileSize},
                {"SheetName",((ProjectInfo)result).SheetName},
                {"RowCol",$"({((ProjectInfo)result).Rows.ToString("N0")} / {((ProjectInfo)result).Cols.ToString("N0")})" }
            };
        }

        #endregion

        #region Private Static Methods

        private static string GetBaserUrl()
        {
            return $"http://{_ip}:{_port}";
        }

        private static async Task<string?> GetRequestAsync(string domain)
        {
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    string urlSend = $"{GetBaserUrl()}/{domain}";
                    HttpResponseMessage response = await client.GetAsync(urlSend);
                    response.EnsureSuccessStatusCode();
                    string responseBody = await response.Content.ReadAsStringAsync();
                    return responseBody;
                }
            }
            catch (HttpRequestException e)
            {
                return null;
            }
        }

        private static async Task<string?> PostRequestAsync(string domain, object payload)
        {
            try
            {
                using (HttpClient client = new HttpClient() { Timeout = TimeSpan.FromSeconds(_timeout) })
                {
                    string urlSend = $"{GetBaserUrl()}/{domain}";
                    var options = new JsonSerializerOptions
                    {
                        NumberHandling = JsonNumberHandling.AllowNamedFloatingPointLiterals
                    };
                    // JSON 직렬화
                    var jsonPayload = JsonSerializer.Serialize(payload, options);
                    var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

                    // POST 요청
                    HttpResponseMessage response = await client.PostAsync(urlSend, content);
                    response.EnsureSuccessStatusCode(); // 상태 코드가 200-299가 아니면 예외 발생

                    // JSON 응답 역직렬화
                    string jsonResponse = await response.Content.ReadAsStringAsync();
                    return jsonResponse;
                }
            }
            catch (HttpRequestException e)
            {
                return null;
            }
        }

        private static object GetRequestResultFormat(string? jsonResult)
        {
            var resultPack = JsonSerializer.Deserialize<Dictionary<string, object>>(jsonResult);
            var error = resultPack["error"];
            if (error != null)
            {
                string errorDetail = JsonSerializer.Deserialize<string>(JsonSerializer.Serialize(error));
                ModernWpf.MessageBox.Show(errorDetail, "에러", MessageBoxButton.OK);
                return null;
            }
            return resultPack["result"];
        }

        private static object ProcessChartOption(ChartOption option)
        {
            var result = new
            {
                key = option.Key,
                value = option.Value,
                type = option.Type,
                lines = option.LinesOption != null ? ProcessChartLineOption(option.LinesOption) : null,
                columns = option.AddedColumnOptions != null ? ProcessChartAddedColumnOption(option.AddedColumnOptions) : null
            };

            return result;
        }

        private static object ProcessChartAddedColumnOption(ObservableCollection<ChartColumnOption> addedColumnOptions)
        {
            return addedColumnOptions.Select(c => new
            {
                column = c.Column,
                linestyle = c.LineStyle,
                linewidth = c.LineWidth,
                linecolor = c.Color,
                marker = c.Marker,
                marker_size = c.MarkerSize,
                label = c.Label,
                is_secondary_axis = c.IsSecondaryAxis
            }).ToList();
        }

        private static object ProcessChartLineOption(ObservableCollection<ChartLineOption> linesOption)
        {
            return linesOption.Select(l => new
            {
                axis = l.Axis,
                kind = l.Kind,
                is_custom_double = l.IsCustomValueDouble,
                custom_value = l.CustomValue != null ? ((double)l.CustomValue).ToString("E5") : string.Empty,
                custom_dt = l.CustomDateTime != null ? l.CustomDateTime : string.Empty,
                linestyle = l.LineStyle,
                linewidth = l.LineWidth,
                linecolor = l.Color,
                text = l.Text,
                text_va = l.TextAlignVertical,
                text_ha = l.TextAlignHorizontal,
                text_rotate = l.TextRotation
            }).ToList();
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
