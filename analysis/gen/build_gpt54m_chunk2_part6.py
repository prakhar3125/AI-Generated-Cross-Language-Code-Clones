DATA_T6 = {
    "T224": {
        "python": r'''import re


def get_number(value):
    return float(value)


def main():
    input_string = input()
    if not re.fullmatch(r"[+-]?([0-9]*[.])?[0-9]+", input_string):
        print("Not a Number")
    else:
        result2 = get_number(input_string)
        print("result = " + str(result2))''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

static bool matches_number(const char *s) {
    size_t i = 0;
    if (s[i] == '+' || s[i] == '-') i++;
    size_t digits_before = 0;
    while (s[i] >= '0' && s[i] <= '9') { i++; digits_before++; }
    size_t digits_after = 0;
    if (s[i] == '.') {
        i++;
        while (s[i] >= '0' && s[i] <= '9') { i++; digits_after++; }
    }
    if (i != strlen(s)) return false;
    return digits_before + digits_after > 0;
}

int main(void) {
    char input_string[256];
    if (!fgets(input_string, sizeof(input_string), stdin)) return 0;
    input_string[strcspn(input_string, "\r\n")] = '\0';
    if (!matches_number(input_string)) {
        printf("Not a Number\n");
    } else {
        double result2 = atof(input_string);
        printf("result = %f\n", result2);
    }
    return 0;
}''',
        "csharp": r'''using System;
using System.Text.RegularExpressions;

public static class NumberReader
{
    private static double GetNumber(string value)
    {
        return double.Parse(value);
    }

    public static void Main()
    {
        string inputString = Console.ReadLine();
        if (!Regex.IsMatch(inputString, "^([+-]?([0-9]*[.])?[0-9]+)$"))
        {
            Console.WriteLine("Not a Number");
        }
        else
        {
            Double result2 = GetNumber(inputString);
            Console.WriteLine("result = " + result2);
        }
    }
}'''
    },
    "T479": {
        "python": r'''import random


def main():
    print("Enter first integer: ")
    num_one = int(input())
    print("You have keyed in " + str(num_one))
    print("Enter second integer: ")
    num_two = int(input())
    print("You have keyed in " + str(num_two))
    generator = random.Random()
    num = int(random.random() * num_two)
    print("Random number: " + str(num if num > num_one else num_one + num))''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int num_one, num_two;
    printf("Enter first integer: \n");
    if (scanf("%d", &num_one) != 1) return 0;
    printf("You have keyed in %d\n", num_one);
    printf("Enter second integer: \n");
    if (scanf("%d", &num_two) != 1) return 0;
    printf("You have keyed in %d\n", num_two);
    srand((unsigned)time(NULL));
    int num = (int)((double)rand() / RAND_MAX * num_two);
    printf("Random number: %d\n", num > num_one ? num : num_one + num);
    return 0;
}''',
        "csharp": r'''using System;

public static class RandomCompare
{
    public static void Main()
    {
        Console.WriteLine("Enter first integer: ");
        int numOne = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numOne);
        Console.WriteLine("Enter second integer: ");
        int numTwo = int.Parse(Console.ReadLine());
        Console.WriteLine("You have keyed in " + numTwo);
        var generator = new Random();
        int num = (int)(new Random().NextDouble() * numTwo);
        Console.WriteLine("Random number: " + (num > numOne ? num : numOne + num));
    }
}'''
    },
    "T212": {
        "python": r'''def main():
    needle = "ABC"
    haystack = "ABCDSGDABCSAGAABCCCCAAABAABC"
    number_of_occurences = 0
    index = haystack.find(needle)
    while index != -1:
        number_of_occurences += 1
        haystack = haystack[index + len(needle):]
        index = haystack.find(needle)
    print(str(number_of_occurences))''',
        "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *needle = "ABC";
    char haystack[] = "ABCDSGDABCSAGAABCCCCAAABAABC";
    int number_of_occurences = 0;
    char *index = strstr(haystack, needle);
    while (index != NULL) {
        number_of_occurences++;
        memmove(haystack, index + strlen(needle), strlen(index + strlen(needle)) + 1);
        index = strstr(haystack, needle);
    }
    printf("%d\n", number_of_occurences);
    return 0;
}''',
        "csharp": r'''using System;

public static class OccurrenceCounter
{
    public static void Main()
    {
        string needle = "ABC";
        string haystack = "ABCDSGDABCSAGAABCCCCAAABAABC";
        int numberOfOccurences = 0;
        int index = haystack.IndexOf(needle, StringComparison.Ordinal);
        while (index != -1)
        {
            numberOfOccurences++;
            haystack = haystack.Substring(index + needle.Length);
            index = haystack.IndexOf(needle, StringComparison.Ordinal);
        }
        Console.WriteLine("" + numberOfOccurences);
    }
}'''
    }
}
