DATA_P4 = {}

DATA_P4["T731"] = {"outputs": {
"python": r'''
import math
import time


class Graphics:
    def draw_image(self, img, x, y, observer): pass
    def set_color(self, c): pass
    def fill_oval(self, x, y, w, h): pass
    def draw_string(self, s, x, y): pass


class Painter:
    RADIUS = 10
    FRAMES = 100

    def __init__(self):
        self.background = None
        self.index = 0
        self.frame_count = 0
        self.total_time = 0
        self.average_time = 0.0
        self.rect = type("Rect", (), {"x": 0, "y": 0, "width": 0, "height": 0})()

    def get_width(self): return 800
    def get_height(self): return 600

    def paintComponent(self, g):
        start = time.perf_counter_ns()
        w = self.get_width()
        h = self.get_height()
        g.draw_image(self.background, 0, 0, self)
        theta = 2 * math.pi * self.index / 64
        self.index += 1
        g.set_color("blue")
        self.rect.x = int(math.sin(theta) * w / 3 + w / 2 - self.RADIUS)
        self.rect.y = int(math.cos(theta) * h / 3 + h / 2 - self.RADIUS)
        self.rect.width = 2 * self.RADIUS
        self.rect.height = 2 * self.RADIUS
        g.fill_oval(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        g.set_color("white")
        if self.frame_count == self.FRAMES:
            self.average_time = self.total_time / self.FRAMES
            self.total_time = 0
            self.frame_count = 0
        else:
            self.total_time += time.perf_counter_ns() - start
            self.frame_count += 1
        g.draw_string("%10.3f" % (self.average_time / 1e6), 5, 16)
''',
"c": r'''
#include <math.h>
#include <stdio.h>
#include <time.h>

#define RADIUS 10
#define FRAMES 100

typedef struct { int x, y, width, height; } Rect;

static void *background = NULL;
static double totalTime = 0;
static double averageTime = 0;
static int frameCount = 0;
static int indexCounter = 0;
static Rect rect;

void drawImage(void *img, int x, int y) {}
void setColor(const char *c) {}
void fillOval(int x, int y, int w, int h) {}
void drawString(const char *s, int x, int y) {}
int getWidth(void) { return 800; }
int getHeight(void) { return 600; }

void paintComponent(void) {
    clock_t start = clock();
    int w = getWidth();
    int h = getHeight();
    drawImage(background, 0, 0);
    double theta = 2 * M_PI * indexCounter++ / 64;
    setColor("blue");
    rect.x = (int)(sin(theta) * w / 3 + w / 2 - RADIUS);
    rect.y = (int)(cos(theta) * h / 3 + h / 2 - RADIUS);
    rect.width = 2 * RADIUS;
    rect.height = 2 * RADIUS;
    fillOval(rect.x, rect.y, rect.width, rect.height);
    setColor("white");
    if (frameCount == FRAMES) {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    } else {
        totalTime += (double)(clock() - start) * 1e9 / CLOCKS_PER_SEC;
        frameCount++;
    }
    char s[32];
    sprintf(s, "%10.3f", averageTime / 1000000.0);
    drawString(s, 5, 16);
}
''',
"csharp": r'''
using System;

public class PointEx { public int X, Y; }

public class GraphicsEx
{
    public void DrawImage(object img, int x, int y) { }
    public void SetColor(string c) { }
    public void FillOval(int x, int y, int w, int h) { }
    public void DrawString(string s, int x, int y) { }
}

public class PaintPanel
{
    private const int RADIUS = 10;
    private const int FRAMES = 100;

    private object background;
    private int index;
    private int frameCount;
    private long totalTime;
    private double averageTime;
    private PointEx rect = new PointEx();

    private int GetWidth() { return 800; }
    private int GetHeight() { return 600; }

    public void PaintComponent(GraphicsEx g)
    {
        long start = DateTime.UtcNow.Ticks * 100;
        int w = GetWidth();
        int h = GetHeight();
        g.DrawImage(background, 0, 0);
        double theta = 2 * Math.PI * index++ / 64;
        g.SetColor("blue");
        rect.X = (int)(Math.Sin(theta) * w / 3 + w / 2 - RADIUS);
        rect.Y = (int)(Math.Cos(theta) * h / 3 + h / 2 - RADIUS);
        g.FillOval(rect.X, rect.Y, 2 * RADIUS, 2 * RADIUS);
        g.SetColor("white");
        if (frameCount == FRAMES)
        {
            averageTime = totalTime / FRAMES;
            totalTime = 0;
            frameCount = 0;
        }
        else
        {
            totalTime += DateTime.UtcNow.Ticks * 100 - start;
            frameCount++;
        }
        string s = string.Format("{0,10:0.000}", averageTime / 1000000d);
        g.DrawString(s, 5, 16);
    }
}
'''}}

DATA_P4["T428"] = {"outputs": {
"python": r'''
import traceback


class ProcessWatcher:
    def __init__(self, pro, out_stream):
        self.pro = pro
        self.out_stream = out_stream

    def println(self, msg):
        print(msg)

    def run(self):
        try:
            ret_value = self.pro.wait()
            self.println("Command exit with return value " + str(ret_value))
            self.out_stream.close()
            self.out_stream = None
        except (OSError, ValueError) as e:
            traceback.print_exc()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

extern FILE *outStream;
extern int childPid;

void println(const char *msg) {
    printf("%s\n", msg);
}

void run(void) {
    int status;
    if (waitpid(childPid, &status, 0) < 0) {
        perror("waitpid failed");
        return;
    }
    int retValue = WEXITSTATUS(status);
    char msg[64];
    sprintf(msg, "Command exit with return value %d", retValue);
    println(msg);
    if (outStream != NULL) {
        fclose(outStream);
        outStream = NULL;
    }
}
''',
"csharp": r'''
using System;
using System.Diagnostics;
using System.IO;

public class ProcessRunner
{
    private Process pro;
    private Stream outStream;

    private void WriteLine(string msg) { Console.WriteLine(msg); }

    public void Run()
    {
        try
        {
            pro.WaitForExit();
            int retValue = pro.ExitCode;
            WriteLine("Command exit with return value " + retValue);
            outStream.Close();
            outStream = null;
        }
        catch (Exception e)
        {
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}
'''}}

DATA_P4["T626"] = {"outputs": {
"python": r'''
def removeEven(k, n):
    counter = 0
    for i in range(n):
        if k[i] % 2 == 1:
            k[counter] = k[i]
            counter += 1
    while counter < n:
        k[counter] = 0
        counter += 1
''',
"c": r'''
void removeEven(int *k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++)
        if (k[i] % 2 == 1) k[counter++] = k[i];
    while (counter < n)
        k[counter++] = 0;
}
''',
"csharp": r'''
public static class EvenRemover
{
    public static void RemoveEven(int[] k, int n)
    {
        int counter = 0;
        for (int i = 0; i < n; i++)
        {
            if (k[i] % 2 == 1)
            {
                k[counter++] = k[i];
            }
        }
        while (counter < n)
        {
            k[counter++] = 0;
        }
    }
}
'''}}

DATA_P4["T813"] = {"outputs": {
"python": r'''
def toHexString(bytes):
    hex_string = []
    for b in bytes:
        hex_string.append(format(b & 0xFF, "02x"))
    return "".join(hex_string)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>

char *toHexString(const unsigned char *bytes, int length) {
    char *hexString = malloc((size_t)length * 2 + 1);
    for (int i = 0; i < length; i++)
        sprintf(hexString + i * 2, "%02x", 0xFF & bytes[i]);
    hexString[length * 2] = '\0';
    return hexString;
}
''',
"csharp": r'''
using System.Text;

public static class HexUtil
{
    public static string ToHexString(byte[] bytes)
    {
        StringBuilder hexString = new StringBuilder(bytes.Length * 2);
        foreach (byte b in bytes)
        {
            hexString.Append(b.ToString("x2"));
        }
        return hexString.ToString();
    }
}
'''}}

DATA_P4["T333"] = {"outputs": {
"python": r'''
UNION_SEPARATOR = " "

TOKENS = ["ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


class UnitProcessor:
    def get_name(self, n):
        return str(n)


unitProcessor = UnitProcessor()


def getName(value):
    buffer = []
    if len(value) > 3:
        number = int(value[len(value) - 3:])
    else:
        number = int(value)
    number %= 100
    if number >= 20:
        buffer.append(TOKENS[(number // 10) - 2])
        number %= 10
        tens_found = True
    else:
        number %= 20
        tens_found = False
    if number != 0:
        if tens_found:
            buffer.append(UNION_SEPARATOR)
        buffer.append(unitProcessor.get_name(number))
    return "".join(buffer)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *TOKENS[9] = {"ten", "twenty", "thirty", "forty", "fifty",
                         "sixty", "seventy", "eighty", "ninety"};
const char *UNION_SEPARATOR = " ";

char *unitProcessor_getName(int n) {
    char *s = malloc(16);
    sprintf(s, "%d", n);
    return s;
}

char *getName(const char *value) {
    char *buffer = malloc(64);
    int number, tensFound = 0;
    buffer[0] = '\0';
    if (strlen(value) > 3) {
        number = atoi(value + strlen(value) - 3);
    } else {
        number = atoi(value);
    }
    number %= 100;
    if (number >= 20) {
        strcat(buffer, TOKENS[(number / 10) - 2]);
        number %= 10;
        tensFound = 1;
    } else {
        number %= 20;
    }
    if (number != 0) {
        if (tensFound) strcat(buffer, UNION_SEPARATOR);
        char *unit = unitProcessor_getName(number);
        strcat(buffer, unit);
        free(unit);
    }
    return buffer;
}
''',
"csharp": r'''
using System.Text;

public static class TensNamer
{
    private static readonly string[] Tokens = { "ten", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety" };
    private const string UnionSeparator = " ";

    private static string UnitGetName(int n) { return n.ToString(); }

    public static string GetName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        int number;
        if (value.Length > 3)
        {
            number = int.Parse(value.Substring(value.Length - 3));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 100;
        bool tensFound;
        if (number >= 20)
        {
            buffer.Append(Tokens[(number / 10) - 2]);
            number %= 10;
            tensFound = true;
        }
        else
        {
            number %= 20;
            tensFound = false;
        }
        if (number != 0)
        {
            if (tensFound)
            {
                buffer.Append(UnionSeparator);
            }
            buffer.Append(UnitGetName(number));
        }
        return buffer.ToString();
    }
}
'''}}
