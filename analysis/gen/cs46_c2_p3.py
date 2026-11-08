DATA3 = {}

DATA3["T111"] = {"outputs": {
"python": r"""
def single_number(nums):
    answer = 0
    al = []
    for n in nums:
        al.append(n)
    for i in range(len(nums)):
        test = nums[i]
        if al.index(test) == al.rindex(test):
            answer = nums[i]
    return answer
""",
"c": r"""
int single_number(const int *nums, int len) {
    int answer = 0;
    for (int i = 0; i < len; i++) {
        int first = -1, last = -1;
        for (int j = 0; j < len; j++) {
            if (nums[j] == nums[i]) {
                if (first == -1) {
                    first = j;
                }
                last = j;
            }
        }
        if (first == last) {
            answer = nums[i];
        }
    }
    return answer;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class SingleNumberFinder
{
    public static int SingleNumber(int[] nums)
    {
        int answer = 0;
        List<int> al = new List<int>();
        foreach (int n in nums)
        {
            al.Add(n);
        }
        for (int i = 0; i < nums.Length; i++)
        {
            int test = nums[i];
            if (al.IndexOf(test) == al.LastIndexOf(test))
            {
                answer = nums[i];
            }
        }
        return answer;
    }
}
"""
}}

DATA3["T170"] = {"outputs": {
"python": r"""
def solution(x, a):
    seen = set()
    sum1 = sum(range(x + 1))
    sum2 = 0
    for i in range(len(a)):
        if a[i] in seen:
            continue
        seen.add(a[i])
        sum2 += a[i]
        if sum1 == sum2:
            return i
    return -1
""",
"c": r"""
#include <stdlib.h>

int solution(int x, const int *a, int aLen) {
    int sum1 = 0;
    for (int i = 0; i <= x; i++) {
        sum1 += i;
    }
    int offset = 1000000;
    int span = 2000001;
    char *set = calloc((size_t)span, 1);
    if (set == NULL) {
        return -1;
    }
    int sum2 = 0;
    int result = -1;
    for (int i = 0; i < aLen; i++) {
        int v = a[i];
        if (set[v + offset]) {
            continue;
        }
        set[v + offset] = 1;
        sum2 += v;
        if (sum1 == sum2) {
            result = i;
            break;
        }
    }
    free(set);
    return result;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class SumFinder
{
    public static int Solution(int x, int[] a)
    {
        HashSet<int> set = new HashSet<int>();
        int sum1 = 0, sum2 = 0;
        for (int i = 0; i <= x; i++)
        {
            sum1 += i;
        }
        for (int i = 0; i < a.Length; i++)
        {
            if (set.Contains(a[i]))
            {
                continue;
            }
            set.Add(a[i]);
            sum2 += a[i];
            if (sum1 == sum2)
            {
                return i;
            }
        }
        return -1;
    }
}
"""
}}

DATA3["T171"] = {"outputs": {
"python": r"""
def solution(x, a):
    leaves = set()
    for i in range(len(a)):
        leaves.add(a[i])
        if x in leaves and len(leaves) == x:
            return i
    return -1
""",
"c": r"""
#include <stdlib.h>
#include <string.h>

int solution(int x, const int *a, int aLen) {
    int offset = 1000000;
    int span = 2000001;
    char *seen = calloc((size_t)span, 1);
    if (seen == NULL) {
        return -1;
    }
    int count = 0;
    int hasX = 0;
    int result = -1;
    for (int i = 0; i < aLen; i++) {
        int v = a[i];
        if (!seen[v + offset]) {
            seen[v + offset] = 1;
            count++;
        }
        if (v == x) {
            hasX = 1;
        }
        if (hasX && count == x) {
            result = i;
            break;
        }
    }
    free(seen);
    return result;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int x, int[] a)
    {
        HashSet<int> leaves = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            leaves.Add(a[i]);
            if (leaves.Contains(x) && leaves.Count == x)
            {
                return i;
            }
        }
        return -1;
    }
}
"""
}}

DATA3["T202"] = {"outputs": {
"python": r"""
import os
import shutil


def copy_folder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            rel = os.path.relpath(root, src)
            d = dest if rel == "." else os.path.join(dest, rel)
            if not os.path.exists(d):
                os.mkdir(d)
            for name in files:
                s = os.path.join(root, name)
                try:
                    shutil.copy(s, os.path.join(d, name))
                except Exception as e:
                    print(e)
    except Exception as ex:
        print(ex)
""",
"c": r"""
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

#ifdef _WIN32
#include <direct.h>
#define MKDIR(p) _mkdir(p)
#else
#define MKDIR(p) mkdir(p, 0755)
#endif

static void copy_tree(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    if (dir == NULL) {
        return;
    }
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        char spath[512], dpath[512];
        snprintf(spath, sizeof(spath), "%s/%s", src, entry->d_name);
        snprintf(dpath, sizeof(dpath), "%s/%s", dest, entry->d_name);
        struct stat st;
        if (stat(spath, &st) != 0) {
            continue;
        }
        if (S_ISDIR(st.st_mode)) {
            MKDIR(dpath);
            copy_tree(spath, dpath);
        } else {
            FILE *in = fopen(spath, "rb");
            FILE *out = fopen(dpath, "wb");
            if (in != NULL && out != NULL) {
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
}

void copy_folder(const char *src, const char *dest) {
    copy_tree(src, dest);
}
""",
"csharp": r"""
using System;
using System.IO;

public static class FolderCopy
{
    public static void CopyFolder(string src, string dest)
    {
        try
        {
            foreach (string s in Directory.EnumerateFileSystemEntries(src))
            {
                try
                {
                    string d = Path.Combine(dest, Path.GetFileName(s));
                    if (Directory.Exists(s))
                    {
                        if (!Directory.Exists(d))
                        {
                            Directory.CreateDirectory(d);
                        }
                        CopyFolder(s, d);
                        continue;
                    }
                    File.Copy(s, d);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }
    }
}
"""
}}

DATA3["T212"] = {"outputs": {
"python": r"""
def main():
    needle = "ABC"
    haystack = "ABCDSGDABCSAGAABCCCCAAABAABC"
    number_of_occurences = 0
    index = haystack.find(needle)
    while index != -1:
        number_of_occurences += 1
        haystack = haystack[index + len(needle):]
        index = haystack.find(needle)
    print(str(number_of_occurences))
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *needle = "ABC";
    char haystack[] = "ABCDSGDABCSAGAABCCCCAAABAABC";
    int numberOfOccurences = 0;
    size_t needleLen = strlen(needle);
    char *index = strstr(haystack, needle);
    while (index != NULL) {
        numberOfOccurences++;
        memmove(haystack, index + needleLen, strlen(index + needleLen) + 1);
        index = strstr(haystack, needle);
    }
    printf("%d\n", numberOfOccurences);
    return 0;
}
""",
"csharp": r"""
using System;

public static class NeedleCounter
{
    public static void Main(string[] args)
    {
        string needle = "ABC";
        string haystack = "ABCDSGDABCSAGAABCCCCAAABAABC";
        int numberOfOccurences = 0;
        int index = haystack.IndexOf(needle, StringComparison.Ordinal);
        while (index != -1)
        {
            numberOfOccurences++;
            haystack = haystack.Substring(index + needle.Length);
            index = haystack.IndexOf(needle, StringComparison.Ordinal);
        }
        Console.WriteLine("" + numberOfOccurences);
    }
}
"""
}}

DATA3["T224"] = {"outputs": {
"python": r"""
import re


def get_number(s):
    return float(s)


def main():
    input_string = input()
    if not re.fullmatch(r"[+-]?([0-9]*[.])?[0-9]+", input_string):
        print("Not a Number")
    else:
        result2 = get_number(input_string)
        print("result = " + str(result2))
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int matches_number(const char *s) {
    const char *p = s;
    if (*p == '+' || *p == '-') {
        p++;
    }
    const char *intDigits = p;
    while (*p >= '0' && *p <= '9') {
        p++;
    }
    size_t intLen = (size_t)(p - intDigits);
    if (*p == '.') {
        p++;
        const char *fracDigits = p;
        while (*p >= '0' && *p <= '9') {
            p++;
        }
        if (p == fracDigits && intLen == 0) {
            return 0;
        }
    } else if (intLen == 0) {
        return 0;
    }
    return *p == '\0';
}

int main(void) {
    char inputString[256];
    if (fgets(inputString, sizeof(inputString), stdin) == NULL) {
        return 0;
    }
    inputString[strcspn(inputString, "\r\n")] = '\0';
    if (!matches_number(inputString)) {
        printf("Not a Number\n");
    } else {
        double result2 = atof(inputString);
        printf("result = %g\n", result2);
    }
    return 0;
}
""",
"csharp": r"""
using System;
using System.Text.RegularExpressions;

public static class NumberReader
{
    private static double GetNumber(string s)
    {
        return double.Parse(s);
    }

    public static void Main(string[] args)
    {
        string inputString = Console.ReadLine();
        if (!Regex.IsMatch(inputString, @"^[+-]?([0-9]*[.])?[0-9]+$"))
        {
            Console.WriteLine("Not a Number");
        }
        else
        {
            double result2 = GetNumber(inputString);
            Console.WriteLine("result = " + result2);
        }
    }
}
"""
}}

DATA3["T238"] = {"outputs": {
"python": r"""
def main():
    name = "AnuvratAnuvra"
    arr = list(name)
    counts = {}
    for val in arr:
        counts[val] = counts.get(val, 0) + 1
    for key, value in counts.items():
        if value > 1:
            print(str(key) + ":" + str(value))
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *name = "AnuvratAnuvra";
    int counts[256] = {0};
    for (size_t i = 0; i < strlen(name); i++) {
        counts[(unsigned char)name[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 1) {
            printf("%c:%d\n", (char)i, counts[i]);
        }
    }
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;

public static class DuplicateChars
{
    public static void Main(string[] args)
    {
        string name = "AnuvratAnuvra";
        Dictionary<char, int> counts = new Dictionary<char, int>();
        foreach (char val in name.ToCharArray())
        {
            counts[val] = counts.TryGetValue(val, out int n) ? n + 1 : 1;
        }
        foreach (KeyValuePair<char, int> entry in counts)
        {
            if (entry.Value > 1)
            {
                Console.WriteLine(entry.Key + ":" + entry.Value);
            }
        }
    }
}
"""
}}

DATA3["T241"] = {"outputs": {
"python": r"""
def main():
    hm = {}
    print("Enter an String:")
    s1 = input()
    for ch in s1:
        hm[ch] = hm.get(ch, 0) + 1
    print("The Charecters are:" + str(hm))
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    int counts[256] = {0};
    char s1[256];
    printf("Enter an String:\n");
    if (fgets(s1, sizeof(s1), stdin) == NULL) {
        return 0;
    }
    s1[strcspn(s1, "\r\n")] = '\0';
    for (size_t i = 0; i < strlen(s1); i++) {
        counts[(unsigned char)s1[i]]++;
    }
    printf("The Charecters are:{");
    int first = 1;
    for (int i = 0; i < 256; i++) {
        if (counts[i] > 0) {
            if (!first) {
                printf(", ");
            }
            printf("%c=%d", (char)i, counts[i]);
            first = 0;
        }
    }
    printf("}\n");
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;

public static class CharFrequency
{
    public static void Main(string[] args)
    {
        Dictionary<char, int> hm = new Dictionary<char, int>();
        Console.WriteLine("Enter an String:");
        string s1 = Console.ReadLine();
        foreach (char ch in s1)
        {
            if (hm.ContainsKey(ch))
            {
                hm[ch] = hm[ch] + 1;
            }
            else
            {
                hm[ch] = 1;
            }
        }
        List<string> parts = new List<string>();
        foreach (KeyValuePair<char, int> entry in hm)
        {
            parts.Add(entry.Key + "=" + entry.Value);
        }
        Console.WriteLine("The Charecters are:{" + string.Join(", ", parts) + "}");
    }
}
"""
}}

DATA3["T253"] = {"outputs": {
"python": r"""
import random


def shuffle_array(ar):
    rnd = random.Random()
    i = len(ar) - 1
    while i > 0:
        index = rnd.randint(0, i)
        ar[index], ar[i] = ar[i], ar[index]
        i -= 1
""",
"c": r"""
#include <stdlib.h>
#include <time.h>

void shuffle_array(int *ar, int len) {
    srand((unsigned int)time(NULL));
    int i = len - 1;
    while (i > 0) {
        int index = rand() % (i + 1);
        int a = ar[index];
        ar[index] = ar[i];
        ar[i] = a;
        i--;
    }
}
""",
"csharp": r"""
using System;

public static class ArrayShuffler
{
    public static void ShuffleArray(int[] ar)
    {
        Random rnd = new Random();
        for (int i = ar.Length - 1; i > 0; i--)
        {
            int index = rnd.Next(i + 1);
            int a = ar[index];
            ar[index] = ar[i];
            ar[i] = a;
        }
    }
}
"""
}}
