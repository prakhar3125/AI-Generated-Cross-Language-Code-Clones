DATA_T4 = {}

DATA_T4["T561"] = {
"python": r'''def main():
    myArray = []
    myArray.append(list("string1"))
    myArray.append(list("string2"))
    myArray.append(list("string3"))
    charArray2D = [list(row) for row in myArray]
    print(len(charArray2D))
    s = ""
    for c in myArray:
        s += "".join(c)
    charArray1D = list(s)
    print(len(charArray1D))

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    char first [] = "string1";
    char second [] = "string2";
    char third [] = "string3";
    char charArray2D [3] [16];
    strcpy (charArray2D [0], first);
    strcpy (charArray2D [1], second);
    strcpy (charArray2D [2], third);
    printf ("%d\n", 3);
    char s [64] = "";
    for (int i = 0; i < 3; i ++) {
        strcat (s, charArray2D [i]);
    }
    int charArray1DLen = (int) strlen (s);
    char charArray1D [64];
    memcpy (charArray1D, s, charArray1DLen + 1);
    printf ("%d\n", charArray1DLen);
    return 0;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;
using System.Text;

public static class CharFlattener
{
    public static void Main(string[] args)
    {
        List<char[]> myArray = new List<char[]>();
        myArray.Add("string1".ToCharArray());
        myArray.Add("string2".ToCharArray());
        myArray.Add("string3".ToCharArray());
        char[][] charArray2D = myArray.ToArray();
        Console.WriteLine(charArray2D.Length);
        StringBuilder s = new StringBuilder();
        foreach (char[] c in myArray)
        {
            s.Append(new string(c));
        }
        char[] charArray1D = s.ToString().ToCharArray();
        Console.WriteLine(charArray1D.Length);
    }
}
''',
}

DATA_T4["T171"] = {
"python": r'''def solution(X, A):
    leaves = set()
    for i in range(len(A)):
        leaves.add(A[i])
        if X in leaves and len(leaves) == X:
            return i
    return -1
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_POS 100000

static bool seen [MAX_POS];

int solution (int X, const int *A, int aLen) {
    memset (seen, 0, sizeof (seen));
    int distinct = 0;
    for (int i = 0; i < aLen; i ++) {
        if (A [i] >= 0 && A [i] < MAX_POS && ! seen [A [i]]) {
            seen [A [i]] = true;
            distinct ++;
        }
        if (X >= 0 && X < MAX_POS && seen [X] && distinct == X) return i;
    }
    return -1;
}
''',
"csharp": r'''using System;
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int X, int[] A)
    {
        HashSet<int> leaves = new HashSet<int>();
        for (int i = 0; i < A.Length; i++)
        {
            leaves.Add(A[i]);
            if (leaves.Contains(X) && leaves.Count == X) return i;
        }
        return -1;
    }
}
''',
}

DATA_T4["T533"] = {
"python": r'''import time

class InfiniteSleeper:
    def run(self):
        o = object()
        while True:
            try:
                time.sleep(9223372036854775)
            except KeyboardInterrupt:
                pass
''',
"c": r'''#include <unistd.h>

static void run (void) {
    void *o = (void *) 0;
    (void) o;
    for (;;) {
        sleep (2147483647);
    }
}
''',
"csharp": r'''using System;
using System.Threading;

public class InfiniteSleeper
{
    private object o = new object();

    public void Run()
    {
        while (true)
        {
            try
            {
                Thread.Sleep(Timeout.Infinite);
            }
            catch (ThreadInterruptedException)
            {
            }
        }
    }
}
''',
}

DATA_T4["T111"] = {
"python": r'''def singleNumber(nums):
    answer = 0
    al = []
    for i in range(len(nums)):
        al.append(nums[i])
    for i in range(len(nums)):
        test = nums[i]
        if al.index(test) == len(al) - 1 - al[::-1].index(test):
            answer = nums[i]
    return answer
''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

static int indexOf (const int *a, int len, int v) {
    for (int i = 0; i < len; i ++) {
        if (a [i] == v) return i;
    }
    return -1;
}

static int lastIndexOf (const int *a, int len, int v) {
    for (int i = len - 1; i >= 0; i --) {
        if (a [i] == v) return i;
    }
    return -1;
}

int singleNumber (const int *nums, int len) {
    int answer = 0;
    int *al = (int *) malloc (len * sizeof (int));
    if (al == NULL) return 0;
    for (int i = 0; i < len; i ++) al [i] = nums [i];
    for (int i = 0; i < len; i ++) {
        int test = nums [i];
        if (indexOf (al, len, test) == lastIndexOf (al, len, test)) {
            answer = nums [i];
        }
    }
    free (al);
    return answer;
}
''',
"csharp": r'''using System;
using System.Collections;

public static class SingleNumberFinder
{
    public static int SingleNumber(int[] nums)
    {
        int answer = 0;
        ArrayList al = new ArrayList();
        for (int i = 0; i < nums.Length; i++)
        {
            al.Add(nums[i]);
        }
        for (int i = 0; i < nums.Length; i++)
        {
            int test = nums[i];
            if (al.IndexOf(test) == al.LastIndexOf(test))
            {
                answer = nums[i];
            }
        }
        return answer;
    }
}
''',
}

DATA_T4["T224"] = {
"python": r'''import re

NUMBER_PATTERN = re.compile(r"([+-]?([0-9]*[.])?[0-9]+)")

def getNumber(s):
    return float(s)

def main():
    inputString = input()
    if NUMBER_PATTERN.fullmatch(inputString) is None:
        print("Not a Number")
    else:
        result2 = getNumber(inputString)
        print("result = " + str(result2))

main()
''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static double getNumber (const char *s) {
    return atof (s);
}

static int matchesNumber (const char *s) {
    int i = 0;
    if (s [i] == '+' || s [i] == '-') i ++;
    int intPart = 0;
    while (s [i] >= '0' && s [i] <= '9') {
        i ++;
        intPart = 1;
    }
    if (s [i] == '.') {
        i ++;
        int fracPart = 0;
        while (s [i] >= '0' && s [i] <= '9') {
            i ++;
            fracPart = 1;
        }
        if (! intPart && ! fracPart) return 0;
    } else if (! intPart) {
        return 0;
    }
    return s [i] == '\0';
}

int main (void) {
    char inputString [256];
    if (fgets (inputString, sizeof (inputString), stdin) == NULL) return 0;
    inputString [strcspn (inputString, "\r\n")] = '\0';
    if (! matchesNumber (inputString)) {
        printf ("Not a Number\n");
    } else {
        double result2 = getNumber (inputString);
        printf ("result = %g\n", result2);
    }
    return 0;
}
''',
"csharp": r'''using System;
using System.Text.RegularExpressions;

public static class NumberChecker
{
    private static readonly Regex NumberRegex = new Regex("^([+-]?([0-9]*[.])?[0-9]+)$");

    private static double GetNumber(string s)
    {
        return double.Parse(s);
    }

    public static void Main(string[] args)
    {
        string inputString = Console.ReadLine();
        if (!NumberRegex.IsMatch(inputString))
        {
            Console.WriteLine("Not a Number");
        }
        else
        {
            double result2 = GetNumber(inputString);
            Console.WriteLine("result = " + result2);
        }
    }
}
''',
}
