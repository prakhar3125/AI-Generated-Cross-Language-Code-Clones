DATA3 = {
"T124": {
 "python": r'''def solution(x, a):
    length = len(a)
    if x > length:
        return -1
    is_filled = [0] * x
    jumped = 0
    for i in range(length):
        v = a[i]
        if v <= x:
            if is_filled[v - 1] == 0:
                is_filled[v - 1] = 1
                jumped += 1
                if jumped == x:
                    return i
    return -1''',
 "c": r'''int solution(int X, const int *A, int len) {
    if (X > len) return -1;
    int *isFilled = calloc(X, sizeof(int));
    int jumped = 0;
    for (int i = 0; i < len; i++) {
        int x = A[i];
        if (x >= 1 && x <= X && isFilled[x - 1] == 0) {
            isFilled[x - 1] = 1;
            jumped += 1;
            if (jumped == X) {
                free(isFilled);
                return i;
            }
        }
    }
    free(isFilled);
    return -1;
}''',
 "csharp": r'''public static int Solution(int x, int[] a) {
    int len = a.Length;
    if (x > len) {
        return -1;
    }
    int[] isFilled = new int[x];
    int jumped = 0;
    for (int i = 0; i < len; i++) {
        int v = a[i];
        if (v <= x) {
            if (isFilled[v - 1] == 0) {
                isFilled[v - 1] = 1;
                jumped += 1;
                if (jumped == x) {
                    return i;
                }
            }
        }
    }
    return -1;
}'''
},
"T614": {
 "python": r'''import re

mo_pattern = re.compile(r".*")
LSINSERT = ""

def log_debug(tag, msg):
    print("DEBUG", tag, msg)

def filter(self, source, start, end, dest, dstart, dend):
    lsStart = ""
    lsInsert = ""
    lsEnd = ""
    lsText = ""
    log_debug("debug", mo_pattern.pattern)
    log_debug("debug", "source: " + str(source) + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + str(dest) + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    lsText = str(dest)
    if len(lsText) > 0:
        lsStart = lsText[:dstart]
        log_debug("debug", "lsStart : " + lsStart)
        if source != "":
            lsInsert = str(source)
            log_debug("debug", "lsInsert: " + lsInsert)
        lsEnd = lsText[dend:]
        log_debug("debug", "lsEnd   : " + lsEnd)
        lsText = lsStart + lsInsert + lsEnd
        log_debug("debug", "lsText  : " + lsText)
    matched = mo_pattern.fullmatch(lsText) is not None
    log_debug("debug", "loMatcher.matches(): " + str(matched) + ", lsText: " + lsText)
    if not matched:
        return ""
    return None''',
 "c": r'''extern int pattern_full_match(const char *text);
extern void log_debug(const char *tag, const char *msg);
extern const char *pattern_to_string(void);

const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    char lsStart[1024] = "";
    char lsInsert[1024] = "";
    char lsEnd[1024] = "";
    char lsText[2048] = "";
    char logBuf[4096];
    log_debug("debug", pattern_to_string());
    snprintf(logBuf, sizeof(logBuf), "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d", source, start, end, dest, dstart, dend);
    log_debug("debug", logBuf);
    if (strlen(dest) > 0) {
        strncpy(lsStart, dest, dstart);
        lsStart[dstart] = '\0';
        if (source != NULL && source[0] != '\0') {
            snprintf(lsInsert, sizeof(lsInsert), "%s", source);
            log_debug("debug", lsInsert);
        }
        snprintf(lsEnd, sizeof(lsEnd), "%s", dest + dend);
        log_debug("debug", lsEnd);
        snprintf(lsText, sizeof(lsText), "%s%s%s", lsStart, lsInsert, lsEnd);
        log_debug("debug", lsText);
    }
    if (!pattern_full_match(lsText)) {
        return "";
    }
    return NULL;
}''',
 "csharp": r'''public CharSequence Filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
    String lsStart = "";
    String lsInsert = "";
    String lsEnd = "";
    String lsText = "";
    Log.d("debug", moPattern.ToString());
    Log.d("debug", "source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
    lsText = dest.ToString();
    if (lsText.Length > 0) {
        lsStart = lsText.Substring(0, dstart);
        Log.d("debug", "lsStart : " + lsStart);
        if (source != "") {
            lsInsert = source.ToString();
            Log.d("debug", "lsInsert: " + lsInsert);
        }
        lsEnd = lsText.Substring(dend);
        Log.d("debug", "lsEnd   : " + lsEnd);
        lsText = lsStart + lsInsert + lsEnd;
        Log.d("debug", "lsText  : " + lsText);
    }
    bool matches = Regex.IsMatch(lsText, moPattern.ToString(), RegexOptions.Anchored);
    Log.d("debug", "loMatcher.matches(): " + matches + ", lsText: " + lsText);
    if (!matches) {
        return "";
    }
    return null;
}'''
},
"T592": {
 "python": r'''import random

def rand_nums(self, total, n):
    results = [0] * n
    if total == 0:
        return results
    while True:
        rs = [random.getrandbits(256) for _ in range(n)]
        s = sum(rs)
        if s == 0:
            continue
        for i in range(n):
            results[i] = (s % rs[i]) % (total + 1)
        return results''',
 "c": r'''#include <stdlib.h>

void rand_nums(int total, int n, int *results) {
    if (total == 0) {
        for (int i = 0; i < n; i++) {
            results[i] = 0;
        }
        return;
    }
    unsigned long long rs[64];
    for (;;) {
        unsigned long long sum = 0;
        for (int i = 0; i < n; i++) {
            rs[i] = ((unsigned long long) rand() << 32) | (unsigned long long) rand();
            sum += rs[i];
        }
        if (sum == 0) {
            continue;
        }
        for (int i = 0; i < n; i++) {
            results[i] = (int) ((sum % rs[i]) % (unsigned long long) (total + 1));
        }
        return;
    }
}''',
 "csharp": r'''using System.Numerics;

public static int[] RandNums(int total, int n) {
    var results = new int[n];
    if (total == 0) {
        return results;
    }
    var rs = new BigInteger[n];
    var totalPlus1 = new BigInteger(total + 1L);
    while (true) {
        for (int i = 0; i < n; i++) {
            byte[] bytes = new byte[32];
            rand.NextBytes(bytes);
            bytes[31] &= 0x7F;
            rs[i] = new BigInteger(bytes);
        }
        var sum = BigInteger.Zero;
        foreach (var r in rs) {
            sum += r;
        }
        if (sum == BigInteger.Zero) {
            continue;
        }
        for (int i = 0; i < n; i++) {
            results[i] = (int) (sum % rs[i] % totalPlus1);
        }
        return results;
    }
}'''
},
"T633": {
 "python": r'''import zipfile

def unzip(self):
    try:
        with zipfile.ZipFile(self._zip_file) as zin:
            for ze in zin.infolist():
                print("Decompress", "Unzipping " + ze.filename)
                if ze.filename.endswith("/"):
                    self._dir_checker(ze.filename)
                else:
                    with zin.open(ze) as src, open(self._location + ze.filename, "wb") as fout:
                        while True:
                            chunk = src.read(1024)
                            if not chunk:
                                break
                            fout.write(chunk)
        print("Unzip", "Unzipping complete. path :  " + self._location)
    except Exception as e:
        print("Decompress", "unzip", e)
        print("Unzip", "Unzipping failed")''',
 "c": r'''extern const char *_zipFile;
extern const char *_location;
extern void _dir_checker(const char *path);
extern void log_v(const char *tag, const char *msg);
extern void log_d(const char *tag, const char *msg);
extern void log_e(const char *tag, const char *msg);

typedef struct ZipEntry ZipEntry;
extern ZipEntry *zip_open(const char *path);
extern ZipEntry *zip_next_entry(ZipEntry *z);
extern const char *zip_entry_name(ZipEntry *e);
extern int zip_entry_is_directory(ZipEntry *e);
extern int zip_entry_read(ZipEntry *e, char *buffer, int size);
extern void zip_entry_close(ZipEntry *e);
extern void zip_close(ZipEntry *z);

void unzip(void) {
    char path[1024];
    ZipEntry *zin = zip_open(_zipFile);
    if (zin == NULL) {
        log_e("Decompress", "unzip");
        log_d("Unzip", "Unzipping failed");
        return;
    }
    ZipEntry *ze;
    while ((ze = zip_next_entry(zin)) != NULL) {
        log_v("Decompress", zip_entry_name(ze));
        if (zip_entry_is_directory(ze)) {
            _dir_checker(zip_entry_name(ze));
        } else {
            snprintf(path, sizeof(path), "%s%s", _location, zip_entry_name(ze));
            FILE *fout = fopen(path, "wb");
            char buffer[1024];
            int read;
            while ((read = zip_entry_read(ze, buffer, sizeof(buffer))) > 0) {
                fwrite(buffer, 1, read, fout);
            }
            zip_entry_close(ze);
            fclose(fout);
        }
    }
    zip_close(zin);
    log_d("Unzip", "Unzipping complete");
}''',
 "csharp": r'''using System.IO.Compression;

public void Unzip() {
    try {
        using (var zin = ZipFile.OpenRead(_zipFile)) {
            foreach (var ze in zin.Entries) {
                Console.WriteLine("Unzipping " + ze.FullName);
                if (ze.FullName.EndsWith("/")) {
                    _dirChecker(ze.FullName);
                } else {
                    using (var src = ze.Open())
                    using (var fout = new FileStream(_location + ze.FullName, FileMode.Create))
                    using (var bufout = new BufferedStream(fout)) {
                        byte[] buffer = new byte[1024];
                        int read;
                        while ((read = src.Read(buffer, 0, buffer.Length)) > 0) {
                            bufout.Write(buffer, 0, read);
                        }
                    }
                }
            }
        }
        Console.WriteLine("Unzipping complete. path :  " + _location);
    } catch (Exception e) {
        Console.WriteLine("unzip " + e);
        Console.WriteLine("Unzipping failed");
    }
}'''
},
"T837": {
 "python": r'''import threading
import time

shared_list = []
cond = threading.Condition()

def run(self):
    with cond:
        for _ in range(10):
            while not shared_list:
                print("Consumer is waiting")
                cond.wait()
            k = shared_list.pop(0)
            print("consume=" + str(k))
            cond.notify_all()
            time.sleep(0.5)''',
 "c": r'''#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

extern int list[64];
extern int listSize;
extern pthread_mutex_t listLock;
extern pthread_cond_t listCond;

void *run(void *arg) {
    pthread_mutex_lock(&listLock);
    for (int i = 0; i < 10; i++) {
        while (listSize == 0) {
            printf("Consumer is waiting\n");
            pthread_cond_wait(&listCond, &listLock);
        }
        int k = list[0];
        memmove(list, list + 1, (listSize - 1) * sizeof(int));
        listSize--;
        printf("consume=%d\n", k);
        pthread_cond_broadcast(&listCond);
        struct timespec ts = {0, 500 * 1000 * 1000};
        nanosleep(&ts, NULL);
    }
    pthread_mutex_unlock(&listLock);
    return NULL;
}''',
 "csharp": r'''static readonly object listLock = new object();
static readonly System.Collections.Generic.List<int> sharedList = new System.Collections.Generic.List<int>();

public void Run() {
    lock (listLock) {
        for (int i = 0; i < 10; i++) {
            while (sharedList.Count == 0) {
                Console.WriteLine("Consumer is waiting");
                Monitor.Wait(listLock);
            }
            int k = sharedList[0];
            sharedList.RemoveAt(0);
            Console.WriteLine("consume=" + k);
            Monitor.PulseAll(listLock);
            Thread.Sleep(500);
        }
    }
}'''
},
"T692": {
 "python": r'''def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    elif amount < 0 or len(coins) == check_from_index:
        return 0
    else:
        with_first = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
        without_first = find_combinations_count(amount, coins, check_from_index + 1)
        return with_first + without_first''',
 "c": r'''int findCombinationsCount(int amount, const int *coins, int coinCount, int checkFromIndex) {
    if (amount == 0) return 1;
    else if (amount < 0 || coinCount == checkFromIndex) return 0;
    else {
        int withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, coinCount, checkFromIndex);
        int withoutFirstCoin = findCombinationsCount(amount, coins, coinCount, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}''',
 "csharp": r'''public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex) {
    if (amount == 0) return 1;
    else if (amount < 0 || coins.Length == checkFromIndex) return 0;
    else {
        int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}'''
},
}
