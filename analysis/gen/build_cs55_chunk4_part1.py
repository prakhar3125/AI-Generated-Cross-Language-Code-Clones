TRANSLATIONS_A = {
    "T297": {
        "python": r'''class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

    def __str__(self):
        values = []
        node = self
        while node is not None:
            values.append(str(node.value))
            node = node.next
        return " ".join(values)

    def switch_pairs(self):
        if self is None or self.next is None:
            return self
        top = self.next
        first = self
        second = first.next
        while True:
            third = second.next
            second.next = first
            first.next = third
            first = third
            print("@@@ " + str(self))
            if first is not None:
                second.next.next = first.next
                second = first.next
            if first is None or second is None:
                break
        return top''',
        "c": r'''#include <stdio.h>
#include <string.h>

typedef struct ListNode {
    int value;
    struct ListNode *next;
} ListNode;

char *list_node_to_string(ListNode *node, char *buf, size_t size) {
    buf[0] = '\0';
    while (node != NULL) {
        char tmp[32];
        snprintf(tmp, sizeof(tmp), "%d ", node->value);
        strncat(buf, tmp, size - strlen(buf) - 1);
        node = node->next;
    }
    return buf;
}

ListNode *switch_pairs(ListNode *head) {
    if (head == NULL || head->next == NULL) return head;
    ListNode *top = head->next;
    ListNode *first = head;
    ListNode *second = first->next;
    char buf[256];
    do {
        ListNode *third = second->next;
        second->next = first;
        first->next = third;
        first = third;
        printf("@@@ %s\n", list_node_to_string(head, buf, sizeof(buf)));
        if (first != NULL) {
            second->next->next = first->next;
            second = first->next;
        }
    } while (first != NULL && second != NULL);
    return top;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;

public class ListNode
{
    public int Value;
    public ListNode Next;

    public override string ToString()
    {
        var parts = new List<string>();
        for (ListNode n = this; n != null; n = n.Next) parts.Add(n.Value.ToString());
        return string.Join(" ", parts);
    }

    public ListNode SwitchPairs()
    {
        if (this == null || this.Next == null) return this;
        ListNode top = this.Next;
        ListNode first = this;
        ListNode second = first.Next;
        do
        {
            ListNode third = second.Next;
            second.Next = first;
            first.Next = third;
            first = third;
            Console.WriteLine("@@@ " + this.ToString());
            if (first != null)
            {
                second.Next.Next = first.Next;
                second = first.Next;
            }
        } while (first != null && second != null);
        return top;
    }
}'''
    },
    "T252": {
        "python": r'''import pickle
import traceback


class DefaultTableModel:
    def __init__(self):
        self.rows = []


class Table:
    def __init__(self):
        self.model = None

    def set_model(self, model):
        self.model = model


class ActionEvent:
    pass


class Component:
    def __init__(self, file=None):
        self.file = file
        self.table = Table()
        self.model = None

    def action_performed(self, event):
        try:
            stream = open(self.file, "rb")
            try:
                self.model = pickle.load(stream)
            finally:
                stream.close()
            self.table.set_model(self.model)
        except OSError as ex:
            traceback.print_exc()''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int rowCount;
    int colCount;
    double **data;
} TableModel;

typedef struct {
    TableModel *model;
} Table;

void table_set_model(Table *table, TableModel *model) {
    table->model = model;
}

typedef struct {
    const char *file;
    Table *table;
    TableModel *model;
} ActionState;

void action_performed(ActionState *state) {
    FILE *is = fopen(state->file, "rb");
    if (is == NULL) {
        perror("actionPerformed");
        return;
    }
    TableModel *model = (TableModel *) malloc(sizeof(TableModel));
    if (model == NULL || fread(model, sizeof(TableModel), 1, is) != 1) {
        perror("actionPerformed");
        free(model);
        fclose(is);
        return;
    }
    state->model = model;
    table_set_model(state->table, model);
    fclose(is);
}''',
        "csharp": r'''using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

public class ActionEvent {}

public class TableModel {}

public class Table
{
    public TableModel model;

    public void setModel(TableModel m) { model = m; }
}

public class Component
{
    public string file;
    public Table table = new Table();
    public TableModel model;

    public void actionPerformed(ActionEvent e)
    {
        try
        {
            using (Stream stream = new BufferedStream(new FileStream(file, FileMode.Open, FileAccess.Read)))
            {
                BinaryFormatter decoder = new BinaryFormatter();
                model = (TableModel) decoder.Deserialize(stream);
            }
            table.setModel(model);
        }
        catch (IOException ex)
        {
            Console.Error.WriteLine(ex.StackTrace);
        }
    }
}'''
    },
    "T10": {
        "python": r'''class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


def reverse(n, p):
    if n is None:
        return None
    if n.next is None:
        n.next = p
        return n
    r = reverse(n.next, n)
    n.next = p
    return r''',
        "c": r'''typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node *reverse(Node *n, Node *p) {
    if (n == NULL) return NULL;
    if (n->next == NULL) {
        n->next = p;
        return n;
    }
    Node *r = reverse(n->next, n);
    n->next = p;
    return r;
}''',
        "csharp": r'''public class Node
{
    public int Value;
    public Node Next;
}

public class ListReverser
{
    public static Node Reverse(Node n, Node p)
    {
        if (n == null) return null;
        if (n.Next == null)
        {
            n.Next = p;
            return n;
        }
        Node r = Reverse(n.Next, n);
        n.Next = p;
        return r;
    }
}'''
    },
    "T146": {
        "python": r'''def solution(X, A):
    seen = set()
    for i in range(len(A)):
        if A[i] <= X:
            seen.add(A[i])
        if len(seen) == X:
            return i
    return -1''',
        "c": r'''#include <string.h>

#define OFFSET 100000

int solution(int X, const int *A, int n) {
    static char seen[2 * OFFSET + 1];
    memset(seen, 0, sizeof(seen));
    int distinct = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] <= X && !seen[A[i] + OFFSET]) {
            seen[A[i] + OFFSET] = 1;
            distinct++;
        }
        if (distinct == X) return i;
    }
    return -1;
}''',
        "csharp": r'''using System.Collections.Generic;

public class Solution
{
    public int solution(int X, int[] A)
    {
        HashSet<int> hset = new HashSet<int>();
        for (int i = 0; i < A.Length; i++)
        {
            if (A[i] <= X) hset.Add(A[i]);
            if (hset.Count == X) return i;
        }
        return -1;
    }
}'''
    },
    "T110": {
        "python": r'''def main():
    throw_catch_time = 0
    new_exception_time = 0
    new_object_time = 0
    no_stack_exception_time = 0
    for _ in range(30):
        throw_catch_time += throw_catch_loop()
        new_exception_time += new_exception_loop()
        new_object_time += new_object_loop()
        no_stack_exception_time += new_no_stack_exception_loop()
    print("throwCatchTime = " + str(throw_catch_time // 30))
    print("newExceptionTime = " + str(new_exception_time // 30))
    print("newStringTime = " + str(new_object_time // 30))
    print("noStackExceptionTime = " + str(no_stack_exception_time // 30))''',
        "c": r'''#include <stdio.h>

extern long throwCatchLoop(void);
extern long newExceptionLoop(void);
extern long newObjectLoop(void);
extern long newNoStackExceptionLoop(void);

int main(void) {
    long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++) {
        throwCatchTime += throwCatchLoop();
        newExceptionTime += newExceptionLoop();
        newObjectTime += newObjectLoop();
        noStackExceptionTime += newNoStackExceptionLoop();
    }
    printf("throwCatchTime = %ld\n", throwCatchTime / 30);
    printf("newExceptionTime = %ld\n", newExceptionTime / 30);
    printf("newStringTime = %ld\n", newObjectTime / 30);
    printf("noStackExceptionTime = %ld\n", noStackExceptionTime / 30);
    return 0;
}''',
        "csharp": r'''using System;

public static class TimingMain
{
    private static long ThrowCatchLoop() { return 0L; }
    private static long NewExceptionLoop() { return 0L; }
    private static long NewObjectLoop() { return 0L; }
    private static long NewNoStackExceptionLoop() { return 0L; }

    public static void Main(string[] args)
    {
        long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
        for (int i = 0; i < 30; i++)
        {
            throwCatchTime += ThrowCatchLoop();
            newExceptionTime += NewExceptionLoop();
            newObjectTime += NewObjectLoop();
            noStackExceptionTime += NewNoStackExceptionLoop();
        }
        Console.WriteLine("throwCatchTime = " + throwCatchTime / 30);
        Console.WriteLine("newExceptionTime = " + newExceptionTime / 30);
        Console.WriteLine("newStringTime = " + newObjectTime / 30);
        Console.WriteLine("noStackExceptionTime = " + noStackExceptionTime / 30);
    }
}'''
    },
    "T34": {
        "python": r'''import traceback

IMAGE_CAPTURE = 1


class Intent:
    def __init__(self, path=None):
        self.path = path


class SQLiteDatabase:
    def exec_sql(self, statement):
        pass

    def close(self):
        pass


class DBHelper:
    def __init__(self, context):
        pass

    def get_writable_database(self):
        return SQLiteDatabase()

    def close(self):
        pass


class Activity:
    RESULT_OK = -1


class Component:
    def on_activity_result(self, request_code, result_code, data):
        if request_code == IMAGE_CAPTURE and result_code == Activity.RESULT_OK:
            db_helper = DBHelper(self)
            sql = db_helper.get_writable_database()
            sql.exec_sql("insert statement for inserting path to database")
            sql.close()
            db_helper.close()''',
        "c": r'''#define IMAGE_CAPTURE 1
#define RESULT_OK 0

typedef struct {
    int dummy;
} SQLiteDatabase;

typedef struct {
    int dummy;
} DBHelper;

extern DBHelper *db_helper_create(void *context);
extern void db_helper_close(DBHelper *db);
extern SQLiteDatabase *db_helper_get_writable_database(DBHelper *db);
extern void sql_exec_sql(SQLiteDatabase *sql, const char *statement);
extern void sql_close(SQLiteDatabase *sql);

void on_activity_result(int requestCode, int resultCode, void *data) {
    if (requestCode == IMAGE_CAPTURE && resultCode == RESULT_OK) {
        DBHelper *dbHelper = db_helper_create(NULL);
        SQLiteDatabase *sql = db_helper_get_writable_database(dbHelper);
        sql_exec_sql(sql, "insert statement for inserting path to database");
        sql_close(sql);
        db_helper_close(dbHelper);
    }
}''',
        "csharp": r'''public class Intent {}

public class Activity
{
    public const int RESULT_OK = -1;
}

public class SQLiteDatabase
{
    public void ExecSQL(string statement) {}
    public void Close() {}
}

public class DBHelper
{
    public DBHelper(object context) {}
    public SQLiteDatabase WritableDatabase { get { return new SQLiteDatabase(); } }
    public void Close() {}
}

public class Screen
{
    private const int IMAGE_CAPTURE = 1;

    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        if (requestCode == IMAGE_CAPTURE && resultCode == Activity.RESULT_OK)
        {
            DBHelper dbHelper = new DBHelper(this);
            SQLiteDatabase sql = dbHelper.WritableDatabase;
            sql.ExecSQL("insert statement for inserting path to database");
            sql.Close();
            dbHelper.Close();
        }
    }
}'''
    },
    "T314": {
        "python": r'''SEPARATOR = " "


class WordProcessor:
    def get_name(self, value):
        return value


class NameSplitter:
    def __init__(self):
        self.part_divider = 3
        self.high_processor = WordProcessor()
        self.low_processor = WordProcessor()

    def get_part_divider(self):
        return self.part_divider

    def get_high_processor(self):
        return self.high_processor

    def get_low_processor(self):
        return self.low_processor

    def get_token(self):
        return "hundred"

    def get_name(self, value):
        buffer_parts = []
        if len(value) < self.get_part_divider():
            high, low = "", value
        else:
            index = len(value) - self.get_part_divider()
            high, low = value[:index], value[index:]
        high_name = self.get_high_processor().get_name(high)
        low_name = self.get_low_processor().get_name(low)
        if high_name != "":
            buffer_parts.append(high_name)
            buffer_parts.append(SEPARATOR)
            buffer_parts.append(self.get_token())
            if low_name != "":
                buffer_parts.append(SEPARATOR)
        if low_name != "":
            buffer_parts.append(low_name)
        return "".join(buffer_parts)''',
        "c": r'''#include <stdio.h>
#include <string.h>

#define SEPARATOR " "
#define PART_DIVIDER 3

extern void processor_get_name(const char *value, char *out, size_t outSize);
extern const char *get_token(void);

void get_name(const char *value, char *buffer, size_t bufferSize) {
    char high[128], low[128], name[128];
    size_t len = strlen(value);
    buffer[0] = '\0';
    if (len < PART_DIVIDER) {
        high[0] = '\0';
        strcpy(low, value);
    } else {
        int index = (int) len - PART_DIVIDER;
        strncpy(high, value, index);
        high[index] = '\0';
        strcpy(low, value + index);
    }
    processor_get_name(high, name, sizeof(name));
    if (name[0] != '\0') {
        strcat(buffer, name);
        strcat(buffer, SEPARATOR);
        strcat(buffer, get_token());
        if (low[0] != '\0') {
            strcat(buffer, SEPARATOR);
        }
    }
    processor_get_name(low, name, sizeof(name));
    if (low[0] != '\0') {
        strcat(buffer, name);
    }
}''',
        "csharp": r'''using System.Text;

public class HighProcessor
{
    public string getName(string v) { return v; }
}

public class LowProcessor
{
    public string getName(string v) { return v; }
}

public class NameSplitter
{
    private const string SEPARATOR = " ";

    public int getPartDivider() { return 3; }
    public HighProcessor getHighProcessor() { return new HighProcessor(); }
    public LowProcessor getLowProcessor() { return new LowProcessor(); }
    public string getToken() { return "hundred"; }

    public string getName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        string high, low;
        if (value.Length < getPartDivider())
        {
            high = "";
            low = value;
        }
        else
        {
            int index = value.Length - getPartDivider();
            high = value.Substring(0, index);
            low = value.Substring(index);
        }
        string highName = getHighProcessor().getName(high);
        string lowName = getLowProcessor().getName(low);
        if (highName != "")
        {
            buffer.Append(highName);
            buffer.Append(SEPARATOR);
            buffer.Append(getToken());
            if (lowName != "")
            {
                buffer.Append(SEPARATOR);
            }
        }
        if (lowName != "")
        {
            buffer.Append(lowName);
        }
        return buffer.ToString();
    }
}'''
    },
    "T22": {
        "python": r'''def main():
    i = 0
    while i < 9:
        j = 0
        broke_all = False
        while j < 9 and not broke_all:
            k = 0
            while k < 9 and not broke_all:
                if condition1:
                    print("Breaking from Loop K and J")
                    k, j = 9, 9
                if condition2:
                    print("Breaking from Loop K, J and I")
                    k, j, i = 9, 9, 9
                    broke_all = True
                k += 1
            j += 1
        if not broke_all:
            i += 1
    print("End of I , J , K")''',
        "c": r'''#include <stdio.h>

extern int condition1;
extern int condition2;

int main(void) {
    for (int i = 0; i < 9; i++) {
        int stop = 0;
        for (int j = 0; j < 9 && !stop; j++) {
            for (int k = 0; k < 9 && !stop; k++) {
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
                    stop = 1;
                }
            }
        }
        if (stop) break;
    }
    printf("End of I , J , K\n");
    return 0;
}''',
        "csharp": r'''using System;

public static class BreakLoops
{
    public static bool condition1;
    public static bool condition2;

    public static void Main(string[] args)
    {
        int i = 0;
        while (i < 9)
        {
            bool stopAll = false;
            int j = 0;
            while (j < 9 && !stopAll)
            {
                int k = 0;
                while (k < 9 && !stopAll)
                {
                    if (condition1)
                    {
                        Console.WriteLine("Breaking from Loop K and J");
                        k = 9;
                        j = 9;
                    }
                    if (condition2)
                    {
                        Console.WriteLine("Breaking from Loop K, J and I");
                        k = 9;
                        j = 9;
                        i = 9;
                        stopAll = true;
                    }
                    k++;
                }
                j++;
            }
            if (!stopAll)
            {
                i++;
            }
        }
        Console.WriteLine("End of I , J , K");
    }
}'''
    },
    "T543": {
        "python": r'''import time

RUN_TIME = 1000.0


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0


class Timer:
    def stop(self):
        pass


class ActionEvent:
    def __init__(self, source):
        self.source = source

    def get_source(self):
        return self.source


class AnimatedPanel:
    def __init__(self):
        self.startTime = 0
        self.linePoint = None
        self.ballPoint = None
        self.width = 400
        self.height = 300

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def repaint(self):
        pass

    def action_performed(self, e):
        duration = time.time() * 1000 - self.startTime
        progress = float(duration) / RUN_TIME
        self.linePoint = Point()
        self.linePoint.x = self.get_width() // 2
        if progress < 0.5:
            self.linePoint.y = round(self.get_height() * (progress * 2))
        else:
            if progress > 1.0:
                progress = 1.0
                e.get_source().stop()
                self.linePoint = None
                self.ballPoint = None
            else:
                self.linePoint.y = round(self.get_height() * (progress * 2))
                self.linePoint.y = self.get_height() - (self.linePoint.y - self.get_height())
                self.ballPoint.y = self.linePoint.y
        self.repaint()''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define RUN_TIME 1000.0f

typedef struct { int x, y; } Point;

extern long long start_time_value;
extern long long now_millis(void);
extern void timer_stop(void);
extern int get_width(void);
extern int get_height(void);
extern void repaint(void);

Point *linePoint = NULL;
Point *ballPoint = NULL;

void action_performed(void) {
    long long duration = now_millis() - start_time_value;
    float progress = (float) duration / RUN_TIME;
    free(linePoint);
    linePoint = (Point *) malloc(sizeof(Point));
    linePoint->x = get_width() / 2;
    if (progress < 0.5f) {
        linePoint->y = (int) llround(get_height() * (progress * 2));
    } else if (progress > 1.0f) {
        progress = 1.0f;
        timer_stop();
        free(linePoint);
        linePoint = NULL;
        free(ballPoint);
        ballPoint = NULL;
    } else {
        linePoint->y = (int) llround(get_height() * (progress * 2));
        linePoint->y = get_height() - (linePoint->y - get_height());
        ballPoint->y = linePoint->y;
    }
    repaint();
}''',
        "csharp": r'''using System;

public class Point
{
    public int x, y;
}

public class Timer
{
    public void stop() {}
}

public class ActionEvent
{
    private readonly Timer source;

    public ActionEvent(Timer source) { this.source = source; }

    public Timer getSource() { return source; }
}

public class AnimatedPanel
{
    private const float RUN_TIME = 1000f;

    public long startTime;
    public Point linePoint;
    public Point ballPoint;

    public int getWidth() { return 400; }
    public int getHeight() { return 300; }
    public void repaint() {}

    public void actionPerformed(ActionEvent e)
    {
        long duration = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond - startTime;
        float progress = (float) duration / RUN_TIME;
        linePoint = new Point();
        linePoint.x = getWidth() / 2;
        if (progress < 0.5f)
        {
            linePoint.y = (int) Math.Floor(getHeight() * (progress * 2) + 0.5);
        }
        else
        {
            if (progress > 1f)
            {
                progress = 1f;
                e.getSource().stop();
                linePoint = null;
                ballPoint = null;
            }
            else
            {
                linePoint.y = (int) Math.Floor(getHeight() * (progress * 2) + 0.5);
                linePoint.y = getHeight() - (linePoint.y - getHeight());
                ballPoint.y = linePoint.y;
            }
        }
        repaint();
    }
}'''
    },
    "T653": {
        "python": r'''def show_input_dialog(icon_path, message):
    return input(message + " ")


class Frame:
    def __init__(self):
        self.width = 0
        self.height = 0

    def set_size(self, width, height):
        self.width = width
        self.height = height


class Listener:
    def __init__(self):
        self.frame = Frame()

    def scale(self, new_width, new_height):
        pass

    def action_performed(self, e):
        scale_width = show_input_dialog("LR-arrows.png", "What should the new width be?")
        scale_height = show_input_dialog("UD-arrows.png", "What should the new height be?")
        x = float(scale_width)
        y = float(scale_height)
        new_width = int(x)
        new_height = int(y)
        self.frame.set_size(new_width, new_height)
        self.scale(new_width, new_height)''',
        "c": r'''#include <stdio.h>

extern void frame_set_size(int width, int height);
extern void scale(int newWidth, int newHeight);

static void read_double(const char *prompt, double *out) {
    printf("%s", prompt);
    scanf("%lf", out);
}

void action_performed(void) {
    double x, y;
    read_double("What should the new width be?", &x);
    read_double("What should the new height be?", &y);
    int newWidth = (int) x;
    int newHeight = (int) y;
    frame_set_size(newWidth, newHeight);
    scale(newWidth, newHeight);
}''',
        "csharp": r'''using System;

public class ActionEvent {}

public class MainFrame
{
    public void setSize(int w, int h) {}
    public void scale(int w, int h) {}
}

public class ScaleDialog
{
    private MainFrame frame = new MainFrame();

    private static string ShowInputDialog(string iconPath, string message)
    {
        Console.Write(message + " ");
        return Console.ReadLine();
    }

    public void actionPerformed(ActionEvent e)
    {
        string scaleWidth = ShowInputDialog("LR-arrows.png", "What should the new width be?");
        string scaleHeight = ShowInputDialog("UD-arrows.png", "What should the new height be?");
        double x = double.Parse(scaleWidth);
        double y = double.Parse(scaleHeight);
        int newWidth = (int) x;
        int newHeight = (int) y;
        frame.setSize(newWidth, newHeight);
        scale(newWidth, newHeight);
    }
}'''
    }
}
