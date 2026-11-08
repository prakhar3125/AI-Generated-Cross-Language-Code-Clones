DATA_P5 = {}

DATA_P5["T807"] = {"outputs": {
"python": r'''
def removeDuplicates(s):
    no_dupes = []
    for ch in s:
        if ch not in no_dupes:
            no_dupes.append(ch)
    return "".join(no_dupes)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

char *removeDuplicates(const char *s) {
    size_t n = strlen(s);
    char *noDupes = malloc(n + 1);
    size_t len = 0;
    for (size_t i = 0; i < n; i++) {
        if (memchr(noDupes, s[i], len) == NULL) {
            noDupes[len++] = s[i];
        }
    }
    noDupes[len] = '\0';
    return noDupes;
}
''',
"csharp": r'''
using System.Collections.Generic;
using System.Text;

public static class Dedup
{
    public static string RemoveDuplicates(string s)
    {
        StringBuilder noDupes = new StringBuilder();
        var seen = new HashSet<char>();
        foreach (char c in s)
        {
            if (seen.Add(c))
            {
                noDupes.Append(c);
            }
        }
        return noDupes.ToString();
    }
}
'''}}

DATA_P5["T447"] = {"outputs": {
"python": r'''
def isAnagram(s1, s2):
    if len(s1) != len(s2):
        return False
    a1 = sorted(s1)
    a2 = sorted(s2)
    print("".join(a1))
    print("".join(a2))
    return a1 == a2
''',
"c": r'''
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmpChar(const void *x, const void *y) {
    return *(const char *)x - *(const char *)y;
}

bool isAnagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) return false;
    char *arr1 = strdup(s1), *arr2 = strdup(s2);
    qsort(arr1, strlen(s1), 1, cmpChar);
    qsort(arr2, strlen(s2), 1, cmpChar);
    printf("%s\n%s\n", arr1, arr2);
    bool equal = strcmp(arr1, arr2) == 0;
    free(arr1);
    free(arr2);
    return equal;
}
''',
"csharp": r'''
using System;
using System.Linq;

public static class AnagramCheck
{
    public static bool IsAnagram(string s1, string s2)
    {
        if (s1.Length != s2.Length) return false;
        var sorted1 = new string(s1.ToCharArray().OrderBy(c => c).ToArray());
        var sorted2 = new string(s2.ToCharArray().OrderBy(c => c).ToArray());
        Console.WriteLine(sorted1);
        Console.WriteLine(sorted2);
        return sorted1 == sorted2;
    }
}
'''}}

DATA_P5["T397"] = {"outputs": {
"python": r'''
import os
import shutil


def copyFolder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            target_root = os.path.join(dest, os.path.relpath(root, src))
            if not os.path.exists(target_root):
                os.mkdir(target_root)
            for f in files:
                shutil.copy(os.path.join(root, f), os.path.join(target_root, f))
    except Exception as ex:
        import traceback
        traceback.print_exc()
''',
"c": r'''
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

static void copyFolderWalk(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    if (!dir) {
        perror("opendir failed");
        return;
    }
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
        char srcPath[512], destPath[512];
        snprintf(srcPath, sizeof srcPath, "%s/%s", src, entry->d_name);
        snprintf(destPath, sizeof destPath, "%s/%s", dest, entry->d_name);
        struct stat st;
        if (stat(srcPath, &st) != 0) continue;
        if (S_ISDIR(st.st_mode)) {
            mkdir(destPath, 0755);
            copyFolderWalk(srcPath, destPath);
        } else {
            FILE *in = fopen(srcPath, "rb");
            FILE *out = fopen(destPath, "wb");
            if (in && out) {
                char buf[4096];
                size_t n;
                while ((n = fread(buf, 1, sizeof buf, in)) > 0)
                    fwrite(buf, 1, n, out);
            }
            if (in) fclose(in);
            if (out) fclose(out);
        }
    }
    closedir(dir);
}

void copyFolder(const char *src, const char *dest) {
    copyFolderWalk(src, dest);
}
''',
"csharp": r'''
using System;
using System.IO;

public static class FolderCopier
{
    public static void CopyFolder(string src, string dest)
    {
        try
        {
            foreach (string dirPath in Directory.GetDirectories(src, "*", SearchOption.AllDirectories))
            {
                string d = Path.Combine(dest, Path.GetRelativePath(src, dirPath));
                if (!Directory.Exists(d)) Directory.CreateDirectory(d);
            }
            foreach (string filePath in Directory.GetFiles(src, "*", SearchOption.AllDirectories))
            {
                string d = Path.Combine(dest, Path.GetRelativePath(src, filePath));
                File.Copy(filePath, d, true);
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.StackTrace);
        }
    }
}
'''}}

DATA_P5["T430"] = {"outputs": {
"python": r'''
import time


class Insets:
    def __init__(self, top, left, bottom, right):
        self.top, self.left, self.bottom, self.right = top, left, bottom, right


class Border:
    def __init__(self, top, left, bottom, right):
        self.top, self.left, self.bottom, self.right = top, left, bottom, right


class Animator:
    def __init__(self, clr, init_margin):
        self.clr = clr
        self.init_margin = init_margin
        self.no_color = 0
        self.runs = False
        self.count = 0

    def changeBtnForegroung(self, color): pass
    def changeBtnMargin(self, m): pass
    def changePnlBorder(self, b): pass

    def run(self):
        try:
            self.runs = True
            if self.no_color < 2:
                self.no_color += 1
            else:
                self.no_color = 0
            self.changeBtnForegroung(self.clr[self.no_color])
            steps = [
                ((10, -10), (0, 5, 10, 5)),
                ((-10, 10), (0, 0, 10, 10)),
                ((10, -10), (5, 10, 5, 0)),
                ((-10, 10), (10, 10, 0, 0)),
                ((0, 0), (5, 5, 5, 5)),
            ]
            for (dl, dr), (bt, bl, bb, br) in steps:
                self.changeBtnMargin(Insets(self.init_margin.top,
                                            self.init_margin.left + dl,
                                            self.init_margin.bottom,
                                            self.init_margin.right + dr))
                self.changePnlBorder(Border(bt, bl, bb, br))
                time.sleep(0.1)
            self.count += 1
        except Exception as e:
            print(e)
''',
"c": r'''
#include <unistd.h>

typedef struct { int top, left, bottom, right; } Insets;
typedef struct { int top, left, bottom, right; } Border;

static const char *clr[3] = {"red", "green", "blue"};
static Insets initMargin = {0, 0, 0, 0};
static int noColor = 0;
static int runs = 0;
static int count = 0;

void changeBtnForegroung(const char *color) {}
void changeBtnMargin(const Insets *m) {}
void changePnlBorder(const Border *b) {}

static void applyStep(int dl, int dr, int bt, int bl, int bb, int br) {
    Insets m = {initMargin.top, initMargin.left + dl, initMargin.bottom, initMargin.right + dr};
    Border border = {bt, bl, bb, br};
    changeBtnMargin(&m);
    changePnlBorder(&border);
    usleep(100000);
}

void run(void) {
    runs = 1;
    if (noColor < 2) noColor++;
    else noColor = 0;
    changeBtnForegroung(clr[noColor]);
    applyStep(10, -10, 0, 5, 10, 5);
    applyStep(-10, 10, 0, 0, 10, 10);
    applyStep(10, -10, 5, 10, 5, 0);
    applyStep(-10, 10, 10, 10, 0, 0);
    applyStep(0, 0, 5, 5, 5, 5);
    count++;
}
''',
"csharp": r'''
using System;

public struct InsetsEx
{
    public int Top, Left, Bottom, Right;
    public InsetsEx(int t, int l, int b, int r) { Top = t; Left = l; Bottom = b; Right = r; }
}

public class ButtonAnimator
{
    private bool runs = false;
    private int noColor = 0;
    private int count = 0;
    private readonly string[] clr = { "red", "green", "blue" };
    private readonly InsetsEx initMargin = new InsetsEx(0, 0, 0, 0);

    private void ChangeBtnForegroung(string color) { }
    private void ChangeBtnMargin(InsetsEx m) { }
    private void ChangePnlBorder(InsetsEx b) { }

    public void Run()
    {
        try
        {
            runs = true;
            if (noColor < 2)
            {
                noColor++;
            }
            else
            {
                noColor = 0;
            }
            ChangeBtnForegroung(clr[noColor]);
            var steps = new[]
            {
                new { Dl = 10, Dr = -10, Border = new[] { 0, 5, 10, 5 } },
                new { Dl = -10, Dr = 10, Border = new[] { 0, 0, 10, 10 } },
                new { Dl = 10, Dr = -10, Border = new[] { 5, 10, 5, 0 } },
                new { Dl = -10, Dr = 10, Border = new[] { 10, 10, 0, 0 } },
                new { Dl = 0, Dr = 0, Border = new[] { 5, 5, 5, 5 } }
            };
            foreach (var step in steps)
            {
                ChangeBtnMargin(new InsetsEx(initMargin.Top,
                    initMargin.Left + step.Dl, initMargin.Bottom, initMargin.Right + step.Dr));
                ChangePnlBorder(new InsetsEx(step.Border[0], step.Border[1],
                    step.Border[2], step.Border[3]));
                System.Threading.Thread.Sleep(100);
            }
            count++;
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
}
'''}}
