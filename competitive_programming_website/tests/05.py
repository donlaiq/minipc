class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def make_list(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for v in arr[1:]:
        curr.next = ListNode(v)
        curr = curr.next
    return head

def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def solve(lists):
    # Check that all lists are sorted in ascending order
    for lst in lists:
        if lst is None:
            continue
        if isinstance(lst, list):
            for k in range(1, len(lst)):
                if lst[k] < lst[k-1]:
                    return None  # invalid: not sorted
    
    import heapq
    heap = []
    for i, node in enumerate(lists):
        if isinstance(node, list):
            node = make_list(node)
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return list_to_array(dummy.next)
