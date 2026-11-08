DATA7 = {
"Re6ed6fb8d3": r"""public static IEnumerable < T > TakeLast < T > (this IEnumerable < T > input, int count) {
    if (count <= 0) yield break;
    if (input is IList < T > inputList) {
        int start = Math.Max (0, inputList.Count - count);
        for (int index = start; index < inputList.Count; index ++) {
            yield return inputList [index];
        }
        yield break;
    }
    var queue = new Queue < T > (count);
    foreach (T item in input) {
        if (queue.Count == count) queue.Dequeue ();
        queue.Enqueue (item);
    }
    foreach (T item in queue) {
        yield return item;
    }
}""",
"Rc93ef31bfe": r'''def matched(s):
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0''',
"R077660cd40": r"""static void report (int numLetters, int numWords) {
    if (numWords == 0) {
        printf ("You didn't enter any words\n");
        return;
    }
    printf ("Average word length: %.1f (C = %d, N = %d)\n", numLetters / (float) numWords, numLetters, numWords);
}

int main (void) {
    int ch;
    int numWords = 0;
    int numLetters = 0;
    int prevWasASpace = 1;
    printf ("Enter a sentence: ");
    while ((ch = getchar ()) != EOF && ch != '\n') {
        if (ch != ' ') {
            numWords += prevWasASpace;
            prevWasASpace = 0;
            numLetters++;
        } else {
            prevWasASpace = 1;
        }
    }
    report (numLetters, numWords);
    return 0;
}""",
"R076547cbe5": r"""public static bool IsWindowOnAnyScreen(Window Window, short WindowSizeX, short WindowSizeY, bool AutoAdjustWindow) {
    var screen = System.Windows.Forms.Screen.FromHandle(new WindowInteropHelper(Window).Handle);
    if (Window.Left >= screen.WorkingArea.Left
        && Window.Top >= screen.WorkingArea.Top
        && Window.Top + WindowSizeY <= screen.WorkingArea.Bottom
        && Window.Left + WindowSizeX <= screen.WorkingArea.Right) {
        return true;
    }
    if (AutoAdjustWindow) {
        if (Window.Left < screen.WorkingArea.Left)
            Window.Left = screen.WorkingArea.Left;
        if (Window.Top < screen.WorkingArea.Top)
            Window.Top = screen.WorkingArea.Top;
        if (Window.Top + WindowSizeY > screen.WorkingArea.Bottom)
            Window.Top -= (Window.Top + WindowSizeY) - screen.WorkingArea.Bottom;
        if (Window.Left + WindowSizeX > screen.WorkingArea.Right)
            Window.Left -= (Window.Left + WindowSizeX) - screen.WorkingArea.Right;
    }
    return false;
}""",
"Rb740b5ce4e": r"""int main () {
    int blah = 1;
    void *chain [9];
    chain [0] = &blah;
    for (int level = 1; level < 9; level ++) {
        chain [level] = &chain [level - 1];
    }
    mega_pointer ((int *********) chain [8]);
    return 0;
}""",
"R2d627295b4": r'''from sklearn.linear_model import LinearRegression
import numpy as np

class MyLinearRegression(LinearRegression):
    def fit(self, X, y, n_jobs=1):
        super().fit(X, y, n_jobs)
        ssr = self._residual_ssr(X, y)
        xtx_inv = np.linalg.inv(np.dot(X.T, X))
        serr = np.sqrt(np.diagonal(ssr[:, None] * xtx_inv))
        self.t = self.coef_ / serr

    def _residual_ssr(self, X, y):
        residual = (self.predict(X) - y) ** 2
        return np.sum(residual, axis=0) / float(X.shape[0] - X.shape[1])''',
"R27ef16612d": r"""int main () {
    int a [50] = {1, 2, -3, 0, 0, 6, 7, -8, 0, SENTINEL};
    int count = 0;
    int *p = a;
    while (*p != SENTINEL) {
        if (*p != 0) count++;
        p++;
    }
    printf ("Total Element :%d ", count);
    return 0;
}""",
"R80bf6ba91c": r"""public static void main (final String [] args) throws IOException {
    BufferedReader br = new BufferedReader (new InputStreamReader (System.in));
    System.out.println ("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    String input;
    while (! isExitCommand (input = br.readLine ())) {
        System.out.println ("...response goes here...");
    }
    System.out.println ("Exiting.");
}

private static boolean isExitCommand (String input) {
    System.out.print ("><![CDATA[ ");
    System.out.println (input);
    return input.length () == EXIT_COMMAND.length () && input.toLowerCase ().equals (EXIT_COMMAND);
}""",
"R5813b54ca5": r"""static double integrand (double t) {
    return fabs (pow (t, 2) + 4);
}

int main () {
    double integralSum = 0;
    for (int i = 1; i <= parts; ++i) {
        integralSum += step * integrand (x + step * i);
    }
    printf ("%f\n", integralSum);
    return 0;
}""",
"R14e363aee6": r"""public static void Main () {
    string baseIP = "192.168.1.";
    Console.WriteLine ("Pinging 255 destinations of D-class in {0}*", baseIP);
    CreatePingers (255);
    PingOptions po = new PingOptions (ttl, true);
    byte [] data = new System.Text.ASCIIEncoding ().GetBytes ("abababababababababababababababab");
    int cnt = 1;
    Stopwatch watch = Stopwatch.StartNew ();
    pingers.ToList ().ForEach (p => {
        lock (@lock) {
            instances += 1;
        }
        p.SendAsync (string.Concat (baseIP, cnt.ToString ()), timeOut, data, po);
        cnt += 1;
    });
    while (instances > 0) {
        new SpinWait ().SpinOnce ();
    }
    watch.Stop ();
    DestroyPingers ();
    Console.WriteLine ("Finished in {0}. Found {1} active IP-addresses.", watch.Elapsed.ToString (), result);
    Console.ReadKey ();
}""",
"R9582f81645": r'''def __init__(self, a=None, b=None, **kwargs):
    self.relations = {
        "e": {"req": ["a", "b"], "func": lambda a, b: a + b},
        "C": {"req": ["e", "a"], "func": lambda e, a: e * 1 / (a * b)},
        "A": {"req": ["C", "e"], "func": lambda e, C: cmplx_func_A(e, C)},
        "a": {"req": ["e", "b"], "func": lambda e, b: e / b},
        "b": {"req": ["e", "a"], "func": lambda e, a: e / a},
    }
    self.a, self.b = a, b
    self.e = self.C = self.A = None
    for key, value in kwargs.items():
        setattr(self, key, value)''',
"Rcc630548aa": r"""public IDisposable Enter (string key) {
    Locker locker = GetOrCreateLocker (key);
    locker.Enter ();
    locker.WaitCount --;
    return locker;
}

private Locker GetOrCreateLocker (string key) {
    lock (this.globalLock) {
        Locker locker;
        if (! this.locks.TryGetValue (key, out locker)) {
            locker = new Locker (this, key);
            this.locks [key] = locker;
        }
        locker.WaitCount ++;
        return locker;
    }
}""",
"R8868947157": r"""int main (void) {
    char first [25];
    int index = 0, n;
    printf ("Enter the number of last names :\n");
    scanf ("%d", & n);
    printf ("Enter the first name \n");
    scanf ("%s", first);
    char last [n] [25];
    for (int i = 0; i < n; i++) {
        scanf ("%s", last [i]);
        if (strcmp (last [i], first) == 0)
            index++;
    }
    printf (index == 0 ? "First name not repeated\n" : "First name repeated %d times", index);
    return 0;
}""",
}
