DATA5 = {
    "T731": {"outputs": {
        "python": '''import math
import time


class Panel:
    def get_size(self):
        return (640, 480)


class BallPainter:
    def __init__(self):
        self.panel = Panel()
        self.index = 0
        self.frame_count = 0
        self.total_time = 0
        self.average_time = 0
        self.radius = 10
        self.frames = 60

    def paint_component(self, g):
        start = time.perf_counter_ns()
        w, h = self.panel.get_size()
        theta = 2 * math.pi * self.index / 64
        self.index += 1
        g.set_color("blue")
        x = int(math.sin(theta) * w / 3 + w / 2 - self.radius)
        y = int(math.cos(theta) * h / 3 + h / 2 - self.radius)
        g.fill_oval(x, y, 2 * self.radius, 2 * self.radius)
        g.set_color("white")
        if self.frame_count == self.frames:
            self.average_time = self.total_time // self.frames
            self.total_time = 0
            self.frame_count = 0
        else:
            self.total_time += time.perf_counter_ns() - start
            self.frame_count += 1
        g.draw_string("{:5.3f}".format(self.average_time / 1e6), 5, 16)''',
        "c": r'''#include <math.h>
#include <stdio.h>
#include <time.h>

#define FRAMES 60
#define RADIUS 10

static int index_counter = 0;
static long frame_count = 0;
static long total_time = 0;
static double average_time = 0;

static void paint_component(int w, int h) {
    long start = (long) clock();
    double theta = 2 * M_PI * index_counter++ / 64;
    int x = (int) (sin(theta) * w / 3 + w / 2 - RADIUS);
    int y = (int) (cos(theta) * h / 3 + h / 2 - RADIUS);
    printf("blue oval at (%d, %d)\n", x, y);
    if (frame_count == FRAMES) {
        average_time = (double) total_time / FRAMES;
        total_time = 0;
        frame_count = 0;
    } else {
        total_time += (long) clock() - start;
        frame_count++;
    }
    printf("%5.3f\n", average_time / 1000000.0);
}''',
        "csharp": '''using System;
using System.Drawing;

public class AnimationPanel
{
    private const int Frames = 60;
    private const int Radius = 10;

    private int index;
    private long totalTime;
    private int frameCount;
    private double averageTime;
    private readonly Image background;

    public void PaintComponent(Graphics g)
    {
        long start = DateTime.Now.Ticks * 100;
        int w = 640;
        int h = 480;
        g.DrawImage(background, 0, 0);
        double theta = 2 * Math.PI * index++ / 64;
        g.FillEllipse(Brushes.Blue,
            (int) (Math.Sin(theta) * w / 3 + w / 2 - Radius),
            (int) (Math.Cos(theta) * h / 3 + h / 2 - Radius),
            2 * Radius, 2 * Radius);
        if (frameCount == Frames)
        {
            averageTime = totalTime / Frames;
            totalTime = 0;
            frameCount = 0;
        }
        else
        {
            totalTime += DateTime.Now.Ticks * 100 - start;
            frameCount++;
        }
        g.DrawString(string.Format("{0,5:0.000}", averageTime / 1000000d), SystemFonts.DefaultFont, Brushes.White, 5, 16);
    }
}'''
    }},
    "T428": {"outputs": {
        "python": '''import subprocess


class ProcessWatcher:
    def __init__(self, pro, out_stream):
        self.pro = pro
        self.out_stream = out_stream

    def run(self):
        try:
            ret_value = self.pro.wait()
            print("Command exit with return value " + str(ret_value))
            self.out_stream.close()
            self.out_stream = None
        except (KeyboardInterrupt, OSError) as e:
            print(e)


def watch(cmd):
    pro = subprocess.Popen(cmd)
    watcher = ProcessWatcher(pro, pro.stdout)
    watcher.run()''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

extern void println(const char *message);

typedef struct {
    int pid;
    FILE *out_stream;
} ProcessWatcher;

void run(ProcessWatcher *watcher) {
    int status;
    if (waitpid(watcher->pid, &status, 0) == -1) {
        perror("waitpid failed");
        return;
    }
    int ret_value = WEXITSTATUS(status);
    char buffer[128];
    snprintf(buffer, sizeof(buffer), "Command exit with return value %d", ret_value);
    println(buffer);
    if (watcher->out_stream != NULL) {
        fclose(watcher->out_stream);
        watcher->out_stream = NULL;
    }
}''',
        "csharp": '''using System;
using System.Diagnostics;
using System.IO;

public class ProcessWatcher
{
    private readonly Process pro;
    private StreamWriter outStream;

    public ProcessWatcher(Process pro, StreamWriter outStream)
    {
        this.pro = pro;
        this.outStream = outStream;
    }

    public void Run()
    {
        try
        {
            pro.WaitForExit();
            int retValue = pro.ExitCode;
            Console.WriteLine("Command exit with return value " + retValue);
            outStream.Close();
            outStream = null;
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
}'''
    }},
    "T626": {"outputs": {
        "python": '''def remove_even(k, n):
    counter = 0
    for i in range(n):
        if k[i] % 2 == 1:
            k[counter] = k[i]
            counter += 1
    for i in range(counter, n):
        k[i] = 0''',
        "c": r'''void remove_even(int *k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 == 1) {
            k[counter++] = k[i];
        }
    }
    for (int i = counter; i < n; i++) {
        k[i] = 0;
    }
}''',
        "csharp": '''public static class ArrayFilter
{
    public static void RemoveEven(int[] k, int n)
    {
        int counter = 0;
        for (int i = 0; i < n; i++)
        {
            if (k[i] % 2 == 1)
            {
                k[counter] = k[i];
                counter++;
            }
        }
        for (int i = counter; i < n; i++)
        {
            k[i] = 0;
        }
    }
}'''
    }},
    "T813": {"outputs": {
        "python": '''def to_hex_string(bytes_):
    return "".join("{:02x}".format(b & 0xFF) for b in bytes_)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>

char *to_hex_string(const unsigned char *bytes, int length) {
    char *hex_string = malloc(length * 2 + 1);
    for (int i = 0; i < length; i++) {
        sprintf(hex_string + i * 2, "%02x", bytes[i] & 0xFF);
    }
    hex_string[length * 2] = '\0';
    return hex_string;
}''',
        "csharp": '''using System.Text;

public static class HexConverter
{
    public static string ToHexString(byte[] bytes)
    {
        var hexString = new StringBuilder(bytes.Length * 2);
        foreach (byte b in bytes)
        {
            hexString.Append(b.ToString("x2"));
        }
        return hexString.ToString();
    }
}'''
    }},
}
