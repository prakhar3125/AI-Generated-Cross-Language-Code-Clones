# -*- coding: utf-8 -*-
DATA1 = {
"T738": {
"python": r'''
def is_prime(number):
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
    return True
''',
"c": r'''
#include <stdbool.h>

bool is_prime(int number) {
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    for (int i = 3; i * i <= number; i += 2) {
        if (number % i == 0) return false;
    }
    return true;
}
''',
"csharp": r'''
public static bool IsPrime(int number) {
    if (number < 2) return false;
    if (number == 2) return true;
    if (number % 2 == 0) return false;
    int i = 3;
    while (i * i <= number) {
        if (number % i == 0) return false;
        i += 2;
    }
    return true;
}
'''
},
"T210": {
"python": r'''
import io
import os

def inputStreamToString(inputStream):
    reader = io.TextIOWrapper(inputStream, encoding="utf-8")
    lines = []
    for line in reader:
        lines.append(line.rstrip("\r\n"))
    return os.linesep.join(lines)
''',
"c": r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *input_stream_to_string(FILE *input_stream) {
    size_t cap = 256;
    size_t len = 0;
    char *result = malloc(cap);
    char line[1024];
    result[0] = '\0';
    while (fgets(line, sizeof(line), input_stream) != NULL) {
        size_t line_len = strlen(line);
        if (line_len > 0 && line[line_len - 1] == '\n') {
            line[--line_len] = '\0';
        }
        if (len + line_len + 2 > cap) {
            cap = (len + line_len + 2) * 2;
            result = realloc(result, cap);
        }
        if (len > 0) {
            result[len++] = '\n';
        }
        memcpy(result + len, line, line_len + 1);
        len += line_len;
    }
    return result;
}
''',
"csharp": r'''
using System;
using System.IO;
using System.Text;

public static string InputStreamToString(Stream inputStream) {
    string newLine = Environment.NewLine;
    StringBuilder result = new StringBuilder();
    using (StreamReader reader = new StreamReader(inputStream)) {
        string line;
        bool first = true;
        while ((line = reader.ReadLine()) != null) {
            if (!first) {
                result.Append(newLine);
            }
            result.Append(line);
            first = false;
        }
    }
    return result.ToString();
}
'''
},
"T251": {
"python": r'''
class Order:
    def __init__(self):
        self.id = None

    def setId(self, id_):
        self.id = id_


class Customer:
    def __init__(self):
        self.orders = None

    def getOrders(self):
        return self.orders

    def setOrders(self, orders):
        self.orders = orders


class ResultSet:
    def getLong(self, column):
        return self.values[column]


def processRow(rs, customerMap):
    id_ = rs.getLong("CUSTOMER_ID")
    customer = customerMap.get(id_)
    if customer is not None:
        ordersList = customer.getOrders()
        if ordersList is None:
            ordersList = []
            customer.setOrders(ordersList)
        order = Order()
        order.setId(rs.getLong("ORDER_ID"))
        ordersList.append(order)
''',
"c": r'''
#include <stdlib.h>
#include <string.h>

typedef struct Order {
    long id;
    struct Order *next;
} Order;

typedef struct {
    long id;
    Order *orders;
    int orderCount;
    int orderCapacity;
} Customer;

typedef struct {
    Customer **entries;
    int entryCount;
} CustomerMap;

typedef struct {
    const char *columns[16];
    long longValues[16];
    int columnCount;
} ResultSet;

extern Customer *find_customer(CustomerMap *map, long id);

long rs_get_long(ResultSet *rs, const char *column) {
    for (int i = 0; i < rs->columnCount; i++) {
        if (strcmp(rs->columns[i], column) == 0) {
            return rs->longValues[i];
        }
    }
    return -1L;
}

void processRow(ResultSet *rs, CustomerMap *map) {
    long id = rs_get_long(rs, "CUSTOMER_ID");
    Customer *customer = find_customer(map, id);
    if (customer != NULL) {
        if (customer->orders == NULL) {
            customer->orderCapacity = 4;
            customer->orderCount = 0;
            customer->orders = malloc(customer->orderCapacity * sizeof(Order *));
        }
        Order *order = malloc(sizeof(Order));
        order->id = rs_get_long(rs, "ORDER_ID");
        order->next = NULL;
        customer->orders[customer->orderCount++] = order;
    }
}
''',
"csharp": r'''
using System;
using System.Collections.Generic;

public class Order {
    public long Id { get; set; }
}

public class Customer {
    public List<Order> Orders { get; set; }
}

public class ResultSet {
    private Dictionary<string, long> longValues = new Dictionary<string, long>();

    public long GetLong(string column) {
        return longValues[column];
    }
}

public class RowProcessor {
    private Dictionary<long, Customer> map = new Dictionary<long, Customer>();

    public void ProcessRow(ResultSet rs) {
        long id = rs.GetLong("CUSTOMER_ID");
        Customer customer;
        map.TryGetValue(id, out customer);
        if (customer != null) {
            if (customer.Orders == null) {
                customer.Orders = new List<Order>();
            }
            Order order = new Order();
            order.Id = rs.GetLong("ORDER_ID");
            customer.Orders.Add(order);
        }
    }
}
'''
},
"T120": {
"python": r'''
def solution(X, A):
    seen = set()
    for i, value in enumerate(A):
        if value <= X:
            seen.add(value)
        if len(seen) == X:
            return i
    return -1
''',
"c": r'''
#include <stdlib.h>

int solution(int X, const int *A, int length) {
    char *seen = calloc(X + 1, sizeof(char));
    int distinct = 0;
    for (int i = 0; i < length; i++) {
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
}
''',
"csharp": r'''
using System.Collections.Generic;

public int Solution(int X, int[] A) {
    HashSet<int> hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++) {
        if (A[i] <= X) {
            hset.Add(A[i]);
        }
        if (hset.Count == X) {
            return i;
        }
    }
    return -1;
}
'''
},
"T620": {
"python": r'''
def zeroFront(nums):
    if nums is None:
        return None
    result = list(nums)
    zerosPos = 0
    for i in range(len(result)):
        if result[i] == 0:
            result[i], result[zerosPos] = result[zerosPos], 0
            zerosPos += 1
    return result
''',
"c": r'''
#include <stddef.h>

int *zero_front(int *nums, int length) {
    if (nums == NULL) {
        return NULL;
    }
    int zerosPos = 0;
    for (int i = 0; i < length; i++) {
        if (nums[i] == 0) {
            nums[i] = nums[zerosPos];
            nums[zerosPos] = 0;
            zerosPos++;
        }
    }
    return nums;
}
''',
"csharp": r'''
public int[] ZeroFront(int[] nums) {
    if (nums == null) {
        return null;
    }
    int[] result = new int[nums.Length];
    nums.CopyTo(result, 0);
    int zerosPos = 0;
    for (int i = 0; i < result.Length; i++) {
        if (result[i] == 0) {
            result[i] = result[zerosPos];
            result[zerosPos] = 0;
            zerosPos++;
        }
    }
    return result;
}
'''
},
"T626": {
"python": r'''
def removeEven(k, n):
    counter = 0
    for i in range(n):
        if k[i] % 2 == 1:
            k[counter] = k[i]
            counter += 1
    for i in range(counter, n):
        k[i] = 0
''',
"c": r'''
void remove_even(int *k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 == 1) {
            k[counter++] = k[i];
        }
    }
    for (int i = counter; i < n; i++) {
        k[i] = 0;
    }
}
''',
"csharp": r'''
public static void RemoveEven(int[] k, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++) {
        if (k[i] % 2 == 1) {
            k[counter] = k[i];
            counter++;
        }
    }
    while (counter < n) {
        k[counter] = 0;
        counter++;
    }
}
'''
},
"T813": {
"python": r'''
def toHexString(data):
    return "".join(format(byte & 0xFF, "02x") for byte in data)
''',
"c": r'''
#include <stdio.h>

void to_hex_string(const unsigned char *bytes, int length, char *out) {
    for (int i = 0; i < length; i++) {
        sprintf(out + (i * 2), "%02x", bytes[i] & 0xFF);
    }
    out[length * 2] = '\0';
}
''',
"csharp": r'''
using System.Text;

public static string ToHexString(byte[] bytes) {
    StringBuilder hexString = new StringBuilder(bytes.Length * 2);
    foreach (byte b in bytes) {
        hexString.Append((b & 0xFF).ToString("x2"));
    }
    return hexString.ToString();
}
'''
}
}
