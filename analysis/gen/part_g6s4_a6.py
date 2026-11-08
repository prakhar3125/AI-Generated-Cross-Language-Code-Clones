DATA_A6 = {
"T314": {
"python": r"""
SEPARATOR = " "

class Processor:
    def get_name(self, value):
        return value

class NumberNameMapper:
    def __init__(self, part_divider=2):
        self.part_divider = part_divider
        self.high_processor = Processor()
        self.low_processor = Processor()

    def get_part_divider(self):
        return self.part_divider

    def get_high_processor(self):
        return self.high_processor

    def get_low_processor(self):
        return self.low_processor

    def get_token(self):
        return "thousand"

    def get_name(self, value):
        buffer = []
        if len(value) < self.get_part_divider():
            high = ""
            low = value
        else:
            index = len(value) - self.get_part_divider()
            high = value[:index]
            low = value[index:]
        high_name = self.get_high_processor().get_name(high)
        low_name = self.get_low_processor().get_name(low)
        if high_name != "":
            buffer.append(high_name)
            buffer.append(SEPARATOR)
            buffer.append(self.get_token())
            if low_name != "":
                buffer.append(SEPARATOR)
        if low_name != "":
            buffer.append(low_name)
        return "".join(buffer)
""",
"c": r"""
#include <stdio.h>
#include <string.h>

#define SEPARATOR " "
#define TOKEN "thousand"

static int get_part_divider(void) { return 2; }

static void get_name(const char *value, char *out, size_t out_size) {
    int len = (int)strlen(value);
    int divider = get_part_divider();
    char high[64], low[64];
    if (len < divider) {
        high[0] = '\0';
        strncpy(low, value, sizeof(low) - 1);
        low[sizeof(low) - 1] = '\0';
    } else {
        int index = len - divider;
        strncpy(high, value, (size_t)index);
        high[index] = '\0';
        strncpy(low, value + index, sizeof(low) - 1);
        low[sizeof(low) - 1] = '\0';
    }
    snprintf(out, out_size, "%s%s%s%s%s", high,
             high[0] != '\0' ? SEPARATOR : "",
             high[0] != '\0' ? TOKEN : "",
             (high[0] != '\0' && low[0] != '\0') ? SEPARATOR : "",
             low);
}
""",
"csharp": r"""
using System.Text;

public class NumberProcessor
{
    public string GetName(string value) { return value; }
}

public class NumberNameMapper
{
    private const string SEPARATOR = " ";
    private int partDivider = 2;

    public int GetPartDivider() { return partDivider; }
    public NumberProcessor GetHighProcessor() { return new NumberProcessor(); }
    public NumberProcessor GetLowProcessor() { return new NumberProcessor(); }
    public string GetToken() { return "thousand"; }

    public string GetName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        string high, low;
        if (value.Length < GetPartDivider())
        {
            high = "";
            low = value;
        }
        else
        {
            int index = value.Length - GetPartDivider();
            high = value.Substring(0, index);
            low = value.Substring(index);
        }
        string highName = GetHighProcessor().GetName(high);
        string lowName = GetLowProcessor().GetName(low);
        if (!highName.IsEmpty())
        {
            buffer.Append(highName);
            buffer.Append(SEPARATOR);
            buffer.Append(GetToken());
            if (!lowName.IsEmpty())
            {
                buffer.Append(SEPARATOR);
            }
        }
        if (!lowName.IsEmpty())
        {
            buffer.Append(lowName);
        }
        return buffer.ToString();
    }
}

public static class StringExtensions
{
    public static bool IsEmpty(this string s) { return string.IsNullOrEmpty(s); }
}
"""
}
}
