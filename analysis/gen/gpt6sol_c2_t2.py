DATA_T2 = {}

DATA_T2["T350"] = {
"python": r'''SEPARATOR = " "

class EchoProcessor:
    def getName(self, value):
        return "" if value == "" else value

_highProcessor = EchoProcessor()
_lowProcessor = EchoProcessor()

def getPartDivider():
    return 3

def getToken():
    return "thousand"

def getName(value):
    buffer = []
    high, low = "", ""
    if len(value) < getPartDivider():
        high = ""
        low = value
    else:
        index = len(value) - getPartDivider()
        high = value[0:index]
        low = value[index:]
    highName = _highProcessor.getName(high)
    lowName = _lowProcessor.getName(low)
    if highName != "":
        buffer.append(highName)
        buffer.append(SEPARATOR)
        buffer.append(getToken())
        if lowName != "":
            buffer.append(SEPARATOR)
    if lowName != "":
        buffer.append(lowName)
    return "".join(buffer)
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SEPARATOR " "

static int getPartDivider (void) { return 3; }
static const char *getToken (void) { return "thousand"; }

static const char *highProcessorGetName (const char *value) {
    return value [0] == '\0' ? "" : value;
}

static const char *lowProcessorGetName (const char *value) {
    return value [0] == '\0' ? "" : value;
}

static char *getName (const char *value) {
    char *buffer = malloc (256);
    if (buffer == NULL) return NULL;
    buffer [0] = '\0';
    char high [128], low [128];
    int len = (int) strlen (value);
    if (len < getPartDivider ()) {
        high [0] = '\0';
        strcpy (low, value);
    } else {
        int index = len - getPartDivider ();
        memcpy (high, value, index);
        high [index] = '\0';
        strcpy (low, value + index);
    }
    const char *highName = highProcessorGetName (high);
    const char *lowName = lowProcessorGetName (low);
    if (highName [0] != '\0') {
        strcat (buffer, highName);
        strcat (buffer, SEPARATOR);
        strcat (buffer, getToken ());
        if (lowName [0] != '\0') strcat (buffer, SEPARATOR);
    }
    if (lowName [0] != '\0') strcat (buffer, lowName);
    return buffer;
}
''',
"csharp": r'''using System;
using System.Text;

public class HighLowNameBuilder
{
    private const string SEPARATOR = " ";

    private int GetPartDivider() { return 3; }

    private string GetToken() { return "thousand"; }

    private string HighProcessorGetName(string value)
    {
        return string.IsNullOrEmpty(value) ? "" : value;
    }

    private string LowProcessorGetName(string value)
    {
        return string.IsNullOrEmpty(value) ? "" : value;
    }

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
        string highName = HighProcessorGetName(high);
        string lowName = LowProcessorGetName(low);
        if (!"".Equals(highName))
        {
            buffer.Append(highName);
            buffer.Append(SEPARATOR);
            buffer.Append(GetToken());
            if (!"".Equals(lowName))
            {
                buffer.Append(SEPARATOR);
            }
        }
        if (!"".Equals(lowName))
        {
            buffer.Append(lowName);
        }
        return buffer.ToString();
    }
}
''',
}

DATA_T2["T815"] = {
"python": r'''import calendar as cal_lib

year = 2024
monthNo = 5
day = 12

def getNextMonth(maxDate):
    nextYear, nextMonth = (year + 1, 1) if monthNo == 12 else (year, monthNo + 1)
    if maxDate:
        d = cal_lib.monthrange(nextYear, nextMonth)[1]
    else:
        d = day
    return str(nextYear) + "-" + str(nextMonth) + "-" + str(d)
''',
"c": r'''#include <stdio.h>

static int year = 2024, monthNo = 5, day = 12;

static int isLeap (int y) {
    return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
}

static int daysInMonth (int y, int m) {
    static const int days [] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (m == 2 && isLeap (y)) return 29;
    return days [m - 1];
}

static char *getNextMonth (int maxDate) {
    static char date [32];
    int nextYear = year, nextMonth = monthNo + 1;
    if (nextMonth > 12) {
        nextMonth = 1;
        nextYear ++;
    }
    int d = maxDate ? daysInMonth (nextYear, nextMonth) : day;
    sprintf (date, "%d-%d-%d", nextYear, nextMonth, d);
    return date;
}
''',
"csharp": r'''using System;

public class MonthNavigator
{
    private int year = 2024;
    private int monthNo = 5;
    private int day = 12;

    public string GetNextMonth(bool maxDate)
    {
        DateTime calendar = new DateTime(year, monthNo, 1).AddMonths(1);
        if (maxDate)
        {
            int maxD = DateTime.DaysInMonth(calendar.Year, calendar.Month);
            calendar = new DateTime(calendar.Year, calendar.Month, maxD);
        }
        else
        {
            calendar = new DateTime(calendar.Year, calendar.Month, day);
        }
        return calendar.Year + "-" + calendar.Month + "-" + calendar.Day;
    }
}
''',
}
