PART = []

PART.append({"id": "T422", "task": "translate", "outputs": {
"python": r'''def decrypt(s):
    crypt = []
    groups = s.split("#")
    for i in range(len(groups)):
        group = groups[i]
        j = 0
        if i == len(groups) - 1 and not s.endswith("#"):
            j = len(group)
        if len(group) > 2:
            j = len(group) - 2
        for k in range(j):
            crypt.append(int(group[k:k + 1]))
        if j < len(group):
            crypt.append(int(group[j:]))
    n = []
    for c in crypt:
        n.append(chr(ord("a") + c - 1))
    return "".join(n)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *decrypt(const char *s) {
    int nums[512];
    int n = 0;
    int len = (int) strlen(s);
    int i = 0;
    while (i <= len) {
        int end = i;
        while (end < len && s[end] != '#') end++;
        int glen = end - i;
        int j = 0;
        if (end == len && (len == 0 || s[len - 1] != '#')) j = glen;
        if (glen > 2) j = glen - 2;
        for (int k = 0; k < j; k++) nums[n++] = s[i + k] - '0';
        if (j < glen) {
            int val = 0;
            for (int k = j; k < glen; k++) val = val * 10 + (s[i + k] - '0');
            nums[n++] = val;
        }
        i = end + 1;
    }
    char *out = malloc((size_t) n + 1);
    for (int k = 0; k < n; k++) out[k] = (char) ('a' + nums[k] - 1);
    out[n] = '\0';
    return out;
}''',
"csharp": r'''public static string Decrypt(string s) {
    var crypt = new List<int>();
    var groups = s.Split('#');
    for (int i = 0; i < groups.Length; i++) {
        var group = groups[i];
        int j = 0;
        if (i == groups.Length - 1 && !s.EndsWith("#")) j = group.Length;
        if (group.Length > 2) j = group.Length - 2;
        for (int k = 0; k < j; k++) crypt.Add(int.Parse(group.Substring(k, 1)));
        if (j < group.Length) crypt.Add(int.Parse(group.Substring(j)));
    }
    var sb = new StringBuilder(crypt.Count);
    foreach (int c in crypt) {
        sb.Append((char) ('a' + c - 1));
    }
    return sb.ToString();
}'''}})

PART.append({"id": "T515", "task": "translate", "outputs": {
"python": r'''class AWTException(Exception):
    pass

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Toolkit:
    _instance = None

    @staticmethod
    def get_default_toolkit():
        if Toolkit._instance is None:
            Toolkit._instance = Toolkit()
        return Toolkit._instance

    def get_screen_size(self):
        return (1920, 1080)

class Robot:
    def create_screen_capture(self, rect):
        return b""

class ImageIO:
    @staticmethod
    def write(data, fmt, path):
        with open(path, "wb") as f:
            f.write(data)

def main():
    try:
        robot = Robot()
        w, h = Toolkit.get_default_toolkit().get_screen_size()
        bi = robot.create_screen_capture(Rectangle(w, h))
        ImageIO.write(bi, "jpg", "C:/imageTest.jpg")
    except AWTException as e:
        print(e)
    except OSError as e:
        print(e)

main()''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

typedef struct { int width, height; } Rectangle;
typedef struct { unsigned char *pixels; int length; } BufferedImage;

Dimension toolkit_get_screen_size(void);

typedef struct { int width, height; } Dimension;

Dimension toolkit_get_screen_size(void) {
    Dimension d;
    d.width = 1920;
    d.height = 1080;
    return d;
}

BufferedImage robot_create_screen_capture(Rectangle rect) {
    BufferedImage img;
    img.length = rect.width * rect.height;
    img.pixels = (unsigned char *) calloc((size_t) img.length, 1);
    return img;
}

int imageio_write(BufferedImage img, const char *format, const char *path) {
    FILE *f = fopen(path, "wb");
    if (f == NULL) return 0;
    fwrite(img.pixels, 1, (size_t) img.length, f);
    fclose(f);
    return 1;
}

int main(void) {
    Dimension size = toolkit_get_screen_size();
    Rectangle rect;
    rect.width = size.width;
    rect.height = size.height;
    BufferedImage bi = robot_create_screen_capture(rect);
    imageio_write(bi, "jpg", "C:/imageTest.jpg");
    return 0;
}''',
"csharp": r'''class Size { public int Width, Height; }
class Rectangle { public int Width, Height; public Rectangle(int w, int h) { Width = w; Height = h; } }
class BufferedImage { public byte[] Data; }
class Toolkit {
    public static readonly Toolkit DefaultToolkit = new Toolkit();
    public Size GetScreenSize() { return new Size { Width = 1920, Height = 1080 }; }
}
class Robot {
    public BufferedImage CreateScreenCapture(Rectangle r) { return new BufferedImage { Data = new byte[r.Width * r.Height] }; }
}
static class ImageIO {
    public static void Write(BufferedImage img, string fmt, string path) { System.IO.File.WriteAllBytes(path, img.Data); }
}

public static void Main() {
    try {
        var robot = new Robot();
        var size = Toolkit.DefaultToolkit.GetScreenSize();
        var bi = robot.CreateScreenCapture(new Rectangle(size.Width, size.Height));
        ImageIO.Write(bi, "jpg", "C:/imageTest.jpg");
    } catch (Exception e) {
        Console.WriteLine(e);
    }
}'''}})

PART.append({"id": "T621", "task": "translate", "outputs": {
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
"c": r'''#include <stdlib.h>

int *zero_front(const int *nums, int length) {
    if (nums == NULL) return NULL;
    int *result = (int *) malloc(length * sizeof(int));
    int zeroes_pos = 0;
    int others_pos = length - 1;
    for (int i = 0; i < length; i++) {
        if (nums[i] == 0) {
            result[zeroes_pos] = 0;
            zeroes_pos++;
        } else {
            result[others_pos] = nums[i];
            others_pos--;
        }
    }
    return result;
}''',
"csharp": r'''public static int[] ZeroFront(int[] nums) {
    if (nums == null) return null;
    var result = new int[nums.Length];
    int zeroesPos = 0;
    int othersPos = result.Length - 1;
    foreach (int value in nums) {
        if (value == 0) {
            result[zeroesPos] = 0;
            zeroesPos++;
        } else {
            result[othersPos] = value;
            othersPos--;
        }
    }
    return result;
}'''}})

PART.append({"id": "T748", "task": "translate", "outputs": {
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
    print("Sex accepted: " + sex)

main()''',
"c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const int valid = 6;
    char s[256];
    char sex[256];
    int a;
    printf("Enter your username: \n");
    scanf("%255s", s);
    if ((int) strlen(s) < valid) {
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
    scanf("%255s", sex);
    printf("Sex accepted: %s\n", sex);
    return 0;
}''',
"csharp": r'''static void Main() {
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
}'''}})

PART.append({"id": "T334", "task": "translate", "outputs": {
"python": r'''def get_name(value):
    buffer = []
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[len(value) - 4:])
    else:
        number = int(value)
    number %= 1000
    if number >= 100:
        buffer.append(unit_processor.get_name(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(scale.get_name(EXPONENT))
    tens_name = tens_processor.get_name(number % 100)
    if tens_name != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tens_name)
    return "".join(buffer)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void get_name(const char *value, char *out) {
    char buffer[512] = "";
    char tmp[128];
    int number;
    if (value[0] == '\0') {
        number = 0;
    } else if (strlen(value) > 4) {
        number = atoi(value + strlen(value) - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        unit_processor_get_name(number / 100, tmp);
        strcat(buffer, tmp);
        strcat(buffer, SEPARATOR);
        scale_get_name(EXPONENT, tmp);
        strcat(buffer, tmp);
    }
    char tens_name[256] = "";
    tens_processor_get_name(number % 100, tens_name);
    if (tens_name[0] != '\0' && number >= 100) {
        strcat(buffer, SEPARATOR);
    }
    strcat(buffer, tens_name);
    strcpy(out, buffer);
}''',
"csharp": r'''public string GetName(string value) {
    var buffer = new StringBuilder();
    int number;
    if ("" == value) {
        number = 0;
    } else if (value.Length > 4) {
        number = int.Parse(value.Substring(value.Length - 4));
    } else {
        number = int.Parse(value);
    }
    number %= 1000;
    if (number >= 100) {
        buffer.Append(unitProcessor.GetName(number / 100));
        buffer.Append(SEPARATOR);
        buffer.Append(scale.GetName(EXPONENT));
    }
    string tensName = tensProcessor.GetName(number % 100);
    if (tensName != "" && number >= 100) {
        buffer.Append(SEPARATOR);
    }
    buffer.Append(tensName);
    return buffer.ToString();
}'''}})

PART.append({"id": "T492", "task": "translate", "outputs": {
"python": r'''import sys
import xml.etree.ElementTree as ET

def main():
    try:
        tree = ET.parse(r"d:\xml\soap.xml")
    except Exception:
        print("invalid xml")
        sys.exit(0)
    root = tree.getroot()
    for part in root.iter("part"):
        for child in part:
            if child.text and child.text.strip():
                print(" " + child.tag + " = " + child.text.strip())

main()''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char name[64]; char text[256]; } VTDEntry;
typedef struct { VTDEntry *entries; int count; } VTDNav;
typedef struct { VTDNav *nav; const char *xpath; } AutoPilot;

int vtd_parse_file(const char *path, int ns) {
    return path != NULL;
}

VTDNav *vtd_get_nav(void) {
    static VTDEntry entry;
    static VTDNav nav;
    strcpy(entry.name, "part");
    strcpy(entry.text, "value");
    nav.entries = &entry;
    nav.count = 1;
    return &nav;
}

void ap_select_xpath(AutoPilot *ap, const char *xpath) { ap->xpath = xpath; }
void ap_bind(AutoPilot *ap, VTDNav *nav) { ap->nav = nav; }

int ap_eval_xpath(AutoPilot *ap, int current) {
    int next = current + 1;
    return next < ap->nav->count ? next : -1;
}

int main(void) {
    AutoPilot ap;
    ap.nav = NULL;
    ap_select_xpath(&ap, "//part/*[text()]");
    if (!vtd_parse_file("d:\\xml\\soap.xml", 0)) {
        printf("invalid xml\n");
        exit(0);
    }
    VTDNav *vn = vtd_get_nav();
    ap_bind(&ap, vn);
    int i = 0;
    while ((i = ap_eval_xpath(&ap, i)) != -1) {
        printf(" %s = %s\n", vn->entries[i].name, vn->entries[i].text);
    }
    return 0;
}''',
"csharp": r'''using System.Xml.XPath;

public static void Main() {
    try {
        var doc = new XPathDocument(@"d:\xml\soap.xml");
        var nav = doc.CreateNavigator();
        var iter = nav.Select("//part/*[text()]");
        while (iter.MoveNext()) {
            Console.WriteLine(" " + iter.Current.Name + " = " + iter.Current.Value.Trim());
        }
    } catch (Exception) {
        Console.WriteLine("invalid xml");
        Environment.Exit(0);
    }
}'''}})

PART.append({"id": "T484", "task": "translate", "outputs": {
"python": r'''import random

def show_random_integer(start, end, generator):
    print(generator.randint(start, end))

def log(message):
    print(message)

def main():
    log("Generating 10 random integers in range 1..10.")
    start = 1
    end = 10
    generator = random.Random()
    for _ in range(10):
        show_random_integer(start, end, generator)
    log("Done")

main()''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int random_in_range(int start, int end) {
    return start + rand() % (end - start + 1);
}

void show_random_integer(int start, int end) {
    printf("%d\n", random_in_range(start, end));
}

int main(void) {
    srand((unsigned) time(NULL));
    printf("Generating 10 random integers in range 1..10.\n");
    const int start = 1;
    const int end = 10;
    for (int idx = 1; idx <= 10; ++idx) {
        show_random_integer(start, end);
    }
    printf("Done\n");
    return 0;
}''',
"csharp": r'''static void Main() {
    Log("Generating 10 random integers in range 1..10.");
    const int START = 1;
    const int END = 10;
    var randomGenerator = new Random();
    for (int idx = 1; idx <= 10; ++idx) {
        ShowRandomInteger(START, END, randomGenerator);
    }
    Log("Done");
}

static void ShowRandomInteger(int start, int end, Random generator) {
    Console.WriteLine(generator.Next(start, end + 1));
}

static void Log(string message) {
    Console.WriteLine(message);
}'''}})

PART.append({"id": "T79", "task": "translate", "outputs": {
"python": r'''def main():
    list_of_strings = []
    while True:
        print("Current list is " + str(list_of_strings))
        print("Add more? (y/n)")
        if input().startswith("y"):
            print("Enter : ")
            list_of_strings.append(input())
        else:
            break
    print("List is " + str(list_of_strings))
    print("Array is " + str(list(list_of_strings)))

main()''',
"c": r'''#include <stdio.h>

static void print_list(char list[][128], int count) {
    printf("[");
    for (int i = 0; i < count; i++) {
        if (i > 0) printf(", ");
        printf("%s", list[i]);
    }
    printf("]\n");
}

int main(void) {
    char list[64][128];
    char answer[16];
    int count = 0;
    do {
        print_list(list, count);
        printf("Add more? (y/n)\n");
        scanf("%15s", answer);
        if (answer[0] == 'y') {
            printf("Enter : \n");
            scanf("%127s", list[count++]);
        } else {
            break;
        }
    } while (1);
    printf("List is ");
    print_list(list, count);
    printf("Array is ");
    print_list(list, count);
    return 0;
}''',
"csharp": r'''static void Main() {
    var list = new List<string>();
    while (true) {
        Console.WriteLine("Current list is [" + string.Join(", ", list) + "]");
        Console.WriteLine("Add more? (y/n)");
        if (Console.ReadLine().StartsWith("y")) {
            Console.WriteLine("Enter : ");
            list.Add(Console.ReadLine());
        } else {
            break;
        }
    }
    Console.WriteLine("List is [" + string.Join(", ", list) + "]");
    string[] arr = list.ToArray();
    Console.WriteLine("Array is [" + string.Join(", ", arr) + "]");
}'''}})
