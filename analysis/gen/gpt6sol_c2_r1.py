DATA_R1 = {}

DATA_R1["R8549838705"] = r'''#include <stdio.h>

static void concat (const int *a, const int *b, int *out, int n) {
    int pos = 0;
    for (int k = 0; k < n; k ++) out [pos ++] = a [k];
    for (int k = 0; k < n; k ++) out [pos ++] = b [k];
}

static void printArray (const int *arr, int len) {
    int i = 0;
    while (i < len) {
        printf ("array_c[%d]=%d\n", i, arr [i]);
        i ++;
    }
}

int main () {
    const int array_a [3] = {2, 4, 6}, array_b [3] = {1, 3, 5};
    int array_c [6];
    concat (array_a, array_b, array_c, 3);
    printArray (array_c, 6);
    return 0;
}'''

DATA_R1["Reec8438c4b"] = r'''#include <stdio.h>

extern void printCharWithSpaces (int character, FILE *fin, FILE *fout);

static int processFiles (void) {
    FILE *fin = fopen ("in.txt", "r");
    FILE *fout = fopen ("out.txt", "w");
    if (fin == NULL || fout == NULL) {
        if (fin != NULL) fclose (fin);
        if (fout != NULL) fclose (fout);
        return 1;
    }
    int character;
    do {
        character = fgetc (fin);
        if (character == EOF) break;
        printCharWithSpaces (character, fin, fout);
    } while (character != EOF);
    fclose (fin);
    fclose (fout);
    return 0;
}

int main () {
    processFiles ();
    printf ("\nFile has been created...\n");
    return 0;
}'''

DATA_R1["Rd776867156"] = r'''public static void close (Statement...statements) {
    int i = 0;
    while (i < statements.length) {
        Statement stmt = statements [i];
        try {
            if (stmt == null) {
                i ++;
                continue;
            }
            stmt.close ();
        } catch (SQLException se) {
        }
        i ++;
    }
}'''

DATA_R1["Rb67c7892a4"] = r'''public void run () {
    try {
        printTic ();
        printTic ();
    } catch (Exception e) {
        e.getStackTrace ();
    }
}

private void printTic () {
    System.out.println ("tic");
}'''

DATA_R1["R8818908361"] = r'''#include <stdio.h>
#include <stdlib.h>

extern char **str_split (char *str, const char delimiter);

static void printAndFreeTokens (char **tokens) {
    if (tokens == NULL) return;
    int i = 0;
    while (* (tokens + i)) {
        printf ("month=[%s]\n", * (tokens + i));
        free (* (tokens + i));
        i ++;
    }
    printf ("\n");
    free (tokens);
}

int main () {
    char months [] = "JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC";
    printf ("months=[%s]\n\n", months);
    char **tokens = str_split (months, ',');
    if (tokens == NULL) {
        return 0;
    }
    printAndFreeTokens (tokens);
    return 0;
}'''

DATA_R1["Rd613be00ca"] = r'''public static byte [] readBytes (InputStream inputStream) throws IOException {
    byte [] buffer = new byte [32 * 1024];
    int bufferSize = 0;
    boolean eof = false;
    while (! eof) {
        int read = inputStream.read (buffer, bufferSize, buffer.length - bufferSize);
        if (read == - 1) {
            eof = true;
        } else {
            bufferSize += read;
            if (bufferSize == buffer.length) {
                buffer = growBuffer (buffer, bufferSize * 2);
            }
        }
    }
    return Arrays.copyOf (buffer, bufferSize);
}

private static byte [] growBuffer (byte [] oldBuffer, int newSize) {
    return Arrays.copyOf (oldBuffer, newSize);
}'''

DATA_R1["R84ca6c9dcf"] = r'''public void actionPerformed (ActionEvent e) {
    Color c = label.getBackground ();
    boolean flashing = FLASH_COLOR.equals (c);
    label.setBackground (flashing ? null : FLASH_COLOR);
    label.setForeground (flashing ? Color.black : Color.white);
}'''

DATA_R1["Ra1d335a7d8"] = r'''#include <stdio.h>
#include <string.h>

static void splitAndPrint (char *str, const char *delim) {
    char *in = str;
    for (;;) {
        char *token = strstr (in, delim);
        if (token == NULL) break;
        *token = '\0';
        printf ("%s\n", in);
        in = token + strlen (delim);
    }
    printf ("%s\n", in);
}

int main (void) {
    char str [] = "This is abc test abc string";
    splitAndPrint (str, "abc");
    return 0;
}'''

DATA_R1["R73286ffa0d"] = r'''public static void main (String [] args) {
    CustomClassLoader loader = new CustomClassLoader ();
    try {
        loadClass (loader, "sample.Sample");
    } catch (ClassNotFoundException | InstantiationException | IllegalAccessException e) {
        e.printStackTrace ();
    }
}

private static void loadClass (CustomClassLoader loader, String className)
        throws ClassNotFoundException, InstantiationException, IllegalAccessException {
    Class < ? > c = loader.findClass (className);
    Object o = c.newInstance ();
}'''

DATA_R1["Rf3a21bb32a"] = r'''private static bool ShouldExpand (GridItem gridItem)
{
    if (gridItem == null) return false;
    if (gridItem.GridItemType != GridItemType.Property) return false;
    if (!gridItem.Expandable) return false;
    object[] objs = gridItem.Value.GetType().GetCustomAttributes(typeof(PropertyGridInitialExpandedAttribute), false);
    if (objs.Length == 0) return false;
    return ((PropertyGridInitialExpandedAttribute)objs[0]).InitialExpanded;
}

private static void ExpandItemWithInitialExpandedAttribute (PropertyGrid propertyGrid, GridItem gridItem)
{
    if (ShouldExpand (gridItem))
    {
        gridItem.Expanded = true;
    }
    if (gridItem == null) return;
    foreach (GridItem childItem in gridItem.GridItems)
    {
        ExpandItemWithInitialExpandedAttribute (propertyGrid, childItem);
    }
}'''

DATA_R1["R9955954078"] = r'''public static IEnumerable < IEnumerable < T > > GetPermutations < T > (IEnumerable < IEnumerable < T > > lists) {
    if (! lists.Any ()) {
        yield break;
    }
    List < IEnumerator < T > > iterators = new List < IEnumerator < T > > ();
    foreach (var list in lists) {
        var it = list.GetEnumerator ();
        if (! it.MoveNext ()) {
            continue;
        }
        iterators.Add (it);
    }
    bool done = false;
    while (! done) {
        yield return from it in iterators
            select it.Current;
        done = ! Advance < T > (iterators);
    }
}

private static bool Advance < T > (List < IEnumerator < T > > iterators) {
    var mainIt = iterators.GetEnumerator ();
    mainIt.MoveNext ();
    do {
        var subIt = mainIt.Current;
        if (! subIt.MoveNext ()) {
            subIt.Reset ();
            subIt.MoveNext ();
            if (! mainIt.MoveNext ()) {
                return false;
            }
        } else {
            return true;
        }
    } while (true);
}'''

DATA_R1["Rbcd6619d12"] = r'''public static void main (String [] args) throws InterruptedException, ExecutionException {
    CompletableFuture < String > future = readPage ();
    attachHandlers (future);
}

private static void attachHandlers (CompletableFuture < String > future) {
    future.thenAccept (page -> printAndThrow (page)).exceptionally (e -> logAndRecover (e));
}

private static void printAndThrow (String page) {
    System.out.println (page);
    throw new IllegalArgumentException ("unexpected exception");
}

private static Void logAndRecover (Throwable e) {
    e.printStackTrace (System.err);
    return null;
}'''

DATA_R1["R1ff2f32faf"] = r'''def update(self, instance, validated_data):
    user_data = validated_data.pop('user', {})
    self._update_nested_user(instance, user_data)
    return super().update(instance, validated_data)

def _update_nested_user(self, instance, user_data):
    user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.update(instance.user, user_data)'''
