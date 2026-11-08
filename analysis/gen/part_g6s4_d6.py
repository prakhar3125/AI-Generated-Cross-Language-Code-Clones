DATA_D6 = {
"R4474610115": r"""
int main (void) {
    int start;
    if (scanf ("%d", &start) != 1)
        exit (1);
    int end = start;
    while (scanf ("%d", &end) == 1)
        ;
    int i = start;
    while (i <= end) {
        printf ("%d\n", i);
        i++;
    }
}
"""
}
