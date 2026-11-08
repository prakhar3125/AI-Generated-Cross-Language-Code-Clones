DATA_D5 = {
"R4e335703d6": r"""
int main () {
    char s [SIZE];
    char *months [] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
    int result;
    printf ("enter the month : ");
    fgets (s, SIZE, stdin);
    s[strcspn (s, "\n")] = '\0';
    result = get_month (s, months);
    if (!result)
        printf ("%s invalid\n", s);
    else
        printf ("%s - %d.  is the month of the year.\n", s, result);
    return 0;
}
""",
"R9fdda16e3c": r"""
int main () {
    int num, sum = 0;
    scanf ("%d", & num);
    printf ("Factors are: ");
    print_factor_chain (num, 0);
    printf ("\n");
    printf ("Sum of factors is: ");
    sum = print_factor_chain (num, 1);
    printf ("= %d\n", sum);
}

static int print_factor_chain (int num, int with_sum) {
    int tmp = num, x, sum = 0;
    while (1) {
        x = getFirst (tmp);
        printf ("%d ", x);
        sum += x;
        if (x == tmp)
            break;
        if (with_sum)
            printf ("+ ");
        tmp /= x;
    }
    return sum;
}
""",
"Ra853448a33": r"""
static void set_raw_mode (struct termios *orig_attr, struct termios *new_attr) {
    tcgetattr (fileno (stdin), orig_attr);
    memcpy (new_attr, orig_attr, sizeof (*new_attr));
    new_attr->c_lflag &= ~(ICANON | ECHO);
    tcsetattr (fileno (stdin), TCSANOW, new_attr);
}

int main () {
    int counter = 0;
    struct termios orig_attr, new_attr;
    set_raw_mode (& orig_attr, & new_attr);
    pthread_t pid;
    if (pthread_create (&pid, NULL, thread, &counter)) {
        fprintf (stderr, "Create thread failed");
        exit (1);
    }
    while (1) {
        char c = getchar ();
        __sync_add_and_fetch (& counter, 1);
        printf ("add: %d\n", counter);
    }
    return 0;
}
"""
}
