DATA_T2 = {
"T654": {
"python": r'''
def filter(source, dest, dstart, dend, decimal_digits):
    dot_pos = -1
    for i, c in enumerate(dest):
        if c == '.' or c == ',':
            dot_pos = i
            break
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if len(dest) - dot_pos > decimal_digits:
            return ""
    return None
''',
"c": r'''
#include <stddef.h>
#include <string.h>

const char *decimal_filter(const char *source, const char *dest, int dend, int decimal_digits) {
    int dot_pos = -1;
    for (int i = 0; dest[i] != '\0'; i++) {
        if (dest[i] == '.' || dest[i] == ',') {
            dot_pos = i;
            break;
        }
    }
    if (dot_pos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) {
            return "";
        }
        if (dend <= dot_pos) {
            return NULL;
        }
        if ((int)strlen(dest) - dot_pos > decimal_digits) {
            return "";
        }
    }
    return NULL;
}
''',
"csharp": r'''
public static string Filter(string source, string dest, int dstart, int dend, int decimalDigits)
{
    int dotPos = -1;
    for (int i = 0; i < dest.Length; i++)
    {
        char c = dest[i];
        if (c == '.' || c == ',')
        {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0)
    {
        if (source == "." || source == ",")
        {
            return "";
        }
        if (dend <= dotPos)
        {
            return null;
        }
        if (dest.Length - dotPos > decimalDigits)
        {
            return "";
        }
    }
    return null;
}
'''
},
"T102": {
"python": r'''
def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    i = 0
    while i < len(s2):
        ch = s2[i]
        if ch not in s1:
            return False
        s1 = s1.replace(ch, "", 1)
        s2 = s2.replace(ch, "", 1)
        i += 1
    return True
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

static void remove_first(char *s, char c) {
    char *p = strchr(s, c);
    if (p) memmove(p, p + 1, strlen(p));
}

int is_anagram(const char *a, const char *b) {
    if (strlen(a) != strlen(b)) return 0;
    char *s1 = strdup(a), *s2 = strdup(b);
    int result = 1;
    for (size_t i = 0; i < strlen(s2); i++) {
        char ch = s2[i];
        if (strchr(s1, ch) == NULL) { result = 0; break; }
        remove_first(s1, ch);
        remove_first(s2, ch);
    }
    free(s1);
    free(s2);
    return result;
}
''',
"csharp": r'''
public static bool IsAnagram(string s1, string s2)
{
    if (s1.Length != s2.Length)
    {
        return false;
    }
    for (int i = 0; i < s2.Length; i++)
    {
        string ch = s2[i].ToString();
        if (!s1.Contains(ch))
        {
            return false;
        }
        int idx = s1.IndexOf(ch);
        s1 = s1.Remove(idx, 1);
        idx = s2.IndexOf(ch);
        s2 = s2.Remove(idx, 1);
    }
    return true;
}
'''
},
"T245": {
"python": r'''
def main():
    text = input("Enter the String")
    counts = [0] * 256
    for ch in text:
        counts[ord(ch)] += 1
    for i in range(256):
        if counts[i] > 0:
            if counts[i] == 1:
                print(chr(i), end="")
            else:
                print(chr(i) + str(counts[i]), end="")
''',
"c": r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    int ar[256] = {0};
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) return 1;
    st[strcspn(st, "\n")] = '\0';
    for (size_t i = 0; i < strlen(st); i++) {
        ar[(unsigned char)st[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", i);
            } else {
                printf("%c%d", i, ar[i]);
            }
        }
    }
    return 0;
}
''',
"csharp": r'''
using System;

public static class CharRunLength
{
    public static void Main()
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        foreach (char c in st)
        {
            ar[c]++;
        }
        for (int i = 0; i < 256; i++)
        {
            if (ar[i] > 0)
            {
                if (ar[i] == 1)
                {
                    Console.Write((char)i);
                }
                else
                {
                    Console.Write((char)i + ar[i].ToString());
                }
            }
        }
    }
}
'''
},
"T634": {
"python": r'''
from itertools import product

def show(items):
    print(items)

def main():
    lc = ['A', 'B', 'C', 'D']
    l_c = ['a', 'b', 'c']
    li = [1, 2, 3, 4]
    for lo in product(lc, l_c, li):
        show(list(lo))
''',
"c": r'''
#include <stdio.h>

typedef struct { char kind; int num; } Var;

static void show(const Var *lo, int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        if (lo[i].kind == 'c') printf("'%c'", (char)lo[i].num);
        else printf("%d", lo[i].num);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}

int main(void) {
    Var lc[4] = {{'c','A'},{'c','B'},{'c','C'},{'c','D'}};
    Var lC[3] = {{'c','a'},{'c','b'},{'c','c'}};
    Var li[4] = {{'i',1},{'i',2},{'i',3},{'i',4}};
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            for (int k = 0; k < 4; k++) {
                Var combo[3] = {lc[i], lC[j], li[k]};
                show(combo, 3);
            }
        }
    }
    return 0;
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public static class CartesianDemo
{
    private static void Show(IEnumerable<object> items)
    {
        Console.WriteLine("[" + string.Join(", ", items) + "]");
    }

    public static void Main()
    {
        var lc = new List<object> { 'A', 'B', 'C', 'D' };
        var lC = new List<object> { 'a', 'b', 'c' };
        var li = new List<object> { 1, 2, 3, 4 };
        foreach (var a in lc)
        {
            foreach (var b in lC)
            {
                foreach (var c in li)
                {
                    Show(new List<object> { a, b, c });
                }
            }
        }
    }
}
'''
},
"T682": {
"python": r'''
def filter_input(source, dest, dstart, dend, decimal_digits):
    dot_pos = dest.find('.')
    if dot_pos < 0:
        dot_pos = dest.find(',')
    if dot_pos >= 0:
        if source in ('.', ','):
            return ''
        if dend <= dot_pos:
            return None
        if len(dest) - dot_pos > decimal_digits:
            return ''
    return None
''',
"c": r'''
#include <stddef.h>
#include <string.h>

const char *filter_input(const char *source, const char *dest, int dstart, int dend, int decimal_digits) {
    const char *dot = strchr(dest, '.');
    if (dot == NULL) dot = strchr(dest, ',');
    if (dot != NULL) {
        int dot_pos = (int)(dot - dest);
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) {
            return "";
        }
        if (dend <= dot_pos) {
            return NULL;
        }
        if ((int)strlen(dest) - dot_pos > decimal_digits) {
            return "";
        }
    }
    return NULL;
}
''',
"csharp": r'''
public static string FilterInput(string source, string dest, int dstart, int dend, int decimalDigits)
{
    int dotPos = dest.IndexOfAny(new[] { '.', ',' });
    if (dotPos >= 0)
    {
        if (source == "." || source == ",")
            return "";
        if (dend <= dotPos)
            return null;
        if (dest.Length - dotPos > decimalDigits)
            return "";
    }
    return null;
}
'''
},
"T596": {
"python": r'''
class HttpStatus:
    BAD_REQUEST = 400
    OK = 200

class ResponseEntity:
    def __init__(self, body, status):
        self.body = body
        self.status = status

class HttpRequest:
    def __init__(self, product_id):
        self._product_id = product_id

    def get_product_id(self):
        return self._product_id

class ProductService:
    def get_product(self, product_id):
        raise ValueError("product not found")

service = ProductService()

def match(request, response):
    try:
        p = service.get_product(request.get_product_id())
    except Exception:
        return ResponseEntity("Bad Request", HttpStatus.BAD_REQUEST)
    return ResponseEntity(p, HttpStatus.OK)
''',
"c": r'''
#include <stdlib.h>

typedef struct { int id; } Product;
typedef struct { int product_id; } HttpRequest;

typedef struct {
    Product *body;
    int status;
} ResponseEntity;

typedef struct {
    Product *(*get_product)(void *);
} Service;

static Product *get_product(void *self) { (void)self; return NULL; }

ResponseEntity *match(Service *service, HttpRequest *request) {
    Product *p = service->get_product(request);
    ResponseEntity *r = malloc(sizeof(ResponseEntity));
    if (p == NULL) {
        r->body = NULL;
        r->status = 400;
    } else {
        r->body = p;
        r->status = 200;
    }
    return r;
}
''',
"csharp": r'''
using System;

public class Product { }
public class ProductNotFoundException : Exception { }

public class ProductService
{
    public Product GetProduct(int productId)
    {
        throw new ProductNotFoundException();
    }
}

public class MatchController
{
    private readonly ProductService _service = new ProductService();

    public object Match(int productId)
    {
        Product p;
        try
        {
            p = _service.GetProduct(productId);
        }
        catch (Exception)
        {
            return new { Status = 400 };
        }
        return new { Body = p, Status = 200 };
    }
}
'''
},
"T501": {
"python": r'''
def find_min(a, c):
    x = a[c]
    position = c
    while c < len(a):
        if x > a[c]:
            x = a[c]
            position = c
        c += 1
    return position
''',
"c": r'''
static int find_min(const int *a, int len, int c) {
    int x = a[c];
    int position = c;
    while (c < len) {
        if (x > a[c]) {
            x = a[c];
            position = c;
        }
        c++;
    }
    return position;
}
''',
"csharp": r'''
public static int FindMin(int[] a, int c)
{
    int x = a[c];
    int position = c;
    while (c < a.Length)
    {
        if (x > a[c])
        {
            x = a[c];
            position = c;
        }
        c++;
    }
    return position;
}
'''
},
"T744": {
"python": r'''
import random

def t_gen():
    return random.randint(1, 10)

def tortoise_moves():
    roll = t_gen()
    if 1 <= roll <= 5:
        return 3
    if 6 <= roll <= 8:
        return 1
    if 9 <= roll <= 10:
        return -6
    return 0
''',
"c": r'''
#include <stdlib.h>

static int t_gen(void) {
    return rand() % 10 + 1;
}

int tortoise_moves(void) {
    switch (t_gen()) {
        case 1: case 2: case 3: case 4: case 5:
            return 3;
        case 6: case 7: case 8:
            return 1;
        case 9: case 10:
            return -6;
        default:
            return 0;
    }
}
''',
"csharp": r'''
using System;

public class Race
{
    private static readonly Random Rng = new Random();

    private static int TGen()
    {
        return Rng.Next(1, 11);
    }

    public int TortoiseMoves()
    {
        switch (TGen())
        {
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                return 3;
            case 6:
            case 7:
            case 8:
                return 1;
            case 9:
            case 10:
                return -6;
            default:
                return 0;
        }
    }
}
'''
}
}
