DATA_T7 = {
    "T170": {
        "python": r'''def solution(X, A):
    seen = set()
    sum1 = 0
    sum2 = 0
    for i in range(X + 1):
        sum1 += i
    for i in range(len(A)):
        if A[i] in seen:
            continue
        seen.add(A[i])
        sum2 += A[i]
        if sum1 == sum2:
            return i
    return -1''',
        "c": r'''static int seen_before(const int *A, int i, int value) {
    for (int j = 0; j < i; j++) {
        if (A[j] == value) return 1;
    }
    return 0;
}

int solution(int X, const int *A, int a_len) {
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i++) {
        sum1 += i;
    }
    for (int i = 0; i < a_len; i++) {
        if (seen_before(A, i, A[i])) continue;
        sum2 += A[i];
        if (sum1 == sum2) return i;
    }
    return -1;
}''',
        "csharp": r'''using System.Collections.Generic;

public static class EquiSum
{
    public static int Solution(int X, int[] A)
    {
        var set = new HashSet<int>();
        int sum1 = 0, sum2 = 0;
        for (int i = 0; i <= X; i++)
        {
            sum1 += i;
        }
        for (int i = 0; i < A.Length; i++)
        {
            if (set.Contains(A[i])) continue;
            set.Add(A[i]);
            sum2 += A[i];
            if (sum1 == sum2) return i;
        }
        return -1;
    }
}'''
    },
    "T508": {
        "python": r'''from collections import Counter


def main():
    output = ""
    words_multiset = Counter(list("AAABBBBCC"))
    for element, count in words_multiset.items():
        if element != "":
            output += str(count) + str(element)
    print(output)''',
        "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char output[128] = "";
    const char *word = "AAABBBBCC";
    int counts[26] = {0};
    for (size_t i = 0; i < strlen(word); i++) {
        counts[word[i] - 'A']++;
    }
    for (int ch = 0; ch < 26; ch++) {
        if (counts[ch] > 0) {
            char tmp[16];
            snprintf(tmp, sizeof(tmp), "%d%c", counts[ch], 'A' + ch);
            strcat(output, tmp);
        }
    }
    printf("%s\n", output);
    return 0;
}''',
        "csharp": r'''using System;
using System.Linq;

public static class MultisetCounter
{
    public static void Main()
    {
        string output = "";
        var wordsMultiset = "AAABBBBCC".GroupBy(c => c);
        foreach (var group in wordsMultiset)
        {
            if (group.Key != '\0') output += group.Count() + "" + group.Key;
        }
        Console.WriteLine(output);
    }
}'''
    },
    "T241": {
        "python": r'''def main():
    hm = {}
    print("Enter an String:")
    s1 = input()
    for ch in s1:
        if ch not in hm:
            hm[ch] = 1
        else:
            hm[ch] = hm[ch] + 1
    print("The Charecters are:" + str(hm))''',
        "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    int hm[256] = {0};
    printf("Enter an String:\n");
    char s1[256];
    if (!fgets(s1, sizeof(s1), stdin)) return 0;
    s1[strcspn(s1, "\r\n")] = '\0';
    for (size_t i = 0; i < strlen(s1); i++) {
        hm[(unsigned char)s1[i]]++;
    }
    printf("The Charecters are:{");
    int first = 1;
    for (int i = 0; i < 256; i++) {
        if (hm[i] > 0) {
            if (!first) printf(", ");
            printf("%c=%d", i, hm[i]);
            first = 0;
        }
    }
    printf("}\n");
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;

public static class CharCounter
{
    public static void Main()
    {
        var hm = new Dictionary<char, int>();
        Console.WriteLine("Enter an String:");
        string s1 = Console.ReadLine();
        foreach (char ch in s1)
        {
            if (!hm.ContainsKey(ch))
            {
                hm[ch] = 1;
            }
            else
            {
                hm[ch] = hm[ch] + 1;
            }
        }
        Console.WriteLine("The Charecters are:" + string.Join(", ", hm));
    }
}'''
    }
}
