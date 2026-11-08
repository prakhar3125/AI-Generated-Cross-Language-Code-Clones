DATA_R2 = {
"Rc93ef31bfe": '''def matched(s):
    depth = 0
    for i in range(len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0''',
"R077660cd40": '''#include <stdio.h>

int main(void) {
    int ch;
    int numWords = 0;
    int numLetters = 0;
    int inWord = 0;
    printf("Enter a sentence: ");
    while ((ch = getchar()) != EOF && ch != '\\n') {
        if (ch == ' ') {
            inWord = 0;
        } else {
            numLetters++;
            if (!inWord) {
                numWords++;
                inWord = 1;
            }
        }
    }
    if (numWords > 0) {
        double avg = numLetters / (float)(numWords);
        printf("Average word length: %.1f (C = %d, N = %d)\\n", avg, numLetters, numWords);
    }
    else
        printf("You didn't enter any words\\n");
    return 0;
}''',
"R076547cbe5": '''public static bool IsWindowOnAnyScreen(Window Window, short WindowSizeX, short WindowSizeY, bool AutoAdjustWindow) {
    var Screen = System.Windows.Forms.Screen.FromHandle(new WindowInteropHelper(Window).Handle);
    bool fitsHorizontally = (Window.Left >= Screen.WorkingArea.Left) && ((Window.Left + WindowSizeX) <= Screen.WorkingArea.Right);
    bool fitsVertically = (Window.Top >= Screen.WorkingArea.Top) && ((Window.Top + WindowSizeY) <= Screen.WorkingArea.Bottom);
    if (fitsHorizontally && fitsVertically)
        return true;
    if (AutoAdjustWindow) {
        if (Window.Left + WindowSizeX > Screen.WorkingArea.Right)
            Window.Left = Screen.WorkingArea.Right - WindowSizeX;
        else if (Window.Left < Screen.WorkingArea.Left)
            Window.Left = Screen.WorkingArea.Left;
        if (Window.Top + WindowSizeY > Screen.WorkingArea.Bottom)
            Window.Top = Screen.WorkingArea.Bottom - WindowSizeY;
        else if (Window.Top < Screen.WorkingArea.Top)
            Window.Top = Screen.WorkingArea.Top;
    }
    return false;
}''',
"Rb740b5ce4e": '''int main() {
    int blah = 1;
    void *levels[9];
    levels[0] = &blah;
    for (int i = 1; i < 9; i++) {
        levels[i] = &levels[i - 1];
    }
    mega_pointer((int *********)levels[8]);
    return 0;
}''',
"R2d627295b4": '''from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats


class MyLinearRegression(LinearRegression):
    def fit(self, X, y, n_jobs=1):
        super().fit(X, y, n_jobs)
        residual = (self.predict(X) - y) ** 2
        ssr = np.sum(residual, axis=0) / float(X.shape[0] - X.shape[1])
        self.t = self.coef_ / self._standard_errors(ssr, X)

    @staticmethod
    def _standard_errors(ssr, X):
        inv = np.linalg.inv(np.dot(X.T, X))
        return np.array([np.sqrt(np.diagonal(ssr[i] * inv)) for i in range(ssr.shape[0])])''',
"R27ef16612d": '''int main() {
    int a[50] = {1, 2, -3, 0, 0, 6, 7, -8, 0, SENTINEL};
    int count = 0;
    int *p = a;
    while (*p != SENTINEL) {
        count += (*p != 0);
        p++;
    }
    printf("Total Element :%d ", count);
    return 0;
}''',
"R80bf6ba91c": '''public static void main(final String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    System.out.println("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    while (true) {
        System.out.print("><![CDATA[ ");
        String input = br.readLine();
        System.out.println(input);
        if (isExitCommand(input)) {
            System.out.println("Exiting.");
            return;
        }
        System.out.println("...response goes here...");
    }
}

private static boolean isExitCommand(String input) {
    return input.length() == EXIT_COMMAND.length() && input.toLowerCase().equals(EXIT_COMMAND);
}''',
"R5813b54ca5": '''int main() {
    double integralSum = 0;
    int i;
    for (i = 1; i < (parts + 1); ++i) {
        integralSum += step * integrand(x + (step * i));
    }
    printf("%f\\n", integralSum);
    return 0;
}

static double integrand(double x) {
    return fabs(pow(x, 2) + 4);
}''',
"R14e363aee6": '''public static void Main() {
    string baseIP = "192.168.1.";
    Console.WriteLine("Pinging 255 destinations of D-class in {0}*", baseIP);
    CreatePingers(255);
    PingOptions po = new PingOptions(ttl, true);
    System.Text.ASCIIEncoding enc = new System.Text.ASCIIEncoding();
    byte[] data = enc.GetBytes("abababababababababababababababab");
    int cnt = 1;
    Stopwatch watch = Stopwatch.StartNew();
    foreach (Ping p in pingers) {
        SendOne(p, baseIP, cnt, timeOut, data, po);
        cnt += 1;
    }
    WaitPingers();
    watch.Stop();
    DestroyPingers();
    Console.WriteLine("Finished in {0}. Found {1} active IP-addresses.", watch.Elapsed.ToString(), result);
    Console.ReadKey();
}

private static void SendOne(Ping p, string baseIP, int cnt, int timeOut, byte[] data, PingOptions po) {
    lock (@lock) {
        instances += 1;
    }
    p.SendAsync(string.Concat(baseIP, cnt.ToString()), timeOut, data, po);
}

private static void WaitPingers() {
    SpinWait wait = new SpinWait();
    while (instances > 0) {
        wait.SpinOnce();
    }
}''',
"R9582f81645": '''def __init__(self, a=None, b=None, **kwargs):
    self.relations = {
        "e": {"req": ["a", "b"], "func": lambda a, b: a + b},
        "C": {"req": ["e", "a"], "func": lambda e, a: e * 1 / (a * b)},
        "A": {"req": ["C", "e"], "func": lambda e, C: cmplx_func_A(e, C)},
        "a": {"req": ["e", "b"], "func": lambda e, b: e / b},
        "b": {"req": ["e", "a"], "func": lambda e, a: e / a}}
    self.a = a
    self.b = b
    for name in ("e", "C", "A"):
        setattr(self, name, None)
    for key, value in kwargs.items():
        setattr(self, key, value)''',
"Rcc630548aa": '''public IDisposable Enter(string key) {
    Locker locker = ObtainLocker(key);
    locker.WaitCount++;
    locker.Enter();
    locker.WaitCount--;
    return locker;
}

private Locker ObtainLocker(string key) {
    Locker locker;
    lock (this.globalLock) {
        if (!this.locks.TryGetValue(key, out locker)) {
            this.locks[key] = locker = new Locker(this, key);
        }
    }
    return locker;
}''',
"R8868947157": '''#include <stdio.h>
#include <string.h>

int main(void) {
    char first[25];
    int index = 0, n;
    printf("Enter the number of last names :\\n");
    scanf("%d", &n);
    printf("Enter the first name \\n");
    scanf("%s", first);
    char last[n][25];
    for (int i = 0; i < n; i++)
        scanf("%s", last[i]);
    int j = 0;
    while (j < n) {
        index += (strcmp(last[j], first) == 0);
        j++;
    }
    if (index == 0)
        printf("First name not repeated\\n");
    else
        printf("First name repeated %d times", index);
    return 0;
}'''
}
