DATA5 = {
"Rbf38b9a69d": r'''private void transform (XSSFWorkbook workbookOld, HSSFWorkbook workbookNew, Integer hash, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    copyPlainAttributes (styleOld, styleNew);
    styleNew.setDataFormat (this.transform (workbookOld, workbookNew, styleOld.getDataFormat ()));
    styleNew.setFont (this.transform (workbookNew, (XSSFFont) styleOld.getFont ()));
    this.styleMap.put (hash, styleNew);
}

private void copyPlainAttributes (XSSFCellStyle from, HSSFCellStyle to) {
    to.setAlignment (from.getAlignment ());
    to.setBorderBottom (from.getBorderBottom ());
    to.setBorderLeft (from.getBorderLeft ());
    to.setBorderRight (from.getBorderRight ());
    to.setBorderTop (from.getBorderTop ());
    to.setFillBackgroundColor (from.getFillBackgroundColor ());
    to.setFillForegroundColor (from.getFillForegroundColor ());
    to.setFillPattern (from.getFillPattern ());
    to.setHidden (from.getHidden ());
    to.setIndention (from.getIndention ());
    to.setLocked (from.getLocked ());
    to.setVerticalAlignment (from.getVerticalAlignment ());
    to.setWrapText (from.getWrapText ());
}''',
"Rb9c3635eed": r'''public static void main (String args []) {
    inp = new Scanner (System.in);
    String str = inp.nextLine ();
    Map < Character, Integer > counts = new LinkedHashMap < Character, Integer > ();
    for (int i = 0;
    i < str.length (); i ++) {
        counts.merge (str.charAt (i), 1, Integer::sum);
    }
    for (int i = 0;
    i < str.length (); i ++) {
        System.out.println ("Frequency of " + str.charAt (i) + "  is:   " + counts.get (str.charAt (i)));
    }
}''',
"Rea67761d7d": r'''public static void main (String [] args) {
    String [] samples = {"", null, "Starts with upper case", "starts with lower case"};
    for (String sample : samples) {
        System.out.println (startWithUpperCase (sample));
    }
}''',
"R357f96f327": r'''public static DataTable GetWorksheetAsDataTable(ExcelWorksheet worksheet) {
    DataTable dt = new DataTable(worksheet.Name);
    dt.Columns.AddRange(GetDataColumns(worksheet).ToList().ToArray());
    int headerOffset = 1;
    int width = dt.Columns.Count;
    int depth = GetTableDepth(worksheet, headerOffset);
    Enumerable.Range(1, depth).ToList().ForEach(rowNum => {
        DataRow row = dt.NewRow();
        Enumerable.Range(1, width).ToList().ForEach(colNum => {
            object val = worksheet.Cells[rowNum + headerOffset, colNum].Value;
            row[colNum - 1] = val == null ? null : val.ToString();
        });
        dt.Rows.Add(row);
    });
    return dt;
}''',
"Re3d1dfab68": r'''def create_lookup_list(messages, labels) :
  return [{"message": message, "label": label} for message, label in zip(messages, labels)]''',
"Rfe9a432a46": r'''public override void OnException (ExceptionContext filterContext) {
    filterContext.HttpContext.Response.TrySkipIisCustomErrors = true;
    filterContext.ExceptionHandled = true;
    filterContext.HttpContext.Response.ClearContent ();
    filterContext.Result = BuildErrorResult (filterContext);
    filterContext.Exception = null;
}

private static ViewResult BuildErrorResult (ExceptionContext filterContext) {
    var controllerName = (string) filterContext.RouteData.Values ["controller"];
    var actionName = (string) filterContext.RouteData.Values ["action"];
    var model = new HandleErrorInfo (filterContext.Exception, controllerName, actionName);
    return new ViewResult {ViewName = View, MasterName = Master, ViewData = new ViewDataDictionary < HandleErrorInfo > (model), TempData = filterContext.Controller.TempData};
}''',
"Rb8f6c8b5d0": r'''static int parseRuns (const char *s, char *alp, int *num, int *m, int *n) {
    int i = 0;
    while (s [i]) {
        unsigned char ch = s [i];
        if (isalpha (ch)) {
            alp [(*n)++] = s [i];
            i++;
        }
        else if (isdigit (ch)) {
            int value = 0;
            while (isdigit ((unsigned char) s [i])) {
                value = value * 10 + (s [i] - '0');
                i++;
            }
            num [(*m)++] = value;
        }
        else {
            printf ("include invalid character (%c).\n", ch);
            return 0;
        }
    }
    return 1;
}

int main (void) {
    char s [1000], alp [1000];
    int num [1000];
    int m = 0, n = 0;
    scanf ("%999[^\n]", s);
    if (! parseRuns (s, alp, num, &m, &n)) {
        return -1;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < num [i]; j++) {
            putchar (alp [i]);
        }
    }
    puts ("");
    return 0;
}''',
"R8b80f20070": r'''int main () {
    double v;
    if (scanf ("%lf", &v) != 1) {
        printf ("read failed\n");
        return 0;
    }
    printf ("%lf\n", v);
    return 0;
}''',
"R4e335703d6": r'''int main () {
    char s [SIZE];
    char *months [] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    printf ("enter the month : ");
    gets (s);
    int result = get_month (s, months);
    if (result != 0) {
        printf ("%s - %d.  is the month of the year.\n", s, result);
        return 0;
    }
    printf ("%s invalid\n", s);
    return 0;
}''',
"R9fdda16e3c": r'''static int printFactors (int num, int withSum) {
    int sum = 0;
    int tmp = num;
    while (1) {
        int x = getFirst (tmp);
        printf ("%d ", x);
        sum += x;
        if (x == tmp)
            break;
        if (withSum)
            printf ("+ ");
        tmp /= x;
    }
    return sum;
}

int main () {
    int num;
    scanf ("%d", & num);
    printf ("Factors are: ");
    printFactors (num, 0);
    printf ("\n");
    printf ("Sum of factors is: ");
    int sum = printFactors (num, 1);
    printf ("= %d\n", sum);
    return 0;
}''',
"R8c49ec85d8": r'''public void filter (String [] words, String text) {
    String lowerText = text.toLowerCase ();
    for (String word : words) {
        if (lowerText.contains (word.toLowerCase ())) {
            System.out.println (text);
            return;
        }
    }
}''',
"R8d187f48ce": r'''def traceit(frame, event, arg) :
	if event != "line" :
		return traceit
	lineno = frame.f_lineno
	filename = frame.f_globals ["__file__"]
	if filename == "<stdin>" :
		filename = "traceit.py"
	if filename.endswith((".pyc", ".pyo")) :
		filename = filename[: -1]
	name = frame.f_globals ["__name__"]
	line = linecache.getline(filename, lineno)
	print("%s:%s:%s: %s" % (name, lineno, frame.f_code.co_name, line.rstrip()))
	return traceit''',
"R00a4c22b00": r'''def roundrobin(* iterables):
	iter_items = []
	timers = [iter(it) for it in iterables]
	while timers:
		exhausted = []
		for it in timers:
			try:
				data = next(it)
			except StopIteration:
				exhausted.append(it)
				continue
			iter_items.append(data)
			yield data
		for gone in exhausted:
			timers.remove(gone)''',
"R2710a37612": r'''public static final void main (String...aArgs) {
    int START = 1;
    int END = 10;
    log ("Generating 10 random integers in range 1..10.");
    Random randomGenerator = new Random ();
    int idx = START;
    while (idx <= 10) {
        showRandomInteger (START, END, randomGenerator);
        idx = idx + 1;
    }
    log ("Done");
}''',
}
