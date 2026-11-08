DATA1 = {
"T297": {
 "python": r'''class ListNode:
    def __init__(self):
        self.next = None
    def __str__(self):
        return "ListNode"

def switch_pairs(this):
    if this is None or this.next is None:
        return this
    top = this.next
    first = this
    second = first.next
    while True:
        third = second.next
        second.next = first
        first.next = third
        first = third
        print("@@@ " + str(this))
        if first is not None:
            second.next.next = first.next
            second = first.next
        if not (first is not None and second is not None):
            break
    return top''',
 "c": r'''struct ListNode {
    struct ListNode *next;
};

struct ListNode *switch_pairs(struct ListNode *self) {
    if (self == NULL || self->next == NULL) return self;
    struct ListNode *top = self->next;
    struct ListNode *first = self;
    struct ListNode *second = first->next;
    do {
        struct ListNode *third = second->next;
        second->next = first;
        first->next = third;
        first = third;
        printf("@@@ %p\n", (void *) self);
        if (first != NULL) {
            second->next->next = first->next;
            second = first->next;
        }
    } while (first != NULL && second != NULL);
    return top;
}''',
 "csharp": r'''class ListNode {
    public ListNode next;
    public override string ToString() { return "ListNode"; }

    public ListNode SwitchPairs() {
        if (this == null || this.next == null) return this;
        ListNode top = this.next;
        ListNode first = this;
        ListNode second = first.next;
        do {
            ListNode third = second.next;
            second.next = first;
            first.next = third;
            first = third;
            Console.WriteLine("@@@ " + this.ToString());
            if (first != null) {
                second.next.next = first.next;
                second = first.next;
            }
        } while (first != null && second != null);
        return top;
    }
}'''
},
"T252": {
 "python": r'''import pickle
import traceback

def action_performed(self, event):
    try:
        with open(self.file, "rb") as f:
            self.model = pickle.load(f)
        self.table.setModel(self.model)
    except OSError as ex:
        traceback.print_exc()''',
 "c": r'''typedef struct TableModel TableModel;
typedef struct Table Table;
extern TableModel *xml_decoder_read_object(FILE *fp);
extern void table_set_model(Table *table, TableModel *model);
extern const char *inputFile;

void action_performed(ActionEvent *e) {
    FILE *fp = fopen(inputFile, "rb");
    if (fp == NULL) {
        perror("open failed");
        return;
    }
    TableModel *model = xml_decoder_read_object(fp);
    fclose(fp);
    table_set_model(&table, model);
}''',
 "csharp": r'''public void actionPerformed(ActionEvent e) {
    try {
        var serializer = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
        using (var stream = new FileStream(file, FileMode.Open, FileAccess.Read)) {
            model = (DefaultTableModel) serializer.Deserialize(stream);
        }
        table.setModel(model);
    } catch (IOException ex) {
        Console.WriteLine(ex.ToString());
    }
}'''
},
"T10": {
 "python": r'''class Node:
    def __init__(self):
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
 "c": r'''struct Node {
    struct Node *next;
};

struct Node *reverse(struct Node *n, struct Node *p) {
    if (n == NULL) return NULL;
    if (n->next == NULL) {
        n->next = p;
        return n;
    }
    struct Node *r = reverse(n->next, n);
    n->next = p;
    return r;
}''',
 "csharp": r'''class Node {
    public Node next;
}

public Node Reverse(Node n, Node p) {
    if (n == null) return null;
    if (n.next == null) {
        n.next = p;
        return n;
    }
    Node r = Reverse(n.next, n);
    n.next = p;
    return r;
}'''
},
"T146": {
 "python": r'''def solution(x, a):
    hset = set()
    for i in range(len(a)):
        if a[i] <= x:
            hset.add(a[i])
        if len(hset) == x:
            return i
    return -1''',
 "c": r'''int solution(int X, const int *A, int n) {
    int *seen = calloc(X + 1, sizeof(int));
    int distinct = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] >= 0 && A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
        }
        if (distinct == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}''',
 "csharp": r'''public static int Solution(int x, int[] a) {
    var hset = new HashSet<int>();
    for (int i = 0; i < a.Length; i++) {
        if (a[i] <= x) hset.Add(a[i]);
        if (hset.Count == x) return i;
    }
    return -1;
}'''
},
"T110": {
 "python": r'''import time

def throw_catch_loop():
    start = time.perf_counter_ns()
    try:
        raise RuntimeError("x")
    except RuntimeError:
        pass
    return time.perf_counter_ns() - start

def new_exception_loop():
    start = time.perf_counter_ns()
    err = RuntimeError("x")
    return time.perf_counter_ns() - start

def new_object_loop():
    start = time.perf_counter_ns()
    obj = object()
    return time.perf_counter_ns() - start

def new_no_stack_exception_loop():
    start = time.perf_counter_ns()
    err = RuntimeError()
    err.__traceback__ = None
    return time.perf_counter_ns() - start

def main():
    throwCatchTime = 0
    newExceptionTime = 0
    newObjectTime = 0
    noStackExceptionTime = 0
    for _ in range(30):
        throwCatchTime += throw_catch_loop()
        newExceptionTime += new_exception_loop()
        newObjectTime += new_object_loop()
        noStackExceptionTime += new_no_stack_exception_loop()
    print("throwCatchTime = " + str(throwCatchTime // 30))
    print("newExceptionTime = " + str(newExceptionTime // 30))
    print("newStringTime = " + str(newObjectTime // 30))
    print("noStackExceptionTime = " + str(noStackExceptionTime // 30))''',
 "c": r'''#include <stdio.h>
#include <time.h>

long throwCatchLoop(void) {
    clock_t start = clock();
    volatile int x = 1;
    x++;
    return (long)(clock() - start);
}

long newExceptionLoop(void) {
    clock_t start = clock();
    volatile int x = 1;
    x++;
    return (long)(clock() - start);
}

long newObjectLoop(void) {
    clock_t start = clock();
    volatile int x = 1;
    x++;
    return (long)(clock() - start);
}

long newNoStackExceptionLoop(void) {
    clock_t start = clock();
    volatile int x = 1;
    x++;
    return (long)(clock() - start);
}

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
using System.Diagnostics;

class Program {
    static long ThrowCatchLoop() {
        var watch = Stopwatch.StartNew();
        try { throw new InvalidOperationException("x"); }
        catch (InvalidOperationException) { }
        return watch.ElapsedMilliseconds;
    }

    static long NewExceptionLoop() {
        var watch = Stopwatch.StartNew();
        var e = new InvalidOperationException("x");
        return watch.ElapsedMilliseconds;
    }

    static long NewObjectLoop() {
        var watch = Stopwatch.StartNew();
        var o = new object();
        return watch.ElapsedMilliseconds;
    }

    static long NewNoStackExceptionLoop() {
        var watch = Stopwatch.StartNew();
        var e = new InvalidOperationException();
        return watch.ElapsedMilliseconds;
    }

    static void Main(string[] args) {
        long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
        for (int i = 0; i < 30; i++) {
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
 "python": r'''IMAGE_CAPTURE = 1
RESULT_OK = -1

class SQLiteDatabase:
    def execute(self, sql):
        pass
    def close(self):
        pass

class DBHelper:
    def __init__(self, context):
        self._db = SQLiteDatabase()
    def getWritableDatabase(self):
        return self._db
    def close(self):
        pass

def on_activity_result(self, request_code, result_code, data):
    if request_code == IMAGE_CAPTURE and result_code == RESULT_OK:
        db_helper = DBHelper(self)
        sql = db_helper.getWritableDatabase()
        sql.execute("insert statement for inserting path to database")
        sql.close()
        db_helper.close()''',
 "c": r'''#define IMAGE_CAPTURE 1
#define RESULT_OK (-1)

typedef struct DbHelper DbHelper;
typedef struct SqlDb SqlDb;
extern DbHelper *db_helper_create(void *context);
extern SqlDb *db_helper_get_writable(DbHelper *db);
extern void sql_exec(SqlDb *db, const char *sql);
extern void sql_close(SqlDb *db);
extern void db_helper_close(DbHelper *db);

void on_activity_result(int request_code, int result_code, void *data) {
    if (request_code == IMAGE_CAPTURE && result_code == RESULT_OK) {
        DbHelper *db_helper = db_helper_create(data);
        SqlDb *sql = db_helper_get_writable(db_helper);
        sql_exec(sql, "insert statement for inserting path to database");
        sql_close(sql);
        db_helper_close(db_helper);
    }
}''',
 "csharp": r'''class SQLiteDatabase {
    public void ExecSQL(string sql) { }
    public void Close() { }
}

class DBHelper {
    public DBHelper(object context) { }
    public SQLiteDatabase GetWritableDatabase() { return new SQLiteDatabase(); }
    public void Close() { }
}

protected void OnActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
        var dbHelper = new DBHelper(this);
        var sql = dbHelper.GetWritableDatabase();
        sql.ExecSQL("insert statement for inserting path to database");
        sql.Close();
        dbHelper.Close();
    }
}'''
},
}
