DATA2 = {
    "T251": {"outputs": {
        "python": '''class Customer:
    def __init__(self):
        self.orders = None

    def get_orders(self):
        return self.orders

    def set_orders(self, orders):
        self.orders = orders


class Order:
    def __init__(self):
        self.id = None

    def set_id(self, id_):
        self.id = id_


def process_row(rs, map_):
    id_ = rs.get_long("CUSTOMER_ID")
    customer = map_.get(id_)
    if customer is not None:
        orders_list = customer.get_orders()
        if orders_list is None:
            orders_list = []
            customer.set_orders(orders_list)
        order = Order()
        order.set_id(rs.get_long("ORDER_ID"))
        orders_list.append(order)''',
        "c": r'''#include <stdlib.h>

typedef struct order { long id; } Order;

typedef struct order_list {
    Order *items;
    int count;
    int capacity;
} OrderList;

typedef struct customer { OrderList *orders; } Customer;

typedef struct result_set {
    long (*get_long)(struct result_set *, const char *);
} ResultSet;

#define MAP_SIZE 1024
static Customer *map[MAP_SIZE];

void process_row(ResultSet *rs) {
    long id = rs->get_long(rs, "CUSTOMER_ID");
    Customer *customer = map[id % MAP_SIZE];
    if (customer != NULL) {
        if (customer->orders == NULL) {
            customer->orders = calloc(1, sizeof(OrderList));
        }
        OrderList *orders_list = customer->orders;
        if (orders_list->count == orders_list->capacity) {
            orders_list->capacity = orders_list->capacity == 0 ? 4 : orders_list->capacity * 2;
            orders_list->items = realloc(orders_list->items, orders_list->capacity * sizeof(Order));
        }
        Order order;
        order.id = rs->get_long(rs, "ORDER_ID");
        orders_list->items[orders_list->count++] = order;
    }
}''',
        "csharp": '''using System.Collections.Generic;

public class Customer
{
    public List<Order> Orders { get; set; }
}

public class Order
{
    public long Id { get; set; }
}

public class RowProcessor
{
    private readonly Dictionary<long, Customer> map = new Dictionary<long, Customer>();

    public void ProcessRow(ResultSet rs)
    {
        long id = rs.GetLong("CUSTOMER_ID");
        map.TryGetValue(id, out Customer customer);
        if (customer != null)
        {
            if (customer.Orders == null)
            {
                customer.Orders = new List<Order>();
            }
            Order order = new Order();
            order.Id = rs.GetLong("ORDER_ID");
            customer.Orders.Add(order);
        }
    }
}

public abstract class ResultSet
{
    public abstract long GetLong(string column);
}'''
    }},
    "T270": {"outputs": {
        "python": '''def is_permutation(a, b):
    if len(a) != len(b):
        return False
    b_chars = list(b)
    found = 0
    for each_a in a:
        for k, each_b in enumerate(b_chars):
            if each_a == each_b:
                found += 1
                b_chars[k] = "\\uffff"
                break
    return found == len(a)''',
        "c": r'''#include <string.h>
#include <stdbool.h>

static bool is_permutation(const char *a, const char *b) {
    size_t len_a = strlen(a);
    if (len_a != strlen(b)) {
        return false;
    }
    char b_array[len_a + 1];
    strcpy(b_array, b);
    int found = 0;
    for (size_t i = 0; i < len_a; i++) {
        for (size_t k = 0; k < len_a; k++) {
            if (a[i] == b_array[k]) {
                found++;
                b_array[k] = (char) 0xFF;
                break;
            }
        }
    }
    return found == (int) len_a;
}''',
        "csharp": '''public static class PermutationChecker
{
    public static bool IsPermutation(string a, string b)
    {
        if (a.Length != b.Length)
        {
            return false;
        }
        char[] bArray = b.ToCharArray();
        int found = 0;
        foreach (char eachA in a)
        {
            for (int k = 0; k < bArray.Length; k++)
            {
                if (eachA == bArray[k])
                {
                    found++;
                    bArray[k] = '\\uFFFF';
                    break;
                }
            }
        }
        return found == a.Length;
    }
}'''
    }},
    "T323": {"outputs": {
        "python": '''class ScaleNamer:
    def get_name(self, value):
        raise NotImplementedError


ZERO_TOKEN = "zero"
MINUS = "minus"
SEPARATOR = " "
UNION_AND = "and"


class NumberNamer:
    def __init__(self, processor, scale):
        self.processor = processor
        self.scale = scale

    def get_name(self, value):
        negative = value.startswith("-")
        if negative:
            value = value[1:]
        decimals = value.find(".")
        decimal_value = None
        if decimals >= 0:
            decimal_value = value[decimals + 1:]
            value = value[:decimals]
        name = self.processor.get_name(value)
        if not name:
            name = ZERO_TOKEN
        elif negative:
            name = MINUS + SEPARATOR + name
        if decimal_value:
            name = (name + SEPARATOR + UNION_AND + SEPARATOR
                    + self.processor.get_name(decimal_value) + SEPARATOR
                    + self.scale.get_name(-len(decimal_value)))
        return name''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern const char *processor_get_name(const char *value);

#define ZERO_TOKEN "zero"
#define MINUS "minus"
#define SEPARATOR " "
#define UNION_AND " and "

char *get_name(const char *value) {
    char negative = 0;
    if (value[0] == '-') {
        negative = 1;
        value++;
    }
    const char *dot = strchr(value, '.');
    char *int_part = NULL;
    const char *decimal_part = NULL;
    if (dot != NULL) {
        size_t int_len = (size_t) (dot - value);
        int_part = malloc(int_len + 1);
        memcpy(int_part, value, int_len);
        int_part[int_len] = '\0';
        decimal_part = dot + 1;
        value = int_part;
    }
    const char *base = processor_get_name(value);
    char name[512];
    if (base[0] == '\0') {
        strcpy(name, ZERO_TOKEN);
    } else if (negative) {
        snprintf(name, sizeof(name), "%s%s%s", MINUS, SEPARATOR, base);
    } else {
        strcpy(name, base);
    }
    if (decimal_part != NULL && decimal_part[0] != '\0') {
        char tail[512];
        snprintf(tail, sizeof(tail), "%s%s%s%s", name, SEPARATOR, UNION_AND, processor_get_name(decimal_part));
        strcpy(name, tail);
    }
    free(int_part);
    return strdup(name);
}''',
        "csharp": '''public class NameFormatter
{
    private const string ZeroToken = "zero";
    private const string Minus = "minus";
    private const string Separator = " ";
    private const string UnionAnd = "and";

    private readonly IProcessor processor;
    private readonly IProcessor scale;

    public NameFormatter(IProcessor processor, IProcessor scale)
    {
        this.processor = processor;
        this.scale = scale;
    }

    public string GetName(string value)
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
        string name = processor.GetName(value);
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
            name = name + Separator + UnionAnd + Separator + processor.GetName(decimalValue)
                   + Separator + scale.GetName((-decimalValue.Length).ToString());
        }
        return name;
    }
}

public interface IProcessor
{
    string GetName(string value);
}'''
    }},
    "T120": {"outputs": {
        "python": '''def solution(x, a):
    seen = set()
    for i, value in enumerate(a):
        if value <= x:
            seen.add(value)
        if len(seen) == x:
            return i
    return -1''',
        "c": r'''#include <stdbool.h>
#include <stdlib.h>

static int solution(int x, const int *a, int length) {
    char *seen = calloc(x + 1, sizeof(char));
    int distinct = 0;
    for (int i = 0; i < length; i++) {
        if (a[i] <= x && !seen[a[i]]) {
            seen[a[i]] = 1;
            distinct++;
        }
        if (distinct == x) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}''',
        "csharp": '''using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int x, int[] a)
    {
        var seen = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            if (a[i] <= x)
            {
                seen.Add(a[i]);
            }
            if (seen.Count == x)
            {
                return i;
            }
        }
        return -1;
    }
}'''
    }},
}
