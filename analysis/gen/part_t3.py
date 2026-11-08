PART = []

PART.append({"id": "T752", "task": "translate", "outputs": {
"python": r'''import xml.etree.ElementTree as ET

def main():
    try:
        tree = ET.parse("input.xml")
    except Exception:
        return
    root = tree.getroot()
    for item in root.iter("item"):
        name = item.get("name")
        if name is not None:
            print(" item name is ===>" + name)

main()''',
"c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char name[64]; char text[256]; } VTDEntry;
typedef struct { VTDEntry *entries; int count; } VTDNav;
typedef struct { VTDNav *nav; const char *xpath; } AutoPilot;

int vtd_parse_file(const char *path, int ns) {
    return path != NULL;
}

VTDNav *vtd_get_nav(void) {
    static VTDEntry entry;
    static VTDNav nav;
    strcpy(entry.name, "part");
    strcpy(entry.text, "value");
    nav.entries = &entry;
    nav.count = 1;
    return &nav;
}

void ap_select_xpath(AutoPilot *ap, const char *xpath) { ap->xpath = xpath; }
void ap_bind(AutoPilot *ap, VTDNav *nav) { ap->nav = nav; }

int ap_eval_xpath(AutoPilot *ap, int current) {
    int next = current + 1;
    return next < ap->nav->count ? next : -1;
}

int main(void) {
    VTDGen vg;
    if (!vtd_parse_file("input.xml", 0)) return 0;
    VTDNav *vn = vtd_get_nav();
    AutoPilot ap;
    ap_select_xpath(&ap, "/xml/item/@name");
    ap_bind(&ap, vn);
    int i = 0;
    while ((i = ap_eval_xpath(&ap, i)) != -1) {
        printf(" item name is ===>%s\n", vn->entries[i].text);
    }
    return 0;
}''',
"csharp": r'''using System.Xml.XPath;

public static void Main() {
    try {
        var doc = new XPathDocument("input.xml");
        var nav = doc.CreateNavigator();
        var iter = nav.Select("/xml/item/@name");
        int i = 0;
        while (iter.MoveNext()) {
            Console.WriteLine(" item name is ===>" + iter.Current.Value);
        }
    } catch (Exception) {
        return;
    }
}'''}})

PART.append({"id": "T410", "task": "translate", "outputs": {
"python": r'''def main():
    print("Please enter the red color. Range [0, 255] only please.")
    red = int(input())
    print("Please enter the green color. Range [0, 255] only please.")
    green = int(input())
    print("Please enter the blue color. Range [0, 255] only please.")
    blue = int(input())
    code = 0
    code += red * 2 ** 16
    code += green * 2 ** 8
    code += blue * 2 ** 0
    print("The code is " + str(code) + ".")
    red = 0
    green = 0
    blue = 0
    red = (code & 0xFF0000) >> 16
    green = (code & 0xFF00) >> 8
    blue = code & 0xFF
    print("Your red value is: " + str(red))
    print("Your green value is: " + str(green))
    print("Your blue value is: " + str(blue))

main()''',
"c": r'''#include <stdio.h>
#include <math.h>

int main(void) {
    int code;
    int red, green, blue;
    const int r_mask = 0xFF0000, g_mask = 0xFF00, b_mask = 0xFF;
    printf("Please enter the red color. Range [0, 255] only please.\n");
    scanf("%d", &red);
    printf("Please enter the green color. Range [0, 255] only please.\n");
    scanf("%d", &green);
    printf("Please enter the blue color. Range [0, 255] only please.\n");
    scanf("%d", &blue);
    code = 0;
    code += (int) (red * pow(2, 16));
    code += (int) (green * pow(2, 8));
    code += (int) (blue * pow(2, 0));
    printf("The code is %d.\n", code);
    red = 0;
    green = 0;
    blue = 0;
    red = (code & r_mask) >> 16;
    green = (code & g_mask) >> 8;
    blue = (code & b_mask);
    printf("Your red value is: %d\n", red);
    printf("Your green value is: %d\n", green);
    printf("Your blue value is: %d\n", blue);
    return 0;
}''',
"csharp": r'''static void Main() {
    var scan = Console.In;
    Console.WriteLine("Please enter the red color. Range [0, 255] only please.");
    int red = int.Parse(scan.ReadLine());
    Console.WriteLine("Please enter the green color. Range [0, 255] only please.");
    int green = int.Parse(scan.ReadLine());
    Console.WriteLine("Please enter the blue color. Range [0, 255] only please.");
    int blue = int.Parse(scan.ReadLine());
    int code = 0;
    code += (int) (red * Math.Pow(2, 16));
    code += (int) (green * Math.Pow(2, 8));
    code += (int) (blue * Math.Pow(2, 0));
    Console.WriteLine("The code is " + code + ".");
    int rMask = 0xFF0000, gMask = 0xFF00, bMask = 0xFF;
    red = 0;
    green = 0;
    blue = 0;
    red = (code & rMask) >> 16;
    green = (code & gMask) >> 8;
    blue = (code & bMask);
    Console.WriteLine("Your red value is: " + red);
    Console.WriteLine("Your green value is: " + green);
    Console.WriteLine("Your blue value is: " + blue);
}'''}})

PART.append({"id": "T858", "task": "translate", "outputs": {
"python": r'''def transform(workbook_new, font_old):
    font_new = workbook_new.create_font()
    font_new.boldweight = font_old.boldweight
    font_new.char_set = font_old.char_set
    font_new.color = font_old.color
    font_new.font_name = font_old.font_name
    font_new.font_height = font_old.font_height
    font_new.italic = font_old.italic
    font_new.strikeout = font_old.strikeout
    font_new.type_offset = font_old.type_offset
    font_new.underline = font_old.underline
    return font_new''',
"c": r'''#include <stdlib.h>

typedef struct {
    int boldweight;
    short char_set;
    short color;
    char *font_name;
    short font_height;
    int italic;
    int strikeout;
    short type_offset;
    int underline;
} XSSFFont;

typedef struct {
    int boldweight;
    short char_set;
    short color;
    char *font_name;
    short font_height;
    int italic;
    int strikeout;
    short type_offset;
    int underline;
} HSSFFont;

typedef struct { int unused; } HSSFWorkbook;

HSSFFont *hss_workbook_create_font(HSSFWorkbook *workbook_new) {
    return (HSSFFont *) calloc(1, sizeof(HSSFFont));
}

HSSFFont *transform(HSSFWorkbook *workbook_new, XSSFFont *font_old) {
    HSSFFont *font_new = hss_workbook_create_font(workbook_new);
    font_new->boldweight = font_old->boldweight;
    font_new->char_set = font_old->char_set;
    font_new->color = font_old->color;
    font_new->font_name = font_old->font_name;
    font_new->font_height = font_old->font_height;
    font_new->italic = font_old->italic;
    font_new->strikeout = font_old->strikeout;
    font_new->type_offset = font_old->type_offset;
    font_new->underline = font_old->underline;
    return font_new;
}''',
"csharp": r'''class XSSFFont {
    public int Boldweight, CharSet, Color, FontHeight, TypeOffset, Underline;
    public string FontName;
    public bool Italic, Strikeout;
}
class HSSFFont {
    public int Boldweight, CharSet, Color, FontHeight, TypeOffset, Underline;
    public string FontName;
    public bool Italic, Strikeout;
}
class HSSFWorkbook {
    public HSSFFont CreateFont() { return new HSSFFont(); }
}

public HSSFFont Transform(HSSFWorkbook workbookNew, XSSFFont fontOld) {
    HSSFFont fontNew = workbookNew.CreateFont();
    fontNew.Boldweight = fontOld.Boldweight;
    fontNew.CharSet = fontOld.CharSet;
    fontNew.Color = fontOld.Color;
    fontNew.FontName = fontOld.FontName;
    fontNew.FontHeight = fontOld.FontHeight;
    fontNew.Italic = fontOld.Italic;
    fontNew.Strikeout = fontOld.Strikeout;
    fontNew.TypeOffset = fontOld.TypeOffset;
    fontNew.Underline = fontOld.Underline;
    return fontNew;
}'''}})

PART.append({"id": "T145", "task": "translate", "outputs": {
"python": r'''def solution(x, a):
    searched_value = x
    sum_v = searched_value * (searched_value + 1) // 2
    seen = []
    total = 0
    for i, value in enumerate(a):
        if value <= searched_value and value not in seen:
            total += value
            if total == sum_v:
                return i
            seen.append(value)
    return -1''',
"c": r'''#include <stdlib.h>

int solution(int x, const int *a, int length) {
    int searched_value = x;
    int sum_v = searched_value * (searched_value + 1) / 2;
    int *seen = (int *) malloc((size_t) length * sizeof(int));
    int seen_count = 0;
    int sum = 0;
    for (int i = 0; i < length; i++) {
        int value = a[i];
        int already_seen = 0;
        for (int j = 0; j < seen_count; j++) {
            if (seen[j] == value) {
                already_seen = 1;
                break;
            }
        }
        if (value <= searched_value && !already_seen) {
            sum += value;
            if (sum == sum_v) {
                return i;
            }
            seen[seen_count++] = value;
        }
    }
    free(seen);
    return -1;
}''',
"csharp": r'''using System.Collections.Generic;

public static int Solution(int x, int[] a) {
    int searchedValue = x;
    int sumV = searchedValue * (searchedValue + 1) / 2;
    var seen = new List<int>();
    int sum = 0;
    for (int i = 0; i < a.Length; i++) {
        int value = a[i];
        if (value <= searchedValue && !seen.Contains(value)) {
            sum += value;
            if (sum == sumV) {
                return i;
            }
            seen.Add(value);
        }
    }
    return -1;
}'''}})

PART.append({"id": "T65", "task": "translate", "outputs": {
"python": r'''class JDialog:
    def __init__(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def is_displayable(self):
        return True

class Window:
    @staticmethod
    def get_windows():
        return [JDialog("Settings"), JDialog("About")]

def action_performed(event):
    print()
    print("Display Dialogs")
    for window in Window.get_windows():
        if isinstance(window, JDialog):
            print("\t" + window.get_title() + " " + str(window.is_displayable()))''',
"c": r'''#include <stdio.h>
#include <stdbool.h>

typedef struct {
    const char *title;
    bool displayable;
} JDialog;

static const JDialog windows[] = {
    { "Settings", true },
    { "About", true }
};

static const int window_count = 2;

void action_performed(void *event) {
    printf("\n");
    printf("Display Dialogs\n");
    for (int i = 0; i < window_count; i++) {
        printf("\t%s %d\n", windows[i].title, windows[i].displayable);
    }
}''',
"csharp": r'''class ActionEvent { }
class JDialog {
    public string Title = "";
    public bool IsDisplayable() { return true; }
}
static class Window {
    public static System.Collections.Generic.IEnumerable<object> GetWindows() {
        yield return new JDialog { Title = "Settings" };
        yield return new JDialog { Title = "About" };
    }
}

public void ActionPerformed(ActionEvent e) {
    Console.WriteLine();
    Console.WriteLine("Display Dialogs");
    foreach (object window in Window.GetWindows()) {
        if (window is JDialog dialog) {
            Console.WriteLine("\t" + dialog.Title + " " + dialog.IsDisplayable());
        }
    }
}'''}})

PART.append({"id": "T239", "task": "translate", "outputs": {
"python": r'''def main():
    test = "The quick brown fox jumped over the lazy dog."
    counts = {"A": 0, "O": 0, "Space": 0, "Dot": 0}
    for ch in test:
        if ch in ("a", "A"):
            counts["A"] += 1
        elif ch in ("o", "O"):
            counts["O"] += 1
        elif ch == " ":
            counts["Space"] += 1
        elif ch == ".":
            counts["Dot"] += 1
    print("\n".join(label + ": " + str(value) for label, value in counts.items()))

main()''',
"c": r'''#include <stdio.h>

int main(void) {
    const char *test = "The quick brown fox jumped over the lazy dog.";
    int count_a = 0, count_o = 0, count_space = 0, count_dot = 0;
    for (const char *p = test; *p; p++) {
        switch (*p) {
            case 'a':
            case 'A':
                count_a++;
                break;
            case 'o':
            case 'O':
                count_o++;
                break;
            case ' ':
                count_space++;
                break;
            case '.':
                count_dot++;
                break;
        }
    }
    printf("%s%d\n%s%d\n%s%d\n%s%d", "A: ", count_a, "O: ", count_o, "Space: ", count_space, "Dot: ", count_dot);
    return 0;
}''',
"csharp": r'''static void Main() {
    string test = "The quick brown fox jumped over the lazy dog.";
    int countA = 0, countO = 0, countSpace = 0, countDot = 0;
    foreach (char ch in test) {
        switch (ch) {
            case 'a':
            case 'A':
                countA++;
                break;
            case 'o':
            case 'O':
                countO++;
                break;
            case ' ':
                countSpace++;
                break;
            case '.':
                countDot++;
                break;
        }
    }
    Console.WriteLine("A: " + countA);
    Console.WriteLine("O: " + countO);
    Console.WriteLine("Space: " + countSpace);
    Console.WriteLine("Dot: " + countDot);
}'''}})

PART.append({"id": "T94", "task": "translate", "outputs": {
"python": r'''def read_bytes(input_stream):
    buffer = bytearray()
    while True:
        chunk = input_stream.read(32 * 1024)
        if not chunk:
            return bytes(buffer)
        buffer.extend(chunk)''',
"c": r'''#include <stdio.h>
#include <stdlib.h>

unsigned char *read_bytes(FILE *input_stream, int *out_length) {
    int capacity = 32 * 1024;
    unsigned char *buffer = (unsigned char *) malloc((size_t) capacity);
    int size = 0;
    for (;;) {
        if (size == capacity) {
            capacity *= 2;
            buffer = (unsigned char *) realloc(buffer, (size_t) capacity);
        }
        int read = (int) fread(buffer + size, 1, (size_t) (capacity - size), input_stream);
        if (read == -1) {
            *out_length = size;
            return buffer;
        }
        if (read == 0) {
            break;
        }
        size += read;
        if (size == capacity) {
            capacity *= 2;
            buffer = (unsigned char *) realloc(buffer, (size_t) capacity);
        }
    }
    *out_length = size;
    return buffer;
}''',
"csharp": r'''using System.Linq;

public static byte[] ReadBytes(Stream inputStream) {
    byte[] buffer = new byte[32 * 1024];
    int bufferSize = 0;
    while (true) {
        int read = inputStream.Read(buffer, bufferSize, buffer.Length - bufferSize);
        if (read == -1) {
            return buffer.Take(bufferSize).ToArray();
        }
        if (read == 0) {
            return buffer.Take(bufferSize).ToArray();
        }
        bufferSize += read;
        if (bufferSize == buffer.Length) {
            Array.Resize(ref buffer, bufferSize * 2);
        }
    }
}'''}})

PART.append({"id": "T749", "task": "translate", "outputs": {
"python": r'''class Node:
    def __init__(self, parent=None):
        self.parent = parent

class Pane(Node):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.children = []

class HTMLEditor(Pane):
    def __init__(self):
        super().__init__()
        self.tool_bar = Node(self)
        self.children.append(self.tool_bar)

    def lookup(self, selector):
        if selector == ".tool-bar" and self.tool_bar is not None:
            return self.tool_bar
        return None

class Scene:
    def __init__(self, root):
        self.root = root

class Stage:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def show(self):
        pass

def start(primary_stage):
    html_editor = HTMLEditor()
    primary_stage.set_scene(Scene(html_editor))
    primary_stage.show()
    tool_bar = html_editor.lookup(".tool-bar")
    while tool_bar is not None:
        tool_bar.parent.children.remove(tool_bar)
        tool_bar.parent.tool_bar = None
        tool_bar = html_editor.lookup(".tool-bar")''',
"c": r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct Node {
    void *owner;
    struct Node *parent;
} Node;

typedef struct {
    Node base;
    Node *tool_bar;
} HTMLEditor;

typedef struct { void *root; } Scene;
typedef struct { Scene *scene; } Stage;

Node *html_editor_lookup(HTMLEditor *editor, const char *selector) {
    if (strcmp(selector, ".tool-bar") == 0 && editor->tool_bar != NULL) {
        return editor->tool_bar;
    }
    return NULL;
}

void start(Stage *primary_stage, HTMLEditor *html_editor) {
    Scene scene;
    scene.root = html_editor;
    primary_stage->scene = &scene;
    Node *tool_bar;
    while ((tool_bar = html_editor_lookup(html_editor, ".tool-bar")) != NULL) {
        html_editor->tool_bar = NULL;
        free(tool_bar);
    }
}''',
"csharp": r'''class Node { public object Parent; }
class Pane {
    public System.Collections.Generic.List<Node> Children = new System.Collections.Generic.List<Node>();
}
class HTMLEditor : Pane {
    public Node ToolBar;
    public HTMLEditor() { ToolBar = new Node { Parent = this }; Children.Add(ToolBar); }
    public Node Lookup(string selector) {
        return selector == ".tool-bar" && ToolBar != null ? ToolBar : null;
    }
}
class Scene { public object Root; public Scene(object root) { Root = root; } }
class Stage {
    public Scene Scene;
    public void SetScene(Scene s) { Scene = s; }
    public void Show() { }
}

public void Start(Stage primaryStage) {
    var htmlEditor = new HTMLEditor();
    primaryStage.SetScene(new Scene(htmlEditor));
    primaryStage.Show();
    Node toolBar = htmlEditor.Lookup(".tool-bar");
    while (toolBar != null) {
        ((Pane) toolBar.Parent).Children.Remove(toolBar);
        htmlEditor.ToolBar = null;
        toolBar = htmlEditor.Lookup(".tool-bar");
    }
}'''}})
