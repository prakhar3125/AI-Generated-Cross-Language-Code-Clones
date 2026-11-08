DATA_B6 = {
"T592": {
"python": r"""
import random

def rand_nums(total, n):
    results = [0] * n
    if total == 0:
        return results
    total_plus_1 = total + 1
    while True:
        rs = [random.getrandbits(256) for _ in range(n)]
        s = sum(rs)
        if s == 0:
            continue
        for i in range(n):
            results[i] = (s % rs[i]) % total_plus_1
        return results
""",
"c": r"""
#include <stdlib.h>

/* BigInteger arithmetic approximated with unsigned long for C */
static unsigned long rand_ulong(void) {
    unsigned long v = 0;
    for (int b = 0; b < 4; b++) {
        v = (v << 16) | (unsigned long)(rand() & 0xFFFF);
    }
    return v;
}

int *rand_nums(int total, int n) {
    int *results = malloc(sizeof(int) * (size_t)n);
    if (total == 0) {
        for (int i = 0; i < n; i++) results[i] = 0;
        return results;
    }
    unsigned long total_plus_1 = (unsigned long)total + 1UL;
    while (1) {
        unsigned long *rs = malloc(sizeof(unsigned long) * (size_t)n);
        for (int i = 0; i < n; ++i) {
            rs[i] = rand_ulong();
        }
        unsigned long sum = 0;
        for (int i = 0; i < n; ++i) {
            sum += rs[i];
        }
        if (sum == 0) {
            free(rs);
            continue;
        }
        for (int i = 0; i < n; ++i) {
            results[i] = (int)((sum % rs[i]) % total_plus_1);
        }
        free(rs);
        return results;
    }
}
""",
"csharp": r"""
using System;
using System.Numerics;

public class Randomizer
{
    private readonly Random rand = new Random();

    public int[] RandNums(int total, int n)
    {
        int[] results = new int[n];
        if (total == 0)
        {
            Array.Fill(results, 0);
            return results;
        }
        BigInteger totalPlus1 = new BigInteger(total + 1L);
        while (true)
        {
            BigInteger[] rs = new BigInteger[n];
            byte[] buffer = new byte[32];
            for (int i = 0; i < n; ++i)
            {
                rand.NextBytes(buffer);
                buffer[31] &= 0x7F;
                rs[i] = new BigInteger(buffer);
            }
            BigInteger sum = BigInteger.Zero;
            foreach (BigInteger r in rs)
            {
                sum += r;
            }
            if (sum == BigInteger.Zero)
            {
                continue;
            }
            for (int i = 0; i < n; ++i)
            {
                results[i] = (int)(sum % rs[i] % totalPlus1);
            }
            return results;
        }
    }
}
"""
}
}
