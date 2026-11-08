DATA_R4 = {}

DATA_R4["Rb8f6c8b5d0"] = """int main (void) {
    char s[1000], alp[1000];
    int num[1000];
    int m = 0, n = 0;
    int i = 0, j;
    unsigned char ch;
    scanf("%999[^\\n]", s);
    while ((ch = s[i]) != 0) {
        if (isalpha(ch)) {
            alp[n++] = s[i];
            i++;
        }
        else if (isdigit(ch)) {
            int val = 0;
            while (isdigit((unsigned char) s[i])) {
                val = val * 10 + (s[i] - '0');
                i++;
            }
            num[m++] = val;
        }
        else {
            printf("include invalid character (%c).\\n", ch);
            return -1;
        }
    }
    for (i = 0; i < m; i++) {
        for (j = 0; j < num[i]; j++)
            printf("%c", alp[i]);
    }
    puts("");
    return 0;
}"""

DATA_R4["R8b80f20070"] = """int main () {
    double v;
    int err;
    err = scanf ("%lf", &v);
    switch (err) {
        case 1:
            printf ("%lf\\n", v);
            break;
        default:
            printf ("read failed\\n");
            break;
    }
    return 0;
}"""

DATA_R4["R4e335703d6"] = """int main () {
    char s [SIZE];
    char *months [] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    printf ("enter the month : ");
    gets (s);
    int result = get_month (s, months);
    if (result != 0) {
        printf ("%s - %d.  is the month of the year.\\n", s, result);
        return 0;
    }
    printf ("%s invalid\\n", s);
    return 0;
}"""

DATA_R4["R9fdda16e3c"] = """void print_factors (int n) {
    int x, tmp = n;
    printf ("Factors are: ");
    while (1) {
        x = getFirst (tmp);
        printf ("%d ", x);
        if (x == tmp)
            break;
        tmp /= x;
    }
    printf ("\\n");
}

int main () {
    int num;
    scanf ("%d", & num);
    print_factors (num);
    int tmp = num;
    int x, sum = 0;
    printf ("Sum of factors is: ");
    while (1) {
        x = getFirst (tmp);
        printf ("%d ", x);
        sum += x;
        if (x == tmp)
            break;
        printf ("+ ");
        tmp /= x;
    }
    printf ("= %d\\n", sum);
    return 0;
}"""

DATA_R4["Ra853448a33"] = """int main () {
    int counter = 0;
    struct termios orig_attr, new_attr;
    tcgetattr (fileno (stdin), & orig_attr);
    memcpy (& new_attr, & orig_attr, sizeof (new_attr));
    new_attr.c_lflag &= ~(ICANON | ECHO);
    tcsetattr (fileno (stdin), TCSANOW, & new_attr);
    pthread_t pid;
    if (pthread_create (&pid, NULL, thread, &counter) != 0) {
        fprintf (stderr, "Create thread failed");
        exit (1);
    }
    for (;;) {
        char c = getchar ();
        __sync_add_and_fetch (& counter, 1);
        printf ("add: %d\\n", counter);
    }
    tcsetattr (fileno (stdin), TCSANOW, & orig_attr);
    return 0;
}"""

DATA_R4["R4474610115"] = """int main (void) {
    int start;
    int end;
    if (scanf ("%d", &start) != 1)
        exit (1);
    end = start;
    while (scanf ("%d", &end) == 1)
        ;
    int i = start;
    do {
        printf ("%d\\n", i);
        i++;
    } while (i <= end);
    return 0;
}"""
