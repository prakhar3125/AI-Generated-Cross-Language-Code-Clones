DATA_T5 = {
    "T171": {
        "python": r'''def solution(X, A):
    leaves = set()
    for i in range(len(A)):
        leaves.add(A[i])
        if X in leaves and len(leaves) == X:
            return i
    return -1''',
        "c": r'''#include <stdbool.h>
#include <stdlib.h>

static bool int_set_contains(const unsigned char *seen, int value) {
    return seen[value] != 0;
}

int solution(int X, const int *A, int a_len) {
    unsigned char *seen = calloc(X + 1, 1);
    int seen_size = 0;
    for (int i = 0; i < a_len; i++) {
        if (A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            seen_size++;
        }
        if (int_set_contains(seen, X) && seen_size == X) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}''',
        "csharp": r'''using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int X, int[] A)
    {
        var leaves = new HashSet<int>();
        for (int i = 0; i < A.Length; i++)
        {
            leaves.Add(A[i]);
            if (leaves.Contains(X) && leaves.Count == X)
            {
                return i;
            }
        }
        return -1;
    }
}'''
    },
    "T533": {
        "python": r'''import threading


class Sleeper(threading.Thread):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.daemon = True

    def run(self):
        o = self.obj
        while True:
            try:
                stop_event = threading.Event()
                stop_event.wait()
            except KeyboardInterrupt:
                pass''',
        "c": r'''#include <stdio.h>

void run(void *object) {
    void *o = object;
    for (;;) {
        sleep_until_wakeup(o);
    }
}''',
        "csharp": r'''using System.Threading;

public class Sleeper
{
    private readonly object _object;

    public Sleeper(object obj)
    {
        _object = obj;
    }

    public void Run()
    {
        object o = _object;
        while (true)
        {
            try
            {
                Thread.Sleep(Timeout.Infinite);
            }
            catch (ThreadInterruptedException)
            {
            }
        }
    }
}'''
    },
    "T111": {
        "python": r'''def single_number(nums):
    answer = 0
    al = []
    for i in range(len(nums)):
        al.append(nums[i])
    for i in range(len(nums)):
        test = nums[i]
        if al.index(test) == len(al) - 1 - al[::-1].index(test):
            answer = nums[i]
    return answer''',
        "c": r'''#include <stdio.h>
#include <stdlib.h>

static int list_index_of(const int *list, int len, int value) {
    for (int i = 0; i < len; i++) {
        if (list[i] == value) return i;
    }
    return -1;
}

static int list_last_index_of(const int *list, int len, int value) {
    for (int i = len - 1; i >= 0; i--) {
        if (list[i] == value) return i;
    }
    return -1;
}

int single_number(const int *nums, int nums_len) {
    int answer = 0;
    int *al = malloc(nums_len * sizeof(int));
    for (int i = 0; i < nums_len; i++) {
        al[i] = nums[i];
    }
    for (int i = 0; i < nums_len; i++) {
        int test = nums[i];
        if (list_index_of(al, nums_len, test) == list_last_index_of(al, nums_len, test)) {
            answer = nums[i];
        }
    }
    free(al);
    return answer;
}''',
        "csharp": r'''using System.Collections.Generic;

public static class SingleNumberFinder
{
    public static int SingleNumber(int[] nums)
    {
        int answer = 0;
        var al = new List<int>();
        for (int i = 0; i < nums.Length; i++)
        {
            al.Add(nums[i]);
        }
        for (int i = 0; i < nums.Length; i++)
        {
            int test = nums[i];
            if (al.IndexOf(test) == al.LastIndexOf(test))
            {
                answer = nums[i];
            }
        }
        return answer;
    }
}'''
    }
}
