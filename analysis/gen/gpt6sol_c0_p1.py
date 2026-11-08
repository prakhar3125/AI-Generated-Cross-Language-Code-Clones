DATA1 = {
    "T738": {"outputs": {
        "python": '''def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    i = 3
    while i * i <= number:
        if number % i == 0:
            return False
        i += 2
    return True''',
        "c": r'''int is_prime(int number) {
    if (number < 2) return 0;
    if (number == 2) return 1;
    if (number % 2 == 0) return 0;
    int i = 3;
    while (i * i <= number) {
        if (number % i == 0) return 0;
        i += 2;
    }
    return 1;
}''',
        "csharp": '''static bool IsPrime(int number)
{
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; i * i <= number; i += 2)
    {
        if (number % i == 0) return false;
    }
    return true;
}'''
    }},
    "T862": {"outputs": {
        "python": '''CELL_TYPE_BLANK, CELL_TYPE_BOOLEAN, CELL_TYPE_ERROR, CELL_TYPE_FORMULA, CELL_TYPE_NUMERIC, CELL_TYPE_STRING = range(6)


class CellStyle:
    def hashCode(self):
        return id(self)


class Workbook:
    def create_cell_style(self):
        return CellStyle()


class OldCell:
    def __init__(self, cell_type, style, comment=None, bool_value=False, error_value=0,
                 formula="", numeric_value=0.0, string_value=""):
        self._cell_type = cell_type
        self._style = style
        self._comment = comment
        self._bool_value = bool_value
        self._error_value = error_value
        self._formula = formula
        self._numeric_value = numeric_value
        self._string_value = string_value

    def get_cell_comment(self):
        return self._comment

    def get_cell_style(self):
        return self._style

    def get_cell_type(self):
        return self._cell_type

    def get_boolean_cell_value(self):
        return self._bool_value

    def get_error_cell_value(self):
        return self._error_value

    def get_cell_formula(self):
        return self._formula

    def get_numeric_cell_value(self):
        return self._numeric_value

    def get_string_cell_value(self):
        return self._string_value


class NewCell:
    def __init__(self):
        self.comment = None
        self.style = None
        self.value = None

    def set_cell_comment(self, comment):
        self.comment = comment

    def set_cell_style(self, style):
        self.style = style

    def set_cell_value(self, value):
        self.value = value


class CellMigrator:
    def __init__(self):
        self.style_map = {}
        self.workbook_new = Workbook()

    def transform(self, cell_old, cell_new):
        cell_new.set_cell_comment(cell_old.get_cell_comment())
        style_hash = cell_old.get_cell_style().hashCode()
        if style_hash not in self.style_map:
            self.style_map[style_hash] = self.workbook_new.create_cell_style()
        cell_new.set_cell_style(self.style_map[style_hash])
        kind = cell_old.get_cell_type()
        readers = {
            CELL_TYPE_BOOLEAN: cell_old.get_boolean_cell_value,
            CELL_TYPE_ERROR: cell_old.get_error_cell_value,
            CELL_TYPE_FORMULA: cell_old.get_cell_formula,
            CELL_TYPE_NUMERIC: cell_old.get_numeric_cell_value,
            CELL_TYPE_STRING: cell_old.get_string_cell_value,
        }
        if kind in readers:
            cell_new.set_cell_value(readers[kind]())
        elif kind != CELL_TYPE_BLANK:
            print("transform: Unbekannter Zellentyp " + str(kind))''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>

enum cell_kind { CELL_BLANK, CELL_BOOLEAN, CELL_ERROR, CELL_FORMULA, CELL_NUMERIC, CELL_STRING };

typedef struct cell_style { int hash; } CellStyle;

typedef struct cell {
    int kind;
    int bool_value;
    int error_value;
    char *formula;
    double numeric_value;
    char *string_value;
    CellStyle *style;
    void *comment;
} Cell;

#define STYLE_MAP_SIZE 4096
static CellStyle *style_map[STYLE_MAP_SIZE];

static CellStyle *create_cell_style(void) {
    static int next_hash = 1;
    CellStyle *s = malloc(sizeof(CellStyle));
    s->hash = next_hash++;
    return s;
}

void transform(Cell *cellOld, Cell *cellNew) {
    cellNew->comment = cellOld->comment;
    int hash = cellOld->style->hash % STYLE_MAP_SIZE;
    if (style_map[hash] == NULL) {
        style_map[hash] = create_cell_style();
    }
    cellNew->style = style_map[hash];
    switch (cellOld->kind) {
        case CELL_BLANK:
            break;
        case CELL_BOOLEAN:
            cellNew->bool_value = cellOld->bool_value;
            break;
        case CELL_ERROR:
            cellNew->error_value = cellOld->error_value;
            break;
        case CELL_FORMULA:
            cellNew->formula = cellOld->formula;
            break;
        case CELL_NUMERIC:
            cellNew->numeric_value = cellOld->numeric_value;
            break;
        case CELL_STRING:
            cellNew->string_value = cellOld->string_value;
            break;
        default:
            printf("transform: Unbekannter Zellentyp %d\n", cellOld->kind);
    }
}''',
        "csharp": '''using System;
using System.Collections.Generic;

public enum CellKind { Blank, Boolean, Error, Formula, Numeric, String }

public class CellStyle
{
}

public class Cell
{
    public CellKind Kind { get; set; }
    public CellStyle Style { get; set; }
    public object Comment { get; set; }
    public bool BoolValue { get; set; }
    public int ErrorValue { get; set; }
    public string Formula { get; set; }
    public double NumericValue { get; set; }
    public string StringValue { get; set; }
}

public class Workbook
{
    public CellStyle CreateCellStyle()
    {
        return new CellStyle();
    }
}

public class CellMigrator
{
    private readonly Dictionary<int, CellStyle> styleMap = new Dictionary<int, CellStyle>();
    private readonly Workbook workbookNew = new Workbook();

    public void Transform(Cell cellOld, Cell cellNew)
    {
        cellNew.Comment = cellOld.Comment;
        int hash = cellOld.Style.GetHashCode();
        if (!styleMap.ContainsKey(hash))
        {
            styleMap[hash] = workbookNew.CreateCellStyle();
        }
        cellNew.Style = styleMap[hash];
        switch (cellOld.Kind)
        {
            case CellKind.Blank:
                break;
            case CellKind.Boolean:
                cellNew.BoolValue = cellOld.BoolValue;
                break;
            case CellKind.Error:
                cellNew.ErrorValue = cellOld.ErrorValue;
                break;
            case CellKind.Formula:
                cellNew.Formula = cellOld.Formula;
                break;
            case CellKind.Numeric:
                cellNew.NumericValue = cellOld.NumericValue;
                break;
            case CellKind.String:
                cellNew.StringValue = cellOld.StringValue;
                break;
            default:
                Console.WriteLine("transform: Unbekannter Zellentyp " + cellOld.Kind);
                break;
        }
    }
}'''
    }},
    "T203": {"outputs": {
        "python": '''import gzip


def main():
    try:
        data_to_compress = "This is the test data.".encode("iso-8859-1")
        compressed_data = gzip.compress(data_to_compress)
        with open("C:/Users/UserName/Desktop/zip_file.gz", "wb") as file_stream:
            file_stream.write(compressed_data)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    unsigned char *data;
    size_t length;
} Buffer;

extern int gzip_compress(const unsigned char *src, size_t src_len, Buffer *dst);

int main(void) {
    const char *text = "This is the test data.";
    Buffer compressed;
    if (gzip_compress((const unsigned char *) text, strlen(text), &compressed) != 0) {
        fprintf(stderr, "compression failed\n");
        return 1;
    }
    FILE *fileStream = fopen("C:/Users/UserName/Desktop/zip_file.gz", "wb");
    if (fileStream == NULL) {
        perror("fopen failed");
        free(compressed.data);
        return 1;
    }
    fwrite(compressed.data, 1, compressed.length, fileStream);
    fclose(fileStream);
    free(compressed.data);
    return 0;
}''',
        "csharp": '''using System;
using System.IO;
using System.IO.Compression;
using System.Text;

public static class Program
{
    public static void Main(string[] args)
    {
        try
        {
            byte[] dataToCompress = Encoding.GetEncoding("ISO-8859-1").GetBytes("This is the test data.");
            using (var memoryStream = new MemoryStream())
            {
                using (var zipStream = new GZipStream(memoryStream, CompressionMode.Compress, true))
                {
                    zipStream.Write(dataToCompress, 0, dataToCompress.Length);
                }
                File.WriteAllBytes("C:/Users/UserName/Desktop/zip_file.gz", memoryStream.ToArray());
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }
    }
}'''
    }},
    "T210": {"outputs": {
        "python": r'''import os


def input_stream_to_string(input_stream):
    result_parts = []
    first = True
    for raw_line in iter(input_stream.readline, b""):
        line = raw_line.decode("utf-8").rstrip("\r\n")
        if first:
            result_parts.append(line)
            first = False
        else:
            result_parts.append(os.linesep + line)
    return "".join(result_parts)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *input_stream_to_string(FILE *input_stream) {
    size_t capacity = 256;
    size_t length = 0;
    char *result = malloc(capacity);
    char line[1024];
    int first = 1;
    while (fgets(line, sizeof(line), input_stream) != NULL) {
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len - 1] == '\n') {
            line[--line_len] = '\0';
        }
        size_t needed = length + (first ? 0 : 1) + line_len + 1;
        if (needed > capacity) {
            capacity = needed * 2;
            result = realloc(result, capacity);
        }
        if (!first) {
            result[length++] = '\n';
        }
        memcpy(result + length, line, line_len + 1);
        length += line_len;
        first = 0;
    }
    result[length] = '\0';
    return result;
}''',
        "csharp": '''using System;
using System.IO;
using System.Text;

public class StreamHelper
{
    public string InputStreamToString(Stream inputStream)
    {
        var result = new StringBuilder();
        string newLine = Environment.NewLine;
        using (var reader = new StreamReader(inputStream))
        {
            bool first = true;
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                if (!first)
                {
                    result.Append(newLine);
                }
                result.Append(line);
                first = false;
            }
        }
        return result.ToString();
    }
}'''
    }},
}
