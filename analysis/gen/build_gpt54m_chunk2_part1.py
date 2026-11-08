DATA_T1 = {
    "T673": {
        "python": r'''import re


class _DebugPattern:
    def __init__(self, regex):
        self._compiled = re.compile(regex)

    def fullmatch(self, text):
        return self._compiled.fullmatch(text)

    def __str__(self):
        return self._compiled.pattern


def _log(tag, message):
    print(tag + ": " + str(message))


mo_pattern = _DebugPattern(".*")


def filter(source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    _log("debug", str(mo_pattern))
    _log("debug", "source: " + str(source) + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + str(dest) + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = str(dest)
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        _log("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = str(source)
            _log("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        _log("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        _log("debug", "lsText  : " + ls_text)
    match = mo_pattern.fullmatch(ls_text)
    _log("debug", "loMatcher.matches(): " + str(match is not None) + ", lsText: " + ls_text)
    if match is None:
        return ""
    return None''',
        "c": r'''#include <stdio.h>
#include <string.h>

extern const char *MO_PATTERN;
extern int pattern_matches_full(const char *regex, const char *text);
extern void debug_log(const char *tag, const char *message);

const char *filter(const char *source, int start, int end, const char *dest,
                   int dstart, int dend) {
    static char ls_text[1024];
    char ls_start[512];
    char ls_insert[512];
    char ls_end[512];
    ls_start[0] = '\0';
    ls_insert[0] = '\0';
    ls_end[0] = '\0';
    size_t len = strlen(dest);
    debug_log("debug", MO_PATTERN);
    if (len > 0) {
        snprintf(ls_start, sizeof(ls_start), "%.*s", dstart, dest);
        debug_log("debug", "lsStart");
        if (source != NULL && source[0] != '\0') {
            snprintf(ls_insert, sizeof(ls_insert), "%s", source);
        }
        snprintf(ls_end, sizeof(ls_end), "%s", dest + dend);
        debug_log("debug", "lsEnd");
        snprintf(ls_text, sizeof(ls_text), "%s%s%s", ls_start, ls_insert, ls_end);
        debug_log("debug", "lsText");
    }
    if (!pattern_matches_full(MO_PATTERN, ls_text)) {
        return "";
    }
    return NULL;
}''',
        "csharp": r'''using System;
using System.Text.RegularExpressions;

public class TextFilter
{
    private static readonly Regex MoPattern = new Regex(".*");

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = "";
        System.Diagnostics.Debug.WriteLine("debug: " + MoPattern.ToString());
        lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            if (source != "") lsInsert = source;
            lsEnd = lsText.Substring(dend);
            lsText = lsStart + lsInsert + lsEnd;
        }
        if (!MoPattern.IsMatch(lsText))
        {
            return "";
        }
        return null;
    }
}'''
    },
    "T452": {
        "python": r'''import re


def main():
    text = "my name is khan"
    words = re.split(r"\s", text)
    capitalized_word = ""
    for w in words:
        first = w[:1]
        rest = w[1:]
        capitalized_word += first.upper() + rest + " "
    print(capitalized_word)''',
        "c": r'''#include <stdio.h>
#include <string.h>
#include <ctype.h>

void capitalize_words(const char *str) {
    char buf[256];
    snprintf(buf, sizeof(buf), "%s", str);
    char *word = strtok(buf, " \t\n\r\f\v");
    while (word != NULL) {
        if (word[0] != '\0') {
            printf("%c%s ", toupper((unsigned char)word[0]), word + 1);
        }
        word = strtok(NULL, " \t\n\r\f\v");
    }
    printf("\n");
}''',
        "csharp": r'''using System;
using System.Text.RegularExpressions;

public static class WordCapitalizer
{
    public static void Main(string[] args)
    {
        string str = "my name is khan";
        string[] words = Regex.Split(str, "\s");
        string capitalizedWord = "";
        foreach (string w in words)
        {
            string first = w.Substring(0, 1);
            string rest = w.Substring(1);
            capitalizedWord += first.ToUpper() + rest + " ";
        }
        Console.WriteLine(capitalizedWord);
    }
}'''
    }
}
