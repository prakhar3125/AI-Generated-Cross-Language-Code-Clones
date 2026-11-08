DATA_B10 = {
"T512": {
"python": r"""
def find_min(A, c):
    x = A[c]
    position = c
    while c < len(A):
        if x > A[c]:
            x = A[c]
            position = c
        c += 1
    return position
""",
"c": r"""
int findMIN(const int *A, int len, int c) {
    int x = A[c];
    int position = c;
    while (c < len) {
        if (x > A[c]) {
            x = A[c];
            position = c;
        }
        c++;
    }
    return position;
}
""",
"csharp": r"""
public static class ArraySearch
{
    public static int FindMIN(int[] A, int c)
    {
        int x = A[c];
        int position = c;
        while (c < A.Length)
        {
            if (x > A[c])
            {
                x = A[c];
                position = c;
            }
            c++;
        }
        return position;
    }
}
"""
},
"T14": {
"python": r"""
class Node:
    def __init__(self, val=0):
        self.val = val
        self.next = None

    def setNext(self, n):
        self.next = n

    def getNext(self):
        return self.next

    def equals(self, other):
        return self is other

head = None

def reverse(previous, current):
    global head
    if previous is None:
        return None
    if previous.equals(head):
        previous.setNext(None)
    if current is None:
        head = previous
        return head
    else:
        temp = current.getNext()
        current.setNext(previous)
        reverse(current, temp)
    return None
""",
"c": r"""
#include <stdbool.h>
#include <stdlib.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

static Node *head = NULL;

static bool node_equals(Node *a, Node *b) {
    return a == b;
}

static void node_set_next(Node *n, Node *next) {
    n->next = next;
}

static Node *node_get_next(Node *n) {
    return n->next;
}

Node *reverse(Node *previous, Node *current) {
    if (previous == NULL) return NULL;
    if (node_equals(previous, head)) node_set_next(previous, NULL);
    if (current == NULL) {
        head = previous;
        return head;
    } else {
        Node *temp = node_get_next(current);
        node_set_next(current, previous);
        reverse(current, temp);
    }
    return NULL;
}
""",
"csharp": r"""
public class LinkedList
{
    public class Node
    {
        public int val;
        private Node next;

        public void SetNext(Node n) { next = n; }
        public Node GetNext() { return next; }
        public bool Equals(Node other) { return ReferenceEquals(this, other); }
    }

    private Node head;

    public Node Reverse(Node previous, Node current)
    {
        if (previous == null) return null;
        if (previous.Equals(head)) previous.SetNext(null);
        if (current == null)
        {
            head = previous;
            return head;
        }
        else
        {
            Node temp = current.GetNext();
            current.SetNext(previous);
            Reverse(current, temp);
        }
        return null;
    }
}
"""
}
}
