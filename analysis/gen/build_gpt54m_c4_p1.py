DATA_T1 = {}

DATA_T1["T297"] = {"outputs": {
"python": """class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

    def values(self):
        out = []
        cur = self
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __str__(self):
        return str(self.values())


def switch_pairs(head):
    if head is None or head.next is None:
        return head
    top = head.next
    first = head
    second = first.next
    while True:
        third = second.next
        second.next = first
        first.next = third
        print("@@@ " + str(head))
        if first is not None:
            second.next.next = first.next
            second = first.next
        if not (first is not None and second is not None):
            break
        first = third
    return top
""",
"c": """struct Node {
    int value;
    struct Node *next;
};

void print_list(const char *prefix, struct Node *head) {
    printf("%s [", prefix);
    for (struct Node *cur = head; cur != NULL; cur = cur->next) {
        printf("%d", cur->value);
        if (cur->next != NULL) printf(", ");
    }
    printf("]\\n");
}

struct Node *switch_pairs(struct Node *head) {
    if (head == NULL || head->next == NULL) return head;
    struct Node *top = head->next;
    struct Node *first = head;
    struct Node *second = first->next;
    do {
        struct Node *third = second->next;
        second->next = first;
        first->next = third;
        print_list("@@@ ", head);
        first = third;
        if (first != NULL) {
            second->next->next = first->next;
            second = first->next;
        }
    } while (first != NULL && second != NULL);
    return top;
}
""",
"csharp": """public class ListNode {
    public int Value;
    public ListNode Next;

    public override string ToString() {
        var parts = new List<string>();
        var cur = this;
        while (cur != null) {
            parts.Add(cur.Value.ToString());
            cur = cur.Next;
        }
        return "[" + string.Join(", ", parts) + "]";
    }
}

public ListNode SwitchPairs() {
    if (this == null || this.Next == null) return this;
    ListNode top = this.Next;
    ListNode first = this;
    ListNode second = first.Next;
    do {
        ListNode third = second.Next;
        second.Next = first;
        first.Next = third;
        Console.WriteLine("@@@ " + this.ToString());
        first = third;
        if (first != null) {
            second.Next.Next = first.Next;
            second = first.Next;
        }
    } while (first != null && second != null);
    return top;
}
"""}}

DATA_T1["T252"] = {"outputs": {
"python": """class ActionEvent:
    pass


class XMLDecoder:
    def __init__(self, stream):
        self._stream = stream

    def read_object(self):
        return pickle.load(self._stream)

    def close(self):
        self._stream.close()


class Table:
    def __init__(self):
        self.model = None

    def set_model(self, model):
        self.model = model


file = "backup.xml"
table = Table()


def action_performed(e):
    try:
        with open(file, "rb") as raw:
            is_stream = io.BufferedReader(raw)
            xd = XMLDecoder(is_stream)
            model = xd.read_object()
            table.set_model(model)
    except OSError as ex:
        traceback.print_exc()
""",
"c": """typedef struct TableModel TableModel;

Table *table;
TableModel *model;

TableModel *read_table_model(FILE *in);

void action_performed(void) {
    FILE *is = fopen(file, "rb");
    if (is == NULL) {
        perror("fopen failed");
        return;
    }
    model = read_table_model(is);
    table_set_model(table, model);
    fclose(is);
}
""",
"csharp": """public class ActionEvent {
}


public void ActionPerformed(ActionEvent e) {
    try {
        using (var stream = new BufferedStream(new FileStream(file, FileMode.Open, FileAccess.Read))) {
            var decoder = new XmlSerializer(typeof(DataTable));
            model = (DataTable)decoder.Deserialize(stream);
        }
        table.Model = model;
    } catch (IOException ex) {
        Console.Error.WriteLine(ex.StackTrace);
    }
}
"""}}

DATA_T1["T10"] = {"outputs": {
"python": """class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


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
"c": """struct Node {
    int value;
    struct Node *next;
};

struct Node *reverse(struct Node *n, struct Node *p) {
    if (n == NULL) return NULL;
    if (n->next == NULL) {
        n->next = p;
        return n;
    }
    struct Node *r = reverse(n->next, n);
    n->next = p;
    return r;
}
""",
"csharp": """public class Node {
    public int Value;
    public Node Next;
}

public static Node Reverse(Node n, Node p) {
    if (n == null) return null;
    if (n.Next == null) {
        n.Next = p;
        return n;
    }
    Node r = Reverse(n.Next, n);
    n.Next = p;
    return r;
}
"""}}

DATA_T1["T146"] = {"outputs": {
"python": """def solution(x, a):
    seen = set()
    for i, value in enumerate(a):
        if value <= x:
            seen.add(value)
        if len(seen) == x:
            return i
    return -1
""",
"c": """int solution(int X, int A[], int len) {
    char seen[X + 1];
    memset(seen, 0, sizeof(seen));
    int distinct = 0;
    for (int i = 0; i < len; i++) {
        if (A[i] <= X && !seen[A[i]]) {
            seen[A[i]] = 1;
            distinct++;
        }
        if (distinct == X) return i;
    }
    return -1;
}
""",
"csharp": """public int Solution(int X, int[] A) {
    var hset = new HashSet<int>();
    for (int i = 0; i < A.Length; i++) {
        if (A[i] <= X) hset.Add(A[i]);
        if (hset.Count == X) return i;
    }
    return -1;
}
"""}}

DATA_T1["T110"] = {"outputs": {
"python": """def main():
    throw_catch_time = 0
    new_exception_time = 0
    new_object_time = 0
    no_stack_exception_time = 0
    for _ in range(30):
        throw_catch_time += throw_catch_loop()
        new_exception_time += new_exception_loop()
        new_object_time += new_object_loop()
        no_stack_exception_time += new_no_stack_exception_loop()
    print("throwCatchTime = " + str(throw_catch_time // 30))
    print("newExceptionTime = " + str(new_exception_time // 30))
    print("newStringTime = " + str(new_object_time // 30))
    print("noStackExceptionTime = " + str(no_stack_exception_time // 30))
""",
"c": """long throwCatchLoop(void);
long newExceptionLoop(void);
long newObjectLoop(void);
long newNoStackExceptionLoop(void);

int main(void) {
    long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++) {
        throwCatchTime += throwCatchLoop();
        newExceptionTime += newExceptionLoop();
        newObjectTime += newObjectLoop();
        noStackExceptionTime += newNoStackExceptionLoop();
    }
    printf("throwCatchTime = %ld\\n", throwCatchTime / 30);
    printf("newExceptionTime = %ld\\n", newExceptionTime / 30);
    printf("newStringTime = %ld\\n", newObjectTime / 30);
    printf("noStackExceptionTime = %ld\\n", noStackExceptionTime / 30);
    return 0;
}
""",
"csharp": """public static void Main(string[] args) {
    long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++) {
        throwCatchTime += ThrowCatchLoop();
        newExceptionTime += NewExceptionLoop();
        newObjectTime += NewObjectLoop();
        noStackExceptionTime += NewNoStackExceptionLoop();
    }
    Console.WriteLine("throwCatchTime = " + throwCatchTime / 30);
    Console.WriteLine("newExceptionTime = " + newExceptionTime / 30);
    Console.WriteLine("newStringTime = " + newObjectTime / 30);
    Console.WriteLine("noStackExceptionTime = " + noStackExceptionTime / 30);
}
"""}}
