DATA_T3 = {
"T586": {
"python": r'''
def dedup(text):
    result = ""
    for ch in text:
        if result.find(ch) == -1:
            result = result + ch
    return result

def main():
    source = "harikrishna"
    print(dedup(source))
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char src[64] = "harikrishna";
    char dst[64] = "";
    int used[256] = {0};
    int pos = 0;
    for (size_t i = 0; i < strlen(src); i++) {
        unsigned char c = src[i];
        if (!used[c]) {
            used[c] = 1;
            dst[pos++] = c;
        }
    }
    dst[pos] = '\0';
    printf("%s\n", dst);
    return 0;
}
''',
"csharp": r'''
using System;
using System.Text;

public static class Dedup
{
    public static void Main()
    {
        string s = "harikrishna";
        var seen = new HashSet<char>();
        var sb = new StringBuilder();
        foreach (char c in s)
        {
            if (!seen.Contains(c))
            {
                seen.Add(c);
                sb.Append(c);
            }
        }
        Console.WriteLine(sb.ToString());
    }
}
'''
},
"T407": {
"python": r'''
def main():
    x_sum = 0
    y_sum = 0
    with open("D:/Test.txt") as f:
        for line in f:
            if "x=" in line:
                x_sum += int(line.split("=")[1].strip())
            if "y=" in line:
                y_sum += int(line.split("=")[1].strip())
    print("Sum x is: " + str(x_sum) + " Sum y is: " + str(y_sum))
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *file = fopen("D:/Test.txt", "r");
    if (file == NULL) return 1;
    char line[512];
    int x_sum = 0;
    int y_sum = 0;
    while (fgets(line, sizeof(line), file) != NULL) {
        char *eq = strchr(line, '=');
        if (eq != NULL && eq[1] != '\0') {
            char *key_start = line;
            while (*key_start == ' ') key_start++;
            if (strncmp(key_start, "x=", 2) == 0 || strncmp(key_start, "y=", 2) == 0) {
                int value = atoi(eq + 1);
                if (key_start[0] == 'x') x_sum += value;
                else y_sum += value;
            }
        }
    }
    fclose(file);
    printf("Sum x is: %d Sum y is: %d\n", x_sum, y_sum);
    return 0;
}
''',
"csharp": r'''
using System;
using System.IO;

public static class SumReader
{
    public static void Main()
    {
        int xSum = 0;
        int ySum = 0;
        foreach (string line in File.ReadLines("D:/Test.txt"))
        {
            int eq = line.IndexOf('=');
            if (eq >= 0 && eq + 1 < line.Length)
            {
                int value = int.Parse(line.Substring(eq + 1).Trim());
                if (line.StartsWith("x="))
                {
                    xSum += value;
                }
                if (line.StartsWith("y="))
                {
                    ySum += value;
                }
            }
        }
        Console.WriteLine("Sum x is: " + xSum + " Sum y is: " + ySum);
    }
}
'''
},
"T883": {
"python": r'''
def transform(self, workbook_old, workbook_new, row_old, row_new):
    row_new.height = row_old.height
    for cell in row_old:
        cell_new = row_new.create_cell(cell.column_index, cell.cell_type)
        if cell_new is not None:
            self.transform_cell(workbook_old, workbook_new, cell, cell_new)
    self.last_column = max(self.last_column, row_old.last_cell_num)

def transform_cell(self, workbook_old, workbook_new, cell_old, cell_new):
    cell_new.value = cell_old.value
''',
"c": r'''
#include <stddef.h>
#include <math.h>

typedef struct { int column_index; int cell_type; double value; } OldCell;
typedef struct { int column_index; int cell_type; double value; } NewCell;

typedef struct { double height; int last_cell_num; OldCell cells[64]; int cell_count; } OldRow;
typedef struct { double height; NewCell cells[64]; int cell_count; } NewRow;

typedef struct { int last_column; } Transformer;

void transform_cell(Transformer *t, OldCell *cell_old, NewCell *cell_new) {
    cell_new->value = cell_old->value;
}

void transform(Transformer *t, OldRow *row_old, NewRow *row_new) {
    row_new->height = row_old->height;
    for (int i = 0; i < row_old->cell_count; i++) {
        OldCell *cell = &row_old->cells[i];
        NewCell *cell_new = &row_new->cells[row_new->cell_count++];
        cell_new->column_index = cell->column_index;
        cell_new->cell_type = cell->cell_type;
        transform_cell(t, cell, cell_new);
    }
    if (row_old->last_cell_num > t->last_column) {
        t->last_column = row_old->last_cell_num;
    }
}
''',
"csharp": r'''
using System;

public class RowTransformer
{
    public int LastColumn { get; private set; }

    private void TransformCell(OldCell oldCell, NewCell newCell)
    {
        newCell.Value = oldCell.Value;
    }

    private void Transform(OldRow rowOld, NewRow rowNew)
    {
        rowNew.Height = rowOld.Height;
        foreach (OldCell cell in rowOld.Cells)
        {
            NewCell cellNew = rowNew.CreateCell(cell.ColumnIndex, cell.CellType);
            if (cellNew != null)
            {
                TransformCell(cell, cellNew);
            }
        }
        LastColumn = Math.Max(LastColumn, rowOld.LastCellNum);
    }
}

public class OldCell
{
    public int ColumnIndex { get; set; }
    public int CellType { get; set; }
    public double Value { get; set; }
}

public class OldRow
{
    public double Height { get; set; }
    public int LastCellNum { get; set; }
    public OldCell[] Cells { get; set; }
}

public class NewRow
{
    public double Height { get; set; }
    private readonly System.Collections.Generic.List<NewCell> _cells = new System.Collections.Generic.List<NewCell>();

    public NewCell CreateCell(int index, int type)
    {
        var cell = new NewCell { ColumnIndex = index, CellType = type };
        _cells.Add(cell);
        return cell;
    }
}

public class NewCell
{
    public int ColumnIndex { get; set; }
    public int CellType { get; set; }
    public double Value { get; set; }
}
'''
},
"T477": {
"python": r'''
import math

def get_random_number_between(number_one, number_two):
    if number_one == number_two:
        raise ValueError("Both the numbers can not be equal")
    rand = random.random()
    high_range = max(number_one, number_two)
    low_range = min(number_one, number_two)
    low_rand = math.floor(rand - 1)
    high_rand = math.ceil(rand + 1)
    gen_rand = (high_range - low_range) * ((rand - low_rand) / (high_rand - low_rand)) + low_range
    return gen_rand
''',
"c": r'''
#include <math.h>
#include <stdlib.h>

double get_random_number_between(double number_one, double number_two) {
    if (number_one == number_two) return 0.0;
    double rand = (double)rand() / RAND_MAX;
    double high_range = fmax(number_one, number_two);
    double low_range = fmin(number_one, number_two);
    double low_rand = floor(rand - 1);
    double high_rand = ceil(rand + 1);
    double gen_rand = (high_range - low_range) * ((rand - low_rand) / (high_rand - low_rand)) + low_range;
    return gen_rand;
}
''',
"csharp": r'''
using System;

public static class RandomRange
{
    private static readonly Random Rng = new Random();

    public static float GetRandomNumberBetween(float numberOne, float numberTwo)
    {
        if (numberOne == numberTwo)
        {
            throw new ArgumentException("Both the numbers can not be equal");
        }
        float rand = (float)Rng.NextDouble();
        float highRange = Math.Max(numberOne, numberTwo);
        float lowRange = Math.Min(numberOne, numberTwo);
        float lowRand = (float)Math.Floor(rand - 1);
        float highRand = (float)Math.Ceiling(rand + 1);
        float genRand = (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
        return genRand;
    }
}
'''
},
"T842": {
"python": r'''
def main():
    exit_command = "exit"
    print("Enter some text, or '" + exit_command + "' to quit")
    while True:
        prompt = ">@@ "
        print(prompt, end="")
        line = input()
        print(line)
        if len(line) == len(exit_command) and line.lower() == exit_command:
            print("Exiting.")
            return
        print("...response goes here...")
''',
"c": r'''
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char input[512];
    const char *exit_command = "exit";
    printf("Enter some text, or '%s' to quit\n", exit_command);
    while (1) {
        printf("><@@ ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        input[strcspn(input, "\n")] = '\0';
        printf("%s\n", input);
        char lower[512];
        size_t len = strlen(input);
        for (size_t i = 0; i <= len; i++) {
            lower[i] = (char)tolower((unsigned char)input[i]);
        }
        if (len == strlen(exit_command) && strcmp(lower, exit_command) == 0) {
            printf("Exiting.\n");
            return 0;
        }
        printf("...response goes here...\n");
    }
    return 0;
}
''',
"csharp": r'''
using System;

public static class EchoLoop
{
    public static void Main()
    {
        string exitCommand = "exit";
        Console.WriteLine("Enter some text, or '" + exitCommand + "' to quit");
        while (true)
        {
            Console.Write(">< ");
            string input = Console.ReadLine();
            Console.WriteLine(input);
            if (input.Length == exitCommand.Length && input.ToLower().Equals(exitCommand))
            {
                Console.WriteLine("Exiting.");
                return;
            }
            Console.WriteLine("...response goes here...");
        }
    }
}
'''
},
"T181": {
"python": r'''
def second_max_key(self):
    if self.size() < 2:
        return None
    m1 = m2 = None
    second = self.first.next
    if self.first.key > second.key:
        m1, m2 = self.first, second
    else:
        m1, m2 = second, self.first
    x = second.next
    while x is not None:
        if x.key > m1.key:
            m2, m1 = m1, x
        elif x.key > m2.key and x.key < m1.key:
            m2 = x
        x = x.next
    return m2.key
''',
"c": r'''
#include <stddef.h>

typedef struct Node {
    int key;
    struct Node *next;
} Node;

typedef struct { Node *first; int count; } LinkedList;

int list_size(LinkedList *list) { return list->count; }

int second_max_key(LinkedList *list) {
    if (list_size(list) < 2) return -1;
    Node *m1 = NULL;
    Node *m2 = NULL;
    Node *second = list->first->next;
    if (list->first->key > second->key) {
        m1 = list->first;
        m2 = second;
    } else {
        m1 = second;
        m2 = list->first;
    }
    for (Node *x = second->next; x != NULL; x = x->next) {
        if (x->key > m1->key) {
            m2 = m1;
            m1 = x;
        } else if (x->key > m2->key && x->key < m1->key) {
            m2 = x;
        }
    }
    return m2->key;
}
''',
"csharp": r'''
using System;

public class Node
{
    public IComparable Key { get; set; }
    public Node Next { get; set; }
}

public class LinkedList
{
    public Node First { get; set; }

    public IComparable SecondMaxKey()
    {
        Node first = First;
        Node second = first.Next;
        if (second == null)
        {
            return null;
        }
        Node max, max2;
        if (first.Key.CompareTo(second.Key) > 0)
        {
            max = first;
            max2 = second;
        }
        else
        {
            max = second;
            max2 = first;
        }
        for (Node x = second.Next; x != null; x = x.Next)
        {
            if (x.Key.CompareTo(max.Key) > 0)
            {
                max2 = max;
                max = x;
            }
            else if (x.Key.CompareTo(max2.Key) > 0 && x.Key.CompareTo(max.Key) < 0)
            {
                max2 = x;
            }
        }
        return max2.Key;
    }
}
'''
},
"T216": {
"python": r'''
def print_items(to_print):
    for item in to_print:
        if isinstance(item, list):
            rendered = "[" + ", ".join(str(v) for v in item) + "]"
            print(rendered)
        elif isinstance(item, tuple):
            print(list(item))
        else:
            print(item)
''',
"c": r'''
#include <stdio.h>

static void print_int_array(const int *a, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d", a[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}

static void print_double_array(const double *a, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%g", a[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}

typedef enum { KIND_INT_ARR, KIND_DOUBLE_ARR, KIND_TEXT } Kind;

typedef struct {
    Kind kind;
    const int *ints;
    const double *doubles;
    int n;
    const char *text;
} AnyArg;

static void print(const AnyArg *args, int count) {
    for (int i = 0; i < count; i++) {
        switch (args[i].kind) {
            case KIND_INT_ARR:
                print_int_array(args[i].ints, args[i].n);
                break;
            case KIND_DOUBLE_ARR:
                print_double_array(args[i].doubles, args[i].n);
                break;
            default:
                printf("%s\n", args[i].text);
                break;
        }
    }
}
''',
"csharp": r'''
using System;
using System.Text;

public static class Printer
{
    private static string Describe<T>(T[] items)
    {
        var sb = new StringBuilder("[");
        for (int i = 0; i < items.Length; i++)
        {
            sb.Append(items[i]);
            if (i < items.Length - 1) sb.Append(", ");
        }
        return sb.Append("]").ToString();
    }

    public static void Print(params object[] toPrint)
    {
        foreach (object item in toPrint)
        {
            if (item is int[] intArray)
            {
                Console.WriteLine(Describe(intArray));
            }
            else if (item is double[] doubleArray)
            {
                Console.WriteLine(Describe(doubleArray));
            }
            else if (item is object[] objArray)
            {
                Console.WriteLine(Describe(objArray));
            }
            else
            {
                Console.WriteLine(item);
            }
        }
    }
}
'''
},
"T156": {
"python": r'''
def solution(X, A):
    required = set(range(1, X + 1))
    covered = set()
    for position, leaf in enumerate(A):
        if leaf in required:
            covered.add(leaf)
        if len(covered) == X:
            return position
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    char *covered = calloc(X + 1, sizeof(char));
    int distinct = 0;
    for (int i = 0; i < len; i++) {
        int leaf = A[i];
        if (leaf >= 1 && leaf <= X && !covered[leaf]) {
            covered[leaf] = 1;
            distinct++;
        }
        if (distinct == X) {
            free(covered);
            return i;
        }
    }
    free(covered);
    return -1;
}
''',
"csharp": r'''
using System.Collections.Generic;

public static class EarliestCrossing
{
    public static int Solution(int X, int[] A)
    {
        var covered = new HashSet<int>();
        for (int i = 0; i < A.Length; i++)
        {
            if (A[i] >= 1 && A[i] <= X)
            {
                covered.Add(A[i]);
            }
            if (covered.Count == X)
            {
                return i;
            }
        }
        return -1;
    }
}
'''
},
"T462": {
"python": r'''
import random

class MyRectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class Canvas:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.shapes = []

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def repaint(self):
        pass

    def action_performed(self):
        x = int(random.random() * self.get_width())
        y = int(random.random() * self.get_height())
        width = int(random.random() * (self.get_width() / 4))
        height = int(random.random() * (self.get_height() / 4))
        if x + width > self.get_width():
            x = self.get_width() - width
        if y + height > self.get_height():
            y = self.get_height() - height
        color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        self.shapes.append(MyRectangle(x, y, width, height, color))
        self.repaint()
''',
"c": r'''
#include <stdlib.h>

typedef struct { int r, g, b; } Color;

typedef struct {
    int x, y, width, height;
    Color color;
} MyRectangle;

typedef struct {
    int width, height;
    MyRectangle shapes[64];
    int shape_count;
} Canvas;

static int canvas_width(Canvas *c) { return c->width; }
static int canvas_height(Canvas *c) { return c->height; }
static void repaint(Canvas *c) { (void)c; }

static double unit_random(void) {
    return (double)rand() / RAND_MAX;
}

static void add_random_rectangle(Canvas *c) {
    int x = (int)(unit_random() * canvas_width(c));
    int y = (int)(unit_random() * canvas_height(c));
    int w = (int)(unit_random() * (canvas_width(c) / 4));
    int h = (int)(unit_random() * (canvas_height(c) / 4));
    if (x + w > canvas_width(c)) x = canvas_width(c) - w;
    if (y + h > canvas_height(c)) y = canvas_height(c) - h;
    Color color = {
        (int)(unit_random() * 255),
        (int)(unit_random() * 255),
        (int)(unit_random() * 255)
    };
    c->shapes[c->shape_count++] = (MyRectangle){x, y, w, h, color};
    repaint(c);
}
''',
"csharp": r'''
using System;
using System.Drawing;
using System.Windows.Forms;

public class MyRectangle
{
    public int X { get; set; }
    public int Y { get; set; }
    public int Width { get; set; }
    public int Height { get; set; }
    public Color Color { get; set; }

    public MyRectangle(int x, int y, int width, int height, Color color)
    {
        X = x;
        Y = y;
        Width = width;
        Height = height;
        Color = color;
    }
}

public class ShapeCanvas : Panel
{
    public readonly System.Collections.Generic.List<MyRectangle> Shapes =
        new System.Collections.Generic.List<MyRectangle>();

    private static readonly Random Rng = new Random();

    public void AddRandomShape()
    {
        int x = (int)(Rng.NextDouble() * Width);
        int y = (int)(Rng.NextDouble() * Height);
        int width = (int)(Rng.NextDouble() * (Width / 4));
        int height = (int)(Rng.NextDouble() * (Height / 4));
        if (x + width > Width)
        {
            x = Width - width;
        }
        if (y + height > Height)
        {
            y = Height - height;
        }
        var color = Color.FromArgb((int)(Rng.NextDouble() * 255),
                                   (int)(Rng.NextDouble() * 255),
                                   (int)(Rng.NextDouble() * 255));
        Shapes.Add(new MyRectangle(x, y, width, height, color));
        Invalidate();
    }
}
'''
}
}
