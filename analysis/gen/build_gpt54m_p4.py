# -*- coding: utf-8 -*-
DATA4 = {
"T270": {
"python": r'''
def isPermutation(a, b):
    if len(a) != len(b):
        return False
    bChars = list(b)
    found = 0
    for eachA in a:
        for k, ch in enumerate(bChars):
            if eachA == ch:
                found += 1
                bChars[k] = "￿"
                break
    return found == len(a)
''',
"c": r'''
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

bool is_permutation(const char *a, const char *b) {
    size_t lenA = strlen(a);
    size_t lenB = strlen(b);
    if (lenA != lenB) {
        return false;
    }
    unsigned char *bChars = malloc(lenB + 1);
    memcpy(bChars, b, lenB);
    int found = 0;
    for (size_t i = 0; i < lenA; i++) {
        for (size_t k = 0; k < lenB; k++) {
            if ((unsigned char) a[i] == bChars[k]) {
                found++;
                bChars[k] = 0xFF;
                break;
            }
        }
    }
    free(bChars);
    return found == (int) lenA;
}
''',
"csharp": r'''
public static bool IsPermutation(string a, string b) {
    if (a.Length != b.Length) {
        return false;
    }
    char[] bChars = b.ToCharArray();
    int found = 0;
    foreach (char eachA in a) {
        for (int k = 0; k < bChars.Length; k++) {
            if (eachA == bChars[k]) {
                found++;
                bChars[k] = '￿';
                break;
            }
        }
    }
    return found == a.Length;
}
'''
},
"T323": {
"python": r'''
class NumberProcessor:
    def getName(self, value):
        negative = value.startswith("-")
        if negative:
            value = value[1:]
        dotIndex = value.find(".")
        decimalValue = None
        if dotIndex >= 0:
            decimalValue = value[dotIndex + 1:]
            value = value[:dotIndex]
        name = self.processor.getName(value)
        if not name:
            name = self.ZERO_TOKEN
        elif negative:
            name = self.MINUS + self.SEPARATOR + name
        if decimalValue is not None and decimalValue != "":
            name = (name + self.SEPARATOR + self.UNION_AND + self.SEPARATOR
                    + self.processor.getName(decimalValue) + self.SEPARATOR
                    + self.SCALE.getName(-len(decimalValue)))
        return name
''',
"c": r'''
#include <stdbool.h>
#include <string.h>

#define MAX_NAME 512

extern void processor_get_name(const char *value, char *out);
extern void scale_get_name(int exponent, char *out);
extern const char *ZERO_TOKEN;
extern const char *MINUS;
extern const char *SEPARATOR;
extern const char *UNION_AND;

void get_name(const char *value, char *out) {
    char intPart[MAX_NAME];
    char decimalPart[MAX_NAME];
    char name[MAX_NAME];
    char scaleName[32];
    bool negative = false;
    if (value[0] == '-') {
        negative = true;
        value++;
    }
    const char *dot = strchr(value, '.');
    if (dot != NULL) {
        size_t intLen = (size_t)(dot - value);
        memcpy(intPart, value, intLen);
        intPart[intLen] = '\0';
        strcpy(decimalPart, dot + 1);
    } else {
        strcpy(intPart, value);
        decimalPart[0] = '\0';
    }
    processor_get_name(intPart, name);
    if (name[0] == '\0') {
        strcpy(name, ZERO_TOKEN);
    } else if (negative) {
        char tmp[MAX_NAME];
        strcpy(tmp, MINUS);
        strcat(tmp, SEPARATOR);
        strcat(tmp, name);
        strcpy(name, tmp);
    }
    if (decimalPart[0] != '\0') {
        strcat(name, SEPARATOR);
        strcat(name, UNION_AND);
        strcat(name, SEPARATOR);
        char decimalName[MAX_NAME];
        processor_get_name(decimalPart, decimalName);
        strcat(name, decimalName);
        strcat(name, SEPARATOR);
        scale_get_name(-(int) strlen(decimalPart), scaleName);
        strcat(name, scaleName);
    }
    strcpy(out, name);
}
''',
"csharp": r'''
public string GetName(string value) {
    bool negative = value.StartsWith("-");
    if (negative) {
        value = value.Substring(1);
    }
    int dotIndex = value.IndexOf(".");
    string decimalValue = null;
    if (dotIndex >= 0) {
        decimalValue = value.Substring(dotIndex + 1);
        value = value.Substring(0, dotIndex);
    }
    string name = processor.GetName(value);
    if (name.Length == 0) {
        name = ZERO_TOKEN;
    } else if (negative) {
        name = MINUS + SEPARATOR + name;
    }
    if (!string.IsNullOrEmpty(decimalValue)) {
        name = name + SEPARATOR + UNION_AND + SEPARATOR + processor.GetName(decimalValue)
             + SEPARATOR + Scale.GetName(-decimalValue.Length);
    }
    return name;
}
'''
},
"T333": {
"python": r'''
class TensNameBuilder:
    TOKENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    UNION_SEPARATOR = "-"

    def getName(self, value):
        buffer = []
        if len(value) > 3:
            number = int(value[-3:])
        else:
            number = int(value)
        number %= 100
        tensFound = False
        if number >= 20:
            buffer.append(self.TOKENS[(number // 10) - 2])
            number %= 10
            tensFound = True
        if number != 0:
            if tensFound:
                buffer.append(self.UNION_SEPARATOR)
            buffer.append(self.unitProcessor.getName(number))
        return "".join(buffer)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *TOKENS[] = {"", "", "Twenty", "Thirty", "Forty", "Fifty",
                               "Sixty", "Seventy", "Eighty", "Ninety"};
static const char *UNION_SEPARATOR = "-";

extern void unit_processor_get_name(int number, char *out);

void get_name(const char *value, char *out) {
    char buffer[256] = "";
    int number;
    if (strlen(value) > 3) {
        char last3[4];
        memcpy(last3, value + strlen(value) - 3, 3);
        last3[3] = '\0';
        number = atoi(last3);
    } else {
        number = atoi(value);
    }
    number %= 100;
    int tensFound = 0;
    if (number >= 20) {
        strcat(buffer, TOKENS[(number / 10) - 2]);
        number %= 10;
        tensFound = 1;
    }
    if (number != 0) {
        if (tensFound) {
            strcat(buffer, UNION_SEPARATOR);
        }
        char unitName[64];
        unit_processor_get_name(number, unitName);
        strcat(buffer, unitName);
    }
    strcpy(out, buffer);
}
''',
"csharp": r'''
using System.Text;

public static string GetName(string value) {
    string[] TOKENS = { "", "", "Twenty", "Thirty", "Forty", "Fifty",
                        "Sixty", "Seventy", "Eighty", "Ninety" };
    const string UNION_SEPARATOR = "-";
    StringBuilder buffer = new StringBuilder();
    int number;
    if (value.Length > 3) {
        number = int.Parse(value.Substring(value.Length - 3));
    } else {
        number = int.Parse(value);
    }
    number %= 100;
    bool tensFound = false;
    if (number >= 20) {
        buffer.Append(TOKENS[(number / 10) - 2]);
        number %= 10;
        tensFound = true;
    }
    if (number != 0) {
        if (tensFound) {
            buffer.Append(UNION_SEPARATOR);
        }
        buffer.Append(unitProcessor.GetName(number));
    }
    return buffer.ToString();
}
'''
},
"T807": {
"python": r'''
def removeDuplicates(s):
    seen = ""
    for ch in s:
        if ch not in seen:
            seen += ch
    return seen
''',
"c": r'''
#include <string.h>

void remove_duplicates(const char *s, char *out) {
    int pos = 0;
    size_t len = strlen(s);
    for (size_t i = 0; i < len; i++) {
        int found = 0;
        for (int j = 0; j < pos; j++) {
            if (out[j] == s[i]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            out[pos++] = s[i];
        }
    }
    out[pos] = '\0';
}
''',
"csharp": r'''
using System;
using System.Text;

static string RemoveDuplicates(string s) {
    HashSet<char> seen = new HashSet<char>();
    StringBuilder noDupes = new StringBuilder();
    foreach (char c in s) {
        if (seen.Add(c)) {
            noDupes.Append(c);
        }
    }
    return noDupes.ToString();
}
'''
},
"T447": {
"python": r'''
def isAnagram(s1, s2):
    if len(s1) != len(s2):
        return False
    sorted1 = "".join(sorted(s1))
    sorted2 = "".join(sorted(s2))
    print(sorted1)
    print(sorted2)
    return sorted1 == sorted2
''',
"c": r'''
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp_char(const void *x, const void *y) {
    return (int) (*(const char *) x - *(const char *) y);
}

bool is_anagram(const char *s1, const char *s2) {
    if (strlen(s1) != strlen(s2)) {
        return false;
    }
    char *arr1 = strdup(s1);
    char *arr2 = strdup(s2);
    qsort(arr1, strlen(arr1), 1, cmp_char);
    qsort(arr2, strlen(arr2), 1, cmp_char);
    printf("%s\n%s\n", arr1, arr2);
    bool equal = strcmp(arr1, arr2) == 0;
    free(arr1);
    free(arr2);
    return equal;
}
''',
"csharp": r'''
using System;

public bool IsAnagram(string s1, string s2) {
    if (s1.Length != s2.Length) return false;
    char[] arr1 = s1.ToCharArray();
    char[] arr2 = s2.ToCharArray();
    Array.Sort(arr1);
    Array.Sort(arr2);
    Console.WriteLine(new string(arr1));
    Console.WriteLine(new string(arr2));
    return new string(arr1) == new string(arr2);
}
'''
},
"T92": {
"python": r'''
def compressBad(s):
    countConsecutive = 0
    compressed = []
    for i, ch in enumerate(s):
        countConsecutive += 1
        if i + 1 == len(s):
            compressed.append(ch + str(countConsecutive))
            countConsecutive = 0
            break
        elif ch != s[i + 1]:
            compressed.append(ch + str(countConsecutive))
            countConsecutive = 0
    return "".join(compressed)
''',
"c": r'''
#include <stdio.h>
#include <string.h>

void compressBad(const char *str, char *out) {
    int countConsecutive = 0;
    int pos = 0;
    size_t len = strlen(str);
    for (size_t i = 0; i < len; i++) {
        countConsecutive++;
        if (len == i + 1) {
            pos += sprintf(out + pos, "%c%d", str[i], countConsecutive);
            countConsecutive = 0;
            break;
        } else if (str[i] != str[i + 1]) {
            pos += sprintf(out + pos, "%c%d", str[i], countConsecutive);
            countConsecutive = 0;
        }
    }
    out[pos] = '\0';
}
''',
"csharp": r'''
using System.Text;

public static string CompressBad(string str) {
    int countConsecutive = 0;
    StringBuilder compressedString = new StringBuilder();
    for (int i = 0; i < str.Length; i++) {
        countConsecutive++;
        if (str.Length == i + 1) {
            compressedString.Append(str[i]).Append(countConsecutive);
            countConsecutive = 0;
            break;
        } else if (str[i] != str[i + 1]) {
            compressedString.Append(str[i]).Append(countConsecutive);
            countConsecutive = 0;
        }
    }
    return compressedString.ToString();
}
'''
}
}
