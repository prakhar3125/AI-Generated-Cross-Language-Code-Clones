PART = []

PART.append({"id": "R9f056ca258", "task": "refactor", "output": r'''private void printTree (OutputStreamWriter out, boolean isRight, String indent) throws IOException {
    String branchIndent = isRight ? "        " : " |      ";
    if (right != null) {
        right.printTree (out, true, indent + branchIndent);
    }
    out.write (indent);
    out.write (isRight ? "/" : " \\");
    out.write ("----- ");
    printNodeValue (out);
    if (left != null) {
        left.printTree (out, false, indent + (isRight ? " |      " : "        "));
    }
}'''})

PART.append({"id": "Rda752e8442", "task": "refactor", "output": r'''def mssl(l):
    best = cur = 0
    curi = starti = besti = 0
    for ind, i in enumerate(l):
        if cur + i <= 0:
            cur, curi = 0, ind + 1
        else:
            cur += i
        if cur > best:
            starti, besti, best = curi, ind + 1, cur
    return (starti, besti, best)'''})

PART.append({"id": "Ra2d10bef4b", "task": "refactor", "output": r'''private void Dispose (bool disposing) {
    if (disposedValue) {
        return;
    }
    if (disposing) {
    }
    FreeTextureStack ();
    disposedValue = true;
}

private void FreeTextureStack () {
    if (m_freeStack == null) {
        return;
    }
    SharpDX.Direct3D11.Texture2D texture;
    while (m_freeStack.TryPop (out texture)) {
        texture.Dispose ();
    }
    m_freeStack = null;
}'''})

PART.append({"id": "Rb2a2baaff7", "task": "refactor", "output": r'''public static void main (String [] args) {
    java.util.BitSet bits = new java.util.BitSet ();
    bits.set (1, 101);
    String set = bits.toString ();
    System.out.append (set, 1, set.length () - 1);
}'''})

PART.append({"id": "R20dd558187", "task": "refactor", "output": r'''static void trim_newline (char *x, size_t *len) {
    if (*len > 0 && x [*len - 1] == '\n') {
        x [--*len] = '\0';
    }
}

int main (void) {
    char *strings [10] = {}, *x;
    int i;
    size_t len;
    puts ("Enter 10 strings:");
    for (i = 0; i < 10; ++i) {
        getline (&strings [i], &len, stdin);
    }
    puts ("The strings that end with ed are:");
    for (i = 0; i < 10; ++i) {
        if (! (x = strings [i])) {
            continue;
        }
        len = strlen (x);
        trim_newline (x, &len);
        if (len > 1 && strcmp (x + len - 2, "ed") == 0) {
            puts (x);
        }
        free (x);
    }
    return 0;
}'''})

PART.append({"id": "R5b8db4fec9", "task": "refactor", "output": r'''public override void Write (string value) {
    if (_bufferState == 0) {
        base.Write (value);
        return;
    }
    if (value == AmpToken) {
        _bufferState ++;
        return;
    }
    _bufferState = 0;
    base.Write ("&");
    base.Write (value);
}'''})

PART.append({"id": "R8d0d71b76a", "task": "refactor", "output": r'''public static string Format (this TimeSpan obj) {
    var parts = new List < string > ();
    void AddPart (int value, string label) {
        parts.Add (value + " " + label + " ");
    }
    if (obj.Hours != 0) {
        AddPart (obj.Hours, "hours");
    }
    if (obj.Minutes != 0 || parts.Count != 0) {
        AddPart (obj.Minutes, "minutes");
    }
    if (obj.Seconds != 0 || parts.Count != 0) {
        AddPart (obj.Seconds, "seconds");
    }
    if (obj.Milliseconds != 0 || parts.Count != 0) {
        AddPart (obj.Milliseconds, "Milliseconds");
    }
    if (parts.Count == 0) {
        AddPart (0, "Milliseconds");
    }
    return string.Concat (parts);
}'''})

PART.append({"id": "R241b8d374d", "task": "refactor", "output": r'''protected override void CalculateBiQuadCoefficients () {
    double k = Math.Tan (Math.PI * Frequency / SampleRate);
    double denominator = 1 + k / Q + k * k;
    double norm = 1.0 / denominator;
    A0 = (1 + k * k) * norm;
    A2 = A0;
    A1 = 2 * (k * k - 1) * norm;
    B1 = A1;
    B2 = (1 - k / Q + k * k) * norm;
}'''})
