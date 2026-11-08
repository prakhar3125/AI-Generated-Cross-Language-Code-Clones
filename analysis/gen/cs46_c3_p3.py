DATA3 = {
"T634": {"outputs": {
"python": r"""import itertools

def show(items):
    print(items)

def main():
    lc = ['A', 'B', 'C', 'D']
    lC = ['a', 'b', 'c']
    li = [1, 2, 3, 4]
    llo = [lc, lC, li]
    for lo in itertools.product(*llo):
        show(list(lo))
""",
"c": r"""#include <stdio.h>

static void show(const int *combo, int n) {
    printf("(");
    for (int i = 0; i < n; i++) printf("%d%s", combo[i], i < n - 1 ? ", " : "");
    printf(")\n");
}

int main(void) {
    int g0[] = {'A', 'B', 'C', 'D'};
    int g1[] = {'a', 'b', 'c'};
    int g2[] = {1, 2, 3, 4};
    int *groups[3] = {g0, g1, g2};
    int sizes[3] = {4, 3, 4};
    int combo[3];
    for (int i0 = 0; i0 < sizes[0]; i0++) {
        combo[0] = groups[0][i0];
        for (int i1 = 0; i1 < sizes[1]; i1++) {
            combo[1] = groups[1][i1];
            for (int i2 = 0; i2 < sizes[2]; i2++) {
                combo[2] = groups[2][i2];
                show(combo, 3);
            }
        }
    }
    return 0;
}
""",
"csharp": r"""using System;
using System.Collections.Generic;

public static class Program
{
    private static void Show(List<object> lo)
    {
        Console.WriteLine("(" + string.Join(", ", lo) + ")");
    }

    private static IEnumerable<List<object>> Cartesian(List<object[]> lists)
    {
        var combos = new List<List<object>> { new List<object>() };
        foreach (var list in lists)
        {
            var next = new List<List<object>>();
            foreach (var prefix in combos)
            {
                foreach (var item in list)
                {
                    var copy = new List<object>(prefix);
                    copy.Add(item);
                    next.Add(copy);
                }
            }
            combos = next;
        }
        return combos;
    }

    public static void Main(string[] args)
    {
        var lc = new object[] { 'A', 'B', 'C', 'D' };
        var lC = new object[] { 'a', 'b', 'c' };
        var li = new object[] { 1, 2, 3, 4 };
        var llo = new List<object[]> { lc, lC, li };
        foreach (var lo in Cartesian(llo)) Show(lo);
    }
}
""",
}},
"T596": {"outputs": {
"python": r"""from http import HTTPStatus

class Product:
    def __init__(self, name=""):
        self.name = name

class Service:
    def get_product(self, product_id):
        return Product()

class ResponseEntity:
    def __init__(self, body=None, status=HTTPStatus.OK):
        self.body = body
        self.status = status

service = Service()

def match(match_id, body, request, response):
    try:
        p = service.get_product(request.product_id)
    except Exception:
        return ResponseEntity("Bad Request", HTTPStatus.BAD_REQUEST)
    return ResponseEntity(p, HTTPStatus.OK)
""",
"c": r"""#include <stdlib.h>

typedef struct Product { char *name; } Product;
typedef struct { char *productId; } Request;
typedef struct { int status; void *body; } ResponseEntity;

extern Product *service_getProduct(const char *productId);

ResponseEntity *match(const char *matchId, const char *body, Request *request) {
    Product *p = NULL;
    ResponseEntity *out = malloc(sizeof(ResponseEntity));
    if (request == NULL || request->productId == NULL) {
        out->status = 400;
        out->body = NULL;
        return out;
    }
    p = service_getProduct(request->productId);
    out->status = 200;
    out->body = p;
    return out;
}
""",
"csharp": r"""using System;
using System.Net;

public class Product { }

public static class Program
{
    private static Service service = new Service();

    public static HttpResponseMessage Match(string matchId, string body, Request request)
    {
        Product p;
        try
        {
            p = service.GetProduct(request.GetProductId());
        }
        catch (Exception)
        {
            return new HttpResponseMessage(HttpStatusCode.BadRequest);
        }
        return new HttpResponseMessage(HttpStatusCode.OK) { Content = new ObjectContent(p) };
    }
}
""",
}},
"T501": {"outputs": {
"python": r"""def find_min(A, c):
    x = A[c]
    position = c
    while c < len(A):
        if x > A[c]:
            x = A[c]
            position = c
        c += 1
    return position
""",
"c": r"""int findMIN(const int *A, int n, int c) {
    int x = A[c];
    int position = c;
    while (c < n) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}
""",
"csharp": r"""static int FindMin(int[] A, int c)
{
    int x = A[c];
    int position = c;
    while (c < A.Length)
    {
        if (x > A[c])
        {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}
""",
}},
"T744": {"outputs": {
"python": r"""def tortoise_moves():
    roll = t_gen()
    if roll in (1, 2, 3, 4, 5):
        return 3
    if roll in (6, 7, 8):
        return 1
    if roll in (9, 10):
        return -6
    return 0
""",
"c": r"""int tortoiseMoves(void) {
    switch (tGen()) {
        case 1: case 2: case 3: case 4: case 5: return 3;
        case 6: case 7: case 8: return 1;
        case 9: case 10: return -6;
        default: return 0;
    }
}
""",
"csharp": r"""public int TortoiseMoves()
{
    int roll = TGen();
    return roll switch
    {
        1 or 2 or 3 or 4 or 5 => 3,
        6 or 7 or 8 => 1,
        9 or 10 => -6,
        _ => 0
    };
}
""",
}},
"T586": {"outputs": {
"python": r"""def main():
    s = "harikrishna"
    s2 = ""
    for ch in s:
        if ch not in s2:
            s2 += ch
    print(s2)
""",
"c": r"""#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "harikrishna";
    char s2[64] = "";
    for (char *p = s; *p; p++) {
        if (strchr(s2, *p) == NULL) {
            int len = (int)strlen(s2);
            s2[len] = *p;
            s2[len + 1] = '\0';
        }
    }
    printf("%s\n", s2);
    return 0;
}
""",
"csharp": r"""using System;

public static void Main(string[] args)
{
    string s = "harikrishna";
    string s2 = "";
    foreach (char ch in s)
    {
        if (!s2.Contains(ch)) s2 += ch;
    }
    Console.WriteLine(s2);
}
""",
}},
}
