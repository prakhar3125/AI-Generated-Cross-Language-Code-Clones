DATA_T3 = {
    "T341": {
        "python": r'''def output(four_letter, five_letter, six_letter):
    answer = ""
    count = 1
    longest = max(max(len(four_letter), len(five_letter)), len(six_letter))
    for i in range(longest):
        if len(six_letter) > i:
            answer += six_letter[i] + " "
        if len(five_letter) > i:
            answer += five_letter[i] + " "
        if len(four_letter) > i:
            answer += four_letter[i]
        answer += "\n" + "\t" * count
        count += 1
    return answer''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *output(char *four_letter[], int four_len, char *five_letter[], int five_len,
             char *six_letter[], int six_len) {
    char *answer = malloc(4096);
    answer[0] = '\0';
    char tmp[512];
    int count = 1;
    int longest = four_len;
    if (five_len > longest) longest = five_len;
    if (six_len > longest) longest = six_len;
    for (int i = 0; i < longest; i++) {
        if (six_len > i) {
            snprintf(tmp, sizeof(tmp), "%s ", six_letter[i]);
            strcat(answer, tmp);
        }
        if (five_len > i) {
            snprintf(tmp, sizeof(tmp), "%s ", five_letter[i]);
            strcat(answer, tmp);
        }
        if (four_len > i) {
            strcat(answer, four_letter[i]);
        }
        strcat(answer, "\n");
        for (int j = 0; j < count; j++) {
            strcat(answer, "\t");
        }
        count++;
    }
    return answer;
}''',
        "csharp": r'''using System;

public static class Interleaver
{
    public static string Output(string[] fourLetter, string[] fiveLetter, string[] sixLetter)
    {
        string answer = "";
        int count = 1;
        int longest = Math.Max(Math.Max(fourLetter.Length, fiveLetter.Length), sixLetter.Length);
        for (int i = 0; i < longest; i++)
        {
            if (sixLetter.Length > i) answer += sixLetter[i] + " ";
            if (fiveLetter.Length > i) answer += fiveLetter[i] + " ";
            if (fourLetter.Length > i) answer += fourLetter[i];
            answer += "\n" + new string('\t', count);
            count++;
        }
        return answer;
    }
}'''
    },
    "T350": {
        "python": r'''SEPARATOR = " "
_TOKEN = "hundred"


class _Processor:
    def get_name(self, value):
        return value


def get_part_divider():
    return 3


_high_processor = _Processor()
_low_processor = _Processor()


def get_name(value):
    buffer = []
    high, low = "", ""
    if len(value) < get_part_divider():
        high = ""
        low = value
    else:
        index = len(value) - get_part_divider()
        high = value[:index]
        low = value[index:]
    high_name = _high_processor.get_name(high)
    low_name = _low_processor.get_name(low)
    if high_name != "":
        buffer.append(high_name)
        buffer.append(SEPARATOR)
        buffer.append(_TOKEN)
        if low_name != "":
            buffer.append(SEPARATOR)
    if low_name != "":
        buffer.append(low_name)
    return "".join(buffer)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern const char *SEPARATOR;
extern const char *TOKEN;
extern int get_part_divider(void);
extern void get_high_processor_name(const char *value, char *out, size_t out_size);
extern void get_low_processor_name(const char *value, char *out, size_t out_size);

char *get_name(const char *value) {
    char *buffer = malloc(1024);
    buffer[0] = '\0';
    char high[256], low[256];
    size_t len = strlen(value);
    int divider = get_part_divider();
    if (len < (size_t)divider) {
        high[0] = '\0';
        snprintf(low, sizeof(low), "%s", value);
    } else {
        size_t index = len - (size_t)divider;
        snprintf(high, sizeof(high), "%.*s", (int)index, value);
        snprintf(low, sizeof(low), "%s", value + index);
    }
    char high_name[256], low_name[256];
    get_high_processor_name(high, high_name, sizeof(high_name));
    get_low_processor_name(low, low_name, sizeof(low_name));
    if (high_name[0] != '\0') {
        strcat(buffer, high_name);
        strcat(buffer, SEPARATOR);
        strcat(buffer, TOKEN);
        if (low_name[0] != '\0') {
            strcat(buffer, SEPARATOR);
        }
    }
    if (low_name[0] != '\0') {
        strcat(buffer, low_name);
    }
    return buffer;
}''',
        "csharp": r'''using System.Text;

public class NameFormatter
{
    private const string Separator = " ";
    private const string Token = "hundred";

    private static int GetPartDivider() => 3;
    private static string GetHighProcessorName(string value) => value;
    private static string GetLowProcessorName(string value) => value;

    public string GetName(string value)
    {
        var buffer = new StringBuilder();
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
        string highName = GetHighProcessorName(high);
        string lowName = GetLowProcessorName(low);
        if (highName != "")
        {
            buffer.Append(highName);
            buffer.Append(Separator);
            buffer.Append(Token);
            if (lowName != "")
            {
                buffer.Append(Separator);
            }
        }
        if (lowName != "")
        {
            buffer.Append(lowName);
        }
        return buffer.ToString();
    }
}'''
    },
    "T815": {
        "python": r'''import calendar


year = 2018
month_no = 0
day = 1


def get_next_month(max_date):
    if month_no == 11:
        next_year, next_month = year + 1, 0
    else:
        next_year, next_month = year, month_no + 1
    if max_date:
        day_value = calendar.monthrange(next_year, next_month + 1)[1]
    else:
        day_value = day
    return str(next_year) + "-" + str(next_month + 1) + "-" + str(day_value)''',
        "c": r'''#include <stdio.h>
#include <stddef.h>

int year = 2018, month_no = 1, day = 1;

static int days_in_month(int y, int m) {
    static const int d[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (m == 2) {
        int leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        return leap ? 29 : 28;
    }
    return d[m - 1];
}

void get_next_month(int max_date, char *out, size_t out_size) {
    int y = year, m = month_no + 1;
    if (m > 12) {
        m = 1;
        y = y + 1;
    }
    int d = max_date ? days_in_month(y, m) : day;
    snprintf(out, out_size, "%d-%d-%d", y, m, d);
}''',
        "csharp": r'''using System;

public class MonthNavigator
{
    public int Year { get; set; }
    public int MonthNo { get; set; }
    public int Day { get; set; }

    public string GetNextMonth(bool maxDate)
    {
        DateTime next = new DateTime(Year, MonthNo, 1).AddMonths(1);
        int dayValue = maxDate ? DateTime.DaysInMonth(next.Year, next.Month) : Day;
        return next.Year + "-" + next.Month + "-" + dayValue;
    }
}'''
    }
}
