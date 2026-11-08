PART = []

PART.append({"id": "Ra03011d81d", "task": "refactor", "output": r'''static void read_and_print_sum(int *counter) {
    int a, b;
    scanf("%d %d", &a, &b);
    *counter += 1;
    printf("%d: %d + %d = %d\n", *counter, a, b, sum(a + 1, b + 1));
}

int main() {
    int i = 0;
    for (;;) {
        read_and_print_sum(&i);
    }
    return 0;
}'''})

PART.append({"id": "R63b80bd2a7", "task": "refactor", "output": r'''public static void main (String [] args) {
    if (args.length != 2) {
        System.out.println ("usage: ./zipf size skew");
        System.exit (-1);
        return;
    }
    ZipfGenerator zipf = new ZipfGenerator (Integer.valueOf (args [0]), Double.valueOf (args [1]));
    printProbabilities (zipf);
    testDistribution (zipf);
}

private static void printProbabilities (ZipfGenerator zipf) {
    for (int i = 1; i <= 10; i ++) {
        System.out.println (i + " " + zipf.getProbability (i));
    }
}

private static void testDistribution (ZipfGenerator zipf) {
    int [] hist = new int [12];
    Arrays.fill (hist, 0);
    System.out.println ("Testing the probability distribution:");
    for (int i = 1; i <= 1000000; i ++) {
        hist [zipf.next ()] ++;
    }
    for (int i = 0; i < hist.length; i ++) {
        System.out.println (i + " " + hist [i] / 1000000.0);
    }
}'''})

PART.append({"id": "R4a34d3a4cc", "task": "refactor", "output": r'''def binary_search(L, x):
    low, high = 0, len(L)
    while low < high:
        mid = (low + high) // 2
        if L[mid] < x:
            low = mid + 1
        else:
            high = mid
    if low < len(L) and L[low] == x:
        return low
    return -1'''})

PART.append({"id": "R359253b811", "task": "refactor", "output": r'''public Component getTableCellEditorComponent (JTable table, Object value, boolean isSelected, int row, int col) {
    Component comp = super.getTableCellEditorComponent (table, value, isSelected, row, col);
    if (! (value instanceof java.lang.String)) {
        return comp;
    }
    return createReadOnlyPane ((String) value);
}

private JTextPane createReadOnlyPane (String text) {
    DefaultStyledDocument sty_doc = new DefaultStyledDocument ();
    try {
        sty_doc.insertString (0, text, null);
    } catch (BadLocationException e) {
        e.printStackTrace ();
    }
    JTextPane pane = new JTextPane (sty_doc);
    pane.setEditable (false);
    return pane;
}'''})

PART.append({"id": "R1cabb3fa54", "task": "refactor", "output": r'''def access(obj, indexes):
    current = obj
    for index in indexes:
        try:
            current = list.__getitem__(current, index)
        except Exception:
            return None
    return current'''})

PART.append({"id": "R7da0cb9ba0", "task": "refactor", "output": r'''public string GetResultsWithHyphen (string inText) {
    var sb = new StringBuilder ();
    for (int counter = 0; counter < inText.Length; counter ++) {
        if (counter % 4 == 0) {
            sb.Append (sb.ToString ()).Append ("-").Append (inText.Substring (counter, 1));
        } else {
            sb.Append (inText.Substring (counter, 1));
        }
    }
    return sb.ToString ();
}'''})

PART.append({"id": "R17e5e197a9", "task": "refactor", "output": r'''def recurse(node, depth, parent):
    global k
    indent = "  " * depth
    if tree_.feature [node] == _tree.TREE_UNDEFINED :
        k = k + 1
        print (k, ')', pathto [parent], tree_.value [node])
        return
    name = feature_name [node]
    threshold = tree_.threshold [node]
    s = "{} <= {} ".format(name, threshold, node)
    pathto [node] = s if node == 0 else pathto [parent] + ' & ' + s
    recurse(tree_.children_left [node], depth + 1, node)
    s = "{} > {}".format(name, threshold)
    pathto [node] = s if node == 0 else pathto [parent] + ' & ' + s
    recurse(tree_.children_right [node], depth + 1, node)'''})

PART.append({"id": "R0c1c130c91", "task": "refactor", "output": r'''static void print_repeat (const char *s, int times) {
    while (times-- > 0) {
        fputs (s, stdout);
    }
}

int main () {
    int i = 0;
    while (i < 6) {
        print_repeat ("+", 5 - i);
        print_repeat ("*", i);
        putchar ('\n');
        i ++;
    }
    return 0;
}'''})
