DATA5 = {
"T216": {"outputs": {
"python": r"""def print_all(*to_print):
    for item in to_print:
        if isinstance(item, (list, tuple)):
            print(list(item))
        else:
            print(item)
""",
"c": r"""#include <stdarg.h>
#include <stdio.h>

enum Kind { KIND_INT, KIND_DOUBLE, KIND_STRING };

void printItems(int count, ...) {
    va_list args;
    va_start(args, count);
    for (int i = 0; i < count; i++) {
        int kind = va_arg(args, int);
        if (kind == KIND_INT) {
            printf("%d\n", va_arg(args, int));
        } else if (kind == KIND_DOUBLE) {
            printf("%f\n", va_arg(args, double));
        } else {
            printf("%s\n", va_arg(args, const char *));
        }
    }
    va_end(args);
}
""",
"csharp": r"""using System;

public static void Print(params object[] toPrint)
{
    foreach (object item in toPrint)
    {
        if (item is int[]) Console.WriteLine(string.Join(", ", (int[])item));
        else if (item is double[]) Console.WriteLine(string.Join(", ", (double[])item));
        else if (item is object[]) Console.WriteLine(string.Join(", ", (object[])item));
        else Console.WriteLine(item);
    }
}
""",
}},
"T156": {"outputs": {
"python": r"""def solution(X, A):
    leaves = set()
    for i, value in enumerate(A):
        leaves.add(value)
        if X in leaves and len(leaves) == X:
            return i
    return -1
""",
"c": r"""#include <stdlib.h>

int solution(int X, const int *A, int n) {
    char *leaves = calloc(X + 1, 1);
    int distinct = 0;
    int seenX = 0;
    for (int i = 0; i < n; i++) {
        int v = A[i];
        if (v >= 0 && v <= X) {
            if (!leaves[v]) {
                leaves[v] = 1;
                distinct++;
            }
            if (v == X) seenX = 1;
        }
        if (seenX && distinct == X) {
            free(leaves);
            return i;
        }
    }
    free(leaves);
    return -1;
}
""",
"csharp": r"""using System.Collections.Generic;

public int Solution(int X, int[] A)
{
    var leaves = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        leaves.Add(A[i]);
        if (leaves.Contains(X) && leaves.Count == X) return i;
    }
    return -1;
}
""",
}},
"T462": {"outputs": {
"python": r"""import random

class MyRectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class Canvas:
    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height
        self.lst_shapes = []

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def repaint(self):
        pass

    def action_performed(self, event):
        x = int(random.random() * self.get_width())
        y = int(random.random() * self.get_height())
        w = int(random.random() * (self.get_width() / 4))
        h = int(random.random() * (self.get_height() / 4))
        if x + w > self.get_width():
            x = self.get_width() - w
        if y + h > self.get_height():
            y = self.get_height() - h
        color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        self.lst_shapes.append(MyRectangle(x, y, w, h, color))
        self.repaint()
""",
"c": r"""#include <stdlib.h>

typedef struct { int x, y, width, height; int r, g, b; } MyRectangle;

static int panelWidth = 800;
static int panelHeight = 600;
static MyRectangle lstShapes[100];
static int shapeCount = 0;

void actionPerformed(void) {
    int x = (int)((double)rand() / RAND_MAX * panelWidth);
    int y = (int)((double)rand() / RAND_MAX * panelHeight);
    int width = (int)((double)rand() / RAND_MAX * (panelWidth / 4));
    int height = (int)((double)rand() / RAND_MAX * (panelHeight / 4));
    if (x + width > panelWidth) x = panelWidth - width;
    if (y + height > panelHeight) y = panelHeight - height;
    int r = (int)((double)rand() / RAND_MAX * 255);
    int g = (int)((double)rand() / RAND_MAX * 255);
    int b = (int)((double)rand() / RAND_MAX * 255);
    lstShapes[shapeCount] = (MyRectangle){x, y, width, height, r, g, b};
    shapeCount++;
}
""",
"csharp": r"""using System;
using System.Collections.Generic;
using System.Drawing;

public void ActionPerformed(EventArgs e)
{
    var rnd = new Random();
    int x = (int)(rnd.NextDouble() * GetWidth());
    int y = (int)(rnd.NextDouble() * GetHeight());
    int width = (int)(rnd.NextDouble() * (GetWidth() / 4));
    int height = (int)(rnd.NextDouble() * (GetHeight() / 4));
    if (x + width > GetWidth()) x = GetWidth() - width;
    if (y + height > GetHeight()) y = GetHeight() - height;
    var color = Color.FromArgb(rnd.Next(255), rnd.Next(255), rnd.Next(255));
    lstShapes.Add(new MyRectangle(x, y, width, height, color));
    Repaint();
}
""",
}},
"R106ccba12f": r"""public static IList ToAnonymousList (this IEnumerable enumerable) {
    var enumerator = enumerable.GetEnumerator ();
    if (! enumerator.MoveNext ())
        throw new Exception ("?? No elements??");
    var listType = typeof (List <>).MakeGenericType (enumerator.Current.GetType ());
    var returnList = (IList) Activator.CreateInstance (listType);
    do {
        returnList.Add (enumerator.Current);
    } while (enumerator.MoveNext ());
    return returnList;
}""",
"R3968bf5162": r"""public void run () {
    int i = 1;
    while (i < 50) {
        waitForState (3);
        synchronized (s) {
            if (s.getState () == 3) System.out.println ("t1 " + i);
            s.setState (1);
            i += 3;
            s.notifyAll ();
        }
    }
}

private void waitForState (int expected) {
    while (s.getState () != expected) {
        synchronized (s) {
            try {
                s.wait ();
            } catch (InterruptedException e) {
                e.printStackTrace ();
            }
        }
    }
}""",
"R3d67d34140": r"""public static void main (String [] args) {
    Scanner sc = new Scanner (System.in);
    String [] [] array = new String [7] [];
    array [0] = new String [] {"continents", "Asia", "Europe", "Africa", "Australia", "South America", "North America"};
    array [1] = new String [] {"profession", "teacher", "doctor", "lawyer"};
    array [2] = new String [] {"brand", "apple", "samsung"};
    array [3] = new String [] {"name", "lisa", "peter", "sam", "jack"};
    array [4] = new String [] {"profession", "engineer", "Professor", "Dentist", "Driver"};
    array [5] = new String [] {"sex", "value", "male", "female"};
    array [6] = new String [] {"exp", "value", "1", "2", "3", "4"};
    int index = sc.nextInt ();
    List < String [] > rows = new ArrayList < String [] > (Arrays.asList (array));
    Collections.rotate (rows, - (index - 1));
    for (String [] tempArray : rows) {
        System.out.println (String.join (" ", tempArray));
    }
}""",
"Rd41c27729f": r"""def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % k for k in range(3, int(n ** 0.5) + 1, 2))""",
}
