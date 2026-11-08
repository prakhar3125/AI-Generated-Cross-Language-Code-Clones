# -*- coding: utf-8 -*-
DATA6 = {
"R3b3bb0bfa8": r'''
int main(void) {
    pthread_t tid;
    thread_data tdata = {.a = 10, .b = 32};
    if (pthread_create(&tid, NULL, myThread, (void *) &tdata) != 0) {
        fprintf(stderr, "pthread_create failed\n");
        return 1;
    }
    pthread_join(tid, NULL);
    printf("%d + %d = %d\n", tdata.a, tdata.b, tdata.result);
    return 0;
}
''',
"R70b5cc83a3": r'''
public void draw (Graphics2D g) {
    BasicStroke stroke = (BasicStroke) g.getStroke ();
    float arrowRatio = 0.5f;
    float arrowLength = 80.0f;
    float endX = 350.0f;
    float veeX = endX - stroke.getLineWidth () * 0.5f / arrowRatio;
    g.setColor (Color.BLUE);
    g.fill (createArrowPath (veeX, endX, arrowLength, arrowRatio));
    g.setColor (Color.RED);
    g.draw (new Line2D.Float (50.0f, 0.0f, veeX - arrowLength * 0.5f, 0.0f));
}

private static Path2D.Float createArrowPath (float veeX, float endX, float arrowLength, float arrowRatio) {
    Path2D.Float path = new Path2D.Float ();
    float waisting = 0.5f;
    float waistX = endX - arrowLength * 0.5f;
    float waistY = arrowRatio * arrowLength * 0.5f * waisting;
    float arrowWidth = arrowRatio * arrowLength;
    path.moveTo (veeX - arrowLength, - arrowWidth);
    path.quadTo (waistX, - waistY, endX, 0.0f);
    path.quadTo (waistX, waistY, veeX - arrowLength, arrowWidth);
    path.lineTo (veeX - arrowLength * 0.75f, 0.0f);
    path.closePath ();
    return path;
}
''',
"R9d7d058df5": r'''
public static void MoveDown (this TreeNode node) {
    TreeNodeCollection siblings;
    if (node.Parent != null) {
        siblings = node.Parent.Nodes;
    } else if (node.TreeView != null && node.TreeView.Nodes.Contains (node)) {
        siblings = node.TreeView.Nodes;
    } else {
        return;
    }
    int index = siblings.IndexOf (node);
    if (index >= siblings.Count - 1) {
        return;
    }
    siblings.RemoveAt (index);
    siblings.Insert (index + 1, node);
}
''',
"R59af819289": r'''
def all_pairs(lst):
    pairs = []
    if len(lst) <= 2:
        pairs.append(tuple(lst))
        return pairs

    def pad_odd(items):
        for candidate in (None, True):
            if candidate not in items:
                items.append(candidate)
                return candidate
        i = True
        while chr(i) in items:
            i += 1
        items.append(chr(i))
        return chr(i)

    if len(lst) % 2 != 0:
        PAD = pad_odd(lst)
    else:
        PAD = False
    a = lst[0]
    for i in range(1, len(lst)):
        pair = (a, lst[i])
        rest_list = lst[1:i] + lst[i + 1:]
        for rest in all_pairs(rest_list):
            pairs_list = [pair] + rest
            if PAD is not False:
                for j, tu in enumerate(pairs_list):
                    if PAD in tu:
                        pairs_list[j] = (tu[0],)
                        break
            pairs.append(pairs_list)
    return pairs
''',
"Rf952aa3c99": r'''
public int solution (int X, int [] A) {
    int sumV = X * (X + 1) / 2;
    int sum = 0;
    Set < Integer > seen = new HashSet < Integer > ();
    for (int iii = 0; iii < A.length; iii ++) {
        if (A [iii] <= X && seen.add (A [iii])) {
            sum += A [iii];
            if (sum == sumV) {
                return iii;
            }
        }
    }
    return - 1;
}
''',
"Rd199c3fba9": r'''
def validate_ip(ip_str):
    reg = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    return re.match(reg, ip_str) is not None
''',
"Rce31c46bb8": r'''
static int product_of_proper_divisors (int inputNumber) {
    int j = 1;
    int prod = 1;
    while (j < inputNumber) {
        if (inputNumber % j == 0) {
            prod *= j;
        }
        j++;
    }
    return prod;
}

int main (void) {
    int numberOfInputs;
    scanf ("%d", & numberOfInputs);
    for (int i = 1; i <= numberOfInputs; i++) {
        int inputNumber;
        scanf ("%d", & inputNumber);
        printf ("%04d\n", product_of_proper_divisors (inputNumber) % 10000);
    }
    return 0;
}
''',
"R8655349b09": r'''
public static void CountbyChar (String s) {
    HashMap < Character, Integer > letterCountMap = new HashMap < Character, Integer > ();
    for (char c : s.toCharArray ()) {
        letterCountMap.merge (c, 1, Integer::sum);
    }
    for (Entry < Character, Integer > entry : letterCountMap.entrySet ()) {
        System.out.println (entry.getValue () + "( for" + entry.getKey () + " )");
    }
}
''',
"R6ec2173375": r'''
def treeToList(node, order=Order.INORDER):
    if node is None:
        return []
    right = treeToList(node.right, order)
    down = treeToList(node.down, order)
    current = [node.data]
    parts = {
        Order.PREORDER: current + right + down,
        Order.POSTORDER: right + down + current,
        Order.INORDER: right + current + down,
    }
    if order not in parts:
        return None
    return parts[order]
''',
"R998677b1ab": r'''
int main (void) {
    FILE *fp = fopen (FILE_NAME, "r");
    if (fp == NULL) {
        perror ("fopen failed");
        exit (EXIT_FAILURE);
    }
    int count = 0;
    while (fgets (words [count], MAX_COLUMNS, fp) != NULL) {
        words [count][strlen (words [count]) - 1] = '\0';
        count++;
    }
    fclose (fp);
    bubbleSortWordsArray (count);
    printWordsArray (count);
    return (0);
}
''',
"Rbef72fa071": r'''
public static int score (final String gene1, final String gene2) {
    return score (gene1.toCharArray (), gene2.toCharArray (), 0, 0);
}
''',
"Rc80ff5796f": r'''
public static boolean twoDuplicates (int [] values) {
    for (int i = 0; i < values.length; i ++) {
        if (hasTwoLaterMatches (values, i)) {
            return true;
        }
    }
    return false;
}

private static boolean hasTwoLaterMatches (int [] values, int index) {
    int counter = 0;
    for (int z = index + 1; z < values.length; z ++) {
        if (values [index] == values [z]) {
            counter ++;
            if (counter == 2) return true;
        }
    }
    return false;
}
''',
"Re56d31c78d": r'''
public static void Dispose(this MethodBuilder mb) {
    if (mb == null)
        return;
    Type mbType = typeof (MethodBuilder);
    FieldInfo mbILGen = mbType.GetField("m_ilGenerator", BindingFlags.Instance | BindingFlags.NonPublic);
    FieldInfo mbMod = mbType.GetField("m_module", BindingFlags.Instance | BindingFlags.NonPublic);
    FieldInfo mbContType = mbType.GetField("m_containingType", BindingFlags.Instance | BindingFlags.NonPublic);
    FieldInfo mbLocSigHelp = mbType.GetField("m_localSignature", BindingFlags.Instance | BindingFlags.NonPublic);
    FieldInfo mbSigHelp = mbType.GetField("m_signature", BindingFlags.Instance | BindingFlags.NonPublic);
    mbContType.SetValue(mb, null);
    DisposeFieldAndClear(mb, mbMod);
    DisposeFieldAndClear(mb, mbLocSigHelp);
    DisposeFieldAndClear(mb, mbSigHelp);
    DisposeFieldAndClear(mb, mbILGen);
}

private static void DisposeFieldAndClear(MethodBuilder mb, FieldInfo field) {
    IDisposable temp = (IDisposable) field.GetValue(mb);
    temp.Dispose();
    field.SetValue(mb, null);
}
'''
}
