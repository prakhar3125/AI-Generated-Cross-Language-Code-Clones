import ast
import json

OUT = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/out/claude-sonnet-5-5_chunk2.json"
SEED = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/seeds/chunk2.json"

OUTPUTS = {}

OUTPUTS["T673"] = {
    "python": r'''
import re


class Log:
    @staticmethod
    def d(tag, msg):
        pass


class Spanned(str):
    pass


class InputFilter:
    def __init__(self, pattern):
        self.mo_pattern = re.compile(pattern)

    def filter(self, source, start, end, dest, dstart, dend):
        ls_start = ""
        ls_insert = ""
        ls_end = ""
        ls_text = ""
        Log.d("debug", self.mo_pattern.pattern)
        Log.d("debug", f"source: {source}, start: {start}, end:{end}, dest: {dest}, dstart: {dstart}, dend: {dend}")
        ls_text = str(dest)
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
        lo_matcher = self.mo_pattern.fullmatch(ls_text)
        Log.d("debug", f"loMatcher.matches(): {bool(lo_matcher)}, lsText: {ls_text}")
        if not lo_matcher:
            return ""
        return None
''',
    "c": r'''
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    const char *pattern_text;
} Pattern;

typedef struct {
    Pattern *pattern;
} Matcher;

void log_d(const char *tag, const char *msg) { (void)tag; (void)msg; }

int pattern_matches_full(Pattern *p, const char *text);

char *filter(Pattern *moPattern, const char *source, int start, int end,
             const char *dest, int dstart, int dend) {
    char lsStart[256] = "";
    char lsInsert[256] = "";
    char lsEnd[256] = "";
    char lsText[512] = "";
    char debugMsg[1024];
    log_d("debug", moPattern->pattern_text);
    snprintf(debugMsg, sizeof(debugMsg),
             "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d",
             source, start, end, dest, dstart, dend);
    log_d("debug", debugMsg);
    strcpy(lsText, dest);
    if (strlen(lsText) > 0) {
        strncpy(lsStart, lsText, dstart);
        lsStart[dstart] = '\0';
        log_d("debug", lsStart);
        if (source[0] != '\0') {
            strcpy(lsInsert, source);
            log_d("debug", lsInsert);
        }
        strcpy(lsEnd, lsText + dend);
        log_d("debug", lsEnd);
        strcpy(lsText, lsStart);
        strcat(lsText, lsInsert);
        strcat(lsText, lsEnd);
        log_d("debug", lsText);
    }
    if (!pattern_matches_full(moPattern, lsText)) {
        return "";
    }
    return NULL;
}
''',
    "csharp": r'''
using System;
using System.Text.RegularExpressions;

public class Log
{
    public static void D(string tag, string msg) { }
}

public class InputFilter
{
    private readonly Regex moPattern;

    public InputFilter(Regex pattern)
    {
        moPattern = pattern;
    }

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = "";
        Log.D("debug", moPattern.ToString());
        Log.D("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
        lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            Log.D("debug", "lsStart : " + lsStart);
            if (source != "")
            {
                lsInsert = source;
                Log.D("debug", "lsInsert: " + lsInsert);
            }
            lsEnd = lsText.Substring(dend);
            Log.D("debug", "lsEnd   : " + lsEnd);
            lsText = lsStart + lsInsert + lsEnd;
            Log.D("debug", "lsText  : " + lsText);
        }
        Match loMatcher = moPattern.Match(lsText);
        bool matches = loMatcher.Success && loMatcher.Length == lsText.Length;
        Log.D("debug", "loMatcher.matches(): " + matches + ", lsText: " + lsText);
        if (!matches)
        {
            return "";
        }
        return null;
    }
}
''',
}

OUTPUTS["T452"] = {
    "python": r'''
def main():
    s = "my name is khan"
    words = s.split()
    capitalized_word = ""
    for w in words:
        capitalized_word += w[0].upper() + w[1:] + " "
    print(capitalized_word)


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char str[] = "my name is khan";
    char capitalizedWord[256] = "";
    char first[2];
    char *word;
    for (word = strtok(str, " "); word != NULL; word = strtok(NULL, " ")) {
        first[0] = (char) toupper((unsigned char) word[0]);
        first[1] = '\0';
        strcat(capitalizedWord, first);
        strcat(capitalizedWord, word + 1);
        strcat(capitalizedWord, " ");
    }
    printf("%s\n", capitalizedWord);
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    public static void Main(string[] args)
    {
        string str = "my name is khan";
        string[] words = str.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        string capitalizedWord = "";
        foreach (string w in words)
        {
            string first = w.Substring(0, 1);
            string fAfter = w.Substring(1);
            capitalizedWord += first.ToUpper() + fAfter + " ";
        }
        Console.WriteLine(capitalizedWord);
    }
}
''',
}

OUTPUTS["T186"] = {
    "python": r'''
class Score:
    def __init__(self, letter, name, value):
        self.letter = letter
        self.name = name
        self.value = value


def main():
    s = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)"
    score_sets = s.split("),")
    score_list = []
    for score in score_sets:
        score = score.strip()[1:]
        if score.endswith(")"):
            score = score[:-1]
        tokens = score.split(",")
        score_list.append(Score(tokens[0], tokens[1], float(tokens[2])))


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char type;
    char name[64];
    double value;
} Score;

int main(void) {
    const char *input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
    Score scoreList[16];
    int count = 0;
    const char *p = input;
    while (*p) {
        char group[128];
        char *tokens[3];
        int g = 0, n = 0;
        char *tok;
        while (*p == ' ' || *p == ',') p++;
        if (*p != '(') break;
        p++;
        while (*p && *p != ')' && g < 127) group[g++] = *p++;
        group[g] = '\0';
        if (*p == ')') p++;
        tok = strtok(group, ",");
        while (tok != NULL && n < 3) {
            tokens[n++] = tok;
            tok = strtok(NULL, ",");
        }
        if (n == 3) {
            scoreList[count].type = tokens[0][0];
            strncpy(scoreList[count].name, tokens[1], sizeof(scoreList[count].name) - 1);
            scoreList[count].name[sizeof(scoreList[count].name) - 1] = '\0';
            scoreList[count].value = atof(tokens[2]);
            count++;
        }
    }
    (void)scoreList;
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;

public class Score
{
    public string Type { get; }
    public string Name { get; }
    public double Value { get; }

    public Score(string type, string name, double value)
    {
        Type = type;
        Name = name;
        Value = value;
    }
}

public static class Program
{
    public static void Main(string[] args)
    {
        string input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
        string[] scoreSets = input.Split(new[] { ")," }, StringSplitOptions.None);
        List<Score> scoreList = new List<Score>();
        foreach (string raw in scoreSets)
        {
            string score = raw.Trim().Substring(1);
            if (score.EndsWith(")"))
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

OUTPUTS["T271"] = {
    "python": r'''
def main():
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


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, m, i, j;
    int **array;
    printf("Enter n:\n");
    scanf("%d", &n);
    printf("Enter m:\n");
    scanf("%d", &m);
    printf("Enter the values:\n");
    array = malloc(n * sizeof(int *));
    for (i = 0; i < n; i++) {
        array[i] = malloc(m * sizeof(int));
        for (j = 0; j < m; j++) {
            scanf("%d", &array[i][j]);
        }
    }
    printf("Result:\n");
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
    for (i = 0; i < n; i++) {
        free(array[i]);
    }
    free(array);
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;

public static class Program
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
            List<int> row = new List<int>();
            array.Add(row);
            for (int j = 0; j < m; j++)
            {
                row.Add(int.Parse(Console.ReadLine()));
            }
        }
        Console.WriteLine("Result:");
        foreach (List<int> row in array)
        {
            Console.WriteLine(string.Join(" ", row));
        }
    }
}
''',
}

OUTPUTS["T597"] = {
    "python": r'''
class HttpStatus:
    BAD_REQUEST = 400
    OK = 200


class ResponseEntity:
    def __init__(self, body=None, status=None):
        self.body = body
        self.status = status


class Product:
    def __init__(self, product_id):
        self.product_id = product_id


class ProductController:
    def __init__(self, service):
        self.service = service

    def match(self, match_id, body, request, response):
        try:
            p = self.service.get_product(request.get_product_id())
        except Exception:
            return ResponseEntity(status=HttpStatus.BAD_REQUEST)
        return ResponseEntity(p, HttpStatus.OK)
''',
    "c": r'''
#include <stdlib.h>

typedef struct {
    int code;
} HttpStatus;

static const HttpStatus HTTP_BAD_REQUEST = { 400 };
static const HttpStatus HTTP_OK = { 200 };

typedef struct {
    void *body;
    HttpStatus status;
} ResponseEntity;

typedef struct {
    int productId;
} Request;

typedef struct {
    int (*getProduct)(void *, int);
    void *service;
} Controller;

/* stand-in: getProduct returns the product id, or 0 on failure */
ResponseEntity match(Controller *self, const char *matchId, const char *body,
                     Request *request, void *response) {
    ResponseEntity result;
    int product = self->getProduct(self->service, request->productId);
    if (product == 0) {
        result.body = NULL;
        result.status = HTTP_BAD_REQUEST;
    } else {
        result.body = (void *) (long) product;
        result.status = HTTP_OK;
    }
    return result;
}
''',
    "csharp": r'''
using System;

public static class HttpStatus
{
    public const int BAD_REQUEST = 400;
    public const int OK = 200;
}

public class ResponseEntity
{
    public object Body { get; }
    public int Status { get; }

    public ResponseEntity(object body, int status)
    {
        Body = body;
        Status = status;
    }
}

public class Product
{
    public int Id { get; set; }
}

public class Request
{
    public int GetProductId() { return 1; }
}

public class Service
{
    public Product GetProduct(int productId)
    {
        if (productId <= 0) throw new InvalidOperationException();
        return new Product { Id = productId };
    }
}

public class MatchController
{
    private readonly Service service;

    public MatchController(Service service)
    {
        this.service = service;
    }

    public ResponseEntity Match(string matchId, string body, Request request, object response)
    {
        Product p;
        try
        {
            p = service.GetProduct(request.GetProductId());
        }
        catch (Exception)
        {
            return new ResponseEntity(null, HttpStatus.BAD_REQUEST);
        }
        return new ResponseEntity(p, HttpStatus.OK);
    }
}
''',
}

OUTPUTS["T341"] = {
    "python": r'''
def output(four_letter, five_letter, six_letter):
    answer = ""
    count = 1
    longest = max(len(four_letter), len(five_letter), len(six_letter))
    for i in range(longest):
        if i < len(six_letter):
            answer += six_letter[i] + " "
        if i < len(five_letter):
            answer += five_letter[i] + " "
        if i < len(four_letter):
            answer += four_letter[i]
        answer += "\n"
        answer += "\t" * count
        count += 1
    return answer
''',
    "c": r'''
#include <stdio.h>
#include <stddef.h>

static char *output(const char *fourLetter[], int fourLen,
                    const char *fiveLetter[], int fiveLen,
                    const char *sixLetter[], int sixLen) {
    static char answer[4096];
    size_t used = 0;
    int longest = fourLen;
    int count = 1;
    if (fiveLen > longest) longest = fiveLen;
    if (sixLen > longest) longest = sixLen;
    answer[0] = '\0';
    for (int i = 0; i < longest; i++) {
        if (i < sixLen) {
            used += (size_t) snprintf(answer + used, sizeof(answer) - used, "%s ", sixLetter[i]);
        }
        if (i < fiveLen) {
            used += (size_t) snprintf(answer + used, sizeof(answer) - used, "%s ", fiveLetter[i]);
        }
        if (i < fourLen) {
            used += (size_t) snprintf(answer + used, sizeof(answer) - used, "%s", fourLetter[i]);
        }
        used += (size_t) snprintf(answer + used, sizeof(answer) - used, "\n");
        for (int j = 0; j < count; j++) {
            used += (size_t) snprintf(answer + used, sizeof(answer) - used, "\t");
        }
        count++;
    }
    return answer;
}
''',
    "csharp": r'''
using System;
using System.Text;

public static class Program
{
    public static string Output(string[] fourLetter, string[] fiveLetter, string[] sixLetter)
    {
        var answer = new StringBuilder();
        int count = 1;
        int longest = Math.Max(Math.Max(fourLetter.Length, fiveLetter.Length), sixLetter.Length);
        for (int i = 0; i < longest; i++)
        {
            if (i < sixLetter.Length)
            {
                answer.Append(sixLetter[i]).Append(' ');
            }
            if (i < fiveLetter.Length)
            {
                answer.Append(fiveLetter[i]).Append(' ');
            }
            if (i < fourLetter.Length)
            {
                answer.Append(fourLetter[i]);
            }
            answer.Append('\n');
            answer.Append('\t', count);
            count++;
        }
        return answer.ToString();
    }
}
''',
}

OUTPUTS["T350"] = {
    "python": r'''
class CommonNumberProcessor:
    SEPARATOR = " "

    def __init__(self, high_processor, low_processor):
        self.high_processor = high_processor
        self.low_processor = low_processor

    def get_part_divider(self):
        return 3

    def get_token(self):
        return "hundred"

    def get_name(self, value):
        buffer = []
        if len(value) < self.get_part_divider():
            high = ""
            low = value
        else:
            index = len(value) - self.get_part_divider()
            high = value[:index]
            low = value[index:]
        high_name = self.high_processor.get_name(high)
        low_name = self.low_processor.get_name(low)
        if high_name != "":
            buffer.append(high_name)
            buffer.append(self.SEPARATOR)
            buffer.append(self.get_token())
            if low_name != "":
                buffer.append(self.SEPARATOR)
        if low_name != "":
            buffer.append(low_name)
        return "".join(buffer)
''',
    "c": r'''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SEPARATOR " "

static int get_part_divider(void);
static const char *get_token(void);
static void high_processor_name(const char *value, char *out, size_t outSize);
static void low_processor_name(const char *value, char *out, size_t outSize);

void get_name(const char *value, char *result, size_t resultSize) {
    char high[64];
    char low[64];
    char highName[64];
    char lowName[64];
    size_t valueLen = strlen(value);
    int divider = get_part_divider();
    result[0] = '\0';
    if ((int) valueLen < divider) {
        high[0] = '\0';
        strcpy(low, value);
    } else {
        int index = (int) valueLen - divider;
        strncpy(high, value, (size_t) index);
        high[index] = '\0';
        strcpy(low, value + index);
    }
    high_processor_name(high, highName, sizeof(highName));
    low_processor_name(low, lowName, sizeof(lowName));
    if (highName[0] != '\0') {
        strcat(result, highName);
        strcat(result, SEPARATOR);
        strcat(result, get_token());
        if (lowName[0] != '\0') {
            strcat(result, SEPARATOR);
        }
    }
    if (lowName[0] != '\0') {
        strcat(result, lowName);
    }
}
''',
    "csharp": r'''
using System.Text;

public interface INameProcessor
{
    string GetName(string value);
}

public class CommonNumberProcessor
{
    private const string SEPARATOR = " ";
    private readonly INameProcessor highProcessor;
    private readonly INameProcessor lowProcessor;

    public CommonNumberProcessor(INameProcessor highProcessor, INameProcessor lowProcessor)
    {
        this.highProcessor = highProcessor;
        this.lowProcessor = lowProcessor;
    }

    protected virtual int GetPartDivider()
    {
        return 3;
    }

    protected virtual string GetToken()
    {
        return "hundred";
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
        string highName = highProcessor.GetName(high);
        string lowName = lowProcessor.GetName(low);
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

OUTPUTS["T815"] = {
    "python": r'''
import calendar


class MonthNavigator:
    def __init__(self, year, month_no, day):
        self.year = year
        self.month_no = month_no
        self.day = day

    def get_next_month(self, max_date):
        y = self.year
        m = self.month_no + 1
        if m > 12:
            m = 1
            y += 1
        if max_date:
            d = calendar.monthrange(y, m)[1]
        else:
            d = self.day
        return f"{y}-{m}-{d}"
''',
    "c": r'''
#include <stdio.h>
#include <stddef.h>

typedef struct {
    int year;
    int month;
    int day;
} Calendar;

static int days_in_month(int year, int month) {
    static const int lengths[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 2) {
        int leap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
        return leap ? 29 : 28;
    }
    return lengths[month - 1];
}

void get_next_month(const Calendar *cal, int maxDate, char *out, size_t outSize) {
    Calendar c = *cal;
    c.month += 1;
    if (c.month > 12) {
        c.month = 1;
        c.year += 1;
    }
    c.day = maxDate ? days_in_month(c.year, c.month) : cal->day;
    snprintf(out, outSize, "%d-%d-%d", c.year, c.month, c.day);
}
''',
    "csharp": r'''
using System;

public class MonthNavigator
{
    private readonly int year;
    private readonly int monthNo;
    private readonly int day;

    public MonthNavigator(int year, int monthNo, int day)
    {
        this.year = year;
        this.monthNo = monthNo;
        this.day = day;
    }

    public string GetNextMonth(bool maxDate)
    {
        DateTime calendar = new DateTime(year, monthNo, 1).AddMonths(1);
        int dayOfMonth = maxDate
            ? DateTime.DaysInMonth(calendar.Year, calendar.Month)
            : day;
        string date = calendar.Year + "-" + calendar.Month + "-" + dayOfMonth;
        return date;
    }
}
''',
}

OUTPUTS["T359"] = {
    "python": r'''
import queue
import threading

output_count = [0]
output_lock = threading.Lock()


class MyRunnable:
    def __init__(self, expensive_objects):
        self.expensive_objects = expensive_objects

    def run(self):
        obj = self.expensive_objects.get()
        with output_lock:
            output_count[0] += 1


def main():
    expensive_objects = queue.Queue()
    for _ in range(4):
        expensive_objects.put(object())
    executor = []
    for _ in range(4):
        worker = threading.Thread(target=MyRunnable(expensive_objects).run)
        executor.append(worker)
        worker.start()
    for worker in executor:
        worker.join(timeout=5)
    print("Final:", output_count[0])


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>

#define THREAD_COUNT 4

typedef struct {
    int *objects;
    int size;
} BlockingQueue;

typedef struct {
    BlockingQueue *queue;
} MyRunnable;

/* stand-in worker; a real build would use pthreads with a condition variable */
extern void runnable_run(MyRunnable *r);

int main(void) {
    MyRunnable runnables[THREAD_COUNT];
    int objects[THREAD_COUNT];
    BlockingQueue queue;
    int i;
    int outputCount = 0;
    for (i = 0; i < THREAD_COUNT; i++) {
        objects[i] = i;
    }
    queue.objects = objects;
    queue.size = THREAD_COUNT;
    for (i = 0; i < THREAD_COUNT; i++) {
        runnables[i].queue = &queue;
        runnable_run(&runnables[i]);
        outputCount++;
    }
    printf("Final: %d\n", outputCount);
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;

public static class Program
{
    private static int outputCount = 0;

    public static void Main(string[] args)
    {
        var expensiveObjects = new BlockingCollection<object>(new ConcurrentQueue<object>());
        for (int i = 0; i < 4; i++)
        {
            expensiveObjects.Add(new object());
        }
        Task[] tasks = new Task[4];
        for (int i = 0; i < 4; i++)
        {
            tasks[i] = Task.Run(() =>
            {
                object item = expensiveObjects.Take();
                Interlocked.Increment(ref outputCount);
            });
        }
        Task.WaitAll(tasks, TimeSpan.FromSeconds(5));
        Console.WriteLine("Final: " + outputCount);
    }
}
''',
}

OUTPUTS["T448"] = {
    "python": r'''
PARENTHESES_MAP_LEFT = {'(': ')', '[': ']', '{': '}'}
PARENTHESES_MAP_RIGHT = {v: k for k, v in PARENTHESES_MAP_LEFT.items()}


def is_balanced(s):
    result = False
    if len(s) < 2:
        return False
    stack = []
    for ch in s:
        if ch not in PARENTHESES_MAP_RIGHT and ch not in PARENTHESES_MAP_LEFT:
            continue
        if ch in PARENTHESES_MAP_LEFT:
            stack.append(ch)
        else:
            if stack and stack.pop() == PARENTHESES_MAP_RIGHT[ch]:
                result = True
            else:
                return False
    if stack:
        return False
    return result
''',
    "c": r'''
#include <stdbool.h>
#include <string.h>

static char leftOf(char right) {
    switch (right) {
        case ')': return '(';
        case ']': return '[';
        case '}': return '{';
        default: return '\0';
    }
}

static bool isLeft(char c) {
    return c == '(' || c == '[' || c == '{';
}

bool isBalanced(const char *str) {
    bool result = false;
    char stack[256];
    int top = 0;
    size_t i;
    if (strlen(str) < 2) return false;
    for (i = 0; i < strlen(str); i++) {
        char ch = str[i];
        if (!isLeft(ch) && leftOf(ch) == '\0') continue;
        if (isLeft(ch)) {
            stack[top++] = ch;
        } else {
            if (top > 0 && stack[--top] == leftOf(ch)) {
                result = true;
            } else {
                return false;
            }
        }
    }
    if (top != 0) return false;
    return result;
}
''',
    "csharp": r'''
using System.Collections.Generic;

public static class BalanceChecker
{
    private static readonly Dictionary<char, char> LeftMap = new Dictionary<char, char>
    {
        { '(', ')' }, { '[', ']' }, { '{', '}' }
    };

    private static readonly Dictionary<char, char> RightMap = new Dictionary<char, char>
    {
        { ')', '(' }, { ']', '[' }, { '}', '{' }
    };

    public static bool IsBalanced(string str)
    {
        bool result = false;
        if (str.Length < 2)
        {
            return false;
        }
        var stack = new Stack<char>();
        foreach (char ch in str)
        {
            if (!RightMap.ContainsKey(ch) && !LeftMap.ContainsKey(ch))
            {
                continue;
            }
            if (LeftMap.ContainsKey(ch))
            {
                stack.Push(ch);
            }
            else if (stack.Count > 0 && stack.Pop() == RightMap[ch])
            {
                result = true;
            }
            else
            {
                return false;
            }
        }
        if (stack.Count > 0)
        {
            return false;
        }
        return result;
    }
}
''',
}

OUTPUTS["T561"] = {
    "python": r'''
def main():
    my_array = [list("string1"), list("string2"), list("string3")]
    print(len(my_array))
    combined = "".join("".join(c) for c in my_array)
    char_array_1d = list(combined)
    print(len(char_array_1d))


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char myArray[3][16];
    char combined[64];
    strcpy(myArray[0], "string1");
    strcpy(myArray[1], "string2");
    strcpy(myArray[2], "string3");
    printf("%d\n", (int) (sizeof(myArray) / sizeof(myArray[0])));
    combined[0] = '\0';
    for (int i = 0; i < 3; i++) {
        strcat(combined, myArray[i]);
    }
    printf("%zu\n", strlen(combined));
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;
using System.Text;

public static class Program
{
    public static void Main(string[] args)
    {
        List<char[]> myArray = new List<char[]>
        {
            "string1".ToCharArray(),
            "string2".ToCharArray(),
            "string3".ToCharArray()
        };
        Console.WriteLine(myArray.Count);
        var s = new StringBuilder();
        foreach (char[] c in myArray)
        {
            s.Append(c);
        }
        char[] charArray1D = s.ToString().ToCharArray();
        Console.WriteLine(charArray1D.Length);
    }
}
''',
}

OUTPUTS["T171"] = {
    "python": r'''
def solution(x, a):
    leaves = set()
    for i, value in enumerate(a):
        leaves.add(value)
        if x in leaves and len(leaves) == x:
            return i
    return -1
''',
    "c": r'''
#include <stdbool.h>

#define MAX_VALUE 1000000

int solution(int x, const int *a, int length) {
    static bool seen[MAX_VALUE + 1];
    int distinct = 0;
    bool xSeen = false;
    for (int i = 0; i < length; i++) {
        int value = a[i];
        if (value >= 0 && value <= MAX_VALUE && !seen[value]) {
            seen[value] = true;
            distinct++;
        }
        if (value == x) xSeen = true;
        if (xSeen && distinct == x) {
            return i;
        }
    }
    return -1;
}
''',
    "csharp": r'''
using System.Collections.Generic;

public class RiverCrossing
{
    public int Solution(int x, int[] a)
    {
        var leaves = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            leaves.Add(a[i]);
            if (leaves.Contains(x) && leaves.Count == x)
            {
                return i;
            }
        }
        return -1;
    }
}
''',
}

OUTPUTS["T533"] = {
    "python": r'''
import threading


class Sleeper:
    def __init__(self, obj):
        self.object = obj

    def run(self):
        o = self.object
        while True:
            waiter = threading.Event()
            waiter.wait()
''',
    "c": r'''
#include <unistd.h>

void run(void *object) {
    void *o = object;
    for (;;) {
        pause();
    }
}
''',
    "csharp": r'''
using System.Threading;

public class ForeverSleeper
{
    private readonly object target;

    public ForeverSleeper(object target)
    {
        this.target = target;
    }

    public void Run()
    {
        object o = target;
        while (true)
        {
            try
            {
                Thread.Sleep(Timeout.Infinite);
            }
            catch (ThreadInterruptedException)
            {
            }
        }
    }
}
''',
}

OUTPUTS["T111"] = {
    "python": r'''
def single_number(nums):
    answer = 0
    al = list(nums)
    for i in range(len(nums)):
        if al.count(nums[i]) == 1:
            answer = nums[i]
    return answer
''',
    "c": r'''
#include <stddef.h>

int single_number(const int *nums, size_t length) {
    int answer = 0;
    size_t i, j;
    for (i = 0; i < length; i++) {
        int first = -1;
        int last = -1;
        for (j = 0; j < length; j++) {
            if (nums[j] == nums[i]) {
                if (first < 0) first = (int) j;
                last = (int) j;
            }
        }
        if (first == last) {
            answer = nums[i];
        }
    }
    return answer;
}
''',
    "csharp": r'''
using System.Collections.Generic;

public static class SingleNumberFinder
{
    public static int SingleNumber(int[] nums)
    {
        int answer = 0;
        var al = new List<int>(nums);
        for (int i = 0; i < nums.Length; i++)
        {
            int test = nums[i];
            if (al.IndexOf(test) == al.LastIndexOf(test))
            {
                answer = nums[i];
            }
        }
        return answer;
    }
}
''',
}

OUTPUTS["T224"] = {
    "python": r'''
import re


def get_number(s):
    return float(s)


def main():
    input_string = input()
    if not re.fullmatch(r"[+-]?([0-9]*[.])?[0-9]+", input_string):
        print("Not a Number")
    else:
        result2 = get_number(input_string)
        print("result = " + str(result2))


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

static int matchesNumber(const char *s) {
    int i = 0;
    int intDigits = 0;
    int fracDigits = 0;
    int dotSeen = 0;
    if (s[i] == '+' || s[i] == '-') i++;
    while (isdigit((unsigned char) s[i])) { i++; intDigits++; }
    if (s[i] == '.') { i++; dotSeen = 1; }
    while (isdigit((unsigned char) s[i])) { i++; fracDigits++; }
    if (s[i] != '\0') return 0;
    if (dotSeen) return fracDigits > 0;
    return intDigits > 0;
}

int main(void) {
    char inputString[256];
    if (scanf("%255s", inputString) != 1) return 0;
    if (!matchesNumber(inputString)) {
        printf("Not a Number\n");
    } else {
        double result2 = atof(inputString);
        printf("result = %g\n", result2);
    }
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Globalization;
using System.Text.RegularExpressions;

public static class Program
{
    private static double GetNumber(string s)
    {
        return double.Parse(s, CultureInfo.InvariantCulture);
    }

    public static void Main(string[] args)
    {
        string inputString = Console.ReadLine();
        if (!Regex.IsMatch(inputString, @"^[+-]?([0-9]*[.])?[0-9]+$"))
        {
            Console.WriteLine("Not a Number");
        }
        else
        {
            double result2 = GetNumber(inputString);
            Console.WriteLine("result = " + result2);
        }
    }
}
''',
}

OUTPUTS["T479"] = {
    "python": r'''
import random


def main():
    print("Enter first integer: ")
    num_one = int(input())
    print("You have keyed in " + str(num_one))
    print("Enter second integer: ")
    num_two = int(input())
    print("You have keyed in " + str(num_two))
    num = random.randrange(num_two)
    print("Random number: " + str(num if num > num_one else num_one + num))


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int numOne, numTwo, num;
    printf("Enter first integer: \n");
    scanf("%d", &numOne);
    printf("You have keyed in %d\n", numOne);
    printf("Enter second integer: \n");
    scanf("%d", &numTwo);
    printf("You have keyed in %d\n", numTwo);
    srand((unsigned) time(NULL));
    num = (int) ((double) rand() / ((double) RAND_MAX + 1.0) * numTwo);
    printf("Random number: %d\n", num > numOne ? num : numOne + num);
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Enter first integer: ");
        int numOne = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numOne);
        Console.WriteLine("Enter second integer: ");
        int numTwo = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numTwo);
        Random generator = new Random();
        int num = generator.Next(numTwo);
        Console.WriteLine("Random number: " + (num > numOne ? num : numOne + num));
    }
}
''',
}

OUTPUTS["T212"] = {
    "python": r'''
def main():
    needle = "ABC"
    haystack = "ABCDSGDABCSAGAABCCCCAAABAABC"
    number_of_occurences = 0
    index = haystack.find(needle)
    while index != -1:
        number_of_occurences += 1
        haystack = haystack[index + len(needle):]
        index = haystack.find(needle)
    print(number_of_occurences)


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *needle = "ABC";
    char haystack[] = "ABCDSGDABCSAGAABCCCCAAABAABC";
    int numberOfOccurences = 0;
    char *index = strstr(haystack, needle);
    while (index != NULL) {
        numberOfOccurences++;
        memmove(haystack, index + strlen(needle), strlen(index + strlen(needle)) + 1);
        index = strstr(haystack, needle);
    }
    printf("%d\n", numberOfOccurences);
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    public static void Main(string[] args)
    {
        string needle = "ABC";
        string haystack = "ABCDSGDABCSAGAABCCCCAAABAABC";
        int numberOfOccurences = 0;
        int index = haystack.IndexOf(needle, StringComparison.Ordinal);
        while (index != -1)
        {
            numberOfOccurences++;
            haystack = haystack.Substring(index + needle.Length);
            index = haystack.IndexOf(needle, StringComparison.Ordinal);
        }
        Console.WriteLine(numberOfOccurences);
    }
}
''',
}

OUTPUTS["T170"] = {
    "python": r'''
def solution(x, a):
    seen = set()
    sum1 = 0
    for i in range(x + 1):
        sum1 += i
    sum2 = 0
    for i, value in enumerate(a):
        if value in seen:
            continue
        seen.add(value)
        sum2 += value
        if sum1 == sum2:
            return i
    return -1
''',
    "c": r'''
#include <stdbool.h>

#define MAX_VALUE 1000000

int solution(int x, const int *a, int length) {
    static bool seen[MAX_VALUE + 1];
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i <= x; i++) {
        sum1 += i;
    }
    for (int i = 0; i < length; i++) {
        int value = a[i];
        if (value >= 0 && value <= MAX_VALUE && seen[value]) {
            continue;
        }
        if (value >= 0 && value <= MAX_VALUE) {
            seen[value] = true;
        }
        sum2 += value;
        if (sum1 == sum2) {
            return i;
        }
    }
    return -1;
}
''',
    "csharp": r'''
using System.Collections.Generic;

public class RiverCrossing
{
    public int Solution(int x, int[] a)
    {
        var set = new HashSet<int>();
        int sum1 = 0, sum2 = 0;
        for (int i = 0; i <= x; i++)
        {
            sum1 += i;
        }
        for (int i = 0; i < a.Length; i++)
        {
            if (set.Contains(a[i]))
            {
                continue;
            }
            set.Add(a[i]);
            sum2 += a[i];
            if (sum1 == sum2)
            {
                return i;
            }
        }
        return -1;
    }
}
''',
}

OUTPUTS["T508"] = {
    "python": r'''
from collections import Counter


def main():
    output = ""
    words_multiset = Counter("AAABBBBCC")
    for element, count in words_multiset.items():
        if element != "":
            output += str(count) + element
    print(output)


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

typedef struct {
    char ch;
    int count;
} MultisetEntry;

int main(void) {
    const char *word = "AAABBBBCC";
    MultisetEntry entries[32];
    int entryCount = 0;
    char output[128] = "";
    size_t i;
    int j;
    for (i = 0; i < strlen(word); i++) {
        int found = -1;
        for (j = 0; j < entryCount; j++) {
            if (entries[j].ch == word[i]) {
                found = j;
                break;
            }
        }
        if (found < 0) {
            entries[entryCount].ch = word[i];
            entries[entryCount].count = 1;
            entryCount++;
        } else {
            entries[found].count++;
        }
    }
    for (j = 0; j < entryCount; j++) {
        char piece[16];
        snprintf(piece, sizeof(piece), "%d%c", entries[j].count, entries[j].ch);
        strcat(output, piece);
    }
    printf("%s\n", output);
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Linq;

public static class Program
{
    public static void Main(string[] args)
    {
        string word = "AAABBBBCC";
        var wordsMultiset = word.GroupBy(c => c).Select(g => new { Element = g.Key, Count = g.Count() });
        string output = "";
        foreach (var entry in wordsMultiset)
        {
            if (entry.Element != '\0')
            {
                output += entry.Count.ToString() + entry.Element;
            }
        }
        Console.WriteLine(output);
    }
}
''',
}

OUTPUTS["T241"] = {
    "python": r'''
def main():
    hm = {}
    print("Enter an String:")
    s1 = input()
    for ch in s1:
        if ch not in hm:
            hm[ch] = 1
        else:
            hm[ch] = hm[ch] + 1
    print("The Charecters are:" + str(hm))


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>

int main(void) {
    int counts[256] = {0};
    char s1[1024];
    int first = 1;
    printf("Enter an String:\n");
    if (scanf("%1023[^\n]", s1) != 1) return 0;
    for (int i = 0; s1[i] != '\0'; i++) {
        counts[(unsigned char) s1[i]]++;
    }
    printf("The Charecters are:{");
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 0) {
            if (!first) printf(", ");
            printf("%c=%d", (char) i, counts[i]);
            first = 0;
        }
    }
    printf("}\n");
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;

public static class Program
{
    public static void Main(string[] args)
    {
        var hm = new Dictionary<char, int>();
        Console.WriteLine("Enter an String:");
        string s1 = Console.ReadLine();
        foreach (char ch in s1)
        {
            if (!hm.ContainsKey(ch))
            {
                hm[ch] = 1;
            }
            else
            {
                hm[ch] = hm[ch] + 1;
            }
        }
        Console.WriteLine("The Charecters are:" + string.Join(", ", hm));
    }
}
''',
}

OUTPUTS["T238"] = {
    "python": r'''
def main():
    name = "AnuvratAnuvra"
    counts = {}
    for val in name:
        counts[val] = counts.get(val, 0) + 1
    for key, value in counts.items():
        if value > 1:
            print(f"{key}:{value}")


if __name__ == "__main__":
    main()
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *name = "AnuvratAnuvra";
    int counts[256] = {0};
    int first = 1;
    for (size_t i = 0; i < strlen(name); i++) {
        counts[(unsigned char) name[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 1) {
            if (!first) printf("\n");
            printf("%c:%d", (char) i, counts[i]);
            first = 0;
        }
    }
    printf("\n");
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;

public static class Program
{
    public static void Main(string[] args)
    {
        string name = "AnuvratAnuvra";
        var map = new Dictionary<char, int>();
        foreach (char val in name)
        {
            map[val] = map.ContainsKey(val) ? map[val] + 1 : 1;
        }
        foreach (var entry in map)
        {
            if (entry.Value > 1)
            {
                Console.WriteLine(entry.Key + ":" + entry.Value);
            }
        }
    }
}
''',
}

OUTPUTS["T202"] = {
    "python": r'''
import os
import shutil


def copy_folder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            target_root = os.path.join(dest, os.path.relpath(root, src))
            if not os.path.exists(target_root):
                os.makedirs(target_root)
            for name in files:
                s = os.path.join(root, name)
                d = os.path.join(target_root, name)
                shutil.copy(s, d)
    except Exception as ex:
        print(ex)
''',
    "c": r'''
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

static void copy_folder_recursive(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    struct dirent *entry;
    if (!dir) return;
    mkdir(dest, 0755);
    while ((entry = readdir(dir)) != NULL) {
        char srcPath[1024], destPath[1024];
        struct stat st;
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
        snprintf(srcPath, sizeof(srcPath), "%s/%s", src, entry->d_name);
        snprintf(destPath, sizeof(destPath), "%s/%s", dest, entry->d_name);
        if (stat(srcPath, &st) == 0 && S_ISDIR(st.st_mode)) {
            copy_folder_recursive(srcPath, destPath);
        } else {
            FILE *in = fopen(srcPath, "rb");
            FILE *out = fopen(destPath, "wb");
            if (in && out) {
                char buf[4096];
                size_t n;
                while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
                    fwrite(buf, 1, n, out);
                }
            }
            if (in) fclose(in);
            if (out) fclose(out);
        }
    }
    closedir(dir);
}

void copy_folder(const char *src, const char *dest) {
    copy_folder_recursive(src, dest);
}
''',
    "csharp": r'''
using System;
using System.IO;

public static class FolderCopier
{
    public static void CopyFolder(string src, string dest)
    {
        try
        {
            foreach (string dirPath in Directory.GetDirectories(src, "*", SearchOption.AllDirectories))
            {
                Directory.CreateDirectory(dirPath.Replace(src, dest));
            }
            foreach (string filePath in Directory.GetFiles(src, "*", SearchOption.AllDirectories))
            {
                File.Copy(filePath, filePath.Replace(src, dest), true);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.StackTrace);
        }
    }
}
''',
}

OUTPUTS["T693"] = {
    "python": r'''
def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    if amount < 0 or len(coins) == check_from_index:
        return 0
    with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
    without_first_coin = find_combinations_count(amount, coins, check_from_index + 1)
    return with_first_coin + without_first_coin
''',
    "c": r'''
int find_combinations_count(int amount, const int *coins, int coinCount, int check_from_index) {
    if (amount == 0) return 1;
    if (amount < 0 || coinCount == check_from_index) return 0;
    int with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, coinCount, check_from_index);
    int without_first_coin = find_combinations_count(amount, coins, coinCount, check_from_index + 1);
    return with_first_coin + without_first_coin;
}
''',
    "csharp": r'''
public static class CoinCombinations
{
    public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0) return 1;
        if (amount < 0 || coins.Length == checkFromIndex) return 0;
        int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}
''',
}

OUTPUTS["T347"] = {
    "python": r'''
class ThousandsProcessor:
    SEPARATOR = " "
    EXPONENT = 2

    def __init__(self, unit_processor, scale_processor, tens_processor):
        self.unit_processor = unit_processor
        self.scale_processor = scale_processor
        self.tens_processor = tens_processor

    def get_name(self, value):
        buffer = []
        if value == "":
            number = 0
        elif len(value) > 4:
            number = int(value[-4:])
        else:
            number = int(value)
        number %= 1000
        if number >= 100:
            buffer.append(self.unit_processor.get_name(number // 100))
            buffer.append(self.SEPARATOR)
            buffer.append(self.scale_processor.get_name(self.EXPONENT))
        tens_name = self.tens_processor.get_name(number % 100)
        if tens_name != "" and number >= 100:
            buffer.append(self.SEPARATOR)
        buffer.append(tens_name)
        return "".join(buffer)
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SEPARATOR " "
#define EXPONENT 2

static void unit_processor_name(int number, char *out, size_t outSize);
static void scale_processor_name(int exponent, char *out, size_t outSize);
static void tens_processor_name(int number, char *out, size_t outSize);

void get_name(const char *value, char *result, size_t resultSize) {
    int number;
    char piece[64];
    char tensName[64];
    result[0] = '\0';
    if (value[0] == '\0') {
        number = 0;
    } else if (strlen(value) > 4) {
        number = atoi(value + strlen(value) - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        unit_processor_name(number / 100, piece, sizeof(piece));
        strcat(result, piece);
        strcat(result, SEPARATOR);
        scale_processor_name(EXPONENT, piece, sizeof(piece));
        strcat(result, piece);
    }
    tens_processor_name(number % 100, tensName, sizeof(tensName));
    if (tensName[0] != '\0' && number >= 100) {
        strcat(result, SEPARATOR);
    }
    strcat(result, tensName);
}
''',
    "csharp": r'''
using System;
using System.Text;

public interface INameProcessor
{
    string GetName(int number);
}

public class ThousandsProcessor
{
    private const string SEPARATOR = " ";
    private const int EXPONENT = 2;

    private readonly INameProcessor unitProcessor;
    private readonly INameProcessor scaleProcessor;
    private readonly INameProcessor tensProcessor;

    public ThousandsProcessor(INameProcessor unitProcessor, INameProcessor scaleProcessor, INameProcessor tensProcessor)
    {
        this.unitProcessor = unitProcessor;
        this.scaleProcessor = scaleProcessor;
        this.tensProcessor = tensProcessor;
    }

    public string GetName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        int number;
        if ("".Equals(value))
        {
            number = 0;
        }
        else if (value.Length > 4)
        {
            number = int.Parse(value.Substring(value.Length - 4));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 1000;
        if (number >= 100)
        {
            buffer.Append(unitProcessor.GetName(number / 100));
            buffer.Append(SEPARATOR);
            buffer.Append(scaleProcessor.GetName(EXPONENT));
        }
        string tensName = tensProcessor.GetName(number % 100);
        if (!"".Equals(tensName) && number >= 100)
        {
            buffer.Append(SEPARATOR);
        }
        buffer.Append(tensName);
        return buffer.ToString();
    }
}
''',
}

OUTPUTS["T253"] = {
    "python": r'''
import random


def shuffle_array(ar):
    for i in range(len(ar) - 1, 0, -1):
        index = random.randint(0, i)
        ar[index], ar[i] = ar[i], ar[index]
''',
    "c": r'''
#include <stdlib.h>

void shuffle_array(int *ar, int length) {
    int i;
    for (i = length - 1; i > 0; i--) {
        int index = rand() % (i + 1);
        int a = ar[index];
        ar[index] = ar[i];
        ar[i] = a;
    }
}
''',
    "csharp": r'''
using System;

public static class Shuffler
{
    private static readonly Random Rnd = new Random();

    public static void ShuffleArray(int[] ar)
    {
        for (int i = ar.Length - 1; i > 0; i--)
        {
            int index = Rnd.Next(i + 1);
            int temp = ar[index];
            ar[index] = ar[i];
            ar[i] = temp;
        }
    }
}
''',
}

OUTPUTS["R8549838705"] = r'''
int main (void) {
    const int array_a [3] = {2, 4, 6};
    const int array_b [3] = {1, 3, 5};
    int array_c [6] = {0};
    int i = 0;
    concat (array_a, array_b, array_c, 3);
    while (i < 6) {
        printf ("array_c[%d]=%d\n", i, *(array_c + i));
        ++i;
    }
    return 0;
}
'''

OUTPUTS["Reec8438c4b"] = r'''
int main (void) {
    FILE *fin = fopen ("in.txt", "r");
    FILE *fout = fopen ("out.txt", "w");
    int character;
    if (fin == NULL || fout == NULL) {
        return 1;
    }
    do {
        character = fgetc (fin);
        if (character != EOF) {
            printCharWithSpaces (character, fin, fout);
        }
    } while (character != EOF);
    fclose (fin);
    fclose (fout);
    printf ("\nFile has been created...\n");
    return 0;
}
'''

OUTPUTS["Rd776867156"] = r'''
public static void close (Statement...statements) {
    int index = 0;
    while (index < statements.length) {
        Statement stmt = statements [index];
        if (stmt != null) {
            try {
                stmt.close ();
            } catch (SQLException se) {
            }
        }
        index ++;
    }
}
'''

OUTPUTS["Rb67c7892a4"] = r'''
public void run () {
    try {
        int i = 0;
        while (i < 2) {
            System.out.println ("tic");
            i ++;
        }
    } catch (Exception e) {
        e.getStackTrace ();
    }
}
'''

OUTPUTS["R8818908361"] = r'''
#include <stdio.h>
#include <string.h>

int main (void) {
    char months [] = "JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC";
    char *token;
    printf ("months=[%s]\n\n", months);
    token = strtok (months, ",");
    while (token != NULL) {
        printf ("month=[%s]\n", token);
        token = strtok (NULL, ",");
    }
    printf ("\n");
    return 0;
}
'''

OUTPUTS["Rd613be00ca"] = r'''
public static byte [] readBytes (InputStream inputStream) throws IOException {
    byte [] buffer = new byte [32 * 1024];
    int bufferSize = 0;
    boolean eof = false;
    while (! eof) {
        int read = inputStream.read (buffer, bufferSize, buffer.length - bufferSize);
        if (read < 0) {
            eof = true;
        } else {
            bufferSize += read;
            if (bufferSize == buffer.length) {
                buffer = Arrays.copyOf (buffer, bufferSize * 2);
            }
        }
    }
    return Arrays.copyOf (buffer, bufferSize);
}
'''

OUTPUTS["R84ca6c9dcf"] = r'''
public void actionPerformed (ActionEvent e) {
    Color c = label.getBackground ();
    boolean flashing = FLASH_COLOR.equals (c);
    label.setBackground (flashing ? null : FLASH_COLOR);
    label.setForeground (flashing ? Color.black : Color.white);
}
'''

OUTPUTS["Ra1d335a7d8"] = r'''
#include <stdio.h>
#include <string.h>

int main (void) {
    char str [] = "This is abc test abc string";
    char *delim = "abc";
    char *in = str;
    char *token = strstr (in, delim);
    while (token != NULL) {
        *token = '\0';
        printf ("%s\n", in);
        in = token + strlen (delim);
        token = strstr (in, delim);
    }
    printf ("%s\n", in);
    return 0;
}
'''

OUTPUTS["R73286ffa0d"] = r'''
public static void main (String [] args) {
    CustomClassLoader loader = new CustomClassLoader ();
    try {
        Class < ? > c = loader.findClass ("sample.Sample");
        c.newInstance ();
    } catch (ClassNotFoundException | InstantiationException | IllegalAccessException e) {
        e.printStackTrace ();
    }
}
'''

OUTPUTS["Rf3a21bb32a"] = r'''
private static void ExpandItemWithInitialExpandedAttribute (PropertyGrid propertyGrid, GridItem gridItem) {
    if (gridItem == null)
        return;
    if (gridItem.GridItemType == GridItemType.Property && gridItem.Expandable) {
        object [] objs = gridItem.Value.GetType ().GetCustomAttributes (typeof (PropertyGridInitialExpandedAttribute), false);
        if (objs.Length > 0 && ((PropertyGridInitialExpandedAttribute) objs [0]).InitialExpanded) {
            gridItem.Expanded = true;
        }
    }
    foreach (GridItem childItem in gridItem.GridItems) {
        ExpandItemWithInitialExpandedAttribute (propertyGrid, childItem);
    }
}
'''

OUTPUTS["R9955954078"] = r'''
public static IEnumerable < IEnumerable < T > > GetPermutations < T > (IEnumerable < IEnumerable < T > > lists) {
    if (! lists.Any ()) {
        yield break;
    }
    List < IEnumerator < T > > iterators = new List < IEnumerator < T > > ();
    foreach (var list in lists) {
        var it = list.GetEnumerator ();
        if (it.MoveNext ()) {
            iterators.Add (it);
        }
    }
    bool done = false;
    while (! done) {
        yield return iterators.Select (it => it.Current);
        int index = 0;
        while (index < iterators.Count) {
            if (iterators [index].MoveNext ()) {
                break;
            }
            iterators [index].Reset ();
            iterators [index].MoveNext ();
            index ++;
        }
        if (index == iterators.Count) {
            done = true;
        }
    }
}
'''

OUTPUTS["Rbcd6619d12"] = r'''
private static CompletableFuture < Void > logAndFail (String page) {
    System.out.println (page);
    throw new IllegalArgumentException ("unexpected exception");
}

public static void main (String [] args) {
    CompletableFuture < String > future = readPage ();
    CompletableFuture < Void > future2 = future.thenAccept (Program::logAndFail);
    future2.exceptionally (e -> {
        e.printStackTrace (System.err);
        return null;
    });
}
'''

OUTPUTS["R1ff2f32faf"] = r'''
def update(self, instance, validated_data):
    if "user" in validated_data:
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.update(instance.user, user_data)
    super(ProfileSerializer, self).update(instance, validated_data)
    return instance
'''

OUTPUTS["Rb3104c30c4"] = r'''
[Route ("Login")]
public HttpResponseMessage GetLogin () {
    var queryParams = new Dictionary < string, string > {
        ["response_type"] = "code",
        ["client_id"] = _clientId,
        ["redirect_uri"] = HttpUtility.UrlEncode ("http://YourWebsiteURL/api/Account/OAuthCallback"),
        ["scope"] = HttpUtility.UrlEncode ("Space Seperated list of scopes"),
        ["access_type"] = "Either online or offline",
        ["approval_prompt"] = "auto",
        ["include_granted_scopes"] = "true"
    };
    string requestUri = "https://accounts.google.com/o/oauth2/auth?" + string.Join ("&", queryParams.Select (p => p.Key + "=" + p.Value));
    HttpResponseMessage response = Request.CreateResponse (HttpStatusCode.MovedPermanently);
    response.Headers.Location = new Uri (requestUri);
    return response;
}
'''

OUTPUTS["R7ec3eaaa23"] = r'''
static void fill_and_print_1d (int n) {
    arr m = makearr (1, (int []) {n});
    for (int i = 0; i < n; i++)
        *elem (m, i) = i;
    for (int i = 0; i < n; i++, printf (" "))
        printf ("%d", *elem (m, i));
}

static void fill_and_print_2d (int n) {
    arr m = makearr (2, (int []) {n, n});
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            *elem (m, i, j) = i * n + j;
    for (int i = 0; i < n; i++, printf ("\n"))
        for (int j = 0; j < n; j++, printf (" "))
            printf ("%d", *elem (m, i, j));
}

static void fill_and_print_3d (int n) {
    arr m = makearr (3, (int []) {n, n, n});
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                *elem (m, i, j, k) = (i * n + j) * n + k;
    for (int i = 0; i < n; i++, printf ("\n"))
        for (int j = 0; j < n; j++, printf ("\n"))
            for (int k = 0; k < n; k++, printf (" "))
                printf ("%d", *elem (m, i, j, k));
}

int main (void) {
    fill_and_print_1d (6);
    puts ("\n");
    fill_and_print_2d (4);
    puts ("\n");
    fill_and_print_3d (3);
    return 0;
}
'''

OUTPUTS["Rf2339edd09"] = r'''
def checkLen():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    position = days.index("Monday") if "Monday" in days else -1
    if position != -1:
        print("found")
        print(position)
'''

OUTPUTS["R4dea8b0dc2"] = r'''
def graphWriter():
    data = {file: np.fromregex(file, r'\d*\.\d*',
                               dtype=[('1', float), ('2', float),
                                      ('3', float), ('4', float)])
            for file in g.glob('*.TXT')}
    fig, ax = plt.subplots()
    list(ax.plot(d['3'], d['4']) for d in data.values())
    plt.show()
    plt.close(fig)
'''

OUTPUTS["Rd85db6db53"] = r'''
def unique(x):
    seen = set(x)
    return [item for item in x if item in seen]
'''

OUTPUTS["Rbc3ee3aa80"] = r'''
boolean isPalindrome (String s) {
    int left = 0;
    int right = s.length () - 1;
    while (left < right) {
        if (s.charAt (left ++) != s.charAt (right --)) {
            return false;
        }
    }
    return true;
}
'''

OUTPUTS["R429c244914"] = r'''
int main () {
    double num = -1;
    int ret;
    printf ("Enter a positive number:");
    ret = scanf ("%lf", &num);
    while (num < 0) {
        if (ret != 1) {
            while (getchar () != '\n')
                ;
        }
        printf ("%s", (ret != 1)
            ? "Error! Please enter a number: "
            : "Error! Please enter a positive number: ");
        ret = scanf ("%lf", &num);
    }
    printf ("Your number is %.2lf", num);
    return 0;
}
'''

OUTPUTS["Rd469f2767c"] = r'''
int main (void) {
    const char *str = "Polly";
    unsigned int len = strlen (str);
    char buffer [len + 1];
    for (int end = (int) len - 1; end >= 0; end--) {
        for (size_t start = 0; start < len; start++) {
            slice_str (str, buffer, start, end);
            printf ("%s\n", buffer);
        }
    }
    return 0;
}
'''

OUTPUTS["R8fb5cc8c61"] = r'''
def rev(test):
    chars = list(test)
    result = []
    print(chars)
    while chars:
        result.append(chars.pop())
    return "".join(result)
'''

OUTPUTS["R1016fe8c54"] = r'''
int main () {
    char c;
    while (scanf ("%c", &c) == 1) {
        switch (c) {
            case 'q':
            case 'Q':
                continue;
            default:
                printf ("%c", c);
        }
    }
    return 0;
}
'''

OUTPUTS["R7847bddc00"] = r'''
int main () {
    int array [TABLES] [ROWS] [COLS] = {{{10, 20}, {30, 40}, {50, 60}, {70, 80}, {90, 100}}, {{18, 21}, {3, 4}, {5, 6}, {7, 81}, {9, 11}}};
    for (size_t i = 0; i < TABLES; ++i) {
        for (size_t j = 0; j < ROWS; ++j) {
            for (size_t k = 0; k < COLS; ++k) {
                printf ("(%lu, %lu, %lu): %u\n", (unsigned long) i, (unsigned long) j, (unsigned long) k, array [i] [j] [k]);
            }
        }
    }
    return 0;
}
'''

OUTPUTS["R209b6aeaa2"] = r'''
def __init__(self):
    wx.Frame.__init__(self, None, -1, "Test", size=(500, 270))
    panel = wx.Panel(self, -1)
    for label, pos, handler in (("Start thread", (0, 0), self.startThread),
                                ("Change var", (0, 30), self.changeVar)):
        button = wx.Button(panel, -1, label=label, pos=pos)
        panel.Bind(wx.EVT_BUTTON, handler, id=button.GetId())
'''


def main():
    with open(SEED, encoding="utf-8") as f:
        seeds = json.load(f)
    ids = [s["id"] for s in seeds]
    assert len(ids) == len(set(ids)), "duplicate seed ids"
    result = []
    for sid in ids:
        entry = OUTPUTS[sid]
        if isinstance(entry, dict):
            assert set(entry) == {"python", "c", "csharp"}, sid
            for lang, code in entry.items():
                assert len(code.strip()) >= 20, (sid, lang)
                if lang == "python":
                    ast.parse(code)
            result.append({"id": sid, "outputs": entry})
        else:
            assert len(entry.strip()) >= 20, sid
            result.append({"id": sid, "output": entry})
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print("OK", OUT, len(result), "entries")


if __name__ == "__main__":
    main()
