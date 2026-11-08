import json

T = {}
R = {}

T["T234"] = (r'''def main():
    name = "AnuvratAnuvra"
    counts = {}
    for val in name:
        counts[val] = counts[val] + 1 if val in counts else 1
    for key, value in counts.items():
        if value > 1:
            print(str(key) + ":" + str(value))
''', r'''void main_count(void) {
    const char *name = "AnuvratAnuvra";
    int counts[256] = {0};
    size_t n = strlen(name);
    for (size_t i = 0; i < n; i++) {
        counts[(unsigned char) name[i]] += 1;
    }
    for (int k = 0; k < 256; k++) {
        if (counts[k] > 1) {
            printf("%c:%d\n", (char) k, counts[k]);
        }
    }
}
''', r'''public static void Main(string[] args)
{
    string name = "AnuvratAnuvra";
    char[] arr = name.ToCharArray();
    Dictionary<char, int> map = new Dictionary<char, int>();
    foreach (char val in arr)
    {
        map[val] = map.ContainsKey(val) ? map[val] + 1 : 1;
    }
    foreach (KeyValuePair<char, int> entry in map)
    {
        if (entry.Value > 1)
        {
            char key = entry.Key;
            object value = entry.Value;
            Console.WriteLine(key + ":" + value);
        }
    }
}
''')

_t240_py = r'''def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for i in range(len(st)):
        ar[ord(st[i])] = ar[ord(st[i])] + 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + "" + str(ar[i]), end="")
'''
_t240_c = r'''void main_chars(void) {
    char st[4096];
    int ar[256] = {0};
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) {
        return;
    }
    size_t len = strlen(st);
    if (len > 0 && st[len - 1] == '\n') {
        st[--len] = '\0';
    }
    for (size_t i = 0; i < len; i++) {
        ar[(unsigned char) st[i]] = ar[(unsigned char) st[i]] + 1;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", ch);
            } else {
                printf("%c%d", ch, ar[i]);
            }
        }
    }
}
'''
_t240_cs = r'''public static void Main(params string[] a)
{
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    for (int i = 0; i < st.Length; i++)
    {
        ar[st[i]] = ar[st[i]] + 1;
    }
    for (int i = 0; i < 256; i++)
    {
        char ch = (char) i;
        if (ar[i] > 0)
        {
            if (ar[i] == 1)
            {
                Console.Write(ch);
            }
            else
            {
                Console.Write(ch + "" + ar[i]);
            }
        }
    }
}
'''
T["T240"] = (_t240_py, _t240_c, _t240_cs)
T["T247"] = (_t240_py, _t240_c, _t240_cs)

T["T365"] = (r'''import random

def generate_random_password(self, length):
    if length < 1:
        raise ValueError("length must be greater than 0")
    buf = [self.symbols[random.randrange(len(self.symbols))] for _ in range(length)]
    return self.shuffle("".join(buf))
''', r'''extern const char symbols[];
extern const int symbols_length;
extern char *shuffle(const char *s);

char *generate_random_password(int length) {
    if (length < 1) {
        fprintf(stderr, "length must be greater than 0\n");
        return NULL;
    }
    char *buf = (char *) malloc((size_t) length + 1);
    if (buf == NULL) {
        return NULL;
    }
    for (int idx = 0; idx < length; ++idx) {
        buf[idx] = symbols[rand() % symbols_length];
    }
    buf[length] = '\0';
    char *result = shuffle(buf);
    free(buf);
    return result;
}
''', r'''public string GenerateRandomPassword(int length)
{
    if (length < 1)
    {
        throw new ArgumentException("length must be greater than 0");
    }
    char[] buf = new char[length];
    for (int idx = 0; idx < buf.Length; ++idx)
    {
        buf[idx] = symbols[RANDOM.Next(symbols.Length)];
    }
    return Shuffle(new string(buf));
}
''')

T["T506"] = (r'''def main():
    s = input()
    arrlist = []
    for i in range(len(s)):
        arrlist.append(s[i])
    for i in range(len(s)):
        freq = arrlist.count(s[i])
        print("Frequency of " + s[i] + "  is:   " + str(freq))
''', r'''void main_frequency(void) {
    char str[4096];
    if (fgets(str, sizeof(str), stdin) == NULL) {
        return;
    }
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[--len] = '\0';
    }
    for (size_t i = 0; i < len; i++) {
        int freq = 0;
        for (size_t j = 0; j < len; j++) {
            if (str[j] == str[i]) {
                freq++;
            }
        }
        printf("Frequency of %c  is:   %d\n", str[i], freq);
    }
}
''', r'''public static void Main(string[] args)
{
    string str = Console.ReadLine();
    List<char> arrlist = new List<char>();
    for (int i = 0; i < str.Length; i++)
    {
        arrlist.Add(str[i]);
    }
    for (int i = 0; i < str.Length; i++)
    {
        int freq = arrlist.Count(c => c == str[i]);
        Console.WriteLine("Frequency of " + str[i] + "  is:   " + freq);
    }
}
''')

T["T434"] = (r'''def valid_name(input, histogram):
    user = ""
    name = input.next()
    if histogram.find_in_line(name) is not None:
        print("This name exist")
    else:
        print("Name not found")
        user = valid_name(input, histogram)
    return user
''', r'''char *valid_name(FILE *input, const char *histogram_line) {
    char name[256];
    char *user = "";
    if (fscanf(input, "%255s", name) != 1) {
        return user;
    }
    if (strstr(histogram_line, name) != NULL) {
        printf("This name exist\n");
    } else {
        printf("Name not found\n");
        user = valid_name(input, histogram_line);
    }
    return user;
}
''', r'''public static string ValidName(Scanner input, Scanner histogram)
{
    string user = "";
    string name = input.Next();
    if (histogram.FindInLine(name) != null)
    {
        Console.WriteLine("This name exist");
    }
    else
    {
        Console.WriteLine("Name not found");
        user = ValidName(input, histogram);
    }
    return user;
}
''')

T["T639"] = (r'''from pathlib import Path
from urllib.parse import urlparse

def get_protocol(file):
    try:
        result = urlparse(Path(file).absolute().as_uri()).scheme
    except Exception:
        result = "unknown"
    return result
''', r'''static const char *get_protocol(const char *file) {
    const char *result;
    if (file == NULL || file[0] == '\0') {
        result = "unknown";
    } else {
        result = "file";
    }
    return result;
}
''', r'''private static string GetProtocol(FileInfo file)
{
    string result;
    try
    {
        result = new Uri(file.FullName).Scheme;
    }
    catch (Exception)
    {
        result = "unknown";
    }
    return result;
}
''')

T["T848"] = (r'''def main():
    for i in range(1, 16):
        if (i & 1) > 0:
            print("A", end="")
        if (i & 2) > 0:
            print("B", end="")
        if (i & 4) > 0:
            print("C", end="")
        if (i & 8) > 0:
            print("D", end="")
        print("")
''', r'''int main(void) {
    for (int i = 1; i < 16; ++i) {
        if ((i & 1) > 0) printf("A");
        if ((i & 2) > 0) printf("B");
        if ((i & 4) > 0) printf("C");
        if ((i & 8) > 0) printf("D");
        printf("\n");
    }
    return 0;
}
''', r'''public static void Main(string[] args)
{
    for (int i = 1; i < 16; ++i)
    {
        if ((i & 1) > 0) Console.Write("A");
        if ((i & 2) > 0) Console.Write("B");
        if ((i & 4) > 0) Console.Write("C");
        if ((i & 8) > 0) Console.Write("D");
        Console.WriteLine("");
    }
}
''')

T["T613"] = (r'''def sort(numbers, digit):
    if len(numbers) == 0 or digit <= 0:
        return numbers
    space = [[] for _ in range(10)]
    length = [0] * 10
    for j in range(len(numbers)):
        i = (numbers[j] // digit) % 10
        length[i] += 1
        space[i].append(numbers[j])
    for i in range(10):
        bucket = [space[i][k] for k in range(length[i])]
        space[i] = sort(bucket, digit // 10)
    k = 0
    for i in range(10):
        for j in range(length[i]):
            numbers[k] = space[i][j]
            k += 1
    return numbers
''', r'''int *sort(int *numbers, int n, int digit) {
    if (n == 0 || digit <= 0) return numbers;
    int *space[10];
    int len[10];
    int i, j, k;
    for (i = 0; i < 10; i++) {
        space[i] = (int *) malloc((size_t) n * sizeof(int));
        len[i] = 0;
    }
    for (j = 0; j < n; j++) {
        i = (numbers[j] / digit) % 10;
        space[i][len[i]++] = numbers[j];
    }
    for (i = 0; i < 10; i++) {
        int *bucket = (int *) malloc((size_t) (len[i] > 0 ? len[i] : 1) * sizeof(int));
        for (k = 0; k < len[i]; k++) bucket[k] = space[i][k];
        sort(bucket, len[i], digit / 10);
        for (k = 0; k < len[i]; k++) space[i][k] = bucket[k];
        free(bucket);
    }
    k = 0;
    for (i = 0; i < 10; i++) {
        for (j = 0; j < len[i]; j++) {
            numbers[k] = space[i][j];
            k++;
        }
    }
    for (i = 0; i < 10; i++) free(space[i]);
    return numbers;
}
''', r'''public static int[] Sort(int[] numbers, int digit)
{
    if (numbers.Length == 0 || digit <= 0) return numbers;
    int[][] space = new int[10][];
    int[] len = new int[10];
    for (int b = 0; b < 10; b++) space[b] = new int[numbers.Length];
    int i, j = 0;
    for (j = 0; j < numbers.Length; j++)
    {
        i = (numbers[j] / digit) % 10;
        space[i][len[i]] = numbers[j];
        len[i]++;
    }
    for (i = 0; i < 10; i++)
    {
        int[] bucket = new int[len[i]];
        for (int k2 = 0; k2 < len[i]; k2++) bucket[k2] = space[i][k2];
        space[i] = Sort(bucket, digit / 10);
    }
    int k = 0;
    for (i = 0; i < 10; i++)
    {
        for (j = 0; j < len[i]; j++)
        {
            numbers[k] = space[i][j];
            k++;
        }
    }
    return numbers;
}
''')

T["T18"] = (r'''from datetime import datetime

def on_create(self, saved_instance_state):
    super().on_create(saved_instance_state)
    self.tv = TextView(self)
    self.set_content_view(self.tv)
    fmt = "%d.%m.%Y, %H:%M"
    old_time = "19.02.2018, 12:00"
    new_time = "20.02.2018, 14:00"
    try:
        old_date = datetime.strptime(old_time, fmt)
        new_date = datetime.strptime(new_time, fmt)
        self.old_long = int(old_date.timestamp() * 1000)
        self.new_long = int(new_date.timestamp() * 1000)
        self.diff = self.new_long - self.old_long
    except ValueError as e:
        print(e)
    counter = MyCount(self.diff, 1000)
    counter.start()
''', r'''void on_create(void) {
    struct tm tm_old, tm_new;
    const char *old_time = "19.02.2018, 12:00";
    const char *new_time = "20.02.2018, 14:00";
    memset(&tm_old, 0, sizeof(tm_old));
    memset(&tm_new, 0, sizeof(tm_new));
    tv = text_view_new();
    set_content_view(tv);
    if (strptime(old_time, "%d.%m.%Y, %H:%M", &tm_old) == NULL ||
        strptime(new_time, "%d.%m.%Y, %H:%M", &tm_new) == NULL) {
        fprintf(stderr, "ParseException\n");
    } else {
        tm_old.tm_isdst = -1;
        tm_new.tm_isdst = -1;
        old_long = (long long) mktime(&tm_old) * 1000LL;
        new_long = (long long) mktime(&tm_new) * 1000LL;
        diff = new_long - old_long;
    }
    my_count_start(diff, 1000);
}
''', r'''protected override void OnCreate(Bundle savedInstanceState)
{
    base.OnCreate(savedInstanceState);
    tv = new TextView(this);
    this.SetContentView(tv);
    string format = "dd.MM.yyyy, HH:mm";
    string oldTime = "19.02.2018, 12:00";
    string NewTime = "20.02.2018, 14:00";
    DateTime oldDate, newDate;
    try
    {
        oldDate = DateTime.ParseExact(oldTime, format, CultureInfo.InvariantCulture);
        newDate = DateTime.ParseExact(NewTime, format, CultureInfo.InvariantCulture);
        oldLong = new DateTimeOffset(oldDate).ToUnixTimeMilliseconds();
        NewLong = new DateTimeOffset(newDate).ToUnixTimeMilliseconds();
        diff = NewLong - oldLong;
    }
    catch (FormatException e)
    {
        Console.WriteLine(e);
    }
    MyCount counter = new MyCount(diff, 1000);
    counter.Start();
}
''')

T["T130"] = (r'''def solution(X, A):
    hset = set()
    for i in range(len(A)):
        if A[i] <= X:
            hset.add(A[i])
        if len(hset) == X:
            return i
    return -1
''', r'''int solution(int X, int *A, int n) {
    int *set = (int *) malloc((size_t) (n > 0 ? n : 1) * sizeof(int));
    int size = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] <= X) {
            int found = 0;
            for (int j = 0; j < size; j++) {
                if (set[j] == A[i]) {
                    found = 1;
                    break;
                }
            }
            if (!found) {
                set[size++] = A[i];
            }
        }
        if (size == X) {
            free(set);
            return i;
        }
    }
    free(set);
    return -1;
}
''', r'''public int Solution(int X, int[] A)
{
    HashSet<int> hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}
''')

T["T686"] = (r'''import sys

def main():
    num_of_items = 0
    print("Enter How Many Items: ", end="")
    try:
        num_of_items = int(input().strip())
    except ValueError:
        print("Number of items you entered is invalid!", end="")
        sys.exit(0)
    grocery = Grocery(num_of_items)
    for i in range(num_of_items):
        print("Enter Item " + str(i + 1) + " : ", end="")
        if not grocery.add_item(input()):
            print("First Item Duplicate Detected!")
            sys.exit(0)
    print(str(grocery))
''', r'''int main(void) {
    char line[1024];
    char *end;
    long num_of_items = 0;
    printf("Enter How Many Items: ");
    if (fgets(line, sizeof(line), stdin) == NULL) {
        printf("Number of items you entered is invalid!");
        exit(0);
    }
    line[strcspn(line, "\r\n")] = '\0';
    char *start = line;
    while (*start == ' ' || *start == '\t') start++;
    end = start + strlen(start);
    while (end > start && (end[-1] == ' ' || end[-1] == '\t')) end--;
    *end = '\0';
    char *parse_end;
    num_of_items = strtol(start, &parse_end, 10);
    if (*start == '\0' || *parse_end != '\0') {
        printf("Number of items you entered is invalid!");
        exit(0);
    }
    Grocery *grocery = grocery_new((int) num_of_items);
    for (int i = 0; i < num_of_items; i++) {
        printf("Enter Item %d : ", i + 1);
        if (fgets(line, sizeof(line), stdin) == NULL) {
            line[0] = '\0';
        }
        line[strcspn(line, "\r\n")] = '\0';
        if (!grocery_add_item(grocery, line)) {
            printf("First Item Duplicate Detected!\n");
            exit(0);
        }
    }
    char *text = grocery_to_string(grocery);
    printf("%s\n", text);
    return 0;
}
''', r'''public static void Main(string[] args)
{
    int numOfItems = 0;
    Console.Write("Enter How Many Items: ");
    try
    {
        numOfItems = int.Parse(Console.ReadLine().Trim());
    }
    catch (FormatException)
    {
        Console.Write("Number of items you entered is invalid!");
        Environment.Exit(0);
    }
    Grocery grocery = new Grocery(numOfItems);
    for (int i = 0; i < numOfItems; i++)
    {
        Console.Write("Enter Item " + (i + 1) + " : ");
        if (!grocery.AddItem(Console.ReadLine()))
        {
            Console.WriteLine("First Item Duplicate Detected!");
            Environment.Exit(0);
        }
    }
    Console.WriteLine(grocery.ToString());
}
''')

_t139_py = r'''def solution(X, A):
    empty_position = set()
    for i in range(1, X + 1):
        empty_position.add(i)
    for i in range(len(A)):
        empty_position.discard(A[i])
        if len(empty_position) == 0:
            return i
    return -1
'''
_t139_c = r'''int solution(int X, const int *A, int n) {
    char *present = (char *) calloc((size_t) (X > 0 ? X : 0) + 1, 1);
    int remaining = 0;
    for (int i = 1; i <= X; i++) {
        present[i] = 1;
        remaining++;
    }
    for (int i = 0; i < n; i++) {
        if (A[i] >= 1 && A[i] <= X && present[A[i]]) {
            present[A[i]] = 0;
            remaining--;
        }
        if (remaining == 0) {
            free(present);
            return i;
        }
    }
    free(present);
    return -1;
}
'''
_t139_cs = r'''public int Solution(int X, int[] A)
{
    ISet<int> emptyPosition = new HashSet<int>();
    for (int i = 1; i <= X; i++)
    {
        emptyPosition.Add(i);
    }
    for (int i = 0; i < A.Length; i++)
    {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0)
        {
            return i;
        }
    }
    return -1;
}
'''
T["T139"] = (_t139_py, _t139_c, _t139_cs)
T["T158"] = (_t139_py, _t139_c, _t139_cs)

T["T33"] = (r'''def get_rows(i, j, array):
    another = [None] * (j - i + 1)
    while i <= j:
        for k in range(len(another)):
            another[k] = array[i]
            i += 1
    return another
''', r'''int **get_rows(int i, int j, int **array) {
    int len = j - i + 1;
    int **another = (int **) malloc((size_t) (len > 0 ? len : 0) * sizeof(int *));
    while (i <= j) {
        for (int k = 0; k < len; k++) {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
''', r'''public static int[][] GetRows(int i, int j, int[][] array)
{
    int[][] another = new int[j - i + 1][];
    while (i <= j)
    {
        for (int k = 0; k < another.Length; k++)
        {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
''')

T["T445"] = (r'''def _wrap32(x):
    return ((x + 2**31) % 2**32) - 2**31

def is_anagram(word, anagram_word):
    if len(word) != len(anagram_word):
        return False
    words_char_num = 1
    anagram_word_num = 1
    word_prime_map = get_word_prime_map()
    for ch in word:
        words_char_num = _wrap32(words_char_num * word_prime_map[ch])
    for ch in anagram_word:
        anagram_word_num = _wrap32(anagram_word_num * word_prime_map[ch])
    return anagram_word_num == words_char_num
''', r'''extern int word_prime(char c);

bool is_anagram(const char *word, const char *anagram_word) {
    size_t n = strlen(word);
    if (n != strlen(anagram_word)) {
        return false;
    }
    uint32_t words_char_num = 1;
    uint32_t anagram_word_num = 1;
    for (size_t i = 0; i < n; i++) {
        words_char_num *= (uint32_t) word_prime(word[i]);
    }
    for (size_t i = 0; i < n; i++) {
        anagram_word_num *= (uint32_t) word_prime(anagram_word[i]);
    }
    return anagram_word_num == words_char_num;
}
''', r'''public static bool IsAnagram(string word, string anagram_word)
{
    if (word.Length != anagram_word.Length)
    {
        return false;
    }
    char[] words_char = word.ToCharArray();
    char[] anagram_word_char = anagram_word.ToCharArray();
    int words_char_num = 1;
    int anagram_word_num = 1;
    Dictionary<char, int> wordPrimeMap = WordPrimeMap();
    unchecked
    {
        for (int i = 0; i < words_char.Length; i++)
        {
            words_char_num *= wordPrimeMap[words_char[i]];
        }
        for (int i = 0; i < anagram_word_char.Length; i++)
        {
            anagram_word_num *= wordPrimeMap[anagram_word_char[i]];
        }
    }
    return anagram_word_num == words_char_num;
}
''')

T["T826"] = (r'''import subprocess
import sys

def main(args):
    command = [args[0]]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.rstrip("\r\n"))
    print("Program terminated!")
''', r'''int main(int argc, char *argv[]) {
    char line[4096];
    FILE *fp = popen(argv[1], "r");
    if (fp == NULL) {
        return 1;
    }
    while (fgets(line, sizeof(line), fp) != NULL) {
        line[strcspn(line, "\r\n")] = '\0';
        printf("%s\n", line);
    }
    pclose(fp);
    printf("Program terminated!\n");
    return 0;
}
''', r'''public static void Main(string[] args)
{
    List<string> command = new List<string>();
    command.Add(args[0]);
    ProcessStartInfo builder = new ProcessStartInfo(command[0]);
    builder.RedirectStandardOutput = true;
    builder.UseShellExecute = false;
    Process process = Process.Start(builder);
    StreamReader br = process.StandardOutput;
    string line;
    while ((line = br.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
    Console.WriteLine("Program terminated!");
}
''')

T["T774"] = (r'''def main():
    pass_ = "admin"
    print("Insert the admin pass: ", end="")
    test = input()
    if pass_ == test:
        print("Access granted", end="")
    else:
        for i in range(1, 3):
            print("You have " + str(i) + " try(es): ", end="")
            test = input()
            if pass_ == test:
                print("Access granted", end="")
                break
            elif i == 2:
                print("Access denied", end="")
''', r'''static void read_line(char *buf, size_t size) {
    if (fgets(buf, (int) size, stdin) == NULL) {
        buf[0] = '\0';
        return;
    }
    buf[strcspn(buf, "\r\n")] = '\0';
}

int main(void) {
    const char *pass = "admin";
    char test[256];
    printf("Insert the admin pass: ");
    read_line(test, sizeof(test));
    if (strcmp(pass, test) == 0) {
        printf("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            printf("You have %d try(es): ", i);
            read_line(test, sizeof(test));
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
''', r'''public static void Main(string[] args)
{
    string pass = "admin";
    Console.Write("Insert the admin pass: ");
    string test = Console.ReadLine();
    if (pass.Equals(test))
    {
        Console.Write("Access granted");
    }
    else
    {
        for (int i = 1; i < 3; i++)
        {
            Console.Write("You have " + i + " try(es): ");
            test = Console.ReadLine();
            if (pass.Equals(test))
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
''')

T["T729"] = (r'''def solution(self, S, P, Q):
    integer_input = [self.character_mapping[c] for c in S]
    result = [0] * len(P)
    for index in range(len(P)):
        if P[index] == Q[index]:
            result[index] = integer_input[P[index]]
            break
        sub_array = integer_input[P[index]:Q[index] + 1]
        minimum_value = min(sub_array)
        result[index] = minimum_value
    return result
''', r'''extern int character_mapping(char c);

int *solution(const char *S, const int *P, const int *Q, int m) {
    size_t len = strlen(S);
    int *integer_input = (int *) malloc((len > 0 ? len : 1) * sizeof(int));
    for (size_t counter = 0; counter < len; counter++) {
        integer_input[counter] = character_mapping(S[counter]);
    }
    int *result = (int *) calloc((size_t) (m > 0 ? m : 1), sizeof(int));
    for (int index = 0; index < m; index++) {
        if (P[index] == Q[index]) {
            result[index] = integer_input[P[index]];
            break;
        }
        int minimum_value = integer_input[P[index]];
        for (int k = P[index] + 1; k <= Q[index]; k++) {
            if (integer_input[k] < minimum_value) {
                minimum_value = integer_input[k];
            }
        }
        result[index] = minimum_value;
    }
    free(integer_input);
    return result;
}
''', r'''public int[] Solution(string S, int[] P, int[] Q)
{
    char[] characterInput = S.ToCharArray();
    int[] integerInput = new int[characterInput.Length];
    for (int counter = 0; counter < characterInput.Length; counter++)
    {
        integerInput[counter] = characterMapping[characterInput[counter]];
    }
    int[] result = new int[P.Length];
    for (int index = 0; index < P.Length; index++)
    {
        if (P[index] == Q[index])
        {
            result[index] = integerInput[P[index]];
            break;
        }
        int[] subArray = integerInput.Skip(P[index]).Take(Q[index] + 1 - P[index]).ToArray();
        int minimumValue = subArray.Min();
        result[index] = minimumValue;
    }
    return result;
}
''')

T["T126"] = (r'''def solution(X, A):
    leaves = set()
    for i in range(len(A)):
        leaves.add(A[i])
        if X in leaves and len(leaves) == X:
            return i
    return -1
''', r'''int solution(int X, const int *A, int n) {
    int *leaves = (int *) malloc((size_t) (n > 0 ? n : 1) * sizeof(int));
    int size = 0;
    for (int i = 0; i < n; i++) {
        int found = 0;
        for (int j = 0; j < size; j++) {
            if (leaves[j] == A[i]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            leaves[size++] = A[i];
        }
        int has_x = 0;
        for (int j = 0; j < size; j++) {
            if (leaves[j] == X) {
                has_x = 1;
                break;
            }
        }
        if (has_x && size == X) {
            free(leaves);
            return i;
        }
    }
    free(leaves);
    return -1;
}
''', r'''public int Solution(int X, int[] A)
{
    ISet<int> leaves = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        leaves.Add(A[i]);
        if (leaves.Contains(X) && leaves.Count == X) return i;
    }
    return -1;
}
''')

T["T641"] = (r'''def read(self):
    if self.current_pos < self.current_line_end:
        self.in_.seek(self.current_pos)
        self.current_pos += 1
        data = self.in_.read(1)
        if not data:
            raise EOFError()
        read_byte = data[0] - 256 if data[0] > 127 else data[0]
        return read_byte
    elif self.current_pos > self.last_pos_in_file and self.current_line_start < self.current_line_end:
        self.find_prev_line()
        if self.last_char != ord('\n') and self.last_char != ord('\r'):
            return ord('\n')
        else:
            return self.read()
    elif self.current_pos < 0:
        return -1
    else:
        self.find_prev_line()
        return self.read()
''', r'''int read_byte_at_cursor(void) {
    if (currentPos < currentLineEnd) {
        fseek(in, currentPos++, SEEK_SET);
        int c = fgetc(in);
        if (c == EOF) {
            return -2;
        }
        int readByte = (signed char) c;
        return readByte;
    } else if (currentPos > lastPosInFile && currentLineStart < currentLineEnd) {
        findPrevLine();
        if (lastChar != '\n' && lastChar != '\r') {
            return '\n';
        } else {
            return read_byte_at_cursor();
        }
    } else if (currentPos < 0) {
        return -1;
    } else {
        findPrevLine();
        return read_byte_at_cursor();
    }
}
''', r'''public int Read()
{
    if (currentPos < currentLineEnd)
    {
        input.Seek(currentPos++, SeekOrigin.Begin);
        int b = input.ReadByte();
        if (b == -1)
        {
            throw new EndOfStreamException();
        }
        int readByte = (sbyte) b;
        return readByte;
    }
    else if (currentPos > lastPosInFile && currentLineStart < currentLineEnd)
    {
        FindPrevLine();
        if (lastChar != '\n' && lastChar != '\r')
        {
            return '\n';
        }
        else
        {
            return Read();
        }
    }
    else if (currentPos < 0)
    {
        return -1;
    }
    else
    {
        FindPrevLine();
        return Read();
    }
}
''')

T["T605"] = (r'''import xml.etree.ElementTree as ET

def main():
    skip_depth = 0
    for event, elem in ET.iterparse("family.xml", events=("start", "end")):
        if event == "start":
            if skip_depth > 0:
                skip_depth += 1
                continue
            current_element_name = elem.tag
            if "dad" == current_element_name:
                print("isStartElement: true")
                print("Element BEGIN: " + current_element_name)
                skip_depth = 1
            else:
                print(current_element_name)
        else:
            if skip_depth > 0:
                skip_depth -= 1
''', r'''int main(void) {
    xmlTextReaderPtr reader = xmlReaderForFile("family.xml", NULL, 0);
    if (reader == NULL) {
        fprintf(stderr, "File not found: family.xml\n");
        return 1;
    }
    int ret = xmlTextReaderRead(reader);
    while (ret == 1) {
        if (xmlTextReaderNodeType(reader) == XML_READER_TYPE_ELEMENT) {
            const xmlChar *current_element_name = xmlTextReaderConstName(reader);
            if (xmlStrEqual(current_element_name, (const xmlChar *) "dad")) {
                printf("isStartElement: true\n");
                printf("Element BEGIN: %s\n", (const char *) current_element_name);
                ret = xmlTextReaderNext(reader);
                continue;
            } else {
                printf("%s\n", (const char *) current_element_name);
            }
        }
        ret = xmlTextReaderRead(reader);
    }
    xmlFreeTextReader(reader);
    return 0;
}
''', r'''public static void Main(string[] args)
{
    using (FileStream fis = new FileStream("family.xml", FileMode.Open))
    using (XmlReader xmlsr = XmlReader.Create(fis))
    {
        xmlsr.Read();
        while (!xmlsr.EOF)
        {
            if (xmlsr.NodeType == XmlNodeType.Element)
            {
                string currentElementName = xmlsr.Name;
                if ("dad".Equals(currentElementName))
                {
                    Console.WriteLine("isStartElement: " + xmlsr.IsStartElement().ToString().ToLower());
                    Console.WriteLine("Element BEGIN: " + currentElementName);
                    xmlsr.Skip();
                    continue;
                }
                else
                {
                    Console.WriteLine(currentElementName);
                }
            }
            xmlsr.Read();
        }
    }
}
''')

T["T759"] = (r'''def start(self, primary_stage):
    html_editor = HTMLEditor()
    primary_stage.set_scene(Scene(html_editor))
    primary_stage.show()
    tool_bar = html_editor.lookup(".tool-bar")
    while tool_bar is not None:
        tool_bar.get_parent().get_children().remove(tool_bar)
        tool_bar = html_editor.lookup(".tool-bar")
''', r'''void start(Stage *primary_stage) {
    HTMLEditor *html_editor = html_editor_new();
    stage_set_scene(primary_stage, scene_new(html_editor));
    stage_show(primary_stage);
    for (Node *tool_bar = node_lookup(html_editor, ".tool-bar");
         tool_bar != NULL;
         tool_bar = node_lookup(html_editor, ".tool-bar")) {
        pane_children_remove(node_get_parent(tool_bar), tool_bar);
    }
}
''', r'''public void Start(Stage primaryStage)
{
    HTMLEditor htmlEditor = new HTMLEditor();
    primaryStage.SetScene(new Scene(htmlEditor));
    primaryStage.Show();
    for (Node toolBar = htmlEditor.Lookup(".tool-bar");
         toolBar != null;
         toolBar = htmlEditor.Lookup(".tool-bar"))
    {
        ((Pane) toolBar.GetParent()).GetChildren().Remove(toolBar);
    }
}
''')

T["T723"] = (r'''def filter(self, words, text):
    for i in range(len(words)):
        if words[i].lower() in text.lower():
            print(text)
            break
''', r'''static char *to_lower_copy(const char *s) {
    size_t n = strlen(s);
    char *r = (char *) malloc(n + 1);
    for (size_t i = 0; i < n; i++) {
        r[i] = (char) tolower((unsigned char) s[i]);
    }
    r[n] = '\0';
    return r;
}

void filter(const char **words, int count, const char *text) {
    for (int i = 0; i < count; i++) {
        char *lower_text = to_lower_copy(text);
        char *lower_word = to_lower_copy(words[i]);
        int found = strstr(lower_text, lower_word) != NULL;
        free(lower_text);
        free(lower_word);
        if (found) {
            printf("%s\n", text);
            break;
        }
    }
}
''', r'''public void Filter(string[] words, string text)
{
    for (int i = 0; i < words.Length; i++)
    {
        if (text.ToLower().Contains(words[i].ToLower()))
        {
            Console.WriteLine(text);
            break;
        }
    }
}
''')

T["T309"] = (r'''def main():
    list1 = [Animal.Cat, Animal.Mouse, Animal.Dog]
    list2 = [Animal.Dog, Animal.Mouse, Animal.Cat]
    list3 = [Animal.Dog, Animal.Horse, Animal.Cat]
    list4 = [Animal.Dog, Animal.Tiger, Animal.Lion]
    lists = [list1, list2, list3, list4]
    sorted_lists = []
    for animals in lists:
        ar_list = sorted(animals, key=lambda a: a.value)
        if ar_list not in sorted_lists:
            sorted_lists.append(list(ar_list))
    for animals in sorted_lists:
        print("[" + ", ".join(a.name for a in animals) + "]")
''', r'''typedef enum { Cat, Mouse, Dog, Horse, Tiger, Lion } Animal;

static const char *animal_names[] = {"Cat", "Mouse", "Dog", "Horse", "Tiger", "Lion"};

static int cmp_animal(const void *a, const void *b) {
    return (int) *(const Animal *) a - (int) *(const Animal *) b;
}

int main(void) {
    Animal lists[4][3] = {
        {Cat, Mouse, Dog},
        {Dog, Mouse, Cat},
        {Dog, Horse, Cat},
        {Dog, Tiger, Lion}
    };
    Animal sorted[4][3];
    int sorted_count = 0;
    for (int i = 0; i < 4; i++) {
        Animal ar_list[3];
        memcpy(ar_list, lists[i], sizeof(ar_list));
        qsort(ar_list, 3, sizeof(Animal), cmp_animal);
        int duplicate = 0;
        for (int j = 0; j < sorted_count; j++) {
            if (memcmp(sorted[j], ar_list, sizeof(ar_list)) == 0) {
                duplicate = 1;
                break;
            }
        }
        if (!duplicate) {
            memcpy(sorted[sorted_count++], ar_list, sizeof(ar_list));
        }
    }
    for (int i = 0; i < sorted_count; i++) {
        printf("[%s, %s, %s]\n", animal_names[sorted[i][0]], animal_names[sorted[i][1]], animal_names[sorted[i][2]]);
    }
    return 0;
}
''', r'''public static void Main(string[] args)
{
    List<Animal> list1 = new List<Animal> { Animal.Cat, Animal.Mouse, Animal.Dog };
    List<Animal> list2 = new List<Animal> { Animal.Dog, Animal.Mouse, Animal.Cat };
    List<Animal> list3 = new List<Animal> { Animal.Dog, Animal.Horse, Animal.Cat };
    List<Animal> list4 = new List<Animal> { Animal.Dog, Animal.Tiger, Animal.Lion };
    List<List<Animal>> list = new List<List<Animal>> { list1, list2, list3, list4 };
    List<List<Animal>> sorted = new List<List<Animal>>();
    foreach (List<Animal> animals in list)
    {
        List<Animal> arList = new List<Animal>(animals);
        arList.Sort();
        if (!sorted.Any(s => s.SequenceEqual(arList)))
        {
            sorted.Add(new List<Animal>(arList));
        }
    }
    foreach (List<Animal> animals in sorted)
    {
        Console.WriteLine("[" + string.Join(", ", animals) + "]");
    }
}
''')

# ---------------- refactors ----------------
R["Rf3d83a68bd"] = r'''def curry(func):
    return lambda *args: (lambda *more_args: func(*args, *more_args))
'''

R["R7c5881afbf"] = r'''public static String Combine (String path1, String path2) {
    if (path1 == null) {
        throw new ArgumentNullException ("path1");
    }
    if (path2 == null) {
        throw new ArgumentNullException ("path2");
    }
    return CombineNoChecks (path1, path2);
}
'''

R["R0f80f0fb62"] = r'''public static Double Correlation (Double [] Xs, Double [] Ys) {
    int n = Math.Min (Xs.Length, Ys.Length);
    Double totalX = 0;
    Double totalY = 0;
    Double squaresX = 0;
    Double squaresY = 0;
    Double products = 0;
    int i = 0;
    while (i < n) {
        Double x = Xs [i];
        Double y = Ys [i];
        products += x * y;
        squaresY += y * y;
        squaresX += x * x;
        totalY += y;
        totalX += x;
        i++;
    }
    Double stdX = Math.Sqrt (squaresX - totalX * totalX * n);
    Double stdY = Math.Sqrt (squaresY - totalY * totalY * n);
    Double covariance = products - totalX * totalY * n;
    return covariance / stdX / stdY;
}
'''

R["Recd81e23e8"] = r'''int main (int argc, char **argv) {
    char **ipnport;
    ret[1] = (char *) calloc (20, 1);
    ret[0] = (char *) calloc (20, 1);
    ipnport = arguments_handle (argc, argv);
    printf ("IP is :%s port range is %s\n", ipnport [1], ipnport [0]);
    return 0;
}
'''

R["Radd810f35f"] = r'''public static String join (String separator, String...values) {
    if (values.length == 0) return "";
    int sepLength = separator.length ();
    StringBuilder builder = new StringBuilder ();
    for (int i = 0; i < values.length; i++) {
        if (values [i] == null) values [i] = "";
        if (i > 0 && sepLength > 0) builder.append (separator);
        builder.append (values [i]);
    }
    return builder.toString ();
}
'''

R["Ra654f3cacb"] = r'''public static boolean isPalindrome (String str) {
    String upper = str.toUpperCase ();
    int left = 0;
    int right = upper.length () - 1;
    while (left < right) {
        char a = upper.charAt (left);
        char b = upper.charAt (right);
        if (a != b && Character.toLowerCase (a) != Character.toLowerCase (b)) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
'''

R["Rc8ce82f32f"] = r'''int main (int argc, char **argv) {
    char c;
    printf ("Press key");
    for (;;) {
        if (kbhit ()) {
            break;
        }
        printf (".");
        fflush (stdout);
        sleep (1);
    }
    c = getchar ();
    printf ("\nChar received:%c\nDone.\n", c);
    return 0;
}
'''

R["Rdddd23f55c"] = r'''public void SendEmail (MyInternalSystemEmailMessage email) {
    var mailMessage = new System.Net.Mail.MailMessage {
        Subject = email.Subject,
        Body = email.Body,
        IsBodyHtml = email.IsHtml,
        From = new System.Net.Mail.MailAddress (email.FromAddress)
    };
    mailMessage.To.Add (email.ToRecipients);
    mailMessage.ReplyToList.Add (email.FromAddress);
    foreach (System.Net.Mail.Attachment attachment in email.Attachments) {
        mailMessage.Attachments.Add (attachment);
    }
    var mimeMessage = MimeKit.MimeMessage.CreateFromMailMessage (mailMessage);
    var request = service.Users.Messages.Send (
        new Google.Apis.Gmail.v1.Data.Message { Raw = Encode (mimeMessage.ToString ()) },
        ServiceEmail);
    request.Execute ();
}
'''

R["Rfa50623d34"] = r'''def upgrade():
    columns = [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=22), nullable=False),
        sa.Column('secret', sa.String(length=44), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
    ]
    constraints = [
        sa.ForeignKeyConstraint(['client_id'], ['client.id'],),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key'),
    ]
    engine = sa.create_engine(context.config.get_main_option("sqlalchemy.url"))
    DBSession.configure(bind=engine)
    op.create_table('client_credential', *(columns + constraints))
    clients = []
    for client in Client.query.all():
        clients.append({
            'client_id': client.id,
            'key': client.key,
            'secret': client.secret,
            'is_active': True,
            'created_at': sa.func.now(),
            'updated_at': sa.func.now(),
        })
    op.bulk_insert(ClientCredential, clients)
    for column_name in (u'secret', u'key'):
        op.drop_column(u'client', column_name)
'''

R["R6977f1c997"] = r'''def scan(sentence):
    result = []
    for word in sentence.split():
        if word in lexicons:
            result.append((lexicons[word], word))
        elif word.isdigit():
            result.append(('number', int(word)))
        else:
            result.append(('error', word))
    return result
'''

R["Rbcec8876d4"] = r'''def contains(small, big):
    size = len(small)
    for i in xrange(len(big) - size + 1):
        if all(big[i + j] == small[j] for j in xrange(size)):
            return i, i + size
    return False
'''

R["Rab8fdb571d"] = r'''int main () {
    char *str = malloc (100);
    char *token;
    strcpy (str, "test string.");
    token = strtok (str, " ");
    while (token != NULL) {
        printf ("%s\n", token);
        token = strtok (NULL, " ");
    }
    free (str);
    return 0;
}
'''

R["R6b8d361ee9"] = r'''static void Main (string [] args) {
    if (args.Length != 2) {
        Console.WriteLine ("Usage:  repchar {inputfile} {outputfile}");
        return;
    }
    const int blockSize = 100000;
    char [] inBuffer = new char [blockSize];
    char [] outBuffer = new char [blockSize * 3];
    using (StreamReader input = new StreamReader (args [0]))
    using (StreamWriter output = new StreamWriter (args [1]))
    {
        while (true) {
            int readSize = input.ReadBlock (inBuffer, 0, blockSize);
            if (readSize <= 0) {
                break;
            }
            int writeSize = TransformBlock (inBuffer, outBuffer, readSize);
            output.Write (outBuffer, 0, writeSize);
        }
    }
}
'''

R["Rc34ff3d7d3"] = r'''private void initData () {
    long [] [] mach1 = {
        {1477468500000L, 1}, {1477472100000L, 2}, {1477474200000L, 5},
        {1477476000000L, 3}, {1477479600000L, 4}, {1477486800000L, 1}
    };
    long [] [] mach2 = {
        {1477465200000L, 3}, {1477472400000L, 2}, {1477474200000L, 5},
        {1477476000000L, 2}, {1477479600000L, 3}, {1477486800000L, 4}
    };
    testData = new ArrayList < EventStatus > ();
    for (long [] row : mach1) {
        testData.add (new EventStatus ("Mach-1", row [0], (int) row [1], 0));
    }
    for (long [] row : mach2) {
        testData.add (new EventStatus ("Mach-2", row [0], (int) row [1], 1));
    }
    LinkedHashSet < String > names = new LinkedHashSet < > ();
    for (EventStatus eventStatus : testData) {
        names.add (eventStatus.getName ());
    }
    catArray = names.toArray (new String [0]);
}
'''

R["R73c281cc62"] = r'''private static IEnumerable < T [] > EnumerateCombos < T > (IEnumerable < T > items, List < T > currentCombo, int startIndex, int threshold) {
    if (currentCombo.Count < threshold) {
        IList < T > source = items as IList < T > ?? items.ToList ();
        for (int i = startIndex; i < source.Count; i ++) {
            currentCombo.Add (source [i]);
            yield return currentCombo.ToArray ();
            foreach (var combo in EnumerateCombos (source, currentCombo, i + 1, threshold)) {
                yield return combo;
            }
            currentCombo.RemoveAt (currentCombo.Count - 1);
        }
    }
}
'''

R["R91d065403d"] = r'''public static File createTempDir () {
    String baseName = System.currentTimeMillis () + "-";
    File baseDir = new File (System.getProperty ("java.io.tmpdir"));
    int counter = 0;
    while (counter < TEMP_DIR_ATTEMPTS) {
        File tempDir = new File (baseDir, baseName + counter);
        counter++;
        if (tempDir.mkdir ()) {
            return tempDir;
        }
    }
    throw new IllegalStateException ("Failed to create directory within " + TEMP_DIR_ATTEMPTS + " attempts (tried " + baseName + "0 to " + baseName + (TEMP_DIR_ATTEMPTS - 1) + ')');
}
'''

R["R8cfbeb65a3"] = r'''public static IList < ReportFile > ReadFiles (int year, int month) {
    string [] fileNames = { "{0:YYYYMMDD}----1234D.dat", "{0:YYYYMMDD}----5678D.dat" };
    DateTime firstDay = new DateTime (year, month, 1);
    int dayCount = firstDay.AddMonths (1).Subtract (firstDay).Days;
    IList < ReportFile > reportList = new List < ReportFile > ();
    for (int offset = 0; offset < dayCount; offset ++) {
        DateTime date = firstDay.AddDays (offset);
        foreach (string template in fileNames) {
            string file = string.Format (template, date);
            if (!File.Exists (file)) {
                continue;
            }
            reportList.Add (new ReportFile () { Date = date, Path = file, Lines = GetReportLines (file) });
        }
    }
    return reportList;
}
'''

R["R8f617cb401"] = r'''int main () {
    unsigned long *data = malloc (sizeof (unsigned long) * 9);
    int i;
    for (i = 8; i >= 0; --i)
        data[i] = i;
    unsigned long total = sumOfColTwo (data);
    printf ("%lu\n", total);
    free (data);
    return 0;
}
'''

R["R593eed57e6"] = r'''static void Main (string [] args) {
    Console.WriteLine ("Enter A Number :");
    int n = int.Parse (Console.ReadLine ());
    bool by3 = n % 3 == 0;
    bool by5 = n % 5 == 0;
    if (by3 && by5) {
        Console.WriteLine ("This Number is Divisible by 3 and 5!");
    } else if (by3) {
        printf ("\nThe number is divisible by 3 but not by 5");
    } else if (by5) {
        Console.WriteLine ("The number is divisible by 5 but not by 3");
    } else {
        Console.WriteLine ("\nThis Number is Not Divisible by 3 and 5!");
    }
    Console.ReadLine ();
}
'''

R["Rc5e1a6cc9a"] = r'''void initialize () {
    ConcurrentQueue < string > queue = new ConcurrentQueue < string > (websites);
    List < Thread > threads = Enumerable.Range (0, threadCountFromTheUser)
        .Select (_ => new Thread (work))
        .ToList ();
}
'''

R["R35e99f1126"] = r'''static void Main (string [] args) {
    var EDGES = new List < Edge > {
        new Edge (new Point (5, 50), new Point (20, 100)),
        new Edge (new Point (20, 100), new Point (30, 50)),
        new Edge (new Point (30, 50), new Point (10, 0)),
        new Edge (new Point (5, 50), new Point (30, 50)),
        new Edge (new Point (5, 50), new Point (10, 0)),
        new Edge (new Point (20, 100), new Point (80, 100)),
        new Edge (new Point (10, 0), new Point (80, 100))
    };
    var POINTS = new List < double [] > (EDGES.Count * 2);
    FillPoints (EDGES, ref POINTS);
    int index = 0;
    foreach (double [] point in POINTS) {
        Console.WriteLine ($"{index} {point [0]} {point [1]}");
        index ++;
    }
    Console.WriteLine ();
    var edgeIndices = new int [EDGES.Count, 2];
    FillEdges (EDGES, POINTS, ref edgeIndices);
    for (int row = 0; row < edgeIndices.GetLength (0); row ++) {
        Console.WriteLine ($"({edgeIndices [row, 0]}, {edgeIndices [row, 1]})");
    }
    Console.ReadKey (true);
}
'''

R["Ra1eaef8d13"] = r'''private static void removeEven (int [] k, int n) {
    int counter = 0;
    int i = 0;
    while (i < n) {
        if (k [i] % 2 == 1) {
            k [counter] = k [i];
            counter++;
        }
        i++;
    }
    java.util.Arrays.fill (k, counter, n, 0);
}
'''

R["R7fe68d314b"] = r'''public static List < string > LoadCitiesByState (string state) {
    DataTable dt = null;
    try {
        dt = SharedDataAccess.GetCities (state);
    }
    catch {
    }
    List < string > cities = new List < string > ();
    cities.AddRange (dt.Rows.Cast < DataRow > ().Select (row => row [0].ToString ()));
    return cities;
}
'''

R["R83b1b1f08f"] = r'''void main (int argc, char **argv) {
    int myargc = argc;
    char **myargv = malloc ((argc - 1) * sizeof (void *));
    int i = argc - 1;
    while (i > 0) {
        myargv[i - 1] = strdup (argv[i]);
        --i;
    }
    getch ();
}
'''

R["R08feb9bb95"] = r'''public void ResetFields (Control.ControlCollection Controls) {
    foreach (Control control in Controls) {
        switch (control) {
            case TextBox txt:
                txt.Text = string.Empty;
                break;
            case NumericUpDown numericUpDown:
                numericUpDown.Value = 3;
                break;
            default:
                if (control.Controls.Count > 0) {
                    this.ResetFields (control.Controls);
                }
                break;
        }
    }
}
'''

seeds = json.load(open(r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/seeds/chunk1.json", encoding="utf-8"))
out = []
for it in seeds:
    i = it["id"]
    if it["task"] == "translate":
        p, c, s = T[i]
        out.append({"id": i, "outputs": {"python": p.strip("\n"), "c": c.strip("\n"), "csharp": s.strip("\n")}})
    else:
        out.append({"id": i, "output": R[i].strip("\n")})
with open(r"C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/out/sonnet_chunk1.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(out))
