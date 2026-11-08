PART = []

PART.append({"id": "T710", "task": "translate", "outputs": {
"python": r'''def filter(source, start, end, dest, dstart, dend):
    dot_pos = -1
    length = len(dest)
    for i in range(length):
        c = dest[i]
        if c == "." or c == ",":
            dot_pos = i
            break
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if length - dot_pos > decimal_digits:
            return ""
    return None''',
"c": r'''#include <string.h>

const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    int dot_pos = -1;
    int len = (int) strlen(dest);
    for (int i = 0; i < len; i++) {
        char c = dest[i];
        if (c == '.' || c == ',') {
            dot_pos = i;
            break;
        }
    }
    if (dot_pos >= 0) {
        if (source[0] == '.' && source[1] == '\0') return "";
        if (source[0] == ',' && source[1] == '\0') return "";
        if (dend <= dot_pos) return NULL;
        if (len - dot_pos > decimal_digits) return "";
    }
    return NULL;
}''',
"csharp": r'''public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
    int dotPos = -1;
    int len = dest.Length;
    for (int i = 0; i < len; i++) {
        char c = dest[i];
        if (c == '.' || c == ',') {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0) {
        if (source == "." || source == ",") {
            return "";
        }
        if (dend <= dotPos) {
            return null;
        }
        if (len - dotPos > decimalDigits) {
            return "";
        }
    }
    return null;
}'''}})

PART.append({"id": "T368", "task": "translate", "outputs": {
"python": r'''import socket

def is_reachable(host, timeout_ms):
    try:
        socket.create_connection((host, 7), timeout_ms / 1000).close()
        return True
    except OSError:
        return False

def main():
    inet = socket.inet_ntoa(bytes([127, 0, 0, 1]))
    print("Sending Ping Request to " + inet)
    print("Host is reachable" if is_reachable(inet, 5000) else "Host is NOT reachable")
    inet = socket.inet_ntoa(bytes([173, 194, 32, 38]))
    print("Sending Ping Request to " + inet)
    print("Host is reachable" if is_reachable(inet, 5000) else "Host is NOT reachable")

main()''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

int is_reachable(const char *ip, int timeout_seconds) {
    char cmd[256];
    sprintf(cmd, "ping -c 1 -W %d %s > /dev/null 2>&1", timeout_seconds, ip);
    return system(cmd) == 0;
}

int main(void) {
    printf("Sending Ping Request to 127.0.0.1\n");
    printf("%s\n", is_reachable("127.0.0.1", 5) ? "Host is reachable" : "Host is NOT reachable");
    printf("Sending Ping Request to 173.194.32.38\n");
    printf("%s\n", is_reachable("173.194.32.38", 5) ? "Host is reachable" : "Host is NOT reachable");
    return 0;
}''',
"csharp": r'''using System.Net.NetworkInformation;

static void Main() {
    var first = IPAddress.Parse("127.0.0.1");
    Console.WriteLine("Sending Ping Request to " + first);
    Console.WriteLine(new Ping().Send(first, 5000).Status == IPStatus.Success ? "Host is reachable" : "Host is NOT reachable");
    var second = IPAddress.Parse("173.194.32.38");
    Console.WriteLine("Sending Ping Request to " + second);
    Console.WriteLine(new Ping().Send(second, 5000).Status == IPStatus.Success ? "Host is reachable" : "Host is NOT reachable");
}'''}})

PART.append({"id": "T305", "task": "translate", "outputs": {
"python": r'''class SQLException(Exception):
    pass

class Driver:
    def __init__(self, name, loader):
        self.name = name
        self.loader = loader

class DriverManager:
    drivers = []

    @staticmethod
    def get_drivers():
        return DriverManager.drivers

    @staticmethod
    def deregister(driver):
        DriverManager.drivers.remove(driver)

def log_info(message):
    print(message)

def log_error(message, ex):
    print(message, ex)

def log_trace(message):
    print(message)

def current_context_classloader():
    return None

def context_destroyed(sce):
    cl = current_context_classloader()
    for driver in list(DriverManager.get_drivers()):
        if driver.loader is cl:
            try:
                log_info("Deregistering JDBC driver {}".format(driver))
                DriverManager.deregister(driver)
            except SQLException as ex:
                log_error("Error deregistering JDBC driver {}".format(driver), ex)
        else:
            log_trace("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader".format(driver))''',
"c": r'''#include <stdio.h>

typedef struct Driver {
    const char *name;
    void *class_loader;
    struct Driver *next;
} Driver;

typedef struct {
    Driver *head;
} DriverList;

DriverList driver_manager = { NULL };

void deregister_driver(Driver *driver) {
    Driver **indirect = &driver_manager.head;
    while (*indirect != NULL && *indirect != driver) {
        indirect = &(*indirect)->next;
    }
    if (*indirect != NULL) {
        *indirect = driver->next;
    }
}

void context_destroyed(void *sce, void *cl) {
    Driver *driver = driver_manager.head;
    while (driver != NULL) {
        Driver *next = driver->next;
        if (driver->class_loader == cl) {
            printf("Deregistering JDBC driver %s\n", driver->name);
            deregister_driver(driver);
        } else {
            printf("Not deregistering JDBC driver %s as it does not belong to this webapp's ClassLoader\n", driver->name);
        }
        driver = next;
    }
}''',
"csharp": r'''class SqlException : Exception { }
class Driver { public object ClassLoader; public string Name; }
static class DriverManager {
    public static readonly System.Collections.Generic.List<Driver> Drivers = new System.Collections.Generic.List<Driver>();
    public static System.Collections.Generic.IEnumerable<Driver> GetDrivers() { return Drivers; }
    public static void Deregister(Driver driver) { Drivers.Remove(driver); }
}
static class Log {
    public static void Info(string msg, object o) { Console.WriteLine(msg); }
    public static void Error(string msg, object o, Exception ex) { Console.WriteLine(msg); }
    public static void Trace(string msg, object o) { Console.WriteLine(msg); }
}

public void ContextDestroyed(ServletContextEvent sce) {
    var cl = Thread.CurrentContextClassLoader;
    foreach (var driver in DriverManager.GetDrivers().ToList()) {
        if (driver.ClassLoader == cl) {
            try {
                Log.Info("Deregistering JDBC driver {0}", driver);
                DriverManager.Deregister(driver);
            } catch (SqlException ex) {
                Log.Error("Error deregistering JDBC driver {0}", driver, ex);
            }
        } else {
            Log.Trace("Not deregistering JDBC driver {0} as it does not belong to this webapp's ClassLoader", driver);
        }
    }
}'''}})

PART.append({"id": "T398", "task": "translate", "outputs": {
"python": r'''def main():
    print("\t\tPlease enter the maximum: ")
    maximum = int(input())
    print("\t\tPlease enter the minimum: ")
    minimum = int(input())
    print("enter: ")
    word = input()
    lengthword = word.split()
    countwords = len(lengthword)
    if minimum <= countwords <= maximum:
        print("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")

main()''',
"c": r'''#include <stdio.h>

int count_words(const char *text) {
    int count = 0;
    int in_word = 0;
    for (const char *p = text; *p; p++) {
        if (*p == ' ' || *p == '\t') {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
    }
    return count;
}

int main(void) {
    int maximum;
    int minimum;
    char word[1024];
    printf("\t\tPlease enter the maximum: \n");
    scanf("%d", &maximum);
    printf("\t\tPlease enter the minimum: \n");
    scanf("%d", &minimum);
    printf("enter: \n");
    scanf(" %1023[^\n]", word);
    int countwords = count_words(word);
    if (countwords <= maximum && countwords >= minimum) {
        printf("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\n");
    } else {
        printf("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\n");
    }
    return 0;
}''',
"csharp": r'''static void Main() {
    Console.Write("\t\tPlease enter the maximum: ");
    int max = int.Parse(Console.ReadLine());
    Console.Write("\t\tPlease enter the minimum: ");
    int min = int.Parse(Console.ReadLine());
    Console.Write("enter: ");
    string word = Console.ReadLine();
    var lengthword = word.Split((char[]) null, StringSplitOptions.RemoveEmptyEntries);
    int countwords = lengthword.Length;
    if (countwords <= max && countwords >= min) {
        Console.WriteLine("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
    } else {
        Console.WriteLine("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
    }
}'''}})

PART.append({"id": "T732", "task": "translate", "outputs": {
"python": r'''def solution(s, p, q):
    answer = [0] * len(p)
    chars = list(s)
    cumulative = [[0] * (len(chars) + 1) for _ in range(4)]
    for i in range(len(chars)):
        if i > 0:
            for z in range(4):
                cumulative[z][i + 1] = cumulative[z][i]
        impact = {"A": 0, "C": 1, "G": 2, "T": 3}.get(chars[i])
        if impact is not None:
            cumulative[impact][i + 1] += 1
    for i in range(len(p)):
        for z in range(4):
            if cumulative[z][q[i] + 1] - cumulative[z][p[i]] > 0:
                answer[i] = z + 1
                break
    return answer''',
"c": r'''#include <stdlib.h>
#include <string.h>

int *solution(const char *s, const int *p, const int *q, int query_count) {
    int len = (int) strlen(s);
    int *answer = (int *) calloc((size_t) query_count, sizeof(int));
    static int cumulative[4][512];
    memset(cumulative, 0, sizeof(cumulative));
    for (int i = 0; i < len; i++) {
        if (i > 0) {
            for (int z = 0; z < 4; z++) {
                cumulative[z][i + 1] = cumulative[z][i];
            }
        }
        switch (s[i]) {
            case 'A': cumulative[0][i + 1]++; break;
            case 'C': cumulative[1][i + 1]++; break;
            case 'G': cumulative[2][i + 1]++; break;
            case 'T': cumulative[3][i + 1]++; break;
        }
    }
    for (int i = 0; i < query_count; i++) {
        for (int z = 0; z < 4; z++) {
            if (cumulative[z][q[i] + 1] - cumulative[z][p[i]] > 0) {
                answer[i] = z + 1;
                break;
            }
        }
    }
    return answer;
}''',
"csharp": r'''public static int[] Solution(string s, int[] p, int[] q) {
    var answer = new int[p.Length];
    var chars = s.ToCharArray();
    var cumulative = new int[4][];
    for (int z = 0; z < 4; z++) {
        cumulative[z] = new int[chars.Length + 1];
    }
    for (int i = 0; i < chars.Length; i++) {
        if (i > 0) {
            for (int z = 0; z < 4; z++) {
                cumulative[z][i + 1] = cumulative[z][i];
            }
        }
        switch (chars[i]) {
            case 'A': cumulative[0][i + 1]++; break;
            case 'C': cumulative[1][i + 1]++; break;
            case 'G': cumulative[2][i + 1]++; break;
            case 'T': cumulative[3][i + 1]++; break;
        }
    }
    for (int i = 0; i < p.Length; i++) {
        for (int z = 0; z < 4; z++) {
            if (cumulative[z][q[i] + 1] - cumulative[z][p[i]] > 0) {
                answer[i] = z + 1;
                break;
            }
        }
    }
    return answer;
}'''}})

PART.append({"id": "T644", "task": "translate", "outputs": {
"python": r'''import re
import logging

def filter(source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    logging.debug(str(mo_pattern.pattern))
    logging.debug("source: " + source + ", start: " + str(start) + ", end:" + str(end) + ", dest: " + dest + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = dest
    if len(ls_text) > 0:
        ls_start = ls_text[0:dstart]
        logging.debug("lsStart : " + ls_start)
        if source != "":
            ls_insert = source
            logging.debug("lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        logging.debug("lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        logging.debug("lsText  : " + ls_text)
    lo_match = re.fullmatch(mo_pattern, ls_text)
    logging.debug("match: " + str(lo_match is not None) + ", lsText: " + ls_text)
    if lo_match is None:
        return ""
    return None''',
"c": r'''#include <stdio.h>
#include <string.h>

extern int regex_full_match(const char *text);

const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    char ls_start[256] = "";
    char ls_insert[256] = "";
    char ls_end[256] = "";
    char ls_text[768] = "";
    printf("debug: %s\n", pattern_to_string());
    printf("debug: source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d\n", source, start, end, dest, dstart, dend);
    strcpy(ls_text, dest);
    if (strlen(ls_text) > 0) {
        strncpy(ls_start, ls_text, (size_t) dstart);
        ls_start[dstart] = '\0';
        printf("debug: lsStart : %s\n", ls_start);
        if (source[0] != '\0') {
            strcpy(ls_insert, source);
            printf("debug: lsInsert: %s\n", ls_insert);
        }
        strcpy(ls_end, ls_text + dend);
        printf("debug: lsEnd   : %s\n", ls_end);
        strcpy(ls_text, ls_start);
        strcat(ls_text, ls_insert);
        strcat(ls_text, ls_end);
        printf("debug: lsText  : %s\n", ls_text);
    }
    if (!regex_full_match(ls_text)) {
        return "";
    }
    return NULL;
}''',
"csharp": r'''public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
    string lsStart = "";
    string lsInsert = "";
    string lsEnd = "";
    string lsText = "";
    Debug.WriteLine(moPattern.ToString());
    Debug.WriteLine("source: " + source + ", start: " + start + ", end:" + end + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
    lsText = dest;
    if (lsText.Length > 0) {
        lsStart = lsText.Substring(0, dstart);
        Debug.WriteLine("lsStart : " + lsStart);
        if (source != "") {
            lsInsert = source;
            Debug.WriteLine("lsInsert: " + lsInsert);
        }
        lsEnd = lsText.Substring(dend);
        Debug.WriteLine("lsEnd   : " + lsEnd);
        lsText = lsStart + lsInsert + lsEnd;
        Debug.WriteLine("lsText  : " + lsText);
    }
    if (!moPattern.IsMatch(lsText)) {
        return "";
    }
    return null;
}'''}})

PART.append({"id": "T104", "task": "translate", "outputs": {
"python": r'''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    return sorted(s1.lower()) == sorted(s2.lower())''',
"c": r'''#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static int compare_chars(const void *a, const void *b) {
    return (int) *(const unsigned char *) a - (int) *(const unsigned char *) b;
}

bool is_anagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) {
        return false;
    }
    char a[256];
    char b[256];
    strcpy(a, s1);
    strcpy(b, s2);
    for (char *p = a; *p; p++) *p = (char) tolower((unsigned char) *p);
    for (char *p = b; *p; p++) *p = (char) tolower((unsigned char) *p);
    qsort(a, strlen(a), 1, compare_chars);
    qsort(b, strlen(b), 1, compare_chars);
    return strcmp(a, b) == 0;
}''',
"csharp": r'''using System.Linq;

public static bool IsAnagram(string s1, string s2) {
    if (s1.Length != s2.Length) {
        return false;
    }
    string sc1 = string.Concat(s1.ToLower().OrderBy(c => c));
    string sc2 = string.Concat(s2.ToLower().OrderBy(c => c));
    return sc1.Equals(sc2);
}'''}})

PART.append({"id": "T417", "task": "translate", "outputs": {
"python": r'''def read_data(path, start_byte, chunk_size):
    with open(path, "rb") as raf:
        raf.seek(start_byte)
        data = raf.read(chunk_size)
    if len(data) == chunk_size:
        return data
    return bytes(data[:len(data)])''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char *read_data(const char *path, long start_byte, int chunk_size, int *read_out) {
    FILE *raf = fopen(path, "rb");
    if (raf == NULL) return NULL;
    fseek(raf, start_byte, SEEK_SET);
    unsigned char *data = (unsigned char *) malloc((size_t) chunk_size);
    int read = (int) fread(data, 1, (size_t) chunk_size, raf);
    fclose(raf);
    *read_out = read;
    if (read == chunk_size) {
        return data;
    }
    unsigned char *trimmed = (unsigned char *) malloc(read > 0 ? (size_t) read : 1);
    memcpy(trimmed, data, read > 0 ? (size_t) read : 0);
    free(data);
    return trimmed;
}''',
"csharp": r'''using System.Linq;

public byte[] ReadData(FileInfo f, int startByte, int chunkSize) {
    using (var raf = f.OpenRead()) {
        raf.Seek(startByte, SeekOrigin.Begin);
        var data = new byte[chunkSize];
        int read = raf.Read(data, 0, chunkSize);
        raf.Close();
        if (read == data.Length) {
            return data;
        }
        return data.Take(read).ToArray();
    }
}'''}})

PART.append({"id": "T197", "task": "translate", "outputs": {
"python": r'''def solution(n):
    gap = 0
    binary_str = bin(n)[2:]
    zero_arrays = binary_str.split("1")
    print(zero_arrays)
    for zero_array in zero_arrays:
        gap = len(zero_array) if len(zero_array) > gap else gap
    return gap''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int solution(int n) {
    char binary[65];
    char tmp[65];
    int t = 0;
    unsigned int v = (unsigned int) n;
    if (v == 0) {
        binary[0] = '0';
        binary[1] = '\0';
    } else {
        while (v > 0) {
            tmp[t++] = (char) ('0' + (v & 1));
            v >>= 1;
        }
        int pos = 0;
        while (t > 0) {
            binary[pos++] = tmp[--t];
        }
        binary[pos] = '\0';
    }
    int len = (int) strlen(binary);
    char *zero_arrays[65];
    int count = 0;
    int gap = 0;
    int start = 0;
    for (int i = 0; i <= len; i++) {
        if (i == len || binary[i] == '1') {
            zero_arrays[count] = (char *) malloc((size_t) (i - start) + 1);
            memcpy(zero_arrays[count], binary + start, (size_t) (i - start));
            zero_arrays[count][i - start] = '\0';
            if (i - start > gap) gap = i - start;
            start = i + 1;
            count++;
        }
    }
    printf("[");
    for (int i = 0; i < count; i++) {
        printf("%s%s", i > 0 ? ", " : "", zero_arrays[i]);
    }
    printf("]\n");
    return gap;
}''',
"csharp": r'''public static int Solution(int n) {
    int gap = 0;
    string binaryStr = Convert.ToString(n, 2);
    string[] zeroArrays = binaryStr.Split('1');
    Console.WriteLine("[" + string.Join(", ", zeroArrays) + "]");
    foreach (string zeroArray in zeroArrays) {
        gap = zeroArray.Length > gap ? zeroArray.Length : gap;
    }
    return gap;
}'''}})
