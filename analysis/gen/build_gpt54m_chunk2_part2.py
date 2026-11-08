DATA_T2 = {
    "T186": {
        "python": r'''import re


class Score:
    def __init__(self, score_type, name, value):
        self.score_type = score_type
        self.name = name
        self.value = value


def main():
    input_text = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)"
    score_sets = re.split(r"\),", input_text)
    score_list = []
    for score in score_sets:
        score = score.strip()[1:]
        close_brace = score.find(")")
        if close_brace == len(score) - 1:
            score = score[:-1]
        tokens = score.split(",")
        score_list.append(Score(tokens[0], tokens[1], float(tokens[2])))''',
        "c": r'''#include <stdio.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    char type[8];
    char name[64];
    double value;
} Score;

int main(void) {
    const char *input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
    Score score_list[16];
    int count = 0;
    const char *cursor = input;
    char type[8], name[64];
    double value;
    while (count < 16 && sscanf(cursor, " (%7[^,],%63[^,],%lf)", type, name, &value) == 3) {
        snprintf(score_list[count].type, sizeof(score_list[count].type), "%s", type);
        snprintf(score_list[count].name, sizeof(score_list[count].name), "%s", name);
        score_list[count].value = value;
        count++;
        cursor = strchr(cursor, ')');
        if (cursor == NULL) break;
        cursor++;
    }
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class Score
{
    public string Type { get; }
    public string Name { get; }
    public double Value { get; }

    public Score(string type, string name, double value)
    {
        Type = type;
        Name = name;
        Value = value;
    }
}

public static class ScoreParser
{
    public static void Main(string[] args)
    {
        string input = "(A,Name1,200), (A,Name1,200), (R,Name1,200), (A,Name2,900), (A,Name2,500)";
        string[] scoreSets = Regex.Split(input, "\),");
        List<Score> scoreList = new List<Score>();
        foreach (string raw in scoreSets)
        {
            string score = raw.Trim().Substring(1);
            int closeBrace = score.IndexOf(')');
            if (closeBrace == score.Length - 1)
            {
                score = score.Substring(0, score.Length - 1);
            }
            string[] tokens = score.Split(',');
            scoreList.Add(new Score(tokens[0], tokens[1], double.Parse(tokens[2])));
        }
    }
}'''
    },
    "T271": {
        "python": r'''def main():
    array = []
    print("Enter n:")
    n = int(input())
    print("Enter m:")
    m = int(input())
    print("Enter the values:")
    for i in range(n):
        row = []
        array.append(row)
        for j in range(m):
            row.append(int(input()))
    print("Result:")
    print(array)''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, m;
    printf("Enter n:\n");
    if (scanf("%d", &n) != 1) return 1;
    printf("Enter m:\n");
    if (scanf("%d", &m) != 1) return 1;
    int **array = malloc((size_t)n * sizeof(int *));
    printf("Enter the values:\n");
    for (int i = 0; i < n; i++) {
        array[i] = malloc((size_t)m * sizeof(int));
        for (int j = 0; j < m; j++) {
            scanf("%d", &array[i][j]);
        }
    }
    printf("Result:\n");
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("[");
        for (int j = 0; j < m; j++) {
            printf("%d", array[i][j]);
            if (j + 1 < m) printf(", ");
        }
        printf("]");
        if (i + 1 < n) printf(", ");
    }
    printf("]\n");
    return 0;
}''',
        "csharp": r'''using System;
using System.Collections.Generic;
using System.Linq;

public static class MatrixReader
{
    public static void Main(string[] args)
    {
        var array = new List<List<int>>();
        Console.WriteLine("Enter n:");
        int n = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter m:");
        int m = int.Parse(Console.ReadLine());
        Console.WriteLine("Enter the values:");
        for (int i = 0; i < n; i++)
        {
            var list = new List<int>();
            array.Add(list);
            for (int j = 0; j < m; j++)
            {
                list.Add(int.Parse(Console.ReadLine()));
            }
        }
        Console.WriteLine("Result:");
        Console.WriteLine("[" + string.Join(", ", array.Select(r => "[" + string.Join(", ", r) + "]")) + "]");
    }
}'''
    },
    "T597": {
        "python": r'''class Product:
    def __init__(self, product_id=None):
        self.product_id = product_id


class ProductService:
    def get_product(self, product_id):
        return Product(product_id)


service = ProductService()


class HttpStatus:
    OK = 200
    BAD_REQUEST = 400


class ResponseEntity:
    def __init__(self, body, status):
        self.body = body
        self.status = status


class HttpServletRequest:
    def __init__(self, product_id):
        self.product_id = product_id


def match(request, response):
    try:
        p = service.get_product(request.product_id)
    except Exception:
        return ResponseEntity("Bad Request", HttpStatus.BAD_REQUEST)
    return ResponseEntity(p, HttpStatus.OK)''',
        "c": r'''#include <stdio.h>

typedef struct {
    int id;
    char name[64];
} Product;

typedef struct {
    int status;
    Product *body;
} ResponseEntity;

typedef struct {
    int product_id;
} HttpServletRequest;

extern Product *get_product(int product_id);

ResponseEntity match(HttpServletRequest *request) {
    Product *p = get_product(request->product_id);
    ResponseEntity response;
    if (p == NULL) {
        response.body = NULL;
        response.status = 400;
        return response;
    }
    response.body = p;
    response.status = 200;
    return response;
}''',
        "csharp": r'''using System;

public class Product { }

public class ProductService
{
    public Product GetProduct(int productId) => new Product();
}

public class HttpStatus
{
    public const int OK = 200;
    public const int BAD_REQUEST = 400;
}

public class ResponseEntity
{
    public object Body { get; }
    public int Status { get; }

    public ResponseEntity(object body, int status)
    {
        Body = body;
        Status = status;
    }
}

public class RequestData
{
    public int ProductId { get; set; }
}

public class MatchController
{
    private static readonly ProductService Service = new ProductService();

    public ResponseEntity Match(int matchId, string body, RequestData request)
    {
        Product p;
        try
        {
            p = Service.GetProduct(request.ProductId);
        }
        catch (Exception)
        {
            return new ResponseEntity("Bad Request", HttpStatus.BAD_REQUEST);
        }
        return new ResponseEntity(p, HttpStatus.OK);
    }
}'''
    }
}
