# gpt-5.4-mini chunk 1 part 2: T18, T130, T686, T139, T33, T158, T445, T826, T774, T729, T126, T641, T605, T759, T723, T309
DATA2 = {}

DATA2["T18"] = {"outputs": {
"python": r'''
import threading
from datetime import datetime

class TextView:
    def __init__(self, context):
        self.context = context

class MyCount(threading.Thread):
    def __init__(self, millis, interval):
        super().__init__()
        self.millis = millis
        self.interval = interval

    def run(self):
        pass

def on_create(saved_instance_state):
    tv = TextView("main")
    fmt = "%d.%m.%Y, %H:%M"
    old_date = datetime.strptime("19.02.2018, 12:00", fmt)
    new_date = datetime.strptime("20.02.2018, 14:00", fmt)
    old_long = int(old_date.timestamp() * 1000)
    new_long = int(new_date.timestamp() * 1000)
    diff = new_long - old_long
    counter = MyCount(diff, 1000)
    counter.start()
''',
"c": r'''
#include <stdio.h>
#include <time.h>

typedef struct {
    const char *context;
} TextView;

typedef struct {
    long millis;
    long interval;
    int running;
} MyCount;

static void my_count_start(MyCount *counter) {
    counter->running = 1;
}

static long parse_time(const char *text) {
    struct tm tm_val = {0};
    int d, mo, y, h, mi;
    if (sscanf(text, "%d.%d.%d, %d:%d", &d, &mo, &y, &h, &mi) != 5) {
        return 0;
    }
    tm_val.tm_year = y - 1900;
    tm_val.tm_mon = mo - 1;
    tm_val.tm_mday = d;
    tm_val.tm_hour = h;
    tm_val.tm_min = mi;
    return (long)mktime(&tm_val) * 1000;
}

static void on_create(void) {
    TextView tv = {"main"};
    (void)tv;
    long old_long = parse_time("19.02.2018, 12:00");
    long new_long = parse_time("20.02.2018, 14:00");
    long diff = new_long - old_long;
    MyCount counter = {diff, 1000, 0};
    my_count_start(&counter);
}
''',
"csharp": r'''
using System;
using System.Globalization;
using System.Threading;

public class TextView {
    public string Context { get; }
    public TextView(string context) {
        Context = context;
    }
}

public class MyCount {
    private readonly long _millis;
    private readonly long _interval;
    private Timer _timer;

    public MyCount(long millis, long interval) {
        _millis = millis;
        _interval = interval;
    }

    public void Start() {
        _timer = new Timer(_ => { }, null, (int)_interval, (int)_interval);
    }
}

public static void OnCreate(object savedInstanceState) {
    TextView tv = new TextView("main");
    string format = "dd.MM.yyyy, HH:mm";
    DateTime oldDate = DateTime.ParseExact("19.02.2018, 12:00", format, CultureInfo.InvariantCulture);
    DateTime newDate = DateTime.ParseExact("20.02.2018, 14:00", format, CultureInfo.InvariantCulture);
    DateTime epoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
    long oldLong = (long)oldDate.ToUniversalTime().Subtract(epoch).TotalMilliseconds;
    long newLong = (long)newDate.ToUniversalTime().Subtract(epoch).TotalMilliseconds;
    long diff = newLong - oldLong;
    MyCount counter = new MyCount(diff, 1000);
    counter.Start();
}
'''
}}

DATA2["T130"] = {"outputs": {
"python": r'''
def solution(x, a):
    seen = set()
    for i, value in enumerate(a):
        if value <= x:
            seen.add(value)
        if len(seen) == x:
            return i
    return -1
''',
"c": r'''
#include <stdbool.h>

static int seen_contains(const int *seen, int n, int v) {
    for (int i = 0; i < n; i++) {
        if (seen[i] == v) return 1;
    }
    return 0;
}

int solution(int x, const int *a, int len) {
    int seen[1024];
    int n = 0;
    for (int i = 0; i < len; i++) {
        if (a[i] <= x && !seen_contains(seen, n, a[i])) {
            seen[n++] = a[i];
        }
        if (n == x) {
            return i;
        }
    }
    return -1;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static int Solution(int x, int[] a) {
    var seen = new HashSet<int>();
    for (int i = 0; i < a.Length; i++) {
        if (a[i] <= x) {
            seen.Add(a[i]);
        }
        if (seen.Count == x) {
            return i;
        }
    }
    return -1;
}
'''
}}

DATA2["T686"] = {"outputs": {
"python": r'''
class Grocery:
    def __init__(self, num_of_items):
        self.num_of_items = num_of_items
        self.items = []

    def add_item(self, item):
        if len(self.items) >= self.num_of_items:
            return False
        self.items.append(item)
        return True

    def __str__(self):
        return "[" + ", ".join(self.items) + "]"

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

typedef struct {
    int num_of_items;
    int count;
    char items[100][128];
} Grocery;

static int grocery_add_item(Grocery *g, const char *item) {
    if (g->count >= g->num_of_items) {
        return 0;
    }
    snprintf(g->items[g->count], 128, "%s", item);
    g->count++;
    return 1;
}

int main(void) {
    printf("Enter How Many Items: ");
    char line[64];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    char *end;
    int num_of_items = (int)strtol(line, &end, 10);
    if (end == line) {
        printf("Number of items you entered is invalid!");
        return 0;
    }
    Grocery grocery = {num_of_items, 0, {{0}}};
    for (int i = 0; i < num_of_items; i++) {
        printf("Enter Item %d : ", i + 1);
        char item[128];
        if (!fgets(item, sizeof(item), stdin)) return 0;
        item[strcspn(item, "\n")] = '\0';
        if (!grocery_add_item(&grocery, item)) {
            printf("First Item Duplicate Detected!\n");
            return 0;
        }
    }
    printf("[");
    for (int i = 0; i < grocery.count; i++) {
        printf("%s%s", grocery.items[i], i + 1 < grocery.count ? ", " : "");
    }
    printf("]\n");
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public class Grocery {
    private readonly int _numOfItems;
    private readonly List<string> _items = new List<string>();

    public Grocery(int numOfItems) {
        _numOfItems = numOfItems;
    }

    public bool AddItem(string item) {
        if (_items.Count >= _numOfItems) {
            return false;
        }
        _items.Add(item);
        return true;
    }

    public override string ToString() {
        return "[" + string.Join(", ", _items) + "]";
    }
}

public static void Main() {
    Console.Write("Enter How Many Items: ");
    int numOfItems;
    try {
        numOfItems = int.Parse(Console.ReadLine().Trim());
    } catch (FormatException) {
        Console.Write("Number of items you entered is invalid!");
        return;
    }
    Grocery grocery = new Grocery(numOfItems);
    for (int i = 0; i < numOfItems; i++) {
        Console.Write("Enter Item " + (i + 1) + " : ");
        if (!grocery.AddItem(Console.ReadLine())) {
            Console.WriteLine("First Item Duplicate Detected!");
            return;
        }
    }
    Console.WriteLine(grocery);
}
'''
}}

DATA2["T139"] = {"outputs": {
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
#include <stdbool.h>
#include <stdlib.h>

int solution(int x, const int *a, int len) {
    bool *present = calloc(x + 1, sizeof(bool));
    int remaining = x;
    for (int i = 0; i < len; i++) {
        if (a[i] >= 1 && a[i] <= x && present[a[i]]) {
            present[a[i]] = false;
            remaining--;
        }
        if (remaining == 0) {
            free(present);
            return i;
        }
    }
    free(present);
    return -1;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static int Solution(int x, int[] a) {
    var emptyPosition = new HashSet<int>();
    for (int i = 1; i <= x; i++) {
        emptyPosition.Add(i);
    }
    for (int i = 0; i < a.Length; i++) {
        emptyPosition.Remove(a[i]);
        if (emptyPosition.Count == 0) {
            return i;
        }
    }
    return -1;
}
'''
}}

DATA2["T33"] = {"outputs": {
"python": r'''
def get_rows(i, j, array):
    another = [None] * (j - i + 1)
    while i <= j:
        for k in range(len(another)):
            another[k] = array[i]
            i += 1
    return another
''',
"c": r'''
#include <stdlib.h>

int *get_rows(int i, int j, int **array, int *out_len) {
    int n = j - i + 1;
    int *another = malloc((n > 0 ? n : 1) * sizeof(int));
    while (i <= j) {
        for (int k = 0; k < n; k++) {
            another[k] = *array[i];
            i++;
        }
    }
    *out_len = n;
    return another;
}
''',
"csharp": r'''
public static int[][] GetRows(int i, int j, int[][] array) {
    int[][] another = new int[j - i + 1][];
    while (i <= j) {
        for (int k = 0; k < another.Length; k++) {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
'''
}}

DATA2["T158"] = {"outputs": {
"python": r'''
def solution(x, a):
    empty_position = {i for i in range(1, x + 1)}
    for i in range(len(a)):
        empty_position -= {a[i]}
        if len(empty_position) == 0:
            return i
    return -1
''',
"c": r'''
#include <stdbool.h>
#include <stdlib.h>

int solution(int x, const int *a, int len) {
    bool *removed = calloc(x + 2, sizeof(bool));
    int remaining = x;
    int i = 0;
    while (i < len) {
        int value = a[i];
        if (value >= 1 && value <= x && !removed[value]) {
            removed[value] = true;
            remaining--;
        }
        if (remaining == 0) {
            free(removed);
            return i;
        }
        i++;
    }
    free(removed);
    return -1;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

public static int Solution(int x, int[] a) {
    var emptyPosition = new HashSet<int>(Enumerable.Range(1, x));
    int index = 0;
    foreach (int value in a) {
        emptyPosition.Remove(value);
        if (emptyPosition.Count == 0) {
            return index;
        }
        index++;
    }
    return -1;
}
'''
}}

DATA2["T445"] = {"outputs": {
"python": r'''
PRIMES = {
    'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19,
    'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53,
    'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89,
    'y': 97, 'z': 101
}

def is_anagram(word, anagram_word):
    if len(word) != len(anagram_word):
        return False
    words_char_num = 1
    anagram_word_num = 1
    for ch in word:
        words_char_num *= PRIMES[ch]
    for ch in anagram_word:
        anagram_word_num *= PRIMES[ch]
    return anagram_word_num == words_char_num
''',
"c": r'''
#include <string.h>

static int word_prime_map(char c) {
    static const int primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                                 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                                 89, 97, 101};
    if (c >= 'a' && c <= 'z') return primes[c - 'a'];
    if (c >= 'A' && c <= 'Z') return primes[c - 'A'];
    return 1;
}

static int is_anagram(const char *word, const char *anagram_word) {
    if (strlen(word) != strlen(anagram_word)) {
        return 0;
    }
    long long words_char_num = 1;
    long long anagram_word_num = 1;
    for (const char *p = word; *p; p++) {
        words_char_num *= word_prime_map(*p);
    }
    for (const char *p = anagram_word; *p; p++) {
        anagram_word_num *= word_prime_map(*p);
    }
    return anagram_word_num == words_char_num;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static Boolean IsAnagram(String word, String anagram_word) {
    if (word.Length != anagram_word.Length) {
        return false;
    }
    var wordPrimeMap = new Dictionary<char, int> {
        ['a'] = 2, ['b'] = 3, ['c'] = 5, ['d'] = 7, ['e'] = 11, ['f'] = 13,
        ['g'] = 17, ['h'] = 19, ['i'] = 23, ['j'] = 29, ['k'] = 31, ['l'] = 37,
        ['m'] = 41, ['n'] = 43, ['o'] = 47, ['p'] = 53, ['q'] = 59, ['r'] = 61,
        ['s'] = 67, ['t'] = 71, ['u'] = 73, ['v'] = 79, ['w'] = 83, ['x'] = 89,
        ['y'] = 97, ['z'] = 101
    };
    int wordsCharNum = 1;
    int anagramWordNum = 1;
    foreach (char c in word) {
        wordsCharNum *= wordPrimeMap[c];
    }
    foreach (char c in anagram_word) {
        anagramWordNum *= wordPrimeMap[c];
    }
    return anagramWordNum == wordsCharNum;
}
'''
}}

DATA2["T826"] = {"outputs": {
"python": r'''
import subprocess
import sys

def main():
    command = [sys.argv[1]]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.rstrip("\n"))
    process.wait()
    print("Program terminated!")

main()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s command\n", argv[0]);
        return 1;
    }
    FILE *pipe = popen(argv[1], "r");
    if (pipe == NULL) {
        perror("popen failed");
        return 1;
    }
    char line[1024];
    while (fgets(line, sizeof(line), pipe) != NULL) {
        printf("%s", line);
    }
    pclose(pipe);
    printf("Program terminated!\n");
    return 0;
}
''',
"csharp": r'''
using System;
using System.Diagnostics;

public static void Main(string[] args) {
    var builder = new ProcessStartInfo {
        FileName = args[0],
        UseShellExecute = false,
        RedirectStandardOutput = true
    };
    using (Process process = Process.Start(builder)) {
        string line;
        while ((line = process.StandardOutput.ReadLine()) != null) {
            Console.WriteLine(line);
        }
        process.WaitForExit();
    }
    Console.WriteLine("Program terminated!");
}
'''
}}

DATA2["T774"] = {"outputs": {
"python": r'''
def main():
    password = "admin"
    test = input("Insert the admin pass: ")
    if test == password:
        print("Access granted", end="")
    else:
        for i in range(1, 3):
            print(f"You have {i} try(es): ", end="")
            test = input()
            if test == password:
                print("Access granted", end="")
                break
            elif i == 2:
                print("Access denied", end="")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *pass = "admin";
    char test[256];
    printf("Insert the admin pass: ");
    if (!fgets(test, sizeof(test), stdin)) return 0;
    test[strcspn(test, "\n")] = '\0';
    if (strcmp(pass, test) == 0) {
        printf("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            printf("You have %d try(es): ", i);
            if (!fgets(test, sizeof(test), stdin)) return 0;
            test[strcspn(test, "\n")] = '\0';
            if (strcmp(pass, test) == 0) {
                printf("Access granted");
                break;
            } else if (i == 2) {
                printf("Access denied");
            }
        }
    }
    return 0;
}
''',
"csharp": r'''
using System;

public static void Main() {
    string pass = "admin";
    Console.Write("Insert the admin pass: ");
    string test = Console.ReadLine();
    if (pass == test) {
        Console.Write("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            Console.Write("You have " + i + " try(es): ");
            test = Console.ReadLine();
            if (pass == test) {
                Console.Write("Access granted");
                break;
            } else if (i == 2) {
                Console.Write("Access denied");
            }
        }
    }
}
'''
}}

DATA2["T729"] = {"outputs": {
"python": r'''
CHARACTER_MAPPING = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

def minimum(values):
    return min(values)

def solution(s, p, q):
    integer_input = [CHARACTER_MAPPING[ch] for ch in s]
    result = [0] * len(p)
    for index in range(len(p)):
        if p[index] == q[index]:
            result[index] = integer_input[p[index]]
            break
        result[index] = minimum(integer_input[p[index]:q[index] + 1])
    return result
''',
"c": r'''
#include <stdlib.h>

static const int character_mapping[256] = {['A'] = 1, ['C'] = 2, ['G'] = 3, ['T'] = 4};

static int find_min(const int *a, int from, int to) {
    int m = a[from];
    for (int i = from + 1; i <= to; i++) {
        if (a[i] < m) {
            m = a[i];
        }
    }
    return m;
}

int *solution(const char *s, const int *p, const int *q, int n) {
    int len = 0;
    while (s[len] != '\0') len++;
    int *integer_input = malloc(len * sizeof(int));
    for (int i = 0; i < len; i++) {
        integer_input[i] = character_mapping[(unsigned char)s[i]];
    }
    int *result = calloc(n, sizeof(int));
    for (int index = 0; index < n; index++) {
        if (p[index] == q[index]) {
            result[index] = integer_input[p[index]];
            break;
        }
        result[index] = find_min(integer_input, p[index], q[index]);
    }
    free(integer_input);
    return result;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

private static readonly Dictionary<char, int> CharacterMapping = new Dictionary<char, int> {
    ['A'] = 1, ['C'] = 2, ['G'] = 3, ['T'] = 4
};

public static int[] Solution(string s, int[] p, int[] q) {
    int[] integerInput = s.Select(c => CharacterMapping[c]).ToArray();
    int[] result = new int[p.Length];
    for (int index = 0; index < p.Length; index++) {
        if (p[index] == q[index]) {
            result[index] = integerInput[p[index]];
            break;
        }
        result[index] = integerInput.Skip(p[index]).Take(q[index] - p[index] + 1).Min();
    }
    return result;
}
'''
}}

DATA2["T126"] = {"outputs": {
"python": r'''
def solution(x, a):
    leaves = set()
    for i, value in enumerate(a):
        leaves.add(value)
        if x in leaves and len(leaves) == x:
            return i
    return -1
''',
"c": r'''
#include <stdbool.h>

static int leaves_contains(const int *leaves, int n, int v) {
    for (int i = 0; i < n; i++) {
        if (leaves[i] == v) return 1;
    }
    return 0;
}

int solution(int x, const int *a, int len) {
    int leaves[1024];
    int n = 0;
    for (int i = 0; i < len; i++) {
        if (!leaves_contains(leaves, n, a[i])) {
            leaves[n++] = a[i];
        }
        if (leaves_contains(leaves, n, x) && n == x) {
            return i;
        }
    }
    return -1;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static int Solution(int x, int[] a) {
    var leaves = new HashSet<int>();
    for (int i = 0; i < a.Length; i++) {
        leaves.Add(a[i]);
        if (leaves.Contains(x) && leaves.Count == x) {
            return i;
        }
    }
    return -1;
}
'''
}}

DATA2["T641"] = {"outputs": {
"python": r'''
class ReverseLineReader:
    def __init__(self, path):
        self._data = open(path, "rb").read()
        self._pos = len(self._data)
        self._last_pos_in_file = len(self._data)
        self._current_line_start = 0
        self._current_line_end = 0
        self._last_char = "\0"

    def find_prev_line(self):
        while self._pos > 0:
            self._pos -= 1
            ch = chr(self._data[self._pos])
            if ch == "\n":
                self._current_line_start = self._pos + 1
                self._current_line_end = self._pos
                self._last_char = ch
                return
        self._current_line_start = 0
        self._current_line_end = 0

    def read(self):
        if self._pos < self._current_line_end:
            b = self._data[self._pos]
            self._pos += 1
            return b
        elif self._pos > self._last_pos_in_file and self._current_line_start < self._current_line_end:
            self.find_prev_line()
            if self._last_char not in ("\n", "\r"):
                return "\n"
            return self.read()
        elif self._pos < 0:
            return -1
        else:
            self.find_prev_line()
            return self.read()
''',
"c": r'''
#include <stdio.h>

typedef struct {
    FILE *file;
    long pos;
    long last_pos_in_file;
    long current_line_start;
    long current_line_end;
    int last_char;
} ReverseLineReader;

static void reverse_reader_init(ReverseLineReader *r, const char *path) {
    r->file = fopen(path, "rb");
    fseek(r->file, 0, SEEK_END);
    r->last_pos_in_file = ftell(r->file);
    r->pos = r->last_pos_in_file;
    r->current_line_start = 0;
    r->current_line_end = 0;
    r->last_char = '\0';
}

static void find_prev_line(ReverseLineReader *r) {
    while (r->pos > 0) {
        r->pos--;
        fseek(r->file, r->pos, SEEK_SET);
        int ch = fgetc(r->file);
        if (ch == '\n') {
            r->current_line_start = r->pos + 1;
            r->current_line_end = r->pos;
            r->last_char = ch;
            return;
        }
    }
    r->current_line_start = 0;
    r->current_line_end = 0;
}

static int reverse_reader_read(ReverseLineReader *r) {
    if (r->pos < r->current_line_end) {
        fseek(r->file, r->pos++, SEEK_SET);
        return fgetc(r->file);
    } else if (r->pos > r->last_pos_in_file && r->current_line_start < r->current_line_end) {
        find_prev_line(r);
        if (r->last_char != '\n' && r->last_char != '\r') {
            return '\n';
        }
        return reverse_reader_read(r);
    } else if (r->pos < 0) {
        return -1;
    } else {
        find_prev_line(r);
        return reverse_reader_read(r);
    }
}
''',
"csharp": r'''
using System.IO;

public class ReverseLineReader {
    private readonly FileStream _in;
    private long _currentPos;
    private long _currentLineStart;
    private long _currentLineEnd;
    private long _lastPosInFile;
    private int _lastChar;

    public ReverseLineReader(string path) {
        _in = new FileStream(path, FileMode.Open, FileAccess.Read);
        _lastPosInFile = _in.Length;
        _currentPos = _lastPosInFile;
        _currentLineStart = 0;
        _currentLineEnd = 0;
        _lastChar = '\0';
    }

    private void FindPrevLine() {
        while (_currentPos > 0) {
            _currentPos--;
            _in.Seek(_currentPos, SeekOrigin.Begin);
            int ch = _in.ReadByte();
            if (ch == '\n') {
                _currentLineStart = _currentPos + 1;
                _currentLineEnd = _currentPos;
                _lastChar = ch;
                return;
            }
        }
        _currentLineStart = 0;
        _currentLineEnd = 0;
    }

    public int Read() {
        if (_currentPos < _currentLineEnd) {
            _in.Seek(_currentPos++, SeekOrigin.Begin);
            return _in.ReadByte();
        } else if (_currentPos > _lastPosInFile && _currentLineStart < _currentLineEnd) {
            FindPrevLine();
            if (_lastChar != '\n' && _lastChar != '\r') {
                return '\n';
            }
            return Read();
        } else if (_currentPos < 0) {
            return -1;
        } else {
            FindPrevLine();
            return Read();
        }
    }
}
'''
}}

DATA2["T605"] = {"outputs": {
"python": r'''
import xml.etree.ElementTree as ET

def main():
    tree = ET.parse("family.xml")
    root = tree.getroot()
    for element in root.iter():
        current_element_name = element.tag
        if current_element_name == "dad":
            print("isStartElement: True")
            print("Element BEGIN: " + current_element_name)
        else:
            print(current_element_name)

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *fis = fopen("family.xml", "r");
    if (fis == NULL) {
        perror("fopen failed");
        return 1;
    }
    char line[1024];
    char current_element_name[256];
    while (fgets(line, sizeof(line), fis) != NULL) {
        const char *open = strchr(line, '<');
        const char *close = open != NULL ? strchr(open, '>') : NULL;
        if (open != NULL && close != NULL) {
            size_t n = (size_t)(close - open - 1);
            if (n >= sizeof(current_element_name)) {
                n = sizeof(current_element_name) - 1;
            }
            memcpy(current_element_name, open + 1, n);
            current_element_name[n] = '\0';
            if (strcmp(current_element_name, "dad") == 0) {
                printf("isStartElement: true\n");
                printf("Element BEGIN: %s\n", current_element_name);
            } else {
                printf("%s\n", current_element_name);
            }
        }
    }
    fclose(fis);
    return 0;
}
''',
"csharp": r'''
using System;
using System.Xml.Linq;

public static void Main() {
    XDocument doc = XDocument.Load("family.xml");
    foreach (XElement element in doc.Descendants()) {
        string currentElementName = element.Name.ToString();
        if (currentElementName == "dad") {
            Console.WriteLine("isStartElement: true");
            Console.WriteLine("Element BEGIN: " + currentElementName);
        } else {
            Console.WriteLine(currentElementName);
        }
    }
}
'''
}}

DATA2["T759"] = {"outputs": {
"python": r'''
class Node:
    def __init__(self, parent=None):
        self.parent = parent

class Pane(Node):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.children = []

class HTMLEditor(Pane):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bar_removed = False

    def lookup(self, css_class):
        if css_class == ".tool-bar" and not self._bar_removed:
            self._bar_removed = True
            bar = Pane(self)
            self.children.append(bar)
            return bar
        return None

class Scene:
    def __init__(self, root):
        self.root = root

class Stage:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def show(self):
        pass

def start(primary_stage):
    html_editor = HTMLEditor()
    primary_stage.set_scene(Scene(html_editor))
    primary_stage.show()
    tool_bar = html_editor.lookup(".tool-bar")
    while tool_bar is not None:
        tool_bar.parent.children.remove(tool_bar)
        tool_bar = html_editor.lookup(".tool-bar")
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Pane Pane;

struct Pane {
    Pane *parent;
    Pane **children;
    int child_count;
    int bar_removed;
};

static Pane *pane_new(Pane *parent) {
    Pane *p = calloc(1, sizeof(Pane));
    p->parent = parent;
    if (parent != NULL) {
        parent->children = realloc(parent->children, (parent->child_count + 1) * sizeof(Pane *));
        parent->children[parent->child_count] = p;
        parent->child_count++;
    }
    return p;
}

static Pane *html_editor_lookup(Pane *editor, const char *css_class) {
    if (strcmp(css_class, ".tool-bar") == 0 && !editor->bar_removed) {
        editor->bar_removed = 1;
        return pane_new(editor);
    }
    return NULL;
}

static void start(void) {
    Pane *html_editor = pane_new(NULL);
    Pane *tool_bar = html_editor_lookup(html_editor, ".tool-bar");
    while (tool_bar != NULL) {
        tool_bar = html_editor_lookup(html_editor, ".tool-bar");
    }
}
''',
"csharp": r'''
using System.Collections.ObjectModel;

public class Node {
    public Node Parent { get; set; }
}

public class Pane : Node {
    public ObservableCollection<Node> Children { get; } = new ObservableCollection<Node>();
}

public class HTMLEditor : Pane {
    private bool _barRemoved;

    public Node Lookup(string cssSelector) {
        if (cssSelector == ".tool-bar" && !_barRemoved) {
            _barRemoved = true;
            var bar = new Pane { Parent = this };
            Children.Add(bar);
            return bar;
        }
        return null;
    }
}

public class Scene {
    public Scene(Node root) {
        Root = root;
    }
    public Node Root { get; }
}

public class Stage {
    public Scene Scene { get; set; }
    public void SetScene(Scene scene) {
        Scene = scene;
    }
    public void Show() { }
}

public static void Start(Stage primaryStage) {
    var htmlEditor = new HTMLEditor();
    primaryStage.SetScene(new Scene(htmlEditor));
    primaryStage.Show();
    Node toolBar = htmlEditor.Lookup(".tool-bar");
    while (toolBar != null) {
        ((Pane)toolBar.Parent).Children.Remove(toolBar);
        toolBar = htmlEditor.Lookup(".tool-bar");
    }
}
'''
}}

DATA2["T723"] = {"outputs": {
"python": r'''
def filter_words(words, text):
    for word in words:
        if word.lower() in text.lower():
            print(text)
            break
''',
"c": r'''
#include <ctype.h>
#include <stdio.h>
#include <string.h>

static void to_lower(char *s) {
    for (; *s; s++) {
        *s = (char)tolower((unsigned char)*s);
    }
}

static void filter(char **words, int word_count, const char *text) {
    char lower_text[1024];
    snprintf(lower_text, sizeof(lower_text), "%s", text);
    to_lower(lower_text);
    for (int i = 0; i < word_count; i++) {
        char lower_word[256];
        snprintf(lower_word, sizeof(lower_word), "%s", words[i]);
        to_lower(lower_word);
        if (strstr(lower_text, lower_word) != NULL) {
            printf("%s\n", text);
            break;
        }
    }
}
''',
"csharp": r'''
using System;

public void Filter(string[] words, string text) {
    foreach (string word in words) {
        if (text.ToLower().Contains(word.ToLower())) {
            Console.WriteLine(text);
            break;
        }
    }
}
'''
}}

DATA2["T309"] = {"outputs": {
"python": r'''
class Animal:
    def __init__(self, name):
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return self.name

Cat = Animal("Cat")
Mouse = Animal("Mouse")
Dog = Animal("Dog")
Horse = Animal("Horse")
Tiger = Animal("Tiger")
Lion = Animal("Lion")

def main():
    list1 = [Cat, Mouse, Dog]
    list2 = [Dog, Mouse, Cat]
    list3 = [Dog, Horse, Cat]
    list4 = [Dog, Tiger, Lion]
    lists = [list1, list2, list3, list4]
    seen = set()
    for animals in lists:
        ordered = tuple(sorted(animals))
        if ordered not in seen:
            seen.add(ordered)
            print(list(ordered))

main()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *animal_names[4][3] = {
    {"Cat", "Mouse", "Dog"},
    {"Dog", "Mouse", "Cat"},
    {"Dog", "Horse", "Cat"},
    {"Dog", "Tiger", "Lion"}
};

static int cmp_str(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

int main(void) {
    const char *printed[4][3];
    int printed_count = 0;
    for (int i = 0; i < 4; i++) {
        qsort(animal_names[i], 3, sizeof(char *), cmp_str);
        int duplicate = 0;
        for (int p = 0; p < printed_count; p++) {
            if (memcmp(animal_names[i], printed[p], sizeof(animal_names[i])) == 0) {
                duplicate = 1;
                break;
            }
        }
        if (duplicate) {
            continue;
        }
        memcpy(printed[printed_count++], animal_names[i], sizeof(animal_names[i]));
        printf("[");
        for (int j = 0; j < 3; j++) {
            printf("%s%s", animal_names[i][j], j < 2 ? ", " : "");
        }
        printf("]\n");
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

public class Animal : IComparable<Animal> {
    public string Name { get; }
    public Animal(string name) {
        Name = name;
    }
    public int CompareTo(Animal other) {
        return string.Compare(Name, other.Name, StringComparison.Ordinal);
    }
    public override string ToString() {
        return Name;
    }
}

public static void Main() {
    var list1 = new LinkedList<Animal>(new[] { new Animal("Cat"), new Animal("Mouse"), new Animal("Dog") });
    var list2 = new LinkedList<Animal>(new[] { new Animal("Dog"), new Animal("Mouse"), new Animal("Cat") });
    var list3 = new LinkedList<Animal>(new[] { new Animal("Dog"), new Animal("Horse"), new Animal("Cat") });
    var list4 = new LinkedList<Animal>(new[] { new Animal("Dog"), new Animal("Tiger"), new Animal("Lion") });
    var lists = new LinkedList<LinkedList<Animal>>(new[] { list1, list2, list3, list4 });
    var sorted = new List<LinkedList<Animal>>();
    foreach (var animals in lists) {
        var arList = new List<Animal>(animals);
        arList.Sort();
        var sortedList = new LinkedList<Animal>(arList);
        if (!sorted.Any(l => l.SequenceEqual(sortedList))) {
            sorted.Add(sortedList);
        }
    }
    foreach (var animals in sorted) {
        Console.WriteLine("[" + string.Join(", ", animals) + "]");
    }
}
'''
}}
