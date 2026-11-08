DATA_T9 = {
    "T693": {
        "python": r'''def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    elif amount < 0 or len(coins) == check_from_index:
        return 0
    else:
        with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
        without_first_coin = find_combinations_count(amount, coins, check_from_index + 1)
        return with_first_coin + without_first_coin''',
        "c": r'''int find_combinations_count(int amount, const int *coins, int coins_len, int check_from_index) {
    if (amount == 0) return 1;
    else if (amount < 0 || coins_len == check_from_index) return 0;
    else {
        int with_first_coin = find_combinations_count(amount - coins[check_from_index], coins, coins_len, check_from_index);
        int without_first_coin = find_combinations_count(amount, coins, coins_len, check_from_index + 1);
        return with_first_coin + without_first_coin;
    }
}''',
        "csharp": r'''public static class CoinCombinations
{
    public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0) return 1;
        else if (amount < 0 || coins.Length == checkFromIndex) return 0;
        else
        {
            int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
            int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
            return withFirstCoin + withoutFirstCoin;
        }
    }
}'''
    },
    "T347": {
        "python": r'''SEPARATOR = " "
EXPONENT = "2"


class _NameSource:
    def get_name(self, value):
        return str(value) if value < 10 else ""


unit_processor = _NameSource()
tens_processor = _NameSource()


class _Scale:
    def get_name(self, exponent):
        return "hundred"


SCALE = _Scale()


def get_name(value):
    buffer = []
    number = 0
    if value == "":
        number = 0
    elif len(value) > 4:
        number = int(value[len(value) - 4:], 10)
    else:
        number = int(value, 10)
    number %= 1000
    if number >= 100:
        buffer.append(unit_processor.get_name(number // 100))
        buffer.append(SEPARATOR)
        buffer.append(SCALE.get_name(EXPONENT))
    tens_name = tens_processor.get_name(number % 100)
    if tens_name != "" and number >= 100:
        buffer.append(SEPARATOR)
    buffer.append(tens_name)
    return "".join(buffer)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern const char *SEPARATOR;
extern const char *EXPONENT_NAME;
extern void unit_processor_get_name(int value, char *out, size_t out_size);
extern void tens_processor_get_name(int value, char *out, size_t out_size);
extern void scale_get_name(const char *exponent, char *out, size_t out_size);

char *get_name(const char *value) {
    char *buffer = malloc(256);
    buffer[0] = '\0';
    char tmp[64];
    int number;
    if (value[0] == '\0') {
        number = 0;
    } else if (strlen(value) > 4) {
        number = atoi(value + strlen(value) - 4);
    } else {
        number = atoi(value);
    }
    number %= 1000;
    if (number >= 100) {
        unit_processor_get_name(number / 100, tmp, sizeof(tmp));
        strcat(buffer, tmp);
        strcat(buffer, SEPARATOR);
        scale_get_name(EXPONENT_NAME, tmp, sizeof(tmp));
        strcat(buffer, tmp);
    }
    char tens_name[64];
    tens_processor_get_name(number % 100, tens_name, sizeof(tens_name));
    if (tens_name[0] != '\0' && number >= 100) {
        strcat(buffer, SEPARATOR);
    }
    strcat(buffer, tens_name);
    return buffer;
}''',
        "csharp": r'''using System.Text;

public class NumberNamer
{
    private const string Separator = " ";
    private const string Exponent = "2";

    private static string UnitProcessorGetName(int value) => value.ToString();
    private static string TensProcessorGetName(int value) => value.ToString();
    private static string ScaleGetName(string exponent) => "hundred";

    public string GetName(string value)
    {
        var buffer = new StringBuilder();
        int number;
        if (value == "")
        {
            number = 0;
        }
        else if (value.Length > 4)
        {
            number = int.Parse(value.Substring(value.Length - 4));
        }
        else
        {
            number = int.Parse(value);
        }
        number %= 1000;
        if (number >= 100)
        {
            buffer.Append(UnitProcessorGetName(number / 100));
            buffer.Append(Separator);
            buffer.Append(ScaleGetName(Exponent));
        }
        string tensName = TensProcessorGetName(number % 100);
        if (tensName != "" && number >= 100)
        {
            buffer.Append(Separator);
        }
        buffer.Append(tensName);
        return buffer.ToString();
    }
}'''
    },
    "T253": {
        "python": r'''import random


def shuffle_array(ar):
    rnd = random.Random()
    for i in range(len(ar) - 1, 0, -1):
        index = rnd.randint(0, i)
        a = ar[index]
        ar[index] = ar[i]
        ar[i] = a''',
        "c": r'''void shuffle_array(int *ar, int ar_len) {
    for (int i = ar_len - 1; i > 0; i--) {
        int index = rand() % (i + 1);
        int a = ar[index];
        ar[index] = ar[i];
        ar[i] = a;
    }
}''',
        "csharp": r'''using System;

public static class Shuffler
{
    private static readonly Random Rnd = new Random();

    public static void ShuffleArray(int[] ar)
    {
        for (int i = ar.Length - 1; i > 0; i--)
        {
            int index = Rnd.Next(i + 1);
            int a = ar[index];
            ar[index] = ar[i];
            ar[i] = a;
        }
    }
}'''
    }
}
