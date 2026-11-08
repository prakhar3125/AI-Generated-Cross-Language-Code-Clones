DATA4 = {
"T407": {"outputs": {
"python": r"""def main():
    x_sum = 0
    y_sum = 0
    with open(r"D:\Test.txt") as br:
        for line in br:
            line = line.rstrip("\n")
            if "x=" in line:
                x_sum += int(line.split("=")[1].strip())
            if "y=" in line:
                y_sum += int(line.split("=")[1].strip())
    print("Sum x is: " + str(x_sum) + " Sum y is: " + str(y_sum))
""",
"c": r"""#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *file = fopen("D:\\Test.txt", "r");
    if (file == NULL) return 1;
    char line[256];
    int xSum = 0, ySum = 0;
    while (fgets(line, sizeof(line), file) != NULL) {
        char *eq;
        if ((eq = strstr(line, "x=")) != NULL) {
            xSum += atoi(eq + 2);
        }
        if ((eq = strstr(line, "y=")) != NULL) {
            ySum += atoi(eq + 2);
        }
    }
    fclose(file);
    printf("Sum x is: %d Sum y is: %d\n", xSum, ySum);
    return 0;
}
""",
"csharp": r"""using System;
using System.IO;

public static void Main(string[] args)
{
    int xSum = 0, ySum = 0;
    using (var file = new StreamReader(@"D:\Test.txt"))
    {
        string line;
        while ((line = file.ReadLine()) != null)
        {
            if (line.Contains("x=")) xSum += int.Parse(line.Split('=')[1].Trim());
            if (line.Contains("y=")) ySum += int.Parse(line.Split('=')[1].Trim());
        }
    }
    Console.WriteLine("Sum x is: " + xSum + " Sum y is: " + ySum);
}
""",
}},
"T883": {"outputs": {
"python": r"""class Cell:
    def __init__(self, column_index, cell_type):
        self.column_index = column_index
        self.cell_type = cell_type

class RowOld:
    def __init__(self, cells, height, last_cell_num):
        self.cells = cells
        self.height = height
        self.last_cell_num = last_cell_num

    def __iter__(self):
        return iter(self.cells)

class RowNew:
    def __init__(self):
        self.height = 0

    def set_height(self, height):
        self.height = height

    def create_cell(self, column_index, cell_type):
        return Cell(column_index, cell_type)

def transform(workbook_old, workbook_new, row_old, row_new, transform_cell, state):
    row_new.set_height(row_old.height)
    for cell in row_old:
        cell_new = row_new.create_cell(cell.column_index, cell.cell_type)
        if cell_new is not None:
            transform_cell(workbook_old, workbook_new, cell, cell_new)
    state["last_column"] = max(state["last_column"], row_old.last_cell_num)
""",
"c": r"""#include <stddef.h>

typedef struct { int columnIndex; int cellType; } Cell;

typedef Cell *(*CreateCellFn)(int columnIndex, int cellType);
typedef void (*TransformCellFn)(Cell *oldCell, Cell *newCell);

void transformRow(int *rowNewHeight, int rowOldHeight, Cell **rowOldCells, int cellCount,
                  CreateCellFn createCell, TransformCellFn transformCell, int *lastColumn) {
    *rowNewHeight = rowOldHeight;
    for (int i = 0; i < cellCount; i++) {
        Cell *cellNew = createCell(rowOldCells[i]->columnIndex, rowOldCells[i]->cellType);
        if (cellNew != NULL) transformCell(rowOldCells[i], cellNew);
    }
    if (cellCount > *lastColumn) *lastColumn = cellCount;
}
""",
"csharp": r"""using System;
using System.Collections;
using System.Collections.Generic;

public class Cell
{
    public int ColumnIndex { get; }
    public int CellType { get; }
    public Cell(int columnIndex, int cellType) { ColumnIndex = columnIndex; CellType = cellType; }
}

public class HSSFRow : IEnumerable<Cell>
{
    private readonly List<Cell> _cells = new List<Cell>();
    public int Height { get; set; }
    public int LastCellNum { get { return _cells.Count; } }
    public void Add(Cell cell) { _cells.Add(cell); }
    public IEnumerator<Cell> GetEnumerator() { return _cells.GetEnumerator(); }
    IEnumerator IEnumerable.GetEnumerator() { return GetEnumerator(); }
}

public class XSSFRow
{
    public int Height { get; set; }
    public Cell CreateCell(int index, int type) { return new Cell(index, type); }
}

private void Transform(HSSFWorkbook workbookOld, XSSFWorkbook workbookNew, HSSFRow rowOld, XSSFRow rowNew)
{
    XSSFCell cellNew;
    rowNew.Height = rowOld.Height;
    foreach (Cell cell in rowOld)
    {
        cellNew = rowNew.CreateCell(cell.ColumnIndex, cell.CellType);
        if (cellNew != null) this.Transform(workbookOld, workbookNew, (HSSFCell)cell, cellNew);
    }
    this.lastColumn = Math.Max(this.lastColumn, rowOld.LastCellNum);
}
""",
}},
"T477": {"outputs": {
"python": r"""import math
import random

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
""",
"c": r"""#include <math.h>
#include <stdlib.h>

float getRandomNumberBetween(float numberOne, float numberTwo) {
    if (numberOne == numberTwo) {
        return 0.0f;
    }
    float rand = (float)((double)rand() / (double)RAND_MAX);
    float highRange = numberOne > numberTwo ? numberOne : numberTwo;
    float lowRange = numberOne < numberTwo ? numberOne : numberTwo;
    float lowRand = floorf(rand - 1.0f);
    float highRand = ceilf(rand + 1.0f);
    float genRand = (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
    return genRand;
}
""",
"csharp": r"""using System;

public static float GetRandomNumberBetween(float numberOne, float numberTwo)
{
    if (numberOne == numberTwo)
    {
        throw new Exception("Both the numbers can not be equal");
    }
    var shared = new Random();
    float rand = (float)shared.NextDouble();
    float highRange = Math.Max(numberOne, numberTwo);
    float lowRange = Math.Min(numberOne, numberTwo);
    float lowRand = (float)Math.Floor(rand - 1);
    float highRand = (float)Math.Ceiling(rand + 1);
    float genRand = (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
    return genRand;
}
""",
}},
"T842": {"outputs": {
"python": r"""EXIT_COMMAND = "exit"

def main():
    print("Enter some text, or '" + EXIT_COMMAND + "' to quit")
    while True:
        print("><![CDATA[ ", end="")
        user_input = input()
        print(user_input)
        if len(user_input) == len(EXIT_COMMAND) and user_input.lower() == EXIT_COMMAND:
            print("Exiting.")
            return
        print("...response goes here...")
""",
"c": r"""#include <stdio.h>
#include <string.h>
#include <strings.h>

#define EXIT_COMMAND "exit"

int main(void) {
    char input[1024];
    printf("Enter some text, or '%s' to quit\n", EXIT_COMMAND);
    while (1) {
        printf("><![CDATA[ ");
        if (fgets(input, sizeof(input), stdin) == NULL) break;
        input[strcspn(input, "\n")] = '\0';
        printf("%s\n", input);
        if ((int)strlen(input) == (int)strlen(EXIT_COMMAND) && strcasecmp(input, EXIT_COMMAND) == 0) {
            printf("Exiting.\n");
            return 0;
        }
        printf("...response goes here...\n");
    }
    return 0;
}
""",
"csharp": r"""using System;
using System.IO;

public static void Main(string[] args)
{
    const string EXIT_COMMAND = "exit";
    var br = new StreamReader(Console.OpenStandardInput());
    Console.WriteLine("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    while (true)
    {
        Console.Write("><![CDATA[ ");
        string input = br.ReadLine();
        Console.WriteLine(input);
        if (input.Length == EXIT_COMMAND.Length && input.ToLower().Equals(EXIT_COMMAND))
        {
            Console.WriteLine("Exiting.");
            return;
        }
        Console.WriteLine("...response goes here...");
    }
}
""",
}},
"T181": {"outputs": {
"python": r"""class Node:
    def __init__(self, key, next=None):
        self.key = key
        self.next = next

def second_max_key(first):
    if first is None or first.next is None:
        return None
    second = first.next
    if first.key > second.key:
        max_node, max_2 = first, second
    else:
        max_node, max_2 = second, first
    x = second.next
    while x is not None:
        if x.key > max_node.key:
            max_2 = max_node
            max_node = x
        elif x.key > max_2.key and x.key < max_node.key:
            max_2 = x
        x = x.next
    return max_2.key
""",
"c": r"""#include <stddef.h>

typedef struct Node {
    int key;
    struct Node *next;
} Node;

int secondMaxKey(const Node *first) {
    if (first == NULL || first->next == NULL) return 0;
    const Node *max = NULL;
    const Node *max2 = NULL;
    const Node *second = first->next;
    if (first->key > second->key) {
        max = first;
        max2 = second;
    } else {
        max = second;
        max2 = first;
    }
    for (const Node *x = second->next; x != NULL; x = x->next) {
        if (x->key > max->key) {
            max2 = max;
            max = x;
        } else if (x->key > max2->key && x->key < max->key) {
            max2 = x;
        }
    }
    return max2->key;
}
""",
"csharp": r"""public class Node
{
    public IComparable Key;
    public Node Next;
}

public Key SecondMaxKey()
{
    if (size() < 2) return null;
    Node max = null;
    Node max2 = null;
    Node second = first.Next;
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
""",
}},
}
