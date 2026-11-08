DATA_C1 = {
"Rbf38b9a69d": r"""
private void transform (XSSFWorkbook workbookOld, HSSFWorkbook workbookNew, Integer hash, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    copyEdges(styleOld, styleNew);
    styleNew.setDataFormat(this.transform(workbookOld, workbookNew, styleOld.getDataFormat()));
    copyFillAndFont(workbookNew, styleOld, styleNew);
    copyFlags(styleOld, styleNew);
    this.styleMap.put(hash, styleNew);
}

private void copyEdges(XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    styleNew.setAlignment(styleOld.getAlignment());
    styleNew.setBorderBottom(styleOld.getBorderBottom());
    styleNew.setBorderLeft(styleOld.getBorderLeft());
    styleNew.setBorderRight(styleOld.getBorderRight());
    styleNew.setBorderTop(styleOld.getBorderTop());
    styleNew.setVerticalAlignment(styleOld.getVerticalAlignment());
}

private void copyFillAndFont(HSSFWorkbook workbookNew, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    styleNew.setFillBackgroundColor(styleOld.getFillBackgroundColor());
    styleNew.setFillForegroundColor(styleOld.getFillForegroundColor());
    styleNew.setFillPattern(styleOld.getFillPattern());
    styleNew.setFont(this.transform(workbookNew, (XSSFFont) styleOld.getFont()));
}

private void copyFlags(XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    styleNew.setHidden(styleOld.getHidden());
    styleNew.setIndention(styleOld.getIndention());
    styleNew.setLocked(styleOld.getLocked());
    styleNew.setWrapText(styleOld.getWrapText());
}
""",
"Rb9c3635eed": r"""
public static void main (String args []) {
    inp = new Scanner (System.in);
    String str = inp.nextLine ();
    List < Character > arrlist = new ArrayList < Character > ();
    for (char ch : str.toCharArray ()) {
        arrlist.add (ch);
    }
    Map < Character, Integer > freqMap = new LinkedHashMap < Character, Integer > ();
    for (int i = 0;
    i < str.length (); i ++) {
        char ch = str.charAt (i);
        freqMap.merge (ch, 1, Integer::sum);
    }
    for (int i = 0;
    i < str.length (); i ++) {
        char ch = str.charAt (i);
        System.out.println ("Frequency of " + ch + "  is:   " + freqMap.get (ch));
    }
}
""",
"Rea67761d7d": r"""
public static void main (String [] args) {
    String [] testInputs = {
        "",
        null,
        "Starts with upper case",
        "starts with lower case"
    };
    for (String candidate : testInputs) {
        System.out.println (startWithUpperCase (candidate));
    }
}
"""
}
