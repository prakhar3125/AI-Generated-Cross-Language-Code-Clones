DATA_B5 = {
"T614": {
"python": r"""
import re

class Log:
    @staticmethod
    def d(tag, message):
        print(tag + ": " + message)

mo_pattern = re.compile(r"[a-z]+")

class Spanned:
    def __init__(self, text=""):
        self.text = text

    def __str__(self):
        return self.text

    def toString(self):
        return self.text

def filter(source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    Log.d("debug", mo_pattern.pattern)
    Log.d("debug", "source: " + str(source) + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + str(dest) + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = dest.toString()
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        Log.d("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = str(source)
            Log.d("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        Log.d("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        Log.d("debug", "lsText  : " + ls_text)
    if mo_pattern.fullmatch(ls_text) is None:
        return ""
    return None
""",
"c": r"""
#include <stdio.h>
#include <string.h>

/* minimal stand-ins for Android Log and java.util.regex */
extern int regex_full_match(const char *pattern, const char *text);

static void log_d(const char *tag, const char *message) {
    printf("%s: %s\n", tag, message);
}

const char *filter(const char *source, int start, int end,
                   const char *dest, int dstart, int dend) {
    char ls_start[256];
    char ls_insert[256];
    char ls_end[256];
    char ls_text[512];
    ls_start[0] = '\0';
    ls_insert[0] = '\0';
    ls_end[0] = '\0';
    ls_text[0] = '\0';
    log_d("debug", "pattern");
    if (strlen(dest) > 0) {
        int len = (int)strlen(dest);
        int ds = dstart < len ? dstart : len;
        int de = dend < len ? dend : len;
        int i;
        for (i = 0; i < ds; i++) ls_start[i] = dest[i];
        ls_start[i] = '\0';
        strncpy(ls_insert, source, sizeof(ls_insert) - 1);
        ls_insert[sizeof(ls_insert) - 1] = '\0';
        for (i = 0; de + i < len; i++) ls_end[i] = dest[de + i];
        ls_end[i] = '\0';
        snprintf(ls_text, sizeof(ls_text), "%s%s%s", ls_start, ls_insert, ls_end);
        log_d("debug", ls_text);
    }
    if (!regex_full_match("pattern", ls_text)) {
        return "";
    }
    return NULL;
}
""",
"csharp": r"""
using System;
using System.Text.RegularExpressions;

public static class AndroidLog
{
    public static void D(string tag, object message)
    {
        Console.WriteLine(tag + ": " + message);
    }
}

public class InputFilter
{
    private Regex moPattern = new Regex("[a-z]+");

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = "";
        AndroidLog.D("debug", moPattern.ToString());
        AndroidLog.D("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
        lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            AndroidLog.D("debug", "lsStart : " + lsStart);
            if (source != "")
            {
                lsInsert = source.ToString();
                AndroidLog.D("debug", "lsInsert: " + lsInsert);
            }
            lsEnd = lsText.Substring(dend);
            AndroidLog.D("debug", "lsEnd   : " + lsEnd);
            lsText = lsStart + lsInsert + lsEnd;
            AndroidLog.D("debug", "lsText  : " + lsText);
        }
        if (!moPattern.IsMatch(lsText))
        {
            return "";
        }
        return null;
    }
}
"""
}
}
