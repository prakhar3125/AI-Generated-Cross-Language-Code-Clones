DATA2 = {
"T721": {"outputs": {
"python": r"""def num_letters(s):
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    ans = ""
    for i in range(26):
        if count[i] != 0:
            ans += str(count[i]) + chr(i + ord('a'))
    return ans
""",
"c": r"""#include <stdio.h>

void numLetters(const char *s, char *ans) {
    int count[26] = {0};
    for (const char *p = s; *p; p++) count[(unsigned char)*p - 'a']++;
    int pos = 0;
    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) {
            pos += sprintf(ans + pos, "%d%c", count[i], 'a' + i);
        }
    }
    ans[pos] = '\0';
}
""",
"csharp": r"""using System.Text;

public static string NumLetters(string s)
{
    int[] count = new int[26];
    foreach (char c in s) count[c - 'a']++;
    var ans = new StringBuilder();
    for (int i = 0; i < 26; i++)
    {
        if (count[i] != 0) ans.Append(count[i]).Append((char)(i + 'a'));
    }
    return ans.ToString();
}
""",
}},
"T338": {"outputs": {
"python": r"""class NumberToWord:
    def pw(self, number, label):
        if number > 0:
            print(number, label, end="")

def main():
    n = int(input("Enter an integer number: "))
    if n <= 0:
        print("Enter numbers greater than 0", end="")
    else:
        a = NumberToWord()
        print("After conversion number in words is :", end="")
        a.pw(n // 1000000000, " Hundred")
        a.pw((n // 10000000) % 100, " crore")
        a.pw((n // 100000) % 100, " lakh")
        a.pw((n // 1000) % 100, " thousand")
        a.pw((n // 100) % 10, " hundred")
        a.pw(n % 100, "")
""",
"c": r"""#include <stdio.h>

void pw(int number, const char *label) {
    if (number > 0) printf("%d%s", number, label);
}

int main(void) {
    int n = 0;
    printf("Enter an integer number: ");
    scanf("%d", &n);
    if (n <= 0) {
        printf("Enter numbers greater than 0");
    } else {
        printf("After conversion number in words is :");
        pw(n / 1000000000, " Hundred");
        pw((n / 10000000) % 100, " crore");
        pw((n / 100000) % 100, " lakh");
        pw((n / 1000) % 100, " thousand");
        pw((n / 100) % 10, " hundred");
        pw(n % 100, "");
    }
    return 0;
}
""",
"csharp": r"""using System;

public class NumberToWord
{
    public void Pw(int number, string label)
    {
        if (number > 0) Console.Write(number + label);
    }
}

public static class Program
{
    public static void Main(string[] args)
    {
        int n = 0;
        Console.Write("Enter an integer number: ");
        n = int.Parse(Console.ReadLine());
        if (n <= 0)
        {
            Console.Write("Enter numbers greater than 0");
        }
        else
        {
            var a = new NumberToWord();
            Console.Write("After conversion number in words is :");
            a.Pw(n / 1000000000, " Hundred");
            a.Pw((n / 10000000) % 100, " crore");
            a.Pw((n / 100000) % 100, " lakh");
            a.Pw((n / 1000) % 100, " thousand");
            a.Pw((n / 100) % 10, " hundred");
            a.Pw(n % 100, "");
        }
    }
}
""",
}},
"T654": {"outputs": {
"python": r"""def filter(source, start, end, dest, dstart, dend, decimal_digits=2):
    dot_pos = -1
    length = len(dest)
    for i in range(length):
        if dest[i] in ".,":
            dot_pos = i
            break
    if dot_pos >= 0:
        if source in (".", ","):
            return ""
        if dend <= dot_pos:
            return None
        if length - dot_pos > decimal_digits:
            return ""
    return None
""",
"c": r"""#include <string.h>

const char *filter(const char *source, int start, int end, const char *dest,
                   int dstart, int dend, int decimalDigits) {
    int dotPos = -1;
    int len = (int)strlen(dest);
    for (int i = 0; i < len; i++) {
        if (dest[i] == '.' || dest[i] == ',') {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0) {
        if (source[0] == '.' || source[0] == ',') return "";
        if (dend <= dotPos) return 0;
        if (len - dotPos > decimalDigits) return "";
    }
    return 0;
}
""",
"csharp": r"""public class DecimalFilter
{
    private int decimalDigits = 2;

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
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
            if (source == "." || source == ",") return "";
            if (dend <= dotPos) return null;
            if (len - dotPos > decimalDigits) return "";
        }
        return null;
    }
}
""",
}},
"T102": {"outputs": {
"python": r"""def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    while len(s2) > 0:
        ch = s2[0]
        if ch not in s1:
            return False
        s1 = s1.replace(ch, "", 1)
        s2 = s2.replace(ch, "", 1)
    return True
""",
"c": r"""#include <stdbool.h>
#include <string.h>

bool isAnagram(char *s1, char *s2) {
    if (strlen(s1) != strlen(s2)) return false;
    while (s2[0] != '\0') {
        char target = s2[0];
        char *hit = strchr(s1, target);
        if (hit == NULL) return false;
        memmove(hit, hit + 1, strlen(hit));
        memmove(s2, s2 + 1, strlen(s2));
    }
    return true;
}
""",
"csharp": r"""using System;

public static bool IsAnagram(string s1, string s2)
{
    if (s1.Length != s2.Length) return false;
    while (s2.Length > 0)
    {
        char target = s2[0];
        if (!s1.Contains("" + target)) return false;
        int pos1 = s1.IndexOf(target);
        int pos2 = s2.IndexOf(target);
        s1 = s1.Remove(pos1, 1);
        s2 = s2.Remove(pos2, 1);
    }
    return true;
}
""",
}},
"T245": {"outputs": {
"python": r"""def main():
    st = input("Enter the String")
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + str(ar[i]), end="")
""",
"c": r"""#include <stdio.h>

int main(void) {
    char st[1024];
    int ar[256] = {0};
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) return 0;
    for (char *p = st; *p && *p != '\n'; p++) {
        ar[(unsigned char)*p]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) printf("%c", ch);
            else printf("%c%d", ch, ar[i]);
        }
    }
    return 0;
}
""",
"csharp": r"""using System;

public static void Main(string[] args)
{
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char ch in st) ar[ch]++;
    for (int i = 0; i < 256; i++)
    {
        char ch = (char)i;
        if (ar[i] > 0)
        {
            if (ar[i] == 1) Console.Write(ch);
            else Console.Write(ch + "" + ar[i]);
        }
    }
}
""",
}},
}
