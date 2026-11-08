DATA1 = {}

DATA1["T673"] = {"outputs": {
"python": r"""
import re


def _debug(tag, msg):
    pass


_MO_PATTERN = re.compile(r"[0-9]*")


def filter(source, start, end, dest, dstart, dend):
    _debug("debug", str(_MO_PATTERN))
    _debug("debug", "source: %s, start: %s, end:%s, dest: %s, dstart: %s, dend: %s"
           % (source, start, end, dest, dstart, dend))
    ls_text = dest
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        _debug("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = source
            _debug("debug", "lsInsert: " + ls_insert)
        else:
            ls_insert = ""
        ls_end = ls_text[dend:]
        _debug("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        _debug("debug", "lsText  : " + ls_text)
    lo_matcher = _MO_PATTERN.fullmatch(ls_text)
    _debug("debug", "loMatcher.matches(): %s, lsText: %s" % (lo_matcher is not None, ls_text))
    if lo_matcher is None:
        return ""
    return None
""",
"c": r"""
#include <stdio.h>
#include <string.h>

extern int pattern_full_match(const char *pattern, const char *text);
extern void debug_log(const char *tag, const char *msg);

/* Mirrors the Java InputFilter: returns 1 with out set to "" when the text
   must be rejected, 0 with out empty when the insert is allowed (null). */
int filter(const char *pattern, const char *source, int start, int end,
           const char *dest, int dstart, int dend, char *out) {
    char lsStart[256] = "";
    char lsInsert[256] = "";
    char lsEnd[256] = "";
    char lsText[512] = "";
    char msg[640];
    debug_log("debug", "pattern");
    sprintf(msg, "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d",
            source, start, end, dest, dstart, dend);
    debug_log("debug", msg);
    strcpy(lsText, dest);
    if (strlen(lsText) > 0) {
        strncpy(lsStart, lsText, (size_t)dstart);
        lsStart[dstart] = '\0';
        debug_log("debug", "lsStart");
        if (source[0] != '\0') {
            strcpy(lsInsert, source);
            debug_log("debug", "lsInsert");
        }
        strcpy(lsEnd, lsText + dend);
        debug_log("debug", "lsEnd");
        snprintf(lsText, sizeof(lsText), "%s%s%s", lsStart, lsInsert, lsEnd);
        debug_log("debug", "lsText");
    }
    if (!pattern_full_match(pattern, lsText)) {
        strcpy(out, "");
        return 1;
    }
    out[0] = '\0';
    return 0;
}
""",
"csharp": r"""
using System;
using System.Text.RegularExpressions;

public class InputFilter
{
    private static readonly Regex MoPattern = new Regex("^[0-9]*$");

    private static void Log(string tag, string msg)
    {
    }

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = "";
        Log("debug", MoPattern.ToString());
        Log("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
        lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            Log("debug", "lsStart : " + lsStart);
            if (source != "")
            {
                lsInsert = source;
                Log("debug", "lsInsert: " + lsInsert);
            }
            lsEnd = lsText.Substring(dend);
            Log("debug", "lsEnd   : " + lsEnd);
            lsText = lsStart + lsInsert + lsEnd;
            Log("debug", "lsText  : " + lsText);
        }
        if (!MoPattern.IsMatch(lsText))
        {
            return "";
        }
        return null;
    }
}
"""
}}

DATA1["T186"] = {"outputs": {
"python": r"""
class Score:
    def __init__(self, kind, name, value):
        self.kind = kind
        self.name = name
        self.value = value


def main():
    inp = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)"
    score_sets = inp.split("),")
    score_list = []
    for score in score_sets:
        score = score.strip()[1:]
        close_brace = score.find(")")
        if close_brace == len(score) - 1:
            score = score[:len(score) - 1]
        tokens = score.split(",")
        score_list.append(Score(tokens[0], tokens[1], float(tokens[2])))
""",
"c": r"""
#include <stdio.h>
#include <string.h>

typedef struct {
    char kind[16];
    char name[64];
    double value;
} Score;

int main(void) {
    const char *input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
    Score scoreList[16];
    int count = 0;
    const char *p = input;
    while (*p != '\0') {
        char kind[16], name[64];
        double value;
        if (sscanf(p, " ( %15[^,] , %63[^,] , %lf )", kind, name, &value) != 3) {
            break;
        }
        strcpy(scoreList[count].kind, kind);
        strcpy(scoreList[count].name, name);
        scoreList[count].value = value;
        count++;
        p = strchr(p, ')');
        if (p == NULL) {
            break;
        }
        p++;
    }
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;

public class Score
{
    public string Kind { get; set; }
    public string Name { get; set; }
    public double Value { get; set; }

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
        foreach (string raw in scoreSets)
        {
            string score = raw.Trim().Substring(1);
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
"""
}}

DATA1["T271"] = {"outputs": {
"python": r"""
def main():
    array = []
    n = int(input("Enter n:"))
    m = int(input("Enter m:"))
    print("Enter the values:")
    for i in range(n):
        row = []
        array.append(row)
        for j in range(m):
            row.append(int(input()))
    print("Result:")
    print(array)
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, m;
    printf("Enter n:\n");
    if (scanf("%d", &n) != 1) return 1;
    printf("Enter m:\n");
    if (scanf("%d", &m) != 1) return 1;
    printf("Enter the values:\n");
    int **array = malloc((size_t)n * sizeof(int *));
    for (int i = 0; i < n; i++) {
        array[i] = malloc((size_t)m * sizeof(int));
        for (int j = 0; j < m; j++) {
            scanf("%d", &array[i][j]);
        }
    }
    printf("Result:\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
    for (int i = 0; i < n; i++) {
        free(array[i]);
    }
    free(array);
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;

public static class MatrixReader
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
        foreach (List<int> row in array)
        {
            Console.WriteLine(string.Join(" ", row));
        }
    }
}
"""
}}

DATA1["T341"] = {"outputs": {
"python": r"""
def output(four_letter, five_letter, six_letter):
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
        answer += "\n"
        answer += "\t" * count
        count += 1
    return answer
""",
"c": r"""
#include <stdio.h>
#include <string.h>

#define MAX_OF(A, B) ((A) > (B) ? (A) : (B))

static void build_output(const char *four[], int fourLen,
                         const char *five[], int fiveLen,
                         const char *six[], int sixLen,
                         char *answer) {
    int count = 1;
    int longest = MAX_OF(MAX_OF(fourLen, fiveLen), sixLen);
    answer[0] = '\0';
    for (int i = 0; i < longest; i++) {
        if (sixLen > i) {
            strcat(answer, six[i]);
            strcat(answer, " ");
        }
        if (fiveLen > i) {
            strcat(answer, five[i]);
            strcat(answer, " ");
        }
        if (fourLen > i) {
            strcat(answer, four[i]);
        }
        strcat(answer, "\n");
        for (int j = 0; j < count; j++) {
            strcat(answer, "\t");
        }
        count++;
    }
}
""",
"csharp": r"""
using System;

public static class WordOutput
{
    public static string Output(string[] fourLetter, string[] fiveLetter, string[] sixLetter)
    {
        string answer = "";
        int count = 1;
        int longest = Math.Max(Math.Max(fourLetter.Length, fiveLetter.Length), sixLetter.Length);
        for (int i = 0; i < longest; i++)
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
            answer += new string('\t', count);
            count++;
        }
        return answer;
    }
}
"""
}}

DATA1["T350"] = {"outputs": {
"python": r"""
SEPARATOR = " "

_HIGH_PROCESSOR = type("Processor", (), {"get_name": staticmethod(lambda v: "" if v == "" else v)})()
_LOW_PROCESSOR = type("Processor", (), {"get_name": staticmethod(lambda v: "" if v == "" else v)})()


def get_part_divider():
    return 3


def get_token():
    return "hundred"


def get_name(value):
    buffer = []
    if len(value) < get_part_divider():
        high = ""
        low = value
    else:
        index = len(value) - get_part_divider()
        high = value[:index]
        low = value[index:]
    high_name = _HIGH_PROCESSOR.get_name(high)
    low_name = _LOW_PROCESSOR.get_name(low)
    if high_name != "":
        buffer.append(high_name)
        buffer.append(SEPARATOR)
        buffer.append(get_token())
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

static int get_part_divider(void) {
    return 3;
}

static const char *get_token(void) {
    return "hundred";
}

static const char *processor_get_name(const char *value) {
    return value;
}

void get_name(const char *value, char *out, size_t outSize) {
    char high[64], low[64];
    size_t len = strlen(value);
    out[0] = '\0';
    if (len < (size_t)get_part_divider()) {
        high[0] = '\0';
        strcpy(low, value);
    } else {
        size_t index = len - (size_t)get_part_divider();
        memcpy(high, value, index);
        high[index] = '\0';
        strcpy(low, value + index);
    }
    const char *highName = processor_get_name(high);
    const char *lowName = processor_get_name(low);
    if (highName[0] != '\0') {
        strcat(out, highName);
        strcat(out, SEPARATOR);
        strcat(out, get_token());
        if (lowName[0] != '\0') {
            strcat(out, SEPARATOR);
        }
    }
    if (lowName[0] != '\0') {
        strcat(out, lowName);
    }
}
""",
"csharp": r"""
using System;
using System.Text;

public class NameBuilder
{
    private const string Separator = " ";

    protected virtual int GetPartDivider()
    {
        return 3;
    }

    protected virtual string GetToken()
    {
        return "hundred";
    }

    protected virtual string ProcessName(string value)
    {
        return value;
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
        string highName = ProcessName(high);
        string lowName = ProcessName(low);
        if (!"".Equals(highName))
        {
            buffer.Append(highName);
            buffer.Append(Separator);
            buffer.Append(GetToken());
            if (!"".Equals(lowName))
            {
                buffer.Append(Separator);
            }
        }
        if (!"".Equals(lowName))
        {
            buffer.Append(lowName);
        }
        return buffer.ToString();
    }
}
"""
}}

DATA1["T359"] = {"outputs": {
"python": r"""
import threading
from queue import Queue

output_count = 0
_count_lock = threading.Lock()


def worker(expensive_objects):
    global output_count
    expensive_objects.get()
    with _count_lock:
        output_count += 1


def main():
    expensive_objects = Queue()
    for _ in range(4):
        expensive_objects.put(object())
    threads = []
    for _ in range(4):
        t = threading.Thread(target=worker, args=(expensive_objects,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)
    print("Final: " + str(output_count))
""",
"c": r"""
#include <pthread.h>
#include <stdio.h>

static int output_count = 0;
static int pending_objects = 4;
static pthread_mutex_t pool_lock = PTHREAD_MUTEX_INITIALIZER;

static void *worker(void *arg) {
    (void)arg;
    pthread_mutex_lock(&pool_lock);
    if (pending_objects > 0) {
        pending_objects--;
        output_count++;
    }
    pthread_mutex_unlock(&pool_lock);
    return NULL;
}

int main(void) {
    pthread_t threads[4];
    for (int i = 0; i < 4; i++) {
        pthread_create(&threads[i], NULL, worker, NULL);
    }
    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("Final: %d\n", output_count);
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;
using System.Threading;

public static class PoolRunner
{
    private static int _outputCount = 0;
    private static readonly object Gate = new object();

    private static void Worker()
    {
        lock (Gate)
        {
            _outputCount++;
        }
    }

    public static void Main(string[] args)
    {
        Queue<object> expensiveObjects = new Queue<object>();
        for (int i = 0; i < 4; i++)
        {
            expensiveObjects.Enqueue(new object());
        }
        List<Thread> threads = new List<Thread>();
        for (int i = 0; i < 4; i++)
        {
            Thread t = new Thread(Worker);
            threads.Add(t);
            t.Start();
        }
        foreach (Thread t in threads)
        {
            t.Join(5000);
        }
        Console.WriteLine("Final: " + _outputCount);
    }
}
"""
}}
