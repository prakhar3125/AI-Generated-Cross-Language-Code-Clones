TRANSLATIONS_B = {
    "T229": {
        "python": r'''import threading
import traceback

condition = threading.Condition()
token = 0
N = 3


def run(worker_id):
    global token
    try:
        with condition:
            for i in range(5):
                while worker_id != token % N:
                    condition.wait()
                print(worker_id, i)
                token += 1
                condition.notify_all()
    except Exception as e:
        traceback.print_exc()''',
        "c": r'''#include <pthread.h>
#include <stdio.h>

static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static int token = 0;
static int N = 3;

void *run(void *arg) {
    long id = (long) arg;
    pthread_mutex_lock(&lock);
    for (int i = 0; i < 5; i++) {
        while (id != token % N)
            pthread_cond_wait(&cond, &lock);
        printf("%ld %d\n", id, i);
        token++;
        pthread_cond_broadcast(&cond);
    }
    pthread_mutex_unlock(&lock);
    return NULL;
}''',
        "csharp": r'''using System;
using System.Threading;

public class TokenRunner
{
    private static readonly object lockObj = new object();
    private static int token = 0;
    private const int N = 3;

    public void run(int id)
    {
        try
        {
            lock (lockObj)
            {
                for (int i = 0; i < 5; i++)
                {
                    while (id != token % N)
                    {
                        Monitor.Wait(lockObj);
                    }
                    Console.WriteLine(id + " " + i);
                    token++;
                    Monitor.PulseAll(lockObj);
                }
            }
        }
        catch (Exception e)
        {
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}'''
    },
    "T147": {
        "python": r'''def solution(X, A):
    empty_position = set(range(1, X + 1))
    for i in range(len(A)):
        empty_position.discard(A[i])
        if not empty_position:
            return i
    return -1''',
        "c": r'''#include <string.h>

#define MAX_VALUE 100000

int solution(int X, const int *A, int n) {
    static char present[MAX_VALUE + 1];
    memset(present, 0, sizeof(present));
    for (int v = 1; v <= X; v++) present[v] = 1;
    int remaining = X;
    for (int i = 0; i < n; i++) {
        if (A[i] >= 1 && A[i] <= X && present[A[i]]) {
            present[A[i]] = 0;
            remaining--;
        }
        if (remaining == 0) return i;
    }
    return -1;
}''',
        "csharp": r'''using System.Collections.Generic;

public class Solution
{
    public int solution(int X, int[] A)
    {
        HashSet<int> emptyPosition = new HashSet<int>();
        for (int i = 1; i <= X; i++)
        {
            emptyPosition.Add(i);
        }
        for (int i = 0; i < A.Length; i++)
        {
            emptyPosition.Remove(A[i]);
            if (emptyPosition.Count == 0)
            {
                return i;
            }
        }
        return -1;
    }
}'''
    },
    "T124": {
        "python": r'''def solution(X, A):
    length = len(A)
    if X > length:
        return -1
    is_filled = [0] * X
    jumped = 0
    for i in range(length):
        x = A[i]
        if x <= X:
            if x < 1:
                raise IndexError("index out of bounds")
            if is_filled[x - 1] == 0:
                is_filled[x - 1] = 1
                jumped += 1
                if jumped == X:
                    return i
    return -1''',
        "c": r'''#include <stdlib.h>

int solution(int X, const int *A, int n) {
    if (X > n) return -1;
    int *is_filled = (int *) calloc(X, sizeof(int));
    int jumped = 0;
    for (int i = 0; i < n; i++) {
        int x = A[i];
        if (x <= X) {
            if (is_filled[x - 1] == 0) {
                is_filled[x - 1] = 1;
                jumped++;
                if (jumped == X) {
                    free(is_filled);
                    return i;
                }
            }
        }
    }
    free(is_filled);
    return -1;
}''',
        "csharp": r'''public class Solution
{
    public int solution(int X, int[] A)
    {
        int len = A.Length;
        if (X > len)
        {
            return -1;
        }
        int[] isFilled = new int[X];
        int jumped = 0;
        for (int i = 0; i < len; i++)
        {
            int x = A[i];
            if (x <= X && isFilled[x - 1] == 0)
            {
                isFilled[x - 1] = 1;
                jumped += 1;
                if (jumped == X)
                {
                    return i;
                }
            }
        }
        return -1;
    }
}'''
    },
    "T614": {
        "python": r'''import re

mo_pattern = re.compile(r"[0-9]*")


class Spanned(str):
    pass


def log_d(tag, msg):
    print(tag + ": " + msg)


def filter(source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    log_d("debug", str(mo_pattern))
    log_d("debug", "source: " + source + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + dest + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = str(dest)
    if len(ls_text) > 0:
        ls_start = ls_text[0:dstart]
        log_d("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = str(source)
            log_d("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        log_d("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        log_d("debug", "lsText  : " + ls_text)
    matcher = mo_pattern.fullmatch(ls_text)
    log_d("debug", "loMatcher.matches(): " + str(matcher is not None) + ", lsText: " + ls_text)
    if matcher is None:
        return ""
    return None''',
        "c": r'''#include <stdio.h>
#include <string.h>

typedef struct {
    char pattern[128];
} Pattern;

static Pattern mo_pattern = { "[0-9]*" };

static void log_d(const char *tag, const char *msg) {
    printf("%s: %s\n", tag, msg);
}

static int pattern_matches(const Pattern *p, const char *text) {
    for (size_t i = 0; text[i]; i++) {
        if (text[i] < '0' || text[i] > '9') return 0;
    }
    return 1;
}

const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    char ls_start[256] = "";
    char ls_insert[256] = "";
    char ls_end[256] = "";
    char ls_text[256] = "";
    char msg[512];
    log_d("debug", mo_pattern.pattern);
    snprintf(msg, sizeof(msg), "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d",
             source, start, end, dest, dstart, dend);
    log_d("debug", msg);
    if (strlen(dest) > 0) {
        strncpy(ls_start, dest, dstart);
        ls_start[dstart] = '\0';
        log_d("debug", "lsStart");
        if (source[0] != '\0') {
            strcpy(ls_insert, source);
            log_d("debug", "lsInsert");
        }
        strcpy(ls_end, dest + dend);
        log_d("debug", "lsEnd");
        sprintf(ls_text, "%s%s%s", ls_start, ls_insert, ls_end);
        log_d("debug", "lsText");
    }
    if (!pattern_matches(&mo_pattern, ls_text)) {
        return "";
    }
    return NULL;
}''',
        "csharp": r'''using System;
using System.Text.RegularExpressions;

public class InputFilter
{
    private static readonly Regex moPattern = new Regex("^[0-9]*$");

    private static void LogD(string tag, string msg)
    {
        Console.WriteLine(tag + ": " + msg);
    }

    public string filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "", lsInsert = "", lsEnd = "", lsText = "";
        LogD("debug", moPattern.ToString());
        LogD("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
        lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            LogD("debug", "lsStart : " + lsStart);
            if (source != "")
            {
                lsInsert = source;
                LogD("debug", "lsInsert: " + lsInsert);
            }
            lsEnd = lsText.Substring(dend);
            LogD("debug", "lsEnd   : " + lsEnd);
            lsText = lsStart + lsInsert + lsEnd;
            LogD("debug", "lsText  : " + lsText);
        }
        if (!moPattern.IsMatch(lsText))
        {
            return "";
        }
        return null;
    }
}'''
    },
    "T592": {
        "python": r'''import random


def rand_nums(total, n):
    results = [0] * n
    if total == 0:
        return results
    total_plus_1 = total + 1
    while True:
        rs = [random.getrandbits(256) for _ in range(n)]
        s = sum(rs)
        if s == 0:
            continue
        for i in range(n):
            results[i] = (s % rs[i]) % total_plus_1
        return results''',
        "c": r'''#include <stdlib.h>
#include <string.h>

extern unsigned long long next_random_256(void);

int *rand_nums(int total, int n) {
    int *results = (int *) malloc(n * sizeof(int));
    if (results == NULL) return NULL;
    if (total == 0) {
        memset(results, 0, n * sizeof(int));
        return results;
    }
    unsigned long long *rs = (unsigned long long *) malloc(n * sizeof(unsigned long long));
    if (rs == NULL) {
        free(results);
        return NULL;
    }
    unsigned long long totalPlus1 = (unsigned long long) total + 1ULL;
    for (;;) {
        unsigned long long sum = 0ULL;
        int i;
        for (i = 0; i < n; ++i) {
            rs[i] = next_random_256();
            sum += rs[i];
        }
        if (sum == 0ULL) continue;
        for (i = 0; i < n; ++i)
            results[i] = (int) ((sum % rs[i]) % totalPlus1);
        free(rs);
        return results;
    }
}''',
        "csharp": r'''using System;
using System.Numerics;

public class RandomGen
{
    private static readonly Random rand = new Random();

    public static int[] randNums(int total, int n)
    {
        int[] results = new int[n];
        if (total == 0)
        {
            Array.Fill(results, 0);
            return results;
        }
        BigInteger[] rs = new BigInteger[n];
        BigInteger totalPlus1 = new BigInteger(total + 1L);
        while (true)
        {
            for (int i = 0; i < n; ++i)
            {
                byte[] bytes = new byte[257];
                rand.NextBytes(bytes);
                bytes[256] = 0;
                rs[i] = new BigInteger(bytes);
            }
            BigInteger sum = BigInteger.Zero;
            foreach (BigInteger r in rs)
            {
                sum += r;
            }
            if (sum == BigInteger.Zero)
            {
                continue;
            }
            for (int i = 0; i < n; ++i)
            {
                results[i] = (int) (sum % rs[i] % totalPlus1);
            }
            return results;
        }
    }
}'''
    },
    "T633": {
        "python": r'''import logging
import os
import zipfile


def dir_checker(location, name):
    os.makedirs(location + name, exist_ok=True)


def unzip(zip_file, location):
    try:
        with zipfile.ZipFile(zip_file) as zin:
            for ze in zin.infolist():
                logging.getLogger("Decompress").info("Unzipping " + ze.filename)
                if ze.is_dir():
                    dir_checker(location, ze.filename)
                else:
                    target = location + ze.filename
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with zin.open(ze) as src, open(target, "wb") as fout:
                        while True:
                            chunk = src.read(1024)
                            if not chunk:
                                break
                            fout.write(chunk)
        logging.getLogger("Unzip").info("Unzipping complete. path :  " + location)
    except Exception as e:
        logging.getLogger("Decompress").error("unzip", exc_info=e)
        logging.getLogger("Unzip").info("Unzipping failed")''',
        "c": r'''#include <stdio.h>

extern void *zip_open(const char *path);
extern int zip_next_entry(void *z, char *name, int nameSize, int *isDir);
extern int zip_read(void *z, char *buffer, int size);
extern void zip_close_entry(void *z);
extern void zip_close(void *z);
extern void dir_checker(const char *location, const char *name);
extern void log_v(const char *tag, const char *msg);
extern void log_d(const char *tag, const char *msg);
extern void log_e(const char *tag, const char *msg);

void unzip(const char *zipFile, const char *location) {
    void *zin = zip_open(zipFile);
    if (zin == NULL) {
        log_e("Decompress", "unzip");
        log_d("Unzip", "Unzipping failed");
        return;
    }
    char name[1024];
    int isDir;
    char path[2048];
    char buffer[1024];
    for (;;) {
        int found = zip_next_entry(zin, name, (int) sizeof(name), &isDir);
        if (found <= 0) break;
        log_v("Decompress", name);
        if (isDir) {
            dir_checker(location, name);
        } else {
            snprintf(path, sizeof(path), "%s%s", location, name);
            FILE *fout = fopen(path, "wb");
            if (fout != NULL) {
                int read;
                while ((read = zip_read(zin, buffer, (int) sizeof(buffer))) > 0)
                    fwrite(buffer, 1, (size_t) read, fout);
                fclose(fout);
            }
            zip_close_entry(zin);
        }
    }
    zip_close(zin);
    log_d("Unzip", "Unzipping complete");
}''',
        "csharp": r'''using System;
using System.IO;
using System.IO.Compression;

public class Unzipper
{
    public void unzip(string zipFile, string location)
    {
        try
        {
            using (ZipArchive archive = ZipFile.OpenRead(zipFile))
            {
                foreach (ZipArchiveEntry entry in archive.Entries)
                {
                    Log("Decompress", "Unzipping " + entry.FullName);
                    if (entry.FullName.EndsWith("/"))
                    {
                        dirChecker(location, entry.FullName);
                    }
                    else
                    {
                        string target = location + entry.FullName;
                        Directory.CreateDirectory(Path.GetDirectoryName(target));
                        using (Stream entryStream = entry.Open())
                        using (FileStream fout = new FileStream(target, FileMode.Create))
                        {
                            byte[] buffer = new byte[1024];
                            int read;
                            while ((read = entryStream.Read(buffer, 0, buffer.Length)) > 0)
                                fout.Write(buffer, 0, read);
                        }
                    }
                }
            }
            Log("Unzip", "Unzipping complete. path :  " + location);
        }
        catch (Exception e)
        {
            Log("Decompress", "unzip: " + e);
            Log("Unzip", "Unzipping failed");
        }
    }

    private void dirChecker(string location, string name)
    {
        Directory.CreateDirectory(location + name);
    }

    private void Log(string tag, string msg)
    {
        Console.WriteLine(tag + ": " + msg);
    }
}'''
    },
    "T837": {
        "python": r'''import threading
import time
import traceback

lock = threading.Condition()
shared = []


def run():
    try:
        with lock:
            for i in range(10):
                while not shared:
                    print("Consumer is waiting")
                    lock.wait()
                k = shared.pop(0)
                print("consume=" + str(k))
                lock.notify_all()
                time.sleep(0.5)
    except Exception as ex:
        traceback.print_exc()''',
        "c": r'''#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

static int queue[100];
static int queueLen = 0;
static pthread_mutex_t listMutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t listCond = PTHREAD_COND_INITIALIZER;

void *run(void *arg) {
    (void) arg;
    pthread_mutex_lock(&listMutex);
    for (int i = 0; i < 10; i++) {
        while (queueLen == 0) {
            printf("Consumer is waiting\n");
            pthread_cond_wait(&listCond, &listMutex);
        }
        int k = queue[0];
        for (int j = 1; j < queueLen; j++) queue[j - 1] = queue[j];
        queueLen--;
        printf("consume=%d\n", k);
        pthread_cond_broadcast(&listCond);
        usleep(500000);
    }
    pthread_mutex_unlock(&listMutex);
    return NULL;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;
using System.Threading;

public class Consumer
{
    private static readonly object list = new object();
    private static readonly Queue<int> queue = new Queue<int>();

    public void run()
    {
        try
        {
            lock (list)
            {
                for (int i = 0; i < 10; i++)
                {
                    while (queue.Count == 0)
                    {
                        Console.WriteLine("Consumer is waiting");
                        Monitor.Wait(list);
                    }
                    int k = queue.Dequeue();
                    Console.WriteLine("consume=" + k);
                    Monitor.PulseAll(list);
                    Thread.Sleep(500);
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.StackTrace);
        }
    }
}'''
    },
    "T692": {
        "python": r'''def find_combinations_count(amount, coins, check_from_index=0):
    if amount == 0:
        return 1
    if amount < 0 or len(coins) == check_from_index:
        return 0
    with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
    without_first_coin = find_combinations_count(amount, coins, check_from_index + 1)
    return with_first_coin + without_first_coin''',
        "c": r'''int findCombinationsCount(int amount, const int *coins, int numCoins, int checkFromIndex) {
    if (amount == 0) return 1;
    if (amount < 0 || numCoins == checkFromIndex) return 0;
    int withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, numCoins, checkFromIndex);
    int withoutFirstCoin = findCombinationsCount(amount, coins, numCoins, checkFromIndex + 1);
    return withFirstCoin + withoutFirstCoin;
}''',
        "csharp": r'''public static class CoinCounter
{
    public static int findCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0) return 1;
        if (amount < 0 || coins.Length == checkFromIndex) return 0;
        int withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = findCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}'''
    },
    "T512": {
        "python": r'''def find_min(a, c):
    x = a[c]
    position = c
    while c < len(a):
        if x > a[c]:
            x = a[c]
            position = c
        c += 1
    return position''',
        "c": r'''#include <stddef.h>

int findMIN(const int *A, int len, int c) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}''',
        "csharp": r'''public static class MinFinder
{
    public static int findMIN(int[] A, int c)
    {
        int x = A[c];
        int position = c;
        while (c < A.Length)
        {
            if (x > A[c])
            {
                x = A[c];
                position = c;
            }
            c++;
        }
        return position;
    }
}'''
    },
    "T14": {
        "python": r'''class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def reverse(self, previous, current):
        if previous is None:
            return None
        if previous is self.head:
            previous.next = None
        if current is None:
            self.head = previous
            return self.head
        temp = current.next
        current.next = previous
        self.reverse(current, temp)
        return None''',
        "c": r'''typedef struct Node {
    int value;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
} List;

Node *list_reverse(List *list, Node *previous, Node *current) {
    if (previous == NULL) return NULL;
    if (previous == list->head) previous->next = NULL;
    if (current == NULL) {
        list->head = previous;
        return list->head;
    }
    Node *temp = current->next;
    current->next = previous;
    list_reverse(list, current, temp);
    return NULL;
}''',
        "csharp": r'''public class Node
{
    public int Value;
    public Node Next;

    public Node getNext() { return Next; }
    public void setNext(Node n) { Next = n; }
}

public class LinkedList
{
    public Node head;

    public Node reverse(Node previous, Node current)
    {
        if (previous == null) return null;
        if (previous == head) previous.setNext(null);
        if (current == null)
        {
            head = previous;
            return head;
        }
        Node temp = current.getNext();
        current.setNext(previous);
        reverse(current, temp);
        return null;
    }
}'''
    }
}
