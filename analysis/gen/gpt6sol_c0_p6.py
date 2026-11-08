DATA6 = {
    "T333": {"outputs": {
        "python": '''class UnitProcessor:
    def get_name(self, number):
        raise NotImplementedError


TOKENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
UNION_SEPARATOR = "-"


class TensNamer:
    def __init__(self, unit_processor):
        self.unit_processor = unit_processor

    def get_name(self, value):
        buffer = []
        if len(value) > 3:
            number = int(value[-3:])
        else:
            number = int(value)
        number %= 100
        tens_found = False
        if number >= 20:
            buffer.append(TOKENS[number // 10 - 2])
            number %= 10
            tens_found = True
        if number != 0:
            if tens_found:
                buffer.append(UNION_SEPARATOR)
            buffer.append(self.unit_processor.get_name(number))
        return "".join(buffer)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern const char *unit_processor_get_name(int number);

static const char *TOKENS[8] = { "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" };
#define UNION_SEPARATOR "-"

char *get_name(const char *value) {
    int number;
    if (strlen(value) > 3) {
        number = atoi(value + strlen(value) - 3);
    } else {
        number = atoi(value);
    }
    number %= 100;
    char buffer[128];
    buffer[0] = '\0';
    if (number >= 20) {
        strcat(buffer, TOKENS[number / 10 - 2]);
        number %= 10;
    }
    if (number != 0) {
        if (buffer[0] != '\0') {
            strcat(buffer, UNION_SEPARATOR);
        }
        strcat(buffer, unit_processor_get_name(number));
    }
    return strdup(buffer);
}''',
        "csharp": '''using System;
using System.Text;

public class TensNamer
{
    private static readonly string[] Tokens = { "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" };
    private const string UnionSeparator = "-";
    private readonly IUnitProcessor unitProcessor;

    public TensNamer(IUnitProcessor unitProcessor)
    {
        this.unitProcessor = unitProcessor;
    }

    public string GetName(string value)
    {
        var buffer = new StringBuilder();
        int number;
        if (value.Length > 3)
        {
            number = int.Parse(value.Substring(value.Length - 3));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 100;
        bool tensFound = false;
        if (number >= 20)
        {
            buffer.Append(Tokens[number / 10 - 2]);
            number %= 10;
            tensFound = true;
        }
        if (number != 0)
        {
            if (tensFound)
            {
                buffer.Append(UnionSeparator);
            }
            buffer.Append(unitProcessor.GetName(number));
        }
        return buffer.ToString();
    }
}

public interface IUnitProcessor
{
    string GetName(int number);
}'''
    }},
    "T807": {"outputs": {
        "python": '''def remove_duplicates(s):
    seen = set()
    result = []
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)
    return "".join(result)''',
        "c": r'''#include <stdlib.h>
#include <string.h>

char *remove_duplicates(const char *s) {
    size_t len = strlen(s);
    char *no_dupes = malloc(len + 1);
    size_t pos = 0;
    char seen[256] = { 0 };
    for (size_t i = 0; i < len; i++) {
        unsigned char ch = (unsigned char) s[i];
        if (!seen[ch]) {
            seen[ch] = 1;
            no_dupes[pos++] = s[i];
        }
    }
    no_dupes[pos] = '\0';
    return no_dupes;
}''',
        "csharp": '''using System.Collections.Generic;
using System.Text;

public static class Deduplicator
{
    public static string RemoveDuplicates(string s)
    {
        var seen = new HashSet<char>();
        var noDupes = new StringBuilder();
        foreach (char c in s)
        {
            if (seen.Add(c))
            {
                noDupes.Append(c);
            }
        }
        return noDupes.ToString();
    }
}'''
    }},
    "T447": {"outputs": {
        "python": '''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    a1 = sorted(s1)
    a2 = sorted(s2)
    print("".join(a1))
    print("".join(a2))
    return a1 == a2''',
        "c": r'''#include <stdio.h>
#include <stdbool.h>
#include <string.h>

static int compare_chars(const void *x, const void *y) {
    return *(const char *) x - *(const char *) y;
}

static bool is_anagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) {
        return false;
    }
    char arr1[strlen(s1) + 1];
    char arr2[strlen(s2) + 1];
    strcpy(arr1, s1);
    strcpy(arr2, s2);
    qsort(arr1, strlen(arr1), 1, compare_chars);
    qsort(arr2, strlen(arr2), 1, compare_chars);
    printf("%s\n%s\n", arr1, arr2);
    return strcmp(arr1, arr2) == 0;
}''',
        "csharp": '''using System;
using System.Linq;

public static class AnagramChecker
{
    public static bool IsAnagram(string s1, string s2)
    {
        if (s1.Length != s2.Length)
        {
            return false;
        }
        var arr1 = s1.ToCharArray();
        var arr2 = s2.ToCharArray();
        Array.Sort(arr1);
        Array.Sort(arr2);
        Console.WriteLine(new string(arr1));
        Console.WriteLine(new string(arr2));
        return arr1.SequenceEqual(arr2);
    }
}'''
    }},
    "T397": {"outputs": {
        "python": '''import os
import shutil


def copy_folder(src, dest):
    try:
        for root, dirs, files in os.walk(src):
            rel_root = os.path.relpath(root, src)
            target_root = os.path.join(dest, rel_root) if rel_root != "." else dest
            if not os.path.exists(target_root):
                os.mkdir(target_root)
            for name in files:
                shutil.copy(os.path.join(root, name), os.path.join(target_root, name))
    except Exception as ex:
        print(ex)''',
        "c": r'''#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

static void copy_folder(const char *src, const char *dest) {
    DIR *dir = opendir(src);
    if (dir == NULL) {
        perror("opendir failed");
        return;
    }
    struct dirent *entry;
    mkdir(dest, 0755);
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        char src_path[1024], dest_path[1024];
        snprintf(src_path, sizeof(src_path), "%s/%s", src, entry->d_name);
        snprintf(dest_path, sizeof(dest_path), "%s/%s", dest, entry->d_name);
        struct stat st;
        if (stat(src_path, &st) == 0 && S_ISDIR(st.st_mode)) {
            copy_folder(src_path, dest_path);
        } else {
            FILE *in = fopen(src_path, "rb");
            FILE *out = fopen(dest_path, "wb");
            if (in && out) {
                char buffer[4096];
                size_t n;
                while ((n = fread(buffer, 1, sizeof(buffer), in)) > 0) {
                    fwrite(buffer, 1, n, out);
                }
            }
            if (in) fclose(in);
            if (out) fclose(out);
        }
    }
    closedir(dir);
}''',
        "csharp": '''using System;
using System.IO;

public static class FolderCopier
{
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
    }
}'''
    }},
}
