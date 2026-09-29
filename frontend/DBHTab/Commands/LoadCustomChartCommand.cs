using DBHTab.Models;
using DBHTab.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace DBHTab.Commands
{
    public class LoadCustomChartCommand : CommandBase
    {
        #region Field Variables

        private CustomChartViewModel _customChartViewModel;

        #endregion

        #region Initialize

        public LoadCustomChartCommand(CustomChartViewModel customChartViewModel)
        {
            _customChartViewModel = customChartViewModel;
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
            {
                return false;
            }
            if (parameter.Length != 5)
            {
                return false;
            }
            string projectDir = parameter[0] as string;
            string chartGroup = parameter[1] as string;
            string chartType = parameter[2] as string;                        
            IEnumerable<ChartOption> options = parameter[3] as IEnumerable<ChartOption>;
            bool isCreatingChart = (bool)parameter[4];
            if (string.IsNullOrEmpty(projectDir) ||
                string.IsNullOrEmpty(chartGroup) ||
                string.IsNullOrEmpty(chartType))
            {
                return false;
            }
            if (options.Where(o => o.Name.Contains("필수선택")).Count(o => string.IsNullOrEmpty(o.Value))>0)
            {
                _customChartViewModel.ShowDisabledReason("컬럼을 선택하지 않았습니다.");
                return false;
            }
            if (isCreatingChart)
                return false;
            var keysToCheck = new HashSet<string> { "x_num", "y_num", "z_num", "g_num", "x_cat", "y_cat", "z_cat", "g_cat", "x_dt" };
            var filteredInfos = options.Where(o => keysToCheck.Contains(o.Key));
            var duplicates = filteredInfos.GroupBy(o => o.Value)
                .Where(g => g.Count() > 1)
                .Select(g => new { Value = g.Key, Keys = g.Select(o => o.Key) });
            if (duplicates.Any())
            {
                var messages = duplicates.Select(d => $"{string.Join(",", d.Keys)} 이 동일한 컬럼을 가지고 있습니다.:{d.Value}");
                _customChartViewModel.ShowDisabledReason(string.Join("", messages));
                return false;
            }

            var ynums = options.FirstOrDefault(o => o.Key == "y_nums");
            if (ynums!=null)
            {
                if (ynums.AddedColumnOptions==null || ynums.AddedColumnOptions.Count==0)
                {
                    _customChartViewModel.ShowDisabledReason("Y축 컬럼을 1개 이상 추가해주세요.");
                    return false;
                }
                var ycols = ynums.AddedColumnOptions
                    .Where(c => c.Column!=null)
                    .Select(c => c.Column).ToList();
                if (ycols.Count != ynums.AddedColumnOptions.Count)
                {
                    _customChartViewModel.ShowDisabledReason("Y축 컬럼을 지정해주세요.");
                    return false;
                }
                if (ycols.Count != ycols.Distinct().Count())
                {
                    _customChartViewModel.ShowDisabledReason("중복된 컬럼을 지정하였습니다.");
                    return false;
                }
            }

            var lineInfos = options.FirstOrDefault(o => o.Key == "lines");
            if (lineInfos!=null && lineInfos.LinesOption!=null)
            {
                var lineOps = lineInfos.LinesOption.FirstOrDefault(o => string.IsNullOrEmpty(o.Axis));
                if (lineOps != null)
                {
                    _customChartViewModel.ShowDisabledReason("추가할 선의 방향을 선택해주세요.");
                    return false;
                }
                lineOps = lineInfos.LinesOption.FirstOrDefault(o => string.IsNullOrEmpty(o.Kind));
                if (lineOps != null)
                {
                    _customChartViewModel.ShowDisabledReason("추가할 선의 종류를 선택해주세요.");
                    return false;
                }
                lineOps = lineInfos.LinesOption.FirstOrDefault(o => string.IsNullOrEmpty(o.LineStyle));
                if (lineOps != null)
                {
                    _customChartViewModel.ShowDisabledReason("추가할 선의 라인 스타일을 선택해주세요.");
                    return false;
                }
                var keysToCheckKind = new HashSet<string> { "최대값 인덱스(최초)", "최대값 인덱스(전체)", "최소값 인덱스(최초)", "최소값 인덱스(전체)" };
                var filteredChartLineInfos = lineInfos.LinesOption.Where(o => keysToCheckKind.Contains(o.Kind) && o.Axis == "수평").ToList();
                if (filteredChartLineInfos.Count > 0)
                {
                    var errorKind = string.Join(",", filteredChartLineInfos.Select(g => g.Kind));
                    _customChartViewModel.ShowDisabledReason($"수평선 추가 시 ({errorKind})는 사용할 수 없습니다.");
                    return false;
                }
                keysToCheckKind = new HashSet<string> { "최대값", "최소값", "평균값", "중앙값", "μ+1σ", "μ+2σ", "μ+3σ", "μ-1σ", "μ-2σ", "μ-3σ" };
                filteredChartLineInfos = lineInfos.LinesOption.Where(o => keysToCheckKind.Contains(o.Kind) && o.Axis == "수직").ToList();
                if (filteredChartLineInfos.Count > 0)
                {
                    var errorKind = string.Join(",", filteredChartLineInfos.Select(g => g.Kind));
                    _customChartViewModel.ShowDisabledReason($"수직선 추가 시 ({errorKind})는 사용할 수 없습니다.");
                    return false;
                }
                lineOps = lineInfos.LinesOption.FirstOrDefault(o => o.Kind == "사용자 지정");
                if ((lineOps != null && lineOps.IsCustomValueDouble && lineOps.CustomValue==null) ||
                    (lineOps != null && !lineOps.IsCustomValueDouble && string.IsNullOrEmpty(lineOps.CustomDateTime)))
                {
                    _customChartViewModel.ShowDisabledReason("사용자 지정 값을 입력해주세요.");
                    return false;
                }
            }

            _customChartViewModel.ShowDisabledReason(string.Empty);
            return true;
        }

        public override void Execute(object? parameters)
        {
            var parameter = (object[])parameters;
            string projectDir = parameter[0] as string;
            string chartGroup = parameter[1] as string;
            string chartType = parameter[2] as string;
            IEnumerable<ChartOption> options = parameter[3] as IEnumerable<ChartOption>;
            LoadCustomChart(projectDir, chartGroup, chartType, options);
        }

        #endregion

        #region Private Methods

        private async void LoadCustomChart(string? projectDir, string corrMethod, string? chartType, IEnumerable<ChartOption> options)
        {
            _customChartViewModel.IsCreatingChart = true;
            ChartInfo customChart = await HttpRequest.PostCustomChart(projectDir, corrMethod, chartType, options);            

            _customChartViewModel.UpdateCustomChart(customChart);
        }

        #endregion

        #region Protected Methods
        #endregion
    }
}
