DATA_T1 = {
"T234": {
"python": '''def main():
    name = "AnuvratAnuvra"
    counts = {}
    for ch in name:
        counts[ch] = counts.get(ch, 0) + 1
    for key, value in counts.items():
        if value > 1:
            print(str(key) + ":" + str(value))
''',
"c": r'''int main(void) {
    const char *name = "AnuvratAnuvra";
    int freq[256] = {0};
    for (const char *p = name; *p != '\0'; p++) {
        freq[(unsigned char) *p]++;
    }
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 1) {
            printf("%c:%d\n", (char) i, freq[i]);
        }
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    string name = "AnuvratAnuvra";
    var counts = new Dictionary<char, int>();
    foreach (char ch in name) {
        if (counts.ContainsKey(ch)) counts[ch]++;
        else counts[ch] = 1;
    }
    foreach (var entry in counts) {
        if (entry.Value > 1) {
            Console.WriteLine(entry.Key + ":" + entry.Value);
        }
    }
}
'''
},
"T240": {
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
                print(ch + str(ar[i]), end="")
''',
"c": r'''int main(void) {
    char st[1024];
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    for (const char *p = st; *p != '\0'; p++) {
        ar[(unsigned char) *p]++;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", (char) i);
            } else {
                printf("%c%d", (char) i, ar[i]);
            }
        }
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char ch in st) {
        ar[ch]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                Console.Write(ch);
            } else {
                Console.Write(ch.ToString() + ar[i]);
            }
        }
    }
}
'''
},
"T365": {
"python": '''import random

SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"

def generate_random_password(length):
    if length < 1:
        raise ValueError("length must be greater than 0")
    buf = [random.choice(SYMBOLS) for _ in range(length)]
    random.shuffle(buf)
    return "".join(buf)
''',
"c": r'''static const char SYMBOLS[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";

char *generate_random_password(int length) {
    if (length < 1) {
        return NULL;
    }
    size_t n = sizeof(SYMBOLS) - 1;
    char *buf = malloc((size_t) length + 1);
    for (int idx = 0; idx < length; ++idx) {
        buf[idx] = SYMBOLS[rand() % n];
    }
    buf[length] = '\0';
    for (int i = length - 1; i > 0; --i) {
        int j = rand() % (i + 1);
        char tmp = buf[i];
        buf[i] = buf[j];
        buf[j] = tmp;
    }
    return buf;
}
''',
"csharp": '''private static readonly Random RANDOM = new Random();
private const string SYMBOLS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";

public static string GenerateRandomPassword(int length) {
    if (length < 1) {
        throw new ArgumentException("length must be greater than 0");
    }
    var buf = new char[length];
    for (int idx = 0; idx < buf.Length; ++idx) {
        buf[idx] = SYMBOLS[RANDOM.Next(SYMBOLS.Length)];
    }
    for (int i = buf.Length - 1; i > 0; --i) {
        int j = RANDOM.Next(i + 1);
        char tmp = buf[i];
        buf[i] = buf[j];
        buf[j] = tmp;
    }
    return new string(buf);
}
'''
},
"T506": {
"python": '''def main():
    text = input()
    arrlist = list(text)
    for ch in text:
        freq = arrlist.count(ch)
        print("Frequency of " + ch + "  is:   " + str(freq))
''',
"c": r'''int main(void) {
    char str[1024];
    if (fgets(str, sizeof(str), stdin) == NULL) return 0;
    str[strcspn(str, "\n")] = '\0';
    int len = (int) strlen(str);
    for (int i = 0; i < len; i++) {
        int freq = 0;
        for (int j = 0; j < len; j++) {
            if (str[j] == str[i]) freq++;
        }
        printf("Frequency of %c  is:   %d\n", str[i], freq);
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    string str = Console.ReadLine();
    var arrlist = new List<char>(str);
    foreach (char ch in str) {
        int freq = arrlist.Count(c => c == ch);
        Console.WriteLine("Frequency of " + ch + "  is:   " + freq);
    }
}
'''
},
"T434": {
"python": '''class Histogram:
    def __init__(self, words):
        self.words = words

    def find_in_line(self, token):
        return token if token in self.words else None

def valid_name(input_tokens, histogram):
    user = ""
    name = next(input_tokens)
    if histogram.find_in_line(name) is not None:
        print("This name exist")
    else:
        print("Name not found")
        user = valid_name(input_tokens, histogram)
    return user
''',
"c": r'''typedef struct {
    const char **tokens;
    int pos;
} TokenStream;

const char *next_token(TokenStream *ts) {
    return ts->tokens[ts->pos++];
}

int find_in_line(TokenStream *ts, const char *name) {
    for (int i = ts->pos; ts->tokens[i] != NULL; i++) {
        if (strcmp(ts->tokens[i], name) == 0) return 1;
    }
    return 0;
}

const char *valid_name(TokenStream *input, TokenStream *histogram) {
    const char *user = "";
    const char *name = next_token(input);
    if (find_in_line(histogram, name)) {
        printf("This name exist\n");
    } else {
        printf("Name not found\n");
        user = valid_name(input, histogram);
    }
    return user;
}
''',
"csharp": '''public class TokenScanner {
    private readonly Queue<string> _tokens;
    private readonly HashSet<string> _histogram;

    public TokenScanner(IEnumerable<string> tokens, HashSet<string> histogram = null) {
        _tokens = new Queue<string>(tokens);
        _histogram = histogram;
    }

    public string Next() {
        return _tokens.Dequeue();
    }

    public string FindInLine(string name) {
        return _histogram != null && _histogram.Contains(name) ? name : null;
    }
}

public static string ValidName(TokenScanner input, TokenScanner histogram) {
    string user = "";
    string name = input.Next();
    if (histogram.FindInLine(name) != null) {
        Console.WriteLine("This name exist");
    } else {
        Console.WriteLine("Name not found");
        user = ValidName(input, histogram);
    }
    return user;
}
'''
},
"T639": {
"python": '''from pathlib import Path
from urllib.parse import urlparse

def get_protocol(file):
    try:
        return urlparse(Path(file).absolute().as_uri()).scheme
    except Exception:
        return "unknown"
''',
"c": r'''char *file_to_uri(const char *file) {
    if (file == NULL) return NULL;
    char *uri = malloc(strlen(file) + 8);
    strcpy(uri, "file://");
    strcat(uri, file);
    return uri;
}

const char *url_get_protocol(const char *uri) {
    static const char *protos[] = {"http", "https", "ftp", "file"};
    for (int i = 0; i < 4; i++) {
        size_t n = strlen(protos[i]);
        if (strncmp(uri, protos[i], n) == 0 && uri[n] == ':') return protos[i];
    }
    return NULL;
}

const char *get_protocol(const char *file) {
    const char *result;
    char *uri = file_to_uri(file);
    if (uri != NULL) {
        const char *p = url_get_protocol(uri);
        result = (p != NULL) ? p : "unknown";
        free(uri);
    } else {
        result = "unknown";
    }
    return result;
}
''',
"csharp": '''public static string GetProtocol(string file) {
    string result;
    try {
        result = new Uri(file).Scheme;
    } catch (Exception) {
        result = "unknown";
    }
    return result;
}
'''
},
"T848": {
"python": '''def main():
    for i in range(1, 16):
        if (i & 1) > 0: print("A", end="")
        if (i & 2) > 0: print("B", end="")
        if (i & 4) > 0: print("C", end="")
        if (i & 8) > 0: print("D", end="")
        print()
''',
"c": r'''int main(void) {
    for (int i = 1; i < 16; ++i) {
        if ((i & 1) > 0) printf("A");
        if ((i & 2) > 0) printf("B");
        if ((i & 4) > 0) printf("C");
        if ((i & 8) > 0) printf("D");
        printf("\n");
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    for (int i = 1; i < 16; ++i) {
        if ((i & 1) > 0) Console.Write("A");
        if ((i & 2) > 0) Console.Write("B");
        if ((i & 4) > 0) Console.Write("C");
        if ((i & 8) > 0) Console.Write("D");
        Console.WriteLine("");
    }
}
'''
},
"T613": {
"python": '''def sort(numbers, digit):
    if len(numbers) == 0 or digit <= 0:
        return numbers
    space = [[] for _ in range(10)]
    for num in numbers:
        space[(num // digit) % 10].append(num)
    k = 0
    for i in range(10):
        space[i] = sort(space[i], digit // 10)
        for value in space[i]:
            numbers[k] = value
            k += 1
    return numbers
''',
"c": r'''int *sort(int *numbers, int count, int digit) {
    if (count == 0 || digit <= 0) return numbers;
    int *buckets[10];
    int lens[10];
    for (int b = 0; b < 10; b++) {
        buckets[b] = malloc(sizeof(int) * (size_t) count);
        lens[b] = 0;
    }
    for (int j = 0; j < count; j++) {
        int idx = (numbers[j] / digit) % 10;
        buckets[idx][lens[idx]++] = numbers[j];
    }
    int k = 0;
    for (int i = 0; i < 10; i++) {
        sort(buckets[i], lens[i], digit / 10);
        for (int j = 0; j < lens[i]; j++) {
            numbers[k++] = buckets[i][j];
        }
        free(buckets[i]);
    }
    return numbers;
}
''',
"csharp": '''public static int[] Sort(int[] numbers, int digit) {
    if (numbers.Length == 0 || digit <= 0) return numbers;
    var space = new List<int>[10];
    for (int i = 0; i < 10; i++) space[i] = new List<int>();
    foreach (int num in numbers) {
        space[(num / digit) % 10].Add(num);
    }
    int k = 0;
    for (int i = 0; i < 10; i++) {
        int[] sortedBucket = Sort(space[i].ToArray(), digit / 10);
        foreach (int value in sortedBucket) {
            numbers[k++] = value;
        }
    }
    return numbers;
}
'''
},
"T18": {
"python": '''import threading
import traceback
from datetime import datetime

class TextView:
    def __init__(self, context):
        self.context = context

class MyActivity:
    def setContentView(self, view):
        pass

    def on_tick(self):
        pass

    def onCreate(self, savedInstanceState):
        self.tv = TextView(self)
        self.setContentView(self.tv)
        fmt = "%d.%m.%Y, %H:%M"
        oldTime = "19.02.2018, 12:00"
        newTime = "20.02.2018, 14:00"
        diff = 0
        try:
            oldDate = datetime.strptime(oldTime, fmt)
            newDate = datetime.strptime(newTime, fmt)
            self.oldLong = int(oldDate.timestamp() * 1000)
            self.newLong = int(newDate.timestamp() * 1000)
            diff = self.newLong - self.oldLong
        except ValueError:
            traceback.print_exc()
        counter = threading.Timer(diff / 1000.0, self.on_tick)
        counter.start()
''',
"c": r'''#include <time.h>

typedef struct {
    int ignored;
} Bundle;

static long oldLong, newLong, diff;

static void my_count_start(long millisInFuture, long interval) {
    (void) millisInFuture;
    (void) interval;
}

void onCreate(Bundle *savedInstanceState) {
    (void) savedInstanceState;
    struct tm oldTm, newTm;
    strptime("19.02.2018, 12:00", "%d.%m.%Y, %H:%M", &oldTm);
    strptime("20.02.2018, 14:00", "%d.%m.%Y, %H:%M", &newTm);
    oldLong = (long) timegm(&oldTm) * 1000L;
    newLong = (long) timegm(&newTm) * 1000L;
    diff = newLong - oldLong;
    my_count_start(diff, 1000);
}
''',
"csharp": '''public class Bundle { }

public class MyCount {
    private readonly long _millisInFuture;
    private readonly long _interval;

    public MyCount(long millisInFuture, long interval) {
        _millisInFuture = millisInFuture;
        _interval = interval;
    }

    public void Start() { }
}

public void OnCreate(Bundle savedInstanceState) {
    var formatter = "dd.MM.yyyy, HH:mm";
    string oldTime = "19.02.2018, 12:00";
    string newTime = "20.02.2018, 14:00";
    long diff = 0;
    try {
        var oldDate = DateTime.ParseExact(oldTime, formatter, CultureInfo.InvariantCulture);
        var newDate = DateTime.ParseExact(newTime, formatter, CultureInfo.InvariantCulture);
        var epoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        long oldLong = (long) oldDate.ToUniversalTime().Subtract(epoch).TotalMilliseconds;
        long newLong = (long) newDate.ToUniversalTime().Subtract(epoch).TotalMilliseconds;
        diff = newLong - oldLong;
    } catch (FormatException e) {
        Console.WriteLine(e.StackTrace);
    }
    MyCount counter = new MyCount(diff, 1000);
    counter.Start();
}
'''
},
}
