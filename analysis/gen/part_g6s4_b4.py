DATA_B4 = {
"T124": {
"python": r"""
def solution(X, A):
    length = len(A)
    if X > length:
        return -1
    is_filled = [0] * X
    jumped = 0
    for i in range(length):
        x = A[i]
        if x <= X:
            if is_filled[x - 1] == 0:
                is_filled[x - 1] = 1
                jumped += 1
                if jumped == X:
                    return i
    return -1
""",
"c": r"""
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    if (X > len) {
        return -1;
    }
    int *is_filled = calloc(X > 0 ? (size_t)X : 1, sizeof(int));
    int jumped = 0;
    for (int i = 0; i < len; i++) {
        int x = A[i];
        if (x <= X) {
            if (is_filled[x - 1] == 0) {
                is_filled[x - 1] = 1;
                jumped += 1;
                if (jumped == X) {
                    free(is_filled);
                    return i;
                }
            }
        }
    }
    free(is_filled);
    return -1;
}
""",
"csharp": r"""
using System;

public static class LeafJump
{
    public static int Solution(int X, int[] A)
    {
        int len = A.Length;
        if (X > len)
        {
            return -1;
        }
        int[] isFilled = new int[X];
        int jumped = 0;
        Array.Fill(isFilled, 0);
        for (int i = 0; i < len; i++)
        {
            int x = A[i];
            if (x <= X)
            {
                if (isFilled[x - 1] == 0)
                {
                    isFilled[x - 1] = 1;
                    jumped += 1;
                    if (jumped == X)
                    {
                        return i;
                    }
                }
            }
        }
        return -1;
    }
}
"""
}
}
