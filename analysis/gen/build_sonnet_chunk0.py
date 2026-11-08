import json

T = {}
R = {}

T["T738"] = (r'''def is_prime(number):
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
    return True''', r'''#include <stdbool.h>

bool isPrime(int number) {
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; (i * i) <= number; i += 2) {
        if (number % i == 0) return false;
    }
    return true;
}''', r'''static bool IsPrime(int number)
{
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; (i * i) <= number; i += 2)
    {
        if (number % i == 0) return false;
    }
    return true;
}''')

T["T862"] = (r'''def transform(self, cell_old, cell_new):
    cell_new.set_cell_comment(cell_old.get_cell_comment())
    hash_value = hash(cell_old.get_cell_style())
    if hash_value not in self.style_map:
        self.transform_style(hash_value, cell_old.get_cell_style(), self.workbook_new.create_cell_style())
    cell_new.set_cell_style(self.style_map[hash_value])
    cell_type = cell_old.get_cell_type()
    if cell_type == Cell.CELL_TYPE_BLANK:
        pass
    elif cell_type == Cell.CELL_TYPE_BOOLEAN:
        cell_new.set_cell_value(cell_old.get_boolean_cell_value())
    elif cell_type == Cell.CELL_TYPE_ERROR:
        cell_new.set_cell_value(cell_old.get_error_cell_value())
    elif cell_type == Cell.CELL_TYPE_FORMULA:
        cell_new.set_cell_value(cell_old.get_cell_formula())
    elif cell_type == Cell.CELL_TYPE_NUMERIC:
        cell_new.set_cell_value(cell_old.get_numeric_cell_value())
    elif cell_type == Cell.CELL_TYPE_STRING:
        cell_new.set_cell_value(cell_old.get_string_cell_value())
    else:
        print("transform: Unbekannter Zellentyp " + str(cell_old.get_cell_type()))''', r'''static void transform_cell(Transformer *self, HSSFCell *cellOld, XSSFCell *cellNew) {
    xssf_cell_set_comment(cellNew, hssf_cell_get_comment(cellOld));
    int hash = hssf_style_hash(hssf_cell_get_style(cellOld));
    if (!style_map_contains(self->styleMap, hash)) {
        transform_style(self, hash, hssf_cell_get_style(cellOld), workbook_create_cell_style(self->workbookNew));
    }
    xssf_cell_set_style(cellNew, style_map_get(self->styleMap, hash));
    switch (hssf_cell_get_type(cellOld)) {
        case CELL_TYPE_BLANK:
            break;
        case CELL_TYPE_BOOLEAN:
            xssf_cell_set_boolean(cellNew, hssf_cell_get_boolean(cellOld));
            break;
        case CELL_TYPE_ERROR:
            xssf_cell_set_error(cellNew, hssf_cell_get_error(cellOld));
            break;
        case CELL_TYPE_FORMULA:
            xssf_cell_set_string(cellNew, hssf_cell_get_formula(cellOld));
            break;
        case CELL_TYPE_NUMERIC:
            xssf_cell_set_number(cellNew, hssf_cell_get_numeric(cellOld));
            break;
        case CELL_TYPE_STRING:
            xssf_cell_set_string(cellNew, hssf_cell_get_string(cellOld));
            break;
        default:
            printf("transform: Unbekannter Zellentyp %d\n", hssf_cell_get_type(cellOld));
    }
}''', r'''private void Transform(HSSFCell cellOld, XSSFCell cellNew)
{
    cellNew.SetCellComment(cellOld.GetCellComment());
    int hash = cellOld.GetCellStyle().GetHashCode();
    if (!this.styleMap.ContainsKey(hash))
    {
        this.Transform(hash, cellOld.GetCellStyle(), this.workbookNew.CreateCellStyle());
    }
    cellNew.SetCellStyle(this.styleMap[hash]);
    switch (cellOld.GetCellType())
    {
        case Cell.CELL_TYPE_BLANK:
            break;
        case Cell.CELL_TYPE_BOOLEAN:
            cellNew.SetCellValue(cellOld.GetBooleanCellValue());
            break;
        case Cell.CELL_TYPE_ERROR:
            cellNew.SetCellValue(cellOld.GetErrorCellValue());
            break;
        case Cell.CELL_TYPE_FORMULA:
            cellNew.SetCellValue(cellOld.GetCellFormula());
            break;
        case Cell.CELL_TYPE_NUMERIC:
            cellNew.SetCellValue(cellOld.GetNumericCellValue());
            break;
        case Cell.CELL_TYPE_STRING:
            cellNew.SetCellValue(cellOld.GetStringCellValue());
            break;
        default:
            Console.WriteLine("transform: Unbekannter Zellentyp " + cellOld.GetCellType());
            break;
    }
}''')

T["T203"] = (r'''import gzip
import io
import traceback


def main():
    data_to_compress = "This is the test data.".encode("iso-8859-1")
    try:
        byte_stream = io.BytesIO()
        try:
            zip_stream = gzip.GzipFile(fileobj=byte_stream, mode="wb")
            try:
                zip_stream.write(data_to_compress)
            finally:
                zip_stream.close()
        finally:
            compressed_data = byte_stream.getvalue()
            byte_stream.close()
        file_stream = open("C:/Users/UserName/Desktop/zip_file.gz", "wb")
        try:
            file_stream.write(compressed_data)
        finally:
            try:
                file_stream.close()
            except Exception:
                pass
    except Exception:
        traceback.print_exc()''', r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

int main(void) {
    const char *data = "This is the test data.";
    size_t data_len = strlen(data);
    z_stream zs;
    memset(&zs, 0, sizeof(zs));
    if (deflateInit2(&zs, Z_DEFAULT_COMPRESSION, Z_DEFLATED, 15 + 16, 8, Z_DEFAULT_STRATEGY) != Z_OK) {
        fprintf(stderr, "deflateInit2 failed\n");
        return 0;
    }
    uLong cap = deflateBound(&zs, (uLong) data_len) + 32;
    unsigned char *out = (unsigned char *) malloc(cap);
    if (out == NULL) {
        deflateEnd(&zs);
        return 0;
    }
    zs.next_in = (Bytef *) data;
    zs.avail_in = (uInt) data_len;
    zs.next_out = out;
    zs.avail_out = (uInt) cap;
    if (deflate(&zs, Z_FINISH) != Z_STREAM_END) {
        fprintf(stderr, "deflate failed\n");
        deflateEnd(&zs);
        free(out);
        return 0;
    }
    size_t compressed_len = zs.total_out;
    deflateEnd(&zs);
    FILE *fp = fopen("C:/Users/UserName/Desktop/zip_file.gz", "wb");
    if (fp == NULL) {
        perror("fopen");
        free(out);
        return 0;
    }
    fwrite(out, 1, compressed_len, fp);
    fclose(fp);
    free(out);
    return 0;
}''', r'''public static void Main(string[] args)
{
    byte[] dataToCompress = Encoding.GetEncoding("ISO-8859-1").GetBytes("This is the test data.");
    try
    {
        byte[] compressedData;
        MemoryStream byteStream = new MemoryStream(dataToCompress.Length);
        try
        {
            GZipStream zipStream = new GZipStream(byteStream, CompressionMode.Compress);
            try
            {
                zipStream.Write(dataToCompress, 0, dataToCompress.Length);
            }
            finally
            {
                zipStream.Close();
            }
        }
        finally
        {
            byteStream.Close();
        }
        compressedData = byteStream.ToArray();
        FileStream fileStream = new FileStream("C:/Users/UserName/Desktop/zip_file.gz", FileMode.Create);
        try
        {
            fileStream.Write(compressedData, 0, compressedData.Length);
        }
        finally
        {
            try
            {
                fileStream.Close();
            }
            catch (Exception)
            {
            }
        }
    }
    catch (Exception e)
    {
        Console.WriteLine(e);
    }
}''')

T["T210"] = (r'''import io
import os


def input_stream_to_string(input_stream):
    new_line = os.linesep
    reader = io.TextIOWrapper(input_stream, newline=None)
    result = []
    flag = False
    for line in reader:
        line = line.rstrip("\n")
        result.append(new_line if flag else "")
        result.append(line)
        flag = True
    return "".join(result)''', r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

static void append_text(char **buf, size_t *len, size_t *cap, const char *s, size_t n) {
    if (*len + n + 1 > *cap) {
        while (*len + n + 1 > *cap) *cap *= 2;
        *buf = (char *) realloc(*buf, *cap);
    }
    memcpy(*buf + *len, s, n);
    *len += n;
    (*buf)[*len] = '\0';
}

char *input_stream_to_string(FILE *input_stream) {
    const char *new_line = "\n";
    size_t cap = 128, len = 0;
    char *result = (char *) malloc(cap);
    result[0] = '\0';
    char *line = NULL;
    size_t line_cap = 0;
    ssize_t n;
    bool flag = false;
    while ((n = getline(&line, &line_cap, input_stream)) != -1) {
        if (n > 0 && line[n - 1] == '\n') n--;
        if (n > 0 && line[n - 1] == '\r') n--;
        if (flag) append_text(&result, &len, &cap, new_line, strlen(new_line));
        append_text(&result, &len, &cap, line, (size_t) n);
        flag = true;
    }
    free(line);
    return result;
}''', r'''public string InputStreamToString(Stream inputStream)
{
    string newLine = Environment.NewLine;
    StreamReader reader = new StreamReader(inputStream);
    StringBuilder result = new StringBuilder();
    string line;
    bool flag = false;
    while ((line = reader.ReadLine()) != null)
    {
        result.Append(flag ? newLine : "").Append(line);
        flag = true;
    }
    return result.ToString();
}''')

T["T251"] = (r'''def process_row(self, rs):
    id_ = rs.get_long("CUSTOMER_ID")
    customer = self.map.get(id_)
    if customer is not None:
        orders_list = customer.get_orders()
        if orders_list is None:
            orders_list = []
            customer.set_orders(orders_list)
        order = Order()
        order.set_id(rs.get_long("ORDER_ID"))
        orders_list.append(order)''', r'''void process_row(ResultSet *rs) {
    long id = result_set_get_long(rs, "CUSTOMER_ID");
    Customer *customer = customer_map_get(map, id);
    if (customer != NULL) {
        OrderList *orders_list = customer_get_orders(customer);
        if (orders_list == NULL) {
            orders_list = order_list_new();
            customer_set_orders(customer, orders_list);
        }
        Order *order = order_new();
        order_set_id(order, result_set_get_long(rs, "ORDER_ID"));
        order_list_add(orders_list, order);
    }
}''', r'''public void ProcessRow(IDataReader rs)
{
    long id = Convert.ToInt64(rs["CUSTOMER_ID"]);
    Customer customer;
    map.TryGetValue(id, out customer);
    if (customer != null)
    {
        List<Order> ordersList = customer.GetOrders();
        if (ordersList == null)
        {
            ordersList = new List<Order>();
            customer.SetOrders(ordersList);
        }
        Order order = new Order();
        order.SetId(Convert.ToInt64(rs["ORDER_ID"]));
        ordersList.Add(order);
    }
}''')

T["T270"] = (r'''def is_permutation(a, b):
    a_array = list(a)
    b_array = list(b)
    if len(a) != len(b):
        return False
    found = 0
    for i in range(len(a_array)):
        each_a = a_array[i]
        for k in range(len(b_array)):
            if each_a == b_array[k]:
                found += 1
                b_array[k] = "\uffff"
                break
    return found == len(a)''', r'''#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static bool isPermutation(const char *a, const char *b) {
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    if (len_a != len_b) {
        return false;
    }
    bool *used = (bool *) calloc(len_b + 1, sizeof(bool));
    size_t found = 0;
    for (size_t i = 0; i < len_a; i++) {
        char eachA = a[i];
        for (size_t k = 0; k < len_b; k++) {
            if (!used[k] && eachA == b[k]) {
                found++;
                used[k] = true;
                break;
            }
        }
    }
    free(used);
    return found == len_a;
}''', r'''private static bool IsPermutation(string a, string b)
{
    char[] aArray = a.ToCharArray();
    char[] bArray = b.ToCharArray();
    if (a.Length != b.Length)
    {
        return false;
    }
    int found = 0;
    for (int i = 0; i < aArray.Length; i++)
    {
        char eachA = aArray[i];
        for (int k = 0; k < bArray.Length; k++)
        {
            if (eachA == bArray[k])
            {
                found++;
                bArray[k] = '\uFFFF';
                break;
            }
        }
    }
    return found == a.Length;
}''')

T["T323"] = (r'''def get_name(self, value):
    negative = False
    if value.startswith("-"):
        negative = True
        value = value[1:]
    decimals = value.find(".")
    decimal_value = None
    if 0 <= decimals:
        decimal_value = value[decimals + 1:]
        value = value[:decimals]
    name = self.processor.get_name(value)
    if name == "":
        name = self.ZERO_TOKEN
    elif negative:
        name = self.MINUS + self.SEPARATOR + name
    if not (decimal_value is None or decimal_value == ""):
        name = (name + self.SEPARATOR + self.UNION_AND + self.SEPARATOR
                + self.processor.get_name(decimal_value) + self.SEPARATOR
                + self.SCALE.get_name(-len(decimal_value)))
    return name''', r'''#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static char *dup_n(const char *s, size_t n) {
    char *r = (char *) malloc(n + 1);
    memcpy(r, s, n);
    r[n] = '\0';
    return r;
}

static char *append_str(char *base, const char *add) {
    size_t a = strlen(base), b = strlen(add);
    base = (char *) realloc(base, a + b + 1);
    memcpy(base + a, add, b + 1);
    return base;
}

char *get_name(const char *value) {
    bool negative = false;
    if (value[0] == '-') {
        negative = true;
        value++;
    }
    const char *dot = strchr(value, '.');
    const char *decimal_value = NULL;
    char *integer_part;
    if (dot != NULL) {
        decimal_value = dot + 1;
        integer_part = dup_n(value, (size_t) (dot - value));
    } else {
        integer_part = dup_n(value, strlen(value));
    }
    char *name = processor_get_name(integer_part);
    free(integer_part);
    if (name[0] == '\0') {
        free(name);
        name = dup_n(ZERO_TOKEN, strlen(ZERO_TOKEN));
    } else if (negative) {
        char *tmp = dup_n(MINUS, strlen(MINUS));
        tmp = append_str(tmp, SEPARATOR);
        tmp = append_str(tmp, name);
        free(name);
        name = tmp;
    }
    if (!(decimal_value == NULL || decimal_value[0] == '\0')) {
        char *dec_name = processor_get_name(decimal_value);
        name = append_str(name, SEPARATOR);
        name = append_str(name, UNION_AND);
        name = append_str(name, SEPARATOR);
        name = append_str(name, dec_name);
        name = append_str(name, SEPARATOR);
        name = append_str(name, scale_get_name(-(int) strlen(decimal_value)));
        free(dec_name);
    }
    return name;
}''', r'''public string GetName(string value)
{
    bool negative = false;
    if (value.StartsWith("-"))
    {
        negative = true;
        value = value.Substring(1);
    }
    int decimals = value.IndexOf(".");
    string decimalValue = null;
    if (0 <= decimals)
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
    if (!(decimalValue == null || decimalValue.Length == 0))
    {
        name = name + SEPARATOR + UNION_AND + SEPARATOR + processor.GetName(decimalValue) + SEPARATOR + SCALE.GetName(-decimalValue.Length);
    }
    return name;
}''')

T["T120"] = (r'''def solution(X, A):
    hset = set()
    for i in range(len(A)):
        if A[i] <= X:
            hset.add(A[i])
        if len(hset) == X:
            return i
    return -1''', r'''#include <stdbool.h>
#include <stdlib.h>

int solution(int X, int *A, int n) {
    int *set = (int *) malloc((n > 0 ? n : 1) * sizeof(int));
    int size = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] <= X) {
            bool present = false;
            for (int j = 0; j < size; j++) {
                if (set[j] == A[i]) {
                    present = true;
                    break;
                }
            }
            if (!present) set[size++] = A[i];
        }
        if (size == X) {
            free(set);
            return i;
        }
    }
    free(set);
    return -1;
}''', r'''public int Solution(int X, int[] A)
{
    HashSet<int> hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++)
    {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}''')

T["T879"] = (r'''def transform(self, workbook_new, font_old):
    font_new = workbook_new.create_font()
    font_new.set_boldweight(font_old.get_boldweight())
    font_new.set_char_set(font_old.get_char_set())
    font_new.set_color(font_old.get_color())
    font_new.set_font_name(font_old.get_font_name())
    font_new.set_font_height(font_old.get_font_height())
    font_new.set_italic(font_old.get_italic())
    font_new.set_strikeout(font_old.get_strikeout())
    font_new.set_type_offset(font_old.get_type_offset())
    font_new.set_underline(font_old.get_underline())
    return font_new''', r'''static HSSFFont *transform_font(HSSFWorkbook *workbookNew, XSSFFont *fontOld) {
    HSSFFont *fontNew = workbook_create_font(workbookNew);
    hssf_font_set_boldweight(fontNew, xssf_font_get_boldweight(fontOld));
    hssf_font_set_char_set(fontNew, xssf_font_get_char_set(fontOld));
    hssf_font_set_color(fontNew, xssf_font_get_color(fontOld));
    hssf_font_set_font_name(fontNew, xssf_font_get_font_name(fontOld));
    hssf_font_set_font_height(fontNew, xssf_font_get_font_height(fontOld));
    hssf_font_set_italic(fontNew, xssf_font_get_italic(fontOld));
    hssf_font_set_strikeout(fontNew, xssf_font_get_strikeout(fontOld));
    hssf_font_set_type_offset(fontNew, xssf_font_get_type_offset(fontOld));
    hssf_font_set_underline(fontNew, xssf_font_get_underline(fontOld));
    return fontNew;
}''', r'''private HSSFFont Transform(HSSFWorkbook workbookNew, XSSFFont fontOld)
{
    HSSFFont fontNew = workbookNew.CreateFont();
    fontNew.Boldweight = fontOld.Boldweight;
    fontNew.CharSet = fontOld.CharSet;
    fontNew.Color = fontOld.Color;
    fontNew.FontName = fontOld.FontName;
    fontNew.FontHeight = fontOld.FontHeight;
    fontNew.IsItalic = fontOld.IsItalic;
    fontNew.IsStrikeout = fontOld.IsStrikeout;
    fontNew.TypeOffset = fontOld.TypeOffset;
    fontNew.Underline = fontOld.Underline;
    return fontNew;
}''')

T["T620"] = (r'''def zero_front(nums):
    if nums is None:
        return None
    zeros_pos = 0
    for i in range(len(nums)):
        if nums[i] == 0:
            nums[i] = nums[zeros_pos]
            nums[zeros_pos] = 0
            zeros_pos += 1
    return nums''', r'''#include <stddef.h>

int *zeroFront(int *nums, int length) {
    if (nums == NULL) {
        return NULL;
    }
    int zerosPos = 0;
    for (int i = 0; i < length; ++i) {
        if (nums[i] == 0) {
            nums[i] = nums[zerosPos];
            nums[zerosPos] = 0;
            ++zerosPos;
        }
    }
    return nums;
}''', r'''public int[] ZeroFront(int[] nums)
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
            nums[i] = nums[zerosPos];
            nums[zerosPos] = 0;
            ++zerosPos;
        }
    }
    return nums;
}''')

T["T664"] = (r'''import typing


def investigate(p, *type_args):
    c = typing.get_origin(p)
    b = c.__module__ + "." + c.__qualname__ + "<"
    local_args = list(typing.get_args(p))
    if type_args is not None and len(type_args) > 0:
        i = 0
        next_type_arg = 0
        for local in local_args:
            if typing.get_origin(local) is not None:
                b += str(typing.get_origin(local)) + "<"
                b += str(type_args[next_type_arg])
                next_type_arg += 1
                b += ">"
            elif isinstance(local, typing.TypeVar):
                local_args[next_type_arg] = type_args[next_type_arg]
                b += str(local_args[next_type_arg])
                next_type_arg += 1
            else:
                b += str(local)
            b += ", "
            i += 1
        if len(type_args) > 0:
            b = b[:-2]
        b += ">"
    else:
        args = "[" + ", ".join(str(a) for a in local_args) + "]"
        b += args[1:-1] + ">"
    print(b)
    investigate_class(c, *local_args)''', r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { KIND_CLASS, KIND_PARAMETERIZED, KIND_VARIABLE } TypeKind;

typedef struct TypeInfo {
    TypeKind kind;
    const char *name;
    struct TypeInfo *raw;
    struct TypeInfo **args;
    int nargs;
} TypeInfo;

typedef struct {
    char *data;
    size_t len;
    size_t cap;
} StrBuf;

static void sb_append(StrBuf *sb, const char *s) {
    size_t n = strlen(s);
    if (sb->len + n + 1 > sb->cap) {
        while (sb->len + n + 1 > sb->cap) sb->cap *= 2;
        sb->data = (char *) realloc(sb->data, sb->cap);
    }
    memcpy(sb->data + sb->len, s, n + 1);
    sb->len += n;
}

extern void investigate_class(TypeInfo *c, TypeInfo **args, int nargs);

static void investigate(TypeInfo *p, TypeInfo **typeArgs, int nTypeArgs) {
    TypeInfo *c = p->raw;
    StrBuf b = { (char *) malloc(64), 0, 64 };
    b.data[0] = '\0';
    sb_append(&b, c->name);
    sb_append(&b, "<");
    int nLocal = p->nargs;
    TypeInfo **localArgs = (TypeInfo **) malloc((nLocal > 0 ? nLocal : 1) * sizeof(TypeInfo *));
    for (int k = 0; k < nLocal; k++) localArgs[k] = p->args[k];
    if (typeArgs != NULL && nTypeArgs > 0) {
        int nextTypeArg = 0;
        for (int k = 0; k < nLocal; k++) {
            TypeInfo *local = localArgs[k];
            if (local->kind == KIND_PARAMETERIZED) {
                sb_append(&b, local->raw->name);
                sb_append(&b, "<");
                sb_append(&b, typeArgs[nextTypeArg++]->name);
                sb_append(&b, ">");
            } else if (local->kind == KIND_VARIABLE) {
                localArgs[nextTypeArg] = typeArgs[nextTypeArg];
                sb_append(&b, localArgs[nextTypeArg]->name);
                nextTypeArg++;
            } else {
                sb_append(&b, local->name);
            }
            sb_append(&b, ", ");
        }
        if (nTypeArgs > 0 && b.len >= 2) {
            b.len -= 2;
            b.data[b.len] = '\0';
        }
        sb_append(&b, ">");
    } else {
        for (int k = 0; k < nLocal; k++) {
            if (k > 0) sb_append(&b, ", ");
            sb_append(&b, localArgs[k]->name);
        }
        sb_append(&b, ">");
    }
    printf("%s\n", b.data);
    free(b.data);
    investigate_class(c, localArgs, nLocal);
    free(localArgs);
}''', r'''static void Investigate(Type p, params Type[] typeArgs)
{
    Type c = p.GetGenericTypeDefinition();
    StringBuilder b = new StringBuilder(c.FullName);
    b.Append('<');
    Type[] localArgs = p.GetGenericArguments();
    if (typeArgs != null && typeArgs.Length > 0)
    {
        int i = 0, nextTypeArg = 0;
        foreach (Type local in localArgs)
        {
            if (local.IsGenericType)
            {
                b.Append(local.GetGenericTypeDefinition()).Append('<');
                b.Append(typeArgs[nextTypeArg++]);
                b.Append('>');
            }
            else if (local.IsGenericParameter)
            {
                localArgs[nextTypeArg] = typeArgs[nextTypeArg];
                b.Append(localArgs[nextTypeArg]);
                nextTypeArg++;
            }
            else
            {
                b.Append(local.ToString());
            }
            b.Append(", ");
            i++;
        }
        if (typeArgs.Length > 0)
        {
            b.Remove(b.Length - 2, 2);
        }
        b.Append('>');
    }
    else
    {
        string args = "[" + string.Join(", ", localArgs.Select(t => t.ToString())) + "]";
        b.Append(args.Substring(1, args.Length - 2)).Append('>');
    }
    Console.WriteLine(b);
    InvestigateClass(c, localArgs);
}''')

T["T706"] = (r'''import random


def shuffle(text):
    characters = list(text)
    for i in range(len(characters)):
        random_index = int(random.random() * len(characters))
        temp = characters[i]
        characters[i] = characters[random_index]
        characters[random_index] = temp
    return "".join(characters)''', r'''#include <stdlib.h>
#include <string.h>

char *shuffle(const char *text) {
    size_t length = strlen(text);
    char *characters = (char *) malloc(length + 1);
    memcpy(characters, text, length + 1);
    for (size_t i = 0; i < length; i++) {
        size_t randomIndex = (size_t) (((double) rand() / ((double) RAND_MAX + 1.0)) * length);
        char temp = characters[i];
        characters[i] = characters[randomIndex];
        characters[randomIndex] = temp;
    }
    return characters;
}''', r'''private static readonly Random rng = new Random();

public static string Shuffle(string text)
{
    char[] characters = text.ToCharArray();
    for (int i = 0; i < characters.Length; i++)
    {
        int randomIndex = (int)(rng.NextDouble() * characters.Length);
        char temp = characters[i];
        characters[i] = characters[randomIndex];
        characters[randomIndex] = temp;
    }
    return new string(characters);
}''')

T["T92"] = (r'''def compress_bad(s):
    count_consecutive = 0
    compressed_string = ""
    for i in range(len(s)):
        count_consecutive += 1
        if len(s) == i + 1:
            compressed_string += "" + s[i] + str(count_consecutive)
            count_consecutive = 0
            break
        elif s[i] != s[i + 1]:
            compressed_string += "" + s[i] + str(count_consecutive)
            count_consecutive = 0
    return compressed_string''', r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *compressBad(const char *str) {
    size_t n = strlen(str);
    char *compressed = (char *) malloc(n * 12 + 1);
    size_t pos = 0;
    int countConsecutive = 0;
    compressed[0] = '\0';
    for (size_t i = 0; i < n; i++) {
        countConsecutive++;
        if (n == (i + 1)) {
            pos += sprintf(compressed + pos, "%c%d", str[i], countConsecutive);
            countConsecutive = 0;
            break;
        } else if (str[i] != str[i + 1]) {
            pos += sprintf(compressed + pos, "%c%d", str[i], countConsecutive);
            countConsecutive = 0;
        }
    }
    return compressed;
}''', r'''public static string CompressBad(string str)
{
    int countConsecutive = 0;
    StringBuilder compressedString = new StringBuilder();
    for (int i = 0; i < str.Length; i++)
    {
        countConsecutive++;
        if (str.Length == (i + 1))
        {
            compressedString.Append(str[i]).Append(countConsecutive);
            countConsecutive = 0;
            break;
        }
        else if (str[i] != str[i + 1])
        {
            compressedString.Append(str[i]).Append(countConsecutive);
            countConsecutive = 0;
        }
    }
    return compressedString.ToString();
}''')

T["T694"] = (r'''def main():
    data = {}
    data["foo"] = ["1", "2", "3"]
    data["bar"] = ["3", "2"]
    data["baz"] = ["5", "6", "7"]
    foo = Foo(data)
    for combination in foo.all_unique_combinations():
        print("[" + ", ".join(combination) + "]")''', r'''#include <stdio.h>

typedef struct {
    const char *key;
    const char **values;
    int count;
} Entry;

typedef struct {
    char **items;
    int length;
} Combination;

typedef struct Foo Foo;
extern Foo *foo_new(const Entry *entries, int n);
extern Combination *foo_all_unique_combinations(Foo *foo, int *out_count);

int main(void) {
    const char *foo_vals[] = {"1", "2", "3"};
    const char *bar_vals[] = {"3", "2"};
    const char *baz_vals[] = {"5", "6", "7"};
    Entry data[] = {
        {"foo", foo_vals, 3},
        {"bar", bar_vals, 2},
        {"baz", baz_vals, 3}
    };
    Foo *foo = foo_new(data, 3);
    int count = 0;
    Combination *combos = foo_all_unique_combinations(foo, &count);
    for (int i = 0; i < count; i++) {
        printf("[");
        for (int j = 0; j < combos[i].length; j++) {
            if (j > 0) printf(", ");
            printf("%s", combos[i].items[j]);
        }
        printf("]\n");
    }
    return 0;
}''', r'''public static void Main(string[] args)
{
    Dictionary<string, List<string>> data = new Dictionary<string, List<string>>();
    data["foo"] = new List<string>(new[] { "1", "2", "3" });
    data["bar"] = new List<string>(new[] { "3", "2" });
    data["baz"] = new List<string>(new[] { "5", "6", "7" });
    Foo foo = new Foo(data);
    foreach (string[] combination in foo.AllUniqueCombinations())
    {
        Console.WriteLine("[" + string.Join(", ", combination) + "]");
    }
}''')

T["T546"] = (r'''def join(objects, delimiter):
    if len(objects) == 0:
        return ""
    ret = [str(objects[0])]
    for i in range(1, len(objects)):
        ret.append(delimiter)
        ret.append(str(objects[i]))
    return "".join(ret)''', r'''#include <stdlib.h>
#include <string.h>

char *join(const char **objects, size_t count, const char *delimiter) {
    if (count == 0) {
        char *empty = (char *) malloc(1);
        empty[0] = '\0';
        return empty;
    }
    size_t capacityGuess = (count * strlen(objects[0])) + ((count - 1) * strlen(delimiter));
    size_t cap = capacityGuess + 1;
    char *ret = (char *) malloc(cap);
    size_t len = 0;
    ret[0] = '\0';
    for (size_t i = 0; i < count; i++) {
        const char *parts[2];
        parts[0] = (i == 0) ? "" : delimiter;
        parts[1] = objects[i];
        for (int p = 0; p < 2; p++) {
            size_t n = strlen(parts[p]);
            if (len + n + 1 > cap) {
                while (len + n + 1 > cap) cap *= 2;
                ret = (char *) realloc(ret, cap);
            }
            memcpy(ret + len, parts[p], n + 1);
            len += n;
        }
    }
    return ret;
}''', r'''public static string Join(object[] objects, string delimiter)
{
    if (objects.Length == 0)
    {
        return "";
    }
    int capacityGuess = (objects.Length * objects[0].ToString().Length) + ((objects.Length - 1) * delimiter.Length);
    StringBuilder ret = new StringBuilder(capacityGuess);
    ret.Append(objects[0]);
    for (int i = 1; i < objects.Length; i++)
    {
        ret.Append(delimiter);
        ret.Append(objects[i]);
    }
    return ret.ToString();
}''')

T["T567"] = (r'''import threading


def run(self):
    with self.lock:
        i = 3
        while i < 50:
            while self.s.get_state() != 2:
                with self.s.cond:
                    try:
                        self.s.cond.wait()
                    except InterruptedError:
                        import traceback
                        traceback.print_exc()
            with self.s.cond:
                if self.s.get_state() == 2:
                    print("t3 " + str(i))
                i = i + 3
                self.s.set_state(3)
                self.s.cond.notify_all()''', r'''#include <pthread.h>
#include <stdio.h>

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int state;
} Shared;

void *run(void *arg) {
    Shared *s = (Shared *) arg;
    int i = 3;
    while (i < 50) {
        pthread_mutex_lock(&s->mutex);
        while (s->state != 2) {
            pthread_cond_wait(&s->cond, &s->mutex);
        }
        if (s->state == 2) printf("t3 %d\n", i);
        i = i + 3;
        s->state = 3;
        pthread_cond_broadcast(&s->cond);
        pthread_mutex_unlock(&s->mutex);
    }
    return NULL;
}''', r'''public void Run()
{
    lock (this)
    {
        int i = 3;
        while (i < 50)
        {
            while (s.GetState() != 2)
            {
                lock (s)
                {
                    try
                    {
                        Monitor.Wait(s);
                    }
                    catch (ThreadInterruptedException e)
                    {
                        Console.WriteLine(e);
                    }
                }
            }
            lock (s)
            {
                if (s.GetState() == 2) Console.WriteLine("t3 " + i);
                i = i + 3;
                s.SetState(3);
                Monitor.PulseAll(s);
            }
        }
    }
}''')

T["T731"] = (r'''import math
import time


def paint_component(self, g):
    start = time.perf_counter_ns()
    super().paint_component(g)
    w = self.get_width()
    h = self.get_height()
    g.draw_image(self.background, 0, 0, self)
    theta = 2 * math.pi * self.index / 64
    self.index += 1
    g.set_color(Color.BLUE)
    self.rect.set_rect(int(math.sin(theta) * w / 3 + w // 2 - RADIUS),
                       int(math.cos(theta) * h / 3 + h // 2 - RADIUS),
                       2 * RADIUS, 2 * RADIUS)
    g.fill_oval(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
    g.set_color(Color.WHITE)
    if self.frame_count == FRAMES:
        self.average_time = self.total_time // FRAMES
        self.total_time = 0
        self.frame_count = 0
    else:
        self.total_time += time.perf_counter_ns() - start
        self.frame_count += 1
    s = "%5.3f" % (self.average_time / 1000000.0)
    g.draw_string(s, 5, 16)''', r'''#include <math.h>
#include <stdio.h>
#include <time.h>

static long long now_nanos(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long) ts.tv_sec * 1000000000LL + ts.tv_nsec;
}

void paint_component(Panel *self, Graphics *g) {
    long long start = now_nanos();
    panel_paint_base(self, g);
    int w = panel_get_width(self);
    int h = panel_get_height(self);
    gfx_draw_image(g, background, 0, 0, self);
    double theta = 2 * M_PI * index++ / 64;
    gfx_set_color(g, COLOR_BLUE);
    rect.x = (int) (sin(theta) * w / 3 + w / 2 - RADIUS);
    rect.y = (int) (cos(theta) * h / 3 + h / 2 - RADIUS);
    rect.width = 2 * RADIUS;
    rect.height = 2 * RADIUS;
    gfx_fill_oval(g, rect.x, rect.y, rect.width, rect.height);
    gfx_set_color(g, COLOR_WHITE);
    if (frameCount == FRAMES) {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    } else {
        totalTime += now_nanos() - start;
        frameCount++;
    }
    char s[32];
    snprintf(s, sizeof(s), "%5.3f", averageTime / 1000000.0);
    gfx_draw_string(g, s, 5, 16);
}''', r'''protected override void OnPaint(PaintEventArgs e)
{
    long start = NanoTime();
    base.OnPaint(e);
    Graphics g = e.Graphics;
    int w = this.Width;
    int h = this.Height;
    g.DrawImage(background, 0, 0);
    double theta = 2 * Math.PI * index++ / 64;
    rect = new Rectangle(
        (int)(Math.Sin(theta) * w / 3 + w / 2 - RADIUS),
        (int)(Math.Cos(theta) * h / 3 + h / 2 - RADIUS),
        2 * RADIUS, 2 * RADIUS);
    g.FillEllipse(Brushes.Blue, rect);
    if (frameCount == FRAMES)
    {
        averageTime = totalTime / FRAMES;
        totalTime = 0;
        frameCount = 0;
    }
    else
    {
        totalTime += NanoTime() - start;
        frameCount++;
    }
    string s = string.Format("{0,5:F3}", averageTime / 1000000d);
    g.DrawString(s, this.Font, Brushes.White, 5, 16);
}

private static long NanoTime()
{
    return (long)(Stopwatch.GetTimestamp() * (1000000000.0 / Stopwatch.Frequency));
}''')

T["T428"] = (r'''import traceback


def run(self):
    try:
        ret_value = self.pro.wait()
        self.println("Command exit with return value " + str(ret_value))
        self.out_stream.close()
        self.out_stream = None
    except InterruptedError:
        traceback.print_exc()
    except IOError:
        traceback.print_exc()''', r'''#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>

void run(void) {
    int status = 0;
    if (waitpid(pro_pid, &status, 0) < 0) {
        perror("waitpid");
        return;
    }
    int retValue = WIFEXITED(status) ? WEXITSTATUS(status) : -1;
    char message[64];
    snprintf(message, sizeof(message), "Command exit with return value %d", retValue);
    println(message);
    if (fclose(outStream) != 0) {
        perror("fclose");
        return;
    }
    outStream = NULL;
}''', r'''public void Run()
{
    try
    {
        pro.WaitForExit();
        int retValue = pro.ExitCode;
        Println("Command exit with return value " + retValue);
        outStream.Close();
        outStream = null;
    }
    catch (ThreadInterruptedException e)
    {
        Console.WriteLine(e);
    }
    catch (IOException e)
    {
        Console.WriteLine(e);
    }
}''')

T["T626"] = (r'''def remove_even(k, n):
    counter = 0
    for i in range(n):
        if k[i] > 0 and k[i] % 2 == 1:
            k[counter] = k[i]
            counter += 1
    for i in range(counter, n):
        k[i] = 0''', r'''static void removeEven(int *k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++)
        if (k[i] % 2 == 1) k[counter++] = k[i];
    for (int i = counter; i < n; i++) k[i] = 0;
}''', r'''private static void RemoveEven(int[] k, int n)
{
    int counter = 0;
    for (int i = 0; i < n; i++)
        if (k[i] % 2 == 1) k[counter++] = k[i];
    for (int i = counter; i < n; i++) k[i] = 0;
}''')

T["T813"] = (r'''def to_hex_string(data):
    hex_string = []
    for i in range(len(data)):
        hex_value = format(0xFF & data[i], "x")
        if len(hex_value) == 1:
            hex_string.append("0")
        hex_string.append(hex_value)
    return "".join(hex_string)''', r'''#include <stdio.h>
#include <stdlib.h>

char *toHexString(const unsigned char *bytes, size_t length) {
    char *hexString = (char *) malloc(length * 2 + 1);
    size_t pos = 0;
    for (size_t i = 0; i < length; i++) {
        int value = 0xFF & bytes[i];
        pos += sprintf(hexString + pos, "%02x", value);
    }
    hexString[pos] = '\0';
    return hexString;
}''', r'''public static string ToHexString(byte[] bytes)
{
    StringBuilder hexString = new StringBuilder();
    for (int i = 0; i < bytes.Length; i++)
    {
        string hex = (0xFF & bytes[i]).ToString("x");
        if (hex.Length == 1)
        {
            hexString.Append('0');
        }
        hexString.Append(hex);
    }
    return hexString.ToString();
}''')

T["T333"] = (r'''def get_name(self, value):
    buffer = []
    tens_found = False
    if len(value) > 3:
        number = int(value[-3:], 10)
    else:
        number = int(value, 10)
    number %= 100
    if number >= 20:
        buffer.append(self.TOKENS[(number // 10) - 2])
        number %= 10
        tens_found = True
    else:
        number %= 20
    if number != 0:
        if tens_found:
            buffer.append(self.UNION_SEPARATOR)
        buffer.append(self.unit_processor.get_name(number))
    return "".join(buffer)''', r'''#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *get_name(const char *value) {
    bool tensFound = false;
    size_t len = strlen(value);
    int number;
    if (len > 3) {
        number = (int) strtol(value + len - 3, NULL, 10);
    } else {
        number = (int) strtol(value, NULL, 10);
    }
    number %= 100;
    const char *tens = "";
    const char *separator = "";
    const char *unit = "";
    if (number >= 20) {
        tens = TOKENS[(number / 10) - 2];
        number %= 10;
        tensFound = true;
    } else {
        number %= 20;
    }
    if (number != 0) {
        if (tensFound) {
            separator = UNION_SEPARATOR;
        }
        unit = unit_processor_get_name(number);
    }
    size_t total = strlen(tens) + strlen(separator) + strlen(unit) + 1;
    char *buffer = (char *) malloc(total);
    snprintf(buffer, total, "%s%s%s", tens, separator, unit);
    return buffer;
}''', r'''public string GetName(string value)
{
    StringBuilder buffer = new StringBuilder();
    bool tensFound = false;
    int number;
    if (value.Length > 3)
    {
        number = int.Parse(value.Substring(value.Length - 3));
    }
    else
    {
        number = int.Parse(value);
    }
    number %= 100;
    if (number >= 20)
    {
        buffer.Append(TOKENS[(number / 10) - 2]);
        number %= 10;
        tensFound = true;
    }
    else
    {
        number %= 20;
    }
    if (number != 0)
    {
        if (tensFound)
        {
            buffer.Append(UNION_SEPARATOR);
        }
        buffer.Append(unitProcessor.GetName(number));
    }
    return buffer.ToString();
}''')

T["T807"] = (r'''def remove_duplicates(s):
    no_dupes = ""
    for i in range(len(s)):
        si = s[i:i + 1]
        if no_dupes.find(si) == -1:
            no_dupes += si
    return no_dupes''', r'''#include <stdlib.h>
#include <string.h>

static char *removeDuplicates(const char *s) {
    size_t n = strlen(s);
    char *noDupes = (char *) malloc(n + 1);
    size_t count = 0;
    for (size_t i = 0; i < n; i++) {
        int found = 0;
        for (size_t j = 0; j < count; j++) {
            if (noDupes[j] == s[i]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            noDupes[count++] = s[i];
        }
    }
    noDupes[count] = '\0';
    return noDupes;
}''', r'''static string RemoveDuplicates(string s)
{
    StringBuilder noDupes = new StringBuilder();
    for (int i = 0; i < s.Length; i++)
    {
        string si = s.Substring(i, 1);
        if (noDupes.ToString().IndexOf(si, StringComparison.Ordinal) == -1)
        {
            noDupes.Append(si);
        }
    }
    return noDupes.ToString();
}''')

T["T447"] = (r'''def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    arr1 = sorted(s1)
    arr2 = sorted(s2)
    sb1 = "".join(arr1)
    sb2 = "".join(arr2)
    print(sb1)
    print(sb2)
    if sb1 == sb2:
        return True
    else:
        return False''', r'''#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare_chars(const void *x, const void *y) {
    return (int) (unsigned char) *(const char *) x - (int) (unsigned char) *(const char *) y;
}

bool isAnagram(const char *s1, const char *s2) {
    size_t n = strlen(s1);
    if (n != strlen(s2)) return false;
    char *arr1 = (char *) malloc(n + 1);
    char *arr2 = (char *) malloc(n + 1);
    memcpy(arr1, s1, n + 1);
    memcpy(arr2, s2, n + 1);
    qsort(arr1, n, sizeof(char), compare_chars);
    qsort(arr2, n, sizeof(char), compare_chars);
    printf("%s\n", arr1);
    printf("%s\n", arr2);
    bool result = strcmp(arr1, arr2) == 0;
    free(arr1);
    free(arr2);
    return result;
}''', r'''public bool IsAnagram(string s1, string s2)
{
    StringBuilder sb1 = new StringBuilder();
    StringBuilder sb2 = new StringBuilder();
    if (s1.Length != s2.Length) return false;
    char[] arr1 = s1.ToCharArray();
    char[] arr2 = s2.ToCharArray();
    Array.Sort(arr1);
    Array.Sort(arr2);
    foreach (char c in arr1)
    {
        sb1.Append(c);
    }
    foreach (char c in arr2)
    {
        sb2.Append(c);
    }
    Console.WriteLine(sb1.ToString());
    Console.WriteLine(sb2.ToString());
    if (sb1.ToString().Equals(sb2.ToString())) return true;
    else return false;
}''')

T["T397"] = (r'''import os
import shutil
import traceback


def copy_folder(src, dest):
    try:
        entries = [src]
        for root, dirs, files in os.walk(src):
            for name in dirs + files:
                entries.append(os.path.join(root, name))
        for s in entries:
            try:
                d = os.path.join(dest, os.path.relpath(s, src))
                if os.path.normpath(d) == os.path.normpath(dest) and s == src:
                    d = dest
                if os.path.isdir(s):
                    if not os.path.exists(d):
                        os.mkdir(d)
                    continue
                if os.path.exists(d):
                    raise FileExistsError(d)
                shutil.copyfile(s, d)
            except Exception:
                traceback.print_exc()
    except Exception:
        traceback.print_exc()''', r'''#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

#define PATHBUF 4096

static void copy_one_file(const char *s, const char *d) {
    struct stat st;
    if (stat(d, &st) == 0) {
        fprintf(stderr, "File already exists: %s\n", d);
        return;
    }
    FILE *in = fopen(s, "rb");
    if (in == NULL) {
        perror(s);
        return;
    }
    FILE *out = fopen(d, "wb");
    if (out == NULL) {
        perror(d);
        fclose(in);
        return;
    }
    char buf[8192];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
        fwrite(buf, 1, n, out);
    }
    fclose(in);
    fclose(out);
}

static void visit(const char *root, const char *dest, const char *cur) {
    char d[PATHBUF];
    const char *rel = cur + strlen(root);
    while (*rel == '/') rel++;
    if (*rel == '\0') {
        snprintf(d, sizeof(d), "%s", dest);
    } else {
        snprintf(d, sizeof(d), "%s/%s", dest, rel);
    }
    struct stat st;
    if (stat(cur, &st) != 0) {
        perror(cur);
        return;
    }
    if (S_ISDIR(st.st_mode)) {
        struct stat dst;
        if (stat(d, &dst) != 0) {
            if (mkdir(d, 0777) != 0) perror(d);
        }
        DIR *dir = opendir(cur);
        if (dir == NULL) {
            perror(cur);
            return;
        }
        struct dirent *entry;
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;
            char child[PATHBUF];
            snprintf(child, sizeof(child), "%s/%s", cur, entry->d_name);
            visit(root, dest, child);
        }
        closedir(dir);
        return;
    }
    copy_one_file(cur, d);
}

void copyFolder(const char *src, const char *dest) {
    visit(src, dest, src);
}''', r'''public static void CopyFolder(string src, string dest)
{
    try
    {
        List<string> entries = new List<string> { src };
        entries.AddRange(Directory.EnumerateFileSystemEntries(src, "*", SearchOption.AllDirectories));
        foreach (string s in entries)
        {
            try
            {
                string relative = Path.GetRelativePath(src, s);
                string d = relative == "." ? dest : Path.Combine(dest, relative);
                if (Directory.Exists(s))
                {
                    if (!Directory.Exists(d)) Directory.CreateDirectory(d);
                    continue;
                }
                File.Copy(s, d);
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex);
    }
}''')

T["T430"] = (r'''import time


def run(self):
    try:
        self.runs = True
        if self.no_color < 2:
            self.no_color += 1
            self.change_btn_foreground(self.clr[self.no_color])
        else:
            self.no_color = 0
            self.change_btn_foreground(self.clr[self.no_color])
        steps = [
            (10, (0, 5, 10, 5)),
            (-10, (0, 0, 10, 10)),
            (10, (5, 10, 5, 0)),
            (-10, (10, 10, 0, 0)),
            (0, (5, 5, 5, 5)),
        ]
        m = self.init_margin
        for delta, border_sizes in steps:
            self.change_btn_margin(Insets(m.top, m.left + delta, m.bottom, m.right - delta))
            self.border = EmptyBorder(*border_sizes)
            self.change_pnl_border(self.border)
            time.sleep(0.1)
        self.count += 1
    except Exception as e:
        print(e)''', r'''#include <stdio.h>
#include <unistd.h>

void run(void) {
    static const int deltas[5] = {10, -10, 10, -10, 0};
    static const int borders[5][4] = {
        {0, 5, 10, 5},
        {0, 0, 10, 10},
        {5, 10, 5, 0},
        {10, 10, 0, 0},
        {5, 5, 5, 5}
    };
    runs = 1;
    if (noColor < 2) {
        noColor++;
        changeBtnForegroung(clr[noColor]);
    } else {
        noColor = 0;
        changeBtnForegroung(clr[noColor]);
    }
    for (int step = 0; step < 5; step++) {
        Insets margin = {initMargin.top, initMargin.left + deltas[step], initMargin.bottom, initMargin.right - deltas[step]};
        changeBtnMargin(margin);
        border = makeEmptyBorder(borders[step][0], borders[step][1], borders[step][2], borders[step][3]);
        changePnlBorder(border);
        usleep(100 * 1000);
    }
    count++;
}''', r'''public void Run()
{
    try
    {
        runs = true;
        if (noColor < 2)
        {
            noColor++;
            ChangeBtnForeground(clr[noColor]);
        }
        else
        {
            noColor = 0;
            ChangeBtnForeground(clr[noColor]);
        }
        int[] deltas = { 10, -10, 10, -10, 0 };
        int[][] borders =
        {
            new[] { 0, 5, 10, 5 },
            new[] { 0, 0, 10, 10 },
            new[] { 5, 10, 5, 0 },
            new[] { 10, 10, 0, 0 },
            new[] { 5, 5, 5, 5 }
        };
        for (int step = 0; step < deltas.Length; step++)
        {
            ChangeBtnMargin(new Padding(initMargin.Left + deltas[step], initMargin.Top, initMargin.Right - deltas[step], initMargin.Bottom));
            border = new Padding(borders[step][1], borders[step][0], borders[step][3], borders[step][2]);
            ChangePnlBorder(border);
            Thread.Sleep(100);
        }
        count++;
    }
    catch (Exception e)
    {
        Console.WriteLine(e);
    }
}''')

# ---------------- refactors ----------------

R["R3b3bb0bfa8"] = r'''int main () {
    thread_data tdata = { .a = 10, .b = 32 };
    pthread_t tid;
    int rc = pthread_create (& tid, NULL, myThread, (void *) & tdata);
    (void) rc;
    pthread_join (tid, NULL);
    printf ("%d + %d = %d\n", tdata.a, tdata.b, tdata.result);
    return 0;
}'''

R["R70b5cc83a3"] = r'''public void draw (Graphics2D g) {
    final float arrowRatio = 0.5f;
    final float arrowLength = 80.0f;
    final float endX = 350.0f;
    final float waisting = 0.5f;
    final float arrowWidth = arrowRatio * arrowLength;
    final float waistX = endX - arrowLength * 0.5f;
    final float waistY = arrowWidth * 0.5f * waisting;
    final float lineWidth = ((BasicStroke) g.getStroke ()).getLineWidth ();
    final float veeX = endX - lineWidth * 0.5f / arrowRatio;
    final float tailX = veeX - arrowLength;
    Path2D.Float path = new Path2D.Float ();
    path.moveTo (tailX, - arrowWidth);
    path.quadTo (waistX, - waistY, endX, 0.0f);
    path.quadTo (waistX, waistY, tailX, arrowWidth);
    path.lineTo (veeX - arrowLength * 0.75f, 0.0f);
    path.lineTo (tailX, - arrowWidth);
    g.setColor (Color.BLUE);
    g.fill (path);
    g.setColor (Color.RED);
    g.draw (new Line2D.Float (50.0f, 0.0f, veeX - arrowLength * 0.5f, 0.0f));
}'''

R["R9d7d058df5"] = r'''public static void MoveDown (this TreeNode node) {
    TreeNodeCollection siblings = null;
    if (node.Parent != null) {
        siblings = node.Parent.Nodes;
    } else if (node.TreeView != null && node.TreeView.Nodes.Contains (node)) {
        siblings = node.TreeView.Nodes;
    }
    if (siblings == null) {
        return;
    }
    int index = siblings.IndexOf (node);
    if (index >= siblings.Count - 1) {
        return;
    }
    siblings.RemoveAt (index);
    siblings.Insert (index + 1, node);
}'''

R["R59af819289"] = r'''def all_pairs(lst):
    count = len(lst)
    if count == 0:
        return [tuple()]
    if count <= 2:
        return [tuple(lst)]
    pad = False
    if count % 2 != 0:
        for candidate in (None, True):
            if candidate not in lst:
                lst.append(candidate)
                pad = candidate
                break
        else:
            code = True
            while chr(code) in lst:
                code += 1
            pad = chr(code)
            lst.append(pad)
    first = lst[0]
    result = []
    for idx in range(1, len(lst)):
        pair = (first, lst[idx])
        remaining = lst[1:idx] + lst[idx + 1 :]
        for rest in all_pairs(remaining):
            combo = [pair] + rest
            if pad is not False:
                for pos, tu in enumerate(combo):
                    if pad in tu:
                        combo[pos] = (tu[0],)
                        break
            result.append(combo)
    return result'''

R["Rf952aa3c99"] = r'''public int solution (int X, int [] A) {
    int target = X * (X + 1) / 2;
    int total = 0;
    Set < Integer > seen = new HashSet < Integer > ();
    for (int i = 0; i < A.length; i ++) {
        int v = A [i];
        if (v > X) {
            continue;
        }
        if (! seen.add (v)) {
            continue;
        }
        total += v;
        if (total == target) {
            return i;
        }
    }
    return - 1;
}'''

R["Rd199c3fba9"] = r'''def validate_ip(ip_str):
    if ip_str.endswith("\n"):
        ip_str = ip_str[:-1]
    parts = ip_str.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if len(part) == 0 or len(part) > 3:
            return False
        if any(ch not in "0123456789" for ch in part):
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False
    return True'''

R["Rce31c46bb8"] = r'''static int sumStep (int prod, int value) {
    int j = 1;
    while (j < value) {
        if (value % j == 0) {
            prod = prod * j;
        }
        j++;
    }
    return prod;
}

int main (void) {
    int numberOfInputs;
    int prod = 1;
    scanf ("%d", & numberOfInputs);
    for (int remaining = numberOfInputs; remaining > 0; remaining--) {
        int inputNumber;
        scanf ("%d", & inputNumber);
        prod = sumStep (prod, inputNumber);
        printf ("%04d\n", prod % 10000);
    }
    return 0;
}'''

R["R8655349b09"] = r'''public static void CountbyChar (String s) {
    HashMap < Character, Integer > letterCountMap = new HashMap < Character, Integer > ();
    for (char ch : s.toCharArray ()) {
        letterCountMap.merge (ch, 1, Integer :: sum);
    }
    for (Map.Entry < Character, Integer > entry : letterCountMap.entrySet ()) {
        System.out.println (entry.getValue () + "( for" + entry.getKey () + " )");
    }
}'''

R["R6ec2173375"] = r'''def treeToList(node, order = Order.INORDER) :
	if node is None :
		return []
	current = [node.data]
	right = treeToList(node.right, order)
	down = treeToList(node.down, order)
	if order == Order.PREORDER :
		sequence = (current, right, down)
	elif order == Order.INORDER :
		sequence = (right, current, down)
	elif order == Order.POSTORDER :
		sequence = (right, down, current)
	else :
		return None
	return sequence[0] + sequence[1] + sequence[2]'''

R["R998677b1ab"] = r'''int main (void) {
    FILE *fp = fopen (FILE_NAME, "r");
    if (fp == NULL) {
        perror ("fopen failed");
        exit (EXIT_FAILURE);
    }
    int count;
    for (count = 0; fgets (words[count], MAX_COLUMNS, fp) != NULL; count++) {
        size_t last = strlen (words[count]) - 1;
        words[count][last] = '\0';
    }
    bubbleSortWordsArray (count);
    printWordsArray (count);
    return 0;
}'''

R["Rbef72fa071"] = r'''public static int score (final String gene1, final String gene2) {
    return score (gene1.toCharArray (), gene2.toCharArray (), 0, 0);
}'''

R["Rc80ff5796f"] = r'''public static boolean twoDuplicates (int [] values) {
    int n = values.length;
    int i = 0;
    while (i < n) {
        int matches = 0;
        int z = n - 1;
        while (z > i) {
            if (values [z] == values [i] && ++ matches == 2) {
                return true;
            }
            z --;
        }
        i ++;
    }
    return false;
}'''

R["Re56d31c78d"] = r'''public static void Dispose(this MethodBuilder mb) {
    if (mb == null)
        return;
    const BindingFlags flags = BindingFlags.Instance | BindingFlags.NonPublic;
    FieldInfo Field(string name) => typeof (MethodBuilder).GetField(name, flags);
    FieldInfo ilGenField = Field("m_ilGenerator");
    FieldInfo moduleField = Field("m_module");
    FieldInfo containingTypeField = Field("m_containingType");
    FieldInfo localSigField = Field("m_localSignature");
    FieldInfo sigField = Field("m_signature");
    ((ModuleBuilder)moduleField.GetValue(mb)).Dispose();
    moduleField.SetValue(mb, null);
    containingTypeField.SetValue(mb, null);
    ((SignatureHelper)localSigField.GetValue(mb)).Dispose();
    localSigField.SetValue(mb, null);
    ((SignatureHelper)sigField.GetValue(mb)).Dispose();
    sigField.SetValue(mb, null);
    ((ILGenerator)ilGenField.GetValue(mb)).Dispose();
    ilGenField.SetValue(mb, null);
}'''

R["R876047a76c"] = r'''def is_prime(x) :
	return x >= 2 and all(x % n != 0 for n in range(2, x - 1))'''

R["R61361acd54"] = r'''public FileVisitResult visitFile (Path file, BasicFileAttributes attrs) throws IOException {
    FileVisitResult outcome = FileVisitResult.CONTINUE;
    System.out.printf ("%s%n", file);
    return outcome;
}'''

R["R8cedc05d13"] = r'''public int readNumber () {
    int x = - 1;
    do {
        System.out.println ("Please enter a positive number.");
        try {
            x = keyboard.nextInt ();
        } catch (java.util.InputMismatchException e) {
        }
    } while (x < 0);
    return x;
}'''

R["Re5e59b66ff"] = r'''def find_nth(string, substring, n) :
	if n < 1 :
		raise RecursionError("maximum recursion depth exceeded")
	position = string.find(substring)
	for _ in range(n - 1) :
		position = string.find(substring, position + 1)
	return position'''

R["R6073c71857"] = r'''static void reportReading (void) {
    temperature = bmp085_GetTemperature (bmp085_ReadUT ());
    pressure = bmp085_GetPressure (bmp085_ReadUP ());
    altitude = bmp085_Altitude (pressure);
    printf ("Temperature\t%0.1f *F\n", ((double) temperature) / 10 * 1.8 + 32);
    printf ("Pressure\t%0.2f hPa\n", ((double) pressure) / 100);
    printf ("Altitude\t%0.1f Feet\n", ((double) altitude) * 3.280839895);
}

int main (int argc, char **argv) {
    bmp085_Calibration ();
    int remaining = 49;
    while (remaining > 0) {
        reportReading ();
        sleep (1800);
        remaining--;
    }
    return 0;
}'''

R["R271e84529a"] = r'''int main (void) {
    unsigned int first, value;
    scanf ("%u", & first);
    scanf ("%u", & value);
    int output = 0;
    for (; value > 0; value /= 10) {
        if (value % 10 == value) {
            output++;
        }
    }
    printf ("%d", output);
    return 0;
}'''

R["Re0be2a9253"] = r'''def collatz(number) :
	if number % 2 == 0 :
		result = number // 2
	else :
		result = 3 * number + 1
	print(result)
	return result'''

R["R79546e7246"] = r'''int main () {
    int var1 = 1048575;
    int var2 = 1048575;
    char buffer [17];
    int len = sprintf (buffer, "%x%x", var1, var2);
    int padding = len < 16 ? 16 - len : 0;
    while (padding-- > 0) {
        putchar ('0');
    }
    printf ("%s\n", buffer);
    return 0;
}'''

R["R9936309be3"] = r'''public void mouseReleased (int mod, Point loc) {
    dragLocation = null;
    pressLocation = null;
}'''

R["R8caade20c5"] = r'''static void Main (string [] args) {
    string [] ahri = {"Academy", "Challenger", "Dynasty", "Foxfire", "Midnight", "Popstar"};
    string [] leeSin = {"Traditional", "Acolyte", "Dragon Fist", "Musy Thai", "Pool Party", "SKT T1", "Knockout"};
    Console.WriteLine ("Conor's Random League of Legends Skin Selector v0.1");
    Console.WriteLine (" ");
    Console.WriteLine (" ");
    Console.ForegroundColor = ConsoleColor.Gray;
    Console.WriteLine ("What champion would you like to select a skin for?..    ");
    string champion = Console.ReadLine ();
    Console.Write ("Press the 'enter' key for a random champion..     ");
    Console.ReadLine ();
    Random rnd = new Random ();
    string [] skins = champion == "ahri" ? ahri : leeSin;
    Console.WriteLine (skins [rnd.Next (skins.Length - 1)]);
}'''

R["Re2915c15ad"] = r'''def dashboard(request) :
	form = FilterForm()
	sightings = None
	if request.POST :
		form = FilterForm(request.POST)
		if form.is_valid() :
			sightings = Sighting.objects.filter(IMS_plant = form.cleaned_data ['selectedplant'])
	if sightings is None :
		sightings = Sighting.objects.all().order_by('date')
	context = {'sightings' : sightings, 'form' : form}
	return render_to_response('dashboard.html', context, context_instance = RequestContext(request))'''

R["Re8e5ba0337"] = r'''def get_info(session, title, url) :
	soup = BeautifulSoup(session.get(url).text, "lxml")
	lists = soup.select("ul.list-unstyled")
	for items in lists :
		tel = items.select_one("a[href^='tel:']")
		if tel is not None :
			phone = tel.text
			break
	else :
		if lists :
			phone = "N/A"
	print (title, phone)'''

seeds = json.load(open("C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/seeds/chunk0.json", encoding="utf-8"))
out = []
for it in seeds:
    if it["task"] == "translate":
        py, c, cs = T[it["id"]]
        out.append({"id": it["id"], "outputs": {"python": py, "c": c, "csharp": cs}})
    else:
        out.append({"id": it["id"], "output": R[it["id"]]})
with open("C:/Users/prakhar.sinha/Projects/Enhancing_Plagiarism_Detection_in_AI_Generated_Code__Dynamic_Multi_Modal_Semantic_Structural_Analysis__1_/repo/analysis/gen/out/sonnet_chunk0.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(out))
