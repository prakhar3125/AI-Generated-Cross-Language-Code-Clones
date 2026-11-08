DATA4 = {
"T512": {
 "python": r'''def find_min(a, c):
    x = a[c]
    position = c
    while c < len(a):
        if x > a[c]:
            x = a[c]
            position = c
        c += 1
    return position''',
 "c": r'''int findMIN(const int *A, int len, int c) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}''',
 "csharp": r'''public static int FindMIN(int[] A, int c) {
    int x = A[c];
    int position = c;
    while (c < A.Length) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}'''
},
"T14": {
 "python": r'''class Node:
    def __init__(self):
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def reverse(self, previous, current):
        if previous is None:
            return None
        if previous is self.head:
            previous.next = None
        if current is None:
            self.head = previous
            return self.head
        else:
            temp = current.next
            current.next = previous
            self.reverse(current, temp)
        return None''',
 "c": r'''struct Node {
    struct Node *next;
};

struct List {
    struct Node *head;
};

struct Node *reverse(struct List *list, struct Node *previous, struct Node *current) {
    if (previous == NULL) return NULL;
    if (previous == list->head) previous->next = NULL;
    if (current == NULL) {
        list->head = previous;
        return list->head;
    } else {
        struct Node *temp = current->next;
        current->next = previous;
        reverse(list, current, temp);
    }
    return NULL;
}''',
 "csharp": r'''class Node {
    public Node Next;
}

class LinkedList {
    public Node Head;

    public Node Reverse(Node previous, Node current) {
        if (previous == null) return null;
        if (previous == Head) previous.Next = null;
        if (current == null) {
            Head = previous;
            return Head;
        } else {
            Node temp = current.Next;
            current.Next = previous;
            Reverse(current, temp);
        }
        return null;
    }
}'''
},
"T249": {
 "python": r'''def main():
    print("Enter the String", end="")
    st = input()
    ar = [0] * 256
    for ch in st:
        ar[ord(ch)] += 1
    for i in range(256):
        ch = chr(i)
        if ar[i] > 0:
            if ar[i] == 1:
                print(ch, end="")
            else:
                print(ch + str(ar[i]), end="")''',
 "c": r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char st[4096];
    int ar[256] = {0};
    printf("Enter the String");
    if (fgets(st, sizeof(st), stdin) == NULL) return 0;
    st[strcspn(st, "\n")] = '\0';
    for (const char *p = st; *p; p++) {
        ar[(unsigned char) *p]++;
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
}''',
 "csharp": r'''static void Main(string[] args) {
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
}'''
},
"T372": {
 "python": r'''def capitalize(self, s):
    if s is None or len(s) == 0:
        return ""
    first = s[0]
    if first.isupper():
        return s
    else:
        return first.upper() + s[1:]''',
 "c": r'''#include <ctype.h>
#include <stdio.h>
#include <string.h>

void capitalize(const char *s, char *out, size_t outSize) {
    if (s == NULL || s[0] == '\0') {
        out[0] = '\0';
        return;
    }
    if (isupper((unsigned char) s[0])) {
        snprintf(out, outSize, "%s", s);
    } else {
        snprintf(out, outSize, "%c%s", toupper((unsigned char) s[0]), s + 1);
    }
}''',
 "csharp": r'''private String Capitalize(String s) {
    if (s == null || s.Length == 0) {
        return "";
    }
    char first = s[0];
    if (char.IsUpper(first)) {
        return s;
    } else {
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
 "c": r'''#include <stdlib.h>
#include <string.h>

static int compare_chars(const void *a, const void *b) {
    return (int) (unsigned char) *(const char *) a - (int) (unsigned char) *(const char *) b;
}

int is_permutation(const char *str1, const char *str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    if (len1 != len2) return 0;
    char *x = malloc(len1 + 1);
    char *y = malloc(len2 + 1);
    strcpy(x, str1);
    strcpy(y, str2);
    qsort(x, len1, 1, compare_chars);
    qsort(y, len2, 1, compare_chars);
    int result = strcmp(x, y) == 0;
    free(x);
    free(y);
    return result;
}''',
 "csharp": r'''using System.Linq;

public static bool IsPermutation(string str1, string str2) {
    char[] x = str1.ToCharArray();
    char[] y = str2.ToCharArray();
    Array.Sort(x);
    Array.Sort(y);
    if (x.SequenceEqual(y)) return true;
    return false;
}'''
},
"T172": {
 "python": r'''import urllib.request

def is_available(self):
    url = "URL HERE"
    request = urllib.request.Request(url, headers={"Connection": "close"})
    try:
        connection = urllib.request.urlopen(request, timeout=10)
        return connection.getcode() == 200
    except Exception:
        return False''',
 "c": r'''typedef struct HttpConnection HttpConnection;
extern HttpConnection *http_connect(const char *url, int timeoutMs);
extern int http_response_code(HttpConnection *connection);
extern void http_disconnect(HttpConnection *connection);

int is_available(void) {
    HttpConnection *connection = http_connect("URL HERE", 10000);
    if (connection == NULL) {
        return 0;
    }
    int status = http_response_code(connection);
    http_disconnect(connection);
    return status == 200;
}''',
 "csharp": r'''using System.Net;

public bool IsAvailable() {
    var request = (HttpWebRequest) WebRequest.Create("URL HERE");
    request.KeepAlive = false;
    request.Timeout = 10000;
    using (var connection = (HttpWebResponse) request.GetResponse()) {
        if ((int) connection.StatusCode == 200) {
            return true;
        }
        return false;
    }
}'''
},
"T713": {
 "python": r'''class Field:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
    def setAccessible(self, value):
        pass
    def getInt(self, obj):
        return obj._fields[self.name]
    def get(self, obj):
        return obj._fields[self.name]
    def set(self, obj, value):
        obj._fields[self.name] = value

class Editor:
    _fields = {}
    @staticmethod
    def getDeclaredField(name):
        return Field(Editor, name)

class TextView:
    @staticmethod
    def getDeclaredField(name):
        return Field(TextView, name)
    def getContext(self):
        return None

class Drawable:
    def setColorFilter(self, color, mode):
        pass

class ContextCompat:
    @staticmethod
    def getDrawable(context, resId):
        return Drawable()

class PorterDuff:
    class Mode:
        SRC_IN = "src_in"

def set_cursor_color(view, color):
    try:
        field = TextView.getDeclaredField("mCursorDrawableRes")
        field.setAccessible(True)
        drawable_res_id = field.getInt(view)
        field = TextView.getDeclaredField("mEditor")
        field.setAccessible(True)
        editor = Editor()
        drawable = ContextCompat.getDrawable(view.getContext(), drawable_res_id)
        drawable.setColorFilter(color, PorterDuff.Mode.SRC_IN)
        drawables = [drawable, drawable]
        field = editor.getDeclaredField("mCursorDrawable")
        field.setAccessible(True)
        field.set(editor, drawables)
    except Exception:
        pass''',
 "c": r'''typedef struct View View;
typedef struct Editor Editor;
typedef struct Drawable Drawable;
typedef struct Field Field;

extern Field *class_get_declared_field(void *cls, const char *name);
extern void field_set_accessible(Field *field);
extern int field_get_int(Field *field, View *view);
extern void *field_get(Field *field, View *view);
extern void field_set(Field *field, void *obj, void *value);
extern Drawable *context_compat_get_drawable(void *context, int resId);
extern void drawable_set_color_filter(Drawable *d, int color, int mode);
extern void *view_get_context(View *view);
extern void *editor_class(void);

#define PORTER_DUFF_SRC_IN 1

void set_cursor_color(View *view, int color) {
    Field *field = class_get_declared_field(TextView_class, "mCursorDrawableRes");
    field_set_accessible(field);
    int drawableResId = field_get_int(field, view);
    field = class_get_declared_field(TextView_class, "mEditor");
    field_set_accessible(field);
    Editor *editor = (Editor *) field_get(field, view);
    Drawable *drawable = context_compat_get_drawable(view_get_context(view), drawableResId);
    drawable_set_color_filter(drawable, color, PORTER_DUFF_SRC_IN);
    Drawable *drawables[2];
    drawables[0] = drawable;
    drawables[1] = drawable;
    field = class_get_declared_field(editor_class(), "mCursorDrawable");
    field_set_accessible(field);
    field_set(field, editor, drawables);
}''',
 "csharp": r'''using System.Reflection;

public static void SetCursorColor(EditText view, int color) {
    try {
        var field = typeof(TextView).GetField("mCursorDrawableRes", BindingFlags.Instance | BindingFlags.NonPublic);
        int drawableResId = (int) field.GetValue(view);
        field = typeof(TextView).GetField("mEditor", BindingFlags.Instance | BindingFlags.NonPublic);
        var editor = field.GetValue(view);
        var drawable = ContextCompat.GetDrawable(view.GetContext(), drawableResId);
        drawable.SetColorFilter(color, PorterDuff.Mode.SrcIn);
        var drawables = new Drawable[] {drawable, drawable};
        field = editor.GetType().GetField("mCursorDrawable", BindingFlags.Instance | BindingFlags.NonPublic);
        field.SetValue(editor, drawables);
    } catch (Exception) {
    }
}'''
},
}
