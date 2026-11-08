DATA4 = {
    "T92": {"outputs": {
        "python": '''def compress_bad(s):
    count_consecutive = 0
    compressed = []
    for i, ch in enumerate(s):
        count_consecutive += 1
        if i + 1 == len(s):
            compressed.append(ch + str(count_consecutive))
            count_consecutive = 0
            break
        elif ch != s[i + 1]:
            compressed.append(ch + str(count_consecutive))
            count_consecutive = 0
    return "".join(compressed)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *compress_bad(const char *str) {
    size_t len = strlen(str);
    char *compressed = malloc(len * 3 + 1);
    size_t pos = 0;
    int count_consecutive = 0;
    for (size_t i = 0; i < len; i++) {
        count_consecutive++;
        if (len == i + 1) {
            pos += sprintf(compressed + pos, "%c%d", str[i], count_consecutive);
            count_consecutive = 0;
            break;
        } else if (str[i] != str[i + 1]) {
            pos += sprintf(compressed + pos, "%c%d", str[i], count_consecutive);
            count_consecutive = 0;
        }
    }
    compressed[pos] = '\0';
    return compressed;
}''',
        "csharp": '''using System.Text;

public static class Compressor
{
    public static string CompressBad(string str)
    {
        int countConsecutive = 0;
        var compressed = new StringBuilder();
        for (int i = 0; i < str.Length; i++)
        {
            countConsecutive++;
            if (str.Length == i + 1)
            {
                compressed.Append(str[i]).Append(countConsecutive);
                countConsecutive = 0;
                break;
            }
            else if (str[i] != str[i + 1])
            {
                compressed.Append(str[i]).Append(countConsecutive);
                countConsecutive = 0;
            }
        }
        return compressed.ToString();
    }
}'''
    }},
    "T694": {"outputs": {
        "python": '''from itertools import product


class Foo:
    def __init__(self, data):
        self.data = data

    def all_unique_combinations(self):
        columns = list(self.data.values())
        return [tuple(combination) for combination in product(*columns)]


def main():
    data = {
        "foo": ["1", "2", "3"],
        "bar": ["3", "2"],
        "baz": ["5", "6", "7"],
    }
    foo = Foo(data)
    for combination in foo.all_unique_combinations():
        print(list(combination))


if __name__ == "__main__":
    main()''',
        "c": r'''#include <stdio.h>

#define COLS 3

static const char *columns[COLS][3] = {
    { "1", "2", "3" },
    { "3", "2", NULL },
    { "5", "6", "7" }
};
static const int column_sizes[COLS] = { 3, 2, 3 };

static void print_combinations(int col, char **combination) {
    if (col == COLS) {
        printf("[");
        for (int i = 0; i < COLS; i++) {
            printf("%s", combination[i]);
            if (i < COLS - 1) printf(", ");
        }
        printf("]\n");
        return;
    }
    char *choice;
    for (int i = 0; (choice = (char *) columns[col][i]) != NULL && i < column_sizes[col]; i++) {
        combination[col] = choice;
        print_combinations(col + 1, combination);
    }
}

int main(void) {
    char *combination[COLS];
    print_combinations(0, combination);
    return 0;
}''',
        "csharp": '''using System;
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
        var columns = data.Values.ToList();
        IEnumerable<IEnumerable<string>> seed = new List<List<string>> { new List<string>() };
        foreach (var column in columns)
        {
            seed = seed.SelectMany(partial => column.Select(value => partial.Append(value).ToList()));
        }
        return seed.Select(combination => combination.ToArray());
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
        var foo = new Foo(data);
        foreach (var combination in foo.AllUniqueCombinations())
        {
            Console.WriteLine(string.Join(", ", combination));
        }
    }
}'''
    }},
    "T546": {"outputs": {
        "python": '''def join(objects, delimiter):
    if not objects:
        return ""
    return delimiter.join(str(obj) for obj in objects)''',
        "c": r'''#include <stdlib.h>
#include <string.h>

char *join(char **objects, int count, const char *delimiter) {
    if (count == 0) {
        char *empty = malloc(1);
        empty[0] = '\0';
        return empty;
    }
    size_t total = 1;
    for (int i = 0; i < count; i++) {
        total += strlen(objects[i]);
        if (i < count - 1) {
            total += strlen(delimiter);
        }
    }
    char *ret = malloc(total);
    ret[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(ret, objects[i]);
        if (i < count - 1) {
            strcat(ret, delimiter);
        }
    }
    return ret;
}''',
        "csharp": '''using System;
using System.Linq;

public static class Joiner
{
    public static string Join(object[] objects, string delimiter)
    {
        if (objects.Length == 0)
        {
            return "";
        }
        return string.Join(delimiter, objects.Select(o => o.ToString()));
    }
}'''
    }},
    "T567": {"outputs": {
        "python": '''import threading


class SharedState:
    def __init__(self):
        self.state = 0
        self.cond = threading.Condition()


s = SharedState()


class Worker(threading.Thread):
    def run(self):
        i = 3
        while i < 50:
            with s.cond:
                while s.state != 2:
                    s.cond.wait()
                if s.state == 2:
                    print("t3 " + str(i))
                i += 3
                s.state = 3
                s.cond.notify_all()''',
        "c": r'''#include <pthread.h>
#include <stdio.h>

typedef struct shared {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int state;
} Shared;

static Shared s = { .state = 0 };

static void *worker(void *arg) {
    int i = 3;
    while (i < 50) {
        pthread_mutex_lock(&s.mutex);
        while (s.state != 2) {
            pthread_cond_wait(&s.cond, &s.mutex);
        }
        if (s.state == 2) {
            printf("t3 %d\n", i);
        }
        i += 3;
        s.state = 3;
        pthread_cond_broadcast(&s.cond);
        pthread_mutex_unlock(&s.mutex);
    }
    return NULL;
}''',
        "csharp": '''using System;
using System.Threading;

public class SharedState
{
    public int State { get; set; }
}

public class Worker
{
    private readonly SharedState s;

    public Worker(SharedState s)
    {
        this.s = s;
    }

    public void Run()
    {
        int i = 3;
        while (i < 50)
        {
            lock (s)
            {
                while (s.State != 2)
                {
                    Monitor.Wait(s);
                }
                if (s.State == 2)
                {
                    Console.WriteLine("t3 " + i);
                }
                i += 3;
                s.State = 3;
                Monitor.PulseAll(s);
            }
        }
    }
}'''
    }},
}
