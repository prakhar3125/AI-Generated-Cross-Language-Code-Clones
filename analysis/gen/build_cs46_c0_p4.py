DATA4 = {}

DATA4["T428"] = {
    "python": """def run(proc, out_stream):
    try:
        retValue = proc.wait()
        print("Command exit with return value " + str(retValue))
        out_stream.close()
        out_stream = None
    except (KeyboardInterrupt, OSError) as e:
        print(e)""",
    "c": """extern int proc_wait(void);
extern void outStream_close(void);

void run(void) {
    int retValue = proc_wait();
    if (retValue < 0) {
        perror("process failed");
        return;
    }
    printf("Command exit with return value %d\\n", retValue);
    outStream_close();
}""",
    "csharp": """using System;

public void Run()
{
    try
    {
        int retValue = pro.WaitForExit() ? pro.ExitCode : -1;
        Console.WriteLine("Command exit with return value " + retValue);
        outStream.Close();
        outStream = null;
    }
    catch (Exception e)
    {
        Console.WriteLine(e.StackTrace);
    }
}""",
}

DATA4["T626"] = {
    "python": """def remove_even(k, n):
    counter = 0
    for i in range(n):
        if k[i] % 2 == 1:
            k[counter] = k[i]
            counter += 1
    for i in range(counter, n):
        k[i] = 0""",
    "c": """void removeEven(int *k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 == 1) {
            k[counter++] = k[i];
        }
    }
    for (int i = counter; i < n; i++) {
        k[i] = 0;
    }
}""",
    "csharp": """public static void RemoveEven(int[] k, int n)
{
    int counter = 0;
    for (int i = 0; i < n; i++)
    {
        if (k[i] % 2 == 1)
        {
            k[counter++] = k[i];
        }
    }
    for (int i = counter; i < n; i++)
    {
        k[i] = 0;
    }
}""",
}

DATA4["T813"] = {
    "python": """def to_hex_string(data):
    return "".join("%02x" % (b & 0xFF) for b in data)""",
    "c": """char *toHexString(const unsigned char *bytes, int len) {
    char *hexString = malloc(2 * len + 1);
    for (int i = 0; i < len; i++) {
        sprintf(hexString + 2 * i, "%02x", bytes[i] & 0xFF);
    }
    hexString[2 * len] = '\\0';
    return hexString;
}""",
    "csharp": """using System.Text;

public static string ToHexString(byte[] bytes)
{
    var sb = new StringBuilder(bytes.Length * 2);
    foreach (byte b in bytes)
    {
        sb.Append(b.ToString("x2"));
    }
    return sb.ToString();
}""",
}

DATA4["T333"] = {
    "python": """TOKENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
UNION_SEPARATOR = "-"

class UnitProcessor:
    UNITS = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
             "seventeen", "eighteen", "nineteen"]
    def getName(self, n):
        return self.UNITS[n]

unitProcessor = UnitProcessor()

def getName(value):
    buffer = []
    tensFound = False
    if len(value) > 3:
        number = int(value[-3:], 10)
    else:
        number = int(value, 10)
    number %= 100
    if number >= 20:
        buffer.append(TOKENS[number // 10 - 2])
        number %= 10
        tensFound = True
    if number != 0:
        if tensFound:
            buffer.append(UNION_SEPARATOR)
        buffer.append(unitProcessor.getName(number))
    return "".join(buffer)""",
    "c": """static const char *TOKENS[] = {"twenty", "thirty", "forty", "fifty",
                               "sixty", "seventy", "eighty", "ninety"};
static const char *UNITS[] = {"", "one", "two", "three", "four", "five", "six",
                              "seven", "eight", "nine", "ten", "eleven", "twelve",
                              "thirteen", "fourteen", "fifteen", "sixteen",
                              "seventeen", "eighteen", "nineteen"};

void getName(const char *value, char *out) {
    int number = atoi(value);
    number %= 100;
    char buffer[64] = "";
    int tensFound = 0;
    if (number >= 20) {
        strcat(buffer, TOKENS[number / 10 - 2]);
        number %= 10;
        tensFound = 1;
    }
    if (number != 0) {
        if (tensFound) strcat(buffer, "-");
        strcat(buffer, UNITS[number]);
    }
    strcpy(out, buffer);
}""",
    "csharp": """using System.Text;

public class UnitProcessor
{
    private static readonly string[] UNITS = { "", "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" };
    public string GetName(int n) { return UNITS[n]; }
}

public class TensFormatter
{
    private static readonly string[] TOKENS = { "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety" };
    private const string UNION_SEPARATOR = "-";
    private UnitProcessor unitProcessor = new UnitProcessor();

    public string GetName(string value)
    {
        var buffer = new StringBuilder();
        int number = value.Length > 3
            ? int.Parse(value.Substring(value.Length - 3))
            : int.Parse(value);
        number %= 100;
        bool tensFound = false;
        if (number >= 20)
        {
            buffer.Append(TOKENS[(number / 10) - 2]);
            number %= 10;
            tensFound = true;
        }
        if (number != 0)
        {
            if (tensFound) buffer.Append(UNION_SEPARATOR);
            buffer.Append(unitProcessor.GetName(number));
        }
        return buffer.ToString();
    }
}""",
}

DATA4["T807"] = {
    "python": """def remove_duplicates(s):
    noDupes = []
    for ch in s:
        if ch not in noDupes:
            noDupes.append(ch)
    return "".join(noDupes)""",
    "c": """char *removeDuplicates(const char *s) {
    size_t len = strlen(s);
    char *noDupes = malloc(len + 1);
    int pos = 0;
    for (size_t i = 0; i < len; i++) {
        if (strchr(noDupes, s[i]) == NULL) {
            noDupes[pos++] = s[i];
        }
    }
    noDupes[pos] = '\\0';
    return noDupes;
}""",
    "csharp": """using System.Text;

public static string RemoveDuplicates(string s)
{
    var result = new StringBuilder();
    foreach (char c in s)
    {
        if (!result.ToString().Contains(c))
        {
            result.Append(c);
        }
    }
    return result.ToString();
}""",
}

DATA4["T447"] = {
    "python": """def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    arr1 = sorted(s1)
    arr2 = sorted(s2)
    print("".join(arr1))
    print("".join(arr2))
    return arr1 == arr2""",
    "c": """static int cmpChar(const void *a, const void *b) {
    return *(const char *)a - *(const char *)b;
}

int isAnagram(const char *s1, const char *s2) {
    size_t len1 = strlen(s1), len2 = strlen(s2);
    if (len1 != len2) return 0;
    char *arr1 = strdup(s1), *arr2 = strdup(s2);
    qsort(arr1, len1, 1, cmpChar);
    qsort(arr2, len2, 1, cmpChar);
    printf("%s\\n%s\\n", arr1, arr2);
    int result = strcmp(arr1, arr2) == 0;
    free(arr1);
    free(arr2);
    return result;
}""",
    "csharp": """using System;
using System.Linq;

public bool IsAnagram(string s1, string s2)
{
    if (s1.Length != s2.Length) return false;
    char[] arr1 = s1.ToCharArray();
    char[] arr2 = s2.ToCharArray();
    Array.Sort(arr1);
    Array.Sort(arr2);
    Console.WriteLine(new string(arr1));
    Console.WriteLine(new string(arr2));
    return arr1.SequenceEqual(arr2);
}""",
}

DATA4["T397"] = {
    "python": """import os
import shutil

def copyFolder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            d = os.path.join(dest, os.path.relpath(root, src))
            if not os.path.exists(d):
                os.mkdir(d)
            for f in files:
                shutil.copy(os.path.join(root, f), os.path.join(d, f))
    except Exception as e:
        print(e)""",
    "c": """#include <dirent.h>
#include <sys/stat.h>

void copyFolder(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    if (!dir) {
        perror("opendir failed");
        return;
    }
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
        char sPath[1024], dPath[1024];
        snprintf(sPath, sizeof(sPath), "%s/%s", src, entry->d_name);
        snprintf(dPath, sizeof(dPath), "%s/%s", dest, entry->d_name);
        struct stat st;
        if (stat(sPath, &st) == 0 && S_ISDIR(st.st_mode)) {
            if (mkdir(dPath, 0755) != 0 && errno != EEXIST) {
                perror("mkdir failed");
            }
            copyFolder(sPath, dPath);
        } else {
            FILE *in = fopen(sPath, "rb");
            FILE *out = fopen(dPath, "wb");
            if (in && out) {
                char buf[4096];
                size_t n;
                while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
                    fwrite(buf, 1, n, out);
                }
            }
            if (in) fclose(in);
            if (out) fclose(out);
        }
    }
    closedir(dir);
}""",
    "csharp": """using System;
using System.IO;

public static void CopyFolder(string src, string dest)
{
    try
    {
        foreach (string dirPath in Directory.GetDirectories(src, "*", SearchOption.AllDirectories))
        {
            Directory.CreateDirectory(dirPath.Replace(src, dest));
        }
        foreach (string filePath in Directory.GetFiles(src, "*", SearchOption.AllDirectories))
        {
            File.Copy(filePath, filePath.Replace(src, dest), true);
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex);
    }
}""",
}

DATA4["T430"] = {
    "python": """import time

class Animator:
    def __init__(self, init_margin, clr):
        self.initMargin = init_margin
        self.clr = clr
        self.noColor = 0
        self.count = 0
        self.runs = True

    def changeBtnForegroung(self, color): pass
    def changeBtnMargin(self, margin): pass
    def changePnlBorder(self, border): pass

    def run(self):
        try:
            self.runs = True
            if self.noColor < 2:
                self.noColor += 1
            else:
                self.noColor = 0
            self.changeBtnForegroung(self.clr[self.noColor])
            steps = [(10, (0, 5, 10, 5)), (-10, (0, 0, 10, 10)),
                     (10, (5, 10, 5, 0)), (-10, (10, 10, 0, 0)),
                     (0, (5, 5, 5, 5))]
            for shift, border in steps:
                self.changeBtnMargin((self.initMargin[0], self.initMargin[1] + shift,
                                      self.initMargin[2], self.initMargin[3] - shift))
                self.changePnlBorder(border)
                time.sleep(0.1)
            self.count += 1
        except Exception as e:
            print(e)""",
    "c": """#include <unistd.h>

typedef struct { int top, left, bottom, right; } Insets;

extern void changeBtnForegroung(int color);
extern void changeBtnMargin(Insets m);
extern void changePnlBorder(Insets b);

int noColor = 0;
int clr[3] = {0, 1, 2};
Insets initMargin = {0, 0, 0, 0};
int count = 0;

void run(void) {
    noColor = (noColor < 2) ? noColor + 1 : 0;
    changeBtnForegroung(clr[noColor]);
    Insets margins[5] = {
        {initMargin.top, initMargin.left + 10, initMargin.bottom, initMargin.right - 10},
        {initMargin.top, initMargin.left - 10, initMargin.bottom, initMargin.right + 10},
        {initMargin.top, initMargin.left + 10, initMargin.bottom, initMargin.right - 10},
        {initMargin.top, initMargin.left - 10, initMargin.bottom, initMargin.right + 10},
        initMargin
    };
    Insets borders[5] = {
        {0, 5, 10, 5}, {0, 0, 10, 10}, {5, 10, 5, 0}, {10, 10, 0, 0}, {5, 5, 5, 5}
    };
    for (int i = 0; i < 5; i++) {
        changeBtnMargin(margins[i]);
        changePnlBorder(borders[i]);
        usleep(100000);
    }
    count++;
}""",
    "csharp": """using System;
using System.Threading;
using System.Windows.Forms;

public void Run()
{
    try
    {
        noColor = noColor < 2 ? noColor + 1 : 0;
        changeBtnForegroung(clr[noColor]);
        var steps = new[]
        {
            new { Shift = 10, Border = new Insets(0, 5, 10, 5) },
            new { Shift = -10, Border = new Insets(0, 0, 10, 10) },
            new { Shift = 10, Border = new Insets(5, 10, 5, 0) },
            new { Shift = -10, Border = new Insets(10, 10, 0, 0) },
            new { Shift = 0, Border = new Insets(5, 5, 5, 5) }
        };
        foreach (var step in steps)
        {
            changeBtnMargin(new Insets(initMargin.Top, initMargin.Left + step.Shift,
                                       initMargin.Bottom, initMargin.Right - step.Shift));
            changePnlBorder(step.Border);
            Thread.Sleep(100);
        }
        count++;
    }
    catch (Exception e)
    {
        Console.WriteLine(e);
    }
}""",
}
