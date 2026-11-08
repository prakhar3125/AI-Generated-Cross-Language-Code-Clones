DATA_T5 = {
"T641": {"outputs": {
"python": r'''
in_ = None
current_pos = 0
current_line_end = 0
current_line_start = 0
last_pos_in_file = 0
last_char = '\0'


def find_prev_line():
    pass


def read():
    global current_pos, last_char
    if current_pos < current_line_end:
        in_.seek(current_pos)
        current_pos += 1
        return in_.read_byte()
    elif current_pos > last_pos_in_file and current_line_start < current_line_end:
        find_prev_line()
        if last_char != '\n' and last_char != '\r':
            return '\n'
        else:
            return read()
    elif current_pos < 0:
        return -1
    else:
        find_prev_line()
        return read()
''',
"c": r'''
typedef struct {
    long current_pos;
    long current_line_end;
    long current_line_start;
    long last_pos_in_file;
    char last_char;
} Reader;

static void in_seek(Reader *r, long pos);
static int in_read_byte(Reader *r);
static void find_prev_line(Reader *r);

static int read(Reader *r) {
    if (r->current_pos < r->current_line_end) {
        in_seek(r, r->current_pos++);
        return in_read_byte(r);
    } else if (r->current_pos > r->last_pos_in_file && r->current_line_start < r->current_line_end) {
        find_prev_line(r);
        if (r->last_char != '\n' && r->last_char != '\r') {
            return '\n';
        } else {
            return read(r);
        }
    } else if (r->current_pos < 0) {
        return -1;
    } else {
        find_prev_line(r);
        return read(r);
    }
}
''',
"csharp": r'''
public int Read()
{
    if (currentPos < currentLineEnd)
    {
        In.Seek(currentPos++, SeekOrigin.Begin);
        return In.ReadByte();
    }
    else if (currentPos > lastPosInFile && currentLineStart < currentLineEnd)
    {
        FindPrevLine();
        if (lastChar != '\n' && lastChar != '\r')
        {
            return '\n';
        }
        else
        {
            return Read();
        }
    }
    else if (currentPos < 0)
    {
        return -1;
    }
    else
    {
        FindPrevLine();
        return Read();
    }
}
'''}},
"T605": {"outputs": {
"python": r'''
import xml.etree.ElementTree as ET


def main():
    root = ET.parse("family.xml").getroot()

    def walk(element):
        if element.tag == "dad":
            print("isStartElement: True")
            print("Element BEGIN: dad")
            return
        print(element.tag)
        for child in element:
            walk(child)

    walk(root)

main()
''',
"c": r'''
#include <stdio.h>
#include <string.h>

#define START_ELEMENT 1

int xml_read_next(char *name, size_t size);
void xml_skip_element(void);

int main(void) {
    char name[128];
    while (xml_read_next(name, sizeof(name)) == START_ELEMENT) {
        if (strcmp(name, "dad") == 0) {
            printf("isStartElement: %d\n", 1);
            printf("Element BEGIN: %s\n", name);
            xml_skip_element();
        } else {
            printf("%s\n", name);
        }
    }
    return 0;
}
''',
"csharp": r'''
public static void Main(string[] args)
{
    using (XmlReader xmlsr = XmlReader.Create("family.xml"))
    {
        string currentElementName = null;
        while (xmlsr.Read())
        {
            if (xmlsr.NodeType == XmlNodeType.Element)
            {
                currentElementName = xmlsr.Name;
                if ("dad".Equals(currentElementName) == true)
                {
                    Console.WriteLine("isStartElement: " + xmlsr.IsStartElement());
                    Console.WriteLine("Element BEGIN: " + currentElementName);
                    xmlsr.Skip();
                }
                else
                {
                    Console.WriteLine(currentElementName);
                }
            }
        }
    }
}
'''}},
"T759": {"outputs": {
"python": r'''
class Node:
    def __init__(self):
        self.parent = None


class Pane(Node):
    def __init__(self):
        super().__init__()
        self.children = []

    def get_children(self):
        return self.children


class HTMLEditor(Node):
    def __init__(self):
        super().__init__()
        self.tool_bar = Node()
        self._pane = Pane()
        self._pane.children.append(self.tool_bar)
        self.tool_bar.parent = self._pane

    def lookup(self, selector):
        if selector == ".tool-bar" and self.tool_bar in self._pane.children:
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
        tool_bar.parent.get_children().remove(tool_bar)
        tool_bar = html_editor.lookup(".tool-bar")
''',
"c": r'''
typedef struct Stage Stage;
typedef struct Scene Scene;
typedef struct Node Node;

struct Node {
    Node *parent;
    int removed;
};

extern Node *lookup(Node *editor, const char *selector);
extern Node *node_get_parent(Node *node);
extern void pane_remove_child(Node *pane, Node *tool_bar);
extern void stage_set_scene(Stage *stage, Scene *scene);
extern void stage_show(Stage *stage);

void start(Stage *primary_stage) {
    Node *html_editor = htmleditor_new();
    stage_set_scene(primary_stage, scene_new((Node *)html_editor));
    stage_show(primary_stage);
    Node *tool_bar = lookup(html_editor, ".tool-bar");
    while (tool_bar != NULL) {
        pane_remove_child(node_get_parent(tool_bar), tool_bar);
        tool_bar = lookup(html_editor, ".tool-bar");
    }
}
''',
"csharp": r'''
public void Start(Stage primaryStage)
{
    var htmlEditor = new HTMLEditor();
    primaryStage.Scene = new Scene(htmlEditor);
    primaryStage.Show();
    Node toolBar = htmlEditor.Lookup(".tool-bar");
    while (toolBar != null)
    {
        ((Pane)toolBar.Parent).Children.Remove(toolBar);
        toolBar = htmlEditor.Lookup(".tool-bar");
    }
}
'''}},
"T723": {"outputs": {
"python": r'''
def filter(words, text):
    for word in words:
        if word.lower() in text.lower():
            print(text)
            break
''',
"c": r'''
#include <ctype.h>
#include <stdio.h>
#include <string.h>

static void to_lower(char *s) {
    for (; *s; s++) *s = (char)tolower((unsigned char)*s);
}

void filter(char *words[], int words_len, const char *text) {
    char lower_text[1024];
    strncpy(lower_text, text, sizeof(lower_text) - 1);
    lower_text[sizeof(lower_text) - 1] = '\0';
    to_lower(lower_text);
    for (int i = 0; i < words_len; i++) {
        char lower_word[256];
        strncpy(lower_word, words[i], sizeof(lower_word) - 1);
        lower_word[sizeof(lower_word) - 1] = '\0';
        to_lower(lower_word);
        if (strstr(lower_text, lower_word) != NULL) {
            printf("%s\n", text);
            break;
        }
    }
}
''',
"csharp": r'''
public void Filter(string[] words, string text)
{
    foreach (string word in words)
    {
        if (text.ToLower().Contains(word.ToLower()))
        {
            Console.WriteLine(text);
            break;
        }
    }
}
'''}},
"T309": {"outputs": {
"python": r'''
class Animal:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return isinstance(other, Animal) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


Cat, Mouse, Dog, Horse, Tiger, Lion = (Animal(n) for n in ("Cat", "Mouse", "Dog", "Horse", "Tiger", "Lion"))


def main():
    list1 = [Cat, Mouse, Dog]
    list2 = [Dog, Mouse, Cat]
    list3 = [Dog, Horse, Cat]
    list4 = [Dog, Tiger, Lion]
    lists = [list1, list2, list3, list4]
    sorted_lists = []
    seen = set()
    for animals in lists:
        arlist = sorted(animals)
        key = tuple(arlist)
        if key not in seen:
            seen.add(key)
            sorted_lists.append(arlist)
    for animals in sorted_lists:
        print(animals)

main()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *lists[4][3] = {
    {"Cat", "Mouse", "Dog"},
    {"Dog", "Mouse", "Cat"},
    {"Dog", "Horse", "Cat"},
    {"Dog", "Tiger", "Lion"}
};

static int cmp_str(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

int main(void) {
    const char *sorted[4][3];
    for (int i = 0; i < 4; i++) {
        memcpy(sorted[i], lists[i], sizeof(lists[i]));
        qsort(sorted[i], 3, sizeof(const char *), cmp_str);
        int dup = 0;
        for (int j = 0; j < i; j++) {
            if (memcmp(sorted[j], sorted[i], sizeof(lists[i])) == 0) {
                dup = 1;
                break;
            }
        }
        if (!dup) {
            printf("[");
            for (int k = 0; k < 3; k++) {
                printf("%s%s", k ? ", " : "", sorted[i][k]);
            }
            printf("]\n");
        }
    }
    return 0;
}
''',
"csharp": r'''
public static void Main(string[] args)
{
    var lists = new List<List<Animal>>
    {
        new List<Animal> { Animal.Cat, Animal.Mouse, Animal.Dog },
        new List<Animal> { Animal.Dog, Animal.Mouse, Animal.Cat },
        new List<Animal> { Animal.Dog, Animal.Horse, Animal.Cat },
        new List<Animal> { Animal.Dog, Animal.Tiger, Animal.Lion }
    };
    var sorted = new List<List<Animal>>();
    foreach (var animals in lists)
    {
        var arList = new List<Animal>(animals);
        arList.Sort();
        if (!sorted.Any(s => s.SequenceEqual(arList)))
            sorted.Add(arList);
    }
    foreach (var animals in sorted)
        Console.WriteLine(string.Join(", ", animals));
}
'''}},
}
