DATA_T4 = {
"T181": {
"python": '''class Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class LinkedList:
    def __init__(self):
        self.first = None
        self.count = 0

    def size(self):
        return self.count

    def second_max_key(self):
        if self.size() < 2:
            return None
        max_node = None
        max_2 = None
        second = self.first.next
        if self.first.key > second.key:
            max_node, max_2 = self.first, second
        else:
            max_node, max_2 = second, self.first
        x = second.next
        while x is not None:
            if x.key > max_node.key:
                max_2 = max_node
                max_node = x
            elif x.key > max_2.key and x.key < max_node.key:
                max_2 = x
            x = x.next
        return max_2.key''',
"c": '''#include <stddef.h>

typedef struct Node {
    int key;
    struct Node *next;
} Node;

int secondMaxKey(Node *first, size_t size) {
    if (size < 2) return -1;
    Node *max = NULL, *max2 = NULL;
    Node *second = first->next;
    if (first->key > second->key) {
        max = first;
        max2 = second;
    } else {
        max = second;
        max2 = first;
    }
    for (Node *x = second->next; x != NULL; x = x->next) {
        if (x->key > max->key) {
            max2 = max;
            max = x;
        } else if (x->key > max2->key && x->key < max->key) {
            max2 = x;
        }
    }
    return max2->key;
}''',
"csharp": '''public class Node<TKey> where TKey : IComparable<TKey> {
    public TKey Key;
    public Node<TKey> Next;
}

public class LinkedList<TKey> where TKey : IComparable<TKey> {
    public Node<TKey> First;
    public int Size;

    public TKey SecondMaxKey() {
        if (Size < 2) return default;
        Node<TKey> max = null, max2 = null;
        Node<TKey> second = First.Next;
        if (First.Key.CompareTo(second.Key) > 0) {
            max = First;
            max2 = second;
        } else {
            max = second;
            max2 = First;
        }
        for (Node<TKey> x = second.Next; x != null; x = x.Next) {
            if (x.Key.CompareTo(max.Key) > 0) {
                max2 = max;
                max = x;
            } else if (x.Key.CompareTo(max2.Key) > 0 && x.Key.CompareTo(max.Key) < 0) {
                max2 = x;
            }
        }
        return max2.Key;
    }
}'''
},
"T216": {
"python": '''def print_all(*to_print):
    for item in to_print:
        if isinstance(item, list):
            print("[" + ", ".join(str(x) for x in item) + "]")
        else:
            print(item)''',
"c": '''#include <stdio.h>

typedef enum { TYPE_INT_ARRAY, TYPE_DOUBLE_ARRAY, TYPE_STRING } VarargType;

void print_varargs(VarargType type, void *data, int len) {
    if (type == TYPE_INT_ARRAY) {
        int *arr = (int *)data;
        printf("[");
        for (int i = 0; i < len; i++) printf(i ? ", %d" : "%d", arr[i]);
        printf("]\\n");
    } else if (type == TYPE_DOUBLE_ARRAY) {
        double *arr = (double *)data;
        printf("[");
        for (int i = 0; i < len; i++) printf(i ? ", %g" : "%g", arr[i]);
        printf("]\\n");
    } else {
        printf("%s\\n", (char *)data);
    }
}''',
"csharp": '''public static void Print(params object[] toPrint) {
    foreach (object item in toPrint) {
        if (item is int[]) {
            Console.WriteLine("[" + string.Join(", ", (int[])item) + "]");
        } else if (item is double[]) {
            Console.WriteLine("[" + string.Join(", ", (double[])item) + "]");
        } else if (item is object[]) {
            Console.WriteLine("[" + string.Join(", ", (object[])item) + "]");
        } else {
            Console.WriteLine(item);
        }
    }
}'''
},
"T156": {
"python": '''def solution(X, A):
    seen = set()
    sum1 = sum(range(X + 1))
    sum2 = 0
    for i, a in enumerate(A):
        if a in seen:
            continue
        seen.add(a)
        sum2 += a
        if sum1 == sum2:
            return i
    return -1''',
"c": '''#include <stdbool.h>

int solution(int X, int *A, int n) {
    int seen[100000];
    int seenCount = 0;
    long sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    for (int i = 0; i < n; i++) {
        bool dup = false;
        for (int j = 0; j < seenCount; j++) {
            if (seen[j] == A[i]) { dup = true; break; }
        }
        if (dup) continue;
        seen[seenCount++] = A[i];
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}''',
"csharp": '''public static int Solution(int X, int[] A) {
    var seen = new HashSet<int>();
    long sum1 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    long sum2 = 0;
    for (int i = 0; i < A.Length; i++) {
        if (seen.Contains(A[i])) continue;
        seen.Add(A[i]);
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}'''
},
"T462": {
"python": '''import random


class MyRectangle:
    def __init__(self, x, y, width, height, color):
        self.x, self.y, self.width, self.height, self.color = x, y, width, height, color


class Canvas:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.shapes = []

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def repaint(self):
        pass


canvas = Canvas()


def on_action():
    x = int(random.random() * canvas.get_width())
    y = int(random.random() * canvas.get_height())
    width = int(random.random() * (canvas.get_width() / 4))
    height = int(random.random() * (canvas.get_height() / 4))
    if x + width > canvas.get_width():
        x = canvas.get_width() - width
    if y + height > canvas.get_height():
        y = canvas.get_height() - height
    color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
    canvas.shapes.append(MyRectangle(x, y, width, height, color))
    canvas.repaint()''',
"c": '''#include <stdlib.h>

typedef struct {
    int x, y, width, height;
    int r, g, b;
} MyRectangle;

MyRectangle shapes[256];
int shapeCount = 0;
int canvasWidth = 800, canvasHeight = 600;

void repaint(void) {
}

void actionPerformed(void) {
    int x = rand() % canvasWidth;
    int y = rand() % canvasHeight;
    int width = rand() % (canvasWidth / 4);
    int height = rand() % (canvasHeight / 4);
    if (x + width > canvasWidth) x = canvasWidth - width;
    if (y + height > canvasHeight) y = canvasHeight - height;
    MyRectangle rect = {x, y, width, height, rand() % 255, rand() % 255, rand() % 255};
    shapes[shapeCount++] = rect;
    repaint();
}''',
"csharp": '''public class MyRectangle {
    public int X, Y, Width, Height;
    public Color Color;

    public MyRectangle(int x, int y, int width, int height, Color color) {
        X = x; Y = y; Width = width; Height = height; Color = color;
    }
}

public class ShapePanel {
    List<MyRectangle> lstShapes = new List<MyRectangle>();
    int panelWidth = 800, panelHeight = 600;
    Random random = new Random();

    public void OnAction() {
        int x = (int)(random.NextDouble() * panelWidth);
        int y = (int)(random.NextDouble() * panelHeight);
        int width = (int)(random.NextDouble() * (panelWidth / 4));
        int height = (int)(random.NextDouble() * (panelHeight / 4));
        if (x + width > panelWidth) x = panelWidth - width;
        if (y + height > panelHeight) y = panelHeight - height;
        Color color = Color.FromArgb(random.Next(255), random.Next(255), random.Next(255));
        lstShapes.Add(new MyRectangle(x, y, width, height, color));
        Repaint();
    }

    void Repaint() {
    }
}'''
}
}
