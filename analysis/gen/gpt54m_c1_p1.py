# gpt-5.4-mini chunk 1 part 1: T234, T240, T247, T365, T506, T434, T639, T848, T613
DATA1 = {}

DATA1["T234"] = {"outputs": {
"python": r'''
def main():
    name = "AnuvratAnuvra"
    counts = {}
    for ch in name:
        counts[ch] = counts.get(ch, 0) + 1
    for key, value in counts.items():
        if value > 1:
            print(f"{key}:{value}")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *name = "AnuvratAnuvra";
    int counts[256] = {0};
    for (size_t i = 0; i < strlen(name); i++) {
        counts[(unsigned char)name[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 1) {
            printf("%c:%d\n", (char)i, counts[i]);
        }
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static void Main() {
    string name = "AnuvratAnuvra";
    var counts = new Dictionary<char, int>();
    foreach (char ch in name) {
        if (counts.ContainsKey(ch)) {
            counts[ch]++;
        } else {
            counts[ch] = 1;
        }
    }
    foreach (KeyValuePair<char, int> entry in counts) {
        if (entry.Value > 1) {
            Console.WriteLine(entry.Key + ":" + entry.Value);
        }
    }
}
'''
}}

DATA1["T240"] = {"outputs": {
"python": r'''
def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        if ar[i] > 0:
            if ar[i] == 1:
                print(chr(i), end="")
            else:
                print(f"{chr(i)}{ar[i]}", end="")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    printf("Enter the String");
    if (!fgets(st, sizeof(st), stdin)) return 0;
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
"csharp": r'''
using System;

public static void Main() {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char ch in st) {
        ar[ch] = ar[ch] + 1;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 0) {
            char ch = (char)i;
            if (ar[i] == 1) {
                Console.Write(ch);
            } else {
                Console.Write(ch + "" + ar[i]);
            }
        }
    }
}
'''
}}

DATA1["T247"] = {"outputs": {
"python": r'''
from collections import Counter

def main():
    st = input("Enter the String")
    counts = Counter(st)
    pieces = []
    for i in range(256):
        ch = chr(i)
        n = counts.get(ch, 0)
        if n > 0:
            pieces.append(ch if n == 1 else ch + str(n))
    print("".join(pieces), end="")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    printf("Enter the String");
    if (!fgets(st, sizeof(st), stdin)) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    size_t len = strlen(st);
    size_t i = 0;
    while (i < len) {
        ar[(unsigned char)st[i]]++;
        i++;
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
"csharp": r'''
using System;
using System.Linq;
using System.Text;

public static void Main() {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    var groups = st.GroupBy(c => c).ToDictionary(g => g.Key, g => g.Count());
    var sb = new StringBuilder();
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (groups.TryGetValue(ch, out int n) && n > 0) {
            sb.Append(n == 1 ? ch.ToString() : ch + "" + n);
        }
    }
    Console.Write(sb.ToString());
}
'''
}}

DATA1["T365"] = {"outputs": {
"python": r'''
import random

SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

def shuffle(text):
    chars = list(text)
    random.shuffle(chars)
    return "".join(chars)

def generate_random_password(length):
    if length < 1:
        raise ValueError("length must be greater than 0")
    buf = [SYMBOLS[random.randrange(len(SYMBOLS))] for _ in range(length)]
    return shuffle("".join(buf))
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static const char *symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";

static void shuffle(char *text) {
    int n = (int)strlen(text);
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        char tmp = text[i];
        text[i] = text[j];
        text[j] = tmp;
    }
}

char *generate_random_password(int length) {
    if (length < 1) {
        fprintf(stderr, "length must be greater than 0\n");
        return NULL;
    }
    char *buf = malloc(length + 1);
    int symbol_count = (int)strlen(symbols);
    for (int idx = 0; idx < length; ++idx) {
        buf[idx] = symbols[rand() % symbol_count];
    }
    buf[length] = '\0';
    shuffle(buf);
    return buf;
}
''',
"csharp": r'''
using System;
using System.Linq;

private static readonly Random RANDOM = new Random();
private static readonly string symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";

public static string GenerateRandomPassword(int length) {
    if (length < 1) {
        throw new ArgumentException("length must be greater than 0");
    }
    char[] buf = new char[length];
    for (int idx = 0; idx < buf.Length; ++idx) {
        buf[idx] = symbols[RANDOM.Next(symbols.Length)];
    }
    return Shuffle(new string(buf));
}

private static string Shuffle(string text) {
    return new string(text.OrderBy(c => RANDOM.Next()).ToArray());
}
'''
}}

DATA1["T506"] = {"outputs": {
"python": r'''
from collections import Counter

def main():
    text = input()
    counts = Counter(text)
    for ch in text:
        print(f"Frequency of {ch}  is:   {counts[ch]}")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char text[1024];
    if (!fgets(text, sizeof(text), stdin)) return 0;
    text[strcspn(text, "\n")] = '\0';
    size_t n = strlen(text);
    for (size_t i = 0; i < n; i++) {
        int freq = 0;
        for (size_t j = 0; j < n; j++) {
            if (text[j] == text[i]) {
                freq++;
            }
        }
        printf("Frequency of %c  is:   %d\n", text[i], freq);
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

public static void Main() {
    string str = Console.ReadLine();
    List<char> arrlist = str.ToList();
    foreach (char ch in str) {
        int freq = arrlist.Count(c => c == ch);
        Console.WriteLine("Frequency of " + ch + "  is:   " + freq);
    }
}
'''
}}

DATA1["T434"] = {"outputs": {
"python": r'''
class Histogram:
    def __init__(self, text):
        self._text = text

    def find_in_line(self, token):
        return token if token in self._text else None

class TokenReader:
    def __init__(self, tokens):
        self._tokens = tokens
        self._index = 0

    def next(self):
        token = self._tokens[self._index] if self._index < len(self._tokens) else ""
        self._index += 1
        return token

def valid_name(inp, histogram):
    user = ""
    name = inp.next()
    if histogram.find_in_line(name) is not None:
        print("This name exist")
    else:
        print("Name not found")
        user = valid_name(inp, histogram)
    return user
''',
"c": r'''
#include <stdio.h>
#include <string.h>

static char input_buffer[256];

static void read_token(void) {
    if (scanf("%255s", input_buffer) != 1) {
        input_buffer[0] = '\0';
    }
}

static const char *histogram_find_in_line(const char *name) {
    static const char *histogram = "alice bob carol david";
    return strstr(histogram, name) != NULL ? name : NULL;
}

static const char *valid_name(void) {
    const char *user = "";
    read_token();
    if (histogram_find_in_line(input_buffer) != NULL) {
        printf("This name exist\n");
    } else {
        printf("Name not found\n");
        user = valid_name();
    }
    return user;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class Histogram {
    private readonly string _text;
    public Histogram(string text) {
        _text = text;
    }
    public Match FindInLine(string token) {
        Match m = Regex.Match(_text, Regex.Escape(token));
        return m.Success ? m : null;
    }
}

public static string ValidName(Queue<string> input, Histogram histogram) {
    string user = "";
    string name = input.Dequeue();
    if (histogram.FindInLine(name) != null) {
        Console.WriteLine("This name exist");
    } else {
        Console.WriteLine("Name not found");
        user = ValidName(input, histogram);
    }
    return user;
}
'''
}}

DATA1["T639"] = {"outputs": {
"python": r'''
from pathlib import Path
from urllib.parse import urlsplit

def get_protocol(file_path):
    try:
        return urlsplit(Path(file_path).absolute().as_uri()).scheme
    except Exception:
        return "unknown"
''',
"c": r'''
#include <stdio.h>
#include <string.h>

static void get_protocol(const char *path, char *result, size_t result_size) {
    if (strncmp(path, "http://", 7) == 0) {
        snprintf(result, result_size, "http");
    } else if (strncmp(path, "https://", 8) == 0) {
        snprintf(result, result_size, "https");
    } else if (path[0] == '/' || strchr(path, ':') != NULL) {
        snprintf(result, result_size, "file");
    } else {
        snprintf(result, result_size, "unknown");
    }
}
''',
"csharp": r'''
using System;

public static string GetProtocol(string filePath) {
    string result;
    try {
        result = new Uri(filePath).Scheme;
    } catch (Exception) {
        result = "unknown";
    }
    return result;
}
'''
}}

DATA1["T848"] = {"outputs": {
"python": r'''
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
"c": r'''
#include <stdio.h>

int main(void) {
    int masks[4] = {1, 2, 4, 8};
    const char *labels = "ABCD";
    for (int i = 1; i < 16; ++i) {
        for (int b = 0; b < 4; b++) {
            if ((i & masks[b]) > 0) {
                putchar(labels[b]);
            }
        }
        putchar('\n');
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Text;

public static void Main() {
    for (int i = 1; i < 16; ++i) {
        var line = new StringBuilder();
        if ((i & 1) > 0) line.Append("A");
        if ((i & 2) > 0) line.Append("B");
        if ((i & 4) > 0) line.Append("C");
        if ((i & 8) > 0) line.Append("D");
        Console.WriteLine(line.ToString());
    }
}
'''
}}

DATA1["T613"] = {"outputs": {
"python": r'''
def sort(numbers, digit):
    if len(numbers) == 0 or digit <= 0:
        return numbers
    space = [[] for _ in range(10)]
    for value in numbers:
        bucket_index = (value // digit) % 10
        space[bucket_index].append(value)
    result = []
    for bucket in space:
        result.extend(sort(bucket, digit // 10))
    return result
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

static int *put_in_bucket(int *bucket, int len, int value, int *new_len) {
    int *grown = realloc(bucket, (len + 1) * sizeof(int));
    grown[len] = value;
    *new_len = len + 1;
    return grown;
}

int *sort(int *numbers, int count, int digit) {
    if (count == 0 || digit <= 0) return numbers;
    int *space[10] = {0};
    int len[10] = {0};
    for (int j = 0; j < count; j++) {
        int i = (numbers[j] / digit) % 10;
        space[i] = put_in_bucket(space[i], len[i], numbers[j], &len[i]);
    }
    int k = 0;
    for (int i = 0; i < 10; i++) {
        if (len[i] > 0) {
            sort(space[i], len[i], digit / 10);
            memcpy(numbers + k, space[i], len[i] * sizeof(int));
            k += len[i];
            free(space[i]);
        }
    }
    return numbers;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static int[] Sort(int[] numbers, int digit) {
    if (numbers.Length == 0 || digit <= 0) return numbers;
    var buckets = new List<int>[10];
    for (int b = 0; b < 10; b++) {
        buckets[b] = new List<int>();
    }
    foreach (int value in numbers) {
        buckets[(value / digit) % 10].Add(value);
    }
    int k = 0;
    for (int b = 0; b < 10; b++) {
        int[] sortedBucket = Sort(buckets[b].ToArray(), digit / 10);
        foreach (int value in sortedBucket) {
            numbers[k] = value;
            k++;
        }
    }
    return numbers;
}
'''
}}
