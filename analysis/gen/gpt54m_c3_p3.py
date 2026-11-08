DATA_T3 = {
"T501": {
"python": '''def find_min(a, c):
    return min(range(c, len(a)), key=lambda i: a[i])''',
"c": '''int findMIN(int *A, int len, int c) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}''',
"csharp": '''static int FindMin(int[] A, int c) {
    int x = A[c];
    int position = c;
    while (c < A.Length) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}'''
},
"T744": {
"python": '''import random


def t_gen():
    return random.randint(1, 10)


def tortoise_moves():
    roll = t_gen()
    if 1 <= roll <= 5:
        return 3
    if 6 <= roll <= 8:
        return 1
    if roll in (9, 10):
        return -6
    return 0''',
"c": '''#include <stdlib.h>

int tGen(void) {
    return rand() % 10 + 1;
}

int tortoiseMoves(void) {
    switch (tGen()) {
        case 1: case 2: case 3: case 4: case 5: return 3;
        case 6: case 7: case 8: return 1;
        case 9: case 10: return -6;
        default: return 0;
    }
}''',
"csharp": '''static Random random = new Random();

static int TGen() {
    return random.Next(1, 11);
}

public int TortoiseMoves() {
    switch (TGen()) {
        case 1: case 2: case 3: case 4: case 5: return 3;
        case 6: case 7: case 8: return 1;
        case 9: case 10: return -6;
        default: return 0;
    }
}'''
},
"T586": {
"python": '''def main():
    s = "harikrishna"
    s2 = ""
    for ch in s:
        if ch not in s2:
            s2 += ch
    print(s2)''',
"c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "harikrishna";
    char s2[32] = "";
    for (int i = 0; s[i]; i++) {
        if (!strchr(s2, s[i])) {
            int len = strlen(s2);
            s2[len] = s[i];
            s2[len + 1] = '\\0';
        }
    }
    printf("%s\\n", s2);
    return 0;
}''',
"csharp": '''public static void Main() {
    string s = "harikrishna";
    string s2 = "";
    foreach (char c in s) {
        if (!s2.Contains(c)) {
            s2 += c;
        }
    }
    Console.WriteLine(s2);
}'''
},
"T407": {
"python": '''def main():
    x_sum = 0
    y_sum = 0
    with open("D:/Test.txt") as br:
        for line in br:
            line = line.rstrip("\\n")
            if "x=" in line:
                x_sum += int(line.split("=")[1].strip())
            if "y=" in line:
                y_sum += int(line.split("=")[1].strip())
    print("Sum x is: " + str(x_sum) + " Sum y is: " + str(y_sum))''',
"c": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *file = fopen("D:\\\\Test.txt", "r");
    if (!file) return 1;
    char str[256];
    int xSum = 0, ySum = 0;
    while (fgets(str, sizeof(str), file)) {
        char *eq;
        if ((eq = strstr(str, "x=")) != NULL) xSum += atoi(eq + 2);
        if ((eq = strstr(str, "y=")) != NULL) ySum += atoi(eq + 2);
    }
    fclose(file);
    printf("Sum x is: %d Sum y is: %d\\n", xSum, ySum);
    return 0;
}''',
"csharp": '''public static void Main(string[] args) {
    using (StreamReader br = new StreamReader("D:\\\\Test.txt")) {
        string str;
        int xSum = 0, ySum = 0;
        while ((str = br.ReadLine()) != null) {
            if (str.Contains("x=")) xSum += int.Parse(str.Split('=')[1].Trim());
            if (str.Contains("y=")) ySum += int.Parse(str.Split('=')[1].Trim());
        }
        Console.WriteLine("Sum x is: " + xSum + " Sum y is: " + ySum);
    }
}'''
},
"T883": {
"python": '''class Cell:
    def __init__(self, index, cell_type):
        self.column_index = index
        self.cell_type = cell_type
        self.value = ""


class Row:
    def __init__(self):
        self.cells = []
        self.height = 0
        self.last_cell_num = 0

    def __iter__(self):
        return iter(self.cells)

    def create_cell(self, index, cell_type):
        cell = Cell(index, cell_type)
        self.cells.append(cell)
        return cell


class Transformer:
    def __init__(self):
        self.last_column = 0

    def transform_row(self, workbook_old, workbook_new, row_old, row_new):
        row_new.height = row_old.height
        for cell in row_old:
            cell_new = row_new.create_cell(cell.column_index, cell.cell_type)
            if cell_new is not None:
                self.transform_cell(workbook_old, workbook_new, cell, cell_new)
        self.last_column = max(self.last_column, row_old.last_cell_num)

    def transform_cell(self, workbook_old, workbook_new, cell_old, cell_new):
        cell_new.value = cell_old.value''',
"c": '''#include <stddef.h>

typedef struct {
    int index;
    int type;
    int value;
} Cell;

typedef struct {
    Cell cells[64];
    int cellCount;
    int height;
    int lastCellNum;
} Row;

typedef struct {
    int lastColumn;
} WorkbookState;

void transformCell(WorkbookState *state, Cell *cellOld, Cell *cellNew) {
    cellNew->value = cellOld->value;
}

void transformRow(WorkbookState *state, Row *rowOld, Row *rowNew) {
    rowNew->height = rowOld->height;
    rowNew->cellCount = 0;
    for (int i = 0; i < rowOld->cellCount; i++) {
        Cell *cellNew = &rowNew->cells[rowNew->cellCount++];
        cellNew->index = rowOld->cells[i].index;
        cellNew->type = rowOld->cells[i].type;
        transformCell(state, &rowOld->cells[i], cellNew);
    }
    if (rowOld->lastCellNum > state->lastColumn) state->lastColumn = rowOld->lastCellNum;
}''',
"csharp": '''public class Cell {
    public int ColumnIndex;
    public int CellType;
    public string Value;
}

public class Row {
    public List<Cell> Cells = new List<Cell>();
    public int Height;
    public int LastCellNum;

    public Cell CreateCell(int index, int type) {
        var c = new Cell { ColumnIndex = index, CellType = type };
        Cells.Add(c);
        return c;
    }
}

public class WorkbookTransformer {
    private int lastColumn;

    public void Transform(Row rowOld, Row rowNew) {
        rowNew.Height = rowOld.Height;
        foreach (Cell cell in rowOld.Cells) {
            Cell cellNew = rowNew.CreateCell(cell.ColumnIndex, cell.CellType);
            if (cellNew != null) CopyCell(cell, cellNew);
        }
        lastColumn = Math.Max(lastColumn, rowOld.LastCellNum);
    }

    private void CopyCell(Cell cellOld, Cell cellNew) {
        cellNew.Value = cellOld.Value;
    }
}'''
},
"T477": {
"python": '''import math
import random


def get_random_number_between(number_one, number_two):
    if number_one == number_two:
        raise ValueError("Both the numbers can not be equal")
    rand = random.random()
    high_range = max(number_one, number_two)
    low_range = min(number_one, number_two)
    low_rand = math.floor(rand - 1)
    high_rand = math.ceil(rand + 1)
    return (high_range - low_range) * ((rand - low_rand) / (high_rand - low_rand)) + low_range''',
"c": '''#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double getRandomNumberBetween(double numberOne, double numberTwo) {
    if (numberOne == numberTwo) {
        fprintf(stderr, "Both the numbers can not be equal\\n");
        exit(EXIT_FAILURE);
    }
    double rand = (double)std_rand() / RAND_MAX;
    double highRange = numberOne > numberTwo ? numberOne : numberTwo;
    double lowRange = numberOne < numberTwo ? numberOne : numberTwo;
    double lowRand = floor(rand - 1);
    double highRand = ceil(rand + 1);
    return (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
}''',
"csharp": '''static Random random = new Random();

private static float GetRandomNumberBetween(float numberOne, float numberTwo) {
    if (numberOne == numberTwo) {
        throw new Exception("Both the numbers can not be equal");
    }
    float rand = (float)random.NextDouble();
    float highRange = Math.Max(numberOne, numberTwo);
    float lowRange = Math.Min(numberOne, numberTwo);
    float lowRand = (float)Math.Floor(rand - 1);
    float highRand = (float)Math.Ceiling(rand + 1);
    return (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
}'''
},
"T842": {
"python": '''def main():
    exit_command = "quit"
    print("Enter some text, or '" + exit_command + "' to quit")
    while True:
        inp = input("><![CDATA[ ")
        print(inp)
        if len(inp) == len(exit_command) and inp.lower() == exit_command:
            print("Exiting.")
            return
        print("...response goes here...")''',
"c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *exit_command = "quit";
    char input[256];
    printf("Enter some text, or '%s' to quit\\n", exit_command);
    while (1) {
        printf("><![CDATA[ ");
        if (!fgets(input, sizeof(input), stdin)) break;
        input[strcspn(input, "\\n")] = '\\0';
        printf("%s\\n", input);
        if (strlen(input) == strlen(exit_command) && strcasecmp(input, exit_command) == 0) {
            printf("Exiting.\\n");
            return 0;
        }
        printf("...response goes here...\\n");
    }
    return 0;
}''',
"csharp": '''public static void Main(string[] args) {
    const string EXIT_COMMAND = "quit";
    Console.WriteLine("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    while (true) {
        Console.Write("><![CDATA[ ");
        string input = Console.ReadLine();
        Console.WriteLine(input);
        if (input.Length == EXIT_COMMAND.Length && input.ToLower().Equals(EXIT_COMMAND)) {
            Console.WriteLine("Exiting.");
            return;
        }
        Console.WriteLine("...response goes here...");
    }
}'''
}
}
