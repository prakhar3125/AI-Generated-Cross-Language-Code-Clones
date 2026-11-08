DATA_B3 = {
"T147": {
"python": r"""
def solution(X, A):
    empty_position = set(range(1, X + 1))
    for i in range(len(A)):
        empty_position.discard(A[i])
        if len(empty_position) == 0:
            return i
    return -1
""",
"c": r"""
#include <stdbool.h>
#include <stdlib.h>

int solution(int X, const int *A, int len) {
    bool *filled = calloc(X > 0 ? (size_t)X : 1, sizeof(bool));
    int remaining = X;
    for (int i = 0; i < len; i++) {
        if (A[i] >= 1 && A[i] <= X && !filled[A[i] - 1]) {
            filled[A[i] - 1] = true;
            remaining--;
        }
        if (remaining == 0) {
            free(filled);
            return i;
        }
    }
    free(filled);
    return -1;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class RiverCrossing
{
    public static int Solution(int X, int[] A)
    {
        var emptyPosition = new HashSet<int>();
        for (int i = 1; i <= X; i++)
        {
            emptyPosition.Add(i);
        }
        for (int i = 0; i < A.Length; i++)
        {
            emptyPosition.Remove(A[i]);
            if (emptyPosition.Count == 0)
            {
                return i;
            }
        }
        return -1;
    }
}
"""
}
}
