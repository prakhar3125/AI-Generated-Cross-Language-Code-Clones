DATA3 = {
    "T879": {"outputs": {
        "python": '''class Font:
    def __init__(self):
        self.boldweight = None
        self.char_set = None
        self.color = None
        self.font_name = None
        self.font_height = None
        self.italic = None
        self.strikeout = None
        self.type_offset = None
        self.underline = None


class Workbook:
    def create_font(self):
        return Font()


def transform(workbook_new, font_old):
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
        "c": r'''#include <string.h>
#include <stdlib.h>

typedef struct font {
    int boldweight;
    int char_set;
    int color;
    char font_name[64];
    int font_height;
    int italic;
    int strikeout;
    int type_offset;
    int underline;
} Font;

typedef struct workbook {
    Font *(*create_font)(struct workbook *);
} Workbook;

static Font *workbook_create_font(Workbook *wb) {
    Font *f = calloc(1, sizeof(Font));
    return f;
}

Font *transform(Workbook *workbookNew, const Font *fontOld) {
    Font *fontNew = workbook_create_font(workbookNew);
    fontNew->boldweight = fontOld->boldweight;
    fontNew->char_set = fontOld->char_set;
    fontNew->color = fontOld->color;
    strcpy(fontNew->font_name, fontOld->font_name);
    fontNew->font_height = fontOld->font_height;
    fontNew->italic = fontOld->italic;
    fontNew->strikeout = fontOld->strikeout;
    fontNew->type_offset = fontOld->type_offset;
    fontNew->underline = fontOld->underline;
    return fontNew;
}''',
        "csharp": '''public class FontInfo
{
    public short BoldWeight { get; set; }
    public short CharSet { get; set; }
    public short Color { get; set; }
    public string FontName { get; set; }
    public short FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public short TypeOffset { get; set; }
    public short Underline { get; set; }
}

public class Workbook
{
    public FontInfo CreateFont()
    {
        return new FontInfo();
    }
}

public static class FontTransformer
{
    public static FontInfo Transform(Workbook workbookNew, FontInfo fontOld)
    {
        var fontNew = workbookNew.CreateFont();
        fontNew.BoldWeight = fontOld.BoldWeight;
        fontNew.CharSet = fontOld.CharSet;
        fontNew.Color = fontOld.Color;
        fontNew.FontName = fontOld.FontName;
        fontNew.FontHeight = fontOld.FontHeight;
        fontNew.Italic = fontOld.Italic;
        fontNew.Strikeout = fontOld.Strikeout;
        fontNew.TypeOffset = fontOld.TypeOffset;
        fontNew.Underline = fontOld.Underline;
        return fontNew;
    }
}'''
    }},
    "T620": {"outputs": {
        "python": '''def zero_front(nums):
    if nums is None:
        return None
    result = [0] * len(nums)
    zeros_pos = 0
    for value in nums:
        if value == 0:
            result[zeros_pos] = 0
            zeros_pos += 1
    fill = len(nums) - 1
    for value in reversed(nums):
        if value != 0:
            result[fill] = value
            fill -= 1
    return result''',
        "c": r'''#include <stdlib.h>

int *zero_front(const int *nums, int length) {
    if (nums == NULL) {
        return NULL;
    }
    int *result = calloc(length, sizeof(int));
    int zeros_pos = 0;
    for (int i = 0; i < length; i++) {
        if (nums[i] == 0) {
            result[zeros_pos] = 0;
            zeros_pos++;
        }
    }
    int others_pos = length - 1;
    for (int i = length - 1; i >= 0; i--) {
        if (nums[i] != 0) {
            result[others_pos] = nums[i];
            others_pos--;
        }
    }
    return result;
}''',
        "csharp": '''public static class ZeroFrontMover
{
    public static int[] ZeroFront(int[] nums)
    {
        if (nums == null)
        {
            return null;
        }
        int[] result = new int[nums.Length];
        int zerosPos = 0;
        int othersPos = result.Length - 1;
        for (int i = 0; i < nums.Length; i++)
        {
            if (nums[i] == 0)
            {
                result[zerosPos] = 0;
                zerosPos++;
            }
            else
            {
                result[othersPos] = nums[i];
                othersPos--;
            }
        }
        return result;
    }
}'''
    }},
    "T664": {"outputs": {
        "python": '''import inspect


class TypeNode:
    def __init__(self, name, args=()):
        self.name = name
        self.args = list(args)


def investigate(node, type_args=None):
    name = node.name
    pieces = [name]
    if type_args:
        pieces.append("<")
        local_args = list(node.args)
        next_arg = 0
        rendered = []
        for local in local_args:
            if isinstance(local, TypeNode) and local.args:
                rendered.append(str(local.name) + "<" + str(type_args[next_arg]) + ">")
                next_arg += 1
            elif isinstance(local, TypeNode):
                local.name = type_args[next_arg]
                rendered.append(str(type_args[next_arg]))
                next_arg += 1
            else:
                rendered.append(str(local))
        pieces.append(", ".join(rendered))
        pieces.append(">")
    else:
        inner = ", ".join(str(a) for a in node.args)
        pieces.append("<" + inner + ">")
    print("".join(pieces))
    for a in node.args:
        if isinstance(a, TypeNode):
            investigate(a)


investigate(TypeNode("Map", [TypeNode("String"), TypeNode("List", [TypeNode("Integer")])]),
            type_args=["String", "Integer"])''',
        "c": r'''#include <stdio.h>

#define MAX_DEPTH 8

typedef struct type_arg {
    char name[64];
    struct type_arg *nested;
} TypeArg;

typedef struct parameterized_type {
    char name[64];
    TypeArg args[MAX_DEPTH];
    int arg_count;
} ParameterizedType;

static void investigate(ParameterizedType *p, char **type_args, int type_arg_count) {
    printf("%s<", p->name);
    int next = 0;
    for (int i = 0; i < p->arg_count; i++) {
        if (p->args[i].nested != NULL && type_args != NULL && next < type_arg_count) {
            printf("%s<%s>", p->args[i].name, type_args[next++]);
        } else if (p->args[i].nested == NULL && type_args != NULL && next < type_arg_count) {
            printf("%s", type_args[next++]);
        } else {
            printf("%s", p->args[i].name);
        }
        if (i < p->arg_count - 1) {
            printf(", ");
        }
    }
    printf(">\n");
}

int main(void) {
    ParameterizedType inner = { .name = "Integer", .arg_count = 0 };
    ParameterizedType p = { .name = "Map", .arg_count = 2 };
    snprintf(p.args[0].name, 64, "String");
    snprintf(p.args[1].name, 64, "List");
    p.args[1].nested = &inner;
    char *type_args[1] = { "Integer" };
    investigate(&p, type_args, 1);
    return 0;
}''',
        "csharp": '''using System;
using System.Collections.Generic;
using System.Text;

public class TypeNode
{
    public string Name { get; set; }
    public List<object> Args { get; } = new List<object>();
}

public static class TypeInvestigator
{
    public static void Investigate(TypeNode p, params string[] typeArgs)
    {
        var b = new StringBuilder(p.Name);
        b.Append('<');
        if (typeArgs != null && typeArgs.Length > 0)
        {
            int nextTypeArg = 0;
            var rendered = new List<string>();
            foreach (var local in p.Args)
            {
                if (local is TypeNode nested && nested.Args.Count > 0)
                {
                    rendered.Add(nested.Name + "<" + typeArgs[nextTypeArg++] + ">");
                }
                else if (local is TypeNode leaf)
                {
                    leaf.Name = typeArgs[nextTypeArg];
                    rendered.Add(typeArgs[nextTypeArg]);
                    nextTypeArg++;
                }
                else
                {
                    rendered.Add(local.ToString());
                }
            }
            b.Append(string.Join(", ", rendered));
            b.Append('>');
        }
        else
        {
            b.Append(string.Join(", ", p.Args));
            b.Append('>');
        }
        Console.WriteLine(b);
        foreach (var a in p.Args)
        {
            if (a is TypeNode nested)
            {
                Investigate(nested);
            }
        }
    }
}'''
    }},
    "T706": {"outputs": {
        "python": '''import random


def shuffle(text):
    characters = list(text)
    i = 0
    while i < len(characters):
        random_index = random.randrange(len(characters))
        characters[i], characters[random_index] = characters[random_index], characters[i]
        i += 1
    return "".join(characters)''',
        "c": r'''#include <stdlib.h>
#include <string.h>

char *shuffle(const char *text) {
    size_t length = strlen(text);
    char *characters = malloc(length + 1);
    strcpy(characters, text);
    for (size_t i = 0; i < length; i++) {
        size_t random_index = (size_t) (rand() % length);
        char temp = characters[i];
        characters[i] = characters[random_index];
        characters[random_index] = temp;
    }
    return characters;
}''',
        "csharp": '''using System;
using System.Text;

public static class Shuffler
{
    private static readonly Random Rng = new Random();

    public static string Shuffle(string text)
    {
        char[] characters = text.ToCharArray();
        for (int i = 0; i < characters.Length; i++)
        {
            int randomIndex = Rng.Next(characters.Length);
            char temp = characters[i];
            characters[i] = characters[randomIndex];
            characters[randomIndex] = temp;
        }
        return new string(characters);
    }
}'''
    }},
}
