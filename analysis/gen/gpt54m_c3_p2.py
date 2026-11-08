DATA_T2 = {
"T338": {
"python": '''class NumberToWord:
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
             "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def pw(self, n, suffix):
        if n <= 0:
            return
        if n >= 20:
            print(self.tens[n // 10] + (" " + self.words[n % 10] if n % 10 else ""), end="")
        else:
            print(self.words[n], end="")
        print(suffix, end="")


def main():
    print("Enter an integer number: ", end="")
    n = int(input())
    if n <= 0:
        print("Enter numbers greater than 0", end="")
    else:
        a = NumberToWord()
        print("After conversion number in words is :", end="")
        a.pw((n // 1000000000), " Hundred")
        a.pw((n // 10000000) % 100, " crore")
        a.pw(((n // 100000) % 100), " lakh")
        a.pw(((n // 1000) % 100), " thousand")
        a.pw(((n // 100) % 10), " hundred")
        a.pw((n % 100), " ")''',
"c": '''#include <stdio.h>

void pw(int n, const char *suffix) {
    if (n <= 0) return;
    printf("%d%s", n, suffix);
}

int main(void) {
    int n = 0;
    printf("Enter an integer number: ");
    scanf("%d", &n);
    if (n <= 0) {
        printf("Enter numbers greater than 0");
    } else {
        printf("After conversion number in words is :");
        pw((n / 1000000000), " Hundred");
        pw((n / 10000000) % 100, " crore");
        pw(((n / 100000) % 100), " lakh");
        pw(((n / 1000) % 100), " thousand");
        pw(((n / 100) % 10), " hundred");
        pw((n % 100), " ");
    }
    return 0;
}''',
"csharp": '''public class NumberToWord {
    public void Pw(int n, string suffix) {
        if (n <= 0) return;
        Console.Write(n + suffix);
    }
}

public static void Main() {
    Console.Write("Enter an integer number: ");
    int n = int.Parse(Console.ReadLine());
    if (n <= 0) {
        Console.Write("Enter numbers greater than 0");
    } else {
        NumberToWord a = new NumberToWord();
        Console.Write("After conversion number in words is :");
        a.Pw((n / 1000000000), " Hundred");
        a.Pw((n / 10000000) % 100, " crore");
        a.Pw(((n / 100000) % 100), " lakh");
        a.Pw(((n / 1000) % 100), " thousand");
        a.Pw(((n / 100) % 10), " hundred");
        a.Pw((n % 100), " ");
    }
}'''
},
"T654": {
"python": '''DECIMAL_DIGITS = 2


def filter(source, start, end, dest, dstart, dend):
    dot_pos = -1
    length = len(dest)
    for i in range(length):
        if dest[i] == '.' or dest[i] == ',':
            dot_pos = i
            break
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if length - dot_pos > DECIMAL_DIGITS:
            return ""
    return None''',
"c": '''#include <string.h>

int decimalDigits = 2;

char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    int dotPos = -1;
    int len = (int)strlen(dest);
    for (int i = 0; i < len; i++) {
        if (dest[i] == '.' || dest[i] == ',') {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) return "";
        if (dend <= dotPos) return NULL;
        if (len - dotPos > decimalDigits) return "";
    }
    return NULL;
}''',
"csharp": '''private int decimalDigits = 2;

public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
    int dotPos = -1;
    int len = dest.Length;
    for (int i = 0; i < len; i++) {
        char c = dest[i];
        if (c == '.' || c == ',') {
            dotPos = i;
            break;
        }
    }
    if (dotPos >= 0) {
        if (source == "." || source == ",") return "";
        if (dend <= dotPos) return null;
        if (len - dotPos > decimalDigits) return "";
    }
    return null;
}'''
},
"T102": {
"python": '''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    i = 0
    while i < len(s2):
        c = s2[i]
        if c not in s1:
            return False
        s1 = s1.replace(c, "", 1)
        s2 = s2.replace(c, "", 1)
    return True''',
"c": '''#include <stdbool.h>
#include <string.h>

bool isAnagram(char *s1, const char *s2) {
    char buf1[256], buf2[256];
    strcpy(buf1, s1);
    strcpy(buf2, s2);
    if (strlen(buf1) != strlen(buf2)) return false;
    for (int i = 0; buf2[i];) {
        char c[2] = {buf2[i], 0};
        char *pos = strstr(buf1, c);
        if (!pos) return false;
        memmove(pos, pos + 1, strlen(pos));
        memmove(buf2 + i, buf2 + i + 1, strlen(buf2 + i));
    }
    return true;
}''',
"csharp": '''public static bool IsAnagram(string s1, string s2) {
    if (s1.Length != s2.Length) return false;
    int i = 0;
    while (i < s2.Length) {
        char c = s2[i];
        int idx = s1.IndexOf(c);
        if (idx < 0) return false;
        s1 = s1.Remove(idx, 1);
        s2 = s2.Remove(i, 1);
    }
    return true;
}'''
},
"T245": {
"python": '''def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + str(ar[i]), end="")''',
"c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    char st[1024];
    int ar[256] = {0};
    printf("Enter the String");
    if (!fgets(st, sizeof(st), stdin)) return 0;
    st[strcspn(st, "\\n")] = '\\0';
    for (unsigned char *p = (unsigned char *)st; *p; p++) ar[*p]++;
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) printf("%c", ch);
            else printf("%c%d", ch, ar[i]);
        }
    }
    return 0;
}''',
"csharp": '''public static void Main() {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char c in st) {
        ar[(int)c]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char)i;
        if (ar[i] > 0) {
            if (ar[i] == 1) Console.Write(ch);
            else Console.Write(ch + "" + ar[i]);
        }
    }
}'''
},
"T634": {
"python": '''import itertools


def show(items):
    print(items)


def main():
    lc = ['A', 'B', 'C', 'D']
    lC = ['a', 'b', 'c']
    li = [1, 2, 3, 4]
    llo = [lc, lC, li]
    for lo in itertools.product(*llo):
        show(list(lo))''',
"c": '''#include <stdio.h>

void show(char a, char b, int c) {
    printf("[%c, %c, %d]\\n", a, b, c);
}

int main(void) {
    char lc[] = {'A', 'B', 'C', 'D'};
    char lC[] = {'a', 'b', 'c'};
    int li[] = {1, 2, 3, 4};
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            for (int k = 0; k < 4; k++) {
                show(lc[i], lC[j], li[k]);
            }
        }
    }
    return 0;
}''',
"csharp": '''public static void Show(List<object> lo) {
    Console.WriteLine("[" + string.Join(", ", lo) + "]");
}

public static IEnumerable<List<object>> Cartesian(List<List<object>> lists) {
    var indices = new int[lists.Count];
    while (true) {
        var current = new List<object>();
        for (int i = 0; i < lists.Count; i++) current.Add(lists[i][indices[i]]);
        yield return current;
        int pos = lists.Count - 1;
        while (pos >= 0) {
            indices[pos]++;
            if (indices[pos] < lists[pos].Count) break;
            indices[pos] = 0;
            pos--;
        }
        if (pos < 0) yield break;
    }
}

public static void Main() {
    var llo = new List<List<object>> {
        new List<object> {'A', 'B', 'C', 'D'},
        new List<object> {'a', 'b', 'c'},
        new List<object> {1, 2, 3, 4}
    };
    foreach (var lo in Cartesian(llo)) {
        Show(lo);
    }
}'''
},
"T682": {
"python": '''DECIMAL_DIGITS = 2


def filter(source, start, end, dest, dstart, dend):
    dot_pos = -1
    length = len(dest)
    i = 0
    while i < length and dot_pos < 0:
        if dest[i] == '.' or dest[i] == ',':
            dot_pos = i
        i += 1
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if length - dot_pos > DECIMAL_DIGITS:
            return ""
    return None''',
"c": '''#include <string.h>

int decimalDigits = 2;

char *filter(const char *source, int start, int end, const char *dest, int dstart, int dend) {
    int dotPos = -1;
    int len = (int)strlen(dest);
    const char *p = dest;
    while (*p) {
        if (*p == '.' || *p == ',') {
            dotPos = (int)(p - dest);
            break;
        }
        p++;
    }
    if (dotPos >= 0) {
        if (strcmp(source, ".") == 0 || strcmp(source, ",") == 0) return "";
        if (dend <= dotPos) return NULL;
        if (len - dotPos > decimalDigits) return "";
    }
    return NULL;
}''',
"csharp": '''private int decimalDigits = 2;

public string Filter(string source, int start, int end, string dest, int dstart, int dend) {
    int dotPos = dest.IndexOfAny(new[] {'.', ','});
    int len = dest.Length;
    if (dotPos >= 0) {
        if (source == "." || source == ",") return "";
        if (dend <= dotPos) return null;
        if (len - dotPos > decimalDigits) return "";
    }
    return null;
}'''
},
"T596": {
"python": '''class Service:
    def get_product(self, pid):
        return {"id": pid}


class ApiRequest:
    def get_product_id(self):
        return "1"


service = Service()


def match(match_id, body, request, response):
    try:
        p = service.get_product(request.get_product_id())
    except Exception:
        return ("", 400)
    return (p, 200)''',
"c": '''#include <stdlib.h>

typedef struct { int id; } Product;
typedef struct { int status; Product *body; } Response;

Product *tryGetProduct(int productId) {
    (void)productId;
    return NULL;
}

Response match(int productId) {
    Response r;
    Product *p = tryGetProduct(productId);
    if (p == NULL) {
        r.status = 400;
        r.body = NULL;
    } else {
        r.status = 200;
        r.body = p;
    }
    return r;
}''',
"csharp": '''public class Product { }

public class Service {
    public Product GetProduct(Product id) { return id; }
}

public class ApiRequest {
    public Product GetProductId() { return null; }
}

public class ApiResponse { }

public class MatchResult {
    public int Status;
    public Product Body;
}

public class MatchController {
    static Service service = new Service();

    public MatchResult Match(string matchId, string body, ApiRequest request, ApiResponse response) {
        Product p;
        try {
            p = service.GetProduct(request.GetProductId());
        } catch (Exception ex) {
            return new MatchResult { Status = 400 };
        }
        return new MatchResult { Status = 200, Body = p };
    }
}'''
}
}
