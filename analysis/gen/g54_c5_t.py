# Translation outputs for chunk 5, label gpt-5.4-mini
DATA_T = {}

DATA_T["T422"] = {"outputs": {
"python": r'''def decrypt(s):
    crypt = []
    groups = s.split("#")
    last_index = len(groups) - 1
    for i, group in enumerate(groups):
        j = 0
        if i == last_index and not s.endswith("#"):
            j = len(group)
        if len(group) > 2:
            j = len(group) - 2
        for k in range(j):
            crypt.append(int(group[k:k + 1]))
        if j < len(group):
            crypt.append(int(group[j:]))
    return "".join(chr(ord("a") + c - 1) for c in crypt)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *decrypt(const char *s) {
    char *tmp = strdup(s);
    int ends_hash = s[strlen(s) - 1] == '#';
    int ngroups = 1;
    for (const char *p = s; *p; p++)
        if (*p == '#') ngroups++;
    char *buf = malloc(strlen(s) + 2);
    size_t n = 0;
    int i = 0;
    char *token = strtok(tmp, "#");
    while (token != NULL) {
        int len = (int)strlen(token);
        int j = 0;
        if (i == ngroups - 1 && !ends_hash) j = len;
        if (len > 2) j = len - 2;
        for (int k = 0; k < j; k++)
            buf[n++] = (char)('a' + (token[k] - '0') - 1);
        if (j < len)
            buf[n++] = (char)('a' + atoi(token + j) - 1);
        i++;
        token = strtok(NULL, "#");
    }
    buf[n] = '\0';
    free(tmp);
    return buf;
}''',
"csharp": r'''public static string Decrypt(string s) {
    var crypt = new List<int>();
    string[] groups = s.Split('#');
    for (int i = 0; i < groups.Length; i++) {
        string group = groups[i];
        int j = 0;
        if (i == groups.Length - 1 && !s.EndsWith("#")) j = group.Length;
        if (group.Length > 2) j = group.Length - 2;
        for (int k = 0; k < j; k++) crypt.Add(int.Parse(group.Substring(k, 1)));
        if (j < group.Length) crypt.Add(int.Parse(group.Substring(j)));
    }
    var sb = new StringBuilder(crypt.Count);
    foreach (int c in crypt) sb.Append((char)('a' + c - 1));
    return sb.ToString();
}'''
}}

DATA_T["T515"] = {"outputs": {
"python": r'''class AwtException(Exception):
    pass


class IOException(Exception):
    pass


class Rectangle:
    def __init__(self, size):
        self.size = size


class Toolkit:
    @staticmethod
    def get_default_toolkit():
        return Toolkit()

    def get_screen_size(self):
        return (1920, 1080)


class Robot:
    def create_screen_capture(self, rect):
        return b"image-data"


def write_image(image, fmt, path):
    with open(path, "wb") as fh:
        fh.write(image)


def main():
    try:
        robot = Robot()
        bi = robot.create_screen_capture(Rectangle(Toolkit.get_default_toolkit().get_screen_size()))
        write_image(bi, "jpg", "C:/imageTest.jpg")
    except AwtException as e:
        print(e)
    except IOException as e:
        print(e)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

typedef struct { int width, height; } Rectangle;
typedef struct { Rectangle rect; } BufferedImage;

BufferedImage *robot_createScreenCapture(Rectangle rect) {
    BufferedImage *img = malloc(sizeof(BufferedImage));
    img->rect = rect;
    return img;
}

int imageIO_write(BufferedImage *img, const char *fmt, const char *path) {
    FILE *f = fopen(path, "wb");
    if (f == NULL) return -1;
    fclose(f);
    return 0;
}

int main(void) {
    Rectangle rect = {1920, 1080};
    BufferedImage *bi = robot_createScreenCapture(rect);
    if (imageIO_write(bi, "jpg", "C:/imageTest.jpg") != 0)
        fprintf(stderr, "IOException\n");
    free(bi);
    return 0;
}''',
"csharp": r'''public static void Main() {
    try {
        var robot = new Robot();
        var bounds = System.Windows.Forms.Screen.PrimaryScreen.Bounds;
        var rect = new Rectangle(bounds.Width, bounds.Height);
        var bi = robot.CreateScreenCapture(rect);
        bi.Save("C:/imageTest.jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
    } catch (System.Exception e) {
        System.Console.WriteLine(e);
    }
}'''
}}

DATA_T["T621"] = {"outputs": {
"python": r'''def zero_front(nums):
    if nums is None:
        return None
    result = [0] * len(nums)
    zeroes_pos = 0
    others_pos = len(result) - 1
    for value in nums:
        if value == 0:
            result[zeroes_pos] = 0
            zeroes_pos += 1
        else:
            result[others_pos] = value
            others_pos -= 1
    return result''',
"c": r'''int *zeroFront(const int *nums, int n) {
    if (nums == NULL) return NULL;
    int *result = malloc(n * sizeof(int));
    int zeroesPos = 0;
    int othersPos = n - 1;
    for (int i = 0; i < n; ++i) {
        if (nums[i] == 0) {
            result[zeroesPos++] = 0;
        } else {
            result[othersPos--] = nums[i];
        }
    }
    return result;
}''',
"csharp": r'''public int[] ZeroFront(int[] nums) {
    if (nums == null) return null;
    int[] result = new int[nums.Length];
    int zeroesPos = 0;
    int othersPos = result.Length - 1;
    foreach (int value in nums) {
        if (value == 0) {
            result[zeroesPos++] = 0;
        } else {
            result[othersPos--] = value;
        }
    }
    return result;
}'''
}}

DATA_T["T748"] = {"outputs": {
"python": r'''def main():
    valid = 6
    print("Enter your username: ")
    s = input()
    if len(s) < valid:
        print("Enter a valid username")
        print("User name must contain " + str(valid) + " characters")
        print("Enter again: ")
        s = input()
    print("Username accepted: " + s)
    print("Enter your age: ")
    a = int(input())
    print("Age accepted: " + str(a))
    print("Enter your sex: ")
    sex = input()
    print("Sex accepted: " + sex)''',
"c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const int valid = 6;
    char s[256];
    char sex[64];
    int a;
    printf("Enter your username: \n");
    scanf("%255s", s);
    if ((int)strlen(s) < valid) {
        printf("Enter a valid username\n");
        printf("User name must contain %d characters\n", valid);
        printf("Enter again: \n");
        scanf("%255s", s);
    }
    printf("Username accepted: %s\n", s);
    printf("Enter your age: \n");
    scanf("%d", &a);
    printf("Age accepted: %d\n", a);
    printf("Enter your sex: \n");
    scanf(" %63[^\n]", sex);
    printf("Sex accepted: %s\n", sex);
    return 0;
}''',
"csharp": r'''static void Main(string[] args) {
    const int valid = 6;
    Console.WriteLine("Enter your username: ");
    string s = Console.ReadLine();
    if (s.Length < valid) {
        Console.WriteLine("Enter a valid username");
        Console.WriteLine("User name must contain " + valid + " characters");
        Console.WriteLine("Enter again: ");
        s = Console.ReadLine();
    }
    Console.WriteLine("Username accepted: " + s);
    Console.WriteLine("Enter your age: ");
    int a = int.Parse(Console.ReadLine());
    Console.WriteLine("Age accepted: " + a);
    Console.WriteLine("Enter your sex: ");
    string sex = Console.ReadLine();
    Console.WriteLine("Sex accepted: " + sex);
}'''
}}

DATA_T["T334"] = {"outputs": {
"python": r'''SEPARATOR = " "
EXPONENT = 3


class _WordProcessor:
    def get_name(self, n):
        return ""


unit_processor = _WordProcessor()
tens_processor = _WordProcessor()


class _Scale:
    def get_name(self, exponent):
        return ""


SCALE = _Scale()


def get_name(value):
    buffer = []
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[-4:])
    else:
        number = int(value)
    number %= 1000
    if number >= 100:
        buffer.append(unit_processor.get_name(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(SCALE.get_name(EXPONENT))
    tens_name = tens_processor.get_name(number % 100)
    if tens_name != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tens_name)
    return "".join(buffer)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *SEPARATOR = " ";

static const char *tens_name(int n) { (void)n; return ""; }
static const char *scale_name(int exponent) { (void)exponent; return ""; }
static const char *unit_name(int n) { (void)n; return ""; }

char *get_name(const char *value) {
    char buf[64];
    char tmp[32];
    buf[0] = '\0';
    size_t len = strlen(value);
    int number;
    if (len == 0) {
        number = 0;
    } else if (len > 4) {
        number = atoi(value + len - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        snprintf(tmp, sizeof(tmp), "%d%s", number / 100, SEPARATOR);
        strcat(buf, tmp);
        strcat(buf, scale_name(3));
    }
    const char *tens = tens_name(number % 100);
    if (tens[0] != '\0' && number >= 100) strcat(buf, SEPARATOR);
    strcat(buf, tens);
    return strdup(buf);
}''',
"csharp": r'''public class UnitProcessor { public string GetName(int n) => ""; }
public class TensProcessor { public string GetName(int n) => ""; }
public class ScaleHolder { public string GetName(int exponent) => ""; }

private const string Separator = " ";
private const int Exponent = 3;
private readonly UnitProcessor unitProcessor = new UnitProcessor();
private readonly TensProcessor tensProcessor = new TensProcessor();
private readonly ScaleHolder scale = new ScaleHolder();

public string GetName(string value) {
    var buffer = new StringBuilder();
    int number;
    if (value == "") {
        number = 0;
    } else if (value.Length > 4) {
        number = int.Parse(value.Substring(value.Length - 4));
    } else {
        number = int.Parse(value);
    }
    number %= 1000;
    if (number >= 100) {
        buffer.Append(unitProcessor.GetName(number / 100));
        buffer.Append(Separator);
        buffer.Append(scale.GetName(Exponent));
    }
    string tensName = tensProcessor.GetName(number % 100);
    if (tensName != "" && number >= 100) buffer.Append(Separator);
    buffer.Append(tensName);
    return buffer.ToString();
}'''
}}

DATA_T["T492"] = {"outputs": {
"python": r'''import xml.etree.ElementTree as ET


def main():
    try:
        tree = ET.parse("d:/xml/soap.xml")
    except (ET.ParseError, OSError):
        print("invalid xml")
        return
    root = tree.getroot()
    for part in root.iter("part"):
        for child in part:
            if child.text:
                print(" " + child.tag + " = " + child.text.strip())''',
"c": r'''#include <stdio.h>

typedef struct VTDGen VTDGen;
typedef struct VTDNav VTDNav;
typedef struct AutoPilot AutoPilot;

VTDGen *vtdgen_new(void);
int vtdgen_parseFile(VTDGen *vg, const char *file, int ns);
VTDNav *vtdgen_getNav(VTDGen *vg);
AutoPilot *autopilot_new(void);
void autopilot_selectXPath(AutoPilot *ap, const char *xpath);
void autopilot_bind(AutoPilot *ap, VTDNav *vn);
int autopilot_evalXPath(AutoPilot *ap);
const char *vtdnav_toRawString(VTDNav *vn, int index);
const char *vtdnav_toNormalizedString(VTDNav *vn, int textIndex);
int vtdnav_getText(VTDNav *vn);

int main(void) {
    VTDGen *vg = vtdgen_new();
    AutoPilot *ap = autopilot_new();
    autopilot_selectXPath(ap, "//part/*[text()]");
    if (!vtdgen_parseFile(vg, "d:\\xml\\soap.xml", 0)) {
        printf("invalid xml\n");
        return 0;
    }
    VTDNav *vn = vtdgen_getNav(vg);
    autopilot_bind(ap, vn);
    int i = 0;
    while ((i = autopilot_evalXPath(ap)) != -1) {
        printf(" %s = %s\n", vtdnav_toRawString(vn, i), vtdnav_toNormalizedString(vn, vtdnav_getText(vn)));
    }
    return 0;
}''',
"csharp": r'''public static void Main(string[] s) {
    var doc = new System.Xml.XmlDocument();
    try {
        doc.Load("d:\\xml\\soap.xml");
    } catch (System.Xml.XmlException) {
        Console.WriteLine("invalid xml");
        System.Environment.Exit(0);
    }
    System.Xml.XmlNodeList parts = doc.SelectNodes("//part/*[text()]");
    foreach (System.Xml.XmlNode node in parts) {
        Console.WriteLine(" " + node.Name + " = " + node.InnerText.Trim());
    }
}'''
}}

DATA_T["T484"] = {"outputs": {
"python": r'''import random


def log(message):
    print(message)


def show_random_integer(start, end, rng):
    print(rng.randint(start, end))


def main():
    log("Generating 10 random integers in range 1..10.")
    start = 1
    end = 10
    rng = random.Random()
    for _ in range(10):
        show_random_integer(start, end, rng)
    log("Done")''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void log_message(const char *msg) {
    printf("%s\n", msg);
}

void show_random_integer(int start, int end) {
    printf("%d\n", start + rand() % (end - start + 1));
}

int main(void) {
    srand((unsigned) time(NULL));
    log_message("Generating 10 random integers in range 1..10.");
    int start = 1;
    int end = 10;
    for (int idx = 0; idx < 10; ++idx)
        show_random_integer(start, end);
    log_message("Done");
    return 0;
}''',
"csharp": r'''public static void Log(string message) {
    Console.WriteLine(message);
}

public static void ShowRandomInteger(int start, int end, Random randomGenerator) {
    Console.WriteLine(randomGenerator.Next(start, end + 1));
}

public static void Main(string[] aArgs) {
    Log("Generating 10 random integers in range 1..10.");
    int start = 1;
    int end = 10;
    var randomGenerator = new Random();
    for (int idx = 0; idx < 10; ++idx)
        ShowRandomInteger(start, end, randomGenerator);
    Log("Done");
}'''
}}

DATA_T["T79"] = {"outputs": {
"python": r'''def main():
    items = []
    adding = True
    while adding:
        print("Current list is " + str(items))
        print("Add more? (y/n)")
        if input().startswith("y"):
            print("Enter : ")
            items.append(input())
        else:
            adding = False
    print("List is " + str(items))
    print("Array is " + str(items))''',
"c": r'''#include <stdio.h>

int main(void) {
    char list[100][64];
    int count = 0;
    char answer[8];
    do {
        printf("Current list is [");
        for (int i = 0; i < count; i++)
            printf("%s%s", i > 0 ? ", " : "", list[i]);
        printf("]\n");
        printf("Add more? (y/n)\n");
        scanf("%7s", answer);
        if (answer[0] == 'y') {
            printf("Enter : \n");
            scanf("%63s", list[count]);
            count++;
        } else {
            break;
        }
    } while (1);
    printf("List is [");
    for (int i = 0; i < count; i++)
        printf("%s%s", i > 0 ? ", " : "", list[i]);
    printf("]\n");
    return 0;
}''',
"csharp": r'''static void Main(string[] args) {
    var list = new System.Collections.Generic.List<string>();
    do {
        Console.WriteLine("Current list is " + string.Join(", ", list));
        Console.WriteLine("Add more? (y/n)");
        if (!Console.ReadLine().StartsWith("y"))
            break;
        Console.WriteLine("Enter : ");
        list.Add(Console.ReadLine());
    } while (true);
    string[] arr = list.ToArray();
    Console.WriteLine("List is " + string.Join(", ", list));
    Console.WriteLine("Array is [" + string.Join(", ", arr) + "]");
}'''
}}

DATA_T["T710"] = {"outputs": {
"python": r'''def filter(source, dest, dstart, dend, decimal_digits=2):
    dot_pos = -1
    for i, c in enumerate(dest):
        if c in ".,":
            dot_pos = i
            break
    if dot_pos >= 0:
        if source in (".", ","):
            return ""
        if dend <= dot_pos:
            return None
        if len(dest) - dot_pos > decimal_digits:
            return ""
    return None''',
"c": r'''#include <string.h>

const char *filter(const char *source, const char *dest, int dstart, int dend, int decimalDigits) {
    int dotPos = -1;
    int len = (int)strlen(dest);
    for (int i = 0; i < len; i++) {
        char c = dest[i];
        if (c == '.' || c == ',') {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0)
            return "";
        if (dend <= dotPos)
            return NULL;
        if (len - dotPos > decimalDigits)
            return "";
    }
    return NULL;
}''',
"csharp": r'''private int decimalDigits = 2;

public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
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
        if (source == "." || source == ",") return "";
        if (dend <= dotPos) return null;
        if (len - dotPos > decimalDigits) return "";
    }
    return null;
}'''
}}

DATA_T["T368"] = {"outputs": {
"python": r'''import subprocess


def is_reachable(host):
    result = subprocess.call(["ping", "-c", "1", "-W", "5", host])
    return result == 0


def main():
    for target in ("127.0.0.1", "173.194.32.38"):
        print("Sending Ping Request to " + target)
        print("Host is reachable" if is_reachable(target) else "Host is NOT reachable")''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

int is_reachable(const char *host) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "ping -c 1 -W 5 %s > /dev/null 2>&1", host);
    return system(cmd) == 0;
}

int main(void) {
    const char *targets[] = {"127.0.0.1", "173.194.32.38"};
    for (int i = 0; i < 2; i++) {
        printf("Sending Ping Request to %s\n", targets[i]);
        printf("%s\n", is_reachable(targets[i]) ? "Host is reachable" : "Host is NOT reachable");
    }
    return 0;
}''',
"csharp": r'''public static void Main(string[] args) {
    string[] targets = { "127.0.0.1", "173.194.32.38" };
    foreach (string target in targets) {
        Console.WriteLine("Sending Ping Request to " + target);
        using (var ping = new System.Net.NetworkInformation.Ping()) {
            try {
                var reply = ping.Send(target, 5000);
                Console.WriteLine(reply.Status == System.Net.NetworkInformation.IPStatus.Success
                    ? "Host is reachable"
                    : "Host is NOT reachable");
            } catch (System.Net.NetworkInformation.PingException) {
                Console.WriteLine("Host is NOT reachable");
            }
        }
    }
}'''
}}

DATA_T["T305"] = {"outputs": {
"python": r'''class Driver:
    def __init__(self, name, loader):
        self.name = name
        self.loader = loader


_registered_drivers = []


def register_driver(driver):
    _registered_drivers.append(driver)


def deregister_driver(driver):
    _registered_drivers.remove(driver)


def get_drivers():
    return list(_registered_drivers)


_current_loader = object()


def log(msg, *args):
    print(msg.format(*args) if "{}" in msg else msg)


def context_destroyed(sce):
    cl = _current_loader
    for driver in get_drivers():
        if driver.loader == cl:
            try:
                log("Deregistering JDBC driver {}", driver.name)
                deregister_driver(driver)
            except Exception as ex:
                log("Error deregistering JDBC driver {}", driver.name)
        else:
            log("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver.name)''',
"c": r'''#include <stdio.h>

typedef struct Driver Driver;
struct Driver {
    const char *name;
    void *loader;
};

int drivermanager_getDrivers(Driver *out[], int max);
void drivermanager_deregisterDriver(Driver *driver);

void contextDestroyed(void *sce, void *cl) {
    Driver *drivers[64];
    int count = drivermanager_getDrivers(drivers, 64);
    for (int i = 0; i < count; i++) {
        Driver *driver = drivers[i];
        if (driver->loader == cl) {
            printf("Deregistering JDBC driver %s\n", driver->name);
            drivermanager_deregisterDriver(driver);
        } else {
            printf("Not deregistering JDBC driver %s as it does not belong to this webapp's ClassLoader\n", driver->name);
        }
    }
}''',
"csharp": r'''public void ContextDestroyed(object sce) {
    var cl = System.Threading.Thread.CurrentThread;
    foreach (var driver in DriverManager.GetDrivers()) {
        if (driver.ClassLoader == cl) {
            try {
                Log.Info("Deregistering JDBC driver {0}", driver);
                DriverManager.DeregisterDriver(driver);
            } catch (System.Data.SqlServerCe.SqlCeException ex) {
                Log.Error("Error deregistering JDBC driver {0}", driver);
            }
        } else {
            Log.Trace("Not deregistering JDBC driver {0} as it does not belong to this webapp's ClassLoader", driver);
        }
    }
}'''
}}

DATA_T["T398"] = {"outputs": {
"python": r'''def main():
    maximum = int(input("\t\tPlease enter the maximum: "))
    minimum = int(input("\t\tPlease enter the minimum: "))
    word = input("enter: ")
    words = word.split()
    countwords = len(words)
    if minimum <= countwords <= maximum:
        print("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!")''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    int maximum, minimum;
    char line[1024];
    int countwords = 0;
    printf("\t\tPlease enter the maximum: ");
    scanf("%d", &maximum);
    printf("\t\tPlease enter the minimum: ");
    scanf("%d", &minimum);
    printf("enter: ");
    scanf(" %1023[^\n]", line);
    char *token = strtok(line, " \t");
    while (token != NULL) {
        countwords++;
        token = strtok(NULL, " \t");
    }
    if (countwords <= maximum && countwords >= minimum)
        printf("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\n");
    else
        printf("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!\n");
    return 0;
}''',
"csharp": r'''static void Main(string[] args) {
    Console.Write("\t\tPlease enter the maximum: ");
    int max = int.Parse(Console.ReadLine());
    Console.Write("\t\tPlease enter the minimum: ");
    int min = int.Parse(Console.ReadLine());
    Console.Write("enter: ");
    string word = Console.ReadLine();
    int countwords = word.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
    if (countwords <= max && countwords >= min)
        Console.WriteLine("YAY!!!!!!!!! YOU'RE WTHIN THE RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
    else
        Console.WriteLine("Ohh!!!!!!!!! YOU'RE Not in RAAAANGE!!!!!!!!!!!!!!!!!!!!!!!");
}'''
}}

DATA_T["T732"] = {"outputs": {
"python": r'''def solution(s, p, q):
    chars = s
    cumulative = [[0] * (len(chars) + 1) for _ in range(4)]
    factor_index = {"A": 0, "C": 1, "G": 2, "T": 3}
    for i, ch in enumerate(chars):
        for z in range(4):
            cumulative[z][i + 1] = cumulative[z][i]
        if ch in factor_index:
            cumulative[factor_index[ch]][i + 1] += 1
    answer = [0] * len(p)
    for i in range(len(p)):
        for z in range(4):
            if cumulative[z][q[i] + 1] - cumulative[z][p[i]] > 0:
                answer[i] = z + 1
                break
    return answer''',
"c": r'''#include <stdlib.h>
#include <string.h>
#include <string.h>

#define MAX_SEQ 64

int *solution(const char *s, const int *p, const int *q, int plen) {
    int n = (int)strlen(s);
    static int cumulative[4][MAX_SEQ + 1];
    memset(cumulative, 0, sizeof(cumulative));
    for (int i = 0; i < n && i < MAX_SEQ; i++) {
        for (int z = 0; z < 4; z++)
            cumulative[z][i + 1] = cumulative[z][i];
        switch (s[i]) {
            case 'A': cumulative[0][i + 1]++; break;
            case 'C': cumulative[1][i + 1]++; break;
            case 'G': cumulative[2][i + 1]++; break;
            case 'T': cumulative[3][i + 1]++; break;
        }
    }
    int *answer = malloc(plen * sizeof(int));
    for (int i = 0; i < plen; i++) {
        answer[i] = 0;
        for (int z = 0; z < 4; z++) {
            if (cumulative[z][q[i] + 1] - cumulative[z][p[i]] > 0) {
                answer[i] = z + 1;
                break;
            }
        }
    }
    return answer;
}''',
"csharp": r'''public int[] Solution(string s, int[] p, int[] q) {
    int[] answer = new int[p.Length];
    char[] chars = s.ToCharArray();
    int[][] cumulative = new int[4][];
    for (int z = 0; z < 4; z++) cumulative[z] = new int[chars.Length + 1];
    for (int i = 0; i < chars.Length; i++) {
        for (int z = 0; z < 4; z++) cumulative[z][i + 1] = cumulative[z][i];
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
}'''
}}

DATA_T["T644"] = {"outputs": {
"python": r'''import re

mo_pattern = re.compile(r"[0-9]*[.,]?[0-9]*")


def log_debug(tag, message):
    print(message)


def filter_text(source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    ls_text = ""
    log_debug("debug", mo_pattern.pattern)
    log_debug("debug", "source: " + source + ", start: " + str(start)
              + ", end:" + str(end) + ", dest: " + dest
              + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = dest
    if len(ls_text) > 0:
        ls_start = ls_text[0:dstart]
        log_debug("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = source
            log_debug("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        log_debug("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        log_debug("debug", "lsText  : " + ls_text)
    matched = mo_pattern.fullmatch(ls_text) is not None
    log_debug("debug", "loMatcher.matches(): " + str(matched) + ", lsText: " + ls_text)
    if not matched:
        return ""
    return None''',
"c": r'''#include <string.h>
#include <stdio.h>

typedef struct Matcher Matcher;

void log_d(const char *tag, const char *msg);
const char *pattern_toString(void);
Matcher *pattern_matcher(const char *text);
int matcher_matches(Matcher *m);

const char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    char lsStart[256] = "";
    char lsInsert[256] = "";
    char lsEnd[256] = "";
    char lsText[512] = "";
    char msg[1024];
    log_d("debug", pattern_toString());
    snprintf(msg, sizeof(msg), "source: %s, start: %d, end:%d, dest: %s, dstart: %d, dend: %d",
             source, start, end, dest, dstart, dend);
    log_d("debug", msg);
    strcpy(lsText, dest);
    if (strlen(lsText) > 0) {
        strncpy(lsStart, lsText, dstart);
        lsStart[dstart] = '\0';
        log_d("debug", lsStart);
        if (strcmp(source, "") != 0) {
            strcpy(lsInsert, source);
            log_d("debug", lsInsert);
        }
        strcpy(lsEnd, lsText + dend);
        log_d("debug", lsEnd);
        strcpy(lsText, lsStart);
        strcat(lsText, lsInsert);
        strcat(lsText, lsEnd);
        log_d("debug", lsText);
    }
    Matcher *loMatcher = pattern_matcher(lsText);
    snprintf(msg, sizeof(msg), "loMatcher.matches(): %d, lsText: %s", matcher_matches(loMatcher), lsText);
    log_d("debug", msg);
    if (!matcher_matches(loMatcher)) return "";
    return NULL;
}''',
"csharp": r'''private static readonly System.Text.RegularExpressions.Regex moPattern =
    new System.Text.RegularExpressions.Regex("[0-9]*[.,]?[0-9]*");

public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
    string lsStart = "";
    string lsInsert = "";
    string lsEnd = "";
    string lsText = "";
    Log.D("debug", moPattern.ToString());
    Log.D("debug", "source: " + source + ", start: " + start + ", end:" + end
        + ", dest: " + dest + ", dstart: " + dstart + ", dend: " + dend);
    lsText = dest;
    if (lsText.Length > 0) {
        lsStart = lsText.Substring(0, dstart);
        Log.D("debug", "lsStart : " + lsStart);
        if (source != "") {
            lsInsert = source;
            Log.D("debug", "lsInsert: " + lsInsert);
        }
        lsEnd = lsText.Substring(dend);
        Log.D("debug", "lsEnd   : " + lsEnd);
        lsText = lsStart + lsInsert + lsEnd;
        Log.D("debug", "lsText  : " + lsText);
    }
    var loMatcher = moPattern.Match(lsText);
    Log.D("debug", "loMatcher.matches(): " + loMatcher.Success + ", lsText: " + lsText);
    if (!loMatcher.Success) return "";
    return null;
}'''
}}

DATA_T["T104"] = {"outputs": {
"python": r'''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    return sorted(s1.lower()) == sorted(s2.lower())''',
"c": r'''#include <string.h>
#include <stdlib.h>
#include <ctype.h>

static int cmp_char(const void *a, const void *b) {
    return *(const char *) a - *(const char *) b;
}

int isAnagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) return 0;
    char *a = strdup(s1);
    char *b = strdup(s2);
    for (char *p = a; *p; p++) *p = (char) tolower((unsigned char) *p);
    for (char *p = b; *p; p++) *p = (char) tolower((unsigned char) *p);
    qsort(a, strlen(a), 1, cmp_char);
    qsort(b, strlen(b), 1, cmp_char);
    int result = strcmp(a, b) == 0;
    free(a);
    free(b);
    return result;
}''',
"csharp": r'''public static bool IsAnagram(string s1, string s2) {
    if (s1.Length != s2.Length) return false;
    char[] c1 = s1.ToLower().ToCharArray();
    char[] c2 = s2.ToLower().ToCharArray();
    Array.Sort(c1);
    Array.Sort(c2);
    return new string(c1) == new string(c2);
}'''
}}

DATA_T["T417"] = {"outputs": {
"python": r'''def read_data(path, start_byte, chunk_size):
    fh = open(path, "rb")
    try:
        fh.seek(start_byte)
        data = fh.read(chunk_size)
    finally:
        fh.close()
    if len(data) == chunk_size:
        return data
    return data[:len(data)]''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

unsigned char *readData(const char *path, long startByte, int chunkSize, int *readOut) {
    FILE *raf = fopen(path, "rb");
    if (raf == NULL) return NULL;
    fseek(raf, startByte, SEEK_SET);
    unsigned char *data = malloc(chunkSize);
    int read = (int) fread(data, 1, chunkSize, raf);
    fclose(raf);
    *readOut = read;
    if (read == chunkSize) return data;
    if (read > 0) return realloc(data, read);
    free(data);
    return NULL;
}''',
"csharp": r'''public byte[] ReadData(System.IO.FileInfo f, int startByte, int chunkSize) {
    using (var fs = f.OpenRead()) {
        fs.Seek(startByte, System.IO.SeekOrigin.Begin);
        byte[] data = new byte[chunkSize];
        int read = fs.Read(data, 0, chunkSize);
        if (read == data.Length) return data;
        byte[] result = new byte[read];
        Array.Copy(data, result, read);
        return result;
    }
}'''
}}

DATA_T["T197"] = {"outputs": {
"python": r'''def solution(n):
    binary_str = bin(n)[2:]
    zero_arrays = binary_str.split("1")
    print(zero_arrays)
    gap = 0
    for zero_array in zero_arrays:
        gap = max(len(zero_array), gap)
    return gap''',
"c": r'''int solution(int n) {
    char binary[33];
    int idx = 0;
    unsigned int value = (unsigned int) n;
    while (value > 0) {
        binary[idx++] = (char) ('0' + (value & 1u));
        value >>= 1;
    }
    binary[idx] = '\0';
    int gap = 0;
    int current = 0;
    for (int i = 0; i < idx; i++) {
        if (binary[i] == '1') {
            if (current > gap) gap = current;
            current = 0;
        } else {
            current++;
        }
    }
    if (current > gap) gap = current;
    return gap;
}''',
"csharp": r'''public static int Solution(int n) {
    string binaryStr = Convert.ToString(n, 2);
    string[] zeroArrays = binaryStr.Split('1');
    Console.WriteLine("[" + string.Join(", ", zeroArrays) + "]");
    int gap = 0;
    foreach (string zeroArray in zeroArrays) {
        gap = Math.Max(zeroArray.Length, gap);
    }
    return gap;
}'''
}}

DATA_T["T752"] = {"outputs": {
"python": r'''import xml.etree.ElementTree as ET


def main():
    try:
        tree = ET.parse("input.xml")
    except (ET.ParseError, OSError):
        return
    for item in tree.getroot().iter("item"):
        name = item.get("name")
        if name is not None:
            print(" item name is ===>" + name)''',
"c": r'''#include <stdio.h>

typedef struct VTDGen VTDGen;
typedef struct VTDNav VTDNav;
typedef struct AutoPilot AutoPilot;

VTDGen *vtdgen_new(void);
int vtdgen_parseFile(VTDGen *vg, const char *file, int ns);
VTDNav *vtdgen_getNav(VTDGen *vg);
AutoPilot *autopilot_newForNav(VTDNav *vn);
void autopilot_selectXPath(AutoPilot *ap, const char *xpath);
int autopilot_evalXPath(AutoPilot *ap);
const char *vtdnav_toString(VTDNav *vn, int index);

int main(void) {
    VTDGen *vg = vtdgen_new();
    if (!vtdgen_parseFile(vg, "input.xml", 0)) return 0;
    VTDNav *vn = vtdgen_getNav(vg);
    AutoPilot *ap = autopilot_newForNav(vn);
    autopilot_selectXPath(ap, "/xml/item/@name");
    int i = 0;
    while ((i = autopilot_evalXPath(ap)) != -1) {
        printf(" item name is ===>%s\n", vtdnav_toString(vn, i + 1));
    }
    return 0;
}''',
"csharp": r'''public static void Main(string[] s) {
    var doc = new System.Xml.XmlDocument();
    try {
        doc.Load("input.xml");
    } catch (System.Xml.XmlException) {
        return;
    }
    System.Xml.XmlNodeList names = doc.SelectNodes("/xml/item/@name");
    foreach (System.Xml.XmlNode attr in names) {
        Console.WriteLine(" item name is ===>" + attr.Value);
    }
}'''
}}

DATA_T["T410"] = {"outputs": {
"python": r'''def main():
    red = int(input("Please enter the red color. Range [0, 255] only please.\n"))
    green = int(input("Please enter the green color. Range [0, 255] only please.\n"))
    blue = int(input("Please enter the blue color. Range [0, 255] only please.\n"))
    code = red * 256 ** 2 + green * 256 + blue
    print("The code is " + str(code) + ".")
    red = (code & 0xFF0000) >> 16
    green = (code & 0xFF00) >> 8
    blue = code & 0xFF
    print("Your red value is: " + str(red))
    print("Your green value is: " + str(green))
    print("Your blue value is: " + str(blue))''',
"c": r'''#include <stdio.h>

int main(void) {
    int code;
    int red, green, blue;
    const int rMask = 0xFF0000, gMask = 0xFF00, bMask = 0xFF;
    printf("Please enter the red color. Range [0, 255] only please.\n");
    scanf("%d", &red);
    printf("Please enter the green color. Range [0, 255] only please.\n");
    scanf("%d", &green);
    printf("Please enter the blue color. Range [0, 255] only please.\n");
    scanf("%d", &blue);
    code = 0;
    code += red << 16;
    code += green << 8;
    code += blue;
    printf("The code is %d.\n", code);
    red = 0;
    green = 0;
    blue = 0;
    red = (code & rMask) >> 16;
    green = (code & gMask) >> 8;
    blue = code & bMask;
    printf("Your red value is: %d\n", red);
    printf("Your green value is: %d\n", green);
    printf("Your blue value is: %d\n", blue);
    return 0;
}''',
"csharp": r'''static void Main(string[] args) {
    Console.WriteLine("Please enter the red color. Range [0, 255] only please.");
    int red = int.Parse(Console.ReadLine());
    Console.WriteLine("Please enter the green color. Range [0, 255] only please.");
    int green = int.Parse(Console.ReadLine());
    Console.WriteLine("Please enter the blue color. Range [0, 255] only please.");
    int blue = int.Parse(Console.ReadLine());
    int code = (red << 16) + (green << 8) + blue;
    Console.WriteLine("The code is " + code + ".");
    red = (code & 0xFF0000) >> 16;
    green = (code & 0xFF00) >> 8;
    blue = code & 0xFF;
    Console.WriteLine("Your red value is: " + red);
    Console.WriteLine("Your green value is: " + green);
    Console.WriteLine("Your blue value is: " + blue);
}'''
}}

DATA_T["T858"] = {"outputs": {
"python": r'''class HSSFFont:
    def __init__(self):
        self.boldweight = None
        self.char_set = None
        self.color = None
        self.font_name = None
        self.font_height = None
        self.italic = None
        self.strikeout = None
        self.type_offset = None
        self.underline = None

    def set_boldweight(self, v): self.boldweight = v
    def set_char_set(self, v): self.char_set = v
    def set_color(self, v): self.color = v
    def set_font_name(self, v): self.font_name = v
    def set_font_height(self, v): self.font_height = v
    def set_italic(self, v): self.italic = v
    def set_strikeout(self, v): self.strikeout = v
    def set_type_offset(self, v): self.type_offset = v
    def set_underline(self, v): self.underline = v


class XSSFFont:
    def __init__(self):
        self.boldweight = None
        self.char_set = None
        self.color = None
        self.font_name = None
        self.font_height = None
        self.italic = None
        self.strikeout = None
        self.type_offset = None
        self.underline = None

    def get_boldweight(self): return self.boldweight
    def get_char_set(self): return self.char_set
    def get_color(self): return self.color
    def get_font_name(self): return self.font_name
    def get_font_height(self): return self.font_height
    def get_italic(self): return self.italic
    def get_strikeout(self): return self.strikeout
    def get_type_offset(self): return self.type_offset
    def get_underline(self): return self.underline


class HSSFWorkbook:
    def create_font(self):
        return HSSFFont()


def transform(workbook_new, font_old):
    font_new = workbook_new.create_font()
    for attr in ("boldweight", "char_set", "color", "font_name", "font_height",
                 "italic", "strikeout", "type_offset", "underline"):
        getattr(font_new, "set_" + attr)(getattr(font_old, "get_" + attr)())
    return font_new''',
"c": r'''#include <stdlib.h>
#include <string.h>

typedef struct HSSFWorkbook HSSFWorkbook;

typedef struct {
    int boldweight, charSet, color;
    char fontName[64];
    double fontHeight;
    int italic, strikeout, typeOffset, underline;
} HSSFFont;

HSSFFont *workbookCreateFont(HSSFWorkbook *wb);

HSSFFont *transform(HSSFWorkbook *workbookNew, const HSSFFont *fontOld) {
    HSSFFont *fontNew = workbookCreateFont(workbookNew);
    fontNew->boldweight = fontOld->boldweight;
    fontNew->charSet = fontOld->charSet;
    fontNew->color = fontOld->color;
    strcpy(fontNew->fontName, fontOld->fontName);
    fontNew->fontHeight = fontOld->fontHeight;
    fontNew->italic = fontOld->italic;
    fontNew->strikeout = fontOld->strikeout;
    fontNew->typeOffset = fontOld->typeOffset;
    fontNew->underline = fontOld->underline;
    return fontNew;
}''',
"csharp": r'''public class HSSFFont {
    public int Boldweight { get; set; }
    public int CharSet { get; set; }
    public int Color { get; set; }
    public string FontName { get; set; }
    public double FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public int TypeOffset { get; set; }
    public int Underline { get; set; }
}

public class XSSFFont {
    public int Boldweight { get; set; }
    public int CharSet { get; set; }
    public int Color { get; set; }
    public string FontName { get; set; }
    public double FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public int TypeOffset { get; set; }
    public int Underline { get; set; }
}

public class HSSFWorkbook {
    public HSSFFont CreateFont() => new HSSFFont();
}

private HSSFFont Transform(HSSFWorkbook workbookNew, XSSFFont fontOld) {
    HSSFFont fontNew = workbookNew.CreateFont();
    fontNew.Boldweight = fontOld.Boldweight;
    fontNew.CharSet = fontOld.CharSet;
    fontNew.Color = fontOld.Color;
    fontNew.FontName = fontOld.FontName;
    fontNew.FontHeight = fontOld.FontHeight;
    fontNew.Italic = fontOld.Italic;
    fontNew.Strikeout = fontOld.Strikeout;
    fontNew.TypeOffset = fontOld.TypeOffset;
    fontNew.Underline = fontOld.Underline;
    return fontNew;
}'''
}}

DATA_T["T145"] = {"outputs": {
"python": r'''def solution(x, a):
    seen = set()
    target_sum = x * (x + 1) // 2
    running = 0
    for i, value in enumerate(a):
        if value <= x and value not in seen:
            seen.add(value)
            running += value
            if running == target_sum:
                return i
    return -1''',
"c": r'''#include <stdlib.h>

int solution(int x, const int *a, int n) {
    int target = x * (x + 1) / 2;
    int sum = 0;
    int *seen = calloc(x + 1, sizeof(int));
    for (int i = 0; i < n; i++) {
        if (a[i] <= x && a[i] >= 0 && !seen[a[i]]) {
            seen[a[i]] = 1;
            sum += a[i];
            if (sum == target) {
                free(seen);
                return i;
            }
        }
    }
    free(seen);
    return -1;
}''',
"csharp": r'''public int Solution(int x, int[] a) {
    var seen = new HashSet<int>();
    int targetSum = x * (x + 1) / 2;
    int sum = 0;
    for (int i = 0; i < a.Length; i++) {
        if (a[i] <= x && seen.Add(a[i])) {
            sum += a[i];
            if (sum == targetSum) return i;
        }
    }
    return -1;
}'''
}}

DATA_T["T65"] = {"outputs": {
"python": r'''class JDialog:
    def __init__(self, title, displayable):
        self.title = title
        self.displayable = displayable


_windows = [JDialog("Save", True), JDialog("Open", False)]


def get_windows():
    return _windows


def action_performed(e):
    print()
    print("Display Dialogs")
    for window in get_windows():
        if isinstance(window, JDialog):
            print("\t" + window.title + " " + str(window.displayable))''',
"c": r'''#include <stdio.h>

typedef struct {
    const char *title;
    int displayable;
} JDialog;

static JDialog dialogWindows[8] = {
    {"Save", 1},
    {"Open", 0}
};

void actionPerformed(void) {
    printf("\n");
    printf("Display Dialogs\n");
    for (int i = 0; i < 2; i++) {
        printf("\t%s %d\n", dialogWindows[i].title, dialogWindows[i].displayable);
    }
}''',
"csharp": r'''public class JDialogStub {
    public string Title { get; set; }
    public bool IsDisplayable() => true;
}

public static class WindowHost {
    public static System.Collections.Generic.List<object> GetWindows() => new System.Collections.Generic.List<object>();
}

public void ActionPerformed(object e) {
    Console.WriteLine();
    Console.WriteLine("Display Dialogs");
    foreach (var window in WindowHost.GetWindows()) {
        if (window is JDialogStub dialog) {
            Console.WriteLine("\t" + dialog.Title + " " + dialog.IsDisplayable());
        }
    }
}'''
}}

DATA_T["T239"] = {"outputs": {
"python": r'''def main():
    test = "The quick brown fox jumped over the lazy dog."
    count_a = 0
    count_o = 0
    count_space = 0
    count_dot = 0
    for ch in test:
        if ch in ("a", "A"):
            count_a += 1
        elif ch in ("o", "O"):
            count_o += 1
        elif ch == " ":
            count_space += 1
        elif ch == ".":
            count_dot += 1
    print("A: %d\nO: %d\nSpace: %d\nDot: %d" % (count_a, count_o, count_space, count_dot))''',
"c": r'''#include <stdio.h>

int main(void) {
    const char *test = "The quick brown fox jumped over the lazy dog.";
    int countA = 0, countO = 0, countSpace = 0, countDot = 0;
    for (const char *p = test; *p; ++p) {
        switch (*p) {
            case 'a':
            case 'A':
                countA++;
                break;
            case 'o':
            case 'O':
                countO++;
                break;
            case ' ':
                countSpace++;
                break;
            case '.':
                countDot++;
                break;
        }
    }
    printf("A: %d\nO: %d\nSpace: %d\nDot: %d", countA, countO, countSpace, countDot);
    return 0;
}''',
"csharp": r'''public static void Main(string[] args) {
    string test = "The quick brown fox jumped over the lazy dog.";
    int countA = 0, countO = 0, countSpace = 0, countDot = 0;
    foreach (char ch in test) {
        switch (ch) {
            case 'a':
            case 'A':
                countA++;
                break;
            case 'o':
            case 'O':
                countO++;
                break;
            case ' ':
                countSpace++;
                break;
            case '.':
                countDot++;
                break;
        }
    }
    Console.WriteLine("A: {0}\nO: {1}\nSpace: {2}\nDot: {3}", countA, countO, countSpace, countDot);
}'''
}}

DATA_T["T94"] = {"outputs": {
"python": r'''def read_bytes(inputStream):
    chunks = bytearray()
    while True:
        chunk = inputStream.read(32 * 1024)
        if not chunk:
            break
        chunks.extend(chunk)
    return bytes(chunks)''',
"c": r'''#include <stdlib.h>

typedef struct InputStream InputStream;

int stream_read(InputStream *stream, unsigned char *buf, int len);

unsigned char *readBytes(InputStream *inputStream, int *outLen) {
    size_t capacity = 32 * 1024;
    unsigned char *buffer = malloc(capacity);
    size_t size = 0;
    for (;;) {
        if (size == capacity) {
            capacity *= 2;
            buffer = realloc(buffer, capacity);
        }
        int read = stream_read(inputStream, buffer + size, (int) (capacity - size));
        if (read == -1) break;
        size += (size_t) read;
    }
    *outLen = (int) size;
    return buffer;
}''',
"csharp": r'''public static byte[] ReadBytes(System.IO.Stream inputStream) {
    using (var ms = new System.IO.MemoryStream()) {
        byte[] buffer = new byte[32 * 1024];
        int read;
        while ((read = inputStream.Read(buffer, 0, buffer.Length)) > 0) {
            ms.Write(buffer, 0, read);
        }
        return ms.ToArray();
    }
}'''
}}

DATA_T["T749"] = {"outputs": {
"python": r'''class Node:
    def __init__(self, parent):
        self.parent = parent


class Pane:
    def __init__(self):
        self.children = []


class HTMLEditor(Pane):
    def lookup(self, css_selector):
        return Node(self)


class Scene:
    def __init__(self, root):
        self.root = root


class Stage:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def show(self):
        pass


def start(primary_stage):
    html_editor = HTMLEditor()
    primary_stage.set_scene(Scene(html_editor))
    primary_stage.show()
    tool_bar = html_editor.lookup(".tool-bar")
    while tool_bar is not None:
        tool_bar.parent.children.remove(tool_bar)
        tool_bar = html_editor.lookup(".tool-bar")''',
"c": r'''#include <stddef.h>

typedef struct Node Node;
typedef struct Pane Pane;
typedef struct HTMLEditor HTMLEditor;
typedef struct Stage Stage;
typedef struct Scene Scene;

HTMLEditor *htmleditor_create(void);
Scene *scene_create(void *root);
void stage_setScene(Stage *stage, Scene *scene);
void stage_show(Stage *stage);
Node *htmleditor_lookup(HTMLEditor *editor, const char *selector);
Node *node_getParent(Node *node);
void pane_removeChild(Pane *pane, Node *child);

void start(Stage *primaryStage) {
    HTMLEditor *htmlEditor = htmleditor_create();
    stage_setScene(primaryStage, scene_create(htmlEditor));
    stage_show(primaryStage);
    Node *toolBar = htmleditor_lookup(htmlEditor, ".tool-bar");
    while (toolBar != NULL) {
        pane_removeChild((Pane *) node_getParent(toolBar), toolBar);
        toolBar = htmleditor_lookup(htmlEditor, ".tool-bar");
    }
}''',
"csharp": r'''public class NodeStub { public object GetParent() => null; }
public class PaneStub { public System.Collections.Generic.List<NodeStub> GetChildren() => new System.Collections.Generic.List<NodeStub>(); }
public class HTMLEditorStub : PaneStub { public NodeStub Lookup(string css) => null; }
public class SceneStub { public SceneStub(object root) { Root = root; } public object Root { get; } }
public class StageStub { public SceneStub Scene { get; set; } public void Show() { } }

public void Start(StageStub primaryStage) {
    var htmlEditor = new HTMLEditorStub();
    primaryStage.Scene = new SceneStub(htmlEditor);
    primaryStage.Show();
    NodeStub toolBar = htmlEditor.Lookup(".tool-bar");
    while (toolBar != null) {
        toolBar = htmlEditor.Lookup(".tool-bar");
    }
}'''
}}
