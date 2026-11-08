DATA6 = {}

DATA6["R6ec2173375"] = """def treeToList(node, order = Order.INORDER) :
\tif node is None :
\t\treturn []
\tright = treeToList(node.right, order)
\tdown = treeToList(node.down, order)
\tcurrent = [node.data]
\tordering = {
\t\tOrder.PREORDER : current + right + down,
\t\tOrder.INORDER : right + current + down,
\t\tOrder.POSTORDER : right + down + current,
\t}
\tif order not in ordering :
\t\treturn None
\treturn ordering[order]"""

DATA6["R998677b1ab"] = """int readWords (FILE *fp) {
    int i = 0;
    while (fgets (words[i], MAX_COLUMNS, fp) != NULL) {
        words[i][strlen (words[i]) - 1] = '\\0';
        i++;
    }
    return i;
}

int main (void) {
    FILE *fp = NULL;
    if (NULL == (fp = fopen (FILE_NAME, "r"))) {
        perror ("fopen failed");
        exit (EXIT_FAILURE);
    }
    int count = readWords (fp);
    bubbleSortWordsArray (count);
    printWordsArray (count);
    return (0);
}"""

DATA6["Rbef72fa071"] = """public static int score (final String gene1, final String gene2) {
    return score (gene1.toCharArray (), gene2.toCharArray (), 0, 0);
}"""

DATA6["Rc80ff5796f"] = """public static boolean twoDuplicates (int [] values) {
    Map < Integer, Integer > counts = new HashMap < Integer, Integer > ();
    for (int v : values) {
        int c = counts.merge (v, 1, Integer::sum);
        if (c == 3) return true;
    }
    return false;
}"""

DATA6["Re56d31c78d"] = """public static void Dispose(this MethodBuilder mb) {
    if (mb == null)
        return;
    Type mbType = typeof (MethodBuilder);
    DisposeField (mb, mbType, "m_module");
    DisposeField (mb, mbType, "m_containingType");
    DisposeField (mb, mbType, "m_localSignature");
    DisposeField (mb, mbType, "m_signature");
    DisposeField (mb, mbType, "m_ilGenerator");
}

private static void DisposeField (MethodBuilder mb, Type mbType, string fieldName) {
    FieldInfo field = mbType.GetField (fieldName, BindingFlags.Instance | BindingFlags.NonPublic);
    object value = field.GetValue (mb);
    if (value is IDisposable disposable) {
        disposable.Dispose ();
    }
    field.SetValue (mb, null);
}"""

DATA6["R876047a76c"] = """def is_prime(x) :
\tif x < 2 :
\t\treturn False
\treturn all(x % n for n in range(2, x - 1))"""

DATA6["R61361acd54"] = """public FileVisitResult visitFile (Path file, BasicFileAttributes attrs) throws IOException {
                logVisited (file);
                return FileVisitResult.CONTINUE;
}

private void logVisited (Path file) {
                System.out.println (file);
}"""

DATA6["R8cedc05d13"] = """public int readNumber () {
    int x;
    do {
        System.out.println ("Please enter a positive number.");
        try {
            x = keyboard.nextInt ();
        } catch (java.util.InputMismatchException e) {
            x = - 1;
        }
    } while (x < 0);
    return x;
}"""

DATA6["Re5e59b66ff"] = """def find_nth(string, substring, n) :
\tpos = - 1
\tfor _ in range(n) :
\t\tpos = string.find(substring, pos + 1)
\treturn pos"""

DATA6["R6073c71857"] = """static void readAndPrint (void) {
    temperature = bmp085_GetTemperature (bmp085_ReadUT ());
    pressure = bmp085_GetPressure (bmp085_ReadUP ());
    altitude = bmp085_Altitude (pressure);
    printf ("Temperature\\t%0.1f *F\\n", ((double) temperature) / 10 * 1.8 + 32);
    printf ("Pressure\\t%0.2f hPa\\n", ((double) pressure) / 100);
    printf ("Altitude\\t%0.1f Feet\\n", ((double) altitude) * 3.280839895);
}

int main (int argc, char **argv) {
    bmp085_Calibration ();
    int count = 0;
    while (count < 49) {
        readAndPrint ();
        sleep (1800);
        count++;
    }
    return 0;
}"""

DATA6["R271e84529a"] = """int main (void) {
    unsigned int i;
    unsigned int x;
    if (scanf ("%u", & i) != 1) return 0;
    scanf ("%u", & x);
    int output = 0;
    for (;;) {
        if (x == 0) break;
        int t = x % 10;
        output += (t == x) ? 1 : 0;
        x /= 10;
    }
    printf ("%d", output);
    return 0;
}"""

DATA6["Re0be2a9253"] = """def collatz(number) :
\tif number % 2 :
\t\tresult = 3 * number + 1
\telse :
\t\tresult = number // 2
\tprint(result)
\treturn result"""

DATA6["R79546e7246"] = """static void printHex16 (unsigned long var1, unsigned long var2) {
    char buffer [17];
    sprintf (buffer, "%x%x", var1, var2);
    int len = strlen (buffer);
    if (len < 16) {
        char zeros [17];
        memset (zeros, '0', 16 - len);
        zeros[16 - len] = 0x0;
        printf ("%s%s\\n", zeros, buffer);
    }
    else {
        printf ("%s\\n", buffer);
    }
}

int main () {
    printHex16 (1048575, 1048575);
    return 0;
}"""

DATA6["R9936309be3"] = """public void mouseReleased (int mod, Point loc) {
    pressLocation = null;
    dragLocation = null;
}"""

DATA6["R8caade20c5"] = """static void Main (string [] args) {
    var skins = new Dictionary < string, string [] >
    {
        { "ahri", new[] { "Academy", "Challenger", "Dynasty", "Foxfire", "Midnight", "Popstar" } },
        { "leeSin", new[] { "Traditional", "Acolyte", "Dragon Fist", "Musy Thai", "Pool Party", "SKT T1", "Knockout" } }
    };
    Console.WriteLine ("Conor's Random League of Legends Skin Selector v0.1");
    Console.WriteLine (" ");
    Console.WriteLine (" ");
    Random rnd = new Random ();
    Console.ForegroundColor = ConsoleColor.Gray;
    Console.WriteLine ("What champion would you like to select a skin for?..    ");
    string champion = Console.ReadLine ();
    Console.Write ("Press the 'enter' key for a random champion..     ");
    Console.ReadLine ();
    string [] pool = skins.ContainsKey (champion) ? skins [champion] : skins ["leeSin"];
    Console.WriteLine (pool [rnd.Next (pool.Length - 1)]);
}"""

DATA6["Re2915c15ad"] = """def dashboard(request) :
\tvalid = False
\tform = FilterForm()
\tif request.POST :
\t\tform = FilterForm(request.POST)
\t\tvalid = form.is_valid()
\tif valid :
\t\tsightings = Sighting.objects.filter(IMS_plant = form.cleaned_data ['selectedplant'])
\telse :
\t\tsightings = Sighting.objects.all().order_by('date')
\tcontext = {'sightings' : sightings, 'form' : form}
\treturn render_to_response('dashboard.html', context, context_instance = RequestContext(request))"""

DATA6["Re8e5ba0337"] = """def get_info(session, title, url) :
\tr = session.get(url)
\tsoup = BeautifulSoup(r.text, "lxml")
\tphone = "N/A"
\tfor items in soup.select("ul.list-unstyled") :
\t\tlinks = items.select("a[href^='tel:']")
\t\tif links :
\t\t\tphone = links [0].text
\t\t\tbreak
\tprint (title, phone)"""
