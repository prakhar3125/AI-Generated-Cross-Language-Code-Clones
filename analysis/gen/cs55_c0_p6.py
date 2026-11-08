DATA_P6 = {}

DATA_P6["R3b3bb0bfa8"] = r'''
static void spawnAndJoin(thread_data *tdata, pthread_t *tid) {
    thread_data *pdata = tdata;
    if (pthread_create(tid, NULL, myThread, (void *)pdata) != 0) {
        fprintf(stderr, "thread creation failed\n");
        exit(EXIT_FAILURE);
    }
    pthread_join(*tid, NULL);
}

int main() {
    pthread_t tid;
    thread_data tdata = {.a = 10, .b = 32, .result = 0};
    spawnAndJoin(&tdata, &tid);
    printf("%d + %d = %d\n", tdata.a, tdata.b, tdata.result);
    return 0;
}
'''

DATA_P6["R70b5cc83a3"] = r'''
private Path2D.Float buildArrowPath(float veeX, float endX, float waistX, float waistY,
                                    float arrowWidth, float arrowLength) {
    Path2D.Float path = new Path2D.Float();
    path.moveTo(veeX - arrowLength, -arrowWidth);
    path.quadTo(waistX, -waistY, endX, 0.0f);
    path.quadTo(waistX, waistY, veeX - arrowLength, arrowWidth);
    path.lineTo(veeX - arrowLength * 0.75f, 0.0f);
    path.lineTo(veeX - arrowLength, -arrowWidth);
    return path;
}

public void draw(Graphics2D g) {
    float arrowRatio = 0.5f;
    float arrowLength = 80.0f;
    BasicStroke stroke = (BasicStroke) g.getStroke();
    float endX = 350.0f;
    float veeX = endX - stroke.getLineWidth() * 0.5f / arrowRatio;
    float waisting = 0.5f;
    float waistX = endX - arrowLength * 0.5f;
    float waistY = arrowRatio * arrowLength * 0.5f * waisting;
    float arrowWidth = arrowRatio * arrowLength;
    Path2D.Float path = buildArrowPath(veeX, endX, waistX, waistY, arrowWidth, arrowLength);
    g.setColor(Color.BLUE);
    g.fill(path);
    g.setColor(Color.RED);
    g.draw(new Line2D.Float(50.0f, 0.0f, veeX - arrowLength * 0.5f, 0.0f));
}
'''

DATA_P6["R9d7d058df5"] = r'''
public static void MoveDown(this TreeNode node)
{
    TreeNode parent = node.Parent;
    TreeView view = node.TreeView;
    TreeNodeCollection siblings = (parent != null)
        ? parent.Nodes
        : (view != null && view.Nodes.Contains(node) ? view.Nodes : null);
    if (siblings == null)
    {
        return;
    }
    int index = siblings.IndexOf(node);
    if (index >= siblings.Count - 1)
    {
        return;
    }
    siblings.RemoveAt(index);
    siblings.Insert(index + 1, node);
}
'''

DATA_P6["R59af819289"] = r'''
def _find_pad(lst):
    for candidate in (None, True):
        if candidate not in lst:
            lst.append(candidate)
            return candidate
    i = True
    while chr(i) in lst:
        i += 1
    lst.append(chr(i))
    return chr(i)


def all_pairs(lst):
    if not lst:
        return [tuple()]
    if len(lst) <= 2:
        return [tuple(lst)]
    pad = _find_pad(lst) if len(lst) % 2 != 0 else False
    pairs = []
    first = lst[0]
    for i in range(1, len(lst)):
        pair = (first, lst[i])
        rest_list = lst[1:i] + lst[i + 1:]
        for rest in all_pairs(rest_list):
            pairs_list = [pair] + rest
            if pad is not False:
                for j, tu in enumerate(pairs_list):
                    if pad in tu:
                        pairs_list[j] = (tu[0],)
                        break
            pairs.append(pairs_list)
    return pairs
'''

DATA_P6["Rf952aa3c99"] = r'''
public int solution (int X, int [] A) {
    int sumV = X * (X + 1) / 2;
    int sum = 0;
    Set < Integer > seen = new HashSet < Integer > ();
    for (int i = 0;
    i < A.length; i ++) {
        int v = A [i];
        if (v > X || ! seen.add (v)) continue;
        sum += v;
        if (sum == sumV) return i;
    }
    return - 1;
}
'''

DATA_P6["Rd199c3fba9"] = r'''
import re

IP_PATTERN = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")


def validate_ip(ip_str):
    return IP_PATTERN.match(ip_str) is not None
'''

DATA_P6["Rce31c46bb8"] = r'''
static long productOfProperDivisors(int inputNumber) {
    long prod = 1;
    int j = 1;
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
    if (scanf ("%d", & numberOfInputs) != 1) return 0;
    while (numberOfInputs-- > 0) {
        int inputNumber;
        scanf ("%d", & inputNumber);
        printf ("%04d\n", (int)(productOfProperDivisors (inputNumber) % 10000));
    }
    return 0;
}
'''

DATA_P6["R8655349b09"] = r'''
public static void CountbyChar (String s) {
    Map < Character, Integer > letterCountMap = new HashMap < Character, Integer > ();
    for (char c : s.toCharArray ()) {
        letterCountMap.merge (c, 1, Integer::sum);
    }
    for (Map.Entry < Character, Integer > entry : letterCountMap.entrySet ()) {
        System.out.println (entry.getValue () + "( for" + entry.getKey () + " )");
    }
}
'''

DATA_P6["R6ec2173375"] = r'''
def treeToList(node, order = Order.INORDER) :
	if node is None :
		return []
	current = [node.data]
	right = treeToList(node.right, order)
	down = treeToList(node.down, order)
	orderings = {
		Order.PREORDER : current + right + down,
		Order.INORDER : right + current + down,
		Order.POSTORDER : right + down + current,
	}
	return orderings.get(order)
'''

DATA_P6["R998677b1ab"] = r'''
static int readWords (FILE *fp) {
    int i = 0;
    while (fgets (words[i], MAX_COLUMNS, fp)) {
        words[i][strlen (words[i]) - 1] = '\0';
        i++;
    }
    return i;
}

int main (void) {
    FILE *fp = fopen (FILE_NAME, "r");
    if (fp == NULL) {
        perror ("fopen failed");
        exit (EXIT_FAILURE);
    }
    int count = readWords (fp);
    bubbleSortWordsArray (count);
    printWordsArray (count);
    return (0);
}
'''

DATA_P6["Rbef72fa071"] = r'''
public static int score (final String gene1, final String gene2) {
    return score (gene1.toCharArray (), gene2.toCharArray (), 0, 0);
}
'''

DATA_P6["Rc80ff5796f"] = r'''
public static boolean twoDuplicates (int [] values) {
    for (int i = 0;
    i < values.length; i ++) {
        int counter = 0;
        for (int z = values.length - 1;
        z > i; z --) {
            if (values [i] == values [z]) {
                counter ++;
                if (counter == 2) return true;
            }
        }
    }
    return false;
}
'''

DATA_P6["Re56d31c78d"] = r'''
private static FieldInfo GetField (Type type, string name) {
    return type.GetField (name, BindingFlags.Instance | BindingFlags.NonPublic);
}

private static void ClearField (Type type, object target, string name) {
    GetField (type, name).SetValue (target, null);
}

public static void Dispose (this MethodBuilder mb) {
    if (mb == null)
        return;
    Type mbType = typeof (MethodBuilder);
    ModuleBuilder tempMod = (ModuleBuilder) GetField (mbType, "m_module").GetValue (mb);
    tempMod.Dispose ();
    SignatureHelper tempLocSigHelp = (SignatureHelper) GetField (mbType, "m_localSignature").GetValue (mb);
    SignatureHelper tempSigHelp = (SignatureHelper) GetField (mbType, "m_signature").GetValue (mb);
    ILGenerator tempIlGen = (ILGenerator) GetField (mbType, "m_ilGenerator").GetValue (mb);
    ClearField (mbType, mb, "m_module");
    ClearField (mbType, mb, "m_containingType");
    tempLocSigHelp.Dispose ();
    ClearField (mbType, mb, "m_localSignature");
    tempSigHelp.Dispose ();
    ClearField (mbType, mb, "m_signature");
    tempIlGen.Dispose ();
    ClearField (mbType, mb, "m_ilGenerator");
}
'''
