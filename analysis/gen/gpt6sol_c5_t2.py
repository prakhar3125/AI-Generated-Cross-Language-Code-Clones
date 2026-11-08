DATA2 = {}

DATA2["T368"] = {
    "python": '''import socket


def is_reachable(address, timeout=5.0):
    socket.setdefaulttimeout(timeout)
    try:
        socket.gethostbyaddr(address)
        return True
    except OSError:
        return False


def main():
    for octets in ([127, 0, 0, 1], [173, 194, 32, 38]):
        inet = ".".join(str(octet) for octet in octets)
        print("Sending Ping Request to " + inet)
        print("Host is reachable" if is_reachable(inet) else "Host is NOT reachable")''',
    "c": '''#include <stdio.h>

typedef struct { unsigned char a; unsigned char b; unsigned char c; unsigned char d; } InetAddress;

InetAddress inet_get_by_address(unsigned char a, unsigned char b, unsigned char c, unsigned char d);
int inet_is_reachable(InetAddress addr, int timeout_ms);

int main(void) {
    InetAddress inet;
    inet = inet_get_by_address(127, 0, 0, 1);
    printf("Sending Ping Request to %u.%u.%u.%u\\n", inet.a, inet.b, inet.c, inet.d);
    printf("%s\\n", inet_is_reachable(inet, 5000) ? "Host is reachable" : "Host is NOT reachable");
    inet = inet_get_by_address(173, 194, 32, 38);
    printf("Sending Ping Request to %u.%u.%u.%u\\n", inet.a, inet.b, inet.c, inet.d);
    printf("%s\\n", inet_is_reachable(inet, 5000) ? "Host is reachable" : "Host is NOT reachable");
    return 0;
}''',
    "csharp": '''using System;
using System.Net;
using System.Net.NetworkInformation;

public static class ReachabilityProbe
{
    public static void Main(string[] args)
    {
        IPAddress inet = IPAddress.Parse("127.0.0.1");
        Console.WriteLine("Sending Ping Request to " + inet);
        Console.WriteLine(new Ping().Send(inet, 5000).Status == IPStatus.Success ? "Host is reachable" : "Host is NOT reachable");
        inet = IPAddress.Parse("173.194.32.38");
        Console.WriteLine("Sending Ping Request to " + inet);
        Console.WriteLine(new Ping().Send(inet, 5000).Status == IPStatus.Success ? "Host is reachable" : "Host is NOT reachable");
    }
}''',
}

DATA2["T305"] = {
    "python": '''class SQLException(Exception):
    pass


class Log:
    @staticmethod
    def info(message, *args):
        print("INFO: " + (message.format(*args) if args else message))

    @staticmethod
    def error(message, *args):
        print("ERROR: " + (message.format(*args) if args else message))

    @staticmethod
    def trace(message, *args):
        print("TRACE: " + (message.format(*args) if args else message))


class Driver:
    def __init__(self, name, class_loader):
        self.name = name
        self.class_loader = class_loader


class DriverManager:
    _drivers = []

    @classmethod
    def get_drivers(cls):
        return list(cls._drivers)

    @classmethod
    def deregister_driver(cls, driver):
        cls._drivers.remove(driver)


def context_destroyed(sce, current_classloader):
    for driver in DriverManager.get_drivers():
        if driver.class_loader == current_classloader:
            try:
                Log.info("Deregistering JDBC driver {}", driver.name)
                DriverManager.deregister_driver(driver)
            except SQLException as ex:
                Log.error("Error deregistering JDBC driver {}", driver.name, ex)
        else:
            Log.trace("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver.name)''',
    "c": '''#include <stddef.h>

typedef struct DriverTag {
    void *class_loader;
    struct DriverTag *next;
} Driver;

void log_info(const char *msg, void *arg);
void log_trace(const char *msg, void *arg);
void driver_manager_deregister_driver(Driver *driver);

void context_destroyed(Driver *head, void *cl) {
    for (Driver *driver = head; driver != NULL; driver = driver->next) {
        if (driver->class_loader == cl) {
            log_info("Deregistering JDBC driver {}", driver);
            driver_manager_deregister_driver(driver);
        } else {
            log_trace("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver);
        }
    }
}''',
    "csharp": '''using System;
using System.Collections.Generic;

public class ManagedDriver
{
    public Type ClrType { get; set; }
}

public static class Log
{
    public static void Info(string message) { Console.WriteLine("INFO: " + message); }
    public static void Error(string message) { Console.WriteLine("ERROR: " + message); }
    public static void Trace(string message) { Console.WriteLine("TRACE: " + message); }
}

public static class DriverManager
{
    public static List<ManagedDriver> Registered { get; } = new List<ManagedDriver>();

    public static void DeregisterDriver(ManagedDriver driver)
    {
        Registered.Remove(driver);
    }
}

public static class LifecycleListener
{
    public static void ContextDestroyed(object sce, Type contextClrType)
    {
        foreach (ManagedDriver driver in DriverManager.Registered.ToArray())
        {
            if (driver.ClrType == contextClrType)
            {
                try
                {
                    Log.Info("Deregistering JDBC driver " + driver.ClrType);
                    DriverManager.DeregisterDriver(driver);
                }
                catch (Exception ex)
                {
                    Log.Error("Error deregistering JDBC driver " + driver.ClrType + " " + ex);
                }
            }
            else
            {
                Log.Trace("Not deregistering JDBC driver " + driver.ClrType + " as it does not belong to this webapp's ClassLoader");
            }
        }
    }
}''',
}

DATA2["T398"] = {
    "python": '''def main():
    print("\\t\\tPlease enter the maximum: ", end="")
    maximum = int(input())
    print("\\t\\tPlease enter the minimum: ", end="")
    minimum = int(input())
    print("enter: ", end="")
    lengthword = input().split()
    countwords = len(lengthword)
    if countwords <= maximum and countwords >= minimum:
        print("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")''',
    "c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    int max, min;
    printf("\\t\\tPlease enter the maximum: ");
    if (scanf("%d", &max) != 1) return 0;
    printf("\\t\\tPlease enter the minimum: ");
    if (scanf("%d", &min) != 1) return 0;
    printf("enter: ");
    char word[1024];
    scanf(" %1023[^\\n]", word);
    int countwords = 0;
    char *token = strtok(word, " \\t");
    while (token != NULL) {
        countwords++;
        token = strtok(NULL, " \\t");
    }
    if (countwords <= max && countwords >= min) {
        printf("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\\n");
    } else {
        printf("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\\n");
    }
    return 0;
}''',
    "csharp": '''using System;

public static class RangeChecker
{
    public static void Main(string[] args)
    {
        Console.Write("\\t\\tPlease enter the maximum: ");
        int max = int.Parse(Console.ReadLine());
        Console.Write("\\t\\tPlease enter the minimum: ");
        int min = int.Parse(Console.ReadLine());
        Console.Write("enter: ");
        string[] lengthword = Console.ReadLine().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
        int countwords = lengthword.Length;
        if (countwords <= max && countwords >= min)
        {
            Console.WriteLine("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
        }
        else
        {
            Console.WriteLine("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
        }
    }
}''',
}

DATA2["T732"] = {
    "python": '''def solution(s, p, q):
    chars = list(s)
    cumulative_answers = [[0] * (len(chars) + 1) for _ in range(4)]
    letter_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    for iii in range(len(chars)):
        if iii > 0:
            for zzz in range(4):
                cumulative_answers[zzz][iii + 1] = cumulative_answers[zzz][iii]
        if chars[iii] in letter_index:
            cumulative_answers[letter_index[chars[iii]]][iii + 1] += 1
    answer = [0] * len(p)
    for iii in range(len(p)):
        for zzz in range(4):
            if (cumulative_answers[zzz][q[iii] + 1] - cumulative_answers[zzz][p[iii]]) > 0:
                answer[iii] = zzz + 1
                break
    return answer''',
    "c": '''#include <stdlib.h>

int *solution(const char *s, const int *p, const int *q, int plen) {
    int clen = 0;
    while (s[clen]) clen++;
    int **cumulative = malloc(4 * sizeof(int *));
    for (int zzz = 0; zzz < 4; zzz++) {
        cumulative[zzz] = calloc(clen + 1, sizeof(int));
    }
    for (int iii = 0; iii < clen; iii++) {
        if (iii > 0) {
            for (int zzz = 0; zzz < 4; zzz++) {
                cumulative[zzz][iii + 1] = cumulative[zzz][iii];
            }
        }
        switch (s[iii]) {
            case 'A': cumulative[0][iii + 1]++; break;
            case 'C': cumulative[1][iii + 1]++; break;
            case 'G': cumulative[2][iii + 1]++; break;
            case 'T': cumulative[3][iii + 1]++; break;
        }
    }
    int *answer = calloc(plen, sizeof(int));
    for (int iii = 0; iii < plen; iii++) {
        for (int zzz = 0; zzz < 4; zzz++) {
            if ((cumulative[zzz][q[iii] + 1] - cumulative[zzz][p[iii]]) > 0) {
                answer[iii] = zzz + 1;
                break;
            }
        }
    }
    for (int zzz = 0; zzz < 4; zzz++) free(cumulative[zzz]);
    free(cumulative);
    return answer;
}''',
    "csharp": '''public static int[] Solution(string s, int[] p, int[] q)
{
    int[] answer = new int[p.Length];
    char[] chars = s.ToCharArray();
    int[][] cumulativeAnswers = new int[4][];
    for (int i = 0; i < 4; i++)
    {
        cumulativeAnswers[i] = new int[chars.Length + 1];
    }
    for (int iii = 0; iii < chars.Length; iii++)
    {
        if (iii > 0)
        {
            for (int zzz = 0; zzz < 4; zzz++)
            {
                cumulativeAnswers[zzz][iii + 1] = cumulativeAnswers[zzz][iii];
            }
        }
        switch (chars[iii])
        {
            case 'A': cumulativeAnswers[0][iii + 1]++; break;
            case 'C': cumulativeAnswers[1][iii + 1]++; break;
            case 'G': cumulativeAnswers[2][iii + 1]++; break;
            case 'T': cumulativeAnswers[3][iii + 1]++; break;
        }
    }
    for (int iii = 0; iii < p.Length; iii++)
    {
        for (int zzz = 0; zzz < 4; zzz++)
        {
            if ((cumulativeAnswers[zzz][q[iii] + 1] - cumulativeAnswers[zzz][p[iii]]) > 0)
            {
                answer[iii] = zzz + 1;
                break;
            }
        }
    }
    return answer;
}''',
}

DATA2["T644"] = {
    "python": '''import re


def filter(source, start, end, dest, dstart, dend, pattern):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = dest.toString() if hasattr(dest, "toString") else str(dest)
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        if source != "":
            ls_insert = str(source)
        ls_end = ls_text[dend:]
        ls_text = ls_start + ls_insert + ls_end
    if not re.fullmatch(pattern, ls_text):
        return ""
    return None''',
    "c": '''#include <string.h>

int regex_full_match(const char *pattern, const char *text);

const char *filter(const char *source, int start, int end,
                   const char *dest, int dstart, int dend) {
    char ls_text[1024];
    const char *ls_insert = "";
    size_t len = strlen(dest);
    if (len > 0) {
        char ls_start[512];
        char ls_end[512];
        size_t head = (size_t) dstart < len ? (size_t) dstart : len;
        size_t tail_start = (size_t) dend < len ? (size_t) dend : len;
        memcpy(ls_start, dest, head);
        ls_start[head] = '\\0';
        if (source[0] != '\\0') {
            ls_insert = source;
        }
        strcpy(ls_end, dest + tail_start);
        snprintf(ls_text, sizeof(ls_text), "%s%s%s", ls_start, ls_insert, ls_end);
    } else {
        ls_text[0] = '\\0';
    }
    if (!regex_full_match("", ls_text)) {
        return "";
    }
    return NULL;
}''',
    "csharp": '''using System.Text.RegularExpressions;

public static class PatternFilter
{
    private static readonly Regex MoPattern = new Regex("");

    public static string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        string lsStart = "";
        string lsInsert = "";
        string lsEnd = "";
        string lsText = dest;
        if (lsText.Length > 0)
        {
            lsStart = lsText.Substring(0, dstart);
            if (source != "")
            {
                lsInsert = source;
            }
            lsEnd = lsText.Substring(dend);
            lsText = lsStart + lsInsert + lsEnd;
        }
        if (!MoPattern.IsMatch(lsText))
        {
            return "";
        }
        return null;
    }
}''',
}

DATA2["T104"] = {
    "python": '''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    s1 = s1.lower()
    s2 = s2.lower()
    sc1 = "".join(sorted(s1))
    sc2 = "".join(sorted(s2))
    return sc1 == sc2''',
    "c": '''#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static int compare_chars(const void *a, const void *b) {
    return *(const char *) a - *(const char *) b;
}

int is_anagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) {
        return 0;
    }
    size_t n = strlen(s1);
    char *c1 = malloc(n + 1);
    char *c2 = malloc(n + 1);
    for (size_t i = 0; i < n; i++) {
        c1[i] = (char) tolower((unsigned char) s1[i]);
        c2[i] = (char) tolower((unsigned char) s2[i]);
    }
    c1[n] = '\\0';
    c2[n] = '\\0';
    qsort(c1, n, sizeof(char), compare_chars);
    qsort(c2, n, sizeof(char), compare_chars);
    int result = strcmp(c1, c2) == 0;
    free(c1);
    free(c2);
    return result;
}''',
    "csharp": '''using System.Linq;

public static class AnagramChecker
{
    public static bool IsAnagram(string s1, string s2)
    {
        if (s1.Length != s2.Length)
        {
            return false;
        }
        string sc1 = string.Concat(s1.ToLower().OrderBy(c => c));
        string sc2 = string.Concat(s2.ToLower().OrderBy(c => c));
        return sc1.Equals(sc2);
    }
}''',
}

DATA2["T417"] = {
    "python": '''def read_data(path, start_byte, chunk_size):
    with open(path, "rb") as raf:
        raf.seek(start_byte)
        data = raf.read(chunk_size)
    if len(data) == chunk_size:
        return data
    return data[:len(data)]''',
    "c": '''#include <stdio.h>
#include <stdlib.h>

unsigned char *read_data(const char *path, long start_byte, int chunk_size, int *out_len) {
    FILE *raf = fopen(path, "rb");
    if (raf == NULL) {
        *out_len = -1;
        return NULL;
    }
    fseek(raf, start_byte, SEEK_SET);
    unsigned char *data = malloc(chunk_size);
    int read = (int) fread(data, 1, chunk_size, raf);
    fclose(raf);
    *out_len = read;
    if (read == chunk_size) {
        return data;
    }
    unsigned char *trimmed = realloc(data, read > 0 ? read : 1);
    return trimmed != NULL ? trimmed : data;
}''',
    "csharp": '''using System.IO;

public static class ChunkReader
{
    public static byte[] ReadData(FileInfo f, int startByte, int chunkSize)
    {
        using (var raf = new FileStream(f.FullName, FileMode.Open, FileAccess.Read))
        {
            raf.Seek(startByte, SeekOrigin.Begin);
            byte[] data = new byte[chunkSize];
            int read = raf.Read(data, 0, chunkSize);
            if (read == data.Length)
            {
                return data;
            }
            byte[] trimmed = new byte[read];
            System.Array.Copy(data, trimmed, read);
            return trimmed;
        }
    }
}''',
}

DATA2["T197"] = {
    "python": '''def solution(n):
    gap = 0
    binary_str = bin(n)[2:]
    zero_arrays = binary_str.split("1")
    print(zero_arrays)
    for zero_array in zero_arrays:
        gap = len(zero_array) if len(zero_array) > gap else gap
    return gap''',
    "c": '''#include <stdio.h>
#include <string.h>

int solution(int n) {
    int gap = 0;
    char binary_str[33];
    int idx = 0;
    if (n == 0) {
        binary_str[idx++] = '0';
    }
    while (n > 0) {
        binary_str[idx++] = (char) ('0' + (n & 1));
        n >>= 1;
    }
    binary_str[idx] = '\\0';
    for (int i = 0; i < idx / 2; i++) {
        char tmp = binary_str[i];
        binary_str[i] = binary_str[idx - 1 - i];
        binary_str[idx - 1 - i] = tmp;
    }
    printf("[");
    for (int i = 0; i < idx; i++) {
        if (binary_str[i] == '1') {
            printf(", ");
        }
    }
    printf("]\\n");
    int start = 0;
    for (int i = 0; i <= idx; i++) {
        if (binary_str[i] == '1' || binary_str[i] == '\\0') {
            int len = i - start;
            if (len > gap) {
                gap = len;
            }
            start = i + 1;
        }
    }
    return gap;
}''',
    "csharp": '''using System;

public static class BinaryGap
{
    public static int Solution(int N)
    {
        int gap = 0;
        string binaryStr = Convert.ToString(N, 2);
        string[] zeroArrays = binaryStr.Split('1');
        Console.WriteLine("[" + string.Join(", ", zeroArrays) + "]");
        foreach (string zeroArray in zeroArrays)
        {
            gap = zeroArray.Length > gap ? zeroArray.Length : gap;
        }
        return gap;
    }
}''',
}
