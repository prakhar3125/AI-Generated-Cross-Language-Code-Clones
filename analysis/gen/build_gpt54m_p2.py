# -*- coding: utf-8 -*-
DATA2 = {
"T862": {
"python": r'''
class Cell:
    CELL_TYPE_BLANK = 0
    CELL_TYPE_BOOLEAN = 1
    CELL_TYPE_ERROR = 2
    CELL_TYPE_FORMULA = 3
    CELL_TYPE_NUMERIC = 4
    CELL_TYPE_STRING = 5


class StyleStore:
    pass


workbookNew = type("Workbook", (), {"createCellStyle": staticmethod(lambda: object())})()
styleMap = {}


def transformStyle(hash_, styleOld, styleNew):
    styleMap[hash_] = styleNew


def transform(cellOld, cellNew):
    cellNew.setCellComment(cellOld.getCellComment())
    hash_ = cellOld.getCellStyle().hashCode()
    if hash_ not in styleMap:
        transformStyle(hash_, cellOld.getCellStyle(), workbookNew.createCellStyle())
    cellNew.setCellStyle(styleMap[hash_])
    cellType = cellOld.getCellType()
    handlers = {
        Cell.CELL_TYPE_BLANK: lambda: None,
        Cell.CELL_TYPE_BOOLEAN: lambda: cellNew.setCellValue(cellOld.getBooleanCellValue()),
        Cell.CELL_TYPE_ERROR: lambda: cellNew.setCellValue(cellOld.getErrorCellValue()),
        Cell.CELL_TYPE_FORMULA: lambda: cellNew.setCellValue(cellOld.getCellFormula()),
        Cell.CELL_TYPE_NUMERIC: lambda: cellNew.setCellValue(cellOld.getNumericCellValue()),
        Cell.CELL_TYPE_STRING: lambda: cellNew.setCellValue(cellOld.getStringCellValue()),
    }
    if cellType in handlers:
        handlers[cellType]()
    else:
        print("transform: Unbekannter Zellentyp " + str(cellType))
''',
"c": r'''
#include <stdio.h>

enum {
    CELL_TYPE_BLANK, CELL_TYPE_BOOLEAN, CELL_TYPE_ERROR,
    CELL_TYPE_FORMULA, CELL_TYPE_NUMERIC, CELL_TYPE_STRING
};

typedef struct { int dummy; } Style;
typedef struct { int cell; } XSSFCell;
typedef struct { int dummy; } Workbook;

extern int getCellComment(XSSFCell *c);
extern Style *getCellStyle(XSSFCell *c);
extern int cellHashCode(Style *s);
extern int getCellType(XSSFCell *c);
extern int getBooleanCellValue(XSSFCell *c);
extern int getErrorCellValue(XSSFCell *c);
extern char *getCellFormula(XSSFCell *c);
extern double getNumericCellValue(XSSFCell *c);
extern char *getStringCellValue(XSSFCell *c);
extern void setCellComment(XSSFCell *c, int comment);
extern void setCellStyle(XSSFCell *c, Style *s);
extern void setCellValueInt(XSSFCell *c, int v);
extern void setCellValueDouble(XSSFCell *c, double v);
extern void setCellValueStr(XSSFCell *c, const char *v);
extern Style *createCellStyle(Workbook *wb);
extern Style *styleMapGet(int hash);
extern void transformStyle(int hash, Style *styleOld, Style *styleNew);
extern Workbook workbookNew;

void transform(XSSFCell *cellOld, XSSFCell *cellNew) {
    setCellComment(cellNew, getCellComment(cellOld));
    int hash = cellHashCode(getCellStyle(cellOld));
    if (styleMapGet(hash) == NULL) {
        transformStyle(hash, getCellStyle(cellOld), createCellStyle(&workbookNew));
    }
    setCellStyle(cellNew, styleMapGet(hash));
    switch (getCellType(cellOld)) {
        case CELL_TYPE_BLANK:
            break;
        case CELL_TYPE_BOOLEAN:
            setCellValueInt(cellNew, getBooleanCellValue(cellOld));
            break;
        case CELL_TYPE_ERROR:
            setCellValueInt(cellNew, getErrorCellValue(cellOld));
            break;
        case CELL_TYPE_FORMULA:
            setCellValueStr(cellNew, getCellFormula(cellOld));
            break;
        case CELL_TYPE_NUMERIC:
            setCellValueDouble(cellNew, getNumericCellValue(cellOld));
            break;
        case CELL_TYPE_STRING:
            setCellValueStr(cellNew, getStringCellValue(cellOld));
            break;
        default:
            printf("transform: Unbekannter Zellentyp %d\n", getCellType(cellOld));
    }
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public class Cell {
    public const int CELL_TYPE_BLANK = 0;
    public const int CELL_TYPE_BOOLEAN = 1;
    public const int CELL_TYPE_ERROR = 2;
    public const int CELL_TYPE_FORMULA = 3;
    public const int CELL_TYPE_NUMERIC = 4;
    public const int CELL_TYPE_STRING = 5;
}

public class CellStyle { }

public class Workbook {
    public CellStyle CreateCellStyle() {
        return new CellStyle();
    }
}

public class CellTransformer {
    private Dictionary<int, CellStyle> styleMap = new Dictionary<int, CellStyle>();
    private Workbook workbookNew = new Workbook();

    public void Transform(dynamic cellOld, dynamic cellNew) {
        cellNew.setCellComment(cellOld.getCellComment());
        int hash = cellOld.getCellStyle().GetHashCode();
        if (!styleMap.ContainsKey(hash)) {
            TransformStyle(hash, cellOld.getCellStyle(), workbookNew.CreateCellStyle());
        }
        cellNew.setCellStyle(styleMap[hash]);
        switch (cellOld.getCellType()) {
            case Cell.CELL_TYPE_BLANK:
                break;
            case Cell.CELL_TYPE_BOOLEAN:
                cellNew.setCellValue(cellOld.getBooleanCellValue());
                break;
            case Cell.CELL_TYPE_ERROR:
                cellNew.setCellValue(cellOld.getErrorCellValue());
                break;
            case Cell.CELL_TYPE_FORMULA:
                cellNew.setCellValue(cellOld.getCellFormula());
                break;
            case Cell.CELL_TYPE_NUMERIC:
                cellNew.setCellValue(cellOld.getNumericCellValue());
                break;
            case Cell.CELL_TYPE_STRING:
                cellNew.setCellValue(cellOld.getStringCellValue());
                break;
            default:
                Console.WriteLine("transform: Unbekannter Zellentyp " + cellOld.getCellType());
                break;
        }
    }

    private void TransformStyle(int hash, CellStyle styleOld, CellStyle styleNew) {
        styleMap[hash] = styleNew;
    }
}
'''
},
"T879": {
"python": r'''
class HSSFFont:
    def __init__(self):
        self.boldweight = 0
        self.charSet = 0
        self.color = 0
        self.fontName = ""
        self.fontHeight = 0
        self.italic = False
        self.strikeout = False
        self.typeOffset = 0
        self.underline = 0


class Workbook:
    def createFont(self):
        return HSSFFont()


def transform(workbookNew, fontOld):
    fontNew = workbookNew.createFont()
    for attribute in ("boldweight", "charSet", "color", "fontName", "fontHeight",
                      "italic", "strikeout", "typeOffset", "underline"):
        setattr(fontNew, attribute, getattr(fontOld, attribute))
    return fontNew
''',
"c": r'''
#include <string.h>

#define MAX_FONT_NAME 64

typedef struct {
    int boldweight;
    int charSet;
    int color;
    char fontName[MAX_FONT_NAME];
    int fontHeight;
    int italic;
    int strikeout;
    int typeOffset;
    int underline;
} HSSFFont;

typedef struct {
    HSSFFont *font;
    int fontCount;
} Workbook;

HSSFFont *create_font(Workbook *wb) {
    wb->fontCount++;
    return wb->font;
}

HSSFFont *transform(Workbook *workbookNew, const HSSFFont *fontOld) {
    HSSFFont *fontNew = create_font(workbookNew);
    fontNew->boldweight = fontOld->boldweight;
    fontNew->charSet = fontOld->charSet;
    fontNew->color = fontOld->color;
    strncpy(fontNew->fontName, fontOld->fontName, MAX_FONT_NAME - 1);
    fontNew->fontHeight = fontOld->fontHeight;
    fontNew->italic = fontOld->italic;
    fontNew->strikeout = fontOld->strikeout;
    fontNew->typeOffset = fontOld->typeOffset;
    fontNew->underline = fontOld->underline;
    return fontNew;
}
''',
"csharp": r'''
public class HSSFFont {
    public int Boldweight { get; set; }
    public int CharSet { get; set; }
    public int Color { get; set; }
    public string FontName { get; set; }
    public int FontHeight { get; set; }
    public bool Italic { get; set; }
    public bool Strikeout { get; set; }
    public int TypeOffset { get; set; }
    public int Underline { get; set; }
}

public class HSSFWorkbook {
    public HSSFFont CreateFont() {
        return new HSSFFont();
    }
}

public class FontTransformer {
    private HSSFFont Transform(HSSFWorkbook workbookNew, HSSFFont fontOld) {
        HSSFFont fontNew = workbookNew.CreateFont();
        foreach (var prop in typeof(HSSFFont).GetProperties()) {
            prop.SetValue(fontNew, prop.GetValue(fontOld));
        }
        return fontNew;
    }
}
'''
}
}
