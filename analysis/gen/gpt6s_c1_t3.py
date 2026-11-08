DATA_T3 = {
"T641": {
"python": '''class ReverseLineReader:
    def __init__(self, filename):
        self.filename = filename
        self.currentPos = None
        self.currentLineEnd = None

    def findPrevLine(self):
        pass

    def read(self):
        with open(self.filename, "rb") as fh:
            if self.currentLineEnd is None:
                fh.seek(0, 2)
                self.currentLineEnd = fh.tell()
            if self.currentPos is None:
                self.currentPos = self.currentLineEnd
            start = max(self.currentPos - 1, 0)
            fh.seek(start)
            chunk = fh.read(self.currentPos - start)
            self.currentPos = start
            if not chunk:
                return ""
            return chunk.decode("utf-8")[::-1]
''',
"c": r'''static long currentPos = -1;
static long currentLineEnd = -1;

void findPrevLine(void) {
}

int read(char *buf, size_t bufsize, const char *filename) {
    FILE *fh = fopen(filename, "rb");
    if (fh == NULL) return -1;
    if (currentLineEnd < 0) {
        fseek(fh, 0, SEEK_END);
        currentLineEnd = ftell(fh);
    }
    if (currentPos < 0) {
        currentPos = currentLineEnd;
    }
    long start = currentPos - 1;
    if (start < 0) start = 0;
    fseek(fh, start, SEEK_SET);
    size_t want = (size_t) (currentPos - start);
    size_t got = fread(buf, 1, want < bufsize - 1 ? want : bufsize - 1, fh);
    buf[got] = '\0';
    currentPos = start;
    fclose(fh);
    for (size_t i = 0; i < got / 2; i++) {
        char tmp = buf[i];
        buf[i] = buf[got - 1 - i];
        buf[got - 1 - i] = tmp;
    }
    return (int) got;
}
''',
"csharp": '''public class ReverseLineReader {
    private readonly string _filename;
    private long? _currentPos;
    private long? _currentLineEnd;

    public ReverseLineReader(string filename) {
        _filename = filename;
    }

    public void FindPrevLine() {
    }

    public string Read() {
        using (var fh = new FileStream(_filename, FileMode.Open, FileAccess.Read)) {
            if (_currentLineEnd == null) {
                _currentLineEnd = fh.Seek(0, SeekOrigin.End);
            }
            if (_currentPos == null) {
                _currentPos = _currentLineEnd;
            }
            long start = Math.Max(_currentPos.Value - 1, 0);
            fh.Seek(start, SeekOrigin.Begin);
            int count = (int) (_currentPos.Value - start);
            var buf = new byte[count];
            int got = fh.Read(buf, 0, count);
            _currentPos = start;
            if (got == 0) return "";
            var bytes = new byte[got];
            Array.Copy(buf, bytes, got);
            Array.Reverse(bytes);
            return Encoding.UTF8.GetString(bytes);
        }
    }
}
'''
},
"T605": {
"python": '''import xml.etree.ElementTree as ET

def walk(elem, path):
    if elem.tag == "dad":
        return
    path.append(elem.tag)
    print("/".join(path))
    for child in elem:
        walk(child, path)
    path.pop()

def main():
    tree = ET.parse("family.xml")
    walk(tree.getroot(), [])
''',
"c": r'''extern void *xml_open(const char *filename);
extern void *xml_next(void *node);
extern const char *xml_name(void *node);
extern int xml_is_start(void *node);
extern void xml_skip_element(void *node);

static void walk(void *node, char *path, size_t pathLen) {
    const char *name = xml_name(node);
    if (strcmp(name, "dad") == 0) {
        return;
    }
    size_t cur = strlen(path);
    if (cur) path[cur++] = '/';
    strcpy(path + cur, name);
    printf("%s\n", path);
    void *child = xml_next(node);
    while (child != NULL) {
        walk(child, path, pathLen);
        child = xml_next(node);
    }
    path[cur] = '\0';
}

int main(void) {
    void *root = xml_open("family.xml");
    if (root == NULL) return 1;
    char path[1024];
    path[0] = '\0';
    walk(root, path, sizeof(path));
    return 0;
}
''',
"csharp": '''public static void Walk(XmlReader reader, List<string> path) {
    while (reader.Read()) {
        if (reader.NodeType == XmlNodeType.Element) {
            if (reader.LocalName == "dad") {
                reader.Skip();
                continue;
            }
            path.Add(reader.LocalName);
            Console.WriteLine(string.Join("/", path));
            if (!reader.IsEmptyElement) {
                Walk(reader, path);
            }
            path.RemoveAt(path.Count - 1);
        } else if (reader.NodeType == XmlNodeType.EndElement) {
            return;
        }
    }
}

public static void Main(string[] args) {
    using (XmlReader reader = XmlReader.Create("family.xml")) {
        Walk(reader, new List<string>());
    }
}
'''
},
"T759": {
"python": '''import javafx.scene as scene
import javafx.scene.layout as layout
import javafx.scene.web as web
import javafx.stage as stage

class HTMLEditorTest:
    def start(self, primaryStage):
        htmlEditor = web.HTMLEditor()
        pane = layout.Pane()
        pane.getChildren().add(htmlEditor)
        root = stage.Scene(pane, 400, 400)
        stageOne = primaryStage
        stageOne.setScene(root)
        stageOne.show()
        while True:
            node = pane.lookup(".tool-bar")
            if node is None:
                break
            pane.getChildren().remove(node)
        stageOne.hide()
        stageOne.show()

def main():
    stageOne = stage.Stage()
    HTMLEditorTest().start(stageOne)
''',
"c": r'''typedef struct {
    int hasToolBar;
} Pane;

typedef struct {
    Pane *pane;
} Stage;

void *pane_lookup(Pane *pane, const char *selector) {
    (void) selector;
    return pane->hasToolBar ? pane : NULL;
}

void pane_remove_child(Pane *pane, void *node) {
    (void) node;
    pane->hasToolBar = 0;
}

void stage_show(Stage *s) {
    (void) s;
}

void htmleditor_test_start(Stage *primaryStage) {
    Pane pane;
    pane.hasToolBar = 1;
    primaryStage->pane = &pane;
    stage_show(primaryStage);
    while (1) {
        void *node = pane_lookup(&pane, ".tool-bar");
        if (node == NULL) {
            break;
        }
        pane_remove_child(&pane, node);
    }
    stage_show(primaryStage);
    stage_show(primaryStage);
}

int main(void) {
    Stage stageOne;
    htmleditor_test_start(&stageOne);
    return 0;
}
''',
"csharp": '''public class Node { }

public class Pane : Node {
    public readonly List<Node> Children = new List<Node>();

    public Node Lookup(string selector) {
        return selector == ".tool-bar" && Children.Count > 0 ? Children[0] : null;
    }
}

public class HTMLEditor : Node { }

public class Stage {
    public void SetScene(object root) { }
    public void Show() { }
    public void Hide() { }
}

public static void Start(Stage primaryStage) {
    HTMLEditor htmlEditor = new HTMLEditor();
    Pane pane = new Pane();
    pane.Children.Add(htmlEditor);
    var root = new { Width = 400, Height = 400 };
    primaryStage.SetScene(root);
    primaryStage.Show();
    while (true) {
        Node node = pane.Lookup(".tool-bar");
        if (node == null) {
            break;
        }
        pane.Children.Remove(node);
    }
    primaryStage.Hide();
    primaryStage.Show();
}

public static void Main(string[] args) {
    Stage stageOne = new Stage();
    Start(stageOne);
}
'''
},
"T723": {
"python": '''def main():
    words = ["apple", "banana", "cherry"]
    text = "I like apples a lot"
    for word in words:
        if word.lower() in text.lower():
            print(text)
            break
''',
"c": r'''void to_lower(char *s) {
    for (; *s; s++) {
        *s = (char) tolower((unsigned char) *s);
    }
}

int main(void) {
    const char *words[] = {"apple", "banana", "cherry"};
    const char *text = "I like apples a lot";
    for (int i = 0; i < 3; i++) {
        char w[64];
        char t[1024];
        snprintf(w, sizeof(w), "%s", words[i]);
        snprintf(t, sizeof(t), "%s", text);
        to_lower(w);
        to_lower(t);
        if (strstr(t, w) != NULL) {
            printf("%s\n", text);
            break;
        }
    }
    return 0;
}
''',
"csharp": '''public static void Main(string[] args) {
    string[] words = { "apple", "banana", "cherry" };
    string text = "I like apples a lot";
    if (words.Any(word => text.ToLower().Contains(word.ToLower()))) {
        Console.WriteLine(text);
    }
}
'''
},
"T309": {
"python": '''class Animal:
    def __init__(self, name):
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return "Animal(" + self.name + ")"

Cat = "cat"
Mouse = "mouse"
Dog = "dog"
Horse = "horse"
Tiger = "tiger"
Lion = "lion"

def main():
    cats = [Animal(Cat), Animal(Mouse)]
    dogs = [Animal(Dog), Animal(Horse)]
    zoo = [Animal(Tiger), Animal(Lion)]
    all_animals = cats + dogs + zoo
    seen = set()
    unique = []
    for animal in sorted(all_animals):
        key = (animal.name,)
        if key not in seen:
            seen.add(key)
            unique.append(animal)
    print([repr(a) for a in unique])
''',
"c": r'''typedef struct {
    char name[32];
} Animal;

static int animal_cmp(const void *a, const void *b) {
    const Animal *pa = (const Animal *) a;
    const Animal *pb = (const Animal *) b;
    return strcmp(pa->name, pb->name);
}

int main(void) {
    Animal cats[2] = {{"cat"}, {"mouse"}};
    Animal dogs[2] = {{"dog"}, {"horse"}};
    Animal zoo[2] = {{"tiger"}, {"lion"}};
    Animal all[6];
    memcpy(&all[0], cats, sizeof(cats));
    memcpy(&all[2], dogs, sizeof(dogs));
    memcpy(&all[4], zoo, sizeof(zoo));
    qsort(all, 6, sizeof(Animal), animal_cmp);
    Animal unique[6];
    int count = 0;
    for (int i = 0; i < 6; i++) {
        if (count == 0 || strcmp(unique[count - 1].name, all[i].name) != 0) {
            unique[count++] = all[i];
        }
    }
    for (int i = 0; i < count; i++) {
        printf("Animal(%s)\n", unique[i].name);
    }
    return 0;
}
''',
"csharp": '''public class Animal : IComparable<Animal> {
    public string Name;

    public Animal(string name) {
        Name = name;
    }

    public int CompareTo(Animal other) {
        return string.Compare(Name, other.Name, StringComparison.Ordinal);
    }

    public override string ToString() {
        return "Animal(" + Name + ")";
    }
}

public static void Main(string[] args) {
    var cats = new List<Animal> { new Animal("cat"), new Animal("mouse") };
    var dogs = new List<Animal> { new Animal("dog"), new Animal("horse") };
    var zoo = new List<Animal> { new Animal("tiger"), new Animal("lion") };
    var allAnimals = new List<Animal>();
    allAnimals.AddRange(cats);
    allAnimals.AddRange(dogs);
    allAnimals.AddRange(zoo);
    var unique = new List<Animal>();
    foreach (Animal animal in allAnimals.OrderBy(a => a.Name)) {
        if (!unique.Any(a => a.Name == animal.Name)) {
            unique.Add(animal);
        }
    }
    Console.WriteLine(string.Join(", ", unique.Select(a => a.ToString())));
}
'''
},
}
