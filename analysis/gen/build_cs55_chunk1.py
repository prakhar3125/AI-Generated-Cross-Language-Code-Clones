import ast
import json
import os

BASE = r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen"
SEED = os.path.join(BASE, "seeds", "chunk1.json")
OUT = os.path.join(BASE, "out", "claude-sonnet-5-5_chunk1.json")

R = {}

# ===ENTRIES===

R["T234"] = dict(
python=r'''
def count_duplicates(text):
    counts = {}
    for val in text:
        counts[val] = counts.get(val, 0) + 1
    return counts

def main():
    name = "AnuvratAnuvra"
    for key, value in sorted(count_duplicates(name).items()):
        if value > 1:
            print(str(key) + ":" + str(value))

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

void printDuplicates(const char *name) {
    int counts[256] = {0};
    for (size_t i = 0; i < strlen(name); i++) {
        counts[(unsigned char)name[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 1) {
            printf("%c:%d\n", (char)i, counts[i]);
        }
    }
}

int main(void) {
    printDuplicates("AnuvratAnuvra");
    return 0;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class Program
{
    public static void Main(string[] args)
    {
        string name = "AnuvratAnuvra";
        var counts = new Dictionary<char, int>();
        foreach (char val in name)
        {
            if (counts.ContainsKey(val)) counts[val] = counts[val] + 1;
            else counts[val] = 1;
        }
        foreach (KeyValuePair<char, int> entry in counts)
        {
            if (entry.Value > 1)
            {
                Console.WriteLine(entry.Key + ":" + entry.Value);
            }
        }
    }
}
''')

R["T240"] = dict(
python=r'''
def main():
    st = input("Enter the String")
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(str(ch) + str(ar[i]), end="")

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    printf("Enter the String");
    if (!fgets(st, sizeof st, stdin)) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    for (size_t i = 0; i < strlen(st); i++) {
        ar[(unsigned char)st[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", (char)i);
            } else {
                printf("%c%d", (char)i, ar[i]);
            }
        }
    }
    return 0;
}
''',
csharp=r'''
using System;

public class Program
{
    public static void Main(string[] a)
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        foreach (char c in st)
        {
            ar[c]++;
        }
        for (int i = 0; i < 256; i++)
        {
            char ch = (char)i;
            if (ar[i] > 0)
            {
                if (ar[i] == 1)
                {
                    Console.Write(ch);
                }
                else
                {
                    Console.Write(ch + "" + ar[i]);
                }
            }
        }
    }
}
''')

R["T365"] = dict(
python=r'''
import random

symbols = "!@#$%^&*()-_=+[]{};:,.<>?/|abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def shuffle(text):
    chars = list(text)
    random.shuffle(chars)
    return "".join(chars)

def generate_random_password(length):
    if length < 1:
        raise ValueError("length must be greater than 0")
    buf = [symbols[random.randrange(len(symbols))] for _ in range(length)]
    return shuffle("".join(buf))
''',
c=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *symbols = "!@#$%^&*()-_=+abcdefghijklmnopqrstuvwxyz";

static void shuffle(char *text) {
    int n = (int)strlen(text);
    for (int i = 0; i < n; i++) {
        int j = rand() % n;
        char tmp = text[i];
        text[i] = text[j];
        text[j] = tmp;
    }
}

char *generateRandomPassword(int length) {
    if (length < 1) {
        fprintf(stderr, "length must be greater than 0\n");
        exit(1);
    }
    char *buf = malloc((size_t)length + 1);
    int n = (int)strlen(symbols);
    for (int idx = 0; idx < length; ++idx) {
        buf[idx] = symbols[rand() % n];
    }
    buf[length] = '\0';
    shuffle(buf);
    return buf;
}
''',
csharp=r'''
using System;
using System.Text;

public class PasswordGenerator
{
    private static readonly Random RANDOM = new Random();
    private static readonly char[] symbols = "!@#$%^&*()-_=+abcdefABCDEF0123456789".ToCharArray();

    private static string Shuffle(string text)
    {
        char[] characters = text.ToCharArray();
        for (int i = 0; i < characters.Length; i++)
        {
            int randomIndex = RANDOM.Next(characters.Length);
            char temp = characters[i];
            characters[i] = characters[randomIndex];
            characters[randomIndex] = temp;
        }
        return new string(characters);
    }

    public string GenerateRandomPassword(int length)
    {
        if (length < 1)
        {
            throw new ArgumentException("length must be greater than 0");
        }
        char[] buf = new char[length];
        for (int idx = 0; idx < buf.Length; ++idx)
        {
            buf[idx] = symbols[RANDOM.Next(symbols.Length)];
        }
        return Shuffle(new string(buf));
    }
}
''')

R["T506"] = dict(
python=r'''
def main():
    text = input()
    arrlist = list(text)
    for ch in text:
        freq = arrlist.count(ch)
        print("Frequency of " + ch + "  is:   " + str(freq))

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char str[1024];
    if (!fgets(str, sizeof str, stdin)) return 0;
    str[strcspn(str, "\n")] = '\0';
    int len = (int)strlen(str);
    for (int i = 0; i < len; i++) {
        int freq = 0;
        for (int j = 0; j < len; j++) {
            if (str[j] == str[i]) freq++;
        }
        printf("Frequency of %c  is:   %d\n", str[i], freq);
    }
    return 0;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;
using System.Linq;

public class Program
{
    public static void Main(string[] args)
    {
        string str = Console.ReadLine();
        var arrlist = new List<char>();
        for (int i = 0; i < str.Length; i++)
        {
            arrlist.Add(str[i]);
        }
        for (int i = 0; i < str.Length; i++)
        {
            int freq = arrlist.Count(c => c == str[i]);
            Console.WriteLine("Frequency of " + str[i] + "  is:   " + freq);
        }
    }
}
''')

R["T434"] = dict(
python=r'''
import re

class Histogram:
    def __init__(self, text):
        self.text = text

    def find_in_line(self, name):
        return re.search(re.escape(name), self.text)

def valid_name(input_tokens, histogram):
    user = ""
    name = next(input_tokens)
    if histogram.find_in_line(name) is not None:
        print("This name exist")
    else:
        print("Name not found")
        user = valid_name(input_tokens, histogram)
    return user
''',
c=r'''
#include <stdio.h>
#include <string.h>

static const char *histogramText = "Alice Bob Carol";

void validName(char *user, size_t userSize) {
    char name[128];
    if (scanf("%127s", name) != 1) {
        return;
    }
    if (strstr(histogramText, name) != NULL) {
        printf("This name exist\n");
    } else {
        printf("Name not found\n");
        validName(user, userSize);
    }
}

int main(void) {
    char user[128] = "";
    validName(user, sizeof user);
    return 0;
}
''',
csharp=r'''
using System;
using System.Text.RegularExpressions;

public class NameValidator
{
    private static string ValidName(Func<string> input, string histogram)
    {
        string user = "";
        string name = input();
        if (Regex.Match(histogram, Regex.Escape(name)).Success)
        {
            Console.WriteLine("This name exist");
        }
        else
        {
            Console.WriteLine("Name not found");
            user = ValidName(input, histogram);
        }
        return user;
    }
}
''')

R["T639"] = dict(
python=r'''
from pathlib import Path
from urllib.parse import urlparse

def get_protocol(file):
    try:
        return urlparse(Path(file).absolute().as_uri()).scheme
    except Exception:
        return "unknown"
''',
c=r'''
#include <string.h>

const char *getProtocol(const char *uri) {
    const char *sep = (uri != NULL) ? strstr(uri, "://") : NULL;
    if (sep == NULL) {
        return "unknown";
    }
    static char protocol[16];
    size_t n = (size_t)(sep - uri);
    if (n >= sizeof protocol) {
        return "unknown";
    }
    memcpy(protocol, uri, n);
    protocol[n] = '\0';
    return protocol;
}
''',
csharp=r'''
using System;
using System.IO;

public class ProtocolHelper
{
    public static string GetProtocol(string path)
    {
        try
        {
            return new Uri(Path.GetFullPath(path)).Scheme;
        }
        catch (Exception)
        {
            return "unknown";
        }
    }
}
''')

R["T848"] = dict(
python=r'''
def main():
    for i in range(1, 16):
        if (i & 1) > 0:
            print("A", end="")
        if (i & 2) > 0:
            print("B", end="")
        if (i & 4) > 0:
            print("C", end="")
        if (i & 8) > 0:
            print("D", end="")
        print()

main()
''',
c=r'''
#include <stdio.h>

int main(void) {
    for (int i = 1; i < 16; ++i) {
        if ((i & 1) > 0) printf("A");
        if ((i & 2) > 0) printf("B");
        if ((i & 4) > 0) printf("C");
        if ((i & 8) > 0) printf("D");
        printf("\n");
    }
    return 0;
}
''',
csharp=r'''
using System;

public class Program
{
    public static void Main(string[] args)
    {
        for (int i = 1; i < 16; ++i)
        {
            if ((i & 1) > 0) Console.Write("A");
            if ((i & 2) > 0) Console.Write("B");
            if ((i & 4) > 0) Console.Write("C");
            if ((i & 8) > 0) Console.Write("D");
            Console.WriteLine("");
        }
    }
}
''')

R["T613"] = dict(
python=r'''
def put_in_bucket(bucket, value):
    bucket.append(value)
    return bucket

def sort(numbers, digit):
    if len(numbers) == 0 or digit <= 0:
        return numbers
    space = [[] for _ in range(10)]
    for number in numbers:
        i = (number // digit) % 10
        space[i] = put_in_bucket(space[i], number)
    result = []
    for i in range(10):
        result.extend(sort(space[i], digit // 10))
    return result
''',
c=r'''
#include <stdlib.h>
#include <string.h>

static int *putInBucket(int *bucket, int len, int value) {
    bucket = realloc(bucket, (size_t)(len + 1) * sizeof(int));
    bucket[len] = value;
    return bucket;
}

int *sort(int *numbers, int count, int digit) {
    if (count == 0 || digit <= 0) return numbers;
    int *space[10] = {0};
    int len[10] = {0};
    int j;
    for (j = 0; j < count; j++) {
        int i = (numbers[j] / digit) % 10;
        space[i] = putInBucket(space[i], len[i], numbers[j]);
        len[i]++;
    }
    int k = 0;
    for (int i = 0; i < 10; i++) {
        if (len[i] > 0) {
            int *sortedBucket = sort(space[i], len[i], digit / 10);
            memcpy(numbers + k, sortedBucket, (size_t)len[i] * sizeof(int));
            k += len[i];
        }
        free(space[i]);
    }
    return numbers;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class RadixSorter
{
    private static List<int> PutInBucket(List<int> bucket, int value)
    {
        bucket.Add(value);
        return bucket;
    }

    public static int[] Sort(int[] numbers, int digit)
    {
        if (numbers.Length == 0 || digit <= 0) return numbers;
        var space = new List<int>[10];
        for (int b = 0; b < 10; b++)
        {
            space[b] = new List<int>();
        }
        foreach (int number in numbers)
        {
            int i = (number / digit) % 10;
            space[i] = PutInBucket(space[i], number);
        }
        var result = new List<int>();
        for (int i = 0; i < 10; i++)
        {
            result.AddRange(Sort(space[i].ToArray(), digit / 10));
        }
        return result.ToArray();
    }
}
''')

R["T18"] = dict(
python=r'''
from datetime import datetime
import threading

def on_create():
    fmt = "%d.%m.%Y, %H:%M"
    old_time = "19.02.2018, 12:00"
    new_time = "20.02.2018, 14:00"
    try:
        old_date = datetime.strptime(old_time, fmt)
        new_date = datetime.strptime(new_time, fmt)
        diff = (new_date - old_date).total_seconds()
    except ValueError:
        diff = 0
    counter = threading.Timer(diff, lambda: None)
    counter.start()

on_create()
''',
c=r'''
#include <stdio.h>
#include <time.h>

int main(void) {
    struct tm oldTm = {0}, newTm = {0};
    strptime("19.02.2018, 12:00", "%d.%m.%Y, %H:%M", &oldTm);
    strptime("20.02.2018, 14:00", "%d.%m.%Y, %H:%M", &newTm);
    time_t oldLong = mktime(&oldTm);
    time_t newLong = mktime(&newTm);
    double diff = difftime(newLong, oldLong);
    printf("elapsed: %f seconds\n", diff);
    return 0;
}
''',
csharp=r'''
using System;
using System.Globalization;
using System.Threading;

public class Program
{
    public static void Main(string[] args)
    {
        string fmt = "dd.MM.yyyy, HH:mm";
        string oldTime = "19.02.2018, 12:00";
        string newTime = "20.02.2018, 14:00";
        long diff = 0;
        try
        {
            DateTime oldDate = DateTime.ParseExact(oldTime, fmt, CultureInfo.InvariantCulture);
            DateTime newDate = DateTime.ParseExact(newTime, fmt, CultureInfo.InvariantCulture);
            diff = (long)(newDate - oldDate).TotalMilliseconds;
        }
        catch (FormatException e)
        {
            Console.WriteLine(e.StackTrace);
        }
        var counter = new Timer(_ => { }, null, diff, Timeout.Infinite);
    }
}
''')

R["T130"] = dict(
python=r'''
def solution(x, a):
    hset = set()
    for i, value in enumerate(a):
        if value <= x:
            hset.add(value)
        if len(hset) == x:
            return i
    return -1
''',
c=r'''
#include <stdlib.h>

int solution(int x, const int *a, int n) {
    char *seen = calloc((size_t)x + 1, 1);
    int distinct = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] >= 0 && a[i] <= x && !seen[a[i]]) {
            seen[a[i]] = 1;
            distinct++;
        }
        if (distinct == x) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class Solution
{
    public int Solve(int x, int[] a)
    {
        var hset = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            if (a[i] <= x) hset.Add(a[i]);
            if (hset.Count == x) return i;
        }
        return -1;
    }
}
''')

R["T686"] = dict(
python=r'''
import sys

class Grocery:
    def __init__(self, num_of_items):
        self.num_of_items = num_of_items
        self.items = []

    def add_item(self, item):
        if item in self.items:
            return False
        self.items.append(item)
        return True

    def __str__(self):
        return "Grocery list: " + ", ".join(self.items)

def main():
    try:
        num_of_items = int(input("Enter How Many Items: ").strip())
    except ValueError:
        print("Number of items you entered is invalid!")
        sys.exit(0)
    grocery = Grocery(num_of_items)
    for i in range(num_of_items):
        item = input("Enter Item " + str(i + 1) + " : ")
        if not grocery.add_item(item):
            print("First Item Duplicate Detected!")
            sys.exit(0)
    print(grocery)

main()
''',
c=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 100
#define MAX_LEN 128

typedef struct {
    int numOfItems;
    char items[MAX_ITEMS][MAX_LEN];
    int count;
} Grocery;

int addItem(Grocery *g, const char *item) {
    for (int i = 0; i < g->count; i++) {
        if (strcmp(g->items[i], item) == 0) return 0;
    }
    if (g->count >= g->numOfItems) return 0;
    strncpy(g->items[g->count], item, MAX_LEN - 1);
    g->items[g->count][MAX_LEN - 1] = '\0';
    g->count++;
    return 1;
}

int main(void) {
    char line[256];
    printf("Enter How Many Items: ");
    if (!fgets(line, sizeof line, stdin)) return 0;
    int numOfItems = atoi(line);
    if (numOfItems <= 0) {
        printf("Number of items you entered is invalid!");
        exit(0);
    }
    Grocery grocery = { numOfItems, {{0}}, 0 };
    for (int i = 0; i < numOfItems; i++) {
        printf("Enter Item %d : ", i + 1);
        if (!fgets(line, sizeof line, stdin)) return 0;
        line[strcspn(line, "\n")] = '\0';
        if (!addItem(&grocery, line)) {
            printf("First Item Duplicate Detected!\n");
            exit(0);
        }
    }
    for (int i = 0; i < grocery.count; i++) {
        printf("%s ", grocery.items[i]);
    }
    printf("\n");
    return 0;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class Grocery
{
    private readonly int _numOfItems;
    private readonly List<string> _items = new List<string>();

    public Grocery(int numOfItems)
    {
        _numOfItems = numOfItems;
    }

    public bool AddItem(string item)
    {
        if (_items.Contains(item)) return false;
        if (_items.Count >= _numOfItems) return false;
        _items.Add(item);
        return true;
    }

    public override string ToString()
    {
        return "Grocery list: " + string.Join(", ", _items);
    }
}

public class Program
{
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
            Environment.Exit(0);
            return;
        }
        var grocery = new Grocery(numOfItems);
        for (int i = 0; i < numOfItems; i++)
        {
            Console.Write("Enter Item " + (i + 1) + " : ");
            if (!grocery.AddItem(Console.ReadLine()))
            {
                Console.WriteLine("First Item Duplicate Detected!");
                Environment.Exit(0);
            }
        }
        Console.WriteLine(grocery.ToString());
    }
}
''')

R["T139"] = dict(
python=r'''
def solution(x, a):
    empty_position = set(range(1, x + 1))
    for i, value in enumerate(a):
        empty_position.discard(value)
        if not empty_position:
            return i
    return -1
''',
c=r'''
#include <stdlib.h>

int solution(int x, const int *a, int n) {
    char *remaining = calloc((size_t)x + 2, 1);
    int empty = x;
    for (int i = 1; i <= x; i++) {
        remaining[i] = 1;
    }
    for (int i = 0; i < n; i++) {
        if (a[i] >= 1 && a[i] <= x && remaining[a[i]]) {
            remaining[a[i]] = 0;
            empty--;
        }
        if (empty == 0) {
            free(remaining);
            return i;
        }
    }
    free(remaining);
    return -1;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class Solution2
{
    public int Solve(int x, int[] a)
    {
        var emptyPosition = new HashSet<int>();
        for (int i = 1; i <= x; i++)
        {
            emptyPosition.Add(i);
        }
        for (int i = 0; i < a.Length; i++)
        {
            emptyPosition.Remove(a[i]);
            if (emptyPosition.Count == 0)
            {
                return i;
            }
        }
        return -1;
    }
}
''')

R["T247"] = dict(
python=r'''
def main():
    st = input("Enter the String")
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] = ar[ord(ch)] + 1
    out = []
    for i in range(256):
        if ar[i] > 0:
            out.append(chr(i) if ar[i] == 1 else chr(i) + str(ar[i]))
    print("".join(out), end="")

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    printf("Enter the String");
    if (!fgets(st, sizeof st, stdin)) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    int len = (int)strlen(st);
    for (int i = 0; i < len; i++) {
        ar[(unsigned char)st[i]] = ar[(unsigned char)st[i]] + 1;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                putchar(ch);
            } else {
                printf("%c%d", ch, ar[i]);
            }
        }
    }
    return 0;
}
''',
csharp=r'''
using System;
using System.Text;

public class Program
{
    public static void Main(string[] a)
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        for (int i = 0; i < st.Length; i++)
        {
            ar[st[i]] = ar[st[i]] + 1;
        }
        var sb = new StringBuilder();
        for (int i = 0; i < 256; i++)
        {
            char ch = (char)i;
            if (ar[i] > 0)
            {
                sb.Append(ar[i] == 1 ? ch.ToString() : ch + "" + ar[i]);
            }
        }
        Console.Write(sb.ToString());
    }
}
''')

R["T33"] = dict(
python=r'''
def get_rows(i, j, array):
    another = [None] * (j - i + 1)
    while i <= j:
        for k in range(len(another)):
            another[k] = array[i]
            i += 1
    return another
''',
c=r'''
#include <stdlib.h>

int **getRows(int i, int j, int **array) {
    int rows = j - i + 1;
    int **another = malloc((size_t)rows * sizeof(int *));
    while (i <= j) {
        for (int k = 0; k < rows; k++) {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
''',
csharp=r'''
public static int[][] GetRows(int i, int j, int[][] array)
{
    int[][] another = new int[j - i + 1][];
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
''')

R["T158"] = dict(
python=r'''
def solution(x, a):
    missing = set(range(1, x + 1))
    for i, value in enumerate(a):
        missing -= {value}
        if len(missing) == 0:
            return i
    return -1
''',
c=r'''
#include <stdlib.h>

int solution(int x, const int *a, int n) {
    int *present = calloc((size_t)x + 1, sizeof(int));
    int left = x;
    for (int v = 1; v <= x; v++) {
        present[v] = 1;
    }
    for (int i = 0; i < n; i++) {
        if (a[i] >= 1 && a[i] <= x && present[a[i]] == 1) {
            present[a[i]] = 0;
            left--;
        }
        if (left == 0) {
            free(present);
            return i;
        }
    }
    free(present);
    return -1;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution3
{
    public int Solve(int x, int[] a)
    {
        ISet<int> emptyPosition = new HashSet<int>(Enumerable.Range(1, x));
        for (int i = 0; i < a.Length; i++)
        {
            emptyPosition.Remove(a[i]);
            if (emptyPosition.Count == 0)
            {
                return i;
            }
        }
        return -1;
    }
}
''')

R["T445"] = dict(
python=r'''
PRIMES = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19,
          'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53,
          'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89,
          'y': 97, 'z': 101}

def word_prime_map():
    return PRIMES

def is_anagram(word, anagram_word):
    if len(word) != len(anagram_word):
        return False
    m = word_prime_map()
    words_char_num = 1
    anagram_word_num = 1
    for ch in word:
        words_char_num *= m[ch]
    for ch in anagram_word:
        anagram_word_num *= m[ch]
    return anagram_word_num == words_char_num
''',
c=r'''
#include <string.h>

static int primeForChar(char c) {
    static const int primes[26] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                                   41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                                   89, 97, 101};
    if (c >= 'a' && c <= 'z') return primes[c - 'a'];
    if (c >= 'A' && c <= 'Z') return primes[c - 'A'];
    return 1;
}

int isAnagram(const char *word, const char *anagram_word) {
    if (strlen(word) != strlen(anagram_word)) {
        return 0;
    }
    long words_char_num = 1;
    long anagram_word_num = 1;
    for (size_t i = 0; i < strlen(word); i++) {
        words_char_num *= primeForChar(word[i]);
    }
    for (size_t i = 0; i < strlen(anagram_word); i++) {
        anagram_word_num *= primeForChar(anagram_word[i]);
    }
    return anagram_word_num == words_char_num;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class AnagramChecker
{
    private static readonly Dictionary<char, int> WordPrimeMap = BuildWordPrimeMap();

    private static Dictionary<char, int> BuildWordPrimeMap()
    {
        var map = new Dictionary<char, int>();
        int[] primes = { 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                         53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101 };
        for (char c = 'a'; c <= 'z'; c++)
        {
            map[c] = primes[c - 'a'];
        }
        return map;
    }

    public static bool IsAnagram(string word, string anagram_word)
    {
        if (word.Length != anagram_word.Length)
        {
            return false;
        }
        long wordsCharNum = 1;
        long anagramWordNum = 1;
        foreach (char c in word)
        {
            wordsCharNum *= WordPrimeMap[c];
        }
        foreach (char c in anagram_word)
        {
            anagramWordNum *= WordPrimeMap[c];
        }
        return anagramWordNum == wordsCharNum;
    }
}
''')

R["T826"] = dict(
python=r'''
import subprocess
import sys

def main():
    command = [sys.argv[1]]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    print("Program terminated!")

main()
''',
c=r'''
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    FILE *pipe = popen(argv[1], "r");
    if (!pipe) return 1;
    char buffer[1024];
    while (fgets(buffer, sizeof buffer, pipe) != NULL) {
        printf("%s", buffer);
    }
    pclose(pipe);
    printf("Program terminated!\n");
    return 0;
}
''',
csharp=r'''
using System;
using System.Diagnostics;

public class Program
{
    public static void Main(string[] args)
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = args[0],
                UseShellExecute = false,
                RedirectStandardOutput = true
            }
        };
        process.Start();
        string line;
        while ((line = process.StandardOutput.ReadLine()) != null)
        {
            Console.WriteLine(line);
        }
        Console.WriteLine("Program terminated!");
    }
}
''')

R["T774"] = dict(
python=r'''
def main():
    password = "admin"
    test = input("Insert the admin pass: ")
    if test == password:
        print("Access granted", end="")
    else:
        for i in range(1, 3):
            print("You have " + str(i) + " try(es): ", end="")
            test = input()
            if test == password:
                print("Access granted", end="")
                break
            elif i == 2:
                print("Access denied", end="")

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *pass = "admin";
    char test[256];
    printf("Insert the admin pass: ");
    if (!fgets(test, sizeof test, stdin)) return 0;
    test[strcspn(test, "\n")] = '\0';
    if (strcmp(pass, test) == 0) {
        printf("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            printf("You have %d try(es): ", i);
            if (!fgets(test, sizeof test, stdin)) return 0;
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
csharp=r'''
using System;

public class Program
{
    public static void Main(string[] args)
    {
        string pass = "admin";
        Console.Write("Insert the admin pass: ");
        string test = Console.ReadLine();
        if (pass == test)
        {
            Console.Write("Access granted");
        }
        else
        {
            for (int i = 1; i < 3; i++)
            {
                Console.Write("You have " + i + " try(es): ");
                test = Console.ReadLine();
                if (pass == test)
                {
                    Console.Write("Access granted");
                    break;
                }
                else if (i == 2)
                {
                    Console.Write("Access denied");
                }
            }
        }
    }
}
''')

R["T729"] = dict(
python=r'''
def solution(s, p, q):
    character_mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    integer_input = [character_mapping[c] for c in s]
    result = [0] * len(p)
    for index in range(len(p)):
        if p[index] == q[index]:
            result[index] = integer_input[p[index]]
            break
        sub_array = integer_input[p[index]:q[index] + 1]
        result[index] = min(sub_array)
    return result
''',
c=r'''
#include <stdlib.h>
#include <string.h>

static int charValue(char c) {
    switch (c) {
        case 'A': return 1;
        case 'C': return 2;
        case 'G': return 3;
        case 'T': return 4;
    }
    return 0;
}

int *solution(const char *s, const int *p, const int *q, int m) {
    int len = (int)strlen(s);
    int *integerInput = malloc((size_t)len * sizeof(int));
    for (int i = 0; i < len; i++) {
        integerInput[i] = charValue(s[i]);
    }
    int *result = malloc((size_t)m * sizeof(int));
    for (int index = 0; index < m; index++) {
        if (p[index] == q[index]) {
            result[index] = integerInput[p[index]];
            break;
        }
        int minimumValue = integerInput[p[index]];
        for (int k = p[index]; k <= q[index]; k++) {
            if (integerInput[k] < minimumValue) minimumValue = integerInput[k];
        }
        result[index] = minimumValue;
    }
    free(integerInput);
    return result;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class GenomicRangeQuery
{
    private static readonly Dictionary<char, int> CharacterMapping = new Dictionary<char, int>
    {
        { 'A', 1 }, { 'C', 2 }, { 'G', 3 }, { 'T', 4 }
    };

    public int[] Solve(string s, int[] p, int[] q)
    {
        char[] characterInput = s.ToCharArray();
        int[] integerInput = new int[characterInput.Length];
        for (int counter = 0; counter < characterInput.Length; counter++)
        {
            integerInput[counter] = CharacterMapping[characterInput[counter]];
        }
        int[] result = new int[p.Length];
        for (int index = 0; index < p.Length; index++)
        {
            if (p[index] == q[index])
            {
                result[index] = integerInput[p[index]];
                break;
            }
            int minimumValue = int.MaxValue;
            for (int k = p[index]; k <= q[index]; k++)
            {
                if (integerInput[k] < minimumValue)
                {
                    minimumValue = integerInput[k];
                }
            }
            result[index] = minimumValue;
        }
        return result;
    }
}
''')

R["T126"] = dict(
python=r'''
def solution(x, a):
    leaves = set()
    for i, value in enumerate(a):
        leaves.add(value)
        if x in leaves and len(leaves) == x:
            return i
    return -1
''',
c=r'''
#include <stdlib.h>

int solution(int x, const int *a, int n) {
    int *distinct = NULL;
    int count = 0;
    int hasX = 0;
    for (int i = 0; i < n; i++) {
        int found = 0;
        for (int j = 0; j < count; j++) {
            if (distinct[j] == a[i]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            distinct = realloc(distinct, (size_t)(count + 1) * sizeof(int));
            distinct[count++] = a[i];
        }
        if (a[i] == x) hasX = 1;
        if (hasX && count == x) {
            free(distinct);
            return i;
        }
    }
    free(distinct);
    return -1;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;

public class FrogRiverOne
{
    public int Solve(int x, int[] a)
    {
        var leaves = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            leaves.Add(a[i]);
            if (leaves.Contains(x) && leaves.Count == x) return i;
        }
        return -1;
    }
}
''')

R["T641"] = dict(
python=r'''
class ReverseLineReader:
    def __init__(self, stream):
        self.in_stream = stream
        self.current_pos = 0
        self.current_line_start = 0
        self.current_line_end = 0
        self.last_pos_in_file = 0
        self.last_char = '\0'

    def find_prev_line(self):
        pass

    def read(self):
        if self.current_pos < self.current_line_end:
            self.current_pos += 1
            return self.in_stream.read_byte()
        elif self.current_pos > self.last_pos_in_file and self.current_line_start < self.current_line_end:
            self.find_prev_line()
            if self.last_char != '\n' and self.last_char != '\r':
                return '\n'
            else:
                return self.read()
        elif self.current_pos < 0:
            return -1
        else:
            self.find_prev_line()
            return self.read()
''',
c=r'''
#include <stdio.h>

typedef struct {
    FILE *fp;
    long currentPos;
    long currentLineStart;
    long currentLineEnd;
    long lastPosInFile;
    char lastChar;
} ReverseReader;

static void findPrevLine(ReverseReader *r) {
    (void)r;
}

static int readChar(ReverseReader *r) {
    if (r->currentPos < r->currentLineEnd) {
        fseek(r->fp, r->currentPos, SEEK_SET);
        r->currentPos++;
        return fgetc(r->fp);
    } else if (r->currentPos > r->lastPosInFile && r->currentLineStart < r->currentLineEnd) {
        findPrevLine(r);
        if (r->lastChar != '\n' && r->lastChar != '\r') {
            return '\n';
        } else {
            return readChar(r);
        }
    } else if (r->currentPos < 0) {
        return -1;
    } else {
        findPrevLine(r);
        return readChar(r);
    }
}
''',
csharp=r'''
using System.IO;

public class ReverseLineReader
{
    private readonly FileStream _stream;
    private long _currentPos;
    private long _currentLineStart;
    private long _currentLineEnd;
    private long _lastPosInFile;
    private char _lastChar;

    public ReverseLineReader(FileStream stream)
    {
        _stream = stream;
    }

    private void FindPrevLine()
    {
    }

    public int Read()
    {
        if (_currentPos < _currentLineEnd)
        {
            _stream.Seek(_currentPos++, SeekOrigin.Begin);
            return _stream.ReadByte();
        }
        else if (_currentPos > _lastPosInFile && _currentLineStart < _currentLineEnd)
        {
            FindPrevLine();
            if (_lastChar != '\n' && _lastChar != '\r')
            {
                return '\n';
            }
            else
            {
                return Read();
            }
        }
        else if (_currentPos < 0)
        {
            return -1;
        }
        else
        {
            FindPrevLine();
            return Read();
        }
    }
}
''')

R["T605"] = dict(
python=r'''
import xml.etree.ElementTree as ET

def main():
    current_element_name = None
    for event, elem in ET.iterparse("family.xml", events=("start",)):
        current_element_name = elem.tag
        if current_element_name == "dad":
            print("isStartElement: True")
            print("Element BEGIN: " + current_element_name)
            elem.clear()
        else:
            print(current_element_name)

main()
''',
c=r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *f = fopen("family.xml", "r");
    if (!f) return 1;
    char buffer[4096];
    size_t n = fread(buffer, 1, sizeof buffer - 1, f);
    buffer[n] = '\0';
    fclose(f);
    const char *p = buffer;
    while ((p = strchr(p, '<')) != NULL) {
        const char *end = strchr(p, '>');
        if (end == NULL) break;
        size_t len = (size_t)(end - p - 1);
        if (len == 0 || p[1] == '/' || p[1] == '?') {
            p = end + 1;
            continue;
        }
        char name[256];
        if (len >= sizeof name) len = sizeof name - 1;
        memcpy(name, p + 1, len);
        name[len] = '\0';
        if (strcmp(name, "dad") == 0) {
            printf("isStartElement: true\n");
            printf("Element BEGIN: %s\n", name);
        } else {
            printf("%s\n", name);
        }
        p = end + 1;
    }
    return 0;
}
''',
csharp=r'''
using System;
using System.Xml;

public class Program
{
    public static void Main(string[] args)
    {
        using (XmlReader xmlsr = XmlReader.Create("family.xml"))
        {
            string currentElementName = null;
            while (xmlsr.Read())
            {
                if (xmlsr.NodeType == XmlNodeType.Element)
                {
                    currentElementName = xmlsr.Name;
                    if ("dad" == currentElementName)
                    {
                        Console.WriteLine("isStartElement: " + xmlsr.IsStartElement());
                        Console.WriteLine("Element BEGIN: " + currentElementName);
                        xmlsr.Skip();
                    }
                    else
                    {
                        Console.WriteLine(currentElementName);
                    }
                }
            }
        }
    }
}
''')

R["T759"] = dict(
python=r'''
class Node:
    def __init__(self, parent=None):
        self.parent = parent

class Pane(Node):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.children = []

    def get_children(self):
        return self.children

class HTMLEditor(Pane):
    def lookup(self, css):
        return self.children[0] if self.children else None

class Stage:
    def __init__(self):
        self.scene = None
        self.visible = False

    def show(self):
        self.visible = True

def start(primary_stage):
    html_editor = HTMLEditor()
    primary_stage.scene = html_editor
    primary_stage.show()
    tool_bar = html_editor.lookup(".tool-bar")
    while tool_bar is not None:
        tool_bar.parent.get_children().remove(tool_bar)
        tool_bar = html_editor.lookup(".tool-bar")
''',
c=r'''
#include <stdlib.h>
#include <string.h>

typedef struct Node Node;
struct Node {
    char selector[64];
    Node *parent;
    Node *children[16];
    int childCount;
};

typedef struct {
    Node *root;
    int visible;
} Stage;

static Node *lookup(Node *root, const char *selector) {
    if (!root) return NULL;
    for (int i = 0; i < root->childCount; i++) {
        if (strcmp(root->children[i]->selector, selector) == 0) {
            return root->children[i];
        }
    }
    return NULL;
}

static void removeChild(Node *parent, Node *child) {
    for (int i = 0; i < parent->childCount; i++) {
        if (parent->children[i] == child) {
            for (int j = i; j < parent->childCount - 1; j++) {
                parent->children[j] = parent->children[j + 1];
            }
            parent->childCount--;
            return;
        }
    }
}

void start(Stage *primaryStage) {
    Node *htmlEditor = calloc(1, sizeof(Node));
    primaryStage->root = htmlEditor;
    primaryStage->visible = 1;
    Node *toolBar = lookup(htmlEditor, ".tool-bar");
    while (toolBar != NULL) {
        removeChild(toolBar->parent, toolBar);
        toolBar = lookup(htmlEditor, ".tool-bar");
    }
}
''',
csharp=r'''
using System.Collections.Generic;

public class Node
{
    public Node Parent { get; set; }
    public List<Node> Children { get; } = new List<Node>();
}

public class Pane : Node
{
}

public class HTMLEditor : Pane
{
    public Node Lookup(string cssSelector)
    {
        return Children.Count > 0 ? Children[0] : null;
    }
}

public class Stage
{
    public void SetScene(object scene) { }
    public void Show() { }
}

public class EditorProgram
{
    public static void Start(Stage primaryStage)
    {
        var htmlEditor = new HTMLEditor();
        primaryStage.SetScene(htmlEditor);
        primaryStage.Show();
        for (Node toolBar = htmlEditor.Lookup(".tool-bar"); toolBar != null; toolBar = htmlEditor.Lookup(".tool-bar"))
        {
            ((Pane)toolBar.Parent).Children.Remove(toolBar);
        }
    }
}
''')

R["T723"] = dict(
python=r'''
def filter(words, text):
    for word in words:
        if word.lower() in text.lower():
            print(text)
            break
''',
c=r'''
#include <stdio.h>
#include <string.h>
#include <ctype.h>

static int containsIgnoreCase(const char *text, const char *word) {
    size_t tlen = strlen(text);
    size_t wlen = strlen(word);
    if (wlen == 0) return 1;
    for (size_t i = 0; i + wlen <= tlen; i++) {
        size_t j;
        for (j = 0; j < wlen; j++) {
            if (tolower((unsigned char)text[i + j]) != tolower((unsigned char)word[j])) break;
        }
        if (j == wlen) return 1;
    }
    return 0;
}

void filter(const char *words[], int wordCount, const char *text) {
    for (int i = 0; i < wordCount; i++) {
        if (containsIgnoreCase(text, words[i])) {
            printf("%s\n", text);
            break;
        }
    }
}
''',
csharp=r'''
using System;

public class WordFilter
{
    public void Filter(string[] words, string text)
    {
        foreach (string word in words)
        {
            if (text.ToLower().Contains(word.ToLower()))
            {
                Console.WriteLine(text);
                break;
            }
        }
    }
}
''')

R["T309"] = dict(
python=r'''
from collections import namedtuple

Animal = namedtuple("Animal", ["name"])

def main():
    list1 = [Animal("Cat"), Animal("Mouse"), Animal("Dog")]
    list2 = [Animal("Dog"), Animal("Mouse"), Animal("Cat")]
    list3 = [Animal("Dog"), Animal("Horse"), Animal("Cat")]
    list4 = [Animal("Dog"), Animal("Tiger"), Animal("Lion")]
    lists = [list1, list2, list3, list4]
    sorted_lists = set()
    for animals in lists:
        sorted_lists.add(tuple(sorted(animals)))
    for animals in sorted_lists:
        print([a.name for a in animals])

main()
''',
c=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmpStrings(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

static void sortCopy(char **src, int n, char **dest) {
    for (int i = 0; i < n; i++) dest[i] = src[i];
    qsort(dest, (size_t)n, sizeof(char *), cmpStrings);
}

int main(void) {
    char *list1[] = {"Cat", "Mouse", "Dog"};
    char *list2[] = {"Dog", "Mouse", "Cat"};
    char *list3[] = {"Dog", "Horse", "Cat"};
    char *list4[] = {"Dog", "Tiger", "Lion"};
    char **lists[] = {list1, list2, list3, list4};
    int sizes[] = {3, 3, 3, 3};
    char *sorted[4][3];
    for (int i = 0; i < 4; i++) {
        sortCopy(lists[i], sizes[i], sorted[i]);
    }
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < sizes[i]; j++) {
            printf("%s ", sorted[i][j]);
        }
        printf("\n");
    }
    return 0;
}
''',
csharp=r'''
using System;
using System.Collections.Generic;
using System.Linq;

public class Program
{
    public static void Main(string[] args)
    {
        var list1 = new List<string> { "Cat", "Mouse", "Dog" };
        var list2 = new List<string> { "Dog", "Mouse", "Cat" };
        var list3 = new List<string> { "Dog", "Horse", "Cat" };
        var list4 = new List<string> { "Dog", "Tiger", "Lion" };
        var list = new List<List<string>> { list1, list2, list3, list4 };
        var sorted = new List<List<string>>();
        foreach (var animals in list)
        {
            var arList = new List<string>(animals);
            arList.Sort();
            if (!sorted.Any(s => s.SequenceEqual(arList)))
            {
                sorted.Add(arList);
            }
        }
        foreach (var animals in sorted)
        {
            Console.WriteLine(string.Join(" ", animals));
        }
    }
}
''')

R["Rf3d83a68bd"] = r'''
from functools import partial

def curry(func):
    def curried(*args):
        return partial(func, *args)
    return curried
'''

R["R7c5881afbf"] = r'''
public static String Combine(String path1, String path2)
{
    if (path1 == null)
        throw new ArgumentNullException("path1");
    if (path2 == null)
        throw new ArgumentNullException("path2");
    return CombineNoChecks(path1, path2);
}
'''

R["R0f80f0fb62"] = r'''
public static Double Correlation(Double[] Xs, Double[] Ys)
{
    int n = Math.Min(Xs.Length, Ys.Length);
    Double sumX = 0;
    Double sumY = 0;
    Double sumX2 = 0;
    Double sumY2 = 0;
    Double sumXY = 0;
    for (int i = 0; i < n; i++)
    {
        sumX += Xs[i];
        sumY += Ys[i];
        sumX2 += Xs[i] * Xs[i];
        sumY2 += Ys[i] * Ys[i];
        sumXY += Xs[i] * Ys[i];
    }
    Double avgX = sumX / n;
    Double avgY = sumY / n;
    Double stdX = Math.Sqrt(sumX2 - n * avgX * avgX);
    Double stdY = Math.Sqrt(sumY2 - n * avgY * avgY);
    Double covariance = sumXY - n * avgX * avgY;
    return covariance / stdX / stdY;
}
'''

R["Recd81e23e8"] = r'''
int main(int argc, char **argv) {
    for (int i = 0; i < 2; i++) {
        ret[i] = calloc(20, 1);
    }
    char **ipnport = arguments_handle(argc, argv);
    printf("IP is :%s port range is %s\n", ipnport[1], ipnport[0]);
    return 0;
}
'''

R["Radd810f35f"] = r'''
public static String join(String separator, String...values) {
    if (values.length == 0) return "";
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < values.length; i++) {
        if (values[i] == null) values[i] = "";
        if (i > 0) sb.append(separator);
        sb.append(values[i]);
    }
    return sb.toString();
}
'''

R["Ra654f3cacb"] = r'''
public static boolean isPalindrome(String str) {
    String upper = str.toUpperCase();
    int left = 0;
    int right = upper.length() - 1;
    while (left < right) {
        if (upper.charAt(left) != upper.charAt(right)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
'''

R["Rc8ce82f32f"] = r'''
int main(int argc, char **argv) {
    char c;
    printf("Press key");
    while (!kbhit()) {
        putchar('.');
        fflush(stdout);
        sleep(1);
    }
    c = (char)getchar();
    printf("\nChar received:%c\nDone.\n", c);
    return 0;
}
'''

R["Rdddd23f55c"] = r'''
public void SendEmail(MyInternalSystemEmailMessage email)
{
    var mailMessage = BuildMailMessage(email);
    var mimeMessage = MimeKit.MimeMessage.CreateFromMailMessage(mailMessage);
    SendViaGmail(mimeMessage);
}

private System.Net.Mail.MailMessage BuildMailMessage(MyInternalSystemEmailMessage email)
{
    var mailMessage = new System.Net.Mail.MailMessage
    {
        From = new System.Net.Mail.MailAddress(email.FromAddress),
        Subject = email.Subject,
        Body = email.Body,
        IsBodyHtml = email.IsHtml
    };
    mailMessage.To.Add(email.ToRecipients);
    mailMessage.ReplyToList.Add(email.FromAddress);
    foreach (var attachment in email.Attachments)
    {
        mailMessage.Attachments.Add(attachment);
    }
    return mailMessage;
}

private void SendViaGmail(MimeKit.MimeMessage mimeMessage)
{
    var gmailMessage = new Google.Apis.Gmail.v1.Data.Message { Raw = Encode(mimeMessage.ToString()) };
    Google.Apis.Gmail.v1.UsersResource.MessagesResource.SendRequest request =
        service.Users.Messages.Send(gmailMessage, ServiceEmail);
    request.Execute();
}
'''

R["Rfa50623d34"] = r'''
def upgrade():
    url = context.config.get_main_option("sqlalchemy.url")
    engine = sa.create_engine(url)
    DBSession.configure(bind=engine)
    op.create_table(
    'client_credential',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=22), nullable=False),
    sa.Column('secret', sa.String(length=44), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'],),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key'))
    now = sa.func.now()
    clients = [dict(secret=c.secret, key=c.key, is_active=True, client_id=c.id,
                    created_at=now, updated_at=now) for c in Client.query.all()]
    op.bulk_insert(ClientCredential, clients)
    op.drop_column(u'client', u'secret')
    op.drop_column(u'client', u'key')
'''

R["R6977f1c997"] = r'''
def scan(sentence):
    tuples = []
    for word in sentence.split():
        if word in lexicons:
            tuples.append((lexicons[word], word))
        elif word.isdigit():
            tuples.append(('number', int(word)))
        else:
            tuples.append(('error', word))
    return tuples
'''

R["Rbcec8876d4"] = r'''
def contains(small, big):
    n = len(small)
    for i in range(len(big) - n + 1):
        if big[i:i + n] == small:
            return i, i + n
    return False
'''

R["Rab8fdb571d"] = r'''
int main() {
    char *str = malloc(100);
    strcpy(str, "test string.");
    char *token = strtok(str, " ");
    while (token != NULL) {
        printf("%s\n", token);
        token = strtok(NULL, " ");
    }
    free(str);
    return 0;
}
'''

R["R6b8d361ee9"] = r'''
static void Main(string[] args)
{
    if (args.Length != 2)
    {
        Console.WriteLine("Usage:  repchar {inputfile} {outputfile}");
        return;
    }
    using (StreamReader input = new StreamReader(args[0]))
    using (StreamWriter output = new StreamWriter(args[1]))
    {
        int blockSize = 100000;
        char[] inBuffer = new char[blockSize];
        char[] outBuffer = new char[blockSize * 3];
        int readSize;
        while ((readSize = input.ReadBlock(inBuffer, 0, blockSize)) > 0)
        {
            int writeSize = TransformBlock(inBuffer, outBuffer, readSize);
            output.Write(outBuffer, 0, writeSize);
        }
    }
}
'''

R["Rc34ff3d7d3"] = r'''
private void initData() {
    testData = new ArrayList<>();
    Object[][] rows = {
        {"Mach-1", 1477468500000L, 1, 0}, {"Mach-1", 1477472100000L, 2, 0},
        {"Mach-1", 1477474200000L, 5, 0}, {"Mach-1", 1477476000000L, 3, 0},
        {"Mach-1", 1477479600000L, 4, 0}, {"Mach-1", 1477486800000L, 1, 0},
        {"Mach-2", 1477465200000L, 3, 1}, {"Mach-2", 1477472400000L, 2, 1},
        {"Mach-2", 1477474200000L, 5, 1}, {"Mach-2", 1477476000000L, 2, 1},
        {"Mach-2", 1477479600000L, 3, 1}, {"Mach-2", 1477486800000L, 4, 1}
    };
    for (Object[] row : rows) {
        testData.add(new EventStatus((String) row[0], (Long) row[1], (Integer) row[2], (Integer) row[3]));
    }
    Set<String> distinct = new LinkedHashSet<>();
    for (EventStatus eventStatus : testData) {
        distinct.add(eventStatus.getName());
    }
    catArray = distinct.toArray(new String[0]);
}
'''

R["R73c281cc62"] = r'''
private static List<T[]> EnumerateCombos<T>(IEnumerable<T> items, List<T> currentCombo, int startIndex, int threshold)
{
    var results = new List<T[]>();
    if (currentCombo.Count >= threshold)
    {
        return results;
    }
    var itemList = items.ToList();
    for (int i = startIndex; i < itemList.Count; i++)
    {
        currentCombo.Add(itemList[i]);
        results.Add(currentCombo.ToArray());
        results.AddRange(EnumerateCombos(itemList, currentCombo, i + 1, threshold));
        currentCombo.RemoveAt(currentCombo.Count - 1);
    }
    return results;
}
'''

R["R91d065403d"] = r'''
public static File createTempDir() {
    File baseDir = new File(System.getProperty("java.io.tmpdir"));
    String baseName = System.currentTimeMillis() + "-";
    int counter = 0;
    while (counter < TEMP_DIR_ATTEMPTS) {
        File tempDir = new File(baseDir, baseName + counter);
        if (tempDir.mkdir()) {
            return tempDir;
        }
        counter++;
    }
    throw new IllegalStateException("Failed to create directory within " + TEMP_DIR_ATTEMPTS
            + " attempts (tried " + baseName + "0 to " + baseName + (TEMP_DIR_ATTEMPTS - 1) + ')');
}
'''

R["R8cfbeb65a3"] = r'''
public static IList<ReportFile> ReadFiles(int year, int month)
{
    string[] fileNames = { "{0:YYYYMMDD}----1234D.dat", "{0:YYYYMMDD}----5678D.dat" };
    DateTime dateStart = new DateTime(year, month, 1);
    DateTime dateEnd = dateStart.AddMonths(1);
    var reportList = new List<ReportFile>();
    for (DateTime date = dateStart; date < dateEnd; date = date.AddDays(1))
    {
        reportList.AddRange(fileNames
            .Select(fileTemplate => string.Format(fileTemplate, date))
            .Where(File.Exists)
            .Select(file => new ReportFile { Date = date, Path = file, Lines = GetReportLines(file) }));
    }
    IList<ReportFile> files = reportList;
    return files;
}
'''

R["R8f617cb401"] = r'''
int main() {
    unsigned long *data = malloc(sizeof(unsigned long) * 9);
    int i;
    for (i = 0; i < 9; ++i) {
        data[i] = i;
    }
    unsigned long total = sumOfColTwo(data);
    printf("%lu\n", total);
    free(data);
    return 0;
}
'''

R["R593eed57e6"] = r'''
static void Main(string[] args)
{
    Console.WriteLine("Enter A Number :");
    int n = int.Parse(Console.ReadLine());
    bool by3 = n % 3 == 0;
    bool by5 = n % 5 == 0;
    if (by3 && by5)
        Console.WriteLine("This Number is Divisible by 3 and 5!");
    else if (by3)
        Console.WriteLine("\nThe number is divisible by 3 but not by 5");
    else if (by5)
        Console.WriteLine("The number is divisible by 5 but not by 3");
    else
        Console.WriteLine("\nThis Number is Not Divisible by 3 and 5!");
    Console.ReadLine();
}
'''

R["Rc5e1a6cc9a"] = r'''
void initialize()
{
    ConcurrentQueue<string> queue = new ConcurrentQueue<string>();
    foreach (string url in websites)
    {
        queue.Enqueue(url);
    }
    List<Thread> threads = Enumerable.Range(0, threadCountFromTheUser)
        .Select(_ => new Thread(work))
        .ToList();
}
'''

R["R35e99f1126"] = r'''
static void Main(string[] args)
{
    var EDGES = new List<Edge>
    {
        new Edge(new Point(5, 50), new Point(20, 100)),
        new Edge(new Point(20, 100), new Point(30, 50)),
        new Edge(new Point(30, 50), new Point(10, 0)),
        new Edge(new Point(5, 50), new Point(30, 50)),
        new Edge(new Point(5, 50), new Point(10, 0)),
        new Edge(new Point(20, 100), new Point(80, 100)),
        new Edge(new Point(10, 0), new Point(80, 100))
    };
    var POINTS = new List<double[]>(EDGES.Count * 2);
    FillPoints(EDGES, ref POINTS);
    for (int i = 0; i < POINTS.Count; i++)
    {
        Console.WriteLine("{0} {1} {2}", i, POINTS[i][0], POINTS[i][1]);
    }
    Console.WriteLine();
    var edgeIndices = new int[EDGES.Count, 2];
    FillEdges(EDGES, POINTS, ref edgeIndices);
    for (int i = 0; i < edgeIndices.GetLength(0); i++)
    {
        Console.WriteLine("({0}, {1})", edgeIndices[i, 0], edgeIndices[i, 1]);
    }
    Console.ReadKey(true);
}
'''

R["Ra1eaef8d13"] = r'''
private static void removeEven(int[] k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 != 0) {
            k[counter] = k[i];
            counter++;
        }
    }
    while (counter < n) {
        k[counter] = 0;
        counter++;
    }
}
'''

R["R7fe68d314b"] = r'''
public static List<string> LoadCitiesByState(string state)
{
    DataTable dt = null;
    try
    {
        dt = SharedDataAccess.GetCities(state);
    }
    catch
    {
    }
    if (dt == null)
    {
        return new List<string>();
    }
    var cities = new List<string>();
    foreach (DataRow row in dt.Rows)
    {
        cities.Add(row[0].ToString());
    }
    return cities;
}
'''

R["R83b1b1f08f"] = r'''
void main(int argc, char **argv) {
    int myargc = argc;
    char **myargv = malloc((argc - 1) * sizeof(void *));
    char **dst = myargv;
    for (char **src = argv + 1; src < argv + argc; ++src, ++dst) {
        *dst = strdup(*src);
    }
    getch();
}
'''

R["R08feb9bb95"] = r'''
public void ResetFields(Control.ControlCollection Controls)
{
    foreach (Control control in Controls)
    {
        switch (control)
        {
            case TextBox txt:
                txt.Text = string.Empty;
                break;
            case NumericUpDown numericUpDown:
                numericUpDown.Value = 3;
                break;
            default:
                if (control.Controls.Count > 0)
                {
                    this.ResetFields(control.Controls);
                }
                break;
        }
    }
}
'''

# ===ENTRIES===

def build():
    seeds = json.load(open(SEED, encoding="utf-8"))
    items = []
    problems = []
    seen = set()
    for s in seeds:
        sid = s["id"]
        if sid in seen:
            problems.append("duplicate seed id " + sid)
        seen.add(sid)
        if sid not in R:
            problems.append("missing output for " + sid)
            continue
        val = R[sid]
        if s["task"] == "translate":
            for lang in ("python", "c", "csharp"):
                code = val[lang]
                if len(code.strip()) < 20:
                    problems.append(sid + "." + lang + " too short")
                if lang == "python":
                    try:
                        ast.parse(code)
                    except SyntaxError as e:
                        problems.append(sid + "." + lang + " parse: " + str(e))
            items.append({"id": sid, "outputs": {"python": val["python"], "c": val["c"], "csharp": val["csharp"]}})
        else:
            code = val
            if len(code.strip()) < 20:
                problems.append(sid + " too short")
            if s["lang"] == "python":
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    problems.append(sid + " parse: " + str(e))
            items.append({"id": sid, "output": code})
    extra = set(R) - seen
    if extra:
        problems.append("extra outputs: " + repr(sorted(extra)))
    if problems:
        raise SystemExit("\n".join(problems))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT):
        raise SystemExit("output file already exists: " + OUT)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=1)
    print("OK wrote " + str(len(items)) + " items to " + OUT)

if __name__ == "__main__":
    build()
