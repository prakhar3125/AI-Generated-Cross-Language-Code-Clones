DATA6 = {
"Refa2e73039": r"""int sumRest (const char *p) {
    int sum = 0, n, len;
    while (sscanf (p, "%d%n", &n, &len) == 1) {
        sum += n;
        p += len;
    }
    return sum;
}

int main (void) {
    char line [128];
    printf ("enter numbers: ");
    scanf ("%127[^\n]", line);
    printf ("sum: %d\n", sumRest (line));
    return 0;
}""",
"R0113c1db9b": r"""def foo(thing=None, thing_seq=None):
    if thing_seq is None and thing is None:
        return
    if thing_seq is not None:
        for _thing in thing_seq:
            foo(thing=_thing)
    if thing is not None:
        print("did foo with", thing)""",
"Rc5f95dbda1": r"""private static void GetUserData (string userName, UserSession user) {
    using (Entities ctx = CommonSERT.GetContext ()) {
        var result = ctx.datUserRoles
            .Where (ur => string.Equals (ur.AccountName, userName, StringComparison.CurrentCultureIgnoreCase))
            .Select (ur => new {ur.Active, ur.ID})
            .FirstOrDefault ();
        if (result != null)
            user.UserActive = result.Active;
        user.UserID = result.ID;
    }
}""",
"Rf9eb0ff068": r'''def function(argument):
    max_arg = max(argument)
    argument.remove(max_arg)
    return "true" if any(
        sum(combo) == max_arg
        for length in range(1, len(argument) + 1)
        for combo in combinations(argument, length)
    ) else "false"''',
"R1479812111": r"""public void doWork () {
    for (int h = 0; h <= 0; h ++) {
        Thread.Sleep (3000);
        h.Dump ();
    }
}""",
"R314ba9cd4a": r"""void printDigit (int digit) {
    if (digit <= 9)
        printf ("%d", digit);
    else
        printf ("%c", 'A' + digit - 10);
}

int main (void) {
    int i, base;
    int word [32];
    unsigned long int number;
    printf ("Enter the decimal number to be converted: ");
    scanf ("%ld", & number);
    printf ("\nEnter the new base: ");
    scanf ("%d", & base);
    i = wordCalculator (word, number, base);
    printf ("The number is: ");
    do {
        printDigit (word [i]);
        i--;
    } while (i >= 0);
    printf ("\n");
    return 0;
}""",
"R7ca8e2a2eb": r"""static boolean isImmutable (Object obj) {
    Class < ? > objClass = obj.getClass ();
    if (! Immutable.class.equals (objClass.getSuperclass ()) || ! Modifier.isFinal (objClass.getModifiers ())) {
        return false;
    }
    for (Field field : objClass.getDeclaredFields ()) {
        if (! Modifier.isFinal (field.getModifiers ()) || ! isValidFieldType (field.getType ())) {
            return false;
        }
    }
    return true;
}""",
"R8db01bf25f": r"""def flatten(xs):
    if not xs:
        return []
    head, *tail = xs
    rest = flatten(tail)
    return flatten(head) + rest if isinstance(head, list) else [head] + rest""",
}
