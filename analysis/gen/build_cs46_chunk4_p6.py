DATA6 = {
"Rf6f525dc34": r'''static void Main (string [] args) {
    var process = StartLibreOffice (args);
    ValidateProcessExitCode (process);
}

private static Process StartLibreOffice (string [] args) {
    var procStartInfo = new ProcessStartInfo (getLibreOfficePath (), string.Format (CreateParamString (args)));
    SetProcessStartInfoProperties (procStartInfo);
    var process = new Process () {StartInfo = procStartInfo};
    ExecuteProcess (process);
    return process;
}''',
"R6ea07c8787": r'''public static void Rename (this FileSystemInfo item, string newName) {
    if (item == null) {
        throw new ArgumentNullException ("item");
    }
    if (item is FileInfo) {
        ((FileInfo) item).Rename (newName);
    }
    else if (item is DirectoryInfo) {
        ((DirectoryInfo) item).Rename (newName);
    }
    else {
        throw new ArgumentException ("Item", "Unexpected subclass of FileSystemInfo " + item.GetType ());
    }
}''',
"Rd744148380": r'''public void onRequestPermissionsResult (int requestCode, String permissions [], int [] grantResults) {
    super.onRequestPermissionsResult (requestCode, permissions, grantResults);
    switch (grantResults.length > 0 ? grantResults [0] : - 1) {
        case PackageManager.PERMISSION_GRANTED :
            break;
        case PackageManager.PERMISSION_DENIED :
            break;
        default :
            break;
    }
}''',
"R51669e3825": r'''def __init__(self) :
	self.secondsRemaining, self.lastTick = 10.0, 0
	self.isPaused = self.isRunning = False
	self.keepGoing = True''',
"Ra853448a33": r'''static void setRawInput (struct termios *orig) {
    struct termios new_attr;
    tcgetattr (fileno (stdin), orig);
    memcpy (& new_attr, orig, sizeof (*orig));
    new_attr.c_lflag &= ~ (ICANON | ECHO);
    tcsetattr (fileno (stdin), TCSANOW, & new_attr);
}

int main () {
    int counter = 0;
    struct termios orig_attr;
    setRawInput (& orig_attr);
    pthread_t pid;
    if (pthread_create (& pid, NULL, thread, & counter) != 0) {
        fprintf (stderr, "Create thread failed");
        exit (1);
    }
    for (;;) {
        int c = getchar ();
        (void) c;
        __sync_add_and_fetch (& counter, 1);
        printf ("add: %d\n", counter);
    }
    return 0;
}''',
"R3713a963cf": r'''def json_scan(json_obj, key) :
	result = None
	for element in json_obj :
		child = json_obj [element]
		if str(element) == key :
			result = child
		elif isinstance(child, (dict, list)) :
			target = child if isinstance(child, dict) else element
			result = json_scan(target, key)
	return result''',
"R4474610115": r'''int main (void) {
    int start;
    if (scanf ("%d", &start) != 1)
        exit (1);
    int end = start;
    while (scanf ("%d", &end) == 1)
        ;
    while (start <= end) {
        printf ("%d\n", start);
        start++;
    }
}''',
"Refd906fcb2": r'''long pow (long a, int b) {
    long result = 1;
    while (b > 0) {
        if (! isEven (b)) {
            result *= a;
        }
        a *= a;
        b /= 2;
    }
    return result;
}''',
"Rd40ca7a94c": r'''public final void contextDestroyed (ServletContextEvent sce) {
    ClassLoader cl = Thread.currentThread ().getContextClassLoader ();
    Enumeration < Driver > drivers = DriverManager.getDrivers ();
    while (drivers.hasMoreElements ()) {
        deregisterIfOwned (drivers.nextElement (), cl);
    }
}

private void deregisterIfOwned (Driver driver, ClassLoader cl) {
    if (driver.getClass ().getClassLoader () != cl) {
        log.trace ("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver);
        return;
    }
    try {
        log.info ("Deregistering JDBC driver {}", driver);
        DriverManager.deregisterDriver (driver);
    } catch (SQLException ex) {
        log.error ("Error deregistering JDBC driver {}", driver, ex);
    }
}''',
"Rfaf0b51ec8": r'''def combinations(iterable, r) :
	pool = tuple(iterable)
	n = len(pool)
	if r > n :
		return
	if r == 0 :
		yield ()
		return
	for i in range(n - r + 1) :
		for rest in combinations(pool [i + 1 :], r - 1) :
			current = (pool [i],) + rest
			if 1 in current and 3 in current :
				pass
			else :
				yield current''',
"R3c52337f3a": r'''internal static string GetIPAddress (HttpRequestBase request) {
    string forwarded = request.Headers ["Forwarded"];
    if (! String.IsNullOrEmpty (forwarded)) {
        string ip = ParseForwardedHeader (forwarded);
        if (ip != null) {
            return ip;
        }
    }
    string xForwardedFor = request.Headers ["X-Forwarded-For"];
    if (! String.IsNullOrEmpty (xForwardedFor)) {
        return xForwardedFor.Split (',') [0];
    }
    return request.UserHostAddress;
}

private static string ParseForwardedHeader (string forwarded) {
    foreach (string segment in forwarded.Split (',') [0].Split (';')) {
        string [] pair = segment.Trim ().Split ('=');
        if (pair.Length != 2 || ! pair [0].Equals ("for", StringComparison.OrdinalIgnoreCase)) {
            continue;
        }
        return UnquoteIp (pair [1].Trim ('"'));
    }
    return null;
}

private static string UnquoteIp (string ip) {
    int left = ip.IndexOf ('[');
    if (left == 0) {
        int right = ip.IndexOf (']');
        return ip.Substring (1, right - 1);
    }
    int colon = ip.IndexOf (':');
    if (colon != - 1) {
        return ip.Substring (0, colon);
    }
    return ip;
}''',
}
