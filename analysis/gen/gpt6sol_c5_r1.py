DATAR1 = {}

DATAR1["R4a34d3a4cc"] = '''def leftmost_search(L, x):
    def helper(lo, hi):
        if lo == hi:
            if lo < len(L) and L[lo] == x:
                return lo
            return -1
        mid = (lo + hi) // 2
        if L[mid] < x:
            return helper(mid + 1, hi)
        return helper(lo, mid)
    return helper(0, len(L))'''

DATAR1["R1cabb3fa54"] = '''def get_nested(obj, indexes):
    try:
        current = obj
        for index in indexes:
            current = current[index]
        return current
    except (IndexError, KeyError, TypeError):
        return None'''

DATAR1["R17e5e197a9"] = '''def build_rules(tree, threshold, name, node=0, parent=None):
    global k
    if len(tree) == 1:
        k += 1
        print(str(k) + ' ' + "{} <= {} ".format(name, threshold, node))
        return
    left_rule = ' <= ' + str(threshold)
    right_rule = ' > ' + str(threshold)
    if node == 0:
        pathto[node] = left_rule
    else:
        pathto[node] = pathto[parent] + ' & ' + left_rule
    print(pathto[node])
    build_rules(tree[0], threshold, name, node * 2 + 1, node)
    build_rules(tree[1], threshold, name, node * 2 + 2, node)'''

DATAR1["R1ab11e56ab"] = '''import numpy as np

def reverse_array(arr):
    result = []
    for i in range(len(arr) - 1, -1, -1):
        result.append(arr[i])
    result.reverse()
    return np.array(result)'''

DATAR1["Rfbf7d4f5c2"] = '''SUFFIXES = {'ing', 'ed', 'ly', 'es'}

def strip_suffix_chars(verb):
    suffixes = set(SUFFIXES)
    return ''.join(c for c in verb if c not in suffixes)'''

DATAR1["R63b6384687"] = '''def merge_sort_range(a, low, high):
    if high - low < 1:
        return
    mid = (low + high) // 2
    merge_sort_range(a, low, mid)
    merge_sort_range(a, mid + 1, high)
    left = a[low:mid + 1]
    right = a[mid + 1:high + 1]
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    a[low:high + 1] = merged'''

DATAR1["Rda752e8442"] = '''def max_subarray_length(nums):
    cur = 0
    curi = 0
    best_len = 0
    for ind, value in enumerate(nums):
        if cur + value <= 0:
            cur = 0
            curi = ind + 1
        else:
            cur += value
        if cur > 0 and ind - curi + 1 > best_len:
            best_len = ind - curi + 1
    return best_len'''

DATAR1["Rd908836b46"] = '''#include <stdio.h>

#define POOL_SIZE 50

int total(const char **items, int count);
void function(const char **items);

char *a[POOL_SIZE] = {0};

int main(void) {
    int counter = 0;
    while (1) {
        counter += 1;
        function((const char **) a);
    }
    return 0;
}'''

DATAR1["Ra03011d81d"] = '''#include <stdio.h>

int sum(const char **items, int count);
void function(const char **items);

int main(void) {
    char *a[10] = {0};
    int counter = 1;
    for (;;) {
        counter += 1;
        printf("counter: %d, sum: %d\\n", counter, sum((const char **) a + 1, 0));
    }
    return 0;
}'''
