DATA_T6 = {}

DATA_T6["T238"] = {
"python": r'''def main():
    name = "AnuvratAnuvra"
    arr = list(name)
    counts = {}
    for val in arr:
        counts[val] = counts[val] + 1 if val in counts else 1
    for key, value in counts.items():
        if value > 1:
            print(str(key) + ":" + str(value))

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    const char *name = "AnuvratAnuvra";
    size_t len = strlen (name);
    int counts [256] = {0};
    for (size_t i = 0; i < len; i ++) {
        counts [(unsigned char) name [i]] ++;
    }
    for (int ch = 0; ch < 256; ch ++) {
        if (counts [ch] > 1) {
            printf ("%c:%d\n", (char) ch, counts [ch]);
        }
    }
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class DuplicateChars
{
    public static void Main(string[] args)
    {
        string name = "AnuvratAnuvra";
        char[] arr = name.ToCharArray();
        Dictionary<char, int> map = new Dictionary<char, int>();
        foreach (char val in arr)
        {
            map[val] = map.ContainsKey(val) ? map[val] + 1 : 1;
        }
        foreach (KeyValuePair<char, int> entry in map)
        {
            if (entry.Value > 1)
            {
                char key = entry.Key;
                object value = entry.Value;
                Console.WriteLine(key + ":" + value);
            }
        }
    }
}
''',
}

DATA_T6["T202"] = {
"python": r'''import os
import shutil

def copyFolder(src, dest):
    try:
        for current, dirs, files in os.walk(src):
            relative = os.path.relpath(current, src)
            targetDir = dest if relative == "." else os.path.join(dest, relative)
            if not os.path.exists(targetDir):
                os.mkdir(targetDir)
            for f in files:
                try:
                    shutil.copy(os.path.join(current, f), os.path.join(targetDir, f))
                except Exception as e:
                    print(e)
    except Exception as ex:
        print(ex)
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>

static void mkdir_p (const char *path) {
    char tmp [512];
    snprintf (tmp, sizeof (tmp), "%s", path);
    size_t len = strlen (tmp);
    if (len == 0) return;
    if (tmp [len - 1] == '/' || tmp [len - 1] == '\\') tmp [len - 1] = '\0';
    for (char *p = tmp + 1; *p; p ++) {
        if (*p == '/' || *p == '\\') {
            *p = '\0';
            mkdir (tmp, 0755);
            *p = '/';
        }
    }
    mkdir (tmp, 0755);
}

static void copyFolder (const char *src, const char *dest) {
    DIR *dir = opendir (src);
    if (dir == NULL) {
        perror ("opendir");
        return;
    }
    mkdir_p (dest);
    struct dirent *entry;
    while ((entry = readdir (dir)) != NULL) {
        if (strcmp (entry->d_name, ".") == 0 || strcmp (entry->d_name, "..") == 0) continue;
        char srcPath [512], destPath [512];
        snprintf (srcPath, sizeof (srcPath), "%s/%s", src, entry->d_name);
        snprintf (destPath, sizeof (destPath), "%s/%s", dest, entry->d_name);
        DIR *sub = opendir (srcPath);
        if (sub != NULL) {
            closedir (sub);
            copyFolder (srcPath, destPath);
        } else {
            FILE *in = fopen (srcPath, "rb");
            FILE *out = fopen (destPath, "wb");
            if (in != NULL && out != NULL) {
                char buffer [4096];
                size_t n;
                while ((n = fread (buffer, 1, sizeof (buffer), in)) > 0) {
                    fwrite (buffer, 1, n, out);
                }
            }
            if (in != NULL) fclose (in);
            if (out != NULL) fclose (out);
        }
    }
    closedir (dir);
}
''',
"csharp": r'''using System;
using System.IO;

public static class FolderCopier
{
    public static void CopyFolder(string src, string dest)
    {
        try
        {
            foreach (string s in Directory.GetFileSystemEntries(src))
            {
                try
                {
                    string d = Path.Combine(dest, Path.GetFileName(s));
                    if (Directory.Exists(s))
                    {
                        if (!Directory.Exists(d)) Directory.CreateDirectory(d);
                        CopyFolder(s, d);
                        continue;
                    }
                    File.Copy(s, d, true);
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
''',
}

DATA_T6["T693"] = {
"python": r'''def findCombinationsCount(amount, coins, checkFromIndex):
    if amount == 0:
        return 1
    elif amount < 0 or len(coins) == checkFromIndex:
        return 0
    else:
        withFirstCoin = findCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex)
        withoutFirstCoin = findCombinationsCount(amount, coins, checkFromIndex + 1)
        return withFirstCoin + withoutFirstCoin
''',
"c": r'''int findCombinationsCount (int amount, const int *coins, int coinsLen, int checkFromIndex) {
    if (amount == 0) return 1;
    else if (amount < 0 || coinsLen == checkFromIndex) return 0;
    else {
        int withFirstCoin = findCombinationsCount (amount - coins [checkFromIndex], coins, coinsLen, checkFromIndex);
        int withoutFirstCoin = findCombinationsCount (amount, coins, coinsLen, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}
''',
"csharp": r'''public static class CoinCombinations
{
    public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0) return 1;
        else if (amount < 0 || coins.Length == checkFromIndex) return 0;
        else
        {
            int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
            int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
            return withFirstCoin + withoutFirstCoin;
        }
    }
}
''',
}

DATA_T6["T347"] = {
"python": r'''SEPARATOR = " "
EXPONENT = 3

class Processor:
    def getName(self, value):
        return ""

SCALE = Processor()
unitProcessor = Processor()
tensProcessor = Processor()

def getName(value):
    buffer = []
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[len(value) - 4:])
    else:
        number = int(value)
    number %= 1000
    if number >= 100:
        buffer.append(unitProcessor.getName(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(SCALE.getName(EXPONENT))
    tensName = tensProcessor.getName(number % 100)
    if tensName != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tensName)
    return "".join(buffer)
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SEPARATOR " "
#define EXPONENT 3

static const char *unitProcessorGetName (int value) {
    (void) value;
    return "";
}

static const char *scaleGetName (int exponent) {
    (void) exponent;
    return "";
}

static const char *tensProcessorGetName (int value) {
    (void) value;
    return "";
}

static char *getName (const char *value) {
    char *buffer = malloc (256);
    if (buffer == NULL) return NULL;
    buffer [0] = '\0';
    int number;
    if (value [0] == '\0') {
        number = 0;
    } else if ((int) strlen (value) > 4) {
        number = atoi (value + strlen (value) - 4);
    } else {
        number = atoi (value);
    }
    number %= 1000;
    if (number >= 100) {
        strcat (buffer, unitProcessorGetName (number / 100));
        strcat (buffer, SEPARATOR);
        strcat (buffer, scaleGetName (EXPONENT));
    }
    const char *tensName = tensProcessorGetName (number % 100);
    if (tensName [0] != '\0' && number >= 100) {
        strcat (buffer, SEPARATOR);
    }
    strcat (buffer, tensName);
    return buffer;
}
''',
"csharp": r'''using System;
using System.Text;

public class NameProcessor
{
    public virtual string GetName(int value) { return ""; }
}

public class ThousandsNameBuilder
{
    private const string SEPARATOR = " ";
    private const int EXPONENT = 3;

    private readonly NameProcessor unitProcessor = new NameProcessor();
    private readonly NameProcessor scaleProcessor = new NameProcessor();
    private readonly NameProcessor tensProcessor = new NameProcessor();

    public string GetName(string value)
    {
        StringBuilder buffer = new StringBuilder();
        int number;
        if ("".Equals(value))
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
            buffer.Append(unitProcessor.GetName(number / 100));
            buffer.Append(SEPARATOR);
            buffer.Append(scaleProcessor.GetName(EXPONENT));
        }
        string tensName = tensProcessor.GetName(number % 100);
        if (!"".Equals(tensName) && (number >= 100))
        {
            buffer.Append(SEPARATOR);
        }
        buffer.Append(tensName);
        return buffer.ToString();
    }
}
''',
}

DATA_T6["T253"] = {
"python": r'''import random

def shuffleArray(ar):
    rnd = random.Random()
    for i in range(len(ar) - 1, 0, -1):
        index = rnd.randint(0, i)
        a = ar[index]
        ar[index] = ar[i]
        ar[i] = a
''',
"c": r'''#include <stdlib.h>

static unsigned long seed = 12345;

static int rndNextInt (int bound) {
    seed = seed * 6364136223846793005UL + 1442695040888963407UL;
    return (int) ((seed >> 33) % (unsigned long) bound);
}

static void shuffleArray (int *ar, int arLen) {
    for (int i = arLen - 1; i > 0; i --) {
        int index = rndNextInt (i + 1);
        int a = ar [index];
        ar [index] = ar [i];
        ar [i] = a;
    }
}
''',
"csharp": r'''using System;

public static class ArrayShuffler
{
    private static readonly Random rnd = new Random();

    public static void ShuffleArray(int[] ar)
    {
        for (int i = ar.Length - 1; i > 0; i--)
        {
            int index = rnd.Next(i + 1);
            int a = ar[index];
            ar[index] = ar[i];
            ar[i] = a;
        }
    }
}
''',
}
