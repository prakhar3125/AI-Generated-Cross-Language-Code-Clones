DATA_T1 = {
"T471": {
"python": '''def get_max(start, arr):
    m = arr[start]
    for v in arr[start + 1:]:
        if v > m:
            m = v
    return m


def main():
    large = [0] * 10
    array = [33, 55, 13, 46, 87, 42, 10, 34, 43, 56]
    k = 0
    for _ in array:
        large[k] = get_max(0, array)
        k += 1
    print("Largest 5 is: " + str(large[:5]))''',
"c": '''#include <stdio.h>

int getMax(int from, int *arr, int len) {
    int m = arr[from];
    for (int i = from + 1; i < len; i++) {
        if (arr[i] > m) m = arr[i];
    }
    return m;
}

int main(void) {
    int large[10];
    int array[10] = {33, 55, 13, 46, 87, 42, 10, 34, 43, 56};
    int k = 0;
    for (int i = 0; i < 10; i++) {
        large[k++] = getMax(0, array, 10);
    }
    printf("Largest 5 is: %d %d %d %d %d\\n", large[0], large[1], large[2], large[3], large[4]);
    return 0;
}''',
"csharp": '''public static void Main() {
    int[] large = new int[10];
    int[] array = {33, 55, 13, 46, 87, 42, 10, 34, 43, 56};
    int k = 0;
    for (int i = 0; i < array.Length; i++) {
        large[k++] = GetMax(0, array);
    }
    int[] top5 = new int[5];
    for (int i = 0; i < 5; i++) top5[i] = large[i];
    System.Console.WriteLine("Largest 5 is: " + string.Join(", ", top5));
}

public static int GetMax(int from, int[] arr) {
    int m = arr[from];
    for (int i = from + 1; i < arr.Length; i++) {
        if (arr[i] > m) m = arr[i];
    }
    return m;
}'''
},
"T23": {
"python": '''def center(s, size, pad):
    if s is None or size <= len(s):
        return s
    result = pad * ((size - len(s)) // 2) + s
    while len(result) < size:
        result += pad
    return result''',
"c": '''#include <stdlib.h>
#include <string.h>

char *center(const char *s, int size, char pad) {
    if (s == NULL || size <= (int)strlen(s)) return (char *)s;
    char *sb = malloc(size + 1);
    int left = (size - (int)strlen(s)) / 2;
    int pos = 0;
    for (int i = 0; i < left; i++) sb[pos++] = pad;
    for (int i = 0; s[i]; i++) sb[pos++] = s[i];
    while (pos < size) sb[pos++] = pad;
    sb[pos] = '\\0';
    return sb;
}''',
"csharp": '''public static string Center(string s, int size, char pad) {
    if (s == null || size <= s.Length) return s;
    var sb = new System.Text.StringBuilder(size);
    for (int i = 0; i < (size - s.Length) / 2; i++) {
        sb.Append(pad);
    }
    sb.Append(s);
    while (sb.Length < size) {
        sb.Append(pad);
    }
    return sb.ToString();
}'''
},
"T135": {
"python": '''def solution(X, A):
    seen = set()
    sum1 = sum(range(X + 1))
    sum2 = 0
    for i, a in enumerate(A):
        if a in seen:
            continue
        seen.add(a)
        sum2 += a
        if sum1 == sum2:
            return i
    return -1''',
"c": '''#include <stdbool.h>

int solution(int X, int *A, int n) {
    int seen[100000];
    int seenCount = 0;
    long sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    for (int i = 0; i < n; i++) {
        bool dup = false;
        for (int j = 0; j < seenCount; j++) {
            if (seen[j] == A[i]) { dup = true; break; }
        }
        if (dup) continue;
        seen[seenCount++] = A[i];
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}''',
"csharp": '''public static int Solution(int X, int[] A) {
    var seen = new HashSet<int>();
    long sum1 = 0;
    for (int i = 0; i <= X; i++) sum1 += i;
    long sum2 = 0;
    for (int i = 0; i < A.Length; i++) {
        if (seen.Contains(A[i])) continue;
        seen.Add(A[i]);
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}'''
},
"T668": {
"python": '''def process_try():
    return float(input())


def main():
    trys = int(input().strip())
    for _ in range(trys):
        probability = process_try()
        print(probability)''',
"c": '''#include <stdio.h>
#include <stdlib.h>

double processTry(FILE *in) {
    double v = 0;
    if (fscanf(in, "%lf", &v) == 1) return v;
    return 0;
}

int main(void) {
    char line[128];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    int trys = atoi(line);
    for (int i = 0; i < trys; i++) {
        double probability = processTry(stdin);
        printf("%f\\n", probability);
    }
    return 0;
}''',
"csharp": '''public static void Main() {
    int trys = int.Parse(Console.ReadLine().Trim());
    for (int i = 0; i < trys; i++) {
        double probability = ProcessTry();
        Console.WriteLine(probability);
    }
}

static double ProcessTry() {
    return double.Parse(Console.ReadLine());
}'''
},
"T159": {
"python": '''def solution(X, A):
    check = [0] * X
    cmp = 0
    for x, temp in enumerate(A):
        if temp <= X:
            if check[temp - 1] > 0:
                continue
            check[temp - 1] += 1
            cmp += 1
        if cmp == X:
            return x
    return -1''',
"c": '''#include <stdlib.h>

int solution(int X, int *A, int size) {
    int *check = calloc(X, sizeof(int));
    int cmp = 0, time = -1;
    for (int x = 0; x < size; x++) {
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
}''',
"csharp": '''public int Solution(int X, int[] A) {
    int size = A.Length;
    int[] check = new int[X];
    int cmp = 0;
    int time = -1;
    for (int x = 0; x < size; x++) {
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
    return time;
}'''
},
"T545": {
"python": '''def join(input_list, delimiter):
    parts = []
    for value in input_list:
        parts.append(value)
        parts.append(delimiter)
    result = "".join(parts)
    if len(result) > 0:
        result = result[:len(result) - len(delimiter)]
    return result''',
"c": '''#include <stdlib.h>
#include <string.h>

char *join(char **input, int count, const char *delimiter) {
    size_t dlen = strlen(delimiter);
    size_t total = 1;
    for (int i = 0; i < count; i++) total += strlen(input[i]) + dlen;
    char *sb = malloc(total);
    sb[0] = '\\0';
    for (int i = 0; i < count; i++) {
        strcat(sb, input[i]);
        strcat(sb, delimiter);
    }
    size_t len = strlen(sb);
    if (len > 0) sb[len - dlen] = '\\0';
    return sb;
}''',
"csharp": '''private string Join(string[] input, string delimiter) {
    var sb = new StringBuilder();
    foreach (string value in input) {
        sb.Append(value);
        sb.Append(delimiter);
    }
    if (sb.Length > 0) {
        sb.Length -= delimiter.Length;
    }
    return sb.ToString();
}'''
},
"T721": {
"python": '''def num_letters(s):
    count = [0] * 26
    for c in s:
        count[ord(c) - ord('a')] += 1
    ans = ""
    for i in range(26):
        if count[i] != 0:
            ans += str(count[i]) + chr(i + ord('a'))
    return ans''',
"c": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *numLetters(const char *s) {
    int count[26] = {0};
    for (int i = 0; s[i]; i++) count[s[i] - 'a']++;
    char *ans = malloc(256);
    ans[0] = '\\0';
    char buf[16];
    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) {
            sprintf(buf, "%d%c", count[i], i + 'a');
            strcat(ans, buf);
        }
    }
    return ans;
}''',
"csharp": '''public static string NumLetters(string s) {
    int[] count = new int[26];
    foreach (char c in s) {
        count[c - 'a']++;
    }
    var ans = new StringBuilder();
    for (int i = 0; i < 26; i++) {
        if (count[i] != 0) {
            ans.Append(count[i]);
            ans.Append((char)(i + 'a'));
        }
    }
    return ans.ToString();
}'''
}
}
