DATA_P3 = {}

DATA_P3["T706"] = {"outputs": {
"python": r'''
import random


def shuffle(text):
    characters = list(text)
    for i in range(len(characters)):
        random_index = random.randrange(len(characters))
        characters[i], characters[random_index] = characters[random_index], characters[i]
    return "".join(characters)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

char *shuffle(const char *text) {
    size_t n = strlen(text);
    char *characters = strdup(text);
    for (size_t i = 0; i < n; i++) {
        size_t randomIndex = rand() % n;
        char temp = characters[i];
        characters[i] = characters[randomIndex];
        characters[randomIndex] = temp;
    }
    return characters;
}
''',
"csharp": r'''
using System;

public static class Shuffler
{
    private static readonly Random random = new Random();

    public static string Shuffle(string text)
    {
        char[] characters = text.ToCharArray();
        for (int i = 0; i < characters.Length; i++)
        {
            int randomIndex = random.Next(characters.Length);
            char temp = characters[i];
            characters[i] = characters[randomIndex];
            characters[randomIndex] = temp;
        }
        return new string(characters);
    }
}
'''}}

DATA_P3["T92"] = {"outputs": {
"python": r'''
def compressBad(str):
    count_consecutive = 0
    compressed = []
    i = 0
    while i < len(str):
        count_consecutive += 1
        if len(str) == i + 1:
            compressed.append(str[i] + str(count_consecutive))
            count_consecutive = 0
            break
        if str[i] != str[i + 1]:
            compressed.append(str[i] + str(count_consecutive))
            count_consecutive = 0
        i += 1
    return "".join(compressed)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *compressBad(const char *str) {
    int countConsecutive = 0;
    size_t cap = strlen(str) * 2 + 8, len = 0;
    char *compressedString = malloc(cap);
    char piece[32];
    compressedString[0] = '\0';
    for (size_t i = 0; i < strlen(str); i++) {
        countConsecutive++;
        sprintf(piece, "%c%d", str[i], countConsecutive);
        if (strlen(str) == i + 1 || str[i] != str[i + 1]) {
            strcat(compressedString, piece);
            len += strlen(piece);
            countConsecutive = 0;
            if (strlen(str) == i + 1) break;
        }
    }
    return compressedString;
}
''',
"csharp": r'''
using System.Text;

public static class StringCompressor
{
    public static string CompressBad(string str)
    {
        int countConsecutive = 0;
        var compressedString = new StringBuilder();
        for (int i = 0; i < str.Length; i++)
        {
            countConsecutive++;
            if (str.Length == i + 1 || str[i] != str[i + 1])
            {
                compressedString.Append(str[i]).Append(countConsecutive);
                countConsecutive = 0;
                if (str.Length == i + 1) break;
            }
        }
        return compressedString.ToString();
    }
}
'''}}

DATA_P3["T694"] = {"outputs": {
"python": r'''
from itertools import product


class Foo:
    def __init__(self, data):
        self.data = data

    def allUniqueCombinations(self):
        pools = list(self.data.values())
        return [list(t) for t in product(*pools)]


def main():
    data = {
        "foo": ["1", "2", "3"],
        "bar": ["3", "2"],
        "baz": ["5", "6", "7"],
    }
    foo = Foo(data)
    for combination in foo.allUniqueCombinations():
        print(combination)


if __name__ == "__main__":
    main()
''',
"c": r'''
#include <stdio.h>

#define KEYS 3

static const char *values[KEYS][8] = {
    {"1", "2", "3"},
    {"3", "2"},
    {"5", "6", "7"}
};
static int counts[KEYS] = {3, 2, 3};

static void allUniqueCombinations(void) {
    int idx[KEYS] = {0, 0, 0};
    for (;;) {
        printf("[");
        for (int i = 0; i < KEYS; i++) {
            printf("%s", values[i][idx[i]]);
            if (i < KEYS - 1) printf(", ");
        }
        printf("]\n");
        int pos = KEYS - 1;
        while (pos >= 0) {
            idx[pos]++;
            if (idx[pos] < counts[pos]) break;
            idx[pos] = 0;
            pos--;
        }
        if (pos < 0) break;
    }
}

int main(void) {
    allUniqueCombinations();
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;
using System.Linq;

public class Foo
{
    private readonly Dictionary<string, List<string>> data;

    public Foo(Dictionary<string, List<string>> data)
    {
        this.data = data;
    }

    public IEnumerable<string[]> AllUniqueCombinations()
    {
        IEnumerable<IEnumerable<string>> pools = data.Values;
        IEnumerable<IEnumerable<string>> product = pools.Aggregate(
            (IEnumerable<IEnumerable<string>>)new[] { Enumerable.Empty<string>() },
            (acc, pool) => acc.SelectMany(prefix => pool,
                (prefix, item) => prefix.Concat(new[] { item })));
        foreach (IEnumerable<string> combo in product)
        {
            yield return combo.ToArray();
        }
    }
}

public static class Program
{
    public static void Main(string[] args)
    {
        var data = new Dictionary<string, List<string>>
        {
            ["foo"] = new List<string> { "1", "2", "3" },
            ["bar"] = new List<string> { "3", "2" },
            ["baz"] = new List<string> { "5", "6", "7" }
        };
        Foo foo = new Foo(data);
        foreach (string[] combination in foo.AllUniqueCombinations())
        {
            Console.WriteLine("[" + string.Join(", ", combination) + "]");
        }
    }
}
'''}}

DATA_P3["T546"] = {"outputs": {
"python": r'''
def join(objects, delimiter):
    if len(objects) == 0:
        return ""
    return delimiter.join(str(o) for o in objects)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

char *join(char **objects, int count, const char *delimiter) {
    if (count == 0) return strdup("");
    size_t total = 1;
    for (int i = 0; i < count; i++) {
        total += strlen(objects[i]);
        if (i < count - 1) total += strlen(delimiter);
    }
    char *ret = malloc(total);
    ret[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(ret, objects[i]);
        if (i < count - 1) strcat(ret, delimiter);
    }
    return ret;
}
''',
"csharp": r'''
using System;
using System.Text;

public static class Joiner
{
    public static string Join(object[] objects, string delimiter)
    {
        if (objects.Length == 0)
        {
            return "";
        }
        StringBuilder ret = new StringBuilder();
        bool first = true;
        foreach (object o in objects)
        {
            if (!first)
            {
                ret.Append(delimiter);
            }
            ret.Append(o);
            first = false;
        }
        return ret.ToString();
    }
}
'''}}

DATA_P3["T567"] = {"outputs": {
"python": r'''
import threading


class Shared:
    def __init__(self):
        self.state = 0
        self.cond = threading.Condition()


s = Shared()


def run():
    i = 3
    while i < 50:
        with s.cond:
            while s.state != 2:
                s.cond.wait()
            if s.state == 2:
                print("t3 " + str(i))
            i = i + 3
            s.state = 3
            s.cond.notify_all()
''',
"c": r'''
#include <pthread.h>
#include <stdio.h>

static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static int state = 0;

void *run(void *arg) {
    int i = 3;
    while (i < 50) {
        pthread_mutex_lock(&lock);
        while (state != 2)
            pthread_cond_wait(&cond, &lock);
        if (state == 2) printf("t3 %d\n", i);
        i = i + 3;
        state = 3;
        pthread_cond_broadcast(&cond);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}
''',
"csharp": r'''
using System;
using System.Threading;

public class Shared
{
    public int State;
    public readonly object Sync = new object();
}

public class Worker
{
    private readonly Shared s = new Shared();

    public void Run()
    {
        int i = 3;
        while (i < 50)
        {
            lock (s.Sync)
            {
                while (s.State != 2)
                {
                    Monitor.Wait(s.Sync);
                }
                if (s.State == 2) Console.WriteLine("t3 " + i);
                i = i + 3;
                s.State = 3;
                Monitor.PulseAll(s.Sync);
            }
        }
    }
}
'''}}
