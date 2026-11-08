DATA_R1 = {
"R106ccba12f": '''public static IList ToAnonymousList(this IEnumerable enumerable) {
    var values = new List<object>();
    foreach (object item in enumerable) {
        values.Add(item);
    }
    if (values.Count == 0)
        throw new Exception("?? No elements??");
    var returnList = (IList)Activator.CreateInstance(typeof(List<>).MakeGenericType(values[0].GetType()));
    foreach (object item in values) {
        returnList.Add(item);
    }
    return returnList;
}''',
"R3968bf5162": '''public void run() {
    int i = 1;
    while (i < 50) {
        awaitState(3);
        synchronized (s) {
            System.out.println("t1 " + i);
            s.setState(1);
            i = i + 3;
            s.notifyAll();
        }
    }
}

private void awaitState(int target) {
    while (s.getState() != target) {
        synchronized (s) {
            try {
                s.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}''',
"R3d67d34140": '''public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    String[][] array = new String[7][];
    array[0] = new String[]{"continents", "Asia", "Europe", "Africa", "Australia", "South America", "North America"};
    array[1] = new String[]{"profession", "teacher", "doctor", "lawyer"};
    array[2] = new String[]{"brand", "apple", "samsung"};
    array[3] = new String[]{"name", "lisa", "peter", "sam", "jack"};
    array[4] = new String[]{"profession", "engineer", "Professor", "Dentist", "Driver"};
    array[5] = new String[]{"sex", "value", "male", "female"};
    array[6] = new String[]{"exp", "value", "1", "2", "3", "4"};
    int index = sc.nextInt();
    rotateToFront(array, index - 1);
    printRows(array);
}

private static void rotateToFront(String[][] array, int row) {
    String moved = array[row];
    for (int i = row; i < array.length - 1; i++) {
        array[i] = array[i + 1];
    }
    array[array.length - 1] = moved;
}

private static void printRows(String[][] array) {
    StringBuilder sb = new StringBuilder();
    for (String[] tempArray : array) {
        sb.setLength(0);
        for (String s : tempArray) {
            sb.append(s).append(' ');
        }
        System.out.println(sb.toString());
    }
}''',
"Rd41c27729f": '''import math


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % k for k in range(3, math.isqrt(n) + 1, 2))''',
"Refa2e73039": '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char line[128];
    int sum = 0;
    printf("enter numbers: ");
    scanf("%127[^\\n]", line);
    char *token = strtok(line, " ");
    while (token != NULL) {
        sum += atoi(token);
        token = strtok(NULL, " ");
    }
    printf("sum: %d\\n", sum);
    return 0;
}''',
"R0113c1db9b": '''def foo(thing=None, thing_seq=None):
    if thing_seq is not None:
        list(map(lambda _thing: foo(thing=_thing), thing_seq))
    if thing is not None:
        print("did foo with", thing)''',
"Rc5f95dbda1": '''private static void GetUserData(string userName, UserSession user) {
    using (Entities ctx = CommonSERT.GetContext()) {
        var result = ctx.datUserRoles
            .Where(ur => ur.AccountName.Equals(userName, StringComparison.CurrentCultureIgnoreCase))
            .Select(ur => new { ur.Active, ur.ID })
            .FirstOrDefault();
        user.UserID = result.ID;
        if (result != null)
            user.UserActive = result.Active;
    }
}''',
"Rf9eb0ff068": '''from itertools import combinations


def function(argument):
    max_arg = max(argument)
    argument.remove(max_arg)
    for length in range(len(argument), 0, -1):
        if any(sum(combo) == max_arg for combo in combinations(argument, length)):
            return "true"
    return "false"''',
"R1479812111": '''public void doWork() {
    int h = 0;
    do {
        Thread.Sleep(3000);
        h.Dump();
        h++;
    } while (h <= 0);
}''',
"R314ba9cd4a": '''#include <stdio.h>

int main(void) {
    int i, base;
    int word[32];
    unsigned long int number;
    const char *digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    printf("Enter the decimal number to be converted: ");
    scanf("%ld", &number);
    printf("\\nEnter the new base: ");
    scanf("%d", &base);
    i = wordCalculator(word, number, base);
    printf("The number is: ");
    while (i >= 0) {
        putchar(digits[word[i]]);
        i--;
    }
    printf("\\n");
    return 0;
}''',
"R7ca8e2a2eb": '''static boolean isImmutable(Object obj) {
    Class<?> objClass = obj.getClass();
    if (!Immutable.class.equals(objClass.getSuperclass())) {
        return false;
    }
    if (!Modifier.isFinal(objClass.getModifiers())) {
        return false;
    }
    return Arrays.stream(objClass.getDeclaredFields())
        .allMatch(f -> Modifier.isFinal(f.getModifiers()) && isValidFieldType(f.getType()));
}''',
"R8db01bf25f": '''def flatten(xs):
    return [leaf for x in xs for leaf in (flatten(x) if isinstance(x, list) else [x])]''',
"Re6ed6fb8d3": '''public static IEnumerable<T> TakeLast<T>(this IEnumerable<T> input, int count) {
    if (count <= 0)
        yield break;
    var inputList = input as IList<T>;
    if (inputList != null) {
        for (int i = Math.Max(0, inputList.Count - count); i < inputList.Count; i++) {
            yield return inputList[i];
        }
    } else {
        var queue = new Queue<T>();
        foreach (T item in input) {
            if (queue.Count == count)
                queue.Dequeue();
            queue.Enqueue(item);
        }
        while (queue.Count > 0) {
            yield return queue.Dequeue();
        }
    }
}'''
}
