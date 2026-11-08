DATA3 = {}

DATA3["T92"] = {
    "python": """def compress_bad(s):
    countConsecutive = 0
    compressedString = []
    for i in range(len(s)):
        countConsecutive += 1
        if len(s) == i + 1:
            compressedString.append(s[i] + str(countConsecutive))
            break
        elif s[i] != s[i + 1]:
            compressedString.append(s[i] + str(countConsecutive))
            countConsecutive = 0
    return "".join(compressedString)""",
    "c": """void compressBad(const char *str, char *out) {
    int countConsecutive = 0, pos = 0;
    size_t len = strlen(str);
    for (size_t i = 0; i < len; i++) {
        countConsecutive++;
        if (len == i + 1) {
            pos += sprintf(out + pos, "%c%d", str[i], countConsecutive);
            break;
        } else if (str[i] != str[i + 1]) {
            pos += sprintf(out + pos, "%c%d", str[i], countConsecutive);
            countConsecutive = 0;
        }
    }
    out[pos] = '\\0';
}""",
    "csharp": """using System.Text;

public static string CompressBad(string str)
{
    int countConsecutive = 0;
    var sb = new StringBuilder();
    for (int i = 0; i < str.Length; i++)
    {
        countConsecutive++;
        if (str.Length == i + 1)
        {
            sb.Append(str[i]).Append(countConsecutive);
            break;
        }
        else if (str[i] != str[i + 1])
        {
            sb.Append(str[i]).Append(countConsecutive);
            countConsecutive = 0;
        }
    }
    return sb.ToString();
}""",
}

DATA3["T694"] = {
    "python": """from itertools import product

class Foo:
    def __init__(self, data):
        self.data = data

    def allUniqueCombinations(self):
        keys = list(self.data.keys())
        return [dict(zip(keys, combo)) for combo in product(*(self.data[k] for k in keys))]

def main():
    data = {"foo": ["1", "2", "3"], "bar": ["3", "2"], "baz": ["5", "6", "7"]}
    foo = Foo(data)
    for combination in foo.allUniqueCombinations():
        print(combination)""",
    "c": """const char *foo[] = {"1", "2", "3"};
const char *bar[] = {"3", "2"};
const char *baz[] = {"5", "6", "7"};

int main(void) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 3; k++) {
                printf("[\\"%s\\", \\"%s\\", \\"%s\\"]\\n", foo[i], bar[j], baz[k]);
            }
        }
    }
    return 0;
}""",
    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;

public static void Main()
{
    var data = new Dictionary<string, List<string>>
    {
        { "foo", new List<string> { "1", "2", "3" } },
        { "bar", new List<string> { "3", "2" } },
        { "baz", new List<string> { "5", "6", "7" } }
    };
    var foo = new Foo(data);
    foreach (var combination in foo.AllUniqueCombinations())
    {
        Console.WriteLine("[" + string.Join(", ", combination) + "]");
    }
}

public class Foo
{
    private Dictionary<string, List<string>> data;

    public Foo(Dictionary<string, List<string>> data) { this.data = data; }

    public IEnumerable<string[]> AllUniqueCombinations()
    {
        var keys = data.Keys.ToList();
        var indices = new int[keys.Count];
        while (true)
        {
            yield return keys.Select((k, i) => data[k][indices[i]]).ToArray();
            int pos = keys.Count - 1;
            while (pos >= 0)
            {
                indices[pos]++;
                if (indices[pos] < data[keys[pos]].Count) break;
                indices[pos] = 0;
                pos--;
            }
            if (pos < 0) yield break;
        }
    }
}""",
}

DATA3["T546"] = {
    "python": """def join(objects, delimiter):
    if len(objects) == 0:
        return ""
    return delimiter.join(str(o) for o in objects)""",
    "c": """char *join(char **objects, int count, const char *delimiter) {
    if (count == 0) return strdup("");
    size_t cap = 64, len = 0;
    char *ret = malloc(cap);
    ret[0] = '\\0';
    for (int i = 0; i < count; i++) {
        const char *piece = objects[i];
        size_t plen = strlen(piece);
        size_t dlen = (i > 0) ? strlen(delimiter) : 0;
        while (len + plen + dlen + 1 > cap) {
            cap *= 2;
            ret = realloc(ret, cap);
        }
        if (i > 0) {
            strcat(ret, delimiter);
        }
        strcat(ret, piece);
        len += plen + dlen;
    }
    return ret;
}""",
    "csharp": """using System;
using System.Linq;

public static string Join(object[] objects, string delimiter)
{
    if (objects.Length == 0) return "";
    return string.Join(delimiter, objects.Select(o => o.ToString()));
}""",
}

DATA3["T567"] = {
    "python": """import threading

class Shared:
    def __init__(self):
        self.state = 0
        self.cond = threading.Condition()

s = Shared()

def run():
    i = 3
    while i < 50:
        with s.cond:
            while s.state != 2:
                s.cond.wait()
            print("t3 " + str(i))
            i += 3
            s.state = 3
            s.cond.notify_all()""",
    "c": """pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int sharedState = 0;

void *run(void *arg) {
    int i = 3;
    while (i < 50) {
        pthread_mutex_lock(&lock);
        while (sharedState != 2) {
            pthread_cond_wait(&cond, &lock);
        }
        printf("t3 %d\\n", i);
        i += 3;
        sharedState = 3;
        pthread_cond_broadcast(&cond);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}""",
    "csharp": """using System;
using System.Threading;

private readonly object s = new object();
private int state;

public void Run()
{
    int i = 3;
    while (i < 50)
    {
        lock (s)
        {
            while (state != 2)
            {
                Monitor.Wait(s);
            }
            Console.WriteLine("t3 " + i);
            i += 3;
            state = 3;
            Monitor.PulseAll(s);
        }
    }
}""",
}

DATA3["T731"] = {
    "python": """import math
import time

class Rect:
    def __init__(self):
        self.x = self.y = self.width = self.height = 0

class Painter:
    def __init__(self, background):
        self.background = background
        self.rect = Rect()
        self.index = 0
        self.frameCount = 0
        self.totalTime = 0
        self.averageTime = 0
        self.RADIUS = 10
        self.FRAMES = 16

    def paintComponent(self, g, w, h):
        start = time.perf_counter_ns()
        g.drawImage(self.background, 0, 0, self)
        theta = 2 * math.pi * self.index / 64
        self.index += 1
        g.setColor("blue")
        self.rect.x = int(math.sin(theta) * w / 3 + w / 2 - self.RADIUS)
        self.rect.y = int(math.cos(theta) * h / 3 + h / 2 - self.RADIUS)
        self.rect.width = 2 * self.RADIUS
        self.rect.height = 2 * self.RADIUS
        g.fillOval(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        g.setColor("white")
        if self.frameCount == self.FRAMES:
            self.averageTime = self.totalTime // self.FRAMES
            self.totalTime = 0
            self.frameCount = 0
        else:
            self.totalTime += time.perf_counter_ns() - start
            self.frameCount += 1
        s = "%8.3f" % (self.averageTime / 1000000)
        g.drawString(s, 5, 16)""",
    "c": """#include <time.h>
#include <math.h>

int indexCounter = 0;
long frameCount = 0, totalTime = 0, averageTime = 0;
#define FRAMES 16
#define RADIUS 10

extern void drawImage(void *background);
extern void fillOval(int x, int y, int w, int h);

void paintComponent(int w, int h) {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    drawImage(NULL);
    double theta = 2 * M_PI * indexCounter++ / 64.0;
    int x = (int)(sin(theta) * w / 3 + w / 2 - RADIUS);
    int y = (int)(cos(theta) * h / 3 + h / 2 - RADIUS);
    fillOval(x, y, 2 * RADIUS, 2 * RADIUS);
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (frameCount == FRAMES) {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    } else {
        totalTime += (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
        frameCount++;
    }
    printf("%8.3f\\n", averageTime / 1000000.0);
}""",
    "csharp": """using System;
using System.Diagnostics;

public override void PaintComponent(Graphics g)
{
    long start = Stopwatch.GetTimestamp();
    base.PaintComponent(g);
    int w = Width;
    int h = Height;
    g.DrawImage(background, 0, 0, this);
    double theta = 2 * Math.PI * index++ / 64;
    g.SetColor(Color.Blue);
    rect.SetRect((int)(Math.Sin(theta) * w / 3 + w / 2 - RADIUS),
                 (int)(Math.Cos(theta) * h / 3 + h / 2 - RADIUS), 2 * RADIUS, 2 * RADIUS);
    g.FillOval(rect.X, rect.Y, rect.Width, rect.Height);
    g.SetColor(Color.White);
    if (frameCount == FRAMES)
    {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    }
    else
    {
        totalTime += Stopwatch.GetTimestamp() - start;
        frameCount++;
    }
    string s = string.Format("{0,8:0.000}", averageTime / 1000000d);
    g.DrawString(s, font, brush, 5, 16);
}""",
}
