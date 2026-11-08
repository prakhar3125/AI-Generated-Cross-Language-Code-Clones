DATA_T5 = {}

DATA_T5["T479"] = {
"python": r'''import random

def main():
    print("Enter first integer: ")
    numOne = int(input())
    print("You have keyed in " + str(numOne))
    print("Enter second integer: ")
    numTwo = int(input())
    print("You have keyed in " + str(numTwo))
    generator = random.Random()
    num = int(random.random() * numTwo)
    print("Random number: " + str(num if num > numOne else numOne + num))

main()
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (void) {
    int numOne, numTwo;
    printf ("Enter first integer: \n");
    if (scanf ("%d", & numOne) != 1) return 0;
    printf ("You have keyed in %d\n", numOne);
    printf ("Enter second integer: \n");
    if (scanf ("%d", & numTwo) != 1) return 0;
    printf ("You have keyed in %d\n", numTwo);
    srand ((unsigned) time (NULL));
    int num = (int) ((double) rand () / RAND_MAX * numTwo);
    printf ("Random number: %d\n", num > numOne ? num : numOne + num);
    return 0;
}
''',
"csharp": r'''using System;

public static class RandomDemo
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Enter first integer: ");
        int numOne = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numOne);
        Console.WriteLine("Enter second integer: ");
        int numTwo = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numTwo);
        Random generator = new Random();
        int num = (int)(generator.NextDouble() * numTwo);
        Console.WriteLine("Random number: " + ((num > numOne) ? num : numOne + num));
    }
}
''',
}

DATA_T5["T212"] = {
"python": r'''def main():
    needle = "ABC"
    haystack = "ABCDSGDABCSAGAABCCCCAAABAABC"
    numberOfOccurences = 0
    index = haystack.find(needle)
    while index != -1:
        numberOfOccurences += 1
        haystack = haystack[index + len(needle):]
        index = haystack.find(needle)
    print("" + str(numberOfOccurences))

main()
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main (void) {
    const char *needle = "ABC";
    char *haystack = strdup ("ABCDSGDABCSAGAABCCCCAAABAABC");
    int numberOfOccurences = 0;
    char *found = strstr (haystack, needle);
    while (found != NULL) {
        numberOfOccurences ++;
        char *rest = strdup (found + strlen (needle));
        free (haystack);
        haystack = rest;
        found = strstr (haystack, needle);
    }
    printf ("%s%d\n", "", numberOfOccurences);
    free (haystack);
    return 0;
}
''',
"csharp": r'''using System;

public static class OccurrenceCounter
{
    public static void Main(string[] args)
    {
        string needle = "ABC";
        string haystack = "ABCDSGDABCSAGAABCCCCAAABAABC";
        int numberOfOccurences = 0;
        int index = haystack.IndexOf(needle);
        while (index != -1)
        {
            numberOfOccurences++;
            haystack = haystack.Substring(index + needle.Length);
            index = haystack.IndexOf(needle);
        }
        Console.WriteLine("" + numberOfOccurences);
    }
}
''',
}

DATA_T5["T170"] = {
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
    return -1
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_VAL 100000

static bool seen [MAX_VAL];

int solution (int X, const int *A, int aLen) {
    memset (seen, 0, sizeof (seen));
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i <= X; i ++) {
        sum1 += i;
    }
    for (int i = 0; i < aLen; i ++) {
        if (A [i] >= 0 && A [i] < MAX_VAL && seen [A [i]]) continue;
        if (A [i] >= 0 && A [i] < MAX_VAL) seen [A [i]] = true;
        sum2 += A [i];
        if (sum1 == sum2) return i;
    }
    return -1;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class SumMatcher
{
    public static int Solution(int X, int[] A)
    {
        HashSet<int> set = new HashSet<int>();
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
}
''',
}

DATA_T5["T508"] = {
"python": r'''from collections import Counter

def main():
    output = ""
    wordsMultiset = Counter("AAABBBBCC")
    for element, count in wordsMultiset.items():
        if element != "":
            output += str(count) + "" + element
    print(output)

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    char output [256] = "";
    const char *text = "AAABBBBCC";
    int counts [256] = {0};
    char order [256];
    int orderCount = 0;
    size_t len = strlen (text);
    for (size_t i = 0; i < len; i ++) {
        unsigned char ch = (unsigned char) text [i];
        if (counts [ch] == 0) {
            order [orderCount ++] = (char) ch;
        }
        counts [ch] ++;
    }
    for (int i = 0; i < orderCount; i ++) {
        unsigned char ch = (unsigned char) order [i];
        if (ch != 0) {
            char piece [8];
            sprintf (piece, "%d%c", counts [ch], (char) ch);
            strcat (output, piece);
        }
    }
    printf ("%s\n", output);
    return 0;
}
''',
"csharp": r'''using System;
using System.Linq;

public static class MultisetCounter
{
    public static void Main(string[] args)
    {
        string output = "";
        string text = "AAABBBBCC";
        var groups = text.Select(c => c.ToString()).GroupBy(c => c);
        foreach (var group in groups)
        {
            if (!group.Key.Equals(""))
            {
                output += group.Count() + "" + group.Key;
            }
        }
        Console.WriteLine(output);
    }
}
''',
}

DATA_T5["T241"] = {
"python": r'''def main():
    hm = {}
    print("Enter an String:")
    s1 = input()
    for i in range(len(s1)):
        ch = s1[i]
        if ch not in hm:
            hm[ch] = 1
        else:
            hm[ch] = hm[ch] + 1
    print("The Charecters are:" + str(hm))

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    int counts [256] = {0};
    char order [256];
    int orderCount = 0;
    printf ("Enter an String:\n");
    char s1 [256];
    if (fgets (s1, sizeof (s1), stdin) == NULL) return 0;
    s1 [strcspn (s1, "\r\n")] = '\0';
    size_t len = strlen (s1);
    for (size_t i = 0; i < len; i ++) {
        unsigned char ch = (unsigned char) s1 [i];
        if (counts [ch] == 0) {
            order [orderCount ++] = (char) ch;
        }
        counts [ch] ++;
    }
    printf ("The Charecters are:{");
    for (int i = 0; i < orderCount; i ++) {
        unsigned char ch = (unsigned char) order [i];
        if (i > 0) printf (", ");
        printf ("%c=%d", (char) ch, counts [ch]);
    }
    printf ("}\n");
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class CharFrequency
{
    public static void Main(string[] args)
    {
        Dictionary<char, int> hm = new Dictionary<char, int>();
        Console.WriteLine("Enter an String:");
        string s1 = Console.ReadLine();
        for (int i = 0; i < s1.Length; i++)
        {
            if (!hm.ContainsKey(s1[i]))
            {
                hm[s1[i]] = 1;
            }
            else
            {
                hm[s1[i]] = hm[s1[i]] + 1;
            }
        }
        Console.WriteLine("The Charecters are:[" + string.Join(", ", hm) + "]");
    }
}
''',
}
