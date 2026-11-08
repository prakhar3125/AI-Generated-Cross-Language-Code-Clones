DATA2 = {}

DATA2["T448"] = {"outputs": {
"python": r"""
parentheses_map_left = {"(": ")"}
parentheses_map_right = {")": "("}


def is_balanced(s):
    result = False
    if len(s) < 2:
        return False
    stack = []
    for ch in s:
        if ch not in parentheses_map_right and ch not in parentheses_map_left:
            continue
        if ch in parentheses_map_left:
            stack.append(ch)
        else:
            if stack and stack.pop() == parentheses_map_right[ch]:
                result = True
            else:
                return False
    if stack:
        return False
    return result
""",
"c": r"""
#include <stdbool.h>
#include <string.h>

#define MAX_STACK 256

static bool opens(char c) {
    return c == '(' || c == '[' || c == '{';
}

static bool closes(char c) {
    return c == ')' || c == ']' || c == '}';
}

static char matches_opener(char c) {
    switch (c) {
        case ')': return '(';
        case ']': return '[';
        case '}': return '{';
        default: return '\0';
    }
}

bool is_balanced(const char *str) {
    bool result = false;
    size_t len = strlen(str);
    char stack[MAX_STACK];
    int top = 0;
    if (len < 2) {
        return false;
    }
    for (size_t i = 0; i < len; i++) {
        char ch = str[i];
        if (!closes(ch) && !opens(ch)) {
            continue;
        }
        if (opens(ch)) {
            if (top < MAX_STACK) {
                stack[top++] = ch;
            }
        } else {
            if (top > 0 && stack[--top] == matches_opener(ch)) {
                result = true;
            } else {
                return false;
            }
        }
    }
    if (top != 0) {
        return false;
    }
    return result;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class BalanceChecker
{
    private static readonly Dictionary<char, char> Left = new Dictionary<char, char> { { '(', ')' } };
    private static readonly Dictionary<char, char> Right = new Dictionary<char, char> { { ')', '(' } };

    public static bool IsBalanced(string str)
    {
        bool result = false;
        if (str.Length < 2)
        {
            return false;
        }
        Stack<char> stack = new Stack<char>();
        foreach (char ch in str)
        {
            if (!Right.ContainsKey(ch) && !Left.ContainsKey(ch))
            {
                continue;
            }
            if (Left.ContainsKey(ch))
            {
                stack.Push(ch);
            }
            else
            {
                if (stack.Count > 0 && stack.Pop() == Right[ch])
                {
                    result = true;
                }
                else
                {
                    return false;
                }
            }
        }
        if (stack.Count > 0)
        {
            return false;
        }
        return result;
    }
}
"""
}}

DATA2["T452"] = {"outputs": {
"python": r"""
def main():
    s = "my name is khan"
    words = s.split(" ")
    capitalized_word = ""
    for w in words:
        first = w[:1]
        f_after = w[1:]
        capitalized_word += first.upper() + f_after + " "
    print(capitalized_word)
""",
"c": r"""
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char str[] = "my name is khan";
    char capitalized[128] = "";
    char *word = strtok(str, " ");
    while (word != NULL) {
        char first = (char)toupper((unsigned char)word[0]);
        sprintf(capitalized + strlen(capitalized), "%c%s ", first, word + 1);
        word = strtok(NULL, " ");
    }
    printf("%s\n", capitalized);
    return 0;
}
""",
"csharp": r"""
using System;

public static class Capitalizer
{
    public static void Main(string[] args)
    {
        string str = "my name is khan";
        string[] words = str.Split(' ');
        string capitalizedWord = "";
        foreach (string w in words)
        {
            string first = w.Substring(0, 1);
            string fAfter = w.Substring(1);
            capitalizedWord += first.ToUpper() + fAfter + " ";
        }
        Console.WriteLine(capitalizedWord);
    }
}
"""
}}

DATA2["T479"] = {"outputs": {
"python": r"""
import random


def main():
    print("Enter first integer: ")
    num_one = int(input())
    print("You have keyed in " + str(num_one))
    print("Enter second integer: ")
    num_two = int(input())
    print("You have keyed in " + str(num_two))
    num = int(random.random() * num_two)
    if num > num_one:
        print("Random number: " + str(num))
    else:
        print("Random number: " + str(num_one + num))
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int numOne, numTwo;
    printf("Enter first integer: \n");
    if (scanf("%d", &numOne) != 1) return 1;
    printf("You have keyed in %d\n", numOne);
    printf("Enter second integer: \n");
    if (scanf("%d", &numTwo) != 1) return 1;
    printf("You have keyed in %d\n", numTwo);
    srand((unsigned int)time(NULL));
    int num = (int)((double)rand() / ((double)RAND_MAX + 1) * numTwo);
    int shown = (num > numOne) ? num : numOne + num;
    printf("Random number: %d\n", shown);
    return 0;
}
""",
"csharp": r"""
using System;

public static class RandomTwo
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
"""
}}

DATA2["T508"] = {"outputs": {
"python": r"""
from collections import Counter


def main():
    words_multiset = Counter()
    words = [""] + list("AAABBBBCC") + [""]
    words_multiset.update(words)
    output = ""
    for element, count in words_multiset.items():
        if element != "":
            output += str(count) + element
    print(output)
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *text = "AAABBBBCC";
    int counts[26] = {0};
    char output[128] = "";
    for (size_t i = 0; i < strlen(text); i++) {
        counts[text[i] - 'A']++;
    }
    for (int i = 0; i < 26; i++) {
        if (counts[i] != 0) {
            char part[8];
            sprintf(part, "%d%c", counts[i], 'A' + i);
            strcat(output, part);
        }
    }
    printf("%s\n", output);
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;
using System.Linq;

public static class MultisetCounter
{
    public static void Main(string[] args)
    {
        string output = "";
        string[] words = "AAABBBBCC".Select(c => c.ToString()).ToArray();
        Dictionary<char, int> counts = new Dictionary<char, int>();
        foreach (string word in words)
        {
            if (word.Length != 1)
            {
                continue;
            }
            char letter = word[0];
            counts[letter] = counts.TryGetValue(letter, out int n) ? n + 1 : 1;
        }
        foreach (KeyValuePair<char, int> entry in counts)
        {
            output += entry.Value + "" + entry.Key;
        }
        Console.WriteLine(output);
    }
}
"""
}}

DATA2["T533"] = {"outputs": {
"python": r"""
import time


class Sleeper:
    def run(self):
        while True:
            try:
                time.sleep(9223372036854775807)
            except KeyboardInterrupt:
                pass
""",
"c": r"""
#include <unistd.h>

static void *object;

void run(void) {
    void *o = object;
    (void)o;
    for (;;) {
        sleep(4294967295U);
    }
}
""",
"csharp": r"""
using System.Threading;

public class Sleeper
{
    private static object _object = new object();

    public void Run()
    {
        object o = _object;
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
"""
}}

DATA2["T561"] = {"outputs": {
"python": r"""
def main():
    my_array = []
    my_array.append(list("string1"))
    my_array.append(list("string2"))
    my_array.append(list("string3"))
    print(len(my_array))
    joined = "".join("".join(chars) for chars in my_array)
    print(len(joined))
""",
"c": r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *myArray[3] = {"string1", "string2", "string3"};
    char charArray2D[3][16];
    char charArray1D[64] = "";
    for (int i = 0; i < 3; i++) {
        strncpy(charArray2D[i], myArray[i], sizeof(charArray2D[i]) - 1);
        charArray2D[i][sizeof(charArray2D[i]) - 1] = '\0';
    }
    printf("%zu\n", sizeof(charArray2D) / sizeof(charArray2D[0]));
    for (int i = 0; i < 3; i++) {
        strcat(charArray1D, charArray2D[i]);
    }
    printf("%zu\n", strlen(charArray1D));
    return 0;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;
using System.Text;

public static class CharArrayJoiner
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
"""
}}

DATA2["T597"] = {"outputs": {
"python": r"""
class Product:
    pass


class Service:
    def get_product(self, product_id):
        return Product()


class Request:
    def get_product_id(self):
        return 0


class HttpStatus:
    BAD_REQUEST = 400
    OK = 200


class ResponseEntity:
    def __init__(self, body, status):
        self.body = body
        self.status = status


service = Service()


def match(match_id, body, request, response):
    try:
        p = service.get_product(request.get_product_id())
    except Exception:
        return ResponseEntity("", HttpStatus.BAD_REQUEST)
    return ResponseEntity(p, HttpStatus.OK)
""",
"c": r"""
typedef struct {
    void *body;
    int status;
} ResponseEntity;

extern void *service_get_product(int product_id);

/* Returns a ResponseEntity: status 400 when the lookup fails, 200 otherwise. */
ResponseEntity match(const char *match_id, const char *body, int product_id) {
    ResponseEntity re;
    void *p = service_get_product(product_id);
    if (p == NULL) {
        re.body = NULL;
        re.status = 400;
        return re;
    }
    re.body = p;
    re.status = 200;
    return re;
}
""",
"csharp": r"""
using System;

public class Product
{
}

public class Request
{
    public int GetProductId()
    {
        return 0;
    }
}

public class Service
{
    public Product GetProduct(int productId)
    {
        return new Product();
    }
}

public class ResponseEntity
{
    public object Body { get; set; }
    public int Status { get; set; }

    public ResponseEntity(object body, int status)
    {
        Body = body;
        Status = status;
    }
}

public static class Matcher
{
    private static readonly Service Service = new Service();

    public static ResponseEntity Match(string matchId, string body, Request request)
    {
        Product p;
        try
        {
            p = Service.GetProduct(request.GetProductId());
        }
        catch (Exception)
        {
            return new ResponseEntity(null, 400);
        }
        return new ResponseEntity(p, 200);
    }
}
"""
}}

DATA2["T693"] = {"outputs": {
"python": r"""
def find_combinations_count(amount, coins, check_from_index):
    if amount == 0:
        return 1
    if amount < 0 or len(coins) == check_from_index:
        return 0
    with_first = find_combinations_count(amount - coins[check_from_index], coins, check_from_index)
    without_first = find_combinations_count(amount, coins, check_from_index + 1)
    return with_first + without_first
""",
"c": r"""
int find_combinations_count(int amount, const int *coins, int coinCount, int checkFromIndex) {
    if (amount == 0) {
        return 1;
    }
    if (amount < 0 || coinCount == checkFromIndex) {
        return 0;
    }
    int withFirst = find_combinations_count(amount - coins[checkFromIndex], coins, coinCount, checkFromIndex);
    int withoutFirst = find_combinations_count(amount, coins, coinCount, checkFromIndex + 1);
    return withFirst + withoutFirst;
}
""",
"csharp": r"""
using System;

public static class CoinCombinations
{
    public static int FindCombinationsCount(int amount, int[] coins, int checkFromIndex)
    {
        if (amount == 0)
        {
            return 1;
        }
        if (amount < 0 || coins.Length == checkFromIndex)
        {
            return 0;
        }
        int withFirstCoin = FindCombinationsCount(amount - coins[checkFromIndex], coins, checkFromIndex);
        int withoutFirstCoin = FindCombinationsCount(amount, coins, checkFromIndex + 1);
        return withFirstCoin + withoutFirstCoin;
    }
}
"""
}}

DATA2["T815"] = {"outputs": {
"python": r"""
import calendar

_year = 2024
_month_no = 5
_day = 21


def get_next_month(max_date):
    month = _month_no + 1
    year = _year
    if month > 12:
        month = 1
        year += 1
    if max_date:
        day = calendar.monthrange(year, month)[1]
    else:
        day = _day
    return "%s-%s-%s" % (year, month, day)
""",
"c": r"""
#include <stdio.h>

static int ctx_year = 2024;
static int ctx_month_no = 5;
static int ctx_day = 21;

static int days_in_month(int year, int month) {
    static const int perMonth[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 2) {
        int leap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
        return leap ? 29 : 28;
    }
    return perMonth[month - 1];
}

void get_next_month(int max_date, char *out, size_t outSize) {
    int year = ctx_year;
    int month = ctx_month_no + 1;
    if (month > 12) {
        month = 1;
        year++;
    }
    int day = max_date ? days_in_month(year, month) : ctx_day;
    snprintf(out, outSize, "%d-%d-%d", year, month, day);
}
""",
"csharp": r"""
using System;

public class MonthNavigator
{
    private int _year = 2024;
    private int _monthNo = 5;
    private int _day = 21;

    public string GetNextMonth(bool maxDate)
    {
        DateTime calendar = new DateTime(_year, _monthNo, 1);
        calendar = calendar.AddMonths(1);
        if (maxDate)
        {
            int maxD = DateTime.DaysInMonth(calendar.Year, calendar.Month);
            calendar = new DateTime(calendar.Year, calendar.Month, maxD);
        }
        else
        {
            calendar = new DateTime(calendar.Year, calendar.Month, _day);
        }
        return calendar.Year + "-" + calendar.Month + "-" + calendar.Day;
    }
}
"""
}}
