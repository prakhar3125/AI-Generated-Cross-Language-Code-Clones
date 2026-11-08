DATA_D3 = {
"Rfaf0b51ec8": r"""
def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    while True:
        i = r - 1
        while i >= 0 and indices[i] == i + n - r:
            i -= 1
        if i < 0:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        current = tuple(pool[k] for k in indices)
        if 1 not in current or 3 not in current:
            yield current
"""
}
