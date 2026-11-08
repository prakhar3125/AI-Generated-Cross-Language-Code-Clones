DATA8 = {
"T682": {"outputs": {
"python": r"""def filter(source, start, end, dest, dstart, dend, decimal_digits=2):
    dot_pos = -1
    length = len(dest)
    for i, c in enumerate(dest):
        if c == "." or c == ",":
            dot_pos = i
            break
    if dot_pos >= 0:
        if source == "." or source == ",":
            return ""
        if dend <= dot_pos:
            return None
        if length - dot_pos > decimal_digits:
            return ""
    return None
""",
"c": r"""#include <string.h>

const char *filter(const char *source, int start, int end, const char *dest,
                   int dstart, int dend, int decimalDigits) {
    int dotPos = -1;
    int len = (int)strlen(dest);
    for (int i = 0; i < len && dotPos < 0; i++) {
        if (dest[i] == '.' || dest[i] == ',') dotPos = i;
    }
    if (dotPos >= 0) {
        if (source[0] == '.' || source[0] == ',') return "";
        if (dend <= dotPos) return 0;
        if (len - dotPos > decimalDigits) return "";
    }
    return 0;
}
""",
"csharp": r"""public class DecimalRangeFilter
{
    private int decimalDigits = 2;

    public string Filter(string source, int start, int end, string dest, int dstart, int dend)
    {
        int dotPos = -1;
        int len = dest.Length;
        int i = 0;
        while (i < len && dotPos < 0)
        {
            if (dest[i] == '.' || dest[i] == ',') dotPos = i;
            i++;
        }
        if (dotPos >= 0)
        {
            if (source == "." || source == ",") return "";
            if (dend <= dotPos) return null;
            if (len - dotPos > decimalDigits) return "";
        }
        return null;
    }
}
""",
}},
}
