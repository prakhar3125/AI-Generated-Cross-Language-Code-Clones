DATA4 = {}

DATA4["R8549838705"] = r"""
#include <stdio.h>

static void concat(const int *first, const int *second, int *out, int n) {
    int pos = 0;
    for (int k = 0; k < n; k++) {
        out[pos++] = first[k];
    }
    for (int k = 0; k < n; k++) {
        out[pos++] = second[k];
    }
}

int main(void) {
    const int array_a[3] = {2, 4, 6};
    const int array_b[3] = {1, 3, 5};
    int array_c[6];
    int i = 0;
    concat(array_a, array_b, array_c, 3);
    while (i < 6) {
        printf("array_c[%d]=%d\n", i, array_c[i]);
        i++;
    }
    return 0;
}
"""

DATA4["Reec8438c4b"] = r"""
#include <stdio.h>

static void print_char_with_spaces(int character, FILE *fout) {
    fputc(character, fout);
    if (character != '\n') {
        fputc(' ', fout);
    }
}

int main(void) {
    FILE *fin = fopen("in.txt", "r");
    FILE *fout = fopen("out.txt", "w");
    if (fin == NULL || fout == NULL) {
        printf("File error\n");
        return 1;
    }
    for (;;) {
        int character = fgetc(fin);
        if (character == EOF) {
            break;
        }
        print_char_with_spaces(character, fout);
    }
    fclose(fin);
    fclose(fout);
    printf("\nFile has been created...\n");
    return 0;
}
"""

DATA4["Rd776867156"] = r"""
public static void close(Statement... statements) {
    int i = statements.length - 1;
    while (i >= 0) {
        Statement stmt = statements[i];
        if (stmt == null) {
            i--;
            continue;
        }
        try {
            stmt.close();
        } catch (SQLException se) {
        }
        i--;
    }
}
"""

DATA4["Rb67c7892a4"] = r"""
public void run() {
    int remaining = 2;
    try {
        while (remaining-- > 0) {
            System.out.println("tic");
        }
    } catch (Exception e) {
        e.getStackTrace();
    }
}
"""

DATA4["R8818908361"] = r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    char months[] = "JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC";
    printf("months=[%s]\n\n", months);
    char *token = strtok(months, ",");
    while (token != NULL) {
        printf("month=[%s]\n", token);
        token = strtok(NULL, ",");
    }
    printf("\n");
    return 0;
}
"""

DATA4["Rd613be00ca"] = r"""
public static byte[] readBytes(InputStream inputStream) throws IOException {
    ByteArrayOutputStream out = new ByteArrayOutputStream();
    byte[] chunk = new byte[32 * 1024];
    int read;
    while ((read = inputStream.read(chunk)) != -1) {
        out.write(chunk, 0, read);
    }
    return out.toByteArray();
}
"""

DATA4["R84ca6c9dcf"] = r"""
public void actionPerformed(ActionEvent e) {
    boolean flashing = FLASH_COLOR.equals(label.getBackground());
    label.setBackground(flashing ? null : FLASH_COLOR);
    label.setForeground(flashing ? Color.black : Color.white);
}
"""

DATA4["Ra1d335a7d8"] = r"""
#include <stdio.h>
#include <string.h>

int main(void) {
    char str[] = "This is abc test abc string";
    const char *delim = "abc";
    char *cursor = str;
    while (1) {
        char *hit = strstr(cursor, delim);
        if (hit == NULL) {
            printf("%s\n", cursor);
            break;
        }
        *hit = '\0';
        printf("%s\n", cursor);
        cursor = hit + strlen(delim);
    }
    return 0;
}
"""

DATA4["R73286ffa0d"] = r"""
public static void main(String[] args) {
    CustomClassLoader loader = new CustomClassLoader();
    Class<?> c = null;
    Object o = null;
    try {
        c = loader.findClass("sample.Sample");
        o = c.newInstance();
    } catch (ClassNotFoundException | InstantiationException | IllegalAccessException e) {
        e.printStackTrace();
    }
}
"""

DATA4["Rf3a21bb32a"] = r"""
private static bool ShouldExpand(GridItem gridItem)
{
    if (gridItem.GridItemType != GridItemType.Property || !gridItem.Expandable)
    {
        return false;
    }
    object[] attrs = gridItem.Value.GetType()
        .GetCustomAttributes(typeof(PropertyGridInitialExpandedAttribute), false);
    return attrs.Length > 0 && ((PropertyGridInitialExpandedAttribute)attrs[0]).InitialExpanded;
}

private static void ExpandItemWithInitialExpandedAttribute(PropertyGrid propertyGrid, GridItem gridItem)
{
    if (gridItem == null)
    {
        return;
    }
    if (ShouldExpand(gridItem))
    {
        gridItem.Expanded = true;
    }
    foreach (GridItem childItem in gridItem.GridItems)
    {
        ExpandItemWithInitialExpandedAttribute(propertyGrid, childItem);
    }
}
"""

DATA4["R9955954078"] = r"""
public static List<List<T>> GetPermutations<T>(IEnumerable<IEnumerable<T>> lists)
{
    var result = new List<List<T>>();
    List<IEnumerator<T>> iterators = new List<IEnumerator<T>>();
    foreach (var list in lists)
    {
        var it = list.GetEnumerator();
        if (it.MoveNext())
        {
            iterators.Add(it);
        }
    }
    if (iterators.Count == 0)
    {
        return result;
    }
    bool done = false;
    while (!done)
    {
        var current = new List<T>();
        foreach (var it in iterators)
        {
            current.Add(it.Current);
        }
        result.Add(current);
        var mainIt = iterators.GetEnumerator();
        mainIt.MoveNext();
        bool recurse;
        do
        {
            recurse = false;
            var subIt = mainIt.Current;
            if (!subIt.MoveNext())
            {
                subIt.Reset();
                subIt.MoveNext();
                if (!mainIt.MoveNext())
                {
                    done = true;
                }
                else
                {
                    recurse = true;
                }
            }
        } while (recurse);
    }
    return result;
}
"""

DATA4["Rbcd6619d12"] = r"""
public static void main(String[] args) throws InterruptedException, ExecutionException {
    CompletableFuture<String> future = readPage();
    logThenFail(future);
}

private static void logThenFail(CompletableFuture<String> future) {
    future.thenAccept(page -> {
        System.out.println(page);
        throw new IllegalArgumentException("unexpected exception");
    }).exceptionally(e -> {
        e.printStackTrace(System.err);
        return null;
    });
}
"""

DATA4["R1ff2f32faf"] = r"""
def update(self, instance, validated_data):
    user_data = validated_data.pop("user", None)
    if user_data is not None:
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        instance.user = user_serializer.update(instance.user, user_data)
    instance = super().update(instance, validated_data)
    return instance
"""
