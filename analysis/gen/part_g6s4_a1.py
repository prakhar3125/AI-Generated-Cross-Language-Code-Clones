DATA_A1 = {
"T10": {
"python": r"""
class Node:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

def reverse(n, p):
    if n is None:
        return None
    if n.next is None:
        n.next = p
        return n
    r = reverse(n.next, n)
    n.next = p
    return r
""",
"c": r"""
#include <stdlib.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node *reverse(Node *n, Node *p) {
    if (n == NULL) return NULL;
    if (n->next == NULL) {
        n->next = p;
        return n;
    }
    Node *r = reverse(n->next, n);
    n->next = p;
    return r;
}
""",
"csharp": r"""
public static class ListOps
{
    public class Node
    {
        public int val;
        public Node next;
    }

    public static Node Reverse(Node n, Node p)
    {
        if (n == null) return null;
        if (n.next == null)
        {
            n.next = p;
            return n;
        }
        Node r = Reverse(n.next, n);
        n.next = p;
        return r;
    }
}
"""
},
"T146": {
"python": r"""
def solution(x, a):
    hset = set()
    for i, v in enumerate(a):
        if v <= x:
            hset.add(v)
        if len(hset) == x:
            return i
    return -1
""",
"c": r"""
#include <stdbool.h>
#include <stdlib.h>

int solution(int x, const int *a, int len) {
    int *seen = malloc(sizeof(int) * (x > 0 ? (size_t)x : 1));
    int count = 0;
    for (int i = 0; i < len; i++) {
        if (a[i] <= x) {
            bool found = false;
            for (int j = 0; j < count; j++) {
                if (seen[j] == a[i]) {
                    found = true;
                    break;
                }
            }
            if (!found) seen[count++] = a[i];
        }
        if (count == x) {
            free(seen);
            return i;
        }
    }
    free(seen);
    return -1;
}
""",
"csharp": r"""
using System.Collections.Generic;

public static class FrogRiver
{
    public static int Solution(int x, int[] a)
    {
        var hset = new HashSet<int>();
        for (int i = 0; i < a.Length; i++)
        {
            if (a[i] <= x) hset.Add(a[i]);
            if (hset.Count == x) return i;
        }
        return -1;
    }
}
"""
}
}
