TRANSLATIONS_C = {
    "T249": {
        "python": r'''def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        if ar[i] > 0:
            ch = chr(i)
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + str(ar[i]), end="")''',
        "c": r'''#include <stdio.h>

int main(void) {
    int ar[256] = {0};
    printf("Enter the String");
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
        ar[c]++;
    }
    for (int i = 0; i < 256; i++) {
        if (ar[i] > 0) {
            if (ar[i] == 1) {
                printf("%c", i);
            } else {
                printf("%c%d", i, ar[i]);
            }
        }
    }
    return 0;
}''',
        "csharp": r'''using System;

public static class CharCounter
{
    public static void Main()
    {
        Console.Write("Enter the String");
        string st = Console.ReadLine();
        int[] ar = new int[256];
        foreach (char ch in st)
        {
            ar[ch]++;
        }
        for (int i = 0; i < 256; i++)
        {
            if (ar[i] > 0)
            {
                char ch = (char) i;
                if (ar[i] == 1)
                {
                    Console.Write(ch);
                }
                else
                {
                    Console.Write(ch.ToString() + ar[i]);
                }
            }
        }
    }
}'''
    },
    "T372": {
        "python": r'''def capitalize(s):
    if s is None or len(s) == 0:
        return ""
    first = s[0]
    if first.isupper():
        return s
    return first.upper() + s[1:]''',
        "c": r'''#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char *capitalize(const char *s) {
    static char empty[] = "";
    if (s == NULL || s[0] == '\0') {
        return empty;
    }
    size_t n = strlen(s);
    char *out = (char *) malloc(n + 1);
    if (out == NULL) return NULL;
    if (isupper((unsigned char) s[0])) {
        strcpy(out, s);
        return out;
    }
    out[0] = (char) toupper((unsigned char) s[0]);
    strcpy(out + 1, s + 1);
    return out;
}''',
        "csharp": r'''public static class Capitalizer
{
    public static string capitalize(string s)
    {
        if (string.IsNullOrEmpty(s))
        {
            return "";
        }
        char first = s[0];
        if (char.IsUpper(first))
        {
            return s;
        }
        return char.ToUpper(first) + s.Substring(1);
    }
}'''
    },
    "T60": {
        "python": r'''def is_permutation(str1, str2):
    x = sorted(str1)
    y = sorted(str2)
    if x == y:
        return True
    return False''',
        "c": r'''#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static int compare_chars(const void *a, const void *b) {
    return (int) (*(const char *) a) - (*(const char *) b);
}

bool isPermutation(const char *str1, const char *str2) {
    size_t n1 = strlen(str1);
    size_t n2 = strlen(str2);
    if (n1 != n2) return false;
    char *x = (char *) malloc(n1 + 1);
    char *y = (char *) malloc(n2 + 1);
    if (x == NULL || y == NULL) {
        free(x);
        free(y);
        return false;
    }
    strcpy(x, str1);
    strcpy(y, str2);
    qsort(x, n1, sizeof(char), compare_chars);
    qsort(y, n2, sizeof(char), compare_chars);
    bool equal = strcmp(x, y) == 0;
    free(x);
    free(y);
    return equal;
}''',
        "csharp": r'''using System;
using System.Linq;

public static class PermutationChecker
{
    public static bool isPermutation(string str1, string str2)
    {
        char[] x = str1.ToCharArray();
        char[] y = str2.ToCharArray();
        Array.Sort(x);
        Array.Sort(y);
        return x.SequenceEqual(y);
    }
}'''
    },
    "T172": {
        "python": r'''import urllib.request


def is_available():
    request = urllib.request.Request("URL HERE", headers={"Connection": "close"})
    response = urllib.request.urlopen(request, timeout=10)
    return response.getcode() == 200''',
        "c": r'''#include <stdbool.h>

extern int http_get_status_code(const char *url, int connect_timeout_ms);

bool is_available(void) {
    return http_get_status_code("URL HERE", 10000) == 200;
}''',
        "csharp": r'''using System.Net;

public class AvailabilityChecker
{
    public bool isAvailable()
    {
        HttpWebRequest connection = (HttpWebRequest) WebRequest.Create("URL HERE");
        connection.Headers.Add("Connection", "close");
        connection.Timeout = 10000;
        using (HttpWebResponse response = (HttpWebResponse) connection.GetResponse())
        {
            return (int) response.StatusCode == 200;
        }
    }
}'''
    },
    "T713": {
        "python": r'''def get_drawable(context, res_id):
    raise NotImplementedError("stand-in for ContextCompat.getDrawable")


class Drawable:
    def __init__(self):
        self.colorFilter = None

    def set_color_filter(self, color, mode):
        self.colorFilter = (color, mode)


class Editor:
    def __init__(self):
        self.mCursorDrawable = None


class EditText:
    def __init__(self):
        self.mCursorDrawableRes = 0
        self.mEditor = Editor()
        self.context = None

    def get_context(self):
        return self.context


def set_cursor_color(view, color):
    try:
        drawable_res_id = view.mCursorDrawableRes
        editor = view.mEditor
        drawable = get_drawable(view.get_context(), drawable_res_id)
        drawable.set_color_filter(color, "SRC_IN")
        editor.mCursorDrawable = [drawable, drawable]
    except Exception:
        pass''',
        "c": r'''#include <stddef.h>

typedef struct Drawable Drawable;
typedef struct Context Context;
typedef struct Editor Editor;
typedef struct EditText EditText;

struct EditText {
    int mCursorDrawableRes;
    Context *context;
    Editor *mEditor;
};

struct Editor {
    Drawable *mCursorDrawable[2];
};

extern Drawable *context_compat_get_drawable(Context *context, int resId);
extern void drawable_set_color_filter(Drawable *drawable, int color, int mode);

void set_cursor_color(EditText *view, int color) {
    int drawableResId = view->mCursorDrawableRes;
    Editor *editor = view->mEditor;
    Drawable *drawable = context_compat_get_drawable(view->context, drawableResId);
    drawable_set_color_filter(drawable, color, 1);
    editor->mCursorDrawable[0] = drawable;
    editor->mCursorDrawable[1] = drawable;
}''',
        "csharp": r'''using System;

public class ContextCompat
{
    public static object GetDrawable(object context, int resId) { return null; }
}

public class PorterDuff
{
    public enum Mode { SrcIn }
}

public class CursorHelper
{
    public static void setCursorColor(EditText view, int color)
    {
        try
        {
            int drawableResId = view.mCursorDrawableRes;
            object editor = view.mEditor;
            object drawable = ContextCompat.GetDrawable(view.getContext(), drawableResId);
            drawable.GetType().GetMethod("SetColorFilter").Invoke(drawable, new object[] { color, PorterDuff.Mode.SrcIn });
            editor.GetType().GetField("mCursorDrawable").SetValue(editor, new[] { drawable, drawable });
        }
        catch (Exception)
        {
        }
    }
}'''
    }
}

REFACTORS_A = {
    "Rbf38b9a69d": r'''private void transform (XSSFWorkbook workbookOld, HSSFWorkbook workbookNew, Integer hash, XSSFCellStyle styleOld, HSSFCellStyle styleNew) {
    copyBorders (styleOld, styleNew);
    styleNew.setAlignment (styleOld.getAlignment ());
    styleNew.setDataFormat (this.transform (workbookOld, workbookNew, styleOld.getDataFormat ()));
    styleNew.setFillBackgroundColor (styleOld.getFillBackgroundColor ());
    styleNew.setFillForegroundColor (styleOld.getFillForegroundColor ());
    styleNew.setFillPattern (styleOld.getFillPattern ());
    styleNew.setFont (this.transform (workbookNew, (XSSFFont) styleOld.getFont ()));
    copyFlags (styleOld, styleNew);
    styleNew.setVerticalAlignment (styleOld.getVerticalAlignment ());
    styleNew.setWrapText (styleOld.getWrapText ());
    this.styleMap.put (hash, styleNew);
}

private void copyBorders (XSSFCellStyle oldStyle, HSSFCellStyle newStyle) {
    newStyle.setBorderBottom (oldStyle.getBorderBottom ());
    newStyle.setBorderLeft (oldStyle.getBorderLeft ());
    newStyle.setBorderRight (oldStyle.getBorderRight ());
    newStyle.setBorderTop (oldStyle.getBorderTop ());
}

private void copyFlags (XSSFCellStyle oldStyle, HSSFCellStyle newStyle) {
    newStyle.setHidden (oldStyle.getHidden ());
    newStyle.setIndention (oldStyle.getIndention ());
    newStyle.setLocked (oldStyle.getLocked ());
}''',
    "Rb9c3635eed": r'''public static void main (String args []) {
    inp = new Scanner (System.in);
    String str = inp.nextLine ();
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
}''',
    "Rea67761d7d": r'''public static void main (String [] args) {
    String [] samples = {"", null, "Starts with upper case", "starts with lower case"};
    for (String sample : samples) {
        System.out.println (startWithUpperCase (sample));
    }
}''',
    "R357f96f327": r'''public static DataTable GetWorksheetAsDataTable(ExcelWorksheet worksheet) {
    DataTable dt = new DataTable(worksheet.Name);
    dt.Columns.AddRange(GetDataColumns(worksheet).ToArray());
    int width = dt.Columns.Count;
    int depth = GetTableDepth(worksheet, 1);
    for (int rowNum = 2; rowNum <= depth + 1; rowNum++)
        dt.Rows.Add(ExtractRow(worksheet, dt, rowNum, width));
    return dt;
}

private static DataRow ExtractRow(ExcelWorksheet worksheet, DataTable dt, int rowNum, int width) {
    DataRow row = dt.NewRow();
    for (int colNum = 1; colNum <= width; colNum++) {
        object val = worksheet.Cells[rowNum, colNum].Value;
        row[colNum - 1] = val == null ? null : val.ToString();
    }
    return row;
}''',
    "Re3d1dfab68": r'''def create_lookup_list(messages, labels):
    return [{"message": m, "label": l} for m, l in zip(messages, labels)]''',
    "Rfe9a432a46": r'''public override void OnException (ExceptionContext filterContext) {
    filterContext.HttpContext.Response.TrySkipIisCustomErrors = true;
    filterContext.ExceptionHandled = true;
    filterContext.HttpContext.Response.ClearContent ();
    filterContext.Result = BuildErrorView (filterContext);
    filterContext.Exception = null;
}

private static ViewResult BuildErrorView (ExceptionContext filterContext) {
    var routeData = filterContext.RouteData.Values;
    var model = new HandleErrorInfo (filterContext.Exception,
        (string) routeData ["controller"], (string) routeData ["action"]);
    return new ViewResult {ViewName = View, MasterName = Master, ViewData = new ViewDataDictionary < HandleErrorInfo > (model), TempData = filterContext.Controller.TempData};
}''',
    "Rb8f6c8b5d0": r'''#include <ctype.h>
#include <stdio.h>

#define MAX_LINE 1000

static int parse_input(const char *s, char *alp, int *num) {
    int m = 0, n = 0, i = 0;
    while (s[i]) {
        unsigned char ch = s[i];
        if (isalpha(ch)) {
            alp[n++] = s[i++];
        } else if (isdigit(ch)) {
            int value = 0;
            while (isdigit((unsigned char) s[i])) {
                value = value * 10 + (s[i] - '0');
                ++i;
            }
            num[m] = value;
            ++m;
        } else {
            printf("include invalid character (%c).\n", ch);
            return -1;
        }
    }
    return m;
}

int main(void) {
    char s[MAX_LINE], alp[MAX_LINE];
    int num[MAX_LINE];
    scanf("%999[^\n]", s);
    int m = parse_input(s, alp, num);
    if (m < 0) return -1;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < num[i]; j++)
            printf("%c", alp[i]);
    }
    puts("");
    return 0;
}''',
    "R8b80f20070": r'''#include <stdio.h>

int main(void) {
    double v;
    if (scanf("%lf", &v) == 1) {
        printf("%lf\n", v);
        return 0;
    }
    printf("read failed\n");
    return 0;
}''',
    "R4e335703d6": r'''#include <stdio.h>

#define SIZE 64

int main(void) {
    char s[SIZE];
    const char *months[] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    int result;
    printf("enter the month : ");
    gets(s);
    result = get_month(s, months);
    printf(result ? "%s - %d.  is the month of the year.\n" : "%s invalid\n", s, result);
    return 0;
}''',
    "R9fdda16e3c": r'''#include <stdio.h>

extern int getFirst(int n);

static int printFactors(int num, int showSum) {
    int x, sum = 0, tmp = num;
    do {
        x = getFirst(tmp);
        printf("%d ", x);
        sum += x;
        if (x == tmp)
            break;
        if (showSum)
            printf("+ ");
        tmp /= x;
    } while (1);
    return sum;
}

int main(void) {
    int num, sum;
    scanf("%d", &num);
    printf("Factors are: ");
    printFactors(num, 0);
    printf("\n");
    printf("Sum of factors is: ");
    sum = printFactors(num, 1);
    printf("= %d\n", sum);
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
    "R8d187f48ce": r'''def traceit(frame, event, arg):
    if event != "line":
        return traceit
    lineno = frame.f_lineno
    filename = frame.f_globals["__file__"]
    if filename == "<stdin>":
        filename = "traceit.py"
    if filename.endswith((".pyc", ".pyo")):
        filename = filename[:-1]
    line = linecache.getline(filename, lineno)
    print("%s:%s:%s: %s" % (frame.f_globals["__name__"], lineno, frame.f_code.co_name, line.rstrip()))
    return traceit''',
    "R00a4c22b00": r'''def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    queue = [iter(x) for x in iterables]
    while queue:
        for iterator in queue:
            item = next(iterator)
            yield item''',
    "R2710a37612": r'''public static final void main (String...aArgs) {
    log ("Generating 10 random integers in range 1..10.");
    Random randomGenerator = new Random ();
    java.util.stream.IntStream.rangeClosed (1, 10).forEach (idx -> showRandomInteger (1, 10, randomGenerator));
    log ("Done");
}''',
    "Rf6f525dc34": r'''static void Main (string [] args) {
    ProcessStartInfo procStartInfo = new ProcessStartInfo (getLibreOfficePath (), string.Format (CreateParamString (args)));
    SetProcessStartInfoProperties (procStartInfo);
    using (Process process = new Process {StartInfo = procStartInfo}) {
        ExecuteProcess (process);
        ValidateProcessExitCode (process);
    }
}''',
    "R6ea07c8787": r'''public static void Rename (this FileSystemInfo item, string newName) {
    if (item == null) {
        throw new ArgumentNullException ("item");
    }
    var fileInfo = item as FileInfo;
    if (fileInfo != null) {
        fileInfo.Rename (newName);
        return;
    }
    var directoryInfo = item as DirectoryInfo;
    if (directoryInfo != null) {
        directoryInfo.Rename (newName);
        return;
    }
    throw new ArgumentException ("Item", "Unexpected subclass of FileSystemInfo " + item.GetType ());
}''',
    "Rd744148380": r'''public void onRequestPermissionsResult (int requestCode, String permissions [], int [] grantResults) {
    super.onRequestPermissionsResult (requestCode, permissions, grantResults);
    if (grantResults.length == 0 || grantResults == null) {
        return;
    }
    switch (grantResults [0]) {
        case PackageManager.PERMISSION_GRANTED:
            break;
        case PackageManager.PERMISSION_DENIED:
            break;
    }
}''',
    "R51669e3825": r'''def __init__(self):
    self.__dict__.update({
        "secondsRemaining": 10.0,
        "lastTick": 0,
        "isPaused": False,
        "isRunning": False,
        "keepGoing": True,
    })''',
}
