DATA5 = {}

DATA5["R3b3bb0bfa8"] = """void runPair(thread_data *tdata) {
    pthread_t tid;
    pthread_create(&tid, NULL, myThread, (void *)tdata);
    pthread_join(tid, NULL);
}

int main() {
    thread_data tdata = { .a = 10, .b = 32, .result = 0 };
    runPair(&tdata);
    printf("%d + %d = %d\\n", tdata.a, tdata.b, tdata.result);
    return 0;
}"""

DATA5["R70b5cc83a3"] = """private static final float ARROW_RATIO = 0.5f;
private static final float ARROW_LENGTH = 80.0f;
private static final float END_X = 350.0f;

public void draw(Graphics2D g) {
    BasicStroke stroke = (BasicStroke) g.getStroke();
    Path2D.Float path = buildArrow(stroke.getLineWidth());
    g.setColor(Color.BLUE);
    g.fill(path);
    g.setColor(Color.RED);
    g.draw(new Line2D.Float(50.0f, 0.0f, shaftEndX(stroke.getLineWidth()), 0.0f));
}

private float shaftEndX(float lineWidth) {
    return END_X - lineWidth * 0.5f / ARROW_RATIO;
}

private Path2D.Float buildArrow(float lineWidth) {
    float veeX = shaftEndX(lineWidth);
    float waistX = END_X - ARROW_LENGTH * 0.5f;
    float waistY = ARROW_RATIO * ARROW_LENGTH * 0.5f * 0.5f;
    float arrowWidth = ARROW_RATIO * ARROW_LENGTH;
    Path2D.Float path = new Path2D.Float();
    path.moveTo(veeX - ARROW_LENGTH, -arrowWidth);
    path.quadTo(waistX, -waistY, END_X, 0.0f);
    path.quadTo(waistX, waistY, veeX - ARROW_LENGTH, arrowWidth);
    path.lineTo(veeX - ARROW_LENGTH * 0.75f, 0.0f);
    path.closePath();
    return path;
}"""

DATA5["R9d7d058df5"] = """public static void MoveDown(this TreeNode node)
{
    TreeNodeCollection siblings = GetSiblings(node);
    if (siblings == null) return;
    int index = siblings.IndexOf(node);
    if (index < siblings.Count - 1)
    {
        siblings.RemoveAt(index);
        siblings.Insert(index + 1, node);
    }
}

private static TreeNodeCollection GetSiblings(TreeNode node)
{
    if (node.Parent != null) return node.Parent.Nodes;
    if (node.TreeView != null && node.TreeView.Nodes.Contains(node)) return node.TreeView.Nodes;
    return null;
}"""

DATA5["R59af819289"] = """def all_pairs(lst):
    if not lst:
        return [tuple()]
    if len(lst) <= 2:
        return [tuple(lst)]
    pairs = []
    pad, lst = _with_pad(lst)
    first = lst[0]
    for i in range(1, len(lst)):
        pair = (first, lst[i])
        rest_list = lst[1:i] + lst[i + 1:]
        for rest in all_pairs(rest_list):
            entry = [pair] + rest
            pairs.append(_collapse_pad(entry, pad))
    return pairs

def _with_pad(lst):
    if len(lst) % 2 == 0:
        return False, lst
    for i in (None, True):
        if i not in lst:
            lst.append(i)
            return i, lst
    i = 0
    while chr(i) in lst:
        i += 1
    pad = chr(i)
    lst.append(pad)
    return pad, lst

def _collapse_pad(entry, pad):
    if pad is not False:
        for j, tu in enumerate(entry):
            if pad in tu:
                entry[j] = (tu[0],)
                break
    return entry"""

DATA5["Rf952aa3c99"] = """public int solution (int X, int [] A) {
    Set < Integer > seen = new HashSet < Integer > ();
    int sum = 0;
    int targetSum = X * (X + 1) / 2;
    for (int i = 0;
    i < A.length; i ++) {
        int value = A [i];
        if (value <= X && seen.add (value)) {
            sum += value;
            if (sum == targetSum) {
                return i;
            }
        }
    }
    return - 1;
}"""

DATA5["Rd199c3fba9"] = """import re

IP_PATTERN = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

def validate_ip(ip_str):
    return IP_PATTERN.match(ip_str) is not None"""

DATA5["Rce31c46bb8"] = """int main (void) {
    int inputNumber, numberOfInputs;
    int prod = 1;
    if (scanf("%d", &numberOfInputs) != 1) return 0;
    int i = 0;
    while (i < numberOfInputs) {
        scanf("%d", &inputNumber);
        int j = 1;
        while (j < inputNumber) {
            if (inputNumber % j == 0) {
                prod *= j;
            }
            j++;
        }
        printf("%04d\\n", prod % 10000);
        i++;
    }
    return 0;
}"""

DATA5["R8655349b09"] = """public static void CountbyChar (String s) {
    HashMap < Character, Integer > letterCountMap = new HashMap < Character, Integer > ();
    for (char c : s.toCharArray ()) {
        letterCountMap.merge (c, 1, Integer::sum);
    }
    for (Map.Entry < Character, Integer > entry : letterCountMap.entrySet ()) {
        System.out.println (entry.getValue () + "( for" + entry.getKey () + " )");
    }
}"""
