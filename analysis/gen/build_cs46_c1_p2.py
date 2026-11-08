DATA_T2 = {
"T639": {"outputs": {
"python": r'''
import os
from urllib.parse import urlparse


def file_to_url(file):
    return "file://" + os.path.abspath(file)


def get_protocol(file):
    try:
        return urlparse(file_to_url(file)).scheme
    except Exception:
        return "unknown"
''',
"c": r'''
#include <string.h>

void get_protocol(const char *path, char *result, size_t size) {
    const char *colon = strchr(path, ':');
    if (colon != NULL && (size_t)(colon - path) < size) {
        size_t n = (size_t)(colon - path);
        memcpy(result, path, n);
        result[n] = '\0';
        return;
    }
    strcpy(result, "unknown");
}
''',
"csharp": r'''
public static string GetProtocol(FileInfo file)
{
    string result;
    try
    {
        result = new Uri(file.FullName).Scheme;
    }
    catch (Exception)
    {
        result = "unknown";
    }
    return result;
}
'''}},
"T848": {"outputs": {
"python": r'''
def main():
    for i in range(1, 16):
        if i & 1:
            print("A", end="")
        if i & 2:
            print("B", end="")
        if i & 4:
            print("C", end="")
        if i & 8:
            print("D", end="")
        print()

main()
''',
"c": r'''
#include <stdio.h>

int main(void) {
    for (int i = 1; i < 16; ++i) {
        if (i & 1) putchar('A');
        if (i & 2) putchar('B');
        if (i & 4) putchar('C');
        if (i & 8) putchar('D');
        putchar('\n');
    }
    return 0;
}
''',
"csharp": r'''
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
'''}},
"T613": {"outputs": {
"python": r'''
def sort(numbers, digit):
    if len(numbers) == 0 or digit <= 0:
        return numbers
    buckets = [[] for _ in range(10)]
    for num in numbers:
        buckets[(num // digit) % 10].append(num)
    k = 0
    for i in range(10):
        for value in sort(buckets[i], digit // 10):
            numbers[k] = value
            k += 1
    return numbers
''',
"c": r'''
#include <stdlib.h>

static int *put_in_bucket(int *bucket, int *len, int value) {
    int *grown = (int *) realloc(bucket, ((size_t)*len + 1) * sizeof(int));
    grown[(*len)++] = value;
    return grown;
}

static int *sort(int *numbers, int len, int digit) {
    if (len == 0 || digit <= 0) return numbers;
    int *buckets[10] = {0};
    int lens[10] = {0};
    for (int j = 0; j < len; j++) {
        int i = (numbers[j] / digit) % 10;
        buckets[i] = put_in_bucket(buckets[i], &lens[i], numbers[j]);
    }
    int k = 0;
    for (int i = 0; i < 10; i++) {
        sort(buckets[i], lens[i], digit / 10);
        for (int j = 0; j < lens[i]; j++) {
            numbers[k++] = buckets[i][j];
        }
        free(buckets[i]);
    }
    return numbers;
}
''',
"csharp": r'''
public static int[] Sort(int[] numbers, int digit)
{
    if (numbers.Length == 0 || digit <= 0) return numbers;
    var buckets = new List<int>[10];
    for (int i = 0; i < 10; i++) buckets[i] = new List<int>();
    foreach (int num in numbers)
        buckets[(num / digit) % 10].Add(num);
    int k = 0;
    for (int i = 0; i < 10; i++)
    {
        int[] sorted = Sort(buckets[i].ToArray(), digit / 10);
        foreach (int value in sorted)
            numbers[k++] = value;
    }
    return numbers;
}
'''}},
"T18": {"outputs": {
"python": r'''
import threading
from datetime import datetime


def on_create(saved_instance_state):
    fmt = "%d.%m.%Y, %H:%M"
    old_time = "19.02.2018, 12:00"
    new_time = "20.02.2018, 14:00"
    diff = 0
    try:
        old_long = datetime.strptime(old_time, fmt).timestamp() * 1000
        new_long = datetime.strptime(new_time, fmt).timestamp() * 1000
        diff = new_long - old_long
    except ValueError as e:
        print(e)
        return
    counter = threading.Timer(diff / 1000.0, lambda: None)
    counter.start()
''',
"c": r'''
#define _XOPEN_SOURCE 700
#include <pthread.h>
#include <stdio.h>
#include <time.h>

static void *my_count(void *arg) {
    return NULL;
}

void on_create(void *saved_instance_state) {
    struct tm old_tm = {0}, new_tm = {0};
    time_t old_long, new_long;
    double diff = 0;
    if (strptime("19.02.2018, 12:00", "%d.%m.%Y, %H:%M", &old_tm) == NULL ||
        strptime("20.02.2018, 14:00", "%d.%m.%Y, %H:%M", &new_tm) == NULL) {
        perror("parse failed");
        return;
    }
    old_long = mktime(&old_tm);
    new_long = mktime(&new_tm);
    diff = difftime(new_long, old_long) * 1000;
    pthread_t counter;
    pthread_create(&counter, NULL, my_count, (void *)(long)diff);
}
''',
"csharp": r'''
public void OnCreate(Bundle savedInstanceState)
{
    string oldTime = "19.02.2018, 12:00";
    string newTime = "20.02.2018, 14:00";
    long diff = 0;
    try
    {
        DateTime oldDate = DateTime.ParseExact(oldTime, "dd.MM.yyyy, HH:mm", null);
        DateTime newDate = DateTime.ParseExact(newTime, "dd.MM.yyyy, HH:mm", null);
        diff = (long)(newDate - oldDate).TotalMilliseconds;
    }
    catch (FormatException e)
    {
        Console.WriteLine(e);
    }
    var counter = new System.Threading.Timer(_ => { }, null, diff, 1000);
}
'''}},
"T130": {"outputs": {
"python": r'''
def solution(x, a):
    hset = set()
    for i, value in enumerate(a):
        if value <= x:
            hset.add(value)
        if len(hset) == x:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, int A[], int len) {
    int *seen = calloc((size_t)X + 1, sizeof(int));
    int count = 0;
    for (int i = 0; i < len; i++) {
        if (A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            count++;
        }
        if (count == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
''',
"csharp": r'''
public int Solution(int X, int[] A)
{
    var hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}
'''}},
}
