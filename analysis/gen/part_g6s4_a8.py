DATA_A8 = {
"T543": {
"python": r"""
import math

RUN_TIME = 1000

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

class TimerHandle:
    def stop(self):
        pass

class ActionEvent:
    def __init__(self, source):
        self.source = source

frame_width = 400
frame_height = 300
start_time = 0
line_point = None
ball_point = None

def get_width():
    return frame_width

def get_height():
    return frame_height

def on_action(e, now_ms):
    global line_point, ball_point, start_time
    duration = now_ms - start_time
    progress = float(duration) / float(RUN_TIME)
    line_point = Point()
    line_point.x = get_width() // 2
    if progress < 0.5:
        line_point.y = round(get_height() * (progress * 2))
    else:
        if progress > 1.0:
            progress = 1.0
            e.source.stop()
            line_point = None
            ball_point = None
        else:
            line_point.y = round(get_height() * (progress * 2))
            line_point.y = get_height() - (line_point.y - get_height())
            ball_point.y = line_point.y
""",
"c": r"""
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>

#define RUN_TIME 1000.0f

typedef struct { int x, y; } Point;

static Point *line_point = NULL;
static Point *ball_point = NULL;
static long start_time = 0;
static int frame_width = 400;
static int frame_height = 300;
static bool timer_running = true;

void on_action(long now_ms) {
    long duration = now_ms - start_time;
    float progress = (float)duration / RUN_TIME;
    free(line_point);
    line_point = malloc(sizeof(Point));
    line_point->x = frame_width / 2;
    if (progress < 0.5f) {
        line_point->y = (int)lround(frame_height * (progress * 2));
    } else {
        if (progress > 1.0f) {
            progress = 1.0f;
            timer_running = false;
            free(line_point);
            line_point = NULL;
            free(ball_point);
            ball_point = NULL;
        } else {
            line_point->y = (int)lround(frame_height * (progress * 2));
            line_point->y = frame_height - (line_point->y - frame_height);
            ball_point->y = line_point->y;
        }
    }
}
""",
"csharp": r"""
using System;

public class Point
{
    public int X;
    public int Y;
}

public class TimerEvent
{
    public void Stop() { }
}

public class Animator
{
    private const float RUN_TIME = 1000f;
    private long startTime = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
    private Point linePoint;
    private Point ballPoint;

    private int Width { get { return 400; } }
    private int Height { get { return 300; } }

    public void OnAction(TimerEvent e)
    {
        long duration = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond - startTime;
        float progress = (float)duration / RUN_TIME;
        linePoint = new Point();
        linePoint.X = Width / 2;
        if (progress < 0.5f)
        {
            linePoint.Y = (int)Math.Round(Height * (progress * 2));
        }
        else
        {
            if (progress > 1f)
            {
                progress = 1f;
                e.Stop();
                linePoint = null;
                ballPoint = null;
            }
            else
            {
                linePoint.Y = (int)Math.Round(Height * (progress * 2));
                linePoint.Y = Height - (linePoint.Y - Height);
                ballPoint.Y = linePoint.Y;
            }
        }
    }
}
"""
}
}
