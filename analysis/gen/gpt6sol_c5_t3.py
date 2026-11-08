DATA3 = {}

DATA3["T752"] = {
    "python": '''import xml.etree.ElementTree as ET


def main():
    tree = ET.parse("input.xml")
    root = tree.getroot()
    for item in root.iter("item"):
        name = item.get("name")
        print("item name: " + name)''',
    "c": '''#include <stdio.h>
#include <stddef.h>

typedef struct XmlNode {
    const char *tag;
    const char *name;
    struct XmlNode *next;
} XmlNode;

void xml_parse_file(const char *path);
XmlNode *xml_root(void);
XmlNode *node_iter_items(XmlNode *root);

int main(void) {
    xml_parse_file("input.xml");
    XmlNode *root = xml_root();
    for (XmlNode *item = node_iter_items(root); item != NULL; item = item->next) {
        printf("item name: %s\\n", item->name);
    }
    return 0;
}''',
    "csharp": '''using System;
using System.Xml.XPath;

public static class XmlItemReader
{
    public static void Main(string[] args)
    {
        XPathDocument doc = new XPathDocument("input.xml");
        XPathNavigator nav = doc.CreateNavigator();
        XPathNodeIterator items = nav.Select("/xml/item/@name");
        while (items.MoveNext())
        {
            Console.WriteLine("item name: " + items.Current.Value);
        }
    }
}''',
}

DATA3["T410"] = {
    "python": '''def encode_color(r, g, b):
    return int(r * pow(2, 16) + g * pow(2, 8) + b * pow(2, 0))


def decode_color(color):
    mask = 0xFF
    r = (color & (mask << 16)) >> 16
    g = (color & (mask << 8)) >> 8
    b = (color & (mask << 0)) >> 0
    return r, g, b''',
    "c": '''#include <stdio.h>

int encode_color(int r, int g, int b) {
    return r * (1 << 16) + g * (1 << 8) + b * (1 << 0);
}

void decode_color(int color, int *r, int *g, int *b) {
    int mask = 0xFF;
    *r = (color & (mask << 16)) >> 16;
    *g = (color & (mask << 8)) >> 8;
    *b = (color & (mask << 0)) >> 0;
}

int main(void) {
    int color = encode_color(255, 128, 4);
    int r, g, b;
    decode_color(color, &r, &g, &b);
    printf("%d -> (%d, %d, %d)\\n", color, r, g, b);
    return 0;
}''',
    "csharp": '''public static class ColorCodec
{
    private const int Mask = 0xFF;

    public static int EncodeColor(int r, int g, int b)
    {
        return r * (1 << 16) + g * (1 << 8) + b * (1 << 0);
    }

    public static (int r, int g, int b) DecodeColor(int color)
    {
        int r = (color & (Mask << 16)) >> 16;
        int g = (color & (Mask << 8)) >> 8;
        int b = (color & (Mask << 0)) >> 0;
        return (r, g, b);
    }
}''',
}

DATA3["T858"] = {
    "python": '''class FontInfo:
    def __init__(self):
        self.boldweight = 0
        self.char_set = 0
        self.color = 0
        self.font_name = None
        self.font_height = 0
        self.italic = False
        self.strikeout = False
        self.type_offset = 0
        self.underline = False


def copy_font(source, target):
    for attr in ("boldweight", "char_set", "color", "font_name",
                 "font_height", "italic", "strikeout", "type_offset",
                 "underline"):
        setattr(target, attr, getattr(source, attr))


def transform_font(cell, workbook_new):
    font = FontInfo()
    style = cell.get_style()
    copy_font(style.font, font)
    return workbook_new.create_font(font)''',
    "c": '''#include <string.h>
#include <stdlib.h>

typedef struct {
    int boldweight;
    int char_set;
    int color;
    char font_name[64];
    int font_height;
    int italic;
    int strikeout;
    int type_offset;
    int underline;
} FontInfo;

void copy_font(const FontInfo *source, FontInfo *target) {
    target->boldweight = source->boldweight;
    target->char_set = source->char_set;
    target->color = source->color;
    strcpy(target->font_name, source->font_name);
    target->font_height = source->font_height;
    target->italic = source->italic;
    target->strikeout = source->strikeout;
    target->type_offset = source->type_offset;
    target->underline = source->underline;
}

FontInfo *transform_font(const FontInfo *cell_font) {
    FontInfo *font = malloc(sizeof(FontInfo));
    copy_font(cell_font, font);
    return font;
}''',
    "csharp": '''public class FontInfo
{
    public int BoldWeight { get; set; }
    public int CharSet { get; set; }
    public int Color { get; set; }
    public string FontName { get; set; }
    public int FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public int TypeOffset { get; set; }
    public bool Underline { get; set; }
}

public class WorkbookNew
{
    public FontInfo CreateFont(FontInfo source)
    {
        return new FontInfo
        {
            BoldWeight = source.BoldWeight,
            CharSet = source.CharSet,
            Color = source.Color,
            FontName = source.FontName,
            FontHeight = source.FontHeight,
            Italic = source.Italic,
            Strikeout = source.Strikeout,
            TypeOffset = source.TypeOffset,
            Underline = source.Underline
        };
    }
}

public static class FontTransformer
{
    public static FontInfo TransformFont(FontInfo cellFont, WorkbookNew workbookNew)
    {
        return workbookNew.CreateFont(cellFont);
    }
}''',
}

DATA3["T145"] = {
    "python": '''def solution(x):
    sum_v = x * (x + 1) // 2
    seen = []
    for divisor in range(1, x):
        if x % divisor == 0:
            if divisor not in seen:
                sum_v -= divisor
                seen.append(divisor)
            if divisor != x // divisor and (x // divisor) not in seen:
                sum_v -= x // divisor
                seen.append(x // divisor)
    return sum_v''',
    "c": '''int solution(int x) {
    int sum_v = x * (x + 1) / 2;
    int seen[1024];
    int seen_count = 0;
    for (int divisor = 1; divisor < x; divisor++) {
        if (x % divisor == 0) {
            int known = 0;
            for (int i = 0; i < seen_count; i++) {
                if (seen[i] == divisor) known = 1;
            }
            if (!known) {
                sum_v -= divisor;
                seen[seen_count++] = divisor;
            }
            if (divisor != x / divisor) {
                known = 0;
                for (int i = 0; i < seen_count; i++) {
                    if (seen[i] == x / divisor) known = 1;
                }
                if (!known) {
                    sum_v -= x / divisor;
                    seen[seen_count++] = x / divisor;
                }
            }
        }
    }
    return sum_v;
}''',
    "csharp": '''using System.Collections.Generic;

public static class MissingNumber
{
    public static int Solution(int x)
    {
        int sumV = x * (x + 1) / 2;
        List<int> seen = new List<int>();
        for (int divisor = 1; divisor < x; divisor++)
        {
            if (x % divisor == 0)
            {
                if (!seen.Contains(divisor))
                {
                    sumV -= divisor;
                    seen.Add(divisor);
                }
                if (divisor != x / divisor && !seen.Contains(x / divisor))
                {
                    sumV -= x / divisor;
                    seen.Add(x / divisor);
                }
            }
        }
        return sumV;
    }
}''',
}

DATA3["T65"] = {
    "python": '''class Window:
    def __init__(self, title):
        self.title = title

    @property
    def displayable(self):
        return False


class Dialog(Window):
    def __init__(self, title):
        super().__init__(title)
        self.modal = False


class WindowManager:
    _dialogs = []

    @classmethod
    def get_dialogs(cls):
        return list(cls._dialogs)

    @classmethod
    def add(cls, dialog):
        cls._dialogs.append(dialog)


def main():
    print("\\tWindowManager.getDialogs():")
    for dialog in WindowManager.get_dialogs():
        print("\\t" + dialog.title + " " + str(dialog.displayable))''',
    "c": '''#include <stdio.h>

typedef struct {
    char title[64];
    int displayable;
} Dialog;

int window_manager_get_dialogs(Dialog *out, int max);
int window_manager_add(const Dialog *dialog);

int main(void) {
    Dialog dialogs[16];
    int count = window_manager_get_dialogs(dialogs, 16);
    printf("\\tWindowManager.getDialogs():\\n");
    for (int i = 0; i < count; i++) {
        printf("\\t%s %s\\n", dialogs[i].title, dialogs[i].displayable ? "true" : "false");
    }
    return 0;
}''',
    "csharp": '''using System;
using System.Collections.Generic;

public class UiDialog
{
    public string Title { get; set; }
    public bool Displayable { get; set; }
}

public static class WindowManager
{
    public static List<UiDialog> Dialogs { get; } = new List<UiDialog>();

    public static void Add(UiDialog dialog)
    {
        Dialogs.Add(dialog);
    }
}

public static class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("\\tWindowManager.getDialogs():");
        foreach (UiDialog dialog in WindowManager.Dialogs)
        {
            Console.WriteLine("\\t" + dialog.Title + " " + dialog.Displayable);
        }
    }
}''',
}

DATA3["T239"] = {
    "python": '''def main():
    string = "The quick brown fox jumped over the lazy dog."
    number_of_a = 0
    number_of_o = 0
    number_of_space = 0
    number_of_dot = 0
    for c in string:
        if c in ("a", "A"):
            number_of_a += 1
        elif c in ("o", "O"):
            number_of_o += 1
        elif c == " ":
            number_of_space += 1
        elif c == ".":
            number_of_dot += 1
    print("number of a : " + str(number_of_a))
    print("number of o : " + str(number_of_o))
    print("number of space : " + str(number_of_space))
    print("number of dot : " + str(number_of_dot))''',
    "c": '''#include <stdio.h>
#include <string.h>

int main(void) {
    const char *string = "The quick brown fox jumped over the lazy dog.";
    int number_of_a = 0, number_of_o = 0, number_of_space = 0, number_of_dot = 0;
    size_t len = strlen(string);
    for (size_t i = 0; i < len; i++) {
        switch (string[i]) {
            case 'a': case 'A': number_of_a++; break;
            case 'o': case 'O': number_of_o++; break;
            case ' ': number_of_space++; break;
            case '.': number_of_dot++; break;
        }
    }
    printf("number of a : %d\\n", number_of_a);
    printf("number of o : %d\\n", number_of_o);
    printf("number of space : %d\\n", number_of_space);
    printf("number of dot : %d\\n", number_of_dot);
    return 0;
}''',
    "csharp": '''using System;

public static class CharCounter
{
    public static void Main(string[] args)
    {
        string str = "The quick brown fox jumped over the lazy dog.";
        int numberOfA = 0, numberOfO = 0, numberOfSpace = 0, numberOfDot = 0;
        foreach (char c in str)
        {
            switch (c)
            {
                case 'a': case 'A': numberOfA++; break;
                case 'o': case 'O': numberOfO++; break;
                case ' ': numberOfSpace++; break;
                case '.': numberOfDot++; break;
            }
        }
        Console.WriteLine("number of a : " + numberOfA);
        Console.WriteLine("number of o : " + numberOfO);
        Console.WriteLine("number of space : " + numberOfSpace);
        Console.WriteLine("number of dot : " + numberOfDot);
    }
}''',
}

DATA3["T94"] = {
    "python": '''def read_bytes(stream):
    buffer = bytearray(32 * 1024)
    total = 0
    while True:
        chunk = stream.read(len(buffer) - total)
        if not chunk:
            break
        buffer[total:total + len(chunk)] = chunk
        total += len(chunk)
        if total == len(buffer):
            buffer.extend(bytearray(len(buffer)))
    return bytes(buffer[:total])''',
    "c": '''#include <stddef.h>
#include <stdlib.h>

typedef size_t (*stream_read_fn)(unsigned char *buf, size_t count, void *ctx);

unsigned char *read_bytes(stream_read_fn read_fn, void *ctx, size_t *out_len) {
    size_t cap = 32 * 1024;
    unsigned char *buffer = malloc(cap);
    size_t total = 0;
    for (;;) {
        size_t read = read_fn(buffer + total, cap - total, ctx);
        total += read;
        if (read == 0) {
            break;
        }
        if (total == cap) {
            cap *= 2;
            buffer = realloc(buffer, cap);
        }
    }
    *out_len = total;
    return buffer;
}''',
    "csharp": '''using System.IO;

public static class StreamCopier
{
    public static byte[] ReadBytes(Stream stream)
    {
        byte[] buffer = new byte[32 * 1024];
        int total = 0;
        int read;
        while ((read = stream.Read(buffer, total, buffer.Length - total)) > 0)
        {
            total += read;
            if (total == buffer.Length)
            {
                byte[] grown = new byte[buffer.Length * 2];
                System.Array.Copy(buffer, grown, buffer.Length);
                buffer = grown;
            }
        }
        byte[] result = new byte[total];
        System.Array.Copy(buffer, result, total);
        return result;
    }
}''',
}

DATA3["T749"] = {
    "python": '''class Node:
    def __init__(self):
        self.children = []

    def lookup(self, selector):
        return self.children[0] if self.children else None


class Pane(Node):
    pass


class Scene:
    def __init__(self, root):
        self.root = root


class HTMLEditor(Node):
    pass


class Stage:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene


def clear_editors(stage):
    scene = stage.scene
    pane = scene.root
    while True:
        editor = pane.lookup(".html-editor")
        if editor is None:
            break
        pane.children.remove(editor)''',
    "c": '''#include <stddef.h>

typedef struct UiNode {
    struct UiNode **children;
    size_t child_count;
} UiNode;

UiNode *html_editor_lookup(UiNode *root, const char *selector);
void pane_remove_child(UiNode *pane, UiNode *child);
UiNode *stage_root(UiNode *stage);

void clear_editors(UiNode *stage) {
    UiNode *pane = stage_root(stage);
    UiNode *editor;
    while ((editor = html_editor_lookup(pane, ".html-editor")) != NULL) {
        pane_remove_child(pane, editor);
    }
}''',
    "csharp": '''using System.Linq;

public class UiNode
{
    public System.Collections.Generic.List<UiNode> Children { get; } =
        new System.Collections.Generic.List<UiNode>();

    public UiNode Lookup(string selector)
    {
        return Children.FirstOrDefault();
    }
}

public class UiPane : UiNode { }

public class UiStage
{
    public UiPane RootPane { get; set; }
}

public static class EditorCleaner
{
    public static void ClearEditors(UiStage stage)
    {
        UiPane pane = stage.RootPane;
        UiNode editor;
        while ((editor = pane.Lookup(".html-editor")) != null)
        {
            pane.Children.Remove(editor);
        }
    }
}''',
}
