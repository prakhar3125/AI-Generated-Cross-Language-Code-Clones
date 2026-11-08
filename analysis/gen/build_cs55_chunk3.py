import ast
import json

SEED = "C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/seeds/chunk3.json"
OUT = "C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/out/claude-sonnet-5-5_chunk3.json"

TRANSLATIONS = {}
TRANSLATIONS["T471"] = {
    "python": r'''
def get_max(start, array):
    best = start
    for value in array:
        if value > best:
            best = value
    return best

def main():
    large = [0] * 10
    array = [33, 55, 13, 46, 87, 42, 10, 34, 43, 56]
    k = 0
    for _ in array:
        large[k] = get_max(0, array)
        k += 1
    print("Largest 5 is: " + str(large[:5]))
''',
    "c": r'''
#include <stdio.h>

int getMax(int start, const int *array, int size) {
    int best = start;
    for (int i = 0; i < size; i++) {
        if (array[i] > best) {
            best = array[i];
        }
    }
    return best;
}

int main(void) {
    int large[10];
    int array[] = {33, 55, 13, 46, 87, 42, 10, 34, 43, 56};
    int size = (int)(sizeof(array) / sizeof(array[0]));
    int k = 0;
    for (int i = 0; i < size; i++) {
        large[k++] = getMax(0, array, size);
    }
    printf("Largest 5 is: [");
    for (int i = 0; i < 5; i++) {
        printf("%d%s", large[i], i < 4 ? ", " : "");
    }
    printf("]\n");
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    private static int GetMax(int start, int[] array)
    {
        int best = start;
        foreach (int value in array)
        {
            if (value > best)
            {
                best = value;
            }
        }
        return best;
    }

    public static void Main()
    {
        int[] large = new int[10];
        int[] array = { 33, 55, 13, 46, 87, 42, 10, 34, 43, 56 };
        int k = 0;
        for (int i = 0; i < array.Length; i++)
        {
            large[k++] = GetMax(0, array);
        }
        int[] firstFive = new int[5];
        Array.Copy(large, firstFive, 5);
        Console.WriteLine("Largest 5 is: [" + string.Join(", ", firstFive) + "]");
    }
}
''',
}
TRANSLATIONS["T23"] = {
    "python": r'''
def center(s, size, pad):
    if s is None or size <= len(s):
        return s
    left = (size - len(s)) // 2
    result = pad * left + s
    while len(result) < size:
        result += pad
    return result
''',
    "c": r'''
#include <stdlib.h>
#include <string.h>

char *center(char *s, int size, char pad) {
    if (s == NULL || size <= (int)strlen(s)) {
        return s;
    }
    int len = (int)strlen(s);
    char *sb = (char *)malloc(size + 1);
    int pos = 0;
    for (int i = 0; i < (size - len) / 2; i++) {
        sb[pos++] = pad;
    }
    for (int i = 0; i < len; i++) {
        sb[pos++] = s[i];
    }
    while (pos < size) {
        sb[pos++] = pad;
    }
    sb[pos] = '\0';
    return sb;
}
''',
    "csharp": r'''
using System.Text;

public static class Strings
{
    public static string Center(string s, int size, char pad)
    {
        if (s == null || size <= s.Length)
        {
            return s;
        }
        var sb = new StringBuilder(size);
        for (int i = 0; i < (size - s.Length) / 2; i++)
        {
            sb.Append(pad);
        }
        sb.Append(s);
        while (sb.Length < size)
        {
            sb.Append(pad);
        }
        return sb.ToString();
    }
}
''',
}
TRANSLATIONS["T135"] = {
    "python": r'''
def solution(x, a):
    seen = set()
    sum1 = 0
    sum2 = 0
    for i in range(x + 1):
        sum1 += i
    for i, value in enumerate(a):
        if value in seen:
            continue
        seen.add(value)
        sum2 += value
        if sum1 == sum2:
            return i
    return -1
''',
    "c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    char *seen = (char *)calloc((size_t)X + 1, 1);
    int sum1 = 0;
    int sum2 = 0;
    for (int i = 0; i <= X; i++) {
        sum1 += i;
    }
    for (int i = 0; i < len; i++) {
        int value = A[i];
        if (value >= 0 && value <= X && seen[value]) {
            continue;
        }
        if (value >= 0 && value <= X) {
            seen[value] = 1;
        }
        sum2 += value;
        if (sum1 == sum2) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
''',
    "csharp": r'''
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int X, int[] A)
    {
        var set = new HashSet<int>();
        int sum1 = 0;
        int sum2 = 0;
        for (int i = 0; i <= X; i++)
        {
            sum1 += i;
        }
        for (int i = 0; i < A.Length; i++)
        {
            if (set.Contains(A[i]))
            {
                continue;
            }
            set.Add(A[i]);
            sum2 += A[i];
            if (sum1 == sum2)
            {
                return i;
            }
        }
        return -1;
    }
}
''',
}
TRANSLATIONS["T156"] = {
    "python": r'''
def solution(x, a):
    seen = set()
    sum1 = sum(range(x + 1))
    sum2 = 0
    for i, value in enumerate(a):
        if value in seen:
            continue
        seen.add(value)
        sum2 += value
        if sum1 == sum2:
            return i
    return -1
''',
    "c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    char *seen = (char *)calloc((size_t)X + 1, 1);
    int sum1 = 0;
    int sum2 = 0;
    for (int i = 0; i <= X; i++) {
        sum1 += i;
    }
    int i = 0;
    while (i < len) {
        int value = A[i];
        if (!(value >= 0 && value <= X && seen[value])) {
            if (value >= 0 && value <= X) {
                seen[value] = 1;
            }
            sum2 += value;
            if (sum1 == sum2) {
                free(seen);
                return i;
            }
        }
        i++;
    }
    free(seen);
    return -1;
}
''',
    "csharp": r'''
using System.Collections.Generic;
using System.Linq;

public static class RiverCross
{
    public static int Solution(int X, int[] A)
    {
        var seen = new HashSet<int>();
        int sum1 = Enumerable.Range(0, X + 1).Sum();
        int sum2 = 0;
        for (int i = 0; i < A.Length; i++)
        {
            if (seen.Add(A[i]))
            {
                sum2 += A[i];
                if (sum1 == sum2)
                {
                    return i;
                }
            }
        }
        return -1;
    }
}
''',
}
TRANSLATIONS["T159"] = {
    "python": r'''
def solution(x, a):
    size = len(a)
    check = [0] * x
    cmp_count = 0
    time = -1
    for idx in range(size):
        temp = a[idx]
        if temp <= x:
            if check[temp - 1] > 0:
                continue
            check[temp - 1] += 1
            cmp_count += 1
        if cmp_count == x:
            time = idx
            break
    return time
''',
    "c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int size) {
    int *check = (int *)calloc((size_t)X, sizeof(int));
    int cmp = 0;
    int time = -1;
    for (int x = 0; x < size; x++) {
        int temp = A[x];
        if (temp <= X) {
            if (check[temp - 1] > 0) {
                continue;
            }
            check[temp - 1]++;
            cmp++;
        }
        if (cmp == X) {
            time = x;
            break;
        }
    }
    free(check);
    return time;
}
''',
    "csharp": r'''
public static class LeafTimes
{
    public static int Solution(int X, int[] A)
    {
        int size = A.Length;
        int[] check = new int[X];
        int cmp = 0;
        int time = -1;
        for (int x = 0; x < size; x++)
        {
            int temp = A[x];
            if (temp <= X)
            {
                if (check[temp - 1] > 0)
                {
                    continue;
                }
                check[temp - 1]++;
                cmp++;
            }
            if (cmp == X)
            {
                time = x;
                break;
            }
        }
        return time;
    }
}
''',
}
TRANSLATIONS["T545"] = {
    "python": r'''
def join(values, delimiter):
    parts = []
    for value in values:
        parts.append(value)
        parts.append(delimiter)
    result = "".join(parts)
    if len(result) > 0:
        result = result[:len(result) - len(delimiter)]
    return result
''',
    "c": r'''
#include <stdlib.h>
#include <string.h>

char *join(char **input, int count, const char *delimiter) {
    size_t dlen = strlen(delimiter);
    size_t total = 1;
    for (int i = 0; i < count; i++) {
        total += strlen(input[i]) + dlen;
    }
    char *sb = (char *)malloc(total);
    sb[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(sb, input[i]);
        strcat(sb, delimiter);
    }
    size_t length = strlen(sb);
    if (length > 0) {
        sb[length - dlen] = '\0';
    }
    return sb;
}
''',
    "csharp": r'''
using System.Text;

public static class Joiner
{
    private static string Join(string[] input, string delimiter)
    {
        var sb = new StringBuilder();
        foreach (string value in input)
        {
            sb.Append(value);
            sb.Append(delimiter);
        }
        int length = sb.Length;
        if (length > 0)
        {
            sb.Length = length - delimiter.Length;
        }
        return sb.ToString();
    }
}
''',
}
TRANSLATIONS["T501"] = {
    "python": r'''
def find_min(a, c):
    x = a[c]
    position = c
    while c < len(a):
        if x > a[c]:
            x = a[c]
            position = c
        c += 1
    return position
''',
    "c": r'''
int findMIN(const int *A, int c, int len) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}
''',
    "csharp": r'''
public static class MinFinder
{
    public static int FindMin(int[] A, int c)
    {
        int x = A[c];
        int position = c;
        while (c < A.Length)
        {
            if (x > A[c])
            {
                x = A[c];
                position = c;
            }
            c++;
        }
        return position;
    }
}
''',
}
TRANSLATIONS["T744"] = {
    "python": r'''
import random

def t_gen():
    return random.randint(1, 10)

def tortoise_moves():
    roll = t_gen()
    if roll in (1, 2, 3, 4, 5):
        return 3
    if roll in (6, 7, 8):
        return 1
    if roll in (9, 10):
        return -6
    return 0
''',
    "c": r'''
#include <stdlib.h>
#include <time.h>

int tGen(void) {
    return rand() % 10 + 1;
}

int tortoiseMoves(void) {
    switch (tGen()) {
        case 1: case 2: case 3: case 4: case 5:
            return 3;
        case 6: case 7: case 8:
            return 1;
        case 9: case 10:
            return -6;
        default:
            return 0;
    }
}
''',
    "csharp": r'''
using System;

public class RaceSimulator
{
    private static readonly Random Rng = new Random();

    private static int TGen()
    {
        return Rng.Next(1, 11);
    }

    public int TortoiseMoves()
    {
        switch (TGen())
        {
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                return 3;
            case 6:
            case 7:
            case 8:
                return 1;
            case 9:
            case 10:
                return -6;
            default:
                return 0;
        }
    }
}
''',
}
TRANSLATIONS["T721"] = {
    "python": r'''
def num_letters(s):
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    ans = ""
    for i in range(26):
        if count[i] != 0:
            ans += str(count[i]) + chr(i + ord('a'))
    return ans
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

void num_letters(const char *s, char *ans) {
    int count[26] = {0};
    size_t len = strlen(s);
    for (size_t i = 0; i < len; i++) {
        count[(unsigned char)s[i] - 'a']++;
    }
    int pos = 0;
    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) {
            pos += sprintf(ans + pos, "%d%c", count[i], (char)(i + 'a'));
        }
    }
    ans[pos] = '\0';
}
''',
    "csharp": r'''
using System.Text;

public static class LetterCounter
{
    public static string NumLetters(string s)
    {
        int[] count = new int[26];
        foreach (char c in s)
        {
            count[c - 'a']++;
        }
        var ans = new StringBuilder();
        for (int i = 0; i < 26; i++)
        {
            if (count[i] != 0)
            {
                ans.Append(count[i]).Append((char)(i + 'a'));
            }
        }
        return ans.ToString();
    }
}
''',
}
TRANSLATIONS["T338"] = {
    "python": r'''
class NumberToWord:
    def pw(self, number, label):
        if number > 0:
            print(str(number) + label, end="")

def main():
    n = int(input("Enter an integer number: "))
    if n <= 0:
        print("Enter numbers greater than 0", end="")
    else:
        converter = NumberToWord()
        print("After conversion number in words is :", end="")
        converter.pw(n // 1000000000, " Hundred")
        converter.pw((n // 10000000) % 100, " crore")
        converter.pw((n // 100000) % 100, " lakh")
        converter.pw((n // 1000) % 100, " thousand")
        converter.pw((n // 100) % 10, " hundred")
        converter.pw(n % 100, " ")
''',
    "c": r'''
#include <stdio.h>

void pw(int number, const char *label) {
    if (number > 0) {
        printf("%d%s", number, label);
    }
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
        pw(n % 100, " ");
    }
    return 0;
}
''',
    "csharp": r'''
using System;

public class NumberToWord
{
    public void Pw(int number, string label)
    {
        if (number > 0)
        {
            Console.Write(number + label);
        }
    }
}

public static class Program
{
    public static void Main()
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
            a.Pw(n % 100, " ");
        }
    }
}
''',
}
TRANSLATIONS["T102"] = {
    "python": r'''
def is_anagram(s1, s2):
    i = 0
    while i < len(s2):
        if s2[i] not in s1:
            return False
        s1 = s1.replace(s2[i], "", 1)
        s2 = s2.replace(s2[i], "", 1)
        i += 1
    return True
''',
    "c": r'''
#include <stdbool.h>
#include <string.h>

static void remove_first(char *s, char c) {
    char *p = strchr(s, c);
    if (p != NULL) {
        memmove(p, p + 1, strlen(p + 1) + 1);
    }
}

bool is_anagram(char *s1, const char *s2_in) {
    char s2[256];
    strcpy(s2, s2_in);
    if (strlen(s1) != strlen(s2)) {
        return false;
    }
    int i = 0;
    while (i < (int)strlen(s2)) {
        if (strchr(s1, s2[i]) == NULL) {
            return false;
        }
        remove_first(s1, s2[i]);
        remove_first(s2, s2[i]);
        i++;
    }
    return true;
}
''',
    "csharp": r'''
using System;

public static class AnagramCheck
{
    private static string RemoveFirst(string s, char c)
    {
        int idx = s.IndexOf(c);
        if (idx < 0)
        {
            return s;
        }
        return s.Remove(idx, 1);
    }

    public static bool IsAnagram(string s1, string s2)
    {
        if (s1.Length != s2.Length)
        {
            return false;
        }
        int i = 0;
        while (i < s2.Length)
        {
            if (!s1.Contains(s2[i].ToString()))
            {
                return false;
            }
            s1 = RemoveFirst(s1, s2[i]);
            s2 = RemoveFirst(s2, s2[i]);
            i++;
        }
        return true;
    }
}
''',
}
TRANSLATIONS["T245"] = {
    "python": r'''
def main():
    print("Enter the String", end="")
    st = input()
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
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    printf("Enter the String");
    if (fgets(st, sizeof st, stdin) == NULL) {
        return 0;
    }
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    size_t len = strlen(st);
    for (size_t i = 0; i < len; i++) {
        ar[(unsigned char)st[i]]++;
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
''',
    "csharp": r'''
using System;

public static class Program
{
    public static void Main()
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        foreach (char ch in st)
        {
            ar[ch]++;
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
''',
}
TRANSLATIONS["T586"] = {
    "python": r'''
def main():
    s = "harikrishna"
    s2 = ""
    for ch in s:
        found = False
        for existing in s2:
            if ch == existing:
                found = True
                break
        if not found:
            s2 = s2 + ch
    print(s2)
''',
    "c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "harikrishna";
    char s2[64] = "";
    size_t len = strlen(s);
    for (size_t i = 0; i < len; i++) {
        int found = 0;
        for (size_t j = 0; j < strlen(s2); j++) {
            if (s[i] == s2[j]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            size_t n = strlen(s2);
            s2[n] = s[i];
            s2[n + 1] = '\0';
        }
    }
    printf("%s\n", s2);
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    public static void Main()
    {
        string s = "harikrishna";
        string s2 = "";
        foreach (char ch in s)
        {
            bool found = false;
            foreach (char existing in s2)
            {
                if (ch == existing)
                {
                    found = true;
                    break;
                }
            }
            if (found == false)
            {
                s2 = s2 + ch.ToString();
            }
        }
        Console.WriteLine(s2);
    }
}
''',
}
TRANSLATIONS["T668"] = {
    "python": r'''
def process_try(scanner):
    return float(scanner())

def main():
    line = input()
    trys = int(line.strip())
    for _ in range(trys):
        probability = process_try(input)
        print(probability)
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>

double process_try(void) {
    double p;
    if (scanf("%lf", &p) != 1) {
        return 0.0;
    }
    return p;
}

int main(void) {
    char line[256];
    if (fgets(line, sizeof line, stdin) == NULL) {
        return 0;
    }
    int trys = atoi(line);
    for (int i = 0; i < trys; i++) {
        double probability = process_try();
        printf("%f\n", probability);
    }
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    private static double ProcessTry()
    {
        return double.Parse(Console.ReadLine());
    }

    public static void Main()
    {
        string line = Console.ReadLine();
        int trys = int.Parse(line.Trim());
        for (int i = 0; i < trys; i++)
        {
            double probability = ProcessTry();
            Console.WriteLine(probability);
        }
    }
}
''',
}
TRANSLATIONS["T634"] = {
    "python": r'''
import itertools

def show(lo):
    print(lo)

def main():
    lc = ['A', 'B', 'C', 'D']
    lC = ['a', 'b', 'c']
    li = [1, 2, 3, 4]
    llo = [lc, lC, li]
    for lo in itertools.product(*llo):
        show(list(lo))
''',
    "c": r'''
#include <stdio.h>

int main(void) {
    int sizes[3] = {4, 3, 4};
    int indices[3] = {0, 0, 0};
    int total = 1;
    for (int i = 0; i < 3; i++) {
        total *= sizes[i];
    }
    for (int n = 0; n < total; n++) {
        printf("[");
        for (int i = 0; i < 3; i++) {
            printf("%d", indices[i]);
            if (i < 2) {
                printf(", ");
            }
        }
        printf("]\n");
        for (int i = 2; i >= 0; i--) {
            indices[i]++;
            if (indices[i] < sizes[i]) {
                break;
            }
            indices[i] = 0;
        }
    }
    return 0;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;

public static class Program
{
    private static IEnumerable<string> CartesianProduct(List<List<object>> lists)
    {
        var counters = new int[lists.Count];
        int total = 1;
        foreach (var l in lists)
        {
            total *= l.Count;
        }
        for (int n = 0; n < total; n++)
        {
            var current = new List<object>();
            for (int i = 0; i < lists.Count; i++)
            {
                current.Add(lists[i][counters[i]]);
            }
            yield return string.Join(", ", current);
            for (int i = lists.Count - 1; i >= 0; i--)
            {
                counters[i]++;
                if (counters[i] < lists[i].Count)
                {
                    break;
                }
                counters[i] = 0;
            }
        }
    }

    public static void Main()
    {
        var llo = new List<List<object>>
        {
            new List<object> { 'A', 'B', 'C', 'D' },
            new List<object> { 'a', 'b', 'c' },
            new List<object> { 1, 2, 3, 4 }
        };
        foreach (string lo in CartesianProduct(llo))
        {
            Console.WriteLine("[" + lo + "]");
        }
    }
}
''',
}
TRANSLATIONS["T654"] = {
    "python": r'''
def filter(source, start, end, dest, dstart, dend, decimal_digits):
    dot_pos = -1
    for i, c in enumerate(dest):
        if c == '.' or c == ',':
            dot_pos = i
            break
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if len(dest) - dot_pos > decimal_digits:
            return ""
    return None
''',
    "c": r'''
#include <string.h>

int filter(const char *source, const char *dest, int dend, int decimal_digits, char **result) {
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
            *result = "";
            return 1;
        }
        if (dend <= dot_pos) {
            *result = NULL;
            return 0;
        }
        if (len - dot_pos > decimal_digits) {
            *result = "";
            return 1;
        }
    }
    *result = NULL;
    return 0;
}
''',
    "csharp": r'''
public class DecimalFilter
{
    public int DecimalDigits;

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
            if (source == "." || source == ",")
            {
                return "";
            }
            if (dend <= dotPos)
            {
                return null;
            }
            if (len - dotPos > DecimalDigits)
            {
                return "";
            }
        }
        return null;
    }
}
''',
}
TRANSLATIONS["T682"] = {
    "python": r'''
def filter(source, start, end, dest, dstart, dend, decimal_digits):
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
    return None
''',
    "c": r'''
#include <string.h>

int filter(const char *source, const char *dest, int dend, int decimal_digits, char **result) {
    size_t len = strlen(dest);
    const char *dot = strpbrk(dest, ".,");
    int dot_pos = (dot == NULL) ? -1 : (int)(dot - dest);
    if (dot_pos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) {
            *result = "";
            return 1;
        }
        if (dend <= dot_pos) {
            *result = NULL;
            return 0;
        }
        if ((int)len - dot_pos > decimal_digits) {
            *result = "";
            return 1;
        }
    }
    *result = NULL;
    return 0;
}
''',
    "csharp": r'''
public class MoneyFilter
{
    public int DecimalDigits { get; set; }

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        int dotPos = -1;
        int len = dest.Length;
        for (int i = 0; i < len; i++)
        {
            if (dest[i] == '.' || dest[i] == ',')
            {
                dotPos = i;
                break;
            }
        }
        if (dotPos >= 0)
        {
            if (source == "." || source == ",")
            {
                return "";
            }
            if (dend <= dotPos)
            {
                return null;
            }
            if (len - dotPos > DecimalDigits)
            {
                return "";
            }
        }
        return null;
    }
}
''',
}
TRANSLATIONS["T596"] = {
    "python": r'''
def match(match_id, body, request, response):
    try:
        p = service.get_product(request.get_product_id())
    except Exception:
        return (None, 400)
    return (p, 200)
''',
    "c": r'''
#include <stddef.h>

typedef struct {
    int id;
} Product;

typedef struct {
    int product_id;
} ServiceRequest;

typedef struct {
    void *body;
    int status;
} ResponseEntity;

extern Product *service_get_product(int id);

ResponseEntity match(const char *match_id, const char *body, const ServiceRequest *request) {
    Product *p = service_get_product(request->product_id);
    ResponseEntity response;
    if (p == NULL) {
        response.body = NULL;
        response.status = 400;
        return response;
    }
    response.body = p;
    response.status = 200;
    return response;
}
''',
    "csharp": r'''
using System;
using System.Net;
using System.Net.Http;

public class MatchController
{
    public HttpRequestMessage Request { get; set; }
    public ProductService Service { get; set; }

    public HttpResponseMessage Match(string matchId, string body, ProductRequest request)
    {
        Product p;
        try
        {
            p = Service.GetProduct(request.ProductId);
        }
        catch (Exception)
        {
            return Request.CreateResponse(HttpStatusCode.BadRequest);
        }
        return Request.CreateResponse(HttpStatusCode.OK, p);
    }
}

public class Product
{
    public int Id { get; set; }
}

public class ProductRequest
{
    public int ProductId { get; set; }
}

public class ProductService
{
    public Product GetProduct(int id)
    {
        return new Product { Id = id };
    }
}
''',
}
TRANSLATIONS["T407"] = {
    "python": r'''
def main():
    x_sum = 0
    y_sum = 0
    with open("D:/Test.txt") as br:
        for raw in br:
            line = raw.rstrip("\n")
            if "x=" in line:
                x_sum += int(line.split("=")[1].strip())
            if "y=" in line:
                y_sum += int(line.split("=")[1].strip())
    print("Sum x is: " + str(x_sum) + " Sum y is: " + str(y_sum))
''',
    "c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *file = fopen("D:\Test.txt", "r");
    if (file == NULL) {
        return 1;
    }
    char line[1024];
    int x_sum = 0;
    int y_sum = 0;
    while (fgets(line, sizeof line, file) != NULL) {
        line[strcspn(line, "\n")] = '\0';
        char *eq;
        if ((eq = strstr(line, "x=")) != NULL) {
            x_sum += atoi(eq + 2);
        }
        if ((eq = strstr(line, "y=")) != NULL) {
            y_sum += atoi(eq + 2);
        }
    }
    fclose(file);
    printf("Sum x is: %d Sum y is: %d\n", x_sum, y_sum);
    return 0;
}
''',
    "csharp": r'''
using System;
using System.IO;

public static class Program
{
    public static void Main()
    {
        int xSum = 0;
        int ySum = 0;
        using (var file = new StreamReader("D:\Test.txt"))
        {
            string line;
            while ((line = file.ReadLine()) != null)
            {
                if (line.Contains("x="))
                {
                    xSum += int.Parse(line.Split('=')[1].Trim());
                }
                if (line.Contains("y="))
                {
                    ySum += int.Parse(line.Split('=')[1].Trim());
                }
            }
        }
        Console.WriteLine("Sum x is: " + xSum + " Sum y is: " + ySum);
    }
}
''',
}
TRANSLATIONS["T477"] = {
    "python": r'''
import math
import random

def get_random_number_between(number_one, number_two):
    if number_one == number_two:
        raise ValueError("Both the numbers can not be equal")
    rand = random.random()
    high_range = max(number_one, number_two)
    low_range = min(number_one, number_two)
    low_rand = math.floor(rand - 1)
    high_rand = math.ceil(rand + 1)
    gen_rand = (high_range - low_range) * ((rand - low_rand) / (high_rand - low_rand)) + low_range
    return gen_rand
''',
    "c": r'''
#include <math.h>
#include <stdlib.h>
#include <time.h>

int getRandomNumberBetween(float numberOne, float numberTwo, float *out) {
    if (numberOne == numberTwo) {
        return -1;
    }
    float rand = (float)rand() / (float)RAND_MAX;
    float highRange = numberOne > numberTwo ? numberOne : numberTwo;
    float lowRange = numberOne < numberTwo ? numberOne : numberTwo;
    float lowRand = (float)floor(rand - 1);
    float highRand = (float)ceil(rand + 1);
    *out = (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
    return 0;
}
''',
    "csharp": r'''
using System;

public static class RandomRange
{
    private static readonly Random Rng = new Random();

    public static float GetRandomNumberBetween(float numberOne, float numberTwo)
    {
        if (numberOne == numberTwo)
        {
            throw new Exception("Both the numbers can not be equal");
        }
        float rand = (float)Rng.NextDouble();
        float highRange = Math.Max(numberOne, numberTwo);
        float lowRange = Math.Min(numberOne, numberTwo);
        float lowRand = (float)Math.Floor(rand - 1);
        float highRand = (float)Math.Ceiling(rand + 1);
        float genRand = (highRange - lowRange) * ((rand - lowRand) / (highRand - lowRand)) + lowRange;
        return genRand;
    }
}
''',
}
TRANSLATIONS["T842"] = {
    "python": r'''
def main():
    exit_command = "quit"
    print("Enter some text, or '" + exit_command + "' to quit")
    while True:
        print("><![CDATA[ ", end="")
        text = input()
        print(text)
        if len(text) == len(exit_command) and text.lower() == exit_command:
            print("Exiting.")
            return
        print("...response goes here...")
''',
    "c": r'''
#include <stdio.h>
#include <string.h>
#include <strings.h>

#define EXIT_COMMAND "quit"

int main(void) {
    char input[1024];
    printf("Enter some text, or '%s' to quit\n", EXIT_COMMAND);
    while (1) {
        printf("><![CDATA[ ");
        if (fgets(input, sizeof input, stdin) == NULL) {
            input[0] = '\0';
        }
        input[strcspn(input, "\n")] = '\0';
        printf("%s\n", input);
        if ((int)strlen(input) == (int)strlen(EXIT_COMMAND) &&
            strcasecmp(input, EXIT_COMMAND) == 0) {
            printf("Exiting.\n");
            return 0;
        }
        printf("...response goes here...\n");
    }
    return 0;
}
''',
    "csharp": r'''
using System;

public static class Program
{
    private const string ExitCommand = "quit";

    public static void Main()
    {
        Console.WriteLine("Enter some text, or '" + ExitCommand + "' to quit");
        while (true)
        {
            Console.Write("><![CDATA[ ");
            string input = Console.ReadLine();
            Console.WriteLine(input);
            if (input.Length == ExitCommand.Length && input.ToLower().Equals(ExitCommand))
            {
                Console.WriteLine("Exiting.");
                return;
            }
            Console.WriteLine("...response goes here...");
        }
    }
}
''',
}
TRANSLATIONS["T181"] = {
    "python": r'''
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

class LinkedList:
    def __init__(self):
        self.first = None
        self.count = 0

    def size(self):
        return self.count

    def second_max_key(self):
        if self.size() < 2:
            return None
        maximum = None
        max_2 = None
        second = self.first.next
        if self.first.key > second.key:
            maximum = self.first
            max_2 = second
        else:
            maximum = second
            max_2 = self.first
        x = second.next
        while x is not None:
            if x.key > maximum.key:
                max_2 = maximum
                maximum = x
            elif x.key > max_2.key and x.key < maximum.key:
                max_2 = x
            x = x.next
        return max_2.key
''',
    "c": r'''
#include <stddef.h>

typedef struct Node {
    int key;
    struct Node *next;
} Node;

int second_max_key(const Node *first, int size, int *found) {
    *found = 0;
    if (size < 2) {
        return 0;
    }
    const Node *max = NULL;
    const Node *max_2 = NULL;
    const Node *second = first->next;
    if (first->key > second->key) {
        max = first;
        max_2 = second;
    } else {
        max = second;
        max_2 = first;
    }
    for (const Node *x = second->next; x != NULL; x = x->next) {
        if (x->key > max->key) {
            max_2 = max;
            max = x;
        } else if (x->key > max_2->key && x->key < max->key) {
            max_2 = x;
        }
    }
    *found = 1;
    return max_2->key;
}
''',
    "csharp": r'''
using System;

public class Node
{
    public IComparable Key;
    public Node Next;
}

public class LinkedList
{
    private Node first;
    private int count;

    public int Size()
    {
        return count;
    }

    public IComparable SecondMaxKey()
    {
        if (Size() < 2)
        {
            return null;
        }
        Node max = null;
        Node max2 = null;
        Node second = first.Next;
        if (first.Key.CompareTo(second.Key) > 0)
        {
            max = first;
            max2 = second;
        }
        else
        {
            max = second;
            max2 = first;
        }
        for (Node x = second.Next; x != null; x = x.Next)
        {
            if (x.Key.CompareTo(max.Key) > 0)
            {
                max2 = max;
                max = x;
            }
            else if (x.Key.CompareTo(max2.Key) > 0 && x.Key.CompareTo(max.Key) < 0)
            {
                max2 = x;
            }
        }
        return max2.Key;
    }
}
''',
}
TRANSLATIONS["T216"] = {
    "python": r'''
def print_all(*to_print):
    for item in to_print:
        if isinstance(item, list) and all(isinstance(v, int) for v in item):
            print(item)
        elif isinstance(item, list) and all(isinstance(v, float) for v in item):
            print(item)
        elif isinstance(item, (list, tuple)):
            print(list(item))
        else:
            print(item)
''',
    "c": r'''
#include <stdarg.h>
#include <stdio.h>

void print_int_array(const int *a, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d%s", a[i], i < n - 1 ? ", " : "");
    }
    printf("]\n");
}

void print_varargs(int count, ...) {
    va_list args;
    va_start(args, count);
    for (int i = 0; i < count; i++) {
        int *values = va_arg(args, int *);
        int n = va_arg(args, int);
        print_int_array(values, n);
    }
    va_end(args);
}
''',
    "csharp": r'''
using System;

public static class Printer
{
    public static void Print(params object[] toPrint)
    {
        foreach (object item in toPrint)
        {
            if (item is int[])
            {
                Console.WriteLine("[" + string.Join(", ", (int[])item) + "]");
            }
            else if (item is double[])
            {
                Console.WriteLine("[" + string.Join(", ", (double[])item) + "]");
            }
            else if (item is object[])
            {
                Console.WriteLine("[" + string.Join(", ", (object[])item) + "]");
            }
            else
            {
                Console.WriteLine(item);
            }
        }
    }
}
''',
}
TRANSLATIONS["T883"] = {
    "python": r'''
class Cell:
    def __init__(self, column_index=0, cell_type=0):
        self.column_index = column_index
        self.cell_type = cell_type
        self.value = None

class Row:
    def __init__(self, height=0, cells=None, last_cell_num=0):
        self.height = height
        self.cells = cells if cells is not None else {}
        self.last_cell_num = last_cell_num
        self.last_column = 0

    def __iter__(self):
        return iter(self.cells.values())

    def create_cell(self, column_index, cell_type):
        cell = Cell(column_index, cell_type)
        self.cells[column_index] = cell
        return cell

def transform_cell(cell_old, cell_new):
    cell_new.value = cell_old.value

def transform(row_old, row_new):
    row_new.height = row_old.height
    for cell in row_old:
        cell_new = row_new.create_cell(cell.column_index, cell.cell_type)
        if cell_new is not None:
            transform_cell(cell, cell_new)
    row_new.last_column = max(row_new.last_column, row_old.last_cell_num)
''',
    "c": r'''
#include <stddef.h>

typedef struct Cell {
    int column_index;
    int cell_type;
    struct Cell *next;
} Cell;

typedef struct Row {
    int height;
    int last_cell_num;
    int last_column;
    Cell *cells;
} Row;

extern Cell *create_cell(Row *row, int column_index, int cell_type);
extern void transform_cell(const Cell *cell_old, Cell *cell_new);

void transform_row(const Row *row_old, Row *row_new) {
    row_new->height = row_old->height;
    for (const Cell *cell = row_old->cells; cell != NULL; cell = cell->next) {
        Cell *cell_new = create_cell((Row *)row_new, cell->column_index, cell->cell_type);
        if (cell_new != NULL) {
            transform_cell(cell, cell_new);
        }
    }
    if (row_old->last_cell_num > row_new->last_column) {
        row_new->last_column = row_old->last_cell_num;
    }
}
''',
    "csharp": r'''
using System;
using System.Collections;
using System.Collections.Generic;

public class Cell
{
    public int ColumnIndex { get; set; }
    public int CellType { get; set; }
}

public class Row : IEnumerable<Cell>
{
    private readonly Dictionary<int, Cell> cells = new Dictionary<int, Cell>();

    public int Height { get; set; }
    public int LastCellNum { get; set; }
    public int LastColumn { get; set; }

    public Cell CreateCell(int columnIndex, int cellType)
    {
        var cell = new Cell { ColumnIndex = columnIndex, CellType = cellType };
        cells[columnIndex] = cell;
        return cell;
    }

    public IEnumerator<Cell> GetEnumerator()
    {
        return cells.Values.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
}

public class WorkbookTransformer
{
    private void Transform(Row rowOld, Row rowNew)
    {
        rowNew.Height = rowOld.Height;
        foreach (Cell cell in rowOld)
        {
            Cell cellNew = rowNew.CreateCell(cell.ColumnIndex, cell.CellType);
            if (cellNew != null)
            {
                TransformCell(cell, cellNew);
            }
        }
        rowNew.LastColumn = Math.Max(rowNew.LastColumn, rowOld.LastCellNum);
    }

    private static void TransformCell(Cell cellOld, Cell cellNew)
    {
        cellNew.CellType = cellOld.CellType;
    }
}
''',
}
TRANSLATIONS["T462"] = {
    "python": r'''
import random

class MyRectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class Canvas:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.lst_shapes = []

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def repaint(self):
        pass

    def action_performed(self, event):
        x = int(random.random() * self.get_width())
        y = int(random.random() * self.get_height())
        width = int(random.random() * (self.get_width() / 4))
        height = int(random.random() * (self.get_height() / 4))
        if x + width > self.get_width():
            x = self.get_width() - width
        if y + height > self.get_height():
            y = self.get_height() - height
        color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        self.lst_shapes.append(MyRectangle(x, y, width, height, color))
        self.repaint()
''',
    "c": r'''
#include <stdlib.h>

typedef struct {
    int x, y, width, height;
    int r, g, b;
} MyRectangle;

static MyRectangle lst_shapes[100];
static int shape_count = 0;
static int panel_width = 800;
static int panel_height = 600;

void action_performed(void) {
    int x = rand() % panel_width;
    int y = rand() % panel_height;
    int width = rand() % (panel_width / 4);
    int height = rand() % (panel_height / 4);
    if (x + width > panel_width) {
        x = panel_width - width;
    }
    if (y + height > panel_height) {
        y = panel_height - height;
    }
    MyRectangle rect;
    rect.x = x;
    rect.y = y;
    rect.width = width;
    rect.height = height;
    rect.r = rand() % 255;
    rect.g = rand() % 255;
    rect.b = rand() % 255;
    lst_shapes[shape_count] = rect;
    shape_count++;
}
''',
    "csharp": r'''
using System;
using System.Collections.Generic;
using System.Drawing;

public class MyRectangle
{
    public int X { get; set; }
    public int Y { get; set; }
    public int Width { get; set; }
    public int Height { get; set; }
    public Color Fill { get; set; }
}

public class DrawingPanel
{
    private static readonly Random Generator = new Random();
    public List<MyRectangle> LstShapes { get; } = new List<MyRectangle>();

    public int GetWidth()
    {
        return 800;
    }

    public int GetHeight()
    {
        return 600;
    }

    public void Repaint()
    {
    }

    public void ActionPerformed(EventArgs e)
    {
        int x = (int)(Generator.NextDouble() * GetWidth());
        int y = (int)(Generator.NextDouble() * GetHeight());
        int width = (int)(Generator.NextDouble() * (GetWidth() / 4));
        int height = (int)(Generator.NextDouble() * (GetHeight() / 4));
        if (x + width > GetWidth())
        {
            x = GetWidth() - width;
        }
        if (y + height > GetHeight())
        {
            y = GetHeight() - height;
        }
        Color color = Color.FromArgb((int)(Generator.NextDouble() * 255),
            (int)(Generator.NextDouble() * 255), (int)(Generator.NextDouble() * 255));
        LstShapes.Add(new MyRectangle { X = x, Y = y, Width = width, Height = height, Fill = color });
        Repaint();
    }
}
''',
}

REFACTORS = {}
REFACTORS["R106ccba12f"] = r'''
public static IList ToAnonymousList (this IEnumerable enumerable) {
    var enumerator = enumerable.GetEnumerator ();
    if (! enumerator.MoveNext ())
        throw new Exception ("?? No elements??");
    var elementType = enumerator.Current.GetType ();
    var returnList = (IList) Activator.CreateInstance (typeof (List <>).MakeGenericType (elementType));
    do {
        returnList.Add (enumerator.Current);
    } while (enumerator.MoveNext ());
    return returnList;
}
'''
REFACTORS["R3968bf5162"] = r'''
public void run () {
    int i = 1;
    while (i < 50) {
        awaitState (3);
        synchronized (s) {
            if (s.getState () == 3) System.out.println ("t1 " + i);
            s.setState (1);
            i = i + 3;
            s.notifyAll ();
        }
    }
}

private void awaitState (int target) {
    while (s.getState () != target) {
        synchronized (s) {
            try {
                s.wait ();
            } catch (InterruptedException e) {
                e.printStackTrace ();
            }
        }
    }
}
'''
REFACTORS["R3d67d34140"] = r'''
public static void main (String [] args) {
    Scanner sc = new Scanner (System.in);
    List < String [] > rows = new ArrayList < > ();
    rows.add (new String [] {"continents", "Asia", "Europe", "Africa", "Australia", "South America", "North America"});
    rows.add (new String [] {"profession", "teacher", "doctor", "lawyer"});
    rows.add (new String [] {"brand", "apple", "samsung"});
    rows.add (new String [] {"name", "lisa", "peter", "sam", "jack"});
    rows.add (new String [] {"profession", "engineer", "Professor", "Dentist", "Driver"});
    rows.add (new String [] {"sex", "value", "male", "female"});
    rows.add (new String [] {"exp", "value", "1", "2", "3", "4"});
    int index = sc.nextInt ();
    String [] moved = rows.remove (index - 1);
    rows.add (moved);
    for (String [] tempArray : rows) {
        System.out.println (String.join (" ", tempArray));
    }
}
'''
REFACTORS["Rd41c27729f"] = r'''
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % k for k in range(3, int(n ** 0.5) + 1, 2))
'''
REFACTORS["Refa2e73039"] = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (void) {
    char line [128];
    int sum = 0;
    printf ("enter numbers: ");
    scanf ("%127[^\n]", line);
    char *token = strtok (line, " \t");
    while (token != NULL) {
        sum += atoi (token);
        token = strtok (NULL, " \t");
    }
    printf ("sum: %d\n", sum);
    return 0;
}
'''
REFACTORS["R0113c1db9b"] = r'''
def foo(thing=None, thing_seq=None):
    if thing_seq is not None:
        list(map(lambda _thing: foo(thing=_thing), thing_seq))
    if thing is not None:
        print("did foo with", thing)
'''
REFACTORS["Rc5f95dbda1"] = r'''
private static void GetUserData (string userName, UserSession user) {
    using (Entities ctx = CommonSERT.GetContext ()) {
        var result = ctx.datUserRoles
            .Where (ur => ur.AccountName.Equals (userName, StringComparison.CurrentCultureIgnoreCase))
            .Select (ur => new {ur.active, ur.ID})
            .FirstOrDefault ();
        if (result != null)
            user.UserActive = result.active;
        user.UserID = result.ID;
    }
}
'''
REFACTORS["Rf9eb0ff068"] = r'''
from itertools import combinations

def function(argument):
    max_arg = max(argument)
    argument.remove(max_arg)
    found = any(sum(combo) == max_arg
                for length in range(1, len(argument) + 1)
                for combo in combinations(argument, length))
    return "true" if found else "false"
'''
REFACTORS["R1479812111"] = r'''
public void doWork () {
    int h = 0;
    while (true)
    {
        if (h > 0)
            break;
        Thread.Sleep (3000);
        h.Dump ();
        h ++;
    }
}
'''
REFACTORS["R314ba9cd4a"] = r'''
#include <stdio.h>

static void printDigits (const int *word, int i) {
    if (i < 0)
        return;
    if (word [i] <= 9)
        printf ("%d", word [i]);
    else
        printf ("%c", (65 - 10 + word [i]));
    printDigits (word, i - 1);
}

int main (void) {
    int i, base;
    int word [32];
    unsigned long int number;
    printf ("Enter the decimal number to be converted: ");
    scanf ("%ld", & number);
    printf ("\nEnter the new base: ");
    scanf ("%d", & base);
    i = wordCalculator (word, number, base);
    printf ("The number is: ");
    printDigits (word, i);
    printf ("\n");
    return 0;
}
'''
REFACTORS["R7ca8e2a2eb"] = r'''
static boolean isImmutable (Object obj) {
    Class < ? > objClass = obj.getClass ();
    Class < ? > superClass = objClass.getSuperclass ();
    if (Immutable.class.equals (superClass) && Modifier.isFinal (objClass.getModifiers ())) {
        for (Field field : objClass.getDeclaredFields ()) {
            if (! Modifier.isFinal (field.getModifiers ()) || ! isValidFieldType (field.getType ())) {
                return false;
            }
        }
        return true;
    }
    return false;
}
'''
REFACTORS["R8db01bf25f"] = r'''
def flatten(xs):
    res = []
    stack = list(reversed(xs))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            res.append(item)
    return res
'''
REFACTORS["Re6ed6fb8d3"] = r'''
public static IEnumerable < T > TakeLast < T > (this IEnumerable < T > input, int count) {
    if (count <= 0)
        yield break;
    var inputList = input as IList < T >;
    if (inputList != null) {
        int start = Math.Max (0, inputList.Count - count);
        for (int index = start; index < inputList.Count; index ++) {
            yield return inputList [index];
        }
        yield break;
    }
    var recent = new Queue < T > ();
    foreach (T item in input) {
        if (recent.Count == count)
            recent.Dequeue ();
        recent.Enqueue (item);
    }
    while (recent.Count > 0) {
        yield return recent.Dequeue ();
    }
}
'''
REFACTORS["Rc93ef31bfe"] = r'''
def matched(s):
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')' and depth == 0:
            return False
        elif ch == ')':
            depth -= 1
    return depth == 0
'''
REFACTORS["R077660cd40"] = r'''
#include <stdio.h>
#include <stdbool.h>

int main (void) {
    int ch;
    int numWords = 0;
    int numLetters = 0;
    bool inWord = false;
    printf ("Enter a sentence: ");
    while ((ch = getchar ()) != EOF && ch != '\n') {
        if (ch == ' ') {
            inWord = false;
        } else {
            if (! inWord)
                numWords ++;
            inWord = true;
            numLetters ++;
        }
    }
    if (numWords == 0) {
        printf ("You didn't enter any words\n");
        return 0;
    }
    printf ("Average word length: %.1f (C = %d, N = %d)\n",
            numLetters / (float) (numWords), numLetters, numWords);
    return 0;
}
'''
REFACTORS["R076547cbe5"] = r'''
public static bool IsWindowOnAnyScreen (Window Window, short WindowSizeX, short WindowSizeY, bool AutoAdjustWindow) {
    var screen = System.Windows.Forms.Screen.FromHandle (new WindowInteropHelper (Window).Handle);
    var area = screen.WorkingArea;
    if (Window.Left >= area.Left && Window.Top >= area.Top &&
        Window.Top + WindowSizeY <= area.Bottom && Window.Left + WindowSizeX <= area.Right)
        return true;
    if (AutoAdjustWindow) {
        if (Window.Left < area.Left)
            Window.Left = area.Left;
        if (Window.Top < area.Top)
            Window.Top = area.Top;
        if (Window.Top + WindowSizeY > area.Bottom)
            Window.Top = area.Bottom - WindowSizeY;
        if (Window.Left + WindowSizeX > area.Right)
            Window.Left = area.Right - WindowSizeX;
    }
    return false;
}
'''
REFACTORS["Rb740b5ce4e"] = r'''
#include <stdio.h>

typedef int *P1;
typedef P1 *P2;
typedef P2 *P3;
typedef P3 *P4;
typedef P4 *P5;
typedef P5 *P6;
typedef P6 *P7;
typedef P7 *P8;
typedef P8 *P9;

void mega_pointer (P9 p);

int main () {
    int blah = 1;
    P1 p1 = & blah;
    P2 p2 = & p1;
    P3 p3 = & p2;
    P4 p4 = & p3;
    P5 p5 = & p4;
    P6 p6 = & p5;
    P7 p7 = & p6;
    P8 p8 = & p7;
    P9 p9 = & p8;
    mega_pointer (p9);
    return 0;
}
'''
REFACTORS["R2d627295b4"] = r'''
from sklearn.linear_model import LinearRegression
import numpy as np

class MyLinearRegression(LinearRegression):
    def fit(self, X, y, n_jobs=1):
        super().fit(X, y, n_jobs)
        residual = (self.predict(X) - y) ** 2
        dof = X.shape[0] - X.shape[1]
        ssr = np.sum(residual, axis=0) / float(dof)
        xtx_inv = np.linalg.inv(np.dot(X.T, X))
        serr = np.sqrt([np.diagonal(ssr[i] * xtx_inv) for i in range(ssr.shape[0])])
        self.t = self.coef_ / serr
'''
REFACTORS["R27ef16612d"] = r'''
#include <stdio.h>

int main () {
    int a [50] = {1, 2, -3, 0, 0, 6, 7, -8, 0, SENTINEL};
    int count = 0;
    int i = 0;
    while (i < 50 && a [i] != SENTINEL) {
        count += (a [i] != 0);
        i ++;
    }
    printf ("Total Element :%d ", count);
    return 0;
}
'''
REFACTORS["R80bf6ba91c"] = r'''
public static void main (final String [] args) throws IOException {
    BufferedReader br = new BufferedReader (new InputStreamReader (System.in));
    System.out.println ("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    String input;
    while (! isExitCommand (input = br.readLine ())) {
        System.out.println ("...response goes here...");
    }
    System.out.println ("Exiting.");
}

private static boolean isExitCommand (String input) {
    System.out.print ("><![CDATA[ ");
    System.out.println (input);
    return input.length () == EXIT_COMMAND.length () && input.toLowerCase ().equals (EXIT_COMMAND);
}
'''
REFACTORS["R5813b54ca5"] = r'''
#include <math.h>
#include <stdio.h>

int main () {
    double integralSum = 0;
    int i = 1;
    while (i < parts + 1) {
        integralSum += step * fabs (pow ((x + (step * i)), 2) + 4);
        i ++;
    }
    printf ("%f\n", integralSum);
    return 0;
}
'''
REFACTORS["R14e363aee6"] = r'''
public static void Main () {
    string baseIP = "192.168.1.";
    Console.WriteLine ("Pinging 255 destinations of D-class in {0}*", baseIP);
    CreatePingers (255);
    PingOptions po = new PingOptions (ttl, true);
    byte [] data = new System.Text.ASCIIEncoding ().GetBytes ("abababababababababababababababab");
    int cnt = 1;
    Stopwatch watch = Stopwatch.StartNew ();
    pingers.Cast < Ping > ().ToList ().ForEach (p => {
        lock (@lock)
        {
            instances += 1;
        } p.SendAsync (string.Concat (baseIP, cnt.ToString ()), timeOut, data, po);
        cnt += 1;
    });
    while (instances > 0) {
        new SpinWait ().SpinOnce ();
    }
    watch.Stop ();
    DestroyPingers ();
    Console.WriteLine ("Finished in {0}. Found {1} active IP-addresses.", watch.Elapsed.ToString (), result);
    Console.ReadKey ();
}
'''
REFACTORS["R9582f81645"] = r'''
def __init__(self, a=None, b=None, **kwargs):
    self.relations = build_relations()
    self.a = a
    self.b = b
    self.e = None
    self.C = None
    self.A = None
    for key, value in kwargs.items():
        setattr(self, key, value)

def build_relations():
    return {
    "e" : {"req" : ["a", "b"], "func" : lambda a, b : a + b},
    "C" : {"req" : ["e", "a"], "func" : lambda e, a : e * 1 / (a * b)},
    "A" : {"req" : ["C", "e"], "func" : lambda e, C : cmplx_func_A(e, C)},
    "a" : {"req" : ["e", "b"], "func" : lambda e, b : e / b},
    "b" : {"req" : ["e", "a"], "func" : lambda e, a : e / a}}
'''
REFACTORS["Rcc630548aa"] = r'''
public IDisposable Enter (string key) {
    Locker locker = GetOrCreateLocker (key);
    locker.Enter ();
    locker.WaitCount --;
    return locker;
}

private Locker GetOrCreateLocker (string key) {
    lock (this.globalLock)
    {
        Locker existing;
        if (this.locks.TryGetValue (key, out existing)) {
            existing.WaitCount ++;
            return existing;
        }
        Locker created = new Locker (this, key);
        this.locks [key] = created;
        created.WaitCount ++;
        return created;
    }
}
'''
REFACTORS["R8868947157"] = r'''
#include <stdio.h>
#include <string.h>

static int countRepeats (char last [] [25], int n, const char *first) {
    int count = 0;
    for (int i = 0; i < n; i ++) {
        if (strcmp (last [i], first) == 0)
            count ++;
    }
    return count;
}

int main (void) {
    char first [25];
    int n;
    printf ("Enter the number of last names :\n");
    scanf ("%d", & n);
    printf ("Enter the first name \n");
    scanf ("%s", first);
    char last [n] [25];
    for (int i = 0; i < n; i++)
        scanf ("%s", last [i]);
    int index = countRepeats (last, n, first);
    if (index == 0)
        printf ("First name not repeated\n");
    else
        printf ("First name repeated %d times", index);
    return 0;
}
'''

ids_seen = set()
result = []
seed = json.load(open(SEED, encoding="utf-8"))
for item in seed:
    iid = item["id"]
    if iid in ids_seen:
        raise SystemExit("duplicate id in output: " + iid)
    ids_seen.add(iid)
    if item["task"] == "translate":
        codes = TRANSLATIONS[iid]
        for lang in ("python", "c", "csharp"):
            code = codes[lang]
            if len(code.strip()) < 20:
                raise SystemExit("too short: %s %s" % (iid, lang))
            if lang == "python":
                ast.parse(code)
        result.append({"id": iid, "outputs": {"python": codes["python"], "c": codes["c"], "csharp": codes["csharp"]}})
    else:
        code = REFACTORS[iid]
        if len(code.strip()) < 20:
            raise SystemExit("too short: " + iid)
        if item["lang"] == "python":
            ast.parse(code)
        result.append({"id": iid, "output": code})

missing = [it["id"] for it in seed if it["id"] not in ids_seen]
if missing:
    raise SystemExit("missing ids: %s" % missing)

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=1)
print("OK: wrote %d entries to %s" % (len(result), OUT))
