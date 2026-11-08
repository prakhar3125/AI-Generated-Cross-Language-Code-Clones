DATA_T2 = {
"T130": {
"python": '''def solution(X, A):
    hset = set()
    for i in range(len(A)):
        if A[i] <= X:
            hset.add(A[i])
        if len(hset) == X:
            return i
    return -1
''',
"c": r'''int solution(int X, const int *A, int n) {
    int *seen = calloc((size_t) X + 1, sizeof(int));
    int distinct = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] <= X && A[i] >= 1 && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
        }
        if (distinct == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
''',
"csharp": '''public static int Solution(int X, int[] A) {
    var hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++) {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}
'''
},
"T686": {
"python": '''import sys

class Grocery:
    def __init__(self, numOfItems):
        self.numOfItems = numOfItems
        self.items = []

    def add_item(self, item):
        if item in self.items:
            return False
        self.items.append(item)
        return True

    def __str__(self):
        return "Grocery items: " + ", ".join(self.items)

def main():
    print("Enter How Many Items: ", end="")
    try:
        numOfItems = int(input().strip())
    except ValueError:
        print("Number of items you entered is invalid!")
        sys.exit(0)
    grocery = Grocery(numOfItems)
    for i in range(numOfItems):
        print("Enter Item " + str(i + 1) + " : ", end="")
        if not grocery.add_item(input()):
            print("First Item Duplicate Detected!")
            sys.exit(0)
    print(grocery)
''',
"c": r'''#define MAX_ITEMS 100
#define ITEM_LEN 64

typedef struct {
    int numOfItems;
    int count;
    char items[MAX_ITEMS][ITEM_LEN];
} Grocery;

int grocery_add_item(Grocery *g, const char *item) {
    for (int i = 0; i < g->count; i++) {
        if (strcmp(g->items[i], item) == 0) return 0;
    }
    snprintf(g->items[g->count], ITEM_LEN, "%s", item);
    g->count++;
    return 1;
}

void grocery_print(const Grocery *g) {
    printf("Grocery items:");
    for (int i = 0; i < g->count; i++) {
        printf(" %s", g->items[i]);
    }
    printf("\n");
}

int main(void) {
    char line[ITEM_LEN];
    printf("Enter How Many Items: ");
    if (fgets(line, sizeof(line), stdin) == NULL) return 0;
    char *end;
    long val = strtol(line, &end, 10);
    if (end == line) {
        printf("Number of items you entered is invalid!\n");
        return 0;
    }
    int numOfItems = (int) val;
    Grocery grocery;
    grocery.numOfItems = numOfItems;
    grocery.count = 0;
    for (int i = 0; i < numOfItems; i++) {
        printf("Enter Item %d : ", i + 1);
        if (fgets(line, sizeof(line), stdin) == NULL) return 0;
        line[strcspn(line, "\n")] = '\0';
        if (!grocery_add_item(&grocery, line)) {
            printf("First Item Duplicate Detected!\n");
            return 0;
        }
    }
    grocery_print(&grocery);
    return 0;
}
''',
"csharp": '''public class Grocery {
    private readonly int _numOfItems;
    private readonly List<string> _items = new List<string>();

    public Grocery(int numOfItems) {
        _numOfItems = numOfItems;
    }

    public bool AddItem(string item) {
        if (_items.Contains(item)) return false;
        _items.Add(item);
        return true;
    }

    public override string ToString() {
        return "Grocery items: " + string.Join(", ", _items);
    }
}

public static void Main(string[] args) {
    Console.Write("Enter How Many Items: ");
    int numOfItems;
    try {
        numOfItems = int.Parse(Console.ReadLine().Trim());
    } catch (FormatException) {
        Console.Write("Number of items you entered is invalid!");
        return;
    }
    Grocery grocery = new Grocery(numOfItems);
    for (int i = 0; i < numOfItems; i++) {
        Console.Write("Enter Item " + (i + 1) + " : ");
        if (!grocery.AddItem(Console.ReadLine())) {
            Console.WriteLine("First Item Duplicate Detected!");
            return;
        }
    }
    Console.WriteLine(grocery.ToString());
}
'''
},
"T139": {
"python": '''def solution(X, A):
    empty_position = set(range(1, X + 1))
    for i in range(len(A)):
        empty_position.discard(A[i])
        if not empty_position:
            return i
    return -1
''',
"c": r'''int solution(int X, const int *A, int n) {
    int *present = calloc((size_t) X + 1, sizeof(int));
    int remaining = X;
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
''',
"csharp": '''public static int Solution(int X, int[] A) {
    var emptyPosition = new HashSet<int>(Enumerable.Range(1, X));
    for (int i = 0; i < A.Length; i++) {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0) return i;
    }
    return -1;
}
'''
},
"T247": {
"python": '''def main():
    print("Enter the String", end="")
    text = input()
    counts = {}
    for ch in text:
        counts[ord(ch)] = counts.get(ord(ch), 0) + 1
    for code in range(256):
        if counts.get(code, 0) > 0:
            if counts[code] == 1:
                print(chr(code), end="")
            else:
                print(chr(code) + str(counts[code]), end="")
''',
"c": r'''int main(void) {
    printf("Enter the String");
    char st[1024];
    if (fgets(st, sizeof(st), stdin) == NULL) return 0;
    st[strcspn(st, "\n")] = '\0';
    int ar[256] = {0};
    for (int i = 0; st[i] != '\0'; i++) {
        ar[(unsigned char) st[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar[i] > 0) {
            if (ar[i] == 1) printf("%c", ch);
            else printf("%c%d", ch, ar[i]);
        }
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    var ar = new Dictionary<int, int>();
    foreach (char ch in st) {
        int code = ch;
        if (ar.ContainsKey(code)) ar[code]++;
        else ar[code] = 1;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar.TryGetValue(i, out int n)) {
            if (n == 1) Console.Write(ch);
            else Console.Write(ch.ToString() + n);
        }
    }
}
'''
},
"T33": {
"python": '''def get_rows(i, j, array):
    another = [None] * (j - i + 1)
    while i <= j:
        for k in range(len(another)):
            another[k] = array[i]
            i += 1
    return another
''',
"c": r'''int **getRows(int i, int j, int **array) {
    int rows = j - i + 1;
    int **another = malloc(sizeof(int *) * (size_t) rows);
    while (i <= j) {
        for (int k = 0; k < rows; k++) {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
''',
"csharp": '''public static int[][] GetRows(int i, int j, int[][] array) {
    int[][] another = new int[j - i + 1][];
    while (i <= j) {
        for (int k = 0; k < another.Length; k++) {
            another[k] = array[i];
            i++;
        }
    }
    return another;
}
'''
},
"T158": {
"python": '''def solution(X, A):
    empty_position = set(range(1, X + 1))
    for i, value in enumerate(A):
        empty_position.discard(value)
        if len(empty_position) == 0:
            return i
    return -1
''',
"c": r'''int solution(int X, const int *A, int n) {
    int *present = calloc((size_t) X + 2, sizeof(int));
    for (int v = 1; v <= X; v++) {
        present[v] = 1;
    }
    int remaining = X;
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
''',
"csharp": '''public static int Solution(int X, int[] A) {
    var emptyPosition = new HashSet<int>();
    for (int v = 1; v <= X; v++) {
        emptyPosition.Add(v);
    }
    for (int i = 0; i < A.Length; i++) {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0) {
            return i;
        }
    }
    return -1;
}
'''
},
"T445": {
"python": '''LETTER_PRIMES = {
    'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19,
    'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53,
    'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89,
    'y': 97, 'z': 101
}

def word_prime_map():
    return LETTER_PRIMES

def is_anagram(word, anagram_word):
    if len(word) != len(anagram_word):
        return False
    primes = word_prime_map()
    words_char_num = 1
    anagram_word_num = 1
    for ch in word:
        words_char_num *= primes[ch]
    for ch in anagram_word:
        anagram_word_num *= primes[ch]
    return anagram_word_num == words_char_num
''',
"c": r'''static const int LETTER_PRIMES[26] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101};

static int wordPrimeMap(char c) {
    return LETTER_PRIMES[c - 'a'];
}

int isAnagram(const char *word, const char *anagram_word) {
    if (strlen(word) != strlen(anagram_word)) return 0;
    unsigned long long words_char_num = 1;
    unsigned long long anagram_word_num = 1;
    for (const char *p = word; *p; p++) {
        words_char_num *= (unsigned long long) wordPrimeMap(*p);
    }
    for (const char *p = anagram_word; *p; p++) {
        anagram_word_num *= (unsigned long long) wordPrimeMap(*p);
    }
    return anagram_word_num == words_char_num;
}
''',
"csharp": '''private static readonly Dictionary<char, int> WordPrimeMap = new Dictionary<char, int> {
    {'a', 2}, {'b', 3}, {'c', 5}, {'d', 7}, {'e', 11}, {'f', 13}, {'g', 17}, {'h', 19},
    {'i', 23}, {'j', 29}, {'k', 31}, {'l', 37}, {'m', 41}, {'n', 43}, {'o', 47}, {'p', 53},
    {'q', 59}, {'r', 61}, {'s', 67}, {'t', 71}, {'u', 73}, {'v', 79}, {'w', 83}, {'x', 89},
    {'y', 97}, {'z', 101}
};

public static bool IsAnagram(string word, string anagram_word) {
    if (word.Length != anagram_word.Length) return false;
    long wordsCharNum = 1;
    long anagramWordNum = 1;
    foreach (char c in word) {
        wordsCharNum *= WordPrimeMap[c];
    }
    foreach (char c in anagram_word) {
        anagramWordNum *= WordPrimeMap[c];
    }
    return anagramWordNum == wordsCharNum;
}
'''
},
"T826": {
"python": '''import subprocess

def main(args):
    process = subprocess.Popen([args[0]], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end="")
    print("Program terminated!")
    process.wait()
''',
"c": r'''int main(int argc, char **argv) {
    (void) argc;
    FILE *fp = popen(argv[1], "r");
    if (fp == NULL) return 1;
    char line[1024];
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("%s", line);
    }
    printf("Program terminated!\n");
    pclose(fp);
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    var startInfo = new ProcessStartInfo(args[0]) {
        RedirectStandardOutput = true,
        UseShellExecute = false
    };
    using (Process process = Process.Start(startInfo)) {
        using (StreamReader reader = process.StandardOutput) {
            string line;
            while ((line = reader.ReadLine()) != null) {
                Console.WriteLine(line);
            }
        }
        Console.WriteLine("Program terminated!");
    }
}
'''
},
"T774": {
"python": '''def main():
    password = "admin"
    print("Insert the admin pass: ", end="")
    test = input()
    if password == test:
        print("Access granted", end="")
    else:
        for i in range(1, 3):
            print("You have " + str(i) + " try(es): ", end="")
            test = input()
            if password == test:
                print("Access granted", end="")
                break
            elif i == 2:
                print("Access denied", end="")
''',
"c": r'''int main(void) {
    const char *pass = "admin";
    char test[128];
    printf("Insert the admin pass: ");
    if (fgets(test, sizeof(test), stdin) == NULL) return 0;
    test[strcspn(test, "\n")] = '\0';
    if (strcmp(pass, test) == 0) {
        printf("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            printf("You have %d try(es): ", i);
            if (fgets(test, sizeof(test), stdin) == NULL) return 0;
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
"csharp": '''public static void Main(string[] args) {
    string pass = "admin";
    Console.Write("Insert the admin pass: ");
    string test = Console.ReadLine();
    if (pass.Equals(test)) {
        Console.Write("Access granted");
    } else {
        for (int i = 1; i < 3; i++) {
            Console.Write("You have " + i + " try(es): ");
            test = Console.ReadLine();
            if (pass.Equals(test)) {
                Console.Write("Access granted");
                break;
            } else if (i == 2) {
                Console.Write("Access denied");
            }
        }
    }
}
'''
},
"T729": {
"python": '''CHARACTER_MAPPING = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

def solution(S, P, Q):
    character_input = list(S)
    integer_input = [CHARACTER_MAPPING[ch] for ch in character_input]
    result = [0] * len(P)
    for index in range(len(P)):
        if P[index] == Q[index]:
            result[index] = integer_input[P[index]]
            break
        result[index] = min(integer_input[P[index]:Q[index] + 1])
    return result
''',
"c": r'''int character_mapping(char c) {
    switch (c) {
        case 'A': return 1;
        case 'C': return 2;
        case 'G': return 3;
        case 'T': return 4;
    }
    return 0;
}

int *solution(const char *S, const int *P, const int *Q, int m) {
    int len = (int) strlen(S);
    int *integer_input = malloc(sizeof(int) * (size_t) len);
    for (int i = 0; i < len; i++) {
        integer_input[i] = character_mapping(S[i]);
    }
    int *result = calloc((size_t) m, sizeof(int));
    for (int index = 0; index < m; index++) {
        if (P[index] == Q[index]) {
            result[index] = integer_input[P[index]];
            break;
        }
        int minVal = integer_input[P[index]];
        for (int i = P[index] + 1; i <= Q[index]; i++) {
            if (integer_input[i] < minVal) minVal = integer_input[i];
        }
        result[index] = minVal;
    }
    free(integer_input);
    return result;
}
''',
"csharp": '''private static readonly Dictionary<char, int> CharacterMapping = new Dictionary<char, int> {
    {'A', 1}, {'C', 2}, {'G', 3}, {'T', 4}
};

public static int[] Solution(string S, int[] P, int[] Q) {
    var integerInput = S.Select(c => CharacterMapping[c]).ToArray();
    int[] result = new int[P.Length];
    for (int index = 0; index < P.Length; index++) {
        if (P[index] == Q[index]) {
            result[index] = integerInput[P[index]];
            break;
        }
        result[index] = integerInput.Skip(P[index]).Take(Q[index] - P[index] + 1).Min();
    }
    return result;
}
'''
},
"T126": {
"python": '''def solution(X, A):
    leaves = set()
    for i in range(len(A)):
        leaves.add(A[i])
        if X in leaves and len(leaves) == X:
            return i
    return -1
''',
"c": r'''int solution(int X, const int *A, int n) {
    int *seen = calloc((size_t) X + 1, sizeof(int));
    int distinct = 0;
    int hasX = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] >= 1 && A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
            if (A[i] == X) hasX = 1;
        }
        if (hasX && distinct == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
''',
"csharp": '''public static int Solution(int X, int[] A) {
    var leaves = new HashSet<int>();
    for (int i = 0; i < A.Length; i++) {
        leaves.Add(A[i]);
        if (leaves.Contains(X) && leaves.Count == X) return i;
    }
    return -1;
}
'''
},
}
