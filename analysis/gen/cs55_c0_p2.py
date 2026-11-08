DATA_P2 = {}

DATA_P2["T323"] = {"outputs": {
"python": r'''
ZERO_TOKEN = "zero"
MINUS = "minus"
SEPARATOR = " "
UNION_AND = "and"


class Processor:
    def get_name(self, value):
        return value


class Scale:
    def get_name(self, n):
        return str(n)


processor = Processor()
SCALE = Scale()


def get_name(value):
    negative = value.startswith("-")
    if negative:
        value = value[1:]
    decimals = value.find(".")
    decimal_value = None
    if decimals >= 0:
        decimal_value = value[decimals + 1:]
        value = value[:decimals]
    name = processor.get_name(value)
    if not name:
        name = ZERO_TOKEN
    elif negative:
        name = MINUS + SEPARATOR + name
    if decimal_value:
        name = SEPARATOR.join([
            name,
            UNION_AND,
            processor.get_name(decimal_value),
            SCALE.get_name(-len(decimal_value)),
        ])
    return name
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *ZERO_TOKEN = "zero";
const char *MINUS = "minus";
const char *SEPARATOR = " ";
const char *UNION_AND = "and";

char *processor_getName(const char *value) {
    return strdup(value);
}

char *scale_getName(int n) {
    char *s = malloc(16);
    sprintf(s, "%d", n);
    return s;
}

char *getName(const char *value) {
    int negative = 0;
    char intPart[128] = "", decPart[128] = "";
    char *name, *joined;
    const char *dot;
    if (value[0] == '-') {
        negative = 1;
        value++;
    }
    dot = strchr(value, '.');
    if (dot != NULL) {
        size_t len = (size_t)(dot - value);
        memcpy(intPart, value, len);
        intPart[len] = '\0';
        strcpy(decPart, dot + 1);
    } else {
        strcpy(intPart, value);
    }
    name = processor_getName(intPart);
    if (name[0] == '\0') {
        free(name);
        name = strdup(ZERO_TOKEN);
    } else if (negative) {
        joined = malloc(strlen(MINUS) + strlen(SEPARATOR) + strlen(name) + 1);
        sprintf(joined, "%s%s%s", MINUS, SEPARATOR, name);
        free(name);
        name = joined;
    }
    if (decPart[0] != '\0') {
        joined = malloc(strlen(name) + strlen(UNION_AND) + strlen(decPart) + 64);
        sprintf(joined, "%s%s%s%s%s%s%s", name, SEPARATOR, UNION_AND, SEPARATOR,
                processor_getName(decPart), SEPARATOR, scale_getName(-(int)strlen(decPart)));
        free(name);
        name = joined;
    }
    return name;
}
''',
"csharp": r'''
using System;

public static class NameBuilder
{
    private const string ZeroToken = "zero";
    private const string Minus = "minus";
    private const string Separator = " ";
    private const string UnionAnd = "and";

    private static Func<string, string> processorGetName = v => v;
    private static Func<int, string> scaleGetName = n => n.ToString();

    public static string GetName(string value)
    {
        bool negative = value.StartsWith("-");
        if (negative)
        {
            value = value.Substring(1);
        }
        int decimals = value.IndexOf('.');
        string decimalValue = null;
        if (decimals >= 0)
        {
            decimalValue = value.Substring(decimals + 1);
            value = value.Substring(0, decimals);
        }
        string name = processorGetName(value);
        if (name.Length == 0)
        {
            name = ZeroToken;
        }
        else if (negative)
        {
            name = Minus + Separator + name;
        }
        if (!string.IsNullOrEmpty(decimalValue))
        {
            name = string.Join(Separator, name, UnionAnd,
                processorGetName(decimalValue), scaleGetName(-decimalValue.Length));
        }
        return name;
    }
}
'''}}

DATA_P2["T120"] = {"outputs": {
"python": r'''
def solution(X, A):
    hset = set()
    for i, value in enumerate(A):
        if value <= X:
            hset.add(value)
        if len(hset) == X:
            return i
    return -1
''',
"c": r'''
#include <stdbool.h>
#include <stdlib.h>

static int seen[1000001];

int solution(int X, const int *A, int aLen) {
    int filled = 0;
    for (int i = 0; i < aLen; i++) {
        if (A[i] >= 0 && A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            filled++;
        }
        if (filled == X) return i;
    }
    return -1;
}
''',
"csharp": r'''
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int X, int[] A)
    {
        var hset = new HashSet<int>();
        for (int i = 0; i < A.Length; i++)
        {
            if (A[i] <= X)
            {
                hset.Add(A[i]);
                if (hset.Count == X) return i;
            }
        }
        return -1;
    }
}
'''}}

DATA_P2["T879"] = {"outputs": {
"python": r'''
class Font:
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


class FontTransformer:
    def __init__(self, workbook_new):
        self.workbook_new = workbook_new

    def transform(self, font_old):
        font_new = self.workbook_new.create_font()
        for attr in ("boldweight", "char_set", "color", "font_name", "font_height",
                     "italic", "strikeout", "type_offset", "underline"):
            setattr(font_new, attr, getattr(font_old, attr))
        return font_new
''',
"c": r'''
#include <stdlib.h>

typedef struct {
    int boldweight;
    int charSet;
    int color;
    char *fontName;
    int fontHeight;
    int italic;
    int strikeout;
    int typeOffset;
    int underline;
} Font;

typedef struct { Font *created[64]; int count; } Workbook;

Font *createFont(Workbook *wb) {
    wb->created[wb->count] = malloc(sizeof(Font));
    return wb->created[wb->count++];
}

Font *transform(Workbook *workbookNew, const Font *fontOld) {
    Font *fontNew = createFont(workbookNew);
    const int *src = (const int *)fontOld;
    int *dst = (int *)fontNew;
    for (int i = 0; i < (int)(sizeof(Font) / sizeof(int)); i++)
        dst[i] = src[i];
    return fontNew;
}
''',
"csharp": r'''
public class Font
{
    public short Boldweight;
    public short CharSet;
    public short Color;
    public string FontName;
    public short FontHeight;
    public bool Italic;
    public bool Strikeout;
    public short TypeOffset;
    public short Underline;
}

public class Workbook
{
    public Font CreateFont() { return new Font(); }
}

public class FontTransformer
{
    private readonly Workbook workbookNew = new Workbook();

    public Font Transform(Font fontOld)
    {
        Font fontNew = workbookNew.CreateFont();
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
    }
}
'''}}

DATA_P2["T620"] = {"outputs": {
"python": r'''
def zeroFront(nums):
    if nums is None:
        return None
    zeros_pos = 0
    for i in range(len(nums)):
        if nums[i] == 0:
            nums[i], nums[zeros_pos] = nums[zeros_pos], nums[i]
            zeros_pos += 1
    return nums
''',
"c": r'''
#include <stdlib.h>

int *zeroFront(int *nums, int n) {
    if (nums == NULL) return NULL;
    int zerosPos = 0;
    for (int i = 0; i < n; ++i) {
        if (nums[i] == 0) {
            int tmp = nums[i];
            nums[i] = nums[zerosPos];
            nums[zerosPos] = tmp;
            ++zerosPos;
        }
    }
    return nums;
}
''',
"csharp": r'''
public static class ArrayMover
{
    public static int[] ZeroFront(int[] nums)
    {
        if (nums == null)
        {
            return null;
        }
        int zerosPos = 0;
        for (int i = 0; i < nums.Length; ++i)
        {
            if (nums[i] == 0)
            {
                int tmp = nums[i];
                nums[i] = nums[zerosPos];
                nums[zerosPos] = tmp;
                ++zerosPos;
            }
        }
        return nums;
    }
}
'''}}

DATA_P2["T664"] = {"outputs": {
"python": r'''
class ParameterizedType:
    def __init__(self, raw_type, actual_type_arguments):
        self.raw = raw_type
        self.args = actual_type_arguments

    def get_raw_type(self):
        return self.raw

    def get_actual_type_arguments(self):
        return self.args


def investigate(p, *type_args):
    c = p.get_raw_type()
    b = [c.get_name(), "<"]
    local_args = list(p.get_actual_type_arguments())
    if type_args:
        next_type_arg = 0
        pieces = []
        for local in local_args:
            if isinstance(local, ParameterizedType):
                pieces.append(str(local.get_raw_type()) + "<" + str(type_args[next_type_arg]) + ">")
                next_type_arg += 1
            elif hasattr(local, "assign_from"):
                local_args[next_type_arg] = type_args[next_type_arg]
                pieces.append(str(local_args[next_type_arg]))
                next_type_arg += 1
            else:
                pieces.append(str(local))
        b.append(", ".join(pieces))
        b.append(">")
    else:
        b.append(", ".join(str(a) for a in local_args))
        b.append(">")
    print("".join(b))
    investigate(c, *local_args)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TypeNode {
    char name[64];
    struct TypeNode **args;
    int argCount;
    int isParameterized;
} TypeNode;

void investigate(const TypeNode *c, char **typeArgs, int typeArgCount) {
    char buffer[512];
    strcpy(buffer, c->name);
    strcat(buffer, "<");
    for (int i = 0; i < c->argCount; i++) {
        if (c->args[i]->isParameterized && typeArgCount > 0) {
            strcat(buffer, c->args[i]->name);
            strcat(buffer, "<");
            strcat(buffer, typeArgs[i]);
            strcat(buffer, ">");
        } else {
            strcat(buffer, c->args[i]->name);
        }
        if (i < c->argCount - 1) strcat(buffer, ", ");
    }
    strcat(buffer, ">");
    printf("%s\n", buffer);
    investigate(c, NULL, 0);
}
''',
"csharp": r'''
using System;
using System.Text;

public class TypeNode
{
    public Func<string> GetName;
    public TypeNode[] Args;
    public bool IsParameterized;
}

public static class TypeInvestigator
{
    public static void Investigate(TypeNode p, params TypeNode[] typeArgs)
    {
        TypeNode c = p.GetName != null ? new TypeNode { GetName = p.GetName, Args = p.Args } : p;
        StringBuilder b = new StringBuilder(p.GetName());
        b.Append('<');
        TypeNode[] localArgs = p.Args;
        if (typeArgs != null && typeArgs.Length > 0)
        {
            int nextTypeArg = 0;
            string[] pieces = new string[localArgs.Length];
            for (int i = 0; i < localArgs.Length; i++)
            {
                TypeNode local = localArgs[i];
                if (local.IsParameterized)
                {
                    pieces[i] = local.GetName() + "<" + typeArgs[nextTypeArg++].GetName() + ">";
                }
                else
                {
                    localArgs[nextTypeArg] = typeArgs[nextTypeArg];
                    pieces[i] = localArgs[nextTypeArg].GetName();
                    nextTypeArg++;
                }
            }
            b.Append(string.Join(", ", pieces));
            b.Append('>');
        }
        else
        {
            string[] all = Array.ConvertAll(localArgs, a => a.GetName());
            b.Append(string.Join(", ", all)).Append('>');
        }
        Console.WriteLine(b);
        Investigate(c, localArgs);
    }
}
'''}}
