DATA_R1 = {}

DATA_R1["Rbf38b9a69d"] = """private void transform (XSSFWorkbook workbookOld, HSSFWorkbook workbookNew, Integer hash, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    copyAlignmentAndBorders (styleOld, styleNew);
    styleNew.setDataFormat (this.transform (workbookOld, workbookNew, styleOld.getDataFormat ()));
    copyFill (styleOld, styleNew);
    styleNew.setFont (this.transform (workbookNew, (XSSFFont) styleOld.getFont ()));
    copyVisibility (styleOld, styleNew);
    this.styleMap.put (hash, styleNew);
}

private void copyAlignmentAndBorders (XSSFCellStyle src, HSSFCellStyle dst) {
    dst.setBorderTop (src.getBorderTop ());
    dst.setBorderBottom (src.getBorderBottom ());
    dst.setBorderLeft (src.getBorderLeft ());
    dst.setBorderRight (src.getBorderRight ());
    dst.setAlignment (src.getAlignment ());
}

private void copyFill (XSSFCellStyle src, HSSFCellStyle dst) {
    dst.setFillForegroundColor (src.getFillForegroundColor ());
    dst.setFillBackgroundColor (src.getFillBackgroundColor ());
    dst.setFillPattern (src.getFillPattern ());
}

private void copyVisibility (XSSFCellStyle src, HSSFCellStyle dst) {
    dst.setHidden (src.getHidden ());
    dst.setLocked (src.getLocked ());
    dst.setIndention (src.getIndention ());
    dst.setVerticalAlignment (src.getVerticalAlignment ());
    dst.setWrapText (src.getWrapText ());
}"""

DATA_R1["Rb9c3635eed"] = """public static void main (String args []) {
    inp = new Scanner (System.in);
    String str = inp.nextLine ();
    List < Character > arrlist = str.chars ().mapToObj (c -> (char) c).collect (Collectors.toList ());
    for (char c : arrlist) {
        int freq = Collections.frequency (arrlist, c);
        System.out.println ("Frequency of " + c + "  is:   " + freq);
    }
}"""

DATA_R1["Rea67761d7d"] = """public static void main (String [] args) {
    String [] testStrings = {"", null, "Starts with upper case", "starts with lower case"};
    for (String candidate : testStrings) {
        System.out.println (startWithUpperCase (candidate));
    }
}"""

DATA_R1["R8c49ec85d8"] = """public void filter (String [] words, String text) {
    String lowerText = text.toLowerCase ();
    for (String word : words) {
        if (lowerText.contains (word.toLowerCase ())) {
            System.out.println (text);
            return;
        }
    }
}"""

DATA_R1["R2710a37612"] = """public static final void main (String...aArgs) {
    log ("Generating 10 random integers in range 1..10.");
    int START = 1;
    int END = 10;
    Random randomGenerator = new Random ();
    int idx = 1;
    while (idx <= 10) {
        showRandomInteger (START, END, randomGenerator);
        idx ++;
    }
    log ("Done");
}"""

DATA_R1["Rd744148380"] = """public void onRequestPermissionsResult (int requestCode, String permissions [], int [] grantResults) {
    super.onRequestPermissionsResult (requestCode, permissions, grantResults);
    if (grantResults.length == 0 || grantResults == null) {
        return;
    }
    if (grantResults [0] == PackageManager.PERMISSION_GRANTED) {
        return;
    }
    if (grantResults [0] == PackageManager.PERMISSION_DENIED) {
        return;
    }
}"""

DATA_R1["Refd906fcb2"] = """long pow (long a, int b) {
    long result = 1;
    int exponent = b;
    long base = a;
    while (exponent > 1) {
        if (! isEven (exponent)) {
            result = result * base;
        }
        base = base * base;
        exponent = exponent / 2;
    }
    if (exponent == 1) {
        return result * base;
    }
    return result;
}"""

DATA_R1["Rd40ca7a94c"] = """public final void contextDestroyed (ServletContextEvent sce) {
    ClassLoader cl = Thread.currentThread ().getContextClassLoader ();
    for (Enumeration < Driver > drivers = DriverManager.getDrivers (); drivers.hasMoreElements ();) {
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
}"""
