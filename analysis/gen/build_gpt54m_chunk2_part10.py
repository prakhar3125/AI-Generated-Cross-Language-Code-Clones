DATA_R1 = {
    "R8549838705": r'''#include <stdio.h>

int main() {
    const int array_a[3] = {2, 4, 6}, array_b[3] = {1, 3, 5};
    int array_c[6];
    int i = 0;
    for (int j = 0; j < 3; j++) {
        array_c[i++] = array_a[j];
    }
    for (int j = 0; j < 3; j++) {
        array_c[i++] = array_b[j];
    }
    i = 0;
    while (i < 6) {
        printf("array_c[%d]=%d\n", i, array_c[i]);
        i++;
    }
    return 0;
}''',
    "Reec8438c4b": r'''#include <stdio.h>

int main() {
    FILE *fin = fopen("in.txt", "r");
    FILE *fout = fopen("out.txt", "w");
    char buffer[1024];
    size_t n;
    while ((n = fread(buffer, 1, sizeof(buffer), fin)) > 0) {
        fwrite(buffer, 1, n, fout);
    }
    fclose(fin);
    fclose(fout);
    printf("\nFile has been created...\n");
    return 0;
}''',
    "Rd776867156": r'''public static void close (Statement...statements) {
    int i = statements.length - 1;
    while (i >= 0) {
        quietClose (statements [i]);
        i --;
    }
}

private static void quietClose (Statement stmt) {
    if (stmt == null) {
        return;
    }
    try {
        stmt.close ();
    } catch (SQLException se) {
    }
}''',
    "Rb67c7892a4": r'''public void run () {
    int i = 2;
    try {
        while (i -- > 0) {
            System.out.println ("tic");
        }
    } catch (Exception e) {
        e.getStackTrace ();
    }
}''',
    "R8818908361": r'''#include <stdio.h>
#include <string.h>

int main () {
    char months [] = "JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC";
    printf ("months=[%s]\n\n", months);
    char *cursor = months;
    for (;;) {
        char *comma = strchr (cursor, ',');
        if (comma != NULL) {
            *comma = '\0';
            printf ("month=[%s]\n", cursor);
            cursor = comma + 1;
        } else {
            printf ("month=[%s]\n", cursor);
            break;
        }
    }
    printf ("\n");
    return 0;
}''',
    "Rd613be00ca": r'''public static byte [] readBytes (InputStream inputStream) throws IOException {
    ByteArrayOutputStream out = new ByteArrayOutputStream ();
    byte [] chunk = new byte [8 * 1024];
    int read;
    while ((read = inputStream.read (chunk)) != - 1) {
        out.write (chunk, 0, read);
    }
    return out.toByteArray ();
}''',
    "R84ca6c9dcf": r'''public void actionPerformed (ActionEvent e) {
    boolean flashing = FLASH_COLOR.equals (label.getBackground ());
    label.setBackground (flashing ? null : FLASH_COLOR);
    label.setForeground (flashing ? Color.black : Color.white);
}''',
    "Ra1d335a7d8": r'''#include <stdio.h>
#include <string.h>

int main (void) {
    char str [] = "This is abc test abc string";
    const char *delim = "abc";
    size_t delim_len = strlen (delim);
    char *start = str;
    while (start != NULL) {
        char *hit = strstr (start, delim);
        if (hit == NULL) {
            printf ("%s\n", start);
            start = NULL;
        } else {
            *hit = '\0';
            printf ("%s\n", start);
            start = hit + delim_len;
        }
    }
    return 0;
}''',
    "R73286ffa0d": r'''public static void main (String [] args) {
    CustomClassLoader loader = new CustomClassLoader ();
    try {
        Class < ? > c = loader.findClass ("sample.Sample");
        Object o = c.newInstance ();
    } catch (ReflectiveOperationException e) {
        e.printStackTrace ();
    }
}''',
    "Rf3a21bb32a": r'''private static void ExpandItemWithInitialExpandedAttribute (PropertyGrid propertyGrid, GridItem gridItem) {
    if (gridItem == null) {
        return;
    }
    ExpandIfAttributed (gridItem);
    foreach (GridItem childItem in gridItem.GridItems) {
        ExpandItemWithInitialExpandedAttribute (propertyGrid, childItem);
    }
}

private static void ExpandIfAttributed (GridItem gridItem) {
    if (gridItem.GridItemType != GridItemType.Property || ! gridItem.Expandable) {
        return;
    }
    object [] objs = gridItem.Value.GetType ().GetCustomAttributes (typeof (PropertyGridInitialExpandedAttribute), false);
    if (objs.Length == 0) {
        return;
    }
    if (((PropertyGridInitialExpandedAttribute) objs [0]).InitialExpanded) {
        gridItem.Expanded = true;
    }
}''',
    "R9955954078": r'''public static IEnumerable < IEnumerable < T > > GetPermutations < T > (IEnumerable < IEnumerable < T > > lists) {
    var pool = lists.Select (list => list.ToList ()).Where (list => list.Count > 0).ToList ();
    if (pool.Count == 0) {
        yield break;
    }
    var positions = new int [pool.Count];
    while (true) {
        yield return pool.Select ((list, idx) => list [positions [idx]]).ToList ();
        int carry = pool.Count - 1;
        while (carry >= 0) {
            positions [carry] ++;
            if (positions [carry] < pool [carry].Count) {
                break;
            }
            positions [carry] = 0;
            carry --;
        }
        if (carry < 0) {
            yield break;
        }
    }
}''',
    "Rbcd6619d12": r'''public static void main (String [] args) throws Exception {
    CompletableFuture < Void > pipeline = readPage ()
        .thenAccept (page -> {
            System.out.println (page);
            throw new IllegalArgumentException ("unexpected exception");
        });
    pipeline.handle ((result, error) -> {
        if (error != null) {
            error.printStackTrace (System.err);
        }
        return null;
    });
}'''
}
