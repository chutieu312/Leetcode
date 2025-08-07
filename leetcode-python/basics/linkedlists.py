# Node class
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Create a linked list: 1 -> 2 -> 3
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)

# Traverse and print the linked list
def print_list(node):
    while node:
        print(node.val, end=" -> " if node.next else "\n")
        node = node.next

print_list(head)  # Output: 1 -> 2 -> 3


# Insert a new node at the beginning
new_node = ListNode(0)
new_node.next = head
head = new_node


# delete a node with a specific value from the linked list 
def delete_node(head, val):
    dummy = ListNode(0, head)
    prev, curr = dummy, head
    while curr:
        if curr.val == val:
            prev.next = curr.next
            break
        prev, curr = curr, curr.next
    return dummy.next


# reverse a linked list
# This function reverses a linked list in place and returns the new head
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev