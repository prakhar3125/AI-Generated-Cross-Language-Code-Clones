DATA_R4 = {
"R106ccba12f": r'''
public static IList ToAnonymousList(this IEnumerable enumerable)
{
    var list = new List<object>();
    foreach (var item in enumerable)
    {
        list.Add(item);
    }
    if (list.Count == 0)
        throw new Exception("?? No elements??");
    var typed = (IList)Activator.CreateInstance(typeof(List<>).MakeGenericType(list[0].GetType()));
    foreach (var item in list)
        typed.Add(item);
    return typed;
}
''',
"R3968bf5162": r'''
public void run () {
    int i = 1;
    while (i < 50) {
        waitForState(s, 3);
        synchronized (s) {
            if (s.getState () == 3) {
                System.out.println ("t1 " + i);
            }
            s.setState (1);
            i += 3;
            s.notifyAll ();
        }
    }
}

private static void waitForState (SharedState s, int wanted) {
    synchronized (s) {
        while (s.getState () != wanted) {
            try {
                s.wait ();
            } catch (InterruptedException e) {
                e.printStackTrace ();
            }
        }
    }
}
''',
"R3d67d34140": r'''
public static void main (String [] args) {
    Scanner sc = new Scanner (System.in);
    String [] [] array = new String [7] [];
    array [0] = new String [] {"continents", "Asia", "Europe", "Africa", "Australia", "South America", "North America"};
    array [1] = new String [] {"profession", "teacher", "doctor", "lawyer"};
    array [2] = new String [] {"brand", "apple", "samsung"};
    array [3] = new String [] {"name", "lisa", "peter", "sam", "jack"};
    array [4] = new String [] {"profession", "engineer", "Professor", "Dentist", "Driver"};
    array [5] = new String [] {"sex", "value", "male", "female"};
    array [6] = new String [] {"exp", "value", "1", "2", "3", "4"};
    int index = sc.nextInt ();
    int chosen = index - 1;
    List < String [] > rotated = new ArrayList < String [] > ();
    rotated.add (array [chosen]);
    for (int i = 0; i < array.length; i ++) {
        if (i != chosen) {
            rotated.add (array [i]);
        }
    }
    for (String [] tempArray : rotated) {
        System.out.println (String.join (" ", tempArray));
    }
}
''',
"Rd41c27729f": r'''
def is_prime(n) :
	if n < 2 :
		return False
	if n == 2 :
		return True
	if n % 2 == 0 :
		return False
	for k in range(3, int(n ** 0.5) + 1, 2) :
		if n % k == 0 :
			return False
	return True
''',
"Refa2e73039": r'''
int main (void) {
    int sum = 0;
    int n;
    printf ("enter numbers: ");
    while (scanf ("%d", &n) == 1) {
        sum += n;
    }
    printf ("sum: %d\n", sum);
    return 0;
}
''',
"R0113c1db9b": r'''
def foo(thing = None, thing_seq = None) :
	pending = []
	if thing is not None :
		pending.append(thing)
	if thing_seq is not None :
		pending.extend(thing_seq)
	while pending :
		current = pending.pop(0)
		print("did foo with", current)
''',
"Rc5f95dbda1": r'''
private static void GetUserData (string userName, UserSession user)
{
    using (Entities ctx = CommonSERT.GetContext ())
    {
        var result = ctx.datUserRoles
            .Where (ur => string.Equals (ur.AccountName, userName, StringComparison.CurrentCultureIgnoreCase))
            .Select (ur => new { ur.Active, ur.ID })
            .FirstOrDefault ();
        if (result != null)
        {
            user.UserActive = result.Active;
        }
        user.UserID = result.ID;
    }
}
''',
"Rf9eb0ff068": r'''
def function(argument) :
	max_arg = max(argument)
	argument.remove(max_arg)
	remaining = sorted(argument)
	def search(start, total) :
		if total == max_arg :
			return True
		if start >= len(remaining) :
			return False
		for i in range(start, len(remaining)) :
			if search(i + 1, total + remaining[i]) :
				return True
		return False
	return "true" if search(0, 0) else "false"
''',
"R1479812111": r'''
public void doWork ()
{
    for (int h = 0; h <= 0; h++)
    {
        Thread.Sleep (3000);
        h.Dump ();
    }
}
''',
"R314ba9cd4a": r'''
int main (void) {
    int word [32];
    unsigned long int number;
    int base;
    printf ("Enter the decimal number to be converted: ");
    scanf ("%ld", & number);
    printf ("\nEnter the new base: ");
    scanf ("%d", & base);
    printf ("The number is: ");
    int i = wordCalculator (word, number, base);
    while (i >= 0) {
        int digit = word [i];
        putchar (digit <= 9 ? '0' + digit : 'A' + digit - 10);
        i--;
    }
    printf ("\n");
    return 0;
}
''',
"R7ca8e2a2eb": r'''
static boolean isImmutable (Object obj) {
    Class < ? > objClass = obj.getClass ();
    boolean result = Immutable.class.equals (objClass.getSuperclass ())
        && Modifier.isFinal (objClass.getModifiers ());
    if (result) {
        for (Field field : objClass.getDeclaredFields ()) {
            if (! Modifier.isFinal (field.getModifiers ())) {
                result = false;
                break;
            }
            if (! isValidFieldType (field.getType ())) {
                result = false;
                break;
            }
        }
    }
    return result;
}
''',
"R8db01bf25f": r'''
def flatten(xs) :
	res = []
	stack = list(reversed(xs))
	while stack :
		item = stack.pop()
		if isinstance(item, list) :
			stack.extend(reversed(item))
		else :
			res.append(item)
	return res
''',
"Re6ed6fb8d3": r'''
public static IEnumerable < T > TakeLast < T > (this IEnumerable < T > input, int count)
{
    if (count <= 0)
        yield break;
    var buffer = new List < T > ();
    foreach (T item in input)
    {
        buffer.Add (item);
    }
    int first = Math.Max (0, buffer.Count - count);
    for (int i = first; i < buffer.Count; i++)
    {
        yield return buffer [i];
    }
}
''',
"Rc93ef31bfe": r'''
def matched(s) :
	balance = 0
	for ch in s :
		if ch == '(' :
			balance += 1
		elif ch == ')' :
			balance -= 1
			if balance < 0 :
				return False
	return balance == 0
''',
"R077660cd40": r'''
int main (void) {
    int ch;
    int numWords = 0;
    int numLetters = 0;
    bool inWord = false;
    printf ("Enter a sentence: ");
    while ((ch = getchar ()) != EOF && ch != '\n') {
        bool isSpace = (ch == ' ');
        if (isSpace) {
            inWord = false;
        } else {
            numLetters++;
            if (! inWord) {
                numWords++;
                inWord = true;
            }
        }
    }
    if (numWords > 0) {
        printf ("Average word length: %.1f (C = %d, N = %d)\n",
            (float) numLetters / numWords, numLetters, numWords);
    } else {
        printf ("You didn't enter any words\n");
    }
    return 0;
}
''',
"R076547cbe5": r'''
public static bool IsWindowOnAnyScreen(Window Window, short WindowSizeX, short WindowSizeY, bool AutoAdjustWindow)
{
    var Screen = System.Windows.Forms.Screen.FromHandle(new WindowInteropHelper(Window).Handle);
    bool fits = Window.Left >= Screen.WorkingArea.Left
        && Window.Top >= Screen.WorkingArea.Top
        && (Window.Top + WindowSizeY) <= Screen.WorkingArea.Bottom
        && (Window.Left + WindowSizeX) <= Screen.WorkingArea.Right;
    if (fits)
    {
        return true;
    }
    if (AutoAdjustWindow)
    {
        if (Window.Left < Screen.WorkingArea.Left)
        {
            Window.Left = Screen.WorkingArea.Left;
        }
        if (Window.Top < Screen.WorkingArea.Top)
        {
            Window.Top = Screen.WorkingArea.Top;
        }
        if ((Window.Top + WindowSizeY) > Screen.WorkingArea.Bottom)
        {
            Window.Top = Screen.WorkingArea.Bottom - WindowSizeY;
        }
        if ((Window.Left + WindowSizeX) > Screen.WorkingArea.Right)
        {
            Window.Left = Screen.WorkingArea.Right - WindowSizeX;
        }
    }
    return false;
}
''',
"Rb740b5ce4e": r'''
int main () {
    int blah = 1;
    void *level = &blah;
    for (int depth = 1; depth <= 8; depth++) {
        level = &level;
    }
    mega_pointer ((int *********) level);
    return 0;
}
''',
"R2d627295b4": r'''
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats
class MyLinearRegression(LinearRegression):
	def fit(self, X, y, n_jobs = 1) :
		super().fit(X, y, n_jobs)
		predicted = self.predict(X)
		squared = (predicted - y) ** 2
		ssr = np.sum(squared, axis = 0) / float(X.shape[0] - X.shape[1])
		serr = []
		diag = np.diagonal(ssr)
		for i in range(ssr.shape[0]) :
			inv = np.linalg.inv(np.dot(X.T, X))
			serr.append(np.sqrt(diag[i] * inv))
		self.t = self.coef_ / np.array(serr)
''',
"R27ef16612d": r'''
int main () {
    int a [50] = {1, 2, -3, 0, 0, 6, 7, -8, 0, SENTINEL};
    int count = 0;
    int *p = a;
    while (*p != SENTINEL && p < a + 50) {
        if (*p != 0) {
            count++;
        }
        p++;
    }
    printf ("Total Element :%d ", count);
    return 0;
}
''',
"R80bf6ba91c": r'''
public static void main (final String [] args) throws IOException {
    BufferedReader br = new BufferedReader (new InputStreamReader (System.in));
    System.out.println ("Enter some text, or '" + EXIT_COMMAND + "' to quit");
    boolean done = false;
    while (! done) {
        System.out.print ("><![CDATA[ ");
        String input = br.readLine ();
        System.out.println (input);
        if (isExitCommand (input)) {
            System.out.println ("Exiting.");
            done = true;
        } else {
            System.out.println ("...response goes here...");
        }
    }
}

private static boolean isExitCommand (String input) {
    return input.length () == EXIT_COMMAND.length () && input.toLowerCase ().equals (EXIT_COMMAND);
}
''',
"R5813b54ca5": r'''
int main () {
    double integralSum = 0;
    for (int i = 1; i < (parts + 1); ++i) {
        double term = pow ((x + (step * i)), 2) + 4;
        integralSum += step * fabs (term);
    }
    printf ("%f\n", integralSum);
    return 0;
}
''',
"R14e363aee6": r'''
public static void Main ()
{
    string baseIP = "192.168.1.";
    Console.WriteLine ("Pinging 255 destinations of D-class in {0}*", baseIP);
    CreatePingers (255);
    PingOptions po = new PingOptions (ttl, true);
    System.Text.ASCIIEncoding enc = new System.Text.ASCIIEncoding ();
    byte [] data = enc.GetBytes ("abababababababababababababababab");
    SpinWait wait = new SpinWait ();
    Stopwatch watch = Stopwatch.StartNew ();
    for (int cnt = 1; cnt <= pingers.Count; cnt++)
    {
        Ping p = pingers [cnt - 1];
        lock (@lock)
        {
            instances += 1;
        }
        p.SendAsync (string.Concat (baseIP, cnt.ToString ()), timeOut, data, po);
    }
    while (instances > 0)
    {
        wait.SpinOnce ();
    }
    watch.Stop ();
    DestroyPingers ();
    Console.WriteLine ("Finished in {0}. Found {1} active IP-addresses.", watch.Elapsed.ToString (), result);
    Console.ReadKey ();
}
''',
"R9582f81645": r'''
def __init__(self, a = None, b = None, ** kwargs) :
	self.relations = {
	"e" : {"req" : ["a", "b"], "func" : lambda a, b : a + b},
	"C" : {"req" : ["e", "a"], "func" : lambda e, a : e * 1 / (a * b)},
	"A" : {"req" : ["C", "e"], "func" : lambda e, C : cmplx_func_A(e, C)},
	"a" : {"req" : ["e", "b"], "func" : lambda e, b : e / b},
	"b" : {"req" : ["e", "a"], "func" : lambda e, a : e / a}}
	for name, value in (("a", a), ("b", b), ("e", None), ("C", None), ("A", None)) :
		setattr(self, name, value)
	if kwargs :
		for key, value in kwargs.items() :
			setattr(self, key, value)
''',
"Rcc630548aa": r'''
public IDisposable Enter (string key)
{
    Locker locker;
    lock (this.globalLock)
    {
        if (this.locks.ContainsKey (key))
        {
            locker = this.locks [key];
        }
        else
        {
            locker = new Locker (this, key);
            this.locks [key] = locker;
        }
        locker.WaitCount ++;
    }
    locker.Enter ();
    locker.WaitCount --;
    return locker;
}
''',
"R8868947157": r'''
int main (void) {
    char first [25];
    int index = 0;
    int n;
    printf ("Enter the number of last names :\n");
    scanf ("%d", & n);
    printf ("Enter the first name \n");
    scanf ("%s", first);
    char last [n] [25];
    for (int i = 0; i < n; i++) {
        scanf ("%s", last [i]);
        if (strcmp (last [i], first) == 0) {
            index++;
        }
    }
    if (index == 0) {
        printf ("First name not repeated\n");
    } else {
        printf ("First name repeated %d times", index);
    }
    return 0;
}
'''
}
