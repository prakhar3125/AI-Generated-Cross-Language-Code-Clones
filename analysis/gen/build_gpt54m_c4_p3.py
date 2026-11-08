DATA_T3 = {}

DATA_T3["T229"] = {"outputs": {
"python": """import threading

lock = threading.Condition()


def run(self):
    with lock:
        try:
            for i in range(5):
                while id != token % N:
                    lock.wait()
                print(str(id) + " " + str(i))
                token += 1
                lock.notify_all()
        except RuntimeError as e:
            traceback.print_exc()
""",
"c": """pthread_mutex_t lock_m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t lock_c = PTHREAD_COND_INITIALIZER;

void *run(void *arg) {
    pthread_mutex_lock(&lock_m);
    for (int i = 0; i < 5; i++) {
        while (id != token % N)
            pthread_cond_wait(&lock_c, &lock_m);
        printf("%d %d\\n", id, i);
        token++;
        pthread_cond_broadcast(&lock_c);
    }
    pthread_mutex_unlock(&lock_m);
    return NULL;
}
""",
"csharp": """public void Run() {
    try {
        lock (lockObj) {
            Monitor.Wait(lockObj);
            for (int i = 0; i < 5; i++) {
                while (id != token % N) Monitor.Wait(lockObj);
                Console.WriteLine(id + " " + i);
                token++;
                Monitor.PulseAll(lockObj);
            }
        }
    } catch (ThreadInterruptedException e) {
        Console.Error.WriteLine(e.StackTrace);
    }
}
"""}}

DATA_T3["T147"] = {"outputs": {
"python": """def solution(x, a):
    remaining = set(range(1, x + 1))
    for i, value in enumerate(a):
        remaining.discard(value)
        if not remaining:
            return i
    return -1
""",
"c": """int solution(int X, int A[], int len) {
    char *present = calloc(X + 2, 1);
    int filled = 0;
    for (int i = 0; i < len; i++) {
        if (A[i] >= 1 && A[i] <= X && !present[A[i]]) {
            present[A[i]] = 1;
            filled++;
        }
        if (filled == X) {
            free(present);
            return i;
        }
    }
    free(present);
    return -1;
}
""",
"csharp": """public int Solution(int X, int[] A) {
    var emptyPosition = new HashSet<int>(Enumerable.Range(1, X));
    for (int i = 0; i < A.Length; i++) {
        emptyPosition.Remove(A[i]);
        if (emptyPosition.Count == 0) return i;
    }
    return -1;
}
"""}}

DATA_T3["T124"] = {"outputs": {
"python": """def solution(x, a):
    length = len(a)
    if x > length:
        return -1
    filled = [0] * x
    jumped = 0
    for i, pos in enumerate(a):
        if pos <= x and filled[pos - 1] == 0:
            filled[pos - 1] = 1
            jumped += 1
            if jumped == x:
                return i
    return -1
""",
"c": """int solution(int X, int A[], int len) {
    if (X > len) return -1;
    int *isFilled = calloc(X, sizeof(int));
    int jumped = 0;
    for (int i = 0; i < len; i++) {
        int x = A[i];
        if (x <= X && isFilled[x - 1] == 0) {
            isFilled[x - 1] = 1;
            jumped++;
            if (jumped == X) {
                free(isFilled);
                return i;
            }
        }
    }
    free(isFilled);
    return -1;
}
""",
"csharp": """public int Solution(int X, int[] A) {
    if (X > A.Length) return -1;
    var isFilled = new bool[X];
    int jumped = 0;
    for (int i = 0; i < A.Length; i++) {
        int x = A[i];
        if (x <= X && !isFilled[x - 1]) {
            isFilled[x - 1] = true;
            jumped++;
            if (jumped == X) return i;
        }
    }
    return -1;
}
"""}}

DATA_T3["T614"] = {"outputs": {
"python": """def filter(self, source, start, end, dest, dstart, dend):
    ls_start = ""
    ls_insert = ""
    ls_end = ""
    log_debug("debug", str(self.pattern))
    log_debug("debug", "source: " + str(source) + ", start: " + str(start) + ", end:" + str(end)
              + ", dest: " + str(dest) + ", dstart: " + str(dstart) + ", dend: " + str(dend))
    ls_text = str(dest)
    if len(ls_text) > 0:
        ls_start = ls_text[:dstart]
        log_debug("debug", "lsStart : " + ls_start)
        if source != "":
            ls_insert = str(source)
            log_debug("debug", "lsInsert: " + ls_insert)
        ls_end = ls_text[dend:]
        log_debug("debug", "lsEnd   : " + ls_end)
        ls_text = ls_start + ls_insert + ls_end
        log_debug("debug", "lsText  : " + ls_text)
    matcher = self.pattern.fullmatch(ls_text)
    log_debug("debug", "matches: " + str(matcher is not None) + ", lsText: " + ls_text)
    return "" if matcher is None else None
""",
"c": """char *filter(const char *source, int start, int end,
             const char *dest, int dstart, int dend) {
    static char ls_text[512];
    char ls_start[512], ls_insert[512], ls_end[512], msg[512];
    log_debug("debug", pattern_to_string());
    ls_text[0] = '\\0';
    strncpy(ls_text, dest, sizeof(ls_text) - 1);
    if (strlen(ls_text) > 0) {
        strncpy(ls_start, ls_text, dstart);
        ls_start[dstart] = '\\0';
        if (source[0] != '\\0') {
            strncpy(ls_insert, source, sizeof(ls_insert) - 1);
        }
        strcpy(ls_end, ls_text + dend);
        snprintf(ls_text, sizeof(ls_text), "%s%s%s", ls_start, ls_insert, ls_end);
    }
    if (!pattern_matches_full(ls_text)) {
        return "";
    }
    return NULL;
}
""",
"csharp": """public CharSequence Filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
    string lsStart = "";
    string lsInsert = "";
    string lsEnd = "";
    string lsText = "";
    Log.Debug("debug", moPattern.ToString());
    lsText = dest.ToString();
    if (lsText.Length > 0) {
        lsStart = lsText.Substring(0, dstart);
        if (source != "") {
            lsInsert = source.ToString();
        }
        lsEnd = lsText.Substring(dend);
        lsText = lsStart + lsInsert + lsEnd;
    }
    bool matches = moPattern.IsMatch(lsText);
    if (!matches) {
        return "";
    }
    return null;
}
"""}}

DATA_T3["T592"] = {"outputs": {
"python": """def rand_nums(self, total, n):
    results = [0] * n
    if total == 0:
        return results
    total_plus_1 = total + 1
    while True:
        rs = [secrets.randbits(256) for _ in range(n)]
        total_sum = sum(rs)
        if total_sum == 0:
            continue
        for i in range(n):
            results[i] = (total_sum % rs[i]) % total_plus_1
        return results
""",
"c": """void rand_nums(int total, int n, int results[]) {
    unsigned long long rs[64];
    unsigned long long totalPlus1 = (unsigned long long) total + 1;
    if (total == 0) {
        for (int i = 0; i < n; i++) results[i] = 0;
        return;
    }
    while (1) {
        unsigned long long sum = 0;
        for (int i = 0; i < n; i++) {
            rs[i] = ((unsigned long long) rand() << 32) | rand();
            sum += rs[i];
        }
        if (sum == 0) continue;
        for (int i = 0; i < n; i++) {
            results[i] = (int) ((sum % rs[i]) % totalPlus1);
        }
        return;
    }
}
""",
"csharp": """private int[] RandNums(int total, int n) {
    var results = new int[n];
    if (total == 0) {
        return results;
    }
    var rs = new System.Numerics.BigInteger[n];
    var totalPlus1 = new System.Numerics.BigInteger(total + 1L);
    while (true) {
        for (int i = 0; i < n; ++i) {
            rs[i] = new System.Numerics.BigInteger(256, rand);
        }
        var sum = System.Numerics.BigInteger.Zero;
        foreach (var r in rs) {
            sum = sum.Add(r);
        }
        if (sum.CompareTo(System.Numerics.BigInteger.Zero) == 0) {
            continue;
        }
        for (int i = 0; i < n; ++i) {
            results[i] = (int) (sum.Mod(rs[i]).Mod(totalPlus1));
        }
        return results;
    }
}
"""}}
