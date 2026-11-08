DATA_R2 = {
"Rc34ff3d7d3": '''private void initData () {
    testData = new ArrayList < EventStatus > ();
    Object [] [] events = {
        {"Mach-1", 1477468500000L, 1, 0},
        {"Mach-1", 1477472100000L, 2, 0},
        {"Mach-1", 1477474200000L, 5, 0},
        {"Mach-1", 1477476000000L, 3, 0},
        {"Mach-1", 1477479600000L, 4, 0},
        {"Mach-1", 1477486800000L, 1, 0},
        {"Mach-2", 1477465200000L, 3, 1},
        {"Mach-2", 1477472400000L, 2, 1},
        {"Mach-2", 1477474200000L, 5, 1},
        {"Mach-2", 1477476000000L, 2, 1},
        {"Mach-2", 1477479600000L, 3, 1},
        {"Mach-2", 1477486800000L, 4, 1}
    };
    for (Object [] row : events) {
        testData.add (new EventStatus ((String) row [0], (Long) row [1], (Integer) row [2], (Integer) row [3]));
    }
    LinkedHashSet < String > names = new LinkedHashSet < > ();
    for (EventStatus eventStatus : testData) {
        names.add (eventStatus.getName ());
    }
    catArray = names.toArray (new String [0]);
}
''',
"R73c281cc62": '''private static IEnumerable < T [] > EnumerateCombos < T > (IEnumerable < T > items, List < T > currentCombo, int startIndex, int threshold) {
    if (currentCombo.Count < threshold) {
        int i = startIndex;
        while (i < items.Count ()) {
            var item = items.Skip (i).First ();
            currentCombo.Add (item);
            yield return currentCombo.ToArray ();
            foreach (var combo in EnumerateCombos (items, currentCombo, i + 1, threshold)) {
                yield return combo;
            }
            currentCombo.RemoveAt (currentCombo.Count - 1);
            i ++;
        }
    }
}
''',
"R91d065403d": '''public static File createTempDir () {
    File baseDir = new File (System.getProperty ("java.io.tmpdir"));
    String baseName = System.currentTimeMillis () + "-";
    int counter = 0;
    while (counter < TEMP_DIR_ATTEMPTS) {
        File tempDir = new File (baseDir, baseName + counter);
        boolean created = tempDir.mkdir ();
        if (created) {
            return tempDir;
        }
        counter ++;
    }
    throw new IllegalStateException ("Failed to create directory within " + TEMP_DIR_ATTEMPTS + " attempts (tried " + baseName + "0 to " + baseName + (TEMP_DIR_ATTEMPTS - 1) + ')');
}
''',
"R8cfbeb65a3": '''public static IList < ReportFile > ReadFiles (int year, int month) {
    string [] fileNames = new string [] {"{0:YYYYMMDD}----1234D.dat", "{0:YYYYMMDD}----5678D.dat"};
    List < ReportFile > reportList = new List < ReportFile > ();
    int days = DateTime.DaysInMonth (year, month);
    for (int day = 1; day <= days; day ++) {
        DateTime date = new DateTime (year, month, day);
        reportList.AddRange (
            from fileTemplate in fileNames
            let file = string.Format (fileTemplate, date)
            where File.Exists (file)
            select new ReportFile () {Date = date, Path = file, Lines = GetReportLines (file)});
    }
    IList < ReportFile > files = reportList;
    return files;
}
''',
"R8f617cb401": '''int main () {
    unsigned long *data = malloc (sizeof (unsigned long) * 9);
    unsigned long total = 0;
    for (int i = 1; i < 9; i += 2)
        total += data [i];
    printf ("%lu\\n", total);
    free (data);
    return 0;
}
''',
"R593eed57e6": '''static void Main (string [] args) {
    Console.WriteLine ("Enter A Number :");
    int n = int.Parse (Console.ReadLine ());
    bool byThree = n % 3 == 0;
    bool byFive = n % 5 == 0;
    if (byThree && byFive) {
        Console.WriteLine ("This Number is Divisible by 3 and 5!");
    } else if (byThree) {
        Console.WriteLine ("\\nThe number is divisible by 3 but not by 5");
    } else if (byFive) {
        Console.WriteLine ("The number is divisible by 5 but not by 3");
    } else {
        Console.WriteLine ("\\nThis Number is Not Divisible by 3 and 5!");
    }
    Console.ReadLine ();
}
''',
"Rc5e1a6cc9a": '''void initialize () {
    ConcurrentQueue < string > queue = new ConcurrentQueue < string > ();
    foreach (string url in websites) {
        queue.Enqueue (url);
    }
    List < Thread > threads = Enumerable.Range (0, threadCountFromTheUser)
        .Select (_ => new Thread (work))
        .ToList ();
}
''',
"R35e99f1126": '''static void Main (string [] args) {
    var EDGES = BuildEdges ();
    var POINTS = new List < double [] > (EDGES.Count * 2);
    FillPoints (EDGES, ref POINTS);
    PrintPoints (POINTS);
    Console.WriteLine ();
    var edgeIndices = new int [EDGES.Count, 2];
    FillEdges (EDGES, POINTS, ref edgeIndices);
    PrintEdgeIndices (edgeIndices);
    Console.ReadKey (true);
}

static List < Edge > BuildEdges () {
    var edges = new List < Edge > ();
    void Add (int x1, int y1, int x2, int y2) {
        edges.Add (new Edge (new Point (x1, y1), new Point (x2, y2)));
    }
    Add (5, 50, 20, 100);
    Add (20, 100, 30, 50);
    Add (30, 50, 10, 0);
    Add (5, 50, 30, 50);
    Add (5, 50, 10, 0);
    Add (20, 100, 80, 100);
    Add (10, 0, 80, 100);
    return edges;
}

static void PrintPoints (List < double [] > points) {
    for (int i = 0; i < points.Count; i ++) {
        Console.WriteLine ("{0} {1} {2}", i, points [i] [0], points [i] [1]);
    }
}

static void PrintEdgeIndices (int [,] edgeIndices) {
    for (int i = 0; i < edgeIndices.GetLength (0); i ++) {
        Console.WriteLine ("({0}, {1})", edgeIndices [i, 0], edgeIndices [i, 1]);
    }
}
''',
"Ra1eaef8d13": '''private static void removeEven (int [] k, int n) {
    int counter = 0;
    int i = 0;
    while (i < n) {
        if (k [i] % 2 == 1) {
            k [counter ++] = k [i];
        }
        i ++;
    }
    Arrays.fill (k, counter, n, 0);
}
''',
"R7fe68d314b": '''public static List < string > LoadCitiesByState (string state) {
    DataTable dt = null;
    try {
        dt = SharedDataAccess.GetCities (state);
    }
    catch {
        dt = new DataTable ();
    }
    List < string > cities = new List < string > ();
    foreach (DataRow row in dt.Rows) {
        cities.Add (row [0].ToString ());
    }
    return cities;
}
''',
"R83b1b1f08f": '''void main (int argc, char **argv) {
    int myargc = argc;
    char **myargv = calloc ((size_t) (argc - 1), sizeof (char *));
    for (int i = 1; i < argc; i++) {
        myargv [i - 1] = strdup (argv [i]);
    }
    getch ();
}
''',
"R08feb9bb95": '''public void ResetFields (Control.ControlCollection Controls) {
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
''',
}
