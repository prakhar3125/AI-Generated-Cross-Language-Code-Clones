DATA = {}

DATA["T422"] = {
    "python": '''def decrypt(s):
    crypt = []
    groups = s.split("#")
    for i in range(len(groups)):
        group = groups[i]
        j = 0
        if (i == (len(groups) - 1)) and not s.endswith("#"):
            j = len(group)
        if len(group) > 2:
            j = len(group) - 2
        for k in range(j):
            crypt.append(int(group[k:k + 1]))
        if j < len(group):
            crypt.append(int(group[j:]))
    return "".join(chr((ord('a') + c) - 1) for c in crypt)''',
    "c": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *decrypt(const char *s) {
    int slen = (int)strlen(s);
    int cap = 16, count = 0;
    int *crypt = malloc(cap * sizeof(int));
    int ngroups = 1;
    int start = 0, gi = 0;
    for (int p = 0; p < slen; p++) {
        if (s[p] == '#') ngroups++;
    }
    for (int p = 0; p <= slen; p++) {
        if (p == slen || s[p] == '#') {
            int len = p - start;
            if (!(p == slen && len == 0)) {
                int j = 0;
                if ((gi == ngroups - 1) && (slen == 0 || s[slen - 1] != '#')) j = len;
                if (len > 2) j = len - 2;
                for (int k = 0; k < j; k++) {
                    if (count == cap) {
                        cap *= 2;
                        crypt = realloc(crypt, cap * sizeof(int));
                    }
                    crypt[count++] = s[start + k] - '0';
                }
                if (j < len) {
                    char tail[8];
                    int tl = len - j;
                    if (count == cap) {
                        cap *= 2;
                        crypt = realloc(crypt, cap * sizeof(int));
                    }
                    memcpy(tail, s + start + j, tl);
                    tail[tl] = '\\0';
                    crypt[count++] = atoi(tail);
                }
            }
            gi++;
            start = p + 1;
        }
    }
    char *result = malloc(count + 1);
    for (int m = 0; m < count; m++) {
        result[m] = (char)(('a' + crypt[m]) - 1);
    }
    result[count] = '\\0';
    free(crypt);
    return result;
}''',
    "csharp": '''using System;
using System.Collections.Generic;
using System.Text;

public static class CryptReader
{
    public static string Decrypt(string s)
    {
        var crypt = new List<int>();
        string[] groups = s.Split('#');
        for (int i = 0; i < groups.Length; i++)
        {
            string group = groups[i];
            int j = 0;
            if ((i == (groups.Length - 1)) && !s.EndsWith("#"))
            {
                j = group.Length;
            }
            if (group.Length > 2)
            {
                j = group.Length - 2;
            }
            for (int k = 0; k < j; k++)
            {
                crypt.Add(int.Parse(group.Substring(k, 1)));
            }
            if (j < group.Length)
            {
                crypt.Add(int.Parse(group.Substring(j)));
            }
        }
        var n = new StringBuilder(crypt.Count);
        foreach (int c in crypt)
        {
            n.Append((char)(('a' + c) - 1));
        }
        return n.ToString();
    }
}''',
}

DATA["T515"] = {
    "python": '''class AWTException(Exception):
    pass


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Toolkit:
    @staticmethod
    def get_default_toolkit():
        return Toolkit()

    def get_screen_size(self):
        return Rectangle(1920, 1080)


class Robot:
    def create_screen_capture(self, rect):
        return None


class ImageIO:
    @staticmethod
    def write(image, fmt, target):
        pass


class File:
    def __init__(self, path):
        self.path = path


def main():
    try:
        robot = Robot()
        bi = robot.create_screen_capture(Toolkit.get_default_toolkit().get_screen_size())
        ImageIO.write(bi, "jpg", File("C:/imageTest.jpg"))
    except AWTException as e:
        print(e)
    except OSError as e:
        print(e)''',
    "c": '''#include <stdio.h>

typedef struct { int width; int height; } Rectangle;
typedef struct { int width; int height; } Image;
typedef struct { const char *path; } FileHandle;

Rectangle toolkit_get_screen_size(void);
Image robot_create_screen_capture(Rectangle rect);
int imageio_write(Image image, const char *fmt, FileHandle target);

int main(void) {
    Rectangle bounds = toolkit_get_screen_size();
    Image bi = robot_create_screen_capture(bounds);
    FileHandle target;
    target.path = "C:/imageTest.jpg";
    if (imageio_write(bi, "jpg", target) != 0) {
        fprintf(stderr, "write failed\\n");
    }
    return 0;
}''',
    "csharp": '''using System;
using System.Drawing;
using System.Drawing.Imaging;

public static class ScreenGrabber
{
    public static void Main()
    {
        try
        {
            var bounds = System.Windows.Forms.Screen.PrimaryScreen.Bounds;
            using (var bi = new Bitmap(bounds.Width, bounds.Height))
            {
                using (var g = Graphics.FromImage(bi))
                {
                    g.CopyFromScreen(0, 0, 0, 0, bi.Size);
                }
                bi.Save("C:/imageTest.jpg", ImageFormat.Jpeg);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
}''',
}

DATA["T621"] = {
    "python": '''def zero_front(nums):
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
    "c": '''#include <stdlib.h>

int *zero_front(const int *nums, int n) {
    if (nums == NULL) {
        return NULL;
    }
    int *result = malloc(n * sizeof(int));
    int zeroes_pos = 0;
    int others_pos = n - 1;
    for (int i = 0; i < n; ++i) {
        if (nums[i] == 0) {
            result[zeroes_pos] = 0;
            ++zeroes_pos;
        } else {
            result[others_pos] = nums[i];
            --others_pos;
        }
    }
    return result;
}''',
    "csharp": '''public static int[] ZeroFront(int[] nums)
{
    if (nums == null)
    {
        return null;
    }
    int[] result = new int[nums.Length];
    int zeroesPos = 0;
    int othersPos = result.Length - 1;
    for (int i = 0; i < nums.Length; ++i)
    {
        if (nums[i] == 0)
        {
            result[zeroesPos] = 0;
            ++zeroesPos;
        }
        else
        {
            result[othersPos] = nums[i];
            --othersPos;
        }
    }
    return result;
}''',
}

DATA["T748"] = {
    "python": '''def main():
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
    "c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    const int valid = 6;
    char s[128];
    int a;
    char sex[128];
    printf("Enter your username: \\n");
    scanf("%127s", s);
    if ((int)strlen(s) < valid) {
        printf("Enter a valid username\\n");
        printf("User name must contain %d characters\\n", valid);
        printf("Enter again: \\n");
        scanf("%127s", s);
    }
    printf("Username accepted: %s\\n", s);
    printf("Enter your age: \\n");
    scanf("%d", &a);
    printf("Age accepted: %d\\n", a);
    printf("Enter your sex: \\n");
    scanf("%127s", sex);
    printf("Sex accepted: %s\\n", sex);
    return 0;
}''',
    "csharp": '''using System;

public static class ProfilePrompt
{
    public static void Main()
    {
        const int valid = 6;
        Console.WriteLine("Enter your username: ");
        string s = Console.ReadLine();
        if (s.Length < valid)
        {
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
    }
}''',
}

DATA["T334"] = {
    "python": '''class _NameProcessor:
    def __init__(self, names):
        self._names = names

    def get_name(self, number):
        return self._names.get(number, "")


unitProcessor = _NameProcessor({1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                                6: "six", 7: "seven", 8: "eight", 9: "nine"})
tensProcessor = _NameProcessor({i: n for i, n in enumerate(
    ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
     "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
     "eighteen", "nineteen"])})
SCALE = _NameProcessor({2: "hundred"})
EXPONENT = 2
SEPARATOR = " "


def get_name(value):
    buffer = []
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[len(value) - 4:])
    else:
        number = int(value)
    number %= 1000
    if number >= 100:
        buffer.append(unitProcessor.get_name(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(SCALE.get_name(EXPONENT))
    tens_name = tensProcessor.get_name(number % 100)
    if tens_name != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tens_name)
    return "".join(buffer)''',
    "c": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *unit_names[] = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
static const char *tens_names[] = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"};

#define SEPARATOR " "
#define EXPONENT 2
#define SCALE_NAME "hundred"

char *get_name(const char *value) {
    char *buffer = malloc(256);
    size_t vlen = strlen(value);
    int number;
    if (buffer == NULL) return NULL;
    buffer[0] = '\\0';
    if (vlen == 0) {
        number = 0;
    } else if (vlen > 4) {
        number = atoi(value + vlen - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        char tmp[16];
        sprintf(tmp, "%d", number / 100);
        strcat(buffer, unit_names[number / 100]);
        strcat(buffer, SEPARATOR);
        strcat(buffer, SCALE_NAME);
    }
    const char *tens_name = (number % 100) < 20 ? tens_names[number % 100] : "";
    if (tens_name[0] != '\\0' && number >= 100) {
        strcat(buffer, SEPARATOR);
    }
    strcat(buffer, tens_name);
    return buffer;
}''',
    "csharp": '''using System.Collections.Generic;

public class TensNamer
{
    private static readonly string[] Units = { "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };
    private static readonly string[] Tens = { "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" };
    private const string Separator = " ";
    private const int Exponent = 2;

    private string UnitGetName(int number)
    {
        return Units[number];
    }

    private string TensGetName(int number)
    {
        return number < 20 ? Tens[number] : "";
    }

    private string ScaleGetName(int exponent)
    {
        return exponent == 2 ? "hundred" : "";
    }

    public string GetName(string value)
    {
        var buffer = new List<string>();
        int number;
        if ("" == value)
        {
            number = 0;
        }
        else if (value.Length > 4)
        {
            number = int.Parse(value.Substring(value.Length - 4));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 1000;
        if (number >= 100)
        {
            buffer.Add(UnitGetName(number / 100));
            buffer.Add(Separator);
            buffer.Add(ScaleGetName(Exponent));
        }
        string tensName = TensGetName(number % 100);
        if (!"".Equals(tensName) && (number >= 100))
        {
            buffer.Add(Separator);
        }
        buffer.Add(tensName);
        return string.Concat(buffer);
    }
}''',
}

DATA["T492"] = {
    "python": '''import sys
import xml.etree.ElementTree as ET


def main():
    try:
        tree = ET.parse("d:/xml/soap.xml")
    except (ET.ParseError, OSError):
        print("invalid xml")
        sys.exit(0)
    root = tree.getroot()
    for part in root.iter("part"):
        for elem in part:
            if elem.text and elem.text.strip():
                print(" " + elem.tag + " = " + elem.text.strip())''',
    "c": '''#include <stdio.h>
#include <stdlib.h>

typedef struct { int index; } VTDNav;

int vtd_parse_file(const char *path, int namespace_aware);
VTDNav *vtd_get_nav(void);
int ap_select_xpath(const char *xpath);
void ap_bind(VTDNav *vn);
int ap_eval_xpath(void);
char *vn_to_raw_string(VTDNav *vn, int i);
char *vn_to_normalized_string(VTDNav *vn, int text_index);
int vn_get_text(VTDNav *vn, int i);

int main() {
    if (!vtd_parse_file("d:\\\\xml\\\\soap.xml", 0)) {
        printf("invalid xml\\n");
        exit(0);
    }
    VTDNav *vn = vtd_get_nav();
    ap_bind(vn);
    int i = 0;
    while ((i = ap_eval_xpath()) != -1) {
        printf(" %s = %s\\n", vn_to_raw_string(vn, i), vn_to_normalized_string(vn, vn_get_text(vn, i)));
    }
    return 0;
}''',
    "csharp": '''using System;
using System.Xml;
using System.Xml.XPath;

public static class PartTextReader
{
    public static void Main()
    {
        var doc = new XPathDocument("d:\\\\xml\\\\soap.xml");
        var nav = doc.CreateNavigator();
        var iter = nav.Select("//part/*[text()]");
        while (iter.MoveNext())
        {
            Console.WriteLine(" " + iter.Current.Name + " = " + iter.Current.Value);
        }
    }
}''',
}

DATA["T484"] = {
    "python": '''import random


def log(message):
    print(message)


def show_random_integer(start, end, generator):
    print(generator.randint(start, end))


def main():
    log("Generating 10 random integers in range 1..10.")
    start = 1
    end = 10
    random_generator = random.Random()
    for _ in range(10):
        show_random_integer(start, end, random_generator)
    log("Done")''',
    "c": '''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static void log(const char *message) {
    printf("%s\\n", message);
}

static void show_random_integer(int start, int end) {
    printf("%d\\n", start + rand() % (end - start + 1));
}

int main(void) {
    srand((unsigned) time(NULL));
    log("Generating 10 random integers in range 1..10.");
    const int START = 1;
    const int END = 10;
    for (int idx = 1; idx <= 10; ++idx) {
        show_random_integer(START, END);
    }
    log("Done");
    return 0;
}''',
    "csharp": '''using System;

public static class RandomIntegers
{
    private static void Log(string message)
    {
        Console.WriteLine(message);
    }

    private static void ShowRandomInteger(int start, int end, Random generator)
    {
        Console.WriteLine(generator.Next(start, end + 1));
    }

    public static void Main(string[] aArgs)
    {
        Log("Generating 10 random integers in range 1..10.");
        int START = 1;
        int END = 10;
        Random randomGenerator = new Random();
        for (int idx = 1; idx <= 10; ++idx)
        {
            ShowRandomInteger(START, END, randomGenerator);
        }
        Log("Done");
    }
}''',
}

DATA["T79"] = {
    "python": '''def main():
    items = []
    while True:
        print("Current list is " + str(items))
        print("Add more? (y/n)")
        if input().startswith("y"):
            print("Enter : ")
            items.append(input())
        else:
            break
    print("List is " + str(items))
    print("Array is " + str(items))''',
    "c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    char list[64][128];
    int count = 0;
    char answer[16];
    for (;;) {
        printf("Current list is ");
        for (int i = 0; i < count; i++) {
            printf("%s%s", i > 0 ? ", " : "", list[i]);
        }
        printf("\\n");
        printf("Add more? (y/n)\\n");
        if (scanf("%15s", answer) != 1 || answer[0] != 'y') {
            break;
        }
        printf("Enter : \\n");
        scanf("%127s", list[count]);
        count++;
    }
    printf("List is ");
    for (int i = 0; i < count; i++) {
        printf("%s%s", i > 0 ? ", " : "", list[i]);
    }
    printf("\\nArray is ");
    for (int i = 0; i < count; i++) {
        printf("%s%s", i > 0 ? ", " : "", list[i]);
    }
    printf("\\n");
    return 0;
}''',
    "csharp": '''using System;
using System.Collections.Generic;

public static class ListBuilder
{
    public static void Main(string[] args)
    {
        var list = new List<string>();
        do
        {
            Console.WriteLine("Current list is [" + string.Join(", ", list) + "]");
            Console.WriteLine("Add more? (y/n)");
            if (Console.ReadLine().StartsWith("y"))
            {
                Console.WriteLine("Enter : ");
                list.Add(Console.ReadLine());
            }
            else
            {
                break;
            }
        } while (true);
        Console.WriteLine("List is [" + string.Join(", ", list) + "]");
        Console.WriteLine("Array is [" + string.Join(", ", list.ToArray()) + "]");
    }
}''',
}

DATA["T710"] = {
    "python": '''def filter(source, start, end, dest, dstart, dend, decimal_digits):
    dot_pos = -1
    length = len(dest)
    for i in range(length):
        c = dest[i]
        if c == '.' or c == ',':
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
    "c": '''#include <string.h>

const char *filter(const char *source, int start, int end,
                   const char *dest, int dstart, int dend, int decimal_digits) {
    int dot_pos = -1;
    int len = (int)strlen(dest);
    for (int i = 0; i < len; i++) {
        char c = dest[i];
        if (c == '.' || c == ',') {
            dot_pos = i;
            break;
        }
    }
    if (dot_pos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) {
            return "";
        }
        if (dend <= dot_pos) {
            return NULL;
        }
        if (len - dot_pos > decimal_digits) {
            return "";
        }
    }
    return NULL;
}''',
    "csharp": '''public static string Filter(string source, int start, int end, string dest, int dstart, int dend, int decimalDigits)
{
    int dotPos = -1;
    int len = dest.Length;
    for (int i = 0; i < len; i++)
    {
        char c = dest[i];
        if (c == '.' || c == ',')
        {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0)
    {
        if (source.Equals(".") || source.Equals(","))
        {
            return "";
        }
        if (dend <= dotPos)
        {
            return null;
        }
        if (len - dotPos > decimalDigits)
        {
            return "";
        }
    }
    return null;
}''',
}
