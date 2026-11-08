DATA_T4 = {
    "T359": {
        "python": r'''import queue
import threading


output_count = 0
_lock = threading.Lock()


class MyRunnable:
    def __init__(self, expensive_objects):
        self.expensive_objects = expensive_objects

    def __call__(self):
        global output_count
        while True:
            try:
                self.expensive_objects.get(timeout=0.1)
            except queue.Empty:
                break
            with _lock:
                output_count += 1


def main():
    global output_count
    expensive_objects = queue.Queue()
    for _ in range(4):
        expensive_objects.put(object())
    executor = []
    for _ in range(4):
        thread = threading.Thread(target=MyRunnable(expensive_objects))
        executor.append(thread)
        thread.start()
    for thread in executor:
        thread.join(timeout=5)
    print("Final: " + str(output_count))''',
        "c": r'''#include <stdio.h>

static int output_count = 0;

static void my_runnable(int *shared_queue, int queue_len) {
    for (int i = 0; i < queue_len; i++) {
        (void)shared_queue[i];
        output_count++;
    }
}

int main(void) {
    int expensive_objects[4];
    for (int i = 0; i < 4; i++) {
        expensive_objects[i] = i;
    }
    my_runnable(expensive_objects, 4);
    printf("Final: %d\n", output_count);
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;

public static class Program
{
    private static int _outputCount;

    public static void Main()
    {
        var expensiveObjects = new ConcurrentQueue<object>();
        for (int i = 0; i < 4; i++)
        {
            expensiveObjects.Enqueue(new object());
        }
        Action drain = () =>
        {
            while (expensiveObjects.TryDequeue(out _))
            {
                Interlocked.Increment(ref _outputCount);
            }
        };
        Task[] tasks = new Task[4];
        for (int i = 0; i < 4; i++)
        {
            tasks[i] = Task.Run(drain);
        }
        Task.WaitAll(tasks, TimeSpan.FromSeconds(5));
        Console.WriteLine("Final: " + _outputCount);
    }
}'''
    },
    "T448": {
        "python": r'''parentheses_map_left = {"(": ")", "[": "]", "{": "}"}
parentheses_map_right = {")": "(", "]": "[", "}": "{"}


def is_balanced(s):
    result = False
    if len(s) < 2:
        return False
    stack = []
    for ch in s:
        if ch not in parentheses_map_right and ch not in parentheses_map_left:
            continue
        if ch in parentheses_map_left:
            stack.append(ch)
        else:
            if stack and stack.pop() == parentheses_map_right[ch]:
                result = True
            else:
                return False
    if stack:
        return False
    return result''',
        "c": r'''#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static char left_of(char ch) {
    switch (ch) {
        case ')': return '(';
        case ']': return '[';
        case '}': return '{';
        default: return '\0';
    }
}

static bool is_left(char ch) {
    return ch == '(' || ch == '[' || ch == '{';
}

static bool is_right(char ch) {
    return ch == ')' || ch == ']' || ch == '}';
}

bool is_balanced(const char *str) {
    bool result = false;
    size_t len = strlen(str);
    if (len < 2) return false;
    char *stack = malloc(len + 1);
    size_t top = 0;
    for (size_t i = 0; i < len; i++) {
        char ch = str[i];
        if (!is_right(ch) && !is_left(ch)) continue;
        if (is_left(ch)) {
            stack[top++] = ch;
        } else {
            if (top > 0 && stack[--top] == left_of(ch)) {
                result = true;
            } else {
                free(stack);
                return false;
            }
        }
    }
    if (top != 0) result = false;
    free(stack);
    return result;
}''',
        "csharp": r'''using System.Collections.Generic;

public static class BalanceChecker
{
    private static readonly Dictionary<char, char> ParenthesesMapLeft =
        new Dictionary<char, char> { { '(', ')' }, { '[', ']' }, { '{', '}' } };
    private static readonly Dictionary<char, char> ParenthesesMapRight =
        new Dictionary<char, char> { { ')', '(' }, { ']', '[' }, { '}', '{' } };

    public static bool IsBalanced(string str)
    {
        bool result = false;
        if (str.Length < 2) return false;
        var stack = new Stack<char>();
        foreach (char ch in str)
        {
            if (!ParenthesesMapRight.ContainsKey(ch) && !ParenthesesMapLeft.ContainsKey(ch)) continue;
            if (ParenthesesMapLeft.ContainsKey(ch))
            {
                stack.Push(ch);
            }
            else
            {
                if (stack.Count > 0 && stack.Pop() == ParenthesesMapRight[ch])
                {
                    result = true;
                }
                else
                {
                    return false;
                }
            }
        }
        if (stack.Count > 0) return false;
        return result;
    }
}'''
    },
    "T561": {
        "python": r'''def main():
    my_array = []
    my_array.append(list("string1"))
    my_array.append(list("string2"))
    my_array.append(list("string3"))
    char_array_2d = [list(row) for row in my_array]
    print(len(char_array_2d))
    s = ""
    for c in my_array:
        s += "".join(c)
    char_array_1d = list(s)
    print(len(char_array_1d))''',
        "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *strings[3] = {"string1", "string2", "string3"};
    char char_array_2d[3][16];
    for (int i = 0; i < 3; i++) {
        snprintf(char_array_2d[i], sizeof(char_array_2d[i]), "%s", strings[i]);
    }
    printf("%d\n", 3);
    char char_array_1d[64];
    int pos = 0;
    for (int i = 0; i < 3; i++) {
        size_t row_len = strlen(strings[i]);
        for (size_t j = 0; j < row_len; j++) {
            char_array_1d[pos++] = strings[i][j];
        }
    }
    char_array_1d[pos] = '\0';
    printf("%d\n", pos);
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;
using System.Text;

public static class CharArrays
{
    public static void Main()
    {
        var myArray = new List<char[]>
        {
            "string1".ToCharArray(),
            "string2".ToCharArray(),
            "string3".ToCharArray()
        };
        char[][] charArray2D = myArray.ToArray();
        Console.WriteLine(charArray2D.Length);
        var s = new StringBuilder();
        foreach (char[] c in myArray)
        {
            s.Append(new string(c));
        }
        char[] charArray1D = s.ToString().ToCharArray();
        Console.WriteLine(charArray1D.Length);
    }
}'''
    }
}
