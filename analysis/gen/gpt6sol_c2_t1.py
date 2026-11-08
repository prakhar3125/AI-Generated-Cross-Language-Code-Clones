DATA_T1 = {}

DATA_T1["T673"] = {
"python": r'''import re

class Log:
    @staticmethod
    def d(tag, msg):
        pass

class Matcher:
    def __init__(self, compiled, text):
        self._compiled = compiled
        self._text = text
    def matches(self):
        return self._compiled.fullmatch(self._text) is not None

class Pattern:
    def __init__(self, pattern):
        self._pattern = pattern
        self._compiled = re.compile(pattern)
    def __str__(self):
        return self._pattern
    def matcher(self, text):
        return Matcher(self._compiled, text)

moPattern = Pattern("[0-9]*")

def filter(source, start, end, dest, dstart, dend):
    lsStart = ""
    lsInsert = ""
    lsEnd = ""
    lsText = ""
    Log.d("debug", str(moPattern))
    Log.d("debug", "source: " + source + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + dest + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    lsText = dest
    if len(lsText) > 0:
        lsStart = lsText[0:dstart]
        Log.d("debug", "lsStart : " + lsStart)
        if source != "":
            lsInsert = source
            Log.d("debug", "lsInsert: " + lsInsert)
        lsEnd = lsText[dend:]
        Log.d("debug", "lsEnd   : " + lsEnd)
        lsText = lsStart + lsInsert + lsEnd
        Log.d("debug", "lsText  : " + lsText)
    loMatcher = moPattern.matcher(lsText)
    Log.d("debug", "loMatcher.matches(): " + str(loMatcher.matches()) + ", lsText: " + lsText)
    if not loMatcher.matches():
        return ""
    return None
''',
"c": r'''#include <stdio.h>
#include <string.h>

static void Log_d (const char *tag, const char *msg) {
    (void) tag;
    (void) msg;
}

static const char *moPattern = "[0-9]*";

extern int pattern_matches_full (const char *pattern, const char *text);

static char *filter (const char *source, int start, int end,
                     const char *dest, int dstart, int dend) {
    char lsStart [256] = "";
    char lsInsert [256] = "";
    char lsEnd [256] = "";
    char lsText [512] = "";
    char msg [640];
    Log_d ("debug", moPattern);
    sprintf (msg, "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d",
             source, start, end, dest, dstart, dend);
    Log_d ("debug", msg);
    strcpy (lsText, dest);
    if (strlen (lsText) > 0) {
        int n = (int) strlen (lsText);
        if (dstart > n) dstart = n;
        if (dend > n) dend = n;
        strncpy (lsStart, lsText, dstart);
        lsStart [dstart] = '\0';
        Log_d ("debug", "lsStart");
        if (source [0] != '\0') {
            strcpy (lsInsert, source);
            Log_d ("debug", "lsInsert");
        }
        strcpy (lsEnd, lsText + dend);
        Log_d ("debug", "lsEnd");
        strcpy (lsText, lsStart);
        strcat (lsText, lsInsert);
        strcat (lsText, lsEnd);
        Log_d ("debug", "lsText");
    }
    if (! pattern_matches_full (moPattern, lsText)) {
        return "";
    }
    return NULL;
}
''',
"csharp": r'''using System;
using System.Text.RegularExpressions;

public class Spanned
{
    public string Text;
}

public static class DebugLog
{
    public static void D(string tag, object msg) { }
}

public class Pattern
{
    private readonly Regex _regex;
    private readonly string _pattern;

    public Pattern(string pattern)
    {
        _pattern = pattern;
        _regex = new Regex("^(?:" + pattern + ")$");
    }

    public override string ToString() { return _pattern; }

    public Matcher Matcher(string text) { return new Matcher(_regex, text); }
}

public class Matcher
{
    private readonly Regex _regex;
    private readonly string _text;

    public Matcher(Regex regex, string text) { _regex = regex; _text = text; }

    public bool Matches() { return _regex.IsMatch(_text); }
}

public class InputFilterDemo
{
    private static Pattern moPattern = new Pattern("[0-9]*");

    public string Filter(string source, int start, int end, Spanned dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = "";
        DebugLog.D("debug", moPattern.ToString());
        DebugLog.D("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
        lsText = dest.Text;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            DebugLog.D("debug", "lsStart : " + lsStart);
            if (!string.IsNullOrEmpty(source))
            {
                lsInsert = source;
                DebugLog.D("debug", "lsInsert: " + lsInsert);
            }
            lsEnd = lsText.Substring(dend);
            DebugLog.D("debug", "lsEnd   : " + lsEnd);
            lsText = lsStart + lsInsert + lsEnd;
            DebugLog.D("debug", "lsText  : " + lsText);
        }
        Matcher loMatcher = moPattern.Matcher(lsText);
        DebugLog.D("debug", "loMatcher.matches(): " + loMatcher.Matches() + ", lsText: " + lsText);
        if (!loMatcher.Matches())
        {
            return "";
        }
        return null;
    }
}
''',
}

DATA_T1["T452"] = {
"python": r'''import re

def main():
    s = "my name is khan"
    words = re.split(r"\s", s)
    capitalizedWord = ""
    for w in words:
        first = w[0:1]
        f_after = w[1:]
        capitalizedWord += first.upper() + f_after + " "
    print(capitalizedWord)

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main (void) {
    char str [] = "my name is khan";
    char *words [16];
    int count = 0;
    char *token = strtok (str, " ");
    while (token != NULL) {
        words [count ++] = token;
        token = strtok (NULL, " ");
    }
    for (int i = 0; i < count; i ++) {
        char first = (char) toupper ((unsigned char) words [i] [0]);
        printf ("%c%s ", first, words [i] + 1);
    }
    printf ("\n");
    return 0;
}
''',
"csharp": r'''using System;

public static class WordCapitalizer
{
    public static void Main(string[] args)
    {
        string str = "my name is khan";
        string[] words = str.Split(' ');
        string capitalizedWord = "";
        foreach (string w in words)
        {
            string first = w.Substring(0, 1);
            string f_after = w.Substring(1);
            capitalizedWord += first.ToUpper() + f_after + " ";
        }
        Console.WriteLine(capitalizedWord);
    }
}
''',
}

DATA_T1["T186"] = {
"python": r'''class Score:
    def __init__(self, kind, name, value):
        self.kind = kind
        self.name = name
        self.value = value

def main():
    input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)"
    scoreSets = input.split("),")
    scoreList = []
    for score in scoreSets:
        score = score.strip()[1:]
        closeBrace = score.find(")")
        if closeBrace == len(score) - 1:
            score = score[0:len(score) - 1]
        tokens = score.split(",")
        scoreList.append(Score(tokens[0], tokens[1], float(tokens[2])))

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char kind [32];
    char name [64];
    double value;
} Score;

int main (void) {
    const char *input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
    Score scoreList [16];
    int count = 0;
    const char *p = input;
    while (*p) {
        const char *open = strchr (p, '(');
        if (open == NULL) break;
        const char *close = strchr (open, ')');
        if (close == NULL) break;
        char inner [128];
        size_t len = (size_t) (close - open - 1);
        memcpy (inner, open + 1, len);
        inner [len] = '\0';
        char *tok = strtok (inner, ",");
        if (tok != NULL) {
            char *a = tok;
            char *b = strtok (NULL, ",");
            char *c = strtok (NULL, ",");
            if (b != NULL && c != NULL) {
                strcpy (scoreList [count].kind, a);
                strcpy (scoreList [count].name, b);
                scoreList [count].value = atof (c);
                count ++;
            }
        }
        p = close + 1;
    }
    (void) count;
    (void) scoreList;
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public class Score
{
    public string Kind;
    public string Name;
    public double Value;

    public Score(string kind, string name, double value)
    {
        Kind = kind;
        Name = name;
        Value = value;
    }
}

public static class ScoreParser
{
    public static void Main(string[] args)
    {
        string input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
        string[] scoreSets = input.Split(new string[] { ")," }, StringSplitOptions.None);
        List<Score> scoreList = new List<Score>();
        foreach (string rawScore in scoreSets)
        {
            string score = rawScore.Trim().Substring(1);
            int closeBrace = score.IndexOf(')');
            if (closeBrace == score.Length - 1)
            {
                score = score.Substring(0, score.Length - 1);
            }
            string[] tokens = score.Split(',');
            scoreList.Add(new Score(tokens[0], tokens[1], double.Parse(tokens[2])));
        }
    }
}
''',
}

DATA_T1["T271"] = {
"python": r'''def main():
    array = []
    print("Enter n:")
    n = int(input())
    print("Enter m:")
    m = int(input())
    print("Enter the values:")
    for i in range(n):
        row = []
        array.append(row)
        for j in range(m):
            row.append(int(input()))
    print("Result:")
    print(array)

main()
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

int main (void) {
    int n, m;
    printf ("Enter n:\n");
    if (scanf ("%d", & n) != 1) return 0;
    printf ("Enter m:\n");
    if (scanf ("%d", & m) != 1) return 0;
    printf ("Enter the values:\n");
    int **array = malloc (n * sizeof (int *));
    for (int i = 0; i < n; i ++) {
        int *list = malloc (m * sizeof (int));
        array [i] = list;
        for (int j = 0; j < m; j ++) {
            scanf ("%d", & list [j]);
        }
    }
    printf ("Result:\n");
    for (int i = 0; i < n; i ++) {
        printf ("[");
        for (int j = 0; j < m; j ++) {
            printf ("%d%s", array [i] [j], j + 1 < m ? ", " : "");
        }
        printf ("]%s", i + 1 < n ? ", " : "\n");
    }
    for (int i = 0; i < n; i ++) free (array [i]);
    free (array);
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class GridReader
{
    public static void Main(string[] args)
    {
        List<List<int>> array = new List<List<int>>();
        Console.WriteLine("Enter n:");
        int n = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter m:");
        int m = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter the values:");
        for (int i = 0; i < n; i++)
        {
            List<int> list = new List<int>();
            array.Add(list);
            for (int j = 0; j < m; j++)
            {
                list.Add(int.Parse(Console.ReadLine()));
            }
        }
        Console.WriteLine("Result:");
        Console.WriteLine("[" + string.Join(", ", array.ConvertAll(row => "[" + string.Join(", ", row) + "]")) + "]");
    }
}
''',
}

DATA_T1["T597"] = {
"python": r'''class HttpStatus:
    OK = "OK"
    BAD_REQUEST = "BAD_REQUEST"

class ResponseEntity:
    def __init__(self, body, status):
        self.body = body
        self.status = status

class HttpServletRequest:
    def __init__(self, productId):
        self._productId = productId
    def getProductId(self):
        return self._productId

class ProductService:
    def getProduct(self, productId):
        if productId is None:
            raise ValueError("missing product id")
        return "Product<" + productId + ">"

service = ProductService()

def match(matchId, body, request, response):
    try:
        p = service.getProduct(request.getProductId())
    except Exception:
        return ResponseEntity(None, HttpStatus.BAD_REQUEST)
    return ResponseEntity(p, HttpStatus.OK)
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { HTTP_OK, HTTP_BAD_REQUEST } HttpStatus;

typedef struct {
    char *body;
    HttpStatus status;
} ResponseEntity;

typedef struct {
    char productId [32];
} HttpServletRequest;

static char *getProduct (const char *productId) {
    char *p = malloc (strlen (productId) + 16);
    if (p == NULL) return NULL;
    sprintf (p, "Product<%s>", productId);
    return p;
}

ResponseEntity match (const char *matchId, const char *body,
                      const HttpServletRequest *request, void *response) {
    ResponseEntity result;
    result.body = NULL;
    result.status = HTTP_BAD_REQUEST;
    char *p = getProduct (request->productId);
    if (p == NULL) {
        return result;
    }
    result.body = p;
    result.status = HTTP_OK;
    return result;
}
''',
"csharp": r'''using System;

public enum HttpStatus { OK, BadRequest }

public class ResponseEntity
{
    public object Body;
    public HttpStatus Status;

    public ResponseEntity(object body, HttpStatus status)
    {
        Body = body;
        Status = status;
    }
}

public class HttpServletRequest
{
    public string GetProductId() { return "42"; }
}

public class ProductService
{
    public string GetProduct(string productId) { return "Product<" + productId + ">"; }
}

public class MatchController
{
    private static ProductService service = new ProductService();

    public ResponseEntity Match(string matchId, string body, HttpServletRequest request, object response)
    {
        try
        {
            var p = service.GetProduct(request.GetProductId());
            return new ResponseEntity(p, HttpStatus.OK);
        }
        catch (Exception)
        {
            return new ResponseEntity(null, HttpStatus.BadRequest);
        }
    }
}
''',
}

DATA_T1["T341"] = {
"python": r'''def output(fourLetter, fiveLetter, sixLetter):
    answer = ""
    count = 1
    maxLength = max(max(len(fourLetter), len(fiveLetter)), len(sixLetter))
    for i in range(maxLength):
        if len(sixLetter) > i:
            answer += sixLetter[i] + " "
        if len(fiveLetter) > i:
            answer += fiveLetter[i] + " "
        if len(fourLetter) > i:
            answer += fourLetter[i]
        answer += "\n"
        for j in range(count):
            answer += "\t"
        count += 1
    return answer
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *output (const char **fourLetter, int fourLen,
                     const char **fiveLetter, int fiveLen,
                     const char **sixLetter, int sixLen) {
    char *answer = malloc (4096);
    if (answer == NULL) return NULL;
    answer [0] = '\0';
    int count = 1;
    int maxLen = fourLen;
    if (fiveLen > maxLen) maxLen = fiveLen;
    if (sixLen > maxLen) maxLen = sixLen;
    for (int i = 0; i < maxLen; i ++) {
        if (sixLen > i) {
            strcat (answer, sixLetter [i]);
            strcat (answer, " ");
        }
        if (fiveLen > i) {
            strcat (answer, fiveLetter [i]);
            strcat (answer, " ");
        }
        if (fourLen > i) strcat (answer, fourLetter [i]);
        strcat (answer, "\n");
        for (int j = 0; j < count; j ++) strcat (answer, "\t");
        count ++;
    }
    return answer;
}
''',
"csharp": r'''using System;

public static class WordStacker
{
    public static string Output(string[] fourLetter, string[] fiveLetter, string[] sixLetter)
    {
        string answer = "";
        int count = 1;
        int maxLength = Math.Max(Math.Max(fourLetter.Length, fiveLetter.Length), sixLetter.Length);
        for (int i = 0; i < maxLength; i++)
        {
            if (sixLetter.Length > i)
            {
                answer += sixLetter[i] + " ";
            }
            if (fiveLetter.Length > i)
            {
                answer += fiveLetter[i] + " ";
            }
            if (fourLetter.Length > i)
            {
                answer += fourLetter[i];
            }
            answer += "\n";
            for (int j = 0; j < count; j++)
            {
                answer += "\t";
            }
            count++;
        }
        return answer;
    }
}
''',
}
