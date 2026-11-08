# -*- coding: utf-8 -*-
DATA5 = {
"T694": {
"python": r'''
from itertools import product

class Foo:
    def __init__(self, data):
        self.data = data

    def allUniqueCombinations(self):
        keys = list(self.data.keys())
        combos = [()]
        for key in keys:
            combos = [c + (v,) for c in combos for v in self.data[key]]
        return combos

def main():
    data = {
        "foo": ["1", "2", "3"],
        "bar": ["3", "2"],
        "baz": ["5", "6", "7"],
    }
    foo = Foo(data)
    for combination in foo.allUniqueCombinations():
        print(list(combination))
''',
"c": r'''
#include <stdio.h>

static const char *data[3][3] = {
    {"1", "2", "3"},
    {"3", "2"},
    {"5", "6", "7"}
};
static const int sizes[3] = {3, 2, 3};

int main(void) {
    for (int i = 0; i < sizes[0]; i++) {
        for (int j = 0; j < sizes[1]; j++) {
            for (int k = 0; k < sizes[2]; k++) {
                printf("[%s, %s, %s]\n", data[0][i], data[1][j], data[2][k]);
            }
        }
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

class Foo {
    private Dictionary<string, List<string>> data;

    public Foo(Dictionary<string, List<string>> data) {
        this.data = data;
    }

    public IEnumerable<string[]> AllUniqueCombinations() {
        IEnumerable<IEnumerable<string>> combos = new List<IEnumerable<string>> { new List<string>() };
        foreach (var values in data.Values) {
            combos = combos.SelectMany(c => values, (c, v) => c.Concat(new[] { v }));
        }
        return combos.Select(c => c.ToArray());
    }
}

public class Program {
    public static void Main() {
        var data = new Dictionary<string, List<string>> {
            ["foo"] = new List<string> { "1", "2", "3" },
            ["bar"] = new List<string> { "3", "2" },
            ["baz"] = new List<string> { "5", "6", "7" }
        };
        Foo foo = new Foo(data);
        foreach (string[] combination in foo.AllUniqueCombinations()) {
            Console.WriteLine("[" + string.Join(", ", combination) + "]");
        }
    }
}
'''
},
"T546": {
"python": r'''
def join(objects, delimiter):
    if len(objects) == 0:
        return ""
    return delimiter.join(str(obj) for obj in objects)
''',
"c": r'''
#include <stdio.h>

void join(char **objects, int count, const char *delimiter, char *out) {
    out[0] = '\0';
    if (count == 0) {
        return;
    }
    int pos = 0;
    for (int i = 0; i < count; i++) {
        if (i > 0) {
            pos += sprintf(out + pos, "%s", delimiter);
        }
        pos += sprintf(out + pos, "%s", objects[i]);
    }
}
''',
"csharp": r'''
using System.Text;

public static string Join(object[] objects, string delimiter) {
    if (objects.Length == 0) {
        return "";
    }
    StringBuilder ret = new StringBuilder();
    ret.Append(objects[0]);
    for (int i = 1; i < objects.Length; i++) {
        ret.Append(delimiter);
        ret.Append(objects[i]);
    }
    return ret.ToString();
}
'''
},
"T664": {
"python": r'''
class Type:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name


class TypeVariable(Type):
    def __init__(self, name):
        super().__init__(name)


class ParameterizedType(Type):
    def __init__(self, name, typeArgs):
        super().__init__(name)
        self.typeArgs = typeArgs

    def getRawType(self):
        return Type(self.name)

    def getActualTypeArguments(self):
        return self.typeArgs


def investigate(p, *typeArgs):
    c = p.getRawType()
    b = [c.getName(), "<"]
    localArgs = list(p.getActualTypeArguments())
    if typeArgs is not None and len(typeArgs) > 0:
        nextTypeArg = 0
        for local in localArgs:
            if isinstance(local, ParameterizedType):
                b.append(str(local.getRawType()))
                b.append("<")
                b.append(typeArgs[nextTypeArg])
                nextTypeArg += 1
                b.append(">")
            elif isinstance(local, TypeVariable):
                localArgs[nextTypeArg] = typeArgs[nextTypeArg]
                b.append(str(localArgs[nextTypeArg]))
                nextTypeArg += 1
            else:
                b.append(str(local))
            b.append(", ")
        if len(typeArgs) > 0:
            b.pop()
            b.pop()
        b.append(">")
    else:
        b.append(", ".join(str(arg) for arg in localArgs))
        b.append(">")
    print("".join(b))
    investigate(c, *localArgs)
''',
"c": r'''
#include <stdio.h>
#include <string.h>

#define MAX_TYPES 32
#define MAX_NAME 128

typedef struct Type {
    char name[MAX_NAME];
    struct Type *typeArgs[MAX_TYPES];
    int typeArgCount;
    int isParameterized;
    int isTypeVariable;
} Type;

extern void investigateType(Type *c, Type **typeArgs, int typeArgCount);

void build_type_string(Type *p, char *b, Type **typeArgs, int typeArgCount) {
    strcat(b, "<");
    Type **localArgs = p->typeArgs;
    int localCount = p->typeArgCount;
    if (typeArgs != NULL && typeArgCount > 0) {
        int nextTypeArg = 0;
        for (int i = 0; i < localCount; i++) {
            Type *local = localArgs[i];
            if (local->isParameterized) {
                strcat(b, local->name);
                strcat(b, "<");
                char argName[MAX_NAME];
                strcpy(argName, typeArgs[nextTypeArg]->name);
                nextTypeArg++;
                strcat(b, argName);
                strcat(b, ">");
            } else if (local->isTypeVariable) {
                localArgs[nextTypeArg] = typeArgs[nextTypeArg];
                strcat(b, localArgs[nextTypeArg]->name);
                nextTypeArg++;
            } else {
                strcat(b, local->name);
            }
            strcat(b, ", ");
        }
        if (typeArgCount > 0) {
            int bLen = strlen(b);
            b[bLen - 2] = '\0';
        }
        strcat(b, ">");
    } else {
        for (int i = 0; i < localCount; i++) {
            if (i > 0) strcat(b, ", ");
            strcat(b, localArgs[i]->name);
        }
        strcat(b, ">");
    }
}

void investigate(ParameterizedType, Type **typeArgs, int typeArgCount) {
    Type *p = (ParameterizedType);
    char b[1024];
    strcpy(b, p->name);
    build_type_string(p, b, typeArgs, typeArgCount);
    printf("%s\n", b);
    investigateType(p, p->typeArgs, p->typeArgCount);
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public class Type {
    public string Name { get; set; }
    public override string ToString() { return Name; }
}

public class TypeVariable : Type { }

public class ParameterizedType : Type {
    public Type[] TypeArgs { get; set; }

    public Type GetRawType() {
        return new Type { Name = Name };
    }

    public Type[] GetActualTypeArguments() {
        return TypeArgs;
    }
}

public class TypePrinter {
    public static void Investigate(ParameterizedType p, params Type[] typeArgs) {
        Type c = p.GetRawType();
        StringBuilder b = new StringBuilder(c.Name);
        b.Append('<');
        Type[] localArgs = p.GetActualTypeArguments();
        if (typeArgs != null && typeArgs.Length > 0) {
            int nextTypeArg = 0;
            foreach (Type local in localArgs) {
                if (local is ParameterizedType localP) {
                    b.Append(localP.GetRawType()).Append('<');
                    b.Append(typeArgs[nextTypeArg++]);
                    b.Append('>');
                } else if (local is TypeVariable) {
                    localArgs[nextTypeArg] = typeArgs[nextTypeArg];
                    b.Append(localArgs[nextTypeArg]);
                    nextTypeArg++;
                } else {
                    b.Append(local.ToString());
                }
                b.Append(", ");
            }
            if (typeArgs.Length > 0) {
                b.Remove(b.Length - 2, 2);
            }
            b.Append('>');
        } else {
            b.Append(string.Join(", ", localArgs.Select(arg => arg.ToString())));
            b.Append('>');
        }
        Console.WriteLine(b);
        Investigate((ParameterizedType) c, localArgs);
    }
}
'''
},
"T706": {
"python": r'''
import random

def shuffle(text):
    characters = list(text)
    for i in range(len(characters)):
        randomIndex = random.randrange(len(characters))
        characters[i], characters[randomIndex] = characters[randomIndex], characters[i]
    return "".join(characters)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

char *shuffle(char *text) {
    size_t len = strlen(text);
    for (size_t i = 0; i < len; i++) {
        size_t randomIndex = rand() % len;
        char temp = text[i];
        text[i] = text[randomIndex];
        text[randomIndex] = temp;
    }
    return text;
}
''',
"csharp": r'''
using System;

public static string Shuffle(string text) {
    char[] characters = text.ToCharArray();
    Random randomIndex = new Random();
    for (int i = 0; i < characters.Length; i++) {
        int j = randomIndex.Next(characters.Length);
        (characters[i], characters[j]) = (characters[j], characters[i]);
    }
    return new string(characters);
}
'''
},
"T567": {
"python": r'''
import threading

class SharedState:
    def __init__(self):
        self.state = 0
        self.cond = threading.Condition()

    def getState(self):
        return self.state

    def setState(self, value):
        self.state = value


def run(s):
    i = 3
    while i < 50:
        with s.cond:
            while s.getState() != 2:
                s.cond.wait()
            if s.getState() == 2:
                print("t3 " + str(i))
            i += 3
            s.setState(3)
            s.cond.notify_all()
''',
"c": r'''
#include <pthread.h>
#include <stdio.h>

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int state;
} SharedState;

void *run(void *arg) {
    SharedState *s = (SharedState *) arg;
    int i = 3;
    while (i < 50) {
        pthread_mutex_lock(&s->mutex);
        while (s->state != 2) {
            pthread_cond_wait(&s->cond, &s->mutex);
        }
        if (s->state == 2) {
            printf("t3 %d\n", i);
        }
        i = i + 3;
        s->state = 3;
        pthread_cond_broadcast(&s->cond);
        pthread_mutex_unlock(&s->mutex);
    }
    return NULL;
}
''',
"csharp": r'''
using System;
using System.Threading;

public class SharedState {
    public object Lock { get; } = new object();
    public int State { get; set; }
}

public class Worker {
    public void Run(SharedState s) {
        int i = 3;
        while (i < 50) {
            lock (s.Lock) {
                while (s.State != 2) {
                    Monitor.Wait(s.Lock);
                }
                if (s.State == 2) {
                    Console.WriteLine("t3 " + i);
                }
                i = i + 3;
                s.State = 3;
                Monitor.PulseAll(s.Lock);
            }
        }
    }
}
'''
},
"T731": {
"python": r'''
import math
import time


class Graphics:
    def drawImage(self, image, x, y):
        pass

    def setColor(self, color):
        pass

    def fillOval(self, x, y, width, height):
        pass

    def drawString(self, text, x, y):
        pass


def paintComponent(self, g):
    start = time.perf_counter_ns()
    self.super_paintComponent(g)
    w = self.getWidth()
    h = self.getHeight()
    g.drawImage(self.background, 0, 0)
    self.index += 1
    theta = 2 * math.pi * self.index / 64
    g.setColor(self.COLOR)
    rectX = int(math.sin(theta) * w / 3 + w / 2 - self.RADIUS)
    rectY = int(math.cos(theta) * h / 3 + h / 2 - self.RADIUS)
    g.fillOval(rectX, rectY, 2 * self.RADIUS, 2 * self.RADIUS)
    g.setColor(Color.WHITE)
    if self.frameCount == self.FRAMES:
        self.averageTime = self.totalTime / self.FRAMES
        self.totalTime = 0
        self.frameCount = 0
    else:
        self.totalTime += time.perf_counter_ns() - start
        self.frameCount += 1
    g.drawString("%8.3f" % (self.averageTime / 1000000), 5, 16)
''',
"c": r'''
#include <math.h>
#include <stdio.h>
#include <time.h>

#define RADIUS 10
#define FRAMES 64

typedef struct {
    int x, y, width, height;
} Rectangle;

typedef struct {
    int index;
    int frameCount;
    long totalTime;
    double averageTime;
    Rectangle rect;
} PanelState;

extern void drawImage(void *g, void *background, int x, int y);
extern void superPaintComponent(void *g);
extern void setColor(void *g, int r, int gr, int b);
extern void fillOval(void *g, int x, int y, int w, int h);
extern void drawString(void *g, const char *text, int x, int y);
extern int getWidth(void);
extern int getHeight(void);
extern void *background;

static long now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000000000L + ts.tv_nsec;
}

void paintComponent(void *g, PanelState *state) {
    long start = now_ns();
    superPaintComponent(g);
    int w = getWidth();
    int h = getHeight();
    drawImage(g, background, 0, 0);
    double theta = 2 * M_PI * state->index++ / 64;
    setColor(g, 0, 0, 255);
    state->rect.x = (int) (sin(theta) * w / 3 + w / 2 - RADIUS);
    state->rect.y = (int) (cos(theta) * h / 3 + h / 2 - RADIUS);
    state->rect.width = 2 * RADIUS;
    state->rect.height = 2 * RADIUS;
    fillOval(g, state->rect.x, state->rect.y, state->rect.width, state->rect.height);
    setColor(g, 255, 255, 255);
    if (state->frameCount == FRAMES) {
        state->averageTime = state->totalTime / FRAMES;
        state->totalTime = 0;
        state->frameCount = 0;
    } else {
        state->totalTime += now_ns() - start;
        state->frameCount++;
    }
    char text[32];
    snprintf(text, sizeof(text), "%8.3f", state->averageTime / 1000000.0);
    drawString(g, text, 5, 16);
}
''',
"csharp": r'''
using System;

public void PaintComponent(Graphics g) {
    long start = System.Diagnostics.Stopwatch.GetTimestamp();
    super.PaintComponent(g);
    int w = this.GetWidth();
    int h = this.GetHeight();
    g.DrawImage(background, 0, 0);
    index++;
    double theta = 2 * Math.PI * index / 64;
    g.SetColor(Color.Blue);
    rect.SetRect((int) (Math.Sin(theta) * w / 3 + w / 2 - RADIUS),
                 (int) (Math.Cos(theta) * h / 3 + h / 2 - RADIUS),
                 2 * RADIUS, 2 * RADIUS);
    g.FillOval(rect.X, rect.Y, rect.Width, rect.Height);
    g.SetColor(Color.White);
    if (frameCount == FRAMES) {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    } else {
        totalTime += System.Diagnostics.Stopwatch.GetTimestamp() - start;
        frameCount++;
    }
    g.DrawString(string.Format("{0,8:0.000}", averageTime / 1000000d), 5, 16);
}
'''
},
"T428": {
"python": r'''
def run(self):
    try:
        retValue = self.pro.wait()
        self.println("Command exit with return value " + str(retValue))
        self.outStream.close()
        self.outStream = None
    except Exception as e:
        print(e)
''',
"c": r'''
#include <stdio.h>

typedef struct {
    int pid;
    FILE *outStream;
} ProcessRunner;

extern int wait_for_process(const ProcessRunner *runner);

void run(ProcessRunner *runner) {
    int retValue = wait_for_process(runner);
    if (retValue < 0) {
        perror("wait failed");
        return;
    }
    printf("Command exit with return value %d\n", retValue);
    if (runner->outStream != NULL) {
        fclose(runner->outStream);
        runner->outStream = NULL;
    }
}
''',
"csharp": r'''
using System;
using System.Diagnostics;
using System.IO;

public void Run() {
    try {
        pro.WaitForExit();
        int retValue = pro.ExitCode;
        Console.WriteLine("Command exit with return value " + retValue);
        outStream.Close();
        outStream = null;
    } catch (Exception e) {
        Console.Error.WriteLine(e.StackTrace);
    }
}
'''
}
}
