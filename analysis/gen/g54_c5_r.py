# Refactor outputs for chunk 5, label gpt-5.4-mini
DATA_R = {}

DATA_R["Ra03011d81d"] = r'''#include <stdio.h>

extern int sum(int a, int b);

int main() {
    int a, b;
    int i = 1;
    for (;;) {
        if (scanf("%d %d", &a, &b) != 2) break;
        int total = sum(a + 1, b + 1);
        printf("%d: %d + %d = %d\n", i, a, b, total);
        i++;
    }
    return 0;
}'''

DATA_R["R63b80bd2a7"] = r'''public static void main(String[] args) {
    if (args.length != 2) {
        System.out.println("usage: ./zipf size skew");
        System.exit(-1);
    }
    ZipfGenerator zipf = new ZipfGenerator(Integer.valueOf(args[0]), Double.valueOf(args[1]));
    printProbabilities(zipf);
    System.out.println("Testing the probability distribution:");
    int[] hist = runHistogram(zipf, 1000000);
    printHistogram(hist);
}

private static void printProbabilities(ZipfGenerator zipf) {
    for (int i = 1; i <= 10; i++)
        System.out.println(i + " " + zipf.getProbability(i));
}

private static int[] runHistogram(ZipfGenerator zipf, int samples) {
    int[] hist = new int[12];
    java.util.Arrays.fill(hist, 0);
    for (int i = 0; i < samples; i++)
        hist[zipf.next()]++;
    return hist;
}

private static void printHistogram(int[] hist) {
    for (int i = 0; i < hist.length; i++)
        System.out.println(i + " " + hist[i] / 1000000.0);
}'''

DATA_R["R4a34d3a4cc"] = r'''def binary_search(L, x):
	lo = 0
	hi = len(L) - 1
	while lo <= hi:
		mid = (lo + hi) // 2
		if L[mid] < x:
			lo = mid + 1
		elif L[mid] > x:
			hi = mid - 1
		else:
			return mid
	return -1'''

DATA_R["R359253b811"] = r'''public Component getTableCellEditorComponent(JTable table, Object value, boolean isSelected, int row, int col) {
    Component comp = super.getTableCellEditorComponent(table, value, isSelected, row, col);
    if (!(value instanceof java.lang.String)) {
        return comp;
    }
    return createReadOnlyTextPane((String) value);
}

private JTextPane createReadOnlyTextPane(String text) {
    DefaultStyledDocument sty_doc = new DefaultStyledDocument();
    try {
        sty_doc.insertString(0, text, null);
    } catch (BadLocationException e) {
        e.printStackTrace();
    }
    JTextPane jtp_comp = new JTextPane(sty_doc);
    jtp_comp.setEditable(false);
    return jtp_comp;
}'''

DATA_R["R1cabb3fa54"] = r'''def access(obj, indexes):
	current = obj
	for index in indexes:
		try:
			current = current[index]
		except Exception:
			return None
	return current'''

DATA_R["R7da0cb9ba0"] = r'''public string GetResultsWithHyphen(string inText) {
    var sb = new StringBuilder();
    var counter = 0;
    while (counter < inText.Length) {
        string current = inText.Substring(counter, 1);
        if (counter % 4 == 0) {
            sb.Append(sb.ToString());
            sb.Append("-");
        }
        sb.Append(current);
        counter++;
    }
    return sb.ToString();
}'''

DATA_R["R17e5e197a9"] = r'''def recurse(node, depth, parent):
	global k
	indent = "  " * depth
	if tree_.feature[node] != _tree.TREE_UNDEFINED:
		name = feature_name[node]
		threshold = tree_.threshold[node]
		prefix = "" if node == 0 else pathto[parent] + " & "
		s = "{} <= {} ".format(name, threshold, node)
		pathto[node] = prefix + s
		recurse(tree_.children_left[node], depth + 1, node)
		s = "{} > {}".format(name, threshold)
		pathto[node] = prefix + s
		recurse(tree_.children_right[node], depth + 1, node)
	else:
		k = k + 1
		print(k, ')', pathto[parent], tree_.value[node])'''

DATA_R["R0c1c130c91"] = r'''#include <stdio.h>

static void printRepeated(char c, int n) {
    while (n-- > 0)
        putchar(c);
}

int main() {
    int i = 0;
    while (i < 6) {
        printRepeated('+', 5 - i);
        printRepeated('*', i);
        putchar('\n');
        i++;
    }
    return 0;
}'''

DATA_R["R1ab11e56ab"] = r'''import numpy as np


def future6(A):
	known = []
	result = []
	idx = len(A) - 1
	while idx >= 0:
		value = A[idx]
		known = [x for (x, y) in known if y > value]
		result.append(known[-1][0] if known else -1)
		known.append((idx, value))
		idx -= 1
	result.reverse()
	return np.array(result)'''

DATA_R["Rfbf7d4f5c2"] = r'''def stemming(verb):
	suffixes = {'ing', 'ed', 'es', 's'}
	return ''.join(ch for ch in verb if ch not in suffixes)'''

DATA_R["Rd908836b46"] = r'''#include <stdio.h>
#include <stdlib.h>

#define STRING_COUNT 50

void function(char **a);

char **allocateStrings(int count) {
    char **a = malloc(count * sizeof(char *));
    for (int i = 0; i < count; ++i)
        a[i] = malloc(10);
    return a;
}

int main(void) {
    char **a = allocateStrings(STRING_COUNT);
    function(a);
    for (int i = 0; i < 2; ++i)
        printf("a[%d]: %s\n", i, a[i]);
    return 0;
}'''

DATA_R["R63b6384687"] = r'''def merge(a, low, mid, high):
	left = a[low:mid + 1]
	right = a[mid + 1:high + 1]
	merged = []
	i = j = 0
	while i < len(left) and j < len(right):
		if left[i] <= right[j]:
			merged.append(left[i])
			i += 1
		else:
			merged.append(right[j])
			j += 1
	merged.extend(left[i:])
	merged.extend(right[j:])
	a[low:high + 1] = merged'''

DATA_R["R06eb22ea20"] = r'''public static void d(Exception e) {
    try {
        string methodName = DescribeMethod(e.TargetSite);
        StackTrace stkTrace = new System.Diagnostics.StackTrace(e, true);
        for (int i = 0; i < 3; i++) {
            if (TraceFrame(stkTrace, i, methodName, e))
                break;
        }
    }
    catch (Exception ee) {
        Console.WriteLine("Tracing exception in d(Exception e)" + ee.Message);
    }
}

private static string DescribeMethod(MethodBase site) {
    return site == null ? "" : ExtractBracketed(site.Name);
}

private static bool TraceFrame(StackTrace stkTrace, int index, string methodName, Exception e) {
    var frame = stkTrace.GetFrame(index);
    int lineNum = frame.GetFileLineNumber();
    int colNum = frame.GetFileColumnNumber();
    string className = ExtractBracketed(frame.GetMethod().ReflectedType.FullName);
    Trace.WriteLine(ThreadAndDateInfo + "Exception: " + className + "." + methodName + ", Ln " + lineNum + " Col " + colNum + ": " + e.Message);
    return lineNum + colNum > 0;
}'''

DATA_R["Reb0aa16636"] = r'''bool isPrime(int number) {
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    return hasNoOddDivisor(number, 3);
}

private bool hasNoOddDivisor(int number, int divisor) {
    if (divisor * divisor > number) return true;
    if (number % divisor == 0) return false;
    return hasNoOddDivisor(number, divisor + 2);
}'''

DATA_R["Rcfc9023e76"] = r'''public static void main(String[] args) {
    Scanner input = new Scanner(System.in);
    System.out.println("Enter a number");
    String number = input.nextLine();
    int total = 0;
    for (char c : number.toCharArray()) {
        int digit = c - '0';
        if (digit % 2 != 0 || digit == 1) {
            total += digit;
        }
    }
    System.out.println("The sum is " + total);
}'''

DATA_R["R7176808dc7"] = r'''protected override void CalculateBiQuadCoefficients() {
    double k = Math.Tan(Math.PI * Frequency / SampleRate);
    double kk = k * k;
    double kOverQ = k / Q;
    double scale = 1 / (1 + kOverQ + kk);
    A0 = kOverQ * scale;
    A1 = 0;
    A2 = -A0;
    B1 = 2 * (kk - 1) * scale;
    B2 = (1 - kOverQ + kk) * scale;
}'''

DATA_R["R5e98c898ba"] = r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef MAX_NAME_SZ
#define MAX_NAME_SZ 256
#endif

static void stripNewline(char *name) {
    size_t last = strlen(name);
    if (last > 0 && name[last - 1] == '\n')
        name[last - 1] = '\0';
}

int main(int argC, char *argV[]) {
    (void) argC;
    (void) argV;
    char *name = malloc(MAX_NAME_SZ);
    if (name == NULL) {
        printf("No memory\n");
        return 1;
    }
    printf("What is your name? ");
    if (fgets(name, MAX_NAME_SZ, stdin) == NULL) {
        free(name);
        return 1;
    }
    stripNewline(name);
    printf("Hello %s. Nice to meet you.\n", name);
    free(name);
    return 0;
}'''

DATA_R["R9f056ca258"] = r'''private void printTree(OutputStreamWriter out, boolean isRight, String indent) throws IOException {
    if (right != null) {
        right.printTree(out, true, childIndent(indent, !isRight));
    }
    out.write(indent);
    out.write(isRight ? " /" : " \\");
    out.write("----- ");
    printNodeValue(out);
    if (left != null) {
        left.printTree(out, false, childIndent(indent, isRight));
    }
}

private String childIndent(String indent, boolean extendsRight) {
    return indent + (extendsRight ? " |      " : "        ");
}'''

DATA_R["Rda752e8442"] = r'''def mssl(l):
	best = cur = 0
	curi = starti = besti = 0
	for ind, i in enumerate(l):
		cur, curi = advance(cur, curi, i, ind)
		if cur > best:
			starti, besti, best = curi, ind + 1, cur
	return starti, besti, best


def advance(cur, curi, value, ind):
	if cur + value > 0:
		return cur + value, curi
	return 0, ind + 1'''

DATA_R["Ra2d10bef4b"] = r'''private void Dispose(bool disposing) {
    if (disposedValue) return;
    if (disposing) {
    }
    ReleaseFreeTextures();
    disposedValue = true;
}

private void ReleaseFreeTextures() {
    if (m_freeStack == null) return;
    while (m_freeStack.TryPop(out SharpDX.Direct3D11.Texture2D texture)) {
        texture.Dispose();
    }
    m_freeStack = null;
}'''

DATA_R["Rb2a2baaff7"] = r'''public static void main(String[] args) {
    java.util.BitSet bits = new java.util.BitSet();
    bits.set(1, 100 + 1);
    String set = bits.toString();
    System.out.append(set, 1, set.length() - 1);
}'''

DATA_R["R20dd558187"] = r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int endsWithEd(char *x) {
    size_t len = strlen(x);
    if (len > 0 && x[len - 1] == '\n')
        x[--len] = '\0';
    return len > 1 && strcmp(x + len - 2, "ed") == 0;
}

int main(void) {
    char *strings[10] = {}, *x;
    int i;
    size_t len;
    puts("Enter 10 strings:");
    for (i = 0; i < 10; ++i)
        getline(&strings[i], &len, stdin);
    puts("The strings that end with ed are:");
    for (i = 0; i < 10; ++i) {
        if ((x = strings[i])) {
            if (endsWithEd(x))
                puts(x);
            free(x);
        }
    }
    return 0;
}'''

DATA_R["R5b8db4fec9"] = r'''public override void Write(string value) {
    if (_bufferState > 0) {
        if (value == AmpToken) {
            _bufferState++;
            return;
        }
        FlushAmpersand();
    }
    base.Write(value);
}

private void FlushAmpersand() {
    _bufferState = 0;
    base.Write("&");
}'''

DATA_R["R8d0d71b76a"] = r'''public static string Format(this TimeSpan obj) {
    StringBuilder sb = new StringBuilder();
    AppendPart(sb, obj.Hours, "hours", false);
    AppendPart(sb, obj.Minutes, "minutes", sb.Length != 0);
    AppendPart(sb, obj.Seconds, "seconds", sb.Length != 0);
    AppendPart(sb, obj.Milliseconds, "Milliseconds", sb.Length != 0);
    if (sb.Length == 0) {
        sb.Append(0);
        sb.Append(" Milliseconds");
    }
    return sb.ToString();
}

private static void AppendPart(StringBuilder sb, int value, string label, bool force) {
    if (value != 0 || force) {
        sb.Append(value);
        sb.Append(" ");
        sb.Append(label);
        sb.Append(" ");
    }
}'''

DATA_R["R241b8d374d"] = r'''protected override void CalculateBiQuadCoefficients() {
    double k = Math.Tan(Math.PI * Frequency / SampleRate);
    double kk = k * k;
    double norm = 1 / (1 + k / Q + kk);
    double gain = 2 * norm;
    A0 = (1 + kk) * norm;
    A1 = (kk - 1) * gain;
    A2 = A0;
    B1 = A1;
    B2 = (1 - (k / Q) + kk) * norm;
}'''
