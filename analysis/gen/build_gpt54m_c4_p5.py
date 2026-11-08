DATA_T5 = {}

DATA_T5["T249"] = {"outputs": {
"python": """def main():
    print("Enter the String", end="")
    st = input()
    counts = [0] * 256
    for ch in st:
        counts[ord(ch)] += 1
    for i in range(256):
        ch = chr(i)
        if counts[i] > 0:
            print(ch if counts[i] == 1 else ch + str(counts[i]), end="")
""",
"c": """int main(void) {
    char st[1024];
    int ar[256] = {0};
    printf("Enter the String");
    scanf("%1023s", st);
    for (size_t i = 0; i < strlen(st); i++) {
        ar[(unsigned char) st[i]]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", ch);
            } else {
                printf("%c%d", ch, ar[i]);
            }
        }
    }
    return 0;
}
""",
"csharp": """public static void Main(string[] args) {
    Console.Write("Enter the String");
    string st = Console.ReadLine();
    int[] ar = new int[256];
    foreach (char ch in st) {
        ar[ch]++;
    }
    for (int i = 0; i < 256; i++) {
        char ch = (char) i;
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                Console.Write(ch);
            } else {
                Console.Write(ch + "" + ar[i]);
            }
        }
    }
}
"""}}

DATA_T5["T372"] = {"outputs": {
"python": """def capitalize(s):
    if not s:
        return ""
    first = s[0]
    if first.isupper():
        return s
    return first.upper() + s[1:]
""",
"c": """char *capitalize(const char *s) {
    static char out[512];
    if (s == NULL || s[0] == '\\0') {
        out[0] = '\\0';
        return out;
    }
    if (isupper((unsigned char) s[0])) {
        strcpy(out, s);
    } else {
        out[0] = (char) toupper((unsigned char) s[0]);
        strcpy(out + 1, s + 1);
    }
    return out;
}
""",
"csharp": """private string Capitalize(string s) {
    if (string.IsNullOrEmpty(s)) {
        return "";
    }
    char first = s[0];
    return char.IsUpper(first) ? s : char.ToUpper(first) + s.Substring(1);
}
"""}}

DATA_T5["T60"] = {"outputs": {
"python": """def is_permutation(str1, str2):
    if sorted(str1) == sorted(str2):
        return True
    return False
""",
"c": """int is_permutation(const char *str1, const char *str2) {
    if (strlen(str1) != strlen(str2)) return 0;
    char x[256], y[256];
    strcpy(x, str1);
    strcpy(y, str2);
    qsort(x, strlen(x), 1, compare_chars);
    qsort(y, strlen(y), 1, compare_chars);
    return strcmp(x, y) == 0;
}

int compare_chars(const void *a, const void *b) {
    return *(const char *) a - *(const char *) b;
}
""",
"csharp": """public static bool IsPermutation(string str1, string str2) {
    char[] x = str1.ToCharArray();
    char[] y = str2.ToCharArray();
    Array.Sort(x);
    Array.Sort(y);
    return x.SequenceEqual(y);
}
"""}}

DATA_T5["T172"] = {"outputs": {
"python": """import urllib.request


def is_available(self):
    url = urllib.request.Request("URL HERE", headers={"Connection": "close"})
    try:
        response = urllib.request.urlopen(url, timeout=10)
        return response.status == 200
    except urllib.error.HTTPError as e:
        return e.code == 200
""",
"c": """int is_available(void) {
    int code = http_get_status("URL HERE", 10000);
    return code == 200;
}

int http_get_status(const char *url, int timeout_ms);
""",
"csharp": """public bool IsAvailable() {
    var url = new Uri("URL HERE");
    var connection = (HttpWebRequest) WebRequest.Create(url);
    connection.KeepAlive = false;
    connection.Timeout = 10000;
    using (var response = (HttpWebResponse) connection.GetResponse()) {
        return (int) response.StatusCode == 200;
    }
}
"""}}

DATA_T5["T713"] = {"outputs": {
"python": """def set_cursor_color(view, color):
    try:
        drawable = _get_drawable(view, color)
        view._cursor_drawables = (drawable, drawable)
    except Exception:
        pass


def _get_drawable(view, color):
    editor = getattr(view, "m_editor", None)
    drawable_res = getattr(view, "m_cursor_drawable_res", 0)
    drawable = get_drawable(view.context, drawable_res)
    drawable.set_color_filter(color, SRC_IN)
    return drawable
""",
"c": """void set_cursor_color(void *view, int color) {
    void *editor;
    int drawableResId;
    void *drawable;
    if (get_reflection_field(view, "mEditor", &editor) != 0) return;
    if (get_reflection_int(view, "mCursorDrawableRes", &drawableResId) != 0) return;
    drawable = compat_get_drawable(view_context(view), drawableResId);
    drawable_set_color_filter(drawable, color, SRC_IN);
    set_reflection_field(editor, "mCursorDrawable", drawable_pair(drawable, drawable));
}
""",
"csharp": """public static void SetCursorColor(EditText view, int color) {
    try {
        var field = typeof(TextView).GetDeclaredField("mCursorDrawableRes");
        field.Accessible = true;
        int drawableResId = field.GetInt(view);
        field = typeof(TextView).GetDeclaredField("mEditor");
        field.Accessible = true;
        object editor = field.Get(view);
        var drawable = ContextCompat.GetDrawable(view.Context, drawableResId);
        drawable.SetColorFilter(color, PorterDuff.Mode.SrcIn);
        field = editor.GetType().GetDeclaredField("mCursorDrawable");
        field.Accessible = true;
        field.Set(editor, new[] { drawable, drawable });
    } catch (Exception) {
    }
}
"""}}
