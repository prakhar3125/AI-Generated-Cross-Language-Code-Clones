DATA = {}

DATA["T738"] = {
    "python": """def is_prime(number):
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
    return True""",
    "c": """int isPrime(int number) {
    if (number < 2) return 0;
    if (number == 2) return 1;
    if (number % 2 == 0) return 0;
    int i = 3;
    while (i * i <= number) {
        if (number % i == 0) return 0;
        i += 2;
    }
    return 1;
}""",
    "csharp": """public static bool IsPrime(int number)
{
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; i * i <= number; i += 2)
    {
        if (number % i == 0) return false;
    }
    return true;
}""",
}

DATA["T862"] = {
    "python": """class Cell:
    CELL_TYPE_BLANK, CELL_TYPE_BOOLEAN, CELL_TYPE_ERROR = 0, 1, 2
    CELL_TYPE_FORMULA, CELL_TYPE_NUMERIC, CELL_TYPE_STRING = 3, 4, 5

class XSSFCell:
    def __init__(self):
        self.comment = None
        self.style = None
        self.value = None
        self.formula = None
    def setCellComment(self, c): self.comment = c
    def setCellStyle(self, s): self.style = s
    def setCellValue(self, v): self.value = v
    def setCellFormula(self, f): self.formula = f

class HSSFCell:
    def __init__(self, cell_type, comment=None, style=None, value=None, formula=None):
        self.cell_type = cell_type
        self.comment = comment
        self.style = style
        self.value = value
        self.formula = formula
    def getCellComment(self): return self.comment
    def getCellStyle(self): return self.style
    def getCellType(self): return self.cell_type
    def getBooleanCellValue(self): return self.value
    def getErrorCellValue(self): return self.value
    def getNumericCellValue(self): return self.value
    def getStringCellValue(self): return self.value
    def getCellFormula(self): return self.formula

class Workbook:
    def createCellStyle(self):
        return object()

class CellTransformer:
    def __init__(self):
        self.styleMap = {}
        self.workbookNew = Workbook()

    def transform(self, cellOld, cellNew):
        cellNew.setCellComment(cellOld.getCellComment())
        hashKey = hash(cellOld.getCellStyle())
        if hashKey not in self.styleMap:
            self.styleMap[hashKey] = cellOld.getCellStyle()
        cellNew.setCellStyle(self.styleMap[hashKey])
        t = cellOld.getCellType()
        if t == Cell.CELL_TYPE_BOOLEAN:
            cellNew.setCellValue(cellOld.getBooleanCellValue())
        elif t == Cell.CELL_TYPE_ERROR:
            cellNew.setCellValue(cellOld.getErrorCellValue())
        elif t == Cell.CELL_TYPE_FORMULA:
            cellNew.setCellFormula(cellOld.getCellFormula())
        elif t == Cell.CELL_TYPE_NUMERIC:
            cellNew.setCellValue(cellOld.getNumericCellValue())
        elif t == Cell.CELL_TYPE_STRING:
            cellNew.setCellValue(cellOld.getStringCellValue())
        else:
            print("transform: Unbekannter Zellentyp " + str(cellOld.getCellType()))""",
    "c": """typedef enum { CELL_BLANK, CELL_BOOLEAN, CELL_ERROR, CELL_FORMULA, CELL_NUMERIC, CELL_STRING } CellType;

typedef struct HSSFCell {
    CellType type;
    void *comment;
    void *style;
    int boolValue;
    int errorValue;
    double numValue;
    char *strValue;
    char *formula;
} HSSFCell;

typedef struct XSSFCell {
    void *comment;
    void *style;
    int boolValue;
    int errorValue;
    double numValue;
    char *strValue;
    char *formula;
} XSSFCell;

void transform(HSSFCell *cellOld, XSSFCell *cellNew, void **styleMap, int mapLen, void *newStyle) {
    cellNew->comment = cellOld->comment;
    long hashKey = (long)(size_t)cellOld->style;
    if (hashKey >= 0 && hashKey < mapLen && styleMap[hashKey] == NULL) {
        styleMap[hashKey] = newStyle;
    }
    cellNew->style = styleMap[hashKey];
    switch (cellOld->type) {
        case CELL_BOOLEAN: cellNew->boolValue = cellOld->boolValue; break;
        case CELL_ERROR: cellNew->errorValue = cellOld->errorValue; break;
        case CELL_FORMULA: cellNew->formula = cellOld->formula; break;
        case CELL_NUMERIC: cellNew->numValue = cellOld->numValue; break;
        case CELL_STRING: cellNew->strValue = cellOld->strValue; break;
        case CELL_BLANK:
        default:
            printf("transform: Unbekannter Zellentyp %d\\n", cellOld->type);
            break;
    }
}""",
    "csharp": """using System;
using System.Collections.Generic;

public class Cell
{
    public const int CELL_TYPE_BLANK = 0;
    public const int CELL_TYPE_BOOLEAN = 1;
    public const int CELL_TYPE_ERROR = 2;
    public const int CELL_TYPE_FORMULA = 3;
    public const int CELL_TYPE_NUMERIC = 4;
    public const int CELL_TYPE_STRING = 5;
}

public class HSSFCell
{
    public int CellType { get; set; }
    public object Comment { get; set; }
    public object Style { get; set; }
    public object Value { get; set; }
    public object Formula { get; set; }
}

public class XSSFCell
{
    public object Comment { get; set; }
    public object Style { get; set; }
    public object Value { get; set; }
    public object Formula { get; set; }
}

public class Workbook
{
    public object CreateCellStyle() { return new object(); }
}

public class CellTransformer
{
    private Dictionary<int, object> styleMap = new Dictionary<int, object>();
    private Workbook workbookNew = new Workbook();

    public void Transform(HSSFCell cellOld, XSSFCell cellNew)
    {
        cellNew.Comment = cellOld.Comment;
        int hashKey = cellOld.Style.GetHashCode();
        if (!styleMap.ContainsKey(hashKey))
        {
            styleMap[hashKey] = cellOld.Style;
        }
        cellNew.Style = styleMap[hashKey];
        switch (cellOld.CellType)
        {
            case Cell.CELL_TYPE_BOOLEAN:
                cellNew.Value = cellOld.Value;
                break;
            case Cell.CELL_TYPE_ERROR:
                cellNew.Value = cellOld.Value;
                break;
            case Cell.CELL_TYPE_FORMULA:
                cellNew.Formula = cellOld.Formula;
                break;
            case Cell.CELL_TYPE_NUMERIC:
                cellNew.Value = cellOld.Value;
                break;
            case Cell.CELL_TYPE_STRING:
                cellNew.Value = cellOld.Value;
                break;
            default:
                Console.WriteLine("transform: Unbekannter Zellentyp " + cellOld.CellType);
                break;
        }
    }
}""",
}

DATA["T203"] = {
    "python": """import gzip

def main():
    dataToCompress = "This is the test data.".encode("iso-8859-1")
    try:
        with open("C:/Users/UserName/Desktop/zip_file.gz", "wb") as f:
            with gzip.GzipFile(fileobj=f, mode="wb") as zipStream:
                zipStream.write(dataToCompress)
    except Exception as e:
        print(e)""",
    "c": """typedef struct {
    unsigned char *data;
    size_t len;
} Buffer;

extern void gzip_compress(const unsigned char *in, size_t inLen, Buffer *out);
extern int write_file(const char *path, const unsigned char *data, size_t len);

int main(void) {
    const unsigned char *dataToCompress = (const unsigned char *)"This is the test data.";
    Buffer compressedData;
    gzip_compress(dataToCompress, 22, &compressedData);
    if (write_file("C:/Users/UserName/Desktop/zip_file.gz", compressedData.data, compressedData.len) != 0) {
        perror("write failed");
        return 1;
    }
    return 0;
}""",
    "csharp": """using System;
using System.IO;
using System.IO.Compression;

public static void Main()
{
    byte[] dataToCompress = System.Text.Encoding.GetEncoding("ISO-8859-1").GetBytes("This is the test data.");
    try
    {
        using (FileStream fileStream = new FileStream("C:/Users/UserName/Desktop/zip_file.gz", FileMode.Create))
        using (GZipStream zipStream = new GZipStream(fileStream, CompressionMode.Compress))
        {
            zipStream.Write(dataToCompress, 0, dataToCompress.Length);
        }
    }
    catch (Exception e)
    {
        Console.WriteLine(e.StackTrace);
    }
}""",
}

DATA["T210"] = {
    "python": """import io

def inputStreamToString(inputStream):
    reader = io.TextIOWrapper(inputStream, encoding="utf-8")
    lines = []
    for line in reader:
        lines.append(line.rstrip("\\r\\n"))
    return "\\n".join(lines)""",
    "c": """char *inputStreamToString(FILE *inputStream) {
    size_t cap = 256, len = 0;
    char *result = malloc(cap);
    int ch;
    while ((ch = fgetc(inputStream)) != EOF) {
        if (len + 2 > cap) {
            cap *= 2;
            result = realloc(result, cap);
        }
        result[len++] = (char)ch;
    }
    result[len] = '\\0';
    return result;
}""",
    "csharp": """using System.Collections.Generic;
using System.IO;

public string InputStreamToString(Stream inputStream)
{
    using (StreamReader reader = new StreamReader(inputStream))
    {
        var lines = new List<string>();
        string line;
        while ((line = reader.ReadLine()) != null)
        {
            lines.Add(line);
        }
        return string.Join(Environment.NewLine, lines);
    }
}""",
}

DATA["T251"] = {
    "python": """class Order:
    def __init__(self):
        self.id = None

class Customer:
    def __init__(self):
        self.orders = None
    def getOrders(self):
        return self.orders
    def setOrders(self, orders):
        self.orders = orders

def processRow(rs, mapping):
    rowId = rs.getLong("CUSTOMER_ID")
    customer = mapping.get(rowId)
    if customer is not None:
        ordersList = customer.getOrders()
        if ordersList is None:
            ordersList = []
            customer.setOrders(ordersList)
        order = Order()
        order.id = rs.getLong("ORDER_ID")
        ordersList.append(order)""",
    "c": """typedef struct {
    long id;
} Order;

typedef struct {
    long id;
    Order *orders;
    int orderCount;
} Customer;

extern long rs_getLong(const char *col);

void processRow(Customer *map, int mapSize) {
    long rowId = rs_getLong("CUSTOMER_ID");
    Customer *customer = NULL;
    for (int i = 0; i < mapSize; i++) {
        if (map[i].id == rowId) {
            customer = &map[i];
            break;
        }
    }
    if (customer != NULL) {
        Order order;
        order.id = rs_getLong("ORDER_ID");
        customer->orders = realloc(customer->orders, (customer->orderCount + 1) * sizeof(Order));
        customer->orders[customer->orderCount++] = order;
    }
}""",
    "csharp": """using System.Collections.Generic;

public class Order { public long Id { get; set; } }

public class Customer { public List<Order> Orders { get; set; } }

public class ResultSet { public long GetLong(string col) { return 0; } }

public void ProcessRow(ResultSet rs, Dictionary<long, Customer> map)
{
    long id = rs.GetLong("CUSTOMER_ID");
    Customer customer;
    if (map.TryGetValue(id, out customer))
    {
        if (customer.Orders == null)
        {
            customer.Orders = new List<Order>();
        }
        Order order = new Order();
        order.Id = rs.GetLong("ORDER_ID");
        customer.Orders.Add(order);
    }
}""",
}

DATA["T270"] = {
    "python": """def is_permutation(a, b):
    if len(a) != len(b):
        return False
    bList = list(b)
    found = 0
    for eachA in a:
        for k in range(len(bList)):
            if eachA == bList[k]:
                found += 1
                bList[k] = '\\uffff'
                break
    return found == len(a)""",
    "c": """int isPermutation(const char *a, const char *b) {
    size_t lenA = strlen(a), lenB = strlen(b);
    if (lenA != lenB) return 0;
    char *bArray = strdup(b);
    int found = 0;
    for (size_t i = 0; i < lenA; i++) {
        for (size_t k = 0; k < lenB; k++) {
            if (a[i] == bArray[k]) {
                found++;
                bArray[k] = (char)0xFF;
                break;
            }
        }
    }
    free(bArray);
    return found == (int)lenA;
}""",
    "csharp": """private static bool IsPermutation(string a, string b)
{
    if (a.Length != b.Length) return false;
    char[] bArray = b.ToCharArray();
    int found = 0;
    foreach (char eachA in a)
    {
        for (int k = 0; k < bArray.Length; k++)
        {
            if (eachA == bArray[k])
            {
                found++;
                bArray[k] = '\\uffff';
                break;
            }
        }
    }
    return found == a.Length;
}""",
}
