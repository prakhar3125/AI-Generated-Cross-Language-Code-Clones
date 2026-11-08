DATA_R1 = {
"Rf3d83a68bd": r'''
def curry(func):
    def curried(*args):
        return lambda *more_args: func(*args, *more_args)
    return curried
''',
"Rfa50623d34": r'''
def upgrade():
    url = context.config.get_main_option("sqlalchemy.url")
    engine = sa.create_engine(url)
    DBSession.configure(bind=engine)
    clients = [
        {"client_id": client.id, "key": client.key, "secret": client.secret,
         "is_active": True, "created_at": sa.func.now(), "updated_at": sa.func.now()}
        for client in Client.query.all()
    ]
    op.create_table(
        "client_credential",
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
        sa.ForeignKeyConstraint(["client_id"], ["client.id"]),
        *[
            sa.Column(name, kind, nullable=False)
            for name, kind in [
                ("id", sa.Integer()),
                ("created_at", sa.DateTime()),
                ("updated_at", sa.DateTime()),
                ("client_id", sa.Integer()),
                ("key", sa.String(length=22)),
                ("secret", sa.String(length=44)),
                ("is_active", sa.Boolean()),
            ]
        ]
    )
    op.bulk_insert(ClientCredential, clients)
    for column in ("secret", "key"):
        op.drop_column(u"client", column)
''',
"R6977f1c997": r'''
def scan(sentence):
    tuples = []
    for word in sentence.split():
        if word in lexicons:
            tuples.append((lexicons[word], word))
        elif word.isdigit():
            tuples.append(("number", int(word)))
        else:
            tuples.append(("error", word))
    return tuples
''',
"Rbcec8876d4": r'''
def contains(small, big):
    n = len(small)
    for i in range(len(big) - n + 1):
        if big[i:i + n] == small:
            return i, i + n
    return False
''',
"Recd81e23e8": r'''
static void zeroed_alloc (char **slot) {
    *slot = (char *) calloc (20, 1);
}

int main (int argc, char **argv) {
    int i = 0;
    do {
        zeroed_alloc (& ret [i]);
        i ++;
    } while (i < 2);
    char **ipnport = arguments_handle (argc, argv);
    printf ("IP is :%s port range is %s\n", ipnport [1], ipnport [0]);
    return 0x0;
}
''',
"Rc8ce82f32f": r'''
int main (int argc, char **argv) {
    char c;
    int waiting = 1;
    printf ("Press key");
    while (waiting) {
        if (kbhit ()) {
            waiting = 0;
        } else {
            printf (".");
            fflush (stdout);
            sleep (1);
        }
    }
    c = getchar ();
    printf ("\nChar received:%c\n", c);
    printf ("Done.\n");
    return 0;
}
''',
"Rab8fdb571d": r'''
int main () {
    char *str = malloc (100);
    strcpy (str, "test string.");
    char *token = strtok (str, " ");
    while (token != NULL) {
        printf ("%s\n", token);
        token = strtok (NULL, " ");
    }
    free (str);
    return 0;
}
''',
"R8f617cb401": r'''
int main () {
    unsigned long data [9];
    unsigned long *p = data;
    unsigned long *end = data + 9;
    unsigned long value = 0;
    while (p < end) {
        *p ++ = value ++;
    }
    printf ("%lu\n", sumOfColTwo (data));
    return 0;
}
''',
"R83b1b1f08f": r'''
void main (int argc, char **argv) {
    char **myargv = malloc ((argc - 1) * sizeof (char *));
    int i = argc - 1;
    while (i > 0) {
        int len = strlen (argv [i]) + 1;
        myargv [i - 1] = malloc (len);
        memcpy (myargv [i - 1], argv [i], len);
        i --;
    }
    getch ();
}
''',
}
