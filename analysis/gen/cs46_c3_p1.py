DATA1 = {
"T471": {"outputs": {
"python": r"""import random

def main():
    large = [0] * 10
    array = [33, 55, 13, 46, 87, 42, 10, 34, 43, 56]
    k = 0
    while k < len(array):
        large[k] = get_max(0, array)
        k += 1
    print("Largest 5 is: " + str(large[:5]))

def get_max(start, values):
    best = start
    for value in values:
        if value > best:
            best = value
    return best
""",
"c": r"""#include <stdio.h>

int getMax(int start, const int *array, int n) {
    int best = start;
    for (int i = 0; i < n; i++) {
        if (array[i] > best) best = array[i];
    }
    return best;
}

int main(void) {
    int large[10];
    int array[] = {33, 55, 13, 46, 87, 42, 10, 34, 43, 56};
    int n = sizeof(array) / sizeof(array[0]);
    int k = 0;
    for (int i = 0; i < n; i++) {
        large[k++] = getMax(0, array, n);
    }
    printf("Largest 5 is: ");
    for (int i = 0; i < 5; i++) {
        printf("%d%s", large[i], i < 4 ? ", " : "");
    }
    printf("\n");
    return 0;
}
""",
"csharp": r"""using System;
using System.Linq;

public static class Program
{
    private static int GetMax(int start, int[] array)
    {
        int best = start;
        foreach (int value in array)
        {
            if (value > best) best = value;
        }
        return best;
    }

    public static void Main(string[] args)
    {
        int[] large = new int[10];
        int[] array = { 33, 55, 13, 46, 87, 42, 10, 34, 43, 56 };
        int k = 0;
        for (int i = 0; i < array.Length; i++)
        {
            large[k++] = GetMax(0, array);
        }
        Console.WriteLine("Largest 5 is: " + string.Join(", ", large.Take(5)));
    }
}
""",
}},
"T23": {"outputs": {
"python": r"""def center(s, size, pad):
    if s is None or size <= len(s):
        return s
    result = pad * ((size - len(s)) // 2) + s
    while len(result) < size:
        result += pad
    return result
""",
"c": r"""#include <stdlib.h>
#include <string.h>

char *center(const char *s, int size, char pad) {
    if (s == NULL || size <= (int)strlen(s)) {
        return (char *)s;
    }
    char *sb = malloc(size + 1);
    int pos = 0;
    for (int i = 0; i < (size - (int)strlen(s)) / 2; i++) {
        sb[pos++] = pad;
    }
    for (const char *p = s; *p; p++) {
        sb[pos++] = *p;
    }
    while (pos < size) {
        sb[pos++] = pad;
    }
    sb[pos] = '\0';
    return sb;
}
""",
"csharp": r"""using System.Text;

public static string Center(string s, int size, char pad)
{
    if (s == null || size <= s.Length) return s;
    var sb = new StringBuilder(size);
    for (int i = 0; i < (size - s.Length) / 2; i++) sb.Append(pad);
    sb.Append(s);
    while (sb.Length < size) sb.Append(pad);
    return sb.ToString();
}
""",
}},
"T135": {"outputs": {
"python": r"""def solution(X, A):
    seen = set()
    sum1 = sum(range(X + 1))
    sum2 = 0
    for i, value in enumerate(A):
        if value in seen:
            continue
        seen.add(value)
        sum2 += value
        if sum1 == sum2:
            return i
    return -1
""",
"c": r"""#include <stdlib.h>

int solution(int X, const int *A, int n) {
    char *seen = calloc(X + 2, 1);
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    for (int i = 0; i < n; i++) {
        int v = A[i];
        if (v >= 0 && v <= X) {
            if (seen[v]) continue;
            seen[v] = 1;
        }
        sum2 += v;
        if (sum1 == sum2) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
""",
"csharp": r"""using System.Collections.Generic;

public static int Solution(int X, int[] A)
{
    var seen = new HashSet<int>();
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    for (int i = 0; i < A.Length; i++)
    {
        if (seen.Contains(A[i])) continue;
        seen.Add(A[i]);
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}
""",
}},
"T668": {"outputs": {
"python": r"""def main():
    trys = int(input().strip())
    for _ in range(trys):
        probability = process_try(input)
        print(probability)
""",
"c": r"""#include <stdio.h>
#include <stdlib.h>

double processTry(void);

int main(void) {
    char line[128];
    if (fgets(line, sizeof(line), stdin) == NULL) return 0;
    int trys = atoi(line);
    for (int i = 0; i < trys; i++) {
        double probability = processTry();
        printf("%f\n", probability);
    }
    return 0;
}
""",
"csharp": r"""using System;

public static void Main(string[] args)
{
    string line = Console.ReadLine();
    int trys = int.Parse(line.Trim());
    for (int i = 0; i < trys; i++)
    {
        double probability = ProcessTry();
        Console.WriteLine(probability);
    }
}
""",
}},
"T159": {"outputs": {
"python": r"""def solution(X, A):
    check = [0] * X
    cmp_count = 0
    time = -1
    for x, temp in enumerate(A):
        if temp <= X:
            if check[temp - 1] > 0:
                continue
            check[temp - 1] += 1
            cmp_count += 1
        if cmp_count == X:
            time = x
            break
    return time
""",
"c": r"""#include <stdlib.h>

int solution(int X, const int *A, int n) {
    int *check = calloc(X, sizeof(int));
    int cmp = 0;
    int time = -1;
    for (int x = 0; x < n; x++) {
        int temp = A[x];
        if (temp <= X) {
            if (check[temp - 1] > 0) continue;
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
""",
"csharp": r"""public int Solution(int X, int[] A)
{
    int[] check = new int[X];
    int cmp = 0;
    int time = -1;
    for (int x = 0; x < A.Length; x++)
    {
        int temp = A[x];
        if (temp <= X)
        {
            if (check[temp - 1] > 0) continue;
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
""",
}},
"T545": {"outputs": {
"python": r"""def join(values, delimiter):
    result = ""
    for value in values:
        result += value + delimiter
    if len(result) > 0:
        result = result[:len(result) - len(delimiter)]
    return result
""",
"c": r"""#include <stdlib.h>
#include <string.h>

char *join(char **input, int count, const char *delimiter) {
    size_t dlen = strlen(delimiter);
    size_t total = 1;
    for (int i = 0; i < count; i++) total += strlen(input[i]) + dlen;
    char *sb = malloc(total);
    sb[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(sb, input[i]);
        strcat(sb, delimiter);
    }
    size_t length = strlen(sb);
    if (length > 0) sb[length - dlen] = '\0';
    return sb;
}
""",
"csharp": r"""using System.Text;

private string Join(string[] input, string delimiter)
{
    var sb = new StringBuilder();
    foreach (string value in input)
    {
        sb.Append(value);
        sb.Append(delimiter);
    }
    int length = sb.Length;
    if (length > 0) sb.Length = length - delimiter.Length;
    return sb.ToString();
}
""",
}},
}
