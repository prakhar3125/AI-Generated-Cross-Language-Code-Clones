DATA2 = {
"T314": {
 "python": r'''SEPARATOR = " "

def get_name(self, value):
    buffer = []
    if len(value) < self.get_part_divider():
        high = ""
        low = value
    else:
        index = len(value) - self.get_part_divider()
        high = value[:index]
        low = value[index:]
    high_name = self.get_high_processor().get_name(high)
    low_name = self.get_low_processor().get_name(low)
    if high_name != "":
        buffer.append(high_name)
        buffer.append(SEPARATOR)
        buffer.append(self.get_token())
        if low_name != "":
            buffer.append(SEPARATOR)
    if low_name != "":
        buffer.append(low_name)
    return "".join(buffer)''',
 "c": r'''#include <stdio.h>
#include <string.h>

extern int get_part_divider(void);
extern void name_of(const char *value, char *out, size_t n);
extern void get_token(char *out, size_t n);

void get_name(const char *value, char *out, size_t outSize) {
    char high[256], low[256];
    int divider = get_part_divider();
    if (strlen(value) < (size_t) divider) {
        high[0] = '\0';
        snprintf(low, sizeof(low), "%s", value);
    } else {
        int index = (int) strlen(value) - divider;
        strncpy(high, value, index);
        high[index] = '\0';
        snprintf(low, sizeof(low), "%s", value + index);
    }
    char highName[256], lowName[256];
    name_of(high, highName, sizeof(highName));
    name_of(low, lowName, sizeof(lowName));
    out[0] = '\0';
    if (highName[0] != '\0') {
        strcat(out, highName);
        strcat(out, " ");
        char token[64];
        get_token(token, sizeof(token));
        strcat(out, token);
        if (lowName[0] != '\0') {
            strcat(out, " ");
        }
    }
    if (lowName[0] != '\0') {
        strcat(out, lowName);
    }
}''',
 "csharp": r'''public String GetName(String value) {
    var buffer = new StringBuilder();
    String high, low;
    if (value.Length < GetPartDivider()) {
        high = "";
        low = value;
    } else {
        int index = value.Length - GetPartDivider();
        high = value.Substring(0, index);
        low = value.Substring(index);
    }
    String highName = GetHighProcessor().GetName(high);
    String lowName = GetLowProcessor().GetName(low);
    if (!"".Equals(highName)) {
        buffer.Append(highName);
        buffer.Append(SEPARATOR);
        buffer.Append(GetToken());
        if (!"".Equals(lowName)) {
            buffer.Append(SEPARATOR);
        }
    }
    if (!"".Equals(lowName)) {
        buffer.Append(lowName);
    }
    return buffer.ToString();
}'''
},
"T22": {
 "python": r'''condition1 = False
condition2 = False

def main():
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            k = 0
            while k < 9:
                if condition1:
                    print("Breaking from Loop K and J")
                    k = 9
                    j = 9
                if condition2:
                    print("Breaking from Loop K, J and I")
                    k = 9
                    j = 9
                    i = 9
                k += 1
            j += 1
        i += 1
    print("End of I , J , K")''',
 "c": r'''#include <stdio.h>

int condition1 = 0;
int condition2 = 0;

int main(void) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            for (int k = 0; k < 9; k++) {
                if (condition1) {
                    printf("Breaking from Loop K and J\n");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    printf("Breaking from Loop K, J and I\n");
                    k = 9;
                    j = 9;
                    i = 9;
                }
            }
        }
    }
    printf("End of I , J , K\n");
    return 0;
}''',
 "csharp": r'''bool condition1 = false;
bool condition2 = false;

static void Main(string[] args) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            for (int k = 0; k < 9; k++) {
                if (condition1) {
                    Console.WriteLine("Breaking from Loop K and J");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    Console.WriteLine("Breaking from Loop K, J and I");
                    k = 9;
                    j = 9;
                    i = 9;
                }
            }
        }
    }
    Console.WriteLine("End of I , J , K");
}'''
},
"T543": {
 "python": r'''import time

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def action_performed(self, event):
    duration = int(time.time() * 1000) - self.start_time
    progress = float(duration) / float(RUN_TIME)
    self.line_point = Point()
    self.line_point.x = self.get_width() // 2
    if progress < 0.5:
        self.line_point.y = round(self.get_height() * (progress * 2))
    else:
        if progress > 1.0:
            progress = 1.0
            event.get_source().stop()
            self.line_point = None
            self.ball_point = None
        else:
            self.line_point.y = round(self.get_height() * (progress * 2))
            self.line_point.y = self.get_height() - (self.line_point.y - self.get_height())
            self.ball_point.y = self.line_point.y
    self.repaint()''',
 "c": r'''typedef struct { int x, y; } Point;

void action_performed(ActionEvent *e) {
    long duration = now_ms() - start_time;
    float progress = (float) duration / (float) RUN_TIME;
    line_point = malloc(sizeof(Point));
    line_point->x = get_width() / 2;
    if (progress < 0.5f) {
        line_point->y = (int) roundf(get_height() * (progress * 2));
    } else {
        if (progress > 1.0f) {
            progress = 1.0f;
            timer_stop(e->source);
            free(line_point);
            line_point = NULL;
            ball_point = NULL;
        } else {
            line_point->y = (int) roundf(get_height() * (progress * 2));
            line_point->y = get_height() - (line_point->y - get_height());
            ball_point->y = line_point->y;
        }
    }
    repaint();
}''',
 "csharp": r'''public void actionPerformed(ActionEvent e) {
    long duration = System.currentTimeMillis() - startTime;
    float progress = (float) duration / (float) RUN_TIME;
    linePoint = new Point();
    linePoint.x = GetWidth() / 2;
    if (progress < 0.5f) {
        linePoint.y = (int) Math.Round(GetHeight() * (progress * 2));
    } else {
        if (progress > 1f) {
            progress = 1f;
            ((Timer) e.getSource()).stop();
            linePoint = null;
            ballPoint = null;
        } else {
            linePoint.y = (int) Math.Round(GetHeight() * (progress * 2));
            linePoint.y = GetHeight() - (linePoint.y - GetHeight());
            ballPoint.y = linePoint.y;
        }
    }
    repaint();
}'''
},
"T653": {
 "python": r'''from tkinter import simpledialog

def action_performed(self, event):
    scale_width = simpledialog.askstring("", "What should the new width be?")
    scale_height = simpledialog.askstring("", "What should the new height be?")
    x = float(scale_width)
    y = float(scale_height)
    new_width = int(x)
    new_height = int(y)
    self.frame.setSize(new_width, new_height)
    self.scale(new_width, new_height)''',
 "c": r'''extern char *show_input_dialog(const char *message);
extern void frame_set_size(Frame *frame, int width, int height);
extern void scale(int width, int height);

void action_performed(ActionEvent *e) {
    char *scaleWidth = show_input_dialog("What should the new width be?");
    char *scaleHeight = show_input_dialog("What should the new height be?");
    double x = atof(scaleWidth);
    double y = atof(scaleHeight);
    int newWidth = (int) x;
    int newHeight = (int) y;
    frame_set_size(&frame, newWidth, newHeight);
    scale(newWidth, newHeight);
}''',
 "csharp": r'''static class Prompt {
    public static string ShowDialog(string message) {
        Console.Write(message + " ");
        return Console.ReadLine();
    }
}

public void actionPerformed(ActionEvent e) {
    string scaleWidth = Prompt.ShowDialog("What should the new width be?");
    string scaleHeight = Prompt.ShowDialog("What should the new height be?");
    double x = double.Parse(scaleWidth);
    double y = double.Parse(scaleHeight);
    int newWidth = (int) x;
    int newHeight = (int) y;
    frame.SetSize(newWidth, newHeight);
    Scale(newWidth, newHeight);
}'''
},
"T229": {
 "python": r'''import threading

token = 0
N = 3
condition = threading.Condition()

def run(self):
    with condition:
        for i in range(5):
            while self.id != token % N:
                condition.wait()
            print(self.id, i)
            token += 1
            condition.notify_all()''',
 "c": r'''#include <pthread.h>
#include <stdio.h>

extern int id;
extern int token;
extern int N;
extern pthread_mutex_t lock;
extern pthread_cond_t cond;

void *run(void *arg) {
    pthread_mutex_lock(&lock);
    for (int i = 0; i < 5; i++) {
        while (id != token % N) {
            pthread_cond_wait(&cond, &lock);
        }
        printf("%d %d\n", id, i);
        token++;
        pthread_cond_broadcast(&cond);
    }
    pthread_mutex_unlock(&lock);
    return NULL;
}''',
 "csharp": r'''static readonly object lockObj = new object();
static int token = 0;
static int N = 3;
int id = 0;

public void Run() {
    lock (lockObj) {
        for (int i = 0; i < 5; i++) {
            while (id != token % N) {
                Monitor.Wait(lockObj);
            }
            Console.WriteLine(id + " " + i);
            token++;
            Monitor.PulseAll(lockObj);
        }
    }
}'''
},
"T147": {
 "python": r'''def solution(x, a):
    empty_positions = set(range(1, x + 1))
    for i in range(len(a)):
        empty_positions.discard(a[i])
        if not empty_positions:
            return i
    return -1''',
 "c": r'''int solution(int X, const int *A, int n) {
    int *inSet = malloc((X + 1) * sizeof(int));
    for (int v = 0; v <= X; v++) {
        inSet[v] = (v >= 1) ? 1 : 0;
    }
    int remaining = X;
    for (int i = 0; i < n; i++) {
        if (A[i] >= 0 && A[i] <= X && inSet[A[i]]) {
            inSet[A[i]] = 0;
            remaining--;
        }
        if (remaining == 0) {
            free(inSet);
            return i;
        }
    }
    free(inSet);
    return -1;
}''',
 "csharp": r'''public static int Solution(int x, int[] a) {
    var emptyPosition = new HashSet<int>(Enumerable.Range(1, x));
    for (int i = 0; i < a.Length; i++) {
        emptyPosition.Remove(a[i]);
        if (emptyPosition.Count == 0) return i;
    }
    return -1;
}'''
},
}
