DATAR2 = {}

DATAR2["R0c1c130c91"] = '''#include <stdio.h>

int main(void) {
    int i = 0;
    while (i < 6) {
        int k = i;
        while (k++ < 5) {
            printf("+");
        }
        for (int j = 0; j < i * 2 + 1; j++) {
            printf("*");
        }
        printf("\\n");
        i++;
    }
    return 0;
}'''

DATAR2["R5e98c898ba"] = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void trim_newline(char *s) {
    size_t len = strlen(s);
    while (len > 0 && (s[len - 1] == '\\n' || s[len - 1] == '\\r')) {
        s[--len] = '\\0';
    }
}

int main(void) {
    char *name = malloc(128);
    if (name == NULL) {
        return 1;
    }
    printf("Enter your name: ");
    if (fgets(name, 128, stdin) == NULL) {
        free(name);
        return 1;
    }
    trim_newline(name);
    printf("Hello %s. Nice to meet you.\\n", name);
    free(name);
    return 0;
}'''

DATAR2["R20dd558187"] = '''#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void trim_newline(char *s, size_t *len) {
    while (*len > 0 && (s[*len - 1] == '\\n' || s[*len - 1] == '\\r')) {
        s[--(*len)] = '\\0';
    }
}

int main(void) {
    char *x = NULL;
    size_t cap = 0;
    size_t len = getline(&x, &cap, stdin);
    if (len == (size_t) -1) {
        free(x);
        return 1;
    }
    trim_newline(x, &len);
    if (len >= 2 && strcmp(x + len - 2, "ed") == 0) {
        printf("already past tense: %s\\n", x);
    } else {
        printf("word: %s\\n", x);
    }
    free(x);
    return 0;
}'''

DATAR2["Ra2d10bef4b"] = '''using System;
using SharpDX.Direct3D11;

public class TexturePool : IDisposable
{
    private System.Collections.Concurrent.ConcurrentStack<Texture2D> m_freeStack;
    private bool disposedValue;

    public void Dispose()
    {
        if (disposedValue) return;
        if (m_freeStack == null)
        {
            disposedValue = true;
            return;
        }
        while (m_freeStack.TryPop(out Texture2D texture))
        {
            texture.Dispose();
        }
        m_freeStack = null;
        disposedValue = true;
    }
}'''

DATAR2["R7176808dc7"] = '''public class FilterCoefficients
{
    private double k;
    private double A0, A1, A2, B1, B2;

    public FilterCoefficients(double sampleRatio)
    {
        k = sampleRatio;
        double denom = k * k + k / Q + 1;
        A0 = k / (Q * denom);
        A2 = -A0;
        B1 = 2 * (k * k - 1) / denom;
        B2 = (k * k - k / Q + 1) / denom;
    }

    private const double Q = 1.0;
}'''

DATAR2["R241b8d374d"] = '''public class FilterCoefficientsDistributed
{
    private double k;
    private double A0, A1, A2, B1, B2;

    public FilterCoefficientsDistributed(double sampleRatio)
    {
        k = sampleRatio;
        double norm = 1.0 / (1 + k / Q + k * k);
        A0 = norm + k * k * norm;
        A1 = 2 * k * k * norm - 2 * norm;
        A2 = A0;
        B1 = A1;
        B2 = norm - (k / Q) * norm + k * k * norm;
    }

    private const double Q = 1.0;
}'''

DATAR2["R5b8db4fec9"] = '''public class AmpBufferedStream : BaseStream
{
    private const char AmpToken = '&';
    private int _bufferState;

    public override void Write(char value)
    {
        if (_bufferState <= 0)
        {
            base.Write(value);
            return;
        }
        if (value != AmpToken)
        {
            string temp = "&";
            _bufferState = 0;
            base.Write(temp);
        }
        else
        {
            _bufferState++;
            return;
        }
        base.Write(value);
    }
}'''

DATAR2["R8d0d71b76a"] = '''using System.Text;

public static class DurationFormatter
{
    public static string Format(TimeSpan span)
    {
        var sb = new StringBuilder();
        void AppendPart(long value, string label)
        {
            if (value != 0 || sb.Length != 0)
            {
                sb.Append(value).Append(' ').Append(label).Append(' ');
            }
        }
        AppendPart(span.Hours, "hours");
        AppendPart(span.Minutes, "minutes");
        AppendPart(span.Seconds, "seconds");
        AppendPart(span.Milliseconds, "Milliseconds");
        if (sb.Length == 0)
        {
            sb.Append(0).Append(' ').Append("seconds");
        }
        return sb.ToString().TrimEnd();
    }
}'''
