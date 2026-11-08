DATA_T3 = {}

DATA_T3["T359"] = {
"python": r'''import queue
import threading

outputCount = 0
countLock = threading.Lock()

def myRunnable(expensiveObjects):
    global outputCount
    obj = expensiveObjects.get()
    with countLock:
        outputCount += 1

def main():
    expensiveObjects = queue.Queue()
    for _ in range(4):
        expensiveObjects.put(object())
    workers = []
    for _ in range(4):
        t = threading.Thread(target=myRunnable, args=(expensiveObjects,))
        workers.append(t)
        t.start()
    for t in workers:
        t.join(5)
    print("Final: " + str(outputCount))

main()
''',
"c": r'''#include <stdio.h>
#include <pthread.h>

#define QUEUE_CAPACITY 8

static int queueCount = 0;
static pthread_mutex_t queueLock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t queueNotEmpty = PTHREAD_COND_INITIALIZER;
static int outputCount = 0;

static void *myRunnable (void *arg) {
    (void) arg;
    pthread_mutex_lock (& queueLock);
    while (queueCount == 0) {
        pthread_cond_wait (& queueNotEmpty, & queueLock);
    }
    queueCount --;
    outputCount ++;
    pthread_mutex_unlock (& queueLock);
    return NULL;
}

int main (void) {
    pthread_t threads [4];
    pthread_mutex_lock (& queueLock);
    for (int i = 0; i < 4; i ++) {
        queueCount ++;
    }
    pthread_cond_broadcast (& queueNotEmpty);
    pthread_mutex_unlock (& queueLock);
    for (int i = 0; i < 4; i ++) {
        pthread_create (& threads [i], NULL, myRunnable, NULL);
    }
    for (int i = 0; i < 4; i ++) {
        pthread_join (threads [i], NULL);
    }
    printf ("Final: %d\n", outputCount);
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;
using System.Threading;

public class ThreadPoolDemo
{
    private static Queue<object> expensiveObjects = new Queue<object>();
    private static object gate = new object();
    private static int outputCount = 0;

    private static void MyRunnable()
    {
        while (true)
        {
            object obj;
            lock (gate)
            {
                if (expensiveObjects.Count == 0) return;
                obj = expensiveObjects.Dequeue();
            }
            outputCount++;
        }
    }

    public static void Main(string[] args)
    {
        for (int i = 0; i < 4; i++) expensiveObjects.Enqueue(new object());
        List<Thread> workers = new List<Thread>();
        for (int i = 0; i < 4; i++)
        {
            Thread t = new Thread(MyRunnable);
            workers.Add(t);
            t.Start();
        }
        foreach (Thread t in workers) t.Join(5000);
        Console.WriteLine("Final: " + outputCount);
    }
}
''',
}

DATA_T3["T448"] = {
"python": r'''parenthesesMapLeft = {'(': ')', '[': ']', '{': '}'}
parenthesesMapRight = {')': '(', ']': '[', '}': '{'}

def isBalanced(s):
    result = False
    if len(s) < 2:
        return False
    stack = []
    for ch in s:
        if ch not in parenthesesMapRight and ch not in parenthesesMapLeft:
            continue
        if ch in parenthesesMapLeft:
            stack.append(ch)
        else:
            if stack and stack.pop() == parenthesesMapRight[ch]:
                result = True
            else:
                return False
    if stack:
        return False
    return result
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdbool.h>

static char leftOf (char ch) {
    switch (ch) {
        case ')': return '(';
        case ']': return '[';
        case '}': return '{';
        default: return '\0';
    }
}

static bool isLeftParen (char ch) {
    return ch == '(' || ch == '[' || ch == '{';
}

static bool isRightParen (char ch) {
    return ch == ')' || ch == ']' || ch == '}';
}

static bool isBalanced (const char *str) {
    bool result = false;
    if (strlen (str) < 2) return false;
    char stack [256];
    int top = 0;
    for (size_t i = 0; i < strlen (str); i ++) {
        char ch = str [i];
        if (! isRightParen (ch) && ! isLeftParen (ch)) continue;
        if (isLeftParen (ch)) {
            stack [top ++] = ch;
        } else {
            if (top > 0 && stack [-- top] == leftOf (ch)) {
                result = true;
            } else {
                return false;
            }
        }
    }
    if (top > 0) return false;
    return result;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class BalanceChecker
{
    private static readonly Dictionary<char, char> parenthesesMapLeft =
        new Dictionary<char, char> { { '(', ')' }, { '[', ']' }, { '{', '}' } };
    private static readonly Dictionary<char, char> parenthesesMapRight =
        new Dictionary<char, char> { { ')', '(' }, { ']', '[' }, { '}', '{' } };

    public static bool IsBalanced(string str)
    {
        bool result = false;
        if (str.Length < 2) return false;
        Stack<char> stack = new Stack<char>();
        foreach (char ch in str)
        {
            if (!parenthesesMapRight.ContainsKey(ch) && !parenthesesMapLeft.ContainsKey(ch))
            {
                continue;
            }
            if (parenthesesMapLeft.ContainsKey(ch))
            {
                stack.Push(ch);
            }
            else
            {
                if (stack.Count > 0 && stack.Pop() == parenthesesMapRight[ch])
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
}
''',
}
