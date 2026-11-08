REFACTORS_B = {
    "Ra853448a33": r'''#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>

static void disable_echo_and_canonical(const struct termios *orig) {
    struct termios raw;
    memcpy(&raw, orig, sizeof(raw));
    raw.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(fileno(stdin), TCSANOW, &raw);
}

int main(void) {
    int counter = 0;
    struct termios orig_attr;
    tcgetattr(fileno(stdin), &orig_attr);
    disable_echo_and_canonical(&orig_attr);
    pthread_t pid;
    if (pthread_create(&pid, NULL, thread, &counter)) {
        fprintf(stderr, "Create thread failed");
        exit(1);
    }
    for (;;) {
        int c = getchar();
        __sync_add_and_fetch(&counter, 1);
        printf("add: %d\n", counter);
    }
    return 0;
}''',
    "R3713a963cf": r'''def json_scan(json_obj, key):
    result = None
    for element in json_obj:
        if str(element) == key:
            result = json_obj[element]
            continue
        child = json_obj[element]
        if type(child) == DictType:
            result = json_scan(child, key)
        elif type(child) == ListType:
            result = json_scan(element, key)
    return result''',
    "R4474610115": r'''#include <stdio.h>
#include <stdlib.h>

static int read_last(int first) {
    int value = first;
    while (scanf("%d", &value) == 1)
        ;
    return value;
}

int main(void) {
    int start;
    if (scanf("%d", &start) != 1)
        exit(1);
    int end = read_last(start);
    for (int i = start; i <= end; i++)
        printf("%d\n", i);
    return 0;
}''',
    "Refd906fcb2": r'''long pow (long a, int b) {
    if (b == 0) return 1;
    if (b == 1) return a;
    long half = pow (a * a, b / 2);
    return isEven (b) ? half : a * half;
}''',
    "Rd40ca7a94c": r'''public final void contextDestroyed (ServletContextEvent sce) {
    ClassLoader cl = Thread.currentThread ().getContextClassLoader ();
    java.util.ArrayList < Driver > list = java.util.Collections.list (DriverManager.getDrivers ());
    for (Driver driver : list) {
        if (driver.getClass ().getClassLoader () != cl) {
            log.trace ("Not deregistering JDBC driver {} as it does not belong to this webapp's ClassLoader", driver);
            continue;
        }
        try {
            log.info ("Deregistering JDBC driver {}", driver);
            DriverManager.deregisterDriver (driver);
        } catch (SQLException ex) {
            log.error ("Error deregistering JDBC driver {}", driver, ex);
        }
    }
}''',
    "Rfaf0b51ec8": r'''def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        candidate = tuple(pool[k] for k in indices)
        if not (1 in candidate and 3 in candidate):
            yield candidate''',
    "R3c52337f3a": r'''internal static string GetIPAddress (HttpRequestBase request) {
    string ip = ExtractForwardedIp (request.Headers ["Forwarded"]);
    if (ip != null) return ip;
    string xForwardedFor = request.Headers ["X-Forwarded-For"];
    if (! String.IsNullOrEmpty (xForwardedFor)) return xForwardedFor.Split (',') [0];
    return request.UserHostAddress;
}

private static string ExtractForwardedIp (string forwarded) {
    if (String.IsNullOrEmpty (forwarded)) return null;
    foreach (string segment in forwarded.Split (',') [0].Split (';')) {
        string [] pair = segment.Trim ().Split ('=');
        if (pair.Length == 2 && pair [0].Equals ("for", StringComparison.OrdinalIgnoreCase)) {
            return NormalizeForwardedIp (pair [1].Trim ('"'));
        }
    }
    return null;
}

private static string NormalizeForwardedIp (string ip) {
    int left = ip.IndexOf ('[');
    if (left == 0) {
        int right = ip.IndexOf (']');
        return ip.Substring (1, right - 1);
    }
    int colon = ip.IndexOf (':');
    return colon != - 1 ? ip.Substring (0, colon) : ip;
}''',
}
