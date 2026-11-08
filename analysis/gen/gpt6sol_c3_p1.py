DATA_T1 = {
"T471": {
"python": r'''
def get_max(start, arr):
    return max(arr[start:]) if arr else 0

def main():
    large = [0] * 10
    array = [33, 55, 13, 46, 87, 42, 10, 34, 43, 56]
    k = 0
    for value in array:
        large[k] = get_max(0, array)
        k += 1
    print("Largest 5 is: " + str(large[:5]))
''',
"c": r'''
#include <stdio.h>

static int get_max(int start, const int *arr, int len) {
    int m = arr[start];
    for (int i = start + 1; i < len; i++) {
        if (arr[i] > m) m = arr[i];
    }
    return m;
}

int main(void) {
    int large[10];
    int array[10] = {33, 55, 13, 46, 87, 42, 10, 34, 43, 56};
    int k = 0;
    for (int i = 0; i < 10; i++) {
        large[k++] = get_max(0, array, 10);
    }
    printf("Largest 5 is: [");
    for (int i = 0; i < 5; i++) {
        if (i > 0) printf(", ");
        printf("%d", large[i]);
    }
    printf("]\n");
    return 0;
}
''',
"csharp": r'''
using System;
using System.Linq;

public static class TopFive
{
    private static int GetMax(int start, int[] arr)
    {
        int m = arr[start];
        for (int i = start + 1; i < arr.Length; i++)
        {
            if (arr[i] > m) m = arr[i];
        }
        return m;
    }

    public static void Main()
    {
        int[] large = new int[10];
        int[] array = { 33, 55, 13, 46, 87, 42, 10, 34, 43, 56 };
        int k = 0;
        foreach (int value in array)
        {
            large[k] = GetMax(0, array);
            k++;
        }
        Console.WriteLine("Largest 5 is: [" + string.Join(", ", large.Take(5)) + "]");
    }
}
'''
},
"T23": {
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

char *center(const char *s, int size, char pad) {
    if (s == NULL || size <= (int)strlen(s)) {
        char *copy = malloc(strlen(s) + 1);
        if (s != NULL) strcpy(copy, s);
        return copy;
    }
    char *out = malloc(size + 1);
    int left = (size - (int)strlen(s)) / 2;
    int pos = 0;
    for (int i = 0; i < left; i++) out[pos++] = pad;
    for (const char *p = s; *p; p++) out[pos++] = *p;
    while (pos < size) out[pos++] = pad;
    out[pos] = '\0';
    return out;
}
''',
"csharp": r'''
public static string Center(string s, int size, char pad)
{
    if (s == null || size <= s.Length) return s;
    char[] result = new char[size];
    int left = (size - s.Length) / 2;
    int pos = 0;
    for (int i = 0; i < left; i++) result[pos++] = pad;
    foreach (char c in s) result[pos++] = c;
    while (pos < size) result[pos++] = pad;
    return new string(result);
}
'''
},
"T135": {
"python": r'''
def solution(X, A):
    seen = set()
    sum1 = sum(range(X + 1))
    sum2 = 0
    for i in range(len(A)):
        if A[i] in seen:
            continue
        seen.add(A[i])
        sum2 += A[i]
        if sum1 == sum2:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    int sum1 = 0, sum2 = 0;
    for (int v = 0; v <= X; v++) sum1 += v;
    for (int i = 0; i < len; i++) {
        int seen = 0;
        for (int j = 0; j < i; j++) {
            if (A[j] == A[i]) { seen = 1; break; }
        }
        if (seen) continue;
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}
''',
"csharp": r'''
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int X, int[] A)
    {
        var seen = new HashSet<int>();
        int sum1 = 0;
        for (int v = 0; v <= X; v++) sum1 += v;
        int sum2 = 0;
        for (int i = 0; i < A.Length; i++)
        {
            if (seen.Contains(A[i])) continue;
            seen.Add(A[i]);
            sum2 += A[i];
            if (sum1 == sum2) return i;
        }
        return -1;
    }
}
'''
},
"T668": {
"python": r'''
def process_try(read_line):
    return float(read_line())

def main():
    trys = int(input().strip())
    for _ in range(trys):
        probability = process_try(input)
        print(probability)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>

static double process_try(void) {
    double p;
    if (scanf("%lf", &p) != 1) return 0.0;
    return p;
}

int main(void) {
    char line[100];
    if (fgets(line, sizeof(line), stdin) == NULL) return 1;
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

public static class ProbabilityRunner
{
    private static double ProcessTry(Func<string> readLine)
    {
        return double.Parse(readLine().Trim());
    }

    public static void Main()
    {
        int trys = int.Parse(Console.ReadLine().Trim());
        for (int i = 0; i < trys; i++)
        {
            double probability = ProcessTry(Console.ReadLine);
            Console.WriteLine(probability);
        }
    }
}
'''
},
"T159": {
"python": r'''
def solution(X, A):
    check = [0] * X
    cmp_count = 0
    time = -1
    for x in range(len(A)):
        temp = A[x]
        if temp <= X:
            if check[temp - 1] > 0:
                continue
            check[temp - 1] += 1
            cmp_count += 1
        if cmp_count == X:
            time = x
            break
    return time
''',
"c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    int *check = calloc(X, sizeof(int));
    int cmp = 0;
    int time = -1;
    for (int x = 0; x < len; x++) {
        int temp = A[x];
        if (temp <= X) {
            if (check[temp - 1] > 0) continue;
            check[temp - 1]++;
            cmp++;
        }
        if (cmp == X) { time = x; break; }
    }
    free(check);
    return time;
}
''',
"csharp": r'''
public static int Solution(int X, int[] A)
{
    int[] check = new int[X];
    int cmp = 0;
    int time = -1;
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X && check[A[i] - 1] == 0)
        {
            check[A[i] - 1]++;
            cmp++;
        }
        if (cmp == X)
        {
            time = i;
            break;
        }
    }
    return time;
}
'''
},
"T545": {
"python": r'''
def join(items, delimiter):
    parts = []
    for value in items:
        parts.append(value)
        parts.append(delimiter)
    if parts:
        parts.pop()
    return "".join(parts)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

char *join(char **input, int n, const char *delimiter) {
    size_t total = 1;
    for (int i = 0; i < n; i++) {
        total += strlen(input[i]) + strlen(delimiter);
    }
    char *out = malloc(total);
    out[0] = '\0';
    for (int i = 0; i < n; i++) {
        strcat(out, input[i]);
        strcat(out, delimiter);
    }
    size_t len = strlen(out);
    if (len > 0) {
        out[len - strlen(delimiter)] = '\0';
    }
    return out;
}
''',
"csharp": r'''
using System.Text;

public static class Joiner
{
    public static string Join(string[] input, string delimiter)
    {
        var sb = new StringBuilder();
        foreach (string value in input)
        {
            sb.Append(value);
            sb.Append(delimiter);
        }
        if (sb.Length > 0)
        {
            sb.Length -= delimiter.Length;
        }
        return sb.ToString();
    }
}
'''
},
"T721": {
"python": r'''
def num_letters(s):
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    pieces = []
    for i in range(26):
        if count[i] != 0:
            pieces.append(str(count[i]) + chr(i + ord('a')))
    return "".join(pieces)
''',
"c": r'''
#include <stdlib.h>
#include <stdio.h>

char *num_letters(const char *s) {
    int count[26] = {0};
    for (const char *p = s; *p; p++) {
        count[*p - 'a']++;
    }
    char *out = malloc(256);
    int pos = 0;
    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) {
            pos += sprintf(out + pos, "%d%c", count[i], 'a' + i);
        }
    }
    out[pos] = '\0';
    return out;
}
''',
"csharp": r'''
using System.Text;

public static class LetterCounts
{
    public static string NumLetters(string s)
    {
        int[] count = new int[26];
        foreach (char c in s)
        {
            count[c - 'a']++;
        }
        var result = new StringBuilder();
        for (int i = 0; i < 26; i++)
        {
            if (count[i] != 0)
            {
                result.Append(count[i]).Append((char)(i + 'a'));
            }
        }
        return result.ToString();
    }
}
'''
},
"T338": {
"python": r'''
class NumberToWord:
    def pw(self, count, label):
        if count > 0:
            print(str(count) + label, end="")

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
        converter.pw(n % 100, "")
''',
"c": r'''
#include <stdio.h>

static void number_to_word_pw(int count, const char *label) {
    if (count > 0) {
        printf("%d%s", count, label);
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
        number_to_word_pw(n / 1000000000, " Hundred");
        number_to_word_pw((n / 10000000) % 100, " crore");
        number_to_word_pw((n / 100000) % 100, " lakh");
        number_to_word_pw((n / 1000) % 100, " thousand");
        number_to_word_pw((n / 100) % 10, " hundred");
        number_to_word_pw(n % 100, "");
    }
    return 0;
}
''',
"csharp": r'''
using System;

public class NumberToWord
{
    public void Pw(int count, string label)
    {
        if (count > 0)
        {
            Console.Write(count + label);
        }
    }
}

public static class Program
{
    public static void Main()
    {
        Console.Write("Enter an integer number: ");
        int n = int.Parse(Console.ReadLine());
        if (n <= 0)
        {
            Console.Write("Enter numbers greater than 0");
        }
        else
        {
            var converter = new NumberToWord();
            Console.Write("After conversion number in words is :");
            converter.Pw(n / 1000000000, " Hundred");
            converter.Pw((n / 10000000) % 100, " crore");
            converter.Pw((n / 100000) % 100, " lakh");
            converter.Pw((n / 1000) % 100, " thousand");
            converter.Pw((n / 100) % 10, " hundred");
            converter.Pw(n % 100, "");
        }
    }
}
'''
}
}
