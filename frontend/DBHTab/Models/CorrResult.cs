namespace DBHTab.Models
{
    public class CorrResult
    {
        public string Column1 { get; set; } = default!;
        public string Column2 { get; set; } = default!;
        public int SampleCount { get; set; } = default!;
        public float? Coefficient { get; set; }
        public float? ConfidenceIntervalLower { get; set; }
        public float? ConfidenceIntervalUpper { get; set; }
        public float? PValue { get; set; }
        public string? CorrelationLevel { get; set; }
    }
}
