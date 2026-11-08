PART = []

PART.append({"id": "R1ab11e56ab", "task": "refactor", "output": r'''def future6(A):
    known = []
    result = []
    for idx in reversed(range(len(A))):
        value = A [idx]
        kept = []
        for x, y in known:
            if y > value:
                kept.append((x, y))
        known = kept
        if known:
            result.append(known [-1] [0])
        else:
            result.append(-1)
        known.append((idx, value))
    result.reverse()
    return np.array(result)'''})

PART.append({"id": "Rfbf7d4f5c2", "task": "refactor", "output": r'''def stemming(verb):
    suffixes = ['ing', 'ed', 'es', 's']
    kept = []
    for ch in verb:
        if ch not in suffixes:
            kept.append(ch)
    return ''.join(kept)'''})

PART.append({"id": "Rd908836b46", "task": "refactor", "output": r'''static void allocate_strings (char **arr, int count, int size) {
    for (int i = 0; i < count; i ++) {
        arr [i] = malloc (size);
    }
}

int main (void) {
    char *a [50];
    allocate_strings (a, 50, 10);
    function (a);
    int i = 0;
    while (i < 2) {
        printf ("a [%d]: %s\n", i, a [i]);
        i ++;
    }
}'''})

PART.append({"id": "R63b6384687", "task": "refactor", "output": r'''def merge(a, low, mid, high):
    left = a [low : mid + 1]
    right = a [mid + 1 : high + 1]
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left [i] <= right [j]:
            merged.append(left [i])
            i += 1
        else:
            merged.append(right [j])
            j += 1
    merged.extend(left [i :])
    merged.extend(right [j :])
    a [low : high + 1] = merged'''})

PART.append({"id": "R06eb22ea20", "task": "refactor", "output": r'''public static void d (Exception e) {
    try {
        MethodBase site = e.TargetSite;
        string methodName = ExtractBracketed (site == null ? "" : site.Name);
        StackTrace stkTrace = new System.Diagnostics.StackTrace (e, true);
        for (int i = 0; i < 3; i ++) {
            if (LogExceptionFrame (stkTrace.GetFrame (i), methodName, e)) {
                break;
            }
        }
    }
    catch (Exception ee) {
        Console.WriteLine ("Tracing exception in d(Exception e)" + ee.Message);
    }
}

private static bool LogExceptionFrame (StackFrame frame, string methodName, Exception e) {
    int lineNum = frame.GetFileLineNumber ();
    int colNum = frame.GetFileColumnNumber ();
    string className = ExtractBracketed (frame.GetMethod ().ReflectedType.FullName);
    Trace.WriteLine (ThreadAndDateInfo + "Exception: " + className + "." + methodName + ", Ln " + lineNum + " Col " + colNum + ": " + e.Message);
    return lineNum + colNum > 0;
}'''})

PART.append({"id": "Reb0aa16636", "task": "refactor", "output": r'''bool isPrime (int number) {
    if (number < 2 || (number != 2 && number % 2 == 0)) {
        return false;
    }
    int i = 3;
    while (i * i <= number) {
        if (number % i == 0) {
            return false;
        }
        i += 2;
    }
    return number >= 2;
}'''})

PART.append({"id": "Rcfc9023e76", "task": "refactor", "output": r'''public static void main (String [] args) {
    Scanner input = new Scanner (System.in);
    System.out.println ("Enter a number");
    String number = input.nextLine ();
    boolean even = false;
    int total = 0;
    for (char digitChar : number.toCharArray ()) {
        int a = Integer.parseInt (String.valueOf (digitChar));
        if (a % 2 != 0 || a == 1) {
            even = false;
            total += a;
        }
    }
    System.out.println ("The sum is " + total);
}'''})

PART.append({"id": "R7176808dc7", "task": "refactor", "output": r'''protected override void CalculateBiQuadCoefficients () {
    double k = Math.Tan (Math.PI * Frequency / SampleRate);
    double normDenom = 1 / (1 + k / Q + k * k);
    A0 = k / Q * normDenom;
    A1 = 0;
    A2 = -A0;
    B1 = 2 * (k * k - 1) * normDenom;
    B2 = (1 - k / Q + k * k) * normDenom;
}'''})

PART.append({"id": "R5e98c898ba", "task": "refactor", "output": r'''int main (int argC, char *argV []) {
    char *name = malloc (MAX_NAME_SZ);
    if (name == NULL) {
        printf ("No memory\n");
        return 1;
    }
    printf ("What is your name? ");
    if (fgets (name, MAX_NAME_SZ, stdin) == NULL) {
        name [0] = '\0';
    }
    size_t len = strlen (name);
    if (len > 0 && name [len - 1] == '\n') {
        name [len - 1] = '\0';
    }
    printf ("Hello %s. Nice to meet you.\n", name);
    free (name);
    return 0;
}'''})
