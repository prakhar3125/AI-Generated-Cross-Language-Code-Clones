DATA2 = {}

DATA2["T323"] = {
    "python": """class Processor:
    def getName(self, value):
        return value

class Scale:
    def getName(self, n):
        return ""

processor = Processor()
SCALE = Scale()
ZERO_TOKEN = "zero"
MINUS = "minus"
SEPARATOR = " "
UNION_AND = "and"

def getName(value):
    negative = value.startswith("-")
    if negative:
        value = value[1:]
    decimals = value.find(".")
    decimalValue = None
    if decimals >= 0:
        decimalValue = value[decimals + 1:]
        value = value[:decimals]
    name = processor.getName(value)
    if not name:
        name = ZERO_TOKEN
    elif negative:
        name = MINUS + SEPARATOR + name
    if decimalValue:
        name = (name + SEPARATOR + UNION_AND + SEPARATOR +
                processor.getName(decimalValue) + SEPARATOR +
                SCALE.getName(-len(decimalValue)))
    return name""",
    "c": """extern void processor_getName(const char *value, char *out, size_t outLen);
extern void scale_getName(int n, char *out, size_t outLen);

void getName(const char *value, char *result, size_t resultLen) {
    char name[256], intValue[64], decimalValue[64];
    int negative = 0;
    if (value[0] == '-') {
        negative = 1;
        value++;
    }
    char *dot = strchr(value, '.');
    decimalValue[0] = '\\0';
    if (dot != NULL) {
        size_t intLen = (size_t)(dot - value);
        strncpy(intValue, value, intLen);
        intValue[intLen] = '\\0';
        strcpy(decimalValue, dot + 1);
    } else {
        strcpy(intValue, value);
    }
    processor_getName(intValue, name, sizeof(name));
    if (name[0] == '\\0') {
        strcpy(name, "zero");
    } else if (negative) {
        char tmp[512];
        snprintf(tmp, sizeof(tmp), "minus %s", name);
        strcpy(name, tmp);
    }
    if (decimalValue[0] != '\\0') {
        char scaleName[64], tail[512];
        scale_getName(-(int)strlen(decimalValue), scaleName, sizeof(scaleName));
        snprintf(tail, sizeof(tail), " and %s %s", decimalValue, scaleName);
        strcat(name, tail);
    }
    snprintf(result, resultLen, "%s", name);
}""",
    "csharp": """using System;

public class Processor { public string GetName(string v) { return v; } }
public class Scale { public string GetName(int n) { return ""; } }

public class NameFormatter
{
    private Processor processor = new Processor();
    private Scale SCALE = new Scale();
    private const string ZERO_TOKEN = "zero";
    private const string MINUS = "minus";
    private const string SEPARATOR = " ";
    private const string UNION_AND = "and";

    public string GetName(string value)
    {
        bool negative = value.StartsWith("-");
        if (negative) value = value.Substring(1);
        int decimals = value.IndexOf(".");
        string decimalValue = null;
        if (decimals >= 0)
        {
            decimalValue = value.Substring(decimals + 1);
            value = value.Substring(0, decimals);
        }
        string name = processor.GetName(value);
        if (name.Length == 0)
        {
            name = ZERO_TOKEN;
        }
        else if (negative)
        {
            name = MINUS + SEPARATOR + name;
        }
        if (!string.IsNullOrEmpty(decimalValue))
        {
            name = name + SEPARATOR + UNION_AND + SEPARATOR + processor.GetName(decimalValue)
                 + SEPARATOR + SCALE.GetName(-decimalValue.Length);
        }
        return name;
    }
}""",
}

DATA2["T120"] = {
    "python": """def solution(X, A):
    hset = set()
    for i in range(len(A)):
        if A[i] <= X:
            hset.add(A[i])
        if len(hset) == X:
            return i
    return -1""",
    "c": """int solution(int X, const int *A, int len) {
    char *seen = calloc(X + 1, 1);
    int distinct = 0;
    for (int i = 0; i < len; i++) {
        if (A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
        }
        if (distinct == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}""",
    "csharp": """using System.Collections.Generic;

public int Solution(int X, int[] A)
{
    var hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}""",
}

DATA2["T879"] = {
    "python": """class HSSFFont:
    def __init__(self):
        self.boldweight = self.charset = self.color = None
        self.fontName = self.fontHeight = None
        self.italic = self.strikeout = self.typeOffset = self.underline = None
    def setBoldweight(self, v): self.boldweight = v
    def setCharSet(self, v): self.charset = v
    def setColor(self, v): self.color = v
    def setFontName(self, v): self.fontName = v
    def setFontHeight(self, v): self.fontHeight = v
    def setItalic(self, v): self.italic = v
    def setStrikeout(self, v): self.strikeout = v
    def setTypeOffset(self, v): self.typeOffset = v
    def setUnderline(self, v): self.underline = v

class XSSFFont:
    def __init__(self):
        self.boldweight = self.charset = self.color = None
        self.fontName = self.fontHeight = None
        self.italic = self.strikeout = self.typeOffset = self.underline = None

class WorkbookNew:
    def createFont(self):
        return HSSFFont()

def transform(workbookNew, fontOld):
    fontNew = workbookNew.createFont()
    fontNew.setBoldweight(fontOld.boldweight)
    fontNew.setCharSet(fontOld.charset)
    fontNew.setColor(fontOld.color)
    fontNew.setFontName(fontOld.fontName)
    fontNew.setFontHeight(fontOld.fontHeight)
    fontNew.setItalic(fontOld.italic)
    fontNew.setStrikeout(fontOld.strikeout)
    fontNew.setTypeOffset(fontOld.typeOffset)
    fontNew.setUnderline(fontOld.underline)
    return fontNew""",
    "c": """typedef struct {
    int boldweight, charSet, color, fontHeight;
    int italic, strikeout, typeOffset, underline;
    char fontName[64];
} FontProps;

FontProps *transformFont(FontProps *fontOld) {
    FontProps *fontNew = calloc(1, sizeof(FontProps));
    fontNew->boldweight = fontOld->boldweight;
    fontNew->charSet = fontOld->charSet;
    fontNew->color = fontOld->color;
    fontNew->fontHeight = fontOld->fontHeight;
    fontNew->italic = fontOld->italic;
    fontNew->strikeout = fontOld->strikeout;
    fontNew->typeOffset = fontOld->typeOffset;
    fontNew->underline = fontOld->underline;
    strcpy(fontNew->fontName, fontOld->fontName);
    return fontNew;
}""",
    "csharp": """public class HSSFFont
{
    public short Boldweight { get; set; }
    public short CharSet { get; set; }
    public short Color { get; set; }
    public string FontName { get; set; }
    public short FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public short TypeOffset { get; set; }
    public short Underline { get; set; }
}

public class XSSFFont
{
    public short Boldweight { get; set; }
    public short CharSet { get; set; }
    public short Color { get; set; }
    public string FontName { get; set; }
    public short FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public short TypeOffset { get; set; }
    public short Underline { get; set; }
}

public class WorkbookNew { public HSSFFont CreateFont() { return new HSSFFont(); } }

public HSSFFont Transform(WorkbookNew workbookNew, XSSFFont fontOld)
{
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
}""",
}

DATA2["T620"] = {
    "python": """def zero_front(nums):
    if nums is None:
        return None
    zerosPos = 0
    for i in range(len(nums)):
        if nums[i] == 0:
            nums[i], nums[zerosPos] = nums[zerosPos], 0
            zerosPos += 1
    return nums""",
    "c": """int *zeroFront(int *nums, int len) {
    if (nums == NULL) return NULL;
    int zerosPos = 0;
    int i = 0;
    while (i < len) {
        if (nums[i] == 0) {
            nums[i] = nums[zerosPos];
            nums[zerosPos] = 0;
            zerosPos++;
        }
        i++;
    }
    return nums;
}""",
    "csharp": """public int[] ZeroFront(int[] nums)
{
    if (nums == null) return null;
    int zerosPos = 0;
    for (int i = 0; i < nums.Length; i++)
    {
        if (nums[i] == 0)
        {
            nums[i] = nums[zerosPos];
            nums[zerosPos] = 0;
            zerosPos++;
        }
    }
    return nums;
}""",
}

DATA2["T664"] = {
    "python": """class ParameterizedType:
    def __init__(self, raw_name, args):
        self.raw_name = raw_name
        self.args = args
    def getRawType(self):
        return self.raw_name
    def getActualTypeArguments(self):
        return self.args

def investigate(p, *typeArgs):
    c = p.getRawType()
    parts = [str(c)]
    localArgs = list(p.getActualTypeArguments())
    if typeArgs and len(typeArgs) > 0:
        nextTypeArg = 0
        inner = []
        for local in localArgs:
            if isinstance(local, ParameterizedType):
                inner.append(str(local.getRawType()) + '<' + str(typeArgs[nextTypeArg]) + '>')
                nextTypeArg += 1
            elif isinstance(local, str) and local.startswith('T'):
                localArgs[nextTypeArg] = typeArgs[nextTypeArg]
                inner.append(str(localArgs[nextTypeArg]))
                nextTypeArg += 1
            else:
                inner.append(str(local))
        parts.append('<')
        parts.append(', '.join(inner))
        parts.append('>')
    else:
        parts.append('<')
        parts.append(', '.join(str(x) for x in localArgs))
        parts.append('>')
    print(''.join(parts))
    investigate(c, *localArgs)""",
    "c": """typedef struct Type {
    char name[64];
    struct Type *args[8];
    int argCount;
} Type;

void investigate(Type *p, Type **typeArgs, int typeArgCount) {
    printf("%s<", p->name);
    int nextTypeArg = 0;
    for (int i = 0; i < p->argCount; i++) {
        Type *local = p->args[i];
        if (local->argCount > 0 && typeArgs != NULL && nextTypeArg < typeArgCount) {
            printf("%s<%s>", local->name, typeArgs[nextTypeArg++]->name);
        } else {
            printf("%s", local->name);
        }
        if (i < p->argCount - 1) printf(", ");
    }
    printf(">\\n");
    for (int i = 0; i < p->argCount; i++) {
        investigate(p->args[i], NULL, 0);
    }
}""",
    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public class MyType
{
    public string Name { get; set; }
    public List<MyType> Args { get; set; }
}

public static void Investigate(MyType p, params MyType[] typeArgs)
{
    var b = new StringBuilder(p.Name);
    b.Append('<');
    var localArgs = new List<MyType>(p.Args);
    if (typeArgs != null && typeArgs.Length > 0)
    {
        int nextTypeArg = 0;
        var inner = new List<string>();
        foreach (var local in p.Args)
        {
            if (local.Args != null && local.Args.Count > 0 && nextTypeArg < typeArgs.Length)
            {
                inner.Add(local.Name + "<" + typeArgs[nextTypeArg++].Name + ">");
            }
            else
            {
                inner.Add(local.Name);
            }
        }
        b.Append(string.Join(", ", inner));
        b.Append('>');
    }
    else
    {
        b.Append(string.Join(", ", localArgs.Select(a => a.Name)));
        b.Append('>');
    }
    Console.WriteLine(b);
}""",
}

DATA2["T706"] = {
    "python": """import random

def shuffle(text):
    characters = list(text)
    for i in range(len(characters)):
        randomIndex = random.randrange(len(characters))
        characters[i], characters[randomIndex] = characters[randomIndex], characters[i]
    return "".join(characters)""",
    "c": """char *shuffle(const char *text) {
    size_t len = strlen(text);
    char *characters = strdup(text);
    for (size_t i = 0; i < len; i++) {
        size_t randomIndex = rand() % len;
        char temp = characters[i];
        characters[i] = characters[randomIndex];
        characters[randomIndex] = temp;
    }
    return characters;
}""",
    "csharp": """using System;

public static string Shuffle(string text)
{
    char[] characters = text.ToCharArray();
    Random rnd = new Random();
    for (int i = 0; i < characters.Length; i++)
    {
        int randomIndex = rnd.Next(characters.Length);
        char temp = characters[i];
        characters[i] = characters[randomIndex];
        characters[randomIndex] = temp;
    }
    return new string(characters);
}""",
}
