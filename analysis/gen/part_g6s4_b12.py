DATA_B12 = {
"T60": {
"python": r"""
def is_permutation(str1, str2):
    x = sorted(str1)
    y = sorted(str2)
    if x == y:
        return True
    return False
""",
"c": r"""
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

static int char_cmp(const void *a, const void *b) {
    return *(const unsigned char *)a - *(const unsigned char *)b;
}

bool is_permutation(const char *str1, const char *str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    if (len1 != len2) return false;
    char *x = malloc(len1 + 1);
    char *y = malloc(len2 + 1);
    strcpy(x, str1);
    strcpy(y, str2);
    qsort(x, len1, sizeof(char), char_cmp);
    qsort(y, len2, sizeof(char), char_cmp);
    bool equal = memcmp(x, y, len1) == 0;
    free(x);
    free(y);
    return equal;
}
""",
"csharp": r"""
using System;
using System.Linq;

public static class PermutationCheck
{
    public static bool IsPermutation(string str1, string str2)
    {
        char[] x = str1.ToCharArray();
        char[] y = str2.ToCharArray();
        Array.Sort(x);
        Array.Sort(y);
        if (x.SequenceEqual(y)) return true;
        return false;
    }
}
"""
},
"T172": {
"python": r"""
import urllib.request

def is_available():
    url = urllib.request.Request("URL HERE", headers={"Connection": "close"})
    connection = urllib.request.urlopen(url, timeout=10)
    return connection.status == 200
""",
"c": r"""
#include <stdbool.h>

/* HTTP client approximated with extern stubs */
extern void *http_connect(const char *url, int timeout_ms);
extern int http_response_code(void *connection);

void is_available(void) {
    void *connection = http_connect("URL HERE", 10000);
    if (connection != NULL && http_response_code(connection) == 200) {
        return;
    }
}
""",
"csharp": r"""
using System;
using System.Net;

public class AvailabilityChecker
{
    public bool IsAvailable()
    {
        var url = new Uri("URL HERE");
        var connection = (HttpWebRequest)WebRequest.Create(url);
        connection.Headers.Add("Connection", "close");
        connection.Timeout = 10000;
        using (var response = (HttpWebResponse)connection.GetResponse())
        {
            if ((int)response.StatusCode == 200)
            {
                return true;
            }
            else return false;
        }
    }
}
"""
}
}
