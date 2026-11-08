DATA_T4 = {
"T445": {"outputs": {
"python": r'''
def word_prime_map():
    return {
        'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19,
        'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53,
        'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89,
        'y': 97, 'z': 101,
    }


def is_anagram(word, anagram_word):
    if len(word) != len(anagram_word):
        return False
    words_char_num = 1
    anagram_word_num = 1
    primes = word_prime_map()
    for ch in word:
        words_char_num *= primes[ch]
    for ch in anagram_word:
        anagram_word_num *= primes[ch]
    return anagram_word_num == words_char_num
''',
"c": r'''
#include <string.h>

static int prime_for(char ch) {
    static const int primes[26] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                                   41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                                   89, 97, 101};
    if (ch >= 'a' && ch <= 'z') return primes[ch - 'a'];
    if (ch >= 'A' && ch <= 'Z') return primes[ch - 'A'];
    return 1;
}

int is_anagram(const char *word, const char *anagram_word) {
    if (strlen(word) != strlen(anagram_word)) {
        return 0;
    }
    long words_char_num = 1;
    long anagram_word_num = 1;
    for (const char *p = word; *p; p++) {
        words_char_num *= prime_for(*p);
    }
    for (const char *p = anagram_word; *p; p++) {
        anagram_word_num *= prime_for(*p);
    }
    return anagram_word_num == words_char_num;
}
''',
"csharp": r'''
public static bool IsAnagram(string word, string anagramWord)
{
    if (word.Length != anagramWord.Length)
    {
        return false;
    }
    var wordPrimeMap = WordPrimeMap();
    int wordsCharNum = 1;
    int anagramWordNum = 1;
    foreach (char ch in word)
        wordsCharNum *= wordPrimeMap[ch];
    foreach (char ch in anagramWord)
        anagramWordNum *= wordPrimeMap[ch];
    return anagramWordNum == wordsCharNum;
}

private static Dictionary<char, int> WordPrimeMap()
{
    return new Dictionary<char, int>
    {
        ['a'] = 2, ['b'] = 3, ['c'] = 5, ['d'] = 7, ['e'] = 11, ['f'] = 13,
        ['g'] = 17, ['h'] = 19, ['i'] = 23, ['j'] = 29, ['k'] = 31, ['l'] = 37,
        ['m'] = 41, ['n'] = 43, ['o'] = 47, ['p'] = 53, ['q'] = 59, ['r'] = 61,
        ['s'] = 67, ['t'] = 71, ['u'] = 73, ['v'] = 79, ['w'] = 83, ['x'] = 89,
        ['y'] = 97, ['z'] = 101
    };
}
'''}},
"T826": {"outputs": {
"python": r'''
import subprocess
import sys


def main(args):
    command = [args[0]]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    print("Program terminated!")

main(sys.argv)
''',
"c": r'''
#include <stdio.h>

int main(int argc, char **argv) {
    FILE *fp = popen(argv[1], "r");
    if (fp == NULL) {
        return 1;
    }
    char line[1024];
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("%s", line);
    }
    pclose(fp);
    printf("Program terminated!\n");
    return 0;
}
''',
"csharp": r'''
public static void Main(string args[])
{
    var builder = new System.Diagnostics.ProcessStartInfo(args[0])
    {
        RedirectStandardOutput = true,
        UseShellExecute = false
    };
    var process = System.Diagnostics.Process.Start(builder);
    string line;
    while ((line = process.StandardOutput.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
    Console.WriteLine("Program terminated!");
}
'''}},
"T774": {"outputs": {
"python": r'''
def main():
    password = "admin"
    test = input("Insert the admin pass: ")
    if test == password:
        print("Access granted", end="")
    else:
        for i in range(1, 3):
            print(f"You have {i} try(es): ", end="")
            test = input()
            if test == password:
                print("Access granted", end="")
                break
            elif i == 2:
                print("Access denied", end="")

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *pass = "admin";
    char test[128];
    printf("Insert the admin pass: ");
    if (!fgets(test, sizeof(test), stdin)) return 0;
    test[strcspn(test, "\n")] = '\0';
    if (strcmp(pass, test) == 0) {
        printf("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            printf("You have %d try(es): ", i);
            if (!fgets(test, sizeof(test), stdin)) return 0;
            test[strcspn(test, "\n")] = '\0';
            if (strcmp(pass, test) == 0) {
                printf("Access granted");
                break;
            } else if (i == 2) {
                printf("Access denied");
            }
        }
    }
    return 0;
}
''',
"csharp": r'''
public static void Main(string[] args)
{
    const string pass = "admin";
    Console.Write("Insert the admin pass: ");
    string test = Console.ReadLine();
    if (pass == test)
    {
        Console.Write("Access granted");
    }
    else
    {
        for (int i = 1; i < 3; i++)
        {
            Console.Write("You have " + i + " try(es): ");
            test = Console.ReadLine();
            if (pass == test)
            {
                Console.Write("Access granted");
                break;
            }
            else if (i == 2)
            {
                Console.Write("Access denied");
            }
        }
    }
}
'''}},
"T729": {"outputs": {
"python": r'''
CHARACTER_MAPPING = {'A': 1, 'C': 2, 'G': 3, 'T': 4}


def minimum(values):
    return min(values)


def solution(s, p, q):
    integer_input = [CHARACTER_MAPPING[ch] for ch in s]
    result = [0] * len(p)
    for index in range(len(p)):
        if p[index] == q[index]:
            result[index] = integer_input[p[index]]
            break
        sub_array = integer_input[p[index]:q[index] + 1]
        result[index] = minimum(sub_array)
    return result
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

static int character_mapping(char c) {
    switch (c) {
        case 'A': return 1;
        case 'C': return 2;
        case 'G': return 3;
        case 'T': return 4;
        default: return 0;
    }
}

int *solution(const char *S, const int P[], const int Q[], int plen) {
    int slen = (int)strlen(S);
    int *integer_input = malloc((size_t)slen * sizeof(int));
    for (int i = 0; i < slen; i++) {
        integer_input[i] = character_mapping(S[i]);
    }
    int *result = calloc((size_t)plen, sizeof(int));
    for (int index = 0; index < plen; index++) {
        if (P[index] == Q[index]) {
            result[index] = integer_input[P[index]];
            break;
        }
        int minimum_value = integer_input[P[index]];
        for (int i = P[index] + 1; i <= Q[index]; i++) {
            if (integer_input[i] < minimum_value) {
                minimum_value = integer_input[i];
            }
        }
        result[index] = minimum_value;
    }
    free(integer_input);
    return result;
}
''',
"csharp": r'''
public int[] Solution(string S, int[] P, int[] Q)
{
    var characterMapping = new Dictionary<char, int> { ['A'] = 1, ['C'] = 2, ['G'] = 3, ['T'] = 4 };
    int[] integerInput = S.Select(c => characterMapping[c]).ToArray();
    int[] result = new int[P.Length];
    for (int index = 0; index < P.Length; index++)
    {
        if (P[index] == Q[index])
        {
            result[index] = integerInput[P[index]];
            break;
        }
        int[] subArray = new int[Q[index] - P[index] + 1];
        Array.Copy(integerInput, P[index], subArray, 0, subArray.Length);
        result[index] = subArray.Min();
    }
    return result;
}
'''}},
"T126": {"outputs": {
"python": r'''
def solution(x, a):
    leaves = set()
    for i, value in enumerate(a):
        leaves.add(value)
        if x in leaves and len(leaves) == x:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, int A[], int len) {
    char *seen = calloc((size_t)X + 1, 1);
    int distinct = 0;
    int result = -1;
    for (int i = 0; i < len; i++) {
        if (A[i] >= 0 && A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
        }
        if (A[i] == X && distinct == X) {
            result = i;
            break;
        }
    }
    free(seen);
    return result;
}
''',
"csharp": r'''
public int Solution(int X, int[] A)
{
    var leaves = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        leaves.Add(A[i]);
        if (leaves.Contains(X) && leaves.Count == X) return i;
    }
    return -1;
}
'''}},
}
