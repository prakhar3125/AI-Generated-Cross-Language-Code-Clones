DATA_T3 = {
"T686": {"outputs": {
"python": r'''
class Grocery:
    def __init__(self, size):
        self.size = size
        self.items = []

    def add_item(self, item):
        if len(self.items) >= self.size or item in self.items:
            return False
        self.items.append(item)
        return True

    def __str__(self):
        return "Items: " + ", ".join(self.items)


def main():
    print("Enter How Many Items: ", end="")
    try:
        num_of_items = int(input().strip())
    except ValueError:
        print("Number of items you entered is invalid!")
        return
    grocery = Grocery(num_of_items)
    for i in range(num_of_items):
        print(f"Enter Item {i + 1} : ", end="")
        if not grocery.add_item(input()):
            print("First Item Duplicate Detected!")
            return
    print(grocery)

main()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 100

static char *grocery[MAX_ITEMS];
static int grocery_count = 0;

static int add_item(const char *item) {
    if (grocery_count >= MAX_ITEMS) return 0;
    for (int i = 0; i < grocery_count; i++) {
        if (strcmp(grocery[i], item) == 0) return 0;
    }
    grocery[grocery_count] = malloc(strlen(item) + 1);
    strcpy(grocery[grocery_count], item);
    grocery_count++;
    return 1;
}

int main(void) {
    char line[256];
    int num_of_items = 0;
    printf("Enter How Many Items: ");
    if (!fgets(line, sizeof(line), stdin)) return 0;
    if (sscanf(line, "%d", &num_of_items) != 1) {
        printf("Number of items you entered is invalid!");
        return 0;
    }
    for (int i = 0; i < num_of_items; i++) {
        printf("Enter Item %d : ", i + 1);
        if (!fgets(line, sizeof(line), stdin)) return 0;
        line[strcspn(line, "\n")] = '\0';
        if (!add_item(line)) {
            printf("First Item Duplicate Detected!\n");
            return 0;
        }
    }
    printf("Items:");
    for (int i = 0; i < grocery_count; i++) printf(" %s", grocery[i]);
    printf("\n");
    for (int i = 0; i < grocery_count; i++) free(grocery[i]);
    return 0;
}
''',
"csharp": r'''
public class Grocery
{
    private readonly int _size;
    private readonly List<string> _items = new List<string>();

    public Grocery(int size) { _size = size; }

    public bool AddItem(string item)
    {
        if (_items.Count >= _size || _items.Contains(item)) return false;
        _items.Add(item);
        return true;
    }

    public override string ToString() { return "Items: " + string.Join(", ", _items); }
}

public static void Main(string[] args)
{
    Console.Write("Enter How Many Items: ");
    int numOfItems;
    try
    {
        numOfItems = int.Parse(Console.ReadLine().Trim());
    }
    catch (FormatException)
    {
        Console.Write("Number of items you entered is invalid!");
        return;
    }
    var grocery = new Grocery(numOfItems);
    for (int i = 0; i < numOfItems; i++)
    {
        Console.Write("Enter Item " + (i + 1) + " : ");
        if (!grocery.AddItem(Console.ReadLine()))
        {
            Console.WriteLine("First Item Duplicate Detected!");
            return;
        }
    }
    Console.WriteLine(grocery.ToString());
}
'''}},
"T139": {"outputs": {
"python": r'''
def solution(x, a):
    empty_position = set(range(1, x + 1))
    for i, value in enumerate(a):
        empty_position.discard(value)
        if not empty_position:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, int A[], int len) {
    int *remaining = malloc(((size_t)X + 1) * sizeof(int));
    for (int i = 1; i <= X; i++) remaining[i] = 1;
    int count = X;
    for (int i = 0; i < len; i++) {
        if (A[i] >= 1 && A[i] <= X && remaining[A[i]]) {
            remaining[A[i]] = 0;
            count--;
        }
        if (count == 0) {
            free(remaining);
            return i;
        }
    }
    free(remaining);
    return -1;
}
''',
"csharp": r'''
public int Solution(int X, int[] A)
{
    var emptyPosition = new HashSet<int>(Enumerable.Range(1, X));
    for (int i = 0; i < A.Length; i++)
    {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0) return i;
    }
    return -1;
}
'''}},
"T247": {"outputs": {
"python": r'''
def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i, count in enumerate(ar):
        if count > 0:
            print(chr(i) if count == 1 else f"{chr(i)}{count}", end="")

main()
''',
"c": r'''
#include <stdio.h>

int main(void) {
    char st[1024];
    int ar[256] = {0};
    printf("Enter the String");
    if (!fgets(st, sizeof(st), stdin)) return 0;
    for (const char *p = st; *p && *p != '\n'; p++) {
        ar[(unsigned char)*p]++;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 1) {
            printf("%c%d", (char)i, ar[i]);
        } else if (ar[i] == 1) {
            printf("%c", (char)i);
        }
    }
    return 0;
}
''',
"csharp": r'''
public static void Main(string... a)
{
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    var ar = new int[256];
    foreach (char ch in st)
    {
        ar[ch] = ar[ch] + 1;
    }
    var sb = new StringBuilder();
    for (int i = 0; i < 256; i++)
    {
        if (ar[i] > 0)
        {
            sb.Append((char)i);
            if (ar[i] > 1) sb.Append(ar[i]);
        }
    }
    Console.Write(sb.ToString());
}
'''}},
"T33": {"outputs": {
"python": r'''
def get_rows(i, j, array):
    another = [None] * (j - i + 1)
    for k in range(len(another)):
        another[k] = array[i + k]
    return another
''',
"c": r'''
#include <stdlib.h>

int **get_rows(int i, int j, int **array) {
    int rows = j - i + 1;
    int **another = malloc((size_t)rows * sizeof(int *));
    for (int k = 0; k < rows; k++) {
        another[k] = array[i + k];
    }
    return another;
}
''',
"csharp": r'''
public static int[][] GetRows(int i, int j, int[][] array)
{
    int[][] another = new int[j - i + 1][];
    int index = 0;
    while (i <= j)
    {
        for (int k = 0; k < another.Length; k++)
        {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
'''}},
"T158": {"outputs": {
"python": r'''
def solution(x, a):
    empty_position = set(range(1, x + 1))
    for i in range(len(a)):
        empty_position -= {a[i]}
        if len(empty_position) == 0:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, const int A[], int len) {
    int *pending = malloc(((size_t)X + 1) * sizeof(int));
    for (int i = 1; i <= X; i++) pending[i] = 1;
    int remaining = X;
    int time = -1;
    for (int i = 0; i < len; i++) {
        if (A[i] >= 1 && A[i] <= X && pending[A[i]]) {
            pending[A[i]] = 0;
            remaining--;
        }
        if (remaining == 0) {
            time = i;
            break;
        }
    }
    free(pending);
    return time;
}
''',
"csharp": r'''
public int Solution(int X, int[] A)
{
    var emptyPosition = new HashSet<int>();
    for (int i = 1; i <= X; i++) emptyPosition.Add(i);
    for (int i = 0; i < A.Length; i++)
    {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0) return i;
    }
    return -1;
}
'''}},
}
