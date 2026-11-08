DATA_A2 = {
"T297": {
"python": r"""
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt

    def __str__(self):
        vals = []
        cur = self
        while cur is not None:
            vals.append(str(cur.val))
            cur = cur.next
        return "[" + ", ".join(vals) + "]"

def switch_pairs(head):
    if head is None or head.next is None:
        return head
    top = head.next
    first = head
    second = head.next
    while True:
        third = second.next
        second.next = first
        first.next = third
        first = third
        print("@@@ " + str(head))
        if first is not None:
            second.next.next = first.next
            second = first.next
        if not (first is not None and second is not None):
            break
    return top
""",
"c": r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int val;
    struct ListNode *next;
} ListNode;

static void print_list(const char *prefix, ListNode *node) {
    printf("%s[", prefix);
    for (ListNode *cur = node; cur != NULL; cur = cur->next)
        printf(cur == node ? "%d" : ", %d", cur->val);
    printf("]\n");
}

ListNode *switch_pairs(ListNode *head) {
    if (head == NULL || head->next == NULL) return head;
    ListNode *top = head->next;
    ListNode *first = head;
    ListNode *second = head->next;
    do {
        ListNode *third = second->next;
        second->next = first;
        first->next = third;
        first = third;
        print_list("@@@ ", head);
        if (first != NULL) {
            second->next->next = first->next;
            second = first->next;
        }
    } while (first != NULL && second != NULL);
    return top;
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;

public class ListNode
{
    public int val;
    public ListNode next;

    public ListNode SwitchPairs()
    {
        if (this == null || this.next == null) return this;
        ListNode top = this.next;
        ListNode first = this;
        ListNode second = first.next;
        do
        {
            ListNode third = second.next;
            second.next = first;
            first.next = third;
            first = third;
            Console.WriteLine("@@@ " + this);
            if (first != null)
            {
                second.next.next = first.next;
                second = first.next;
            }
        } while (first != null && second != null);
        return top;
    }

    public override string ToString()
    {
        var parts = new List<string>();
        for (ListNode cur = this; cur != null; cur = cur.next)
            parts.Add(cur.val.ToString());
        return "[" + string.Join(", ", parts) + "]";
    }
}
"""
}
}
