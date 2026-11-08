DATA = {}

DATA["T738"] = {"outputs": {
"python": r'''
def is_prime(number):
    if number == 2:
        return True
    if number < 2 or number % 2 == 0:
        return False
    i = 3
    while i * i <= number:
        if number % i == 0:
            return False
        i += 2
    return True
''',
"c": r'''
#include <stdbool.h>

bool isPrime(int number) {
    if (number == 2) return true;
    if (number < 2 || number % 2 == 0) return false;
    int i = 3;
    while (i * i <= number) {
        if (number % i == 0) return false;
        i += 2;
    }
    return true;
}
''',
"csharp": r'''
public static class PrimeCheck
{
    public static bool IsPrime(int number)
    {
        if (number == 2) return true;
        if (number < 2 || number % 2 == 0) return false;
        for (int i = 3; i * i <= number; i += 2)
        {
            if (number % i == 0) return false;
        }
        return true;
    }
}
'''}}

DATA["T862"] = {"outputs": {
"python": r'''
class Cell:
    CELL_TYPE_BLANK, CELL_TYPE_BOOLEAN, CELL_TYPE_ERROR, CELL_TYPE_FORMULA, CELL_TYPE_NUMERIC, CELL_TYPE_STRING = range(6)

    def __init__(self):
        self.comment = None
        self.style = None
        self.value = None

    def get_cell_comment(self): return self.comment
    def set_cell_comment(self, c): self.comment = c
    def get_cell_style(self): return self.style
    def set_cell_style(self, s): self.style = s
    def get_cell_type(self): return self._type
    def get_boolean_cell_value(self): return self.value
    def get_error_cell_value(self): return self.value
    def get_cell_formula(self): return self.value
    def get_numeric_cell_value(self): return self.value
    def get_string_cell_value(self): return self.value
    def set_cell_value(self, v): self.value = v


class CellStyle:
    pass


class Workbook:
    def create_cell_style(self):
        return CellStyle()


class CellTransformer:
    def __init__(self, workbook_new):
        self.workbook_new = workbook_new
        self.style_map = {}

    def transform(self, cell_old, cell_new):
        cell_new.set_cell_comment(cell_old.get_cell_comment())
        h = hash(cell_old.get_cell_style())
        if h not in self.style_map:
            self.style_map[h] = self.workbook_new.create_cell_style()
        cell_new.set_cell_style(self.style_map[h])
        t = cell_old.get_cell_type()
        handlers = {
            Cell.CELL_TYPE_BOOLEAN: cell_old.get_boolean_cell_value,
            Cell.CELL_TYPE_ERROR: cell_old.get_error_cell_value,
            Cell.CELL_TYPE_FORMULA: cell_old.get_cell_formula,
            Cell.CELL_TYPE_NUMERIC: cell_old.get_numeric_cell_value,
            Cell.CELL_TYPE_STRING: cell_old.get_string_cell_value,
        }
        if t in handlers:
            cell_new.set_cell_value(handlers[t]())
        elif t != Cell.CELL_TYPE_BLANK:
            print("transform: Unbekannter Zellentyp " + str(t))
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>

enum { CELL_TYPE_BLANK, CELL_TYPE_BOOLEAN, CELL_TYPE_ERROR, CELL_TYPE_FORMULA, CELL_TYPE_NUMERIC, CELL_TYPE_STRING };

typedef struct { int hash; } CellStyle;
typedef struct Cell {
    int type;
    double numericValue;
    int booleanValue;
    int errorValue;
    char *stringValue;
    void *comment;
    CellStyle *style;
} Cell;
typedef struct { CellStyle *created[64]; int count; } Workbook;

static CellStyle *mapKeys[64];
static CellStyle *mapVals[64];
static int mapSize = 0;

CellStyle *createCellStyle(Workbook *wb) {
    wb->created[wb->count] = malloc(sizeof(CellStyle));
    return wb->created[wb->count++];
}

void transform(Workbook *workbookNew, Cell *cellOld, Cell *cellNew) {
    cellNew->comment = cellOld->comment;
    CellStyle *oldStyle = cellOld->style;
    CellStyle *mapped = NULL;
    for (int i = 0; i < mapSize && mapped == NULL; i++)
        if (mapKeys[i] == oldStyle) mapped = mapVals[i];
    if (mapped == NULL) {
        mapped = createCellStyle(workbookNew);
        mapKeys[mapSize] = oldStyle;
        mapVals[mapSize] = mapped;
        mapSize++;
    }
    cellNew->style = mapped;
    int t = cellOld->type;
    if (t == CELL_TYPE_BOOLEAN) cellNew->booleanValue = cellOld->booleanValue;
    else if (t == CELL_TYPE_ERROR) cellNew->errorValue = cellOld->errorValue;
    else if (t == CELL_TYPE_FORMULA) cellNew->stringValue = cellOld->stringValue;
    else if (t == CELL_TYPE_NUMERIC) cellNew->numericValue = cellOld->numericValue;
    else if (t == CELL_TYPE_STRING) cellNew->stringValue = cellOld->stringValue;
    else if (t != CELL_TYPE_BLANK) printf("transform: Unbekannter Zellentyp %d\n", t);
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public enum CellType { Blank, Boolean, Error, Formula, Numeric, String }

public class CellStyle { }

public class Cell
{
    public CellType Type;
    public object Value;
    public object Comment;
    public CellStyle Style;
}

public class Workbook
{
    public CellStyle CreateCellStyle() { return new CellStyle(); }
}

public class CellTransformer
{
    private readonly Workbook workbookNew = new Workbook();
    private readonly Dictionary<int, CellStyle> styleMap = new Dictionary<int, CellStyle>();

    public void Transform(Cell cellOld, Cell cellNew)
    {
        cellNew.Comment = cellOld.Comment;
        int hash = cellOld.Style.GetHashCode();
        if (!styleMap.ContainsKey(hash))
        {
            styleMap[hash] = workbookNew.CreateCellStyle();
        }
        cellNew.Style = styleMap[hash];
        switch (cellOld.Type)
        {
            case CellType.Boolean:
                cellNew.Value = cellOld.Value;
                break;
            case CellType.Error:
                cellNew.Value = cellOld.Value;
                break;
            case CellType.Formula:
            case CellType.Numeric:
            case CellType.String:
                cellNew.Value = cellOld.Value;
                break;
            case CellType.Blank:
                break;
            default:
                Console.WriteLine("transform: Unbekannter Zellentyp " + cellOld.Type);
                break;
        }
    }
}
'''}}

DATA["T203"] = {"outputs": {
"python": r'''
import gzip


def main():
    data_to_compress = "This is the test data.".encode("iso-8859-1")
    try:
        with gzip.open("C:/Users/UserName/Desktop/zip_file.gz", "wb") as zip_stream:
            zip_stream.write(data_to_compress)
    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

int main(void) {
    const char *dataToCompress = "This is the test data.";
    size_t len = strlen(dataToCompress);
    uLongf bound = compressBound((uLong)len);
    Bytef *compressedData = malloc(bound);
    FILE *fileStream;
    if (compressedData == NULL) {
        fputs("allocation failed\n", stderr);
        return 1;
    }
    if (compress2(compressedData, &bound, (const Bytef *)dataToCompress, (uLong)len, Z_BEST_COMPRESSION) != Z_OK) {
        fprintf(stderr, "compression failed\n");
        free(compressedData);
        return 1;
    }
    fileStream = fopen("C:/Users/UserName/Desktop/zip_file.gz", "wb");
    if (fileStream == NULL) {
        perror("fopen failed");
        free(compressedData);
        return 1;
    }
    if (fwrite(compressedData, 1, (size_t)bound, fileStream) != (size_t)bound) {
        fprintf(stderr, "write failed\n");
    }
    fclose(fileStream);
    free(compressedData);
    return 0;
}
''',
"csharp": r'''
using System;
using System.IO;
using System.IO.Compression;
using System.Text;

public static class Compressor
{
    public static void Main(string[] args)
    {
        try
        {
            byte[] dataToCompress = Encoding.GetEncoding("ISO-8859-1").GetBytes("This is the test data.");
            using (FileStream fileStream = new FileStream("C:/Users/UserName/Desktop/zip_file.gz", FileMode.Create))
            using (GZipStream zipStream = new GZipStream(fileStream, CompressionMode.Compress))
            {
                zipStream.Write(dataToCompress, 0, dataToCompress.Length);
            }
        }
        catch (Exception e)
        {
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}
'''}}

DATA["T210"] = {"outputs": {
"python": r'''
import io
import os


def inputStreamToString(inputStream):
    new_line = os.linesep
    reader = io.TextIOWrapper(inputStream)
    result = []
    flag = False
    for line in reader:
        result.append((new_line if flag else "") + line.rstrip("\r\n"))
        flag = True
    return "".join(result)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *inputStreamToString(FILE *inputStream) {
    const char *new_line = "\n";
    size_t cap = 256, len = 0;
    char *result = malloc(cap);
    char line[1024];
    int flag = 0;
    result[0] = '\0';
    while (fgets(line, sizeof line, inputStream) != NULL) {
        size_t n = strlen(line);
        while (len + n + strlen(new_line) + 2 > cap)
            result = realloc(result, cap *= 2);
        if (flag) {
            strcat(result, new_line);
            len += strlen(new_line);
        }
        if (n > 0 && line[n - 1] == '\n') line[--n] = '\0';
        strcat(result, line);
        len += n;
        flag = 1;
    }
    return result;
}
''',
"csharp": r'''
using System;
using System.IO;
using System.Text;

public class Reader
{
    public string InputStreamToString(Stream inputStream)
    {
        string newLine = Environment.NewLine;
        StringBuilder result = new StringBuilder();
        bool flag = false;
        using (StreamReader reader = new StreamReader(inputStream))
        {
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                result.Append(flag ? newLine : "").Append(line);
                flag = true;
            }
        }
        return result.ToString();
    }
}
'''}}

DATA["T251"] = {"outputs": {
"python": r'''
class ResultSet:
    def __init__(self, values):
        self.values = values

    def get_long(self, column):
        return self.values[column]


class Order:
    def __init__(self):
        self.id = None


class Customer:
    def __init__(self):
        self.orders = None

    def get_orders(self):
        return self.orders

    def set_orders(self, orders):
        self.orders = orders


def processRow(rs, map):
    id = rs.get_long("CUSTOMER_ID")
    customer = map.get(id)
    if customer is not None:
        orders_list = customer.get_orders()
        if orders_list is None:
            orders_list = []
            customer.set_orders(orders_list)
        order = Order()
        order.id = rs.get_long("ORDER_ID")
        orders_list.append(order)
''',
"c": r'''
#include <stdlib.h>

typedef struct Order { long id; } Order;
typedef struct Customer { long id; Order **orders; int orderCount; int orderCap; } Customer;
typedef struct { long customerId; long orderId; } Row;

static Customer **map = NULL;
static int mapSize = 0;

long rsGetLong(const Row *rs, const char *column) {
    if (column[0] == 'C') return rs->customerId;
    return rs->orderId;
}

Customer *mapGet(long id) {
    for (int i = 0; i < mapSize; i++)
        if (map[i]->id == id) return map[i];
    return NULL;
}

void processRow(const Row *rs) {
    long id = rsGetLong(rs, "CUSTOMER_ID");
    Customer *customer = mapGet(id);
    if (customer != NULL) {
        if (customer->orders == NULL) {
            customer->orderCap = 8;
            customer->orderCount = 0;
            customer->orders = malloc(sizeof(Order *) * customer->orderCap);
        }
        if (customer->orderCount == customer->orderCap) {
            customer->orderCap *= 2;
            customer->orders = realloc(customer->orders, sizeof(Order *) * customer->orderCap);
        }
        Order *order = malloc(sizeof(Order));
        order->id = rsGetLong(rs, "ORDER_ID");
        customer->orders[customer->orderCount++] = order;
    }
}
''',
"csharp": r'''
using System.Collections.Generic;

public class Order { public long Id; }

public class Customer { public List<Order> Orders; }

public class Row
{
    public Dictionary<string, long> Values = new Dictionary<string, long>();

    public long GetLong(string column) { return Values[column]; }
}

public static class RowProcessor
{
    public static void ProcessRow(Row rs, Dictionary<long, Customer> map)
    {
        long id = rs.GetLong("CUSTOMER_ID");
        Customer customer;
        if (map.TryGetValue(id, out customer))
        {
            if (customer.Orders == null)
            {
                customer.Orders = new List<Order>();
            }
            customer.Orders.Add(new Order { Id = rs.GetLong("ORDER_ID") });
        }
    }
}
'''}}

DATA["T270"] = {"outputs": {
"python": r'''
def is_permutation(a, b):
    if len(a) != len(b):
        return False
    b_chars = list(b)
    found = 0
    for each_a in a:
        for k, each_b in enumerate(b_chars):
            if each_a == each_b:
                found += 1
                b_chars[k] = '\uffff'
                break
    return found == len(a)
''',
"c": r'''
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

bool isPermutation(const char *a, const char *b) {
    size_t aLen = strlen(a), bLen = strlen(b);
    if (aLen != bLen) return false;
    char *bCopy = strdup(b);
    int found = 0;
    for (size_t i = 0; i < aLen; i++) {
        for (size_t k = 0; k < bLen; k++) {
            if (a[i] == bCopy[k]) {
                found++;
                bCopy[k] = '\xff';
                break;
            }
        }
    }
    free(bCopy);
    return found == (int)aLen;
}
''',
"csharp": r'''
public static class PermutationChecker
{
    public static bool IsPermutation(string a, string b)
    {
        if (a.Length != b.Length) return false;
        char[] bChars = b.ToCharArray();
        int found = 0;
        foreach (char eachA in a)
        {
            for (int k = 0; k < bChars.Length; k++)
            {
                if (eachA == bChars[k])
                {
                    found++;
                    bChars[k] = '\uffff';
                    break;
                }
            }
        }
        return found == a.Length;
    }
}
'''}}
