DATA_R2 = {
"Radd810f35f": r'''
public static String join (String separator, String...values) {
    if (values.length == 0) return "";
    StringBuilder sb = new StringBuilder ();
    boolean first = true;
    for (String value : values) {
        String safe = (value == null) ? "" : value;
        if (! first) sb.append (separator);
        sb.append (safe);
        first = false;
    }
    return sb.toString ();
}
''',
"Ra654f3cacb": r'''
public static boolean isPalindrome (String str) {
    String upper = str.toUpperCase ();
    int left = 0;
    int right = upper.length () - 1;
    while (left < right) {
        if (! upper.substring (left, left + 1).equalsIgnoreCase (upper.substring (right, right + 1))) {
            return false;
        }
        left ++;
        right --;
    }
    return true;
}
''',
"Rc34ff3d7d3": r'''
private void initData () {
    testData = new ArrayList < EventStatus > ();
    addEvents ("Mach-1", new long [] {1477468500000L, 1477472100000L, 1477474200000L, 1477476000000L, 1477479600000L, 1477486800000L},
               new int [] {1, 2, 5, 3, 4, 1}, 0);
    addEvents ("Mach-2", new long [] {1477465200000L, 1477472400000L, 1477474200000L, 1477476000000L, 1477479600000L, 1477486800000L},
               new int [] {3, 2, 5, 2, 3, 4}, 1);
    Set < String > names = new LinkedHashSet < > ();
    for (EventStatus eventStatus : testData) {
        names.add (eventStatus.getName ());
    }
    catArray = names.toArray (new String [0]);
}

private void addEvents (String name, long [] times, int [] statuses, int flag) {
    for (int i = 0; i < times.length; i ++) {
        testData.add (new EventStatus (name, times [i], statuses [i], flag));
    }
}
''',
"R91d065403d": r'''
public static File createTempDir () {
    File baseDir = new File (System.getProperty ("java.io.tmpdir"));
    String baseName = System.currentTimeMillis () + "-";
    int counter = 0;
    while (counter < TEMP_DIR_ATTEMPTS) {
        File tempDir = new File (baseDir, baseName + counter);
        if (tempDir.mkdir ()) {
            return tempDir;
        }
        counter ++;
    }
    throw new IllegalStateException ("Failed to create directory within " + TEMP_DIR_ATTEMPTS + " attempts (tried " + baseName + "0 to " + baseName + (TEMP_DIR_ATTEMPTS - 1) + ')');
}
''',
"Ra1eaef8d13": r'''
private static void removeEven (int [] k, int n) {
    int counter = 0;
    int i = 0;
    while (i < n) {
        if (k [i] % 2 == 1) {
            k [counter] = k [i];
            counter ++;
        }
        i ++;
    }
    java.util.Arrays.fill (k, counter, n, 0);
}
''',
}
