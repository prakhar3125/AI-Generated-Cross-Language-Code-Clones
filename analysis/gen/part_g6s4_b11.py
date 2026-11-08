DATA_B11 = {
"T249": {
"python": r"""
def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch) % 256] += 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + str(ar[i]), end="")
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    printf("Enter the String");
    char st[1024];
    if (fgets(st, sizeof(st), stdin) == NULL) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    for (size_t i = 0; i < strlen(st); i++) {
        unsigned char c = (unsigned char)st[i];
        ar[c] = ar[c] + 1;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", ch);
            } else {
                printf("%c%d", ch, ar[i]);
            }
        }
    }
    return 0;
}
""",
"csharp": r"""
using System;

public static class CharCounter
{
    public static void Main(string[] a)
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        foreach (char c in st)
        {
            ar[c] = ar[c] + 1;
        }
        for (int i = 0; i < 256; i++)
        {
            char ch = (char)i;
            if (ar[i] > 0)
            {
                if (ar[i] == 1)
                {
                    Console.Write(ch);
                }
                else
                {
                    Console.Write(ch + "" + ar[i]);
                }
            }
        }
    }
}
"""
},
"T372": {
"python": r"""
def capitalize(s):
    if s is None or len(s) == 0:
        return ""
    first = s[0]
    if first.isupper():
        return s
    else:
        return first.upper() + s[1:]
""",
"c": r"""
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

char *capitalize(const char *s) {
    if (s == NULL || strlen(s) == 0) {
        return "";
    }
    char *out = malloc(strlen(s) + 1);
    strcpy(out, s);
    char first = s[0];
    if (isupper((unsigned char)first)) {
        return out;
    } else {
        out[0] = (char)toupper((unsigned char)first);
        return out;
    }
}
""",
"csharp": r"""
public static class TextUtil
{
    public static string Capitalize(string s)
    {
        if (s == null || s.Length == 0)
        {
            return "";
        }
        char first = s[0];
        if (char.IsUpper(first))
        {
            return s;
        }
        else
        {
            return char.ToUpper(first) + s.Substring(1);
        }
    }
}
"""
}
}
