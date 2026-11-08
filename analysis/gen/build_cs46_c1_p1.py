DATA_T1 = {
"T234": {"outputs": {
"python": r'''
def main():
    name = "AnuvratAnuvra"
    counts = {}
    for val in name:
        counts[val] = counts.get(val, 0) + 1
    for key, value in counts.items():
        if value > 1:
            print(f"{key}:{value}")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char name[] = "AnuvratAnuvra";
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
public static void Main(string[] args)
{
    string name = "AnuvratAnuvra";
    var map = new Dictionary<char, int>();
    foreach (char val in name)
    {
        if (map.ContainsKey(val))
            map[val] = map[val] + 1;
        else
            map[val] = 1;
    }
    foreach (var entry in map)
    {
        if (entry.Value > 1)
        {
            Console.WriteLine(entry.Key + ":" + entry.Value);
        }
    }
}
'''}},
"T240": {"outputs": {
"python": r'''
def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for i in range(len(st)):
        ar[ord(st[i])] += 1
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
    int ar[256] = {0};
    printf("Enter the String");
    if (!fgets(st, sizeof(st), stdin)) return 0;
    st[strcspn(st, "\n")] = '\0';
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
public static void Main(string[] a)
{
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char ch in st)
    {
        ar[ch]++;
    }
    for (int i = 0; i < 256; i++)
    {
        if (ar[i] > 0)
        {
            if (ar[i] == 1)
                Console.Write((char)i);
            else
                Console.Write((char)i + ar[i].ToString());
        }
    }
}
'''}},
"T365": {"outputs": {
"python": r'''
import random

SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
RANDOM = random.SystemRandom()


def shuffle(text):
    characters = list(text)
    random.shuffle(characters, random=RANDOM.random)
    return "".join(characters)


def generate_random_password(length):
    if length < 1:
        raise ValueError("length must be greater than 0")
    buf = [SYMBOLS[RANDOM.randrange(len(SYMBOLS))] for _ in range(length)]
    return shuffle("".join(buf))
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static const char *symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/";

static void shuffle(char *text) {
    size_t n = strlen(text);
    for (size_t i = 0; i < n; i++) {
        size_t j = (size_t)(rand() % (int)n);
        char t = text[i];
        text[i] = text[j];
        text[j] = t;
    }
}

char *generate_random_password(int length) {
    if (length < 1) {
        return NULL;
    }
    char *buf = malloc((size_t)length + 1);
    size_t sym_len = strlen(symbols);
    for (int idx = 0; idx < length; ++idx) {
        buf[idx] = symbols[rand() % (int)sym_len];
    }
    buf[length] = '\0';
    shuffle(buf);
    return buf;
}
''',
"csharp": r'''
public static string GenerateRandomPassword(int length)
{
    if (length < 1)
        throw new ArgumentException("length must be greater than 0");
    var buf = new char[length];
    for (int idx = 0; idx < buf.Length; ++idx)
        buf[idx] = symbols[RANDOM.Next(symbols.Length)];
    return Shuffle(new string(buf));
}
'''}},
"T506": {"outputs": {
"python": r'''
def main():
    st = input()
    arrlist = list(st)
    for i in range(len(st)):
        freq = arrlist.count(st[i])
        print(f"Frequency of {st[i]}  is:   {freq}")

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
    size_t len = strlen(st);
    for (size_t i = 0; i < len; i++) {
        int freq = 0;
        for (size_t j = 0; j < len; j++) {
            if (st[j] == st[i]) freq++;
        }
        printf("Frequency of %c  is:   %d\n", st[i], freq);
    }
    return 0;
}
''',
"csharp": r'''
public static void Main(string[] args)
{
    string st = Console.ReadLine();
    var arrlist = new List<char>(st);
    for (int i = 0; i < st.Length; i++)
    {
        int freq = 0;
        foreach (char c in arrlist)
            if (c == st[i]) freq++;
        Console.WriteLine("Frequency of " + st[i] + "  is:   " + freq);
    }
}
'''}},
"T434": {"outputs": {
"python": r'''
class Histogram:
    def __init__(self, tokens):
        self._tokens = tokens

    def find_in_line(self, name):
        return name if name in self._tokens else None


def valid_name(inp, histogram):
    user = ""
    name = next(inp)
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

static const char *known_names[] = {"Alice", "Bob", "Carol"};

static int find_in_line(const char *name) {
    for (int i = 0; i < 3; i++) {
        if (strcmp(known_names[i], name) == 0) {
            return 1;
        }
    }
    return 0;
}

static void valid_name(char *user, size_t size) {
    char name[128];
    if (scanf("%127s", name) != 1) {
        return;
    }
    if (find_in_line(name)) {
        printf("This name exist\n");
    } else {
        printf("Name not found\n");
        valid_name(user, size);
    }
}
''',
"csharp": r'''
public static string ValidName(IEnumerator<string> input, Func<string, string> findInLine)
{
    string user = "";
    string name = input.Current;
    input.MoveNext();
    if (findInLine(name) != null)
    {
        Console.WriteLine("This name exist");
    }
    else
    {
        Console.WriteLine("Name not found");
        user = ValidName(input, findInLine);
    }
    return user;
}
'''}},
}
