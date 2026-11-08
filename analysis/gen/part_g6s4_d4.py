DATA_D4 = {
"Rb8f6c8b5d0": r"""
static int parse_number (const char *s, int i, int *num, int *m);

int main (void) {
    char s [1000], alp [1000];
    int num [1000];
    int m = 0, n = 0;
    int i = 0, j;
    unsigned char ch;
    scanf ("%999[^\n]", s);
    while ((ch = s[i]) != '\0') {
        if (isalpha (ch)) {
            alp[n++] = s[i];
            i++;
            continue;
        }
        if (!isdigit (ch)) {
            printf ("include invalid character (%c).\n", ch);
            return -1;
        }
        i = parse_number (s, i, num, &m);
    }
    for (i = 0; i < m; i++) {
        for (j = 0; j < num[i]; j++)
            printf ("%c", alp[i]);
    }
    puts ("");
    return 0;
}

static int parse_number (const char *s, int i, int *num, int *m) {
    num[*m] = 0;
    while (isdigit ((unsigned char) s[i])) {
        num[*m] = num[*m] * 10 + s[i] - '0';
        ++i;
    }
    ++(*m);
    return i;
}
""",
"R8b80f20070": r"""
int main () {
    double v;
    int err;
    err = scanf ("%lf", &v);
    if (1 != err) {
        printf ("read failed\n");
        return 0;
    }
    printf ("%lf\n", v);
    return 0;
}
"""
}
