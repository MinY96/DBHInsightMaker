using System.Text.Json;

namespace DBHTab.Converters
{
    public class DateTimeConvertorJson : System.Text.Json.Serialization.JsonConverter<DateTime>
    {
        public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            if (reader.TokenType == JsonTokenType.String)
            {
                var dateString = reader.GetString();
                return DateTime.Parse(dateString); // 문자열을 DateTime으로 변환
            }
            throw new JsonException();
        }

        public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
        {
            writer.WriteStringValue(value.ToString("yyyy-MM-dd HH:mm:ss")); // DateTime을 문자열로 변환
        }
    }
}
