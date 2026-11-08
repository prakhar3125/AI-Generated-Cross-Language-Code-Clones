DATA_A7 = {
"T22": {
"python": r"""
def main(condition1=False, condition2=True):
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            k = 0
            while k < 9:
                if condition1:
                    print("Breaking from Loop K and J")
                    k = 9
                    j = 9
                if condition2:
                    print("Breaking from Loop K, J and I")
                    k = 9
                    j = 9
                    i = 9
                k += 1
            j += 1
        i += 1
    print("End of I , J , K")
""",
"c": r"""
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    bool condition1 = false;
    bool condition2 = true;
    int i = 0;
    while (i < 9) {
        int j = 0;
        while (j < 9) {
            int k = 0;
            while (k < 9) {
                if (condition1) {
                    printf("Breaking from Loop K and J\n");
                    k = 9;
                    j = 9;
                }
                if (condition2) {
                    printf("Breaking from Loop K, J and I\n");
                    k = 9;
                    j = 9;
                    i = 9;
                }
                k++;
            }
            if (condition1 || condition2) break;
            j++;
        }
        if (condition1 || condition2) break;
        i++;
    }
    printf("End of I , J , K\n");
    return 0;
}
""",
"csharp": r"""
using System;

public static class LoopBreaker
{
    private static bool condition1 = false;
    private static bool condition2 = true;

    public static void Main()
    {
        for (int i = 0; i < 9; i++)
        {
            for (int j = 0; j < 9; j++)
            {
                for (int k = 0; k < 9; k++)
                {
                    if (condition1)
                    {
                        Console.WriteLine("Breaking from Loop K and J");
                        k = 9;
                        j = 9;
                    }
                    if (condition2)
                    {
                        Console.WriteLine("Breaking from Loop K, J and I");
                        k = 9;
                        j = 9;
                        i = 9;
                    }
                }
            }
        }
        Console.WriteLine("End of I , J , K");
    }
}
"""
}
}
