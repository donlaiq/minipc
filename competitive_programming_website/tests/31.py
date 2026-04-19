class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def make_bst(arr):
    if not arr:
        return None
    root = TreeNode(arr[0])
    for v in arr[1:]:
        if v is None:
            continue
        node = root
        while True:
            if v < node.val:
                if not node.left:
                    node.left = TreeNode(v)
                    break
                node = node.left
            else:
                if not node.right:
                    node.right = TreeNode(v)
                    break
                node = node.right
    return root

def solve(arr, p_val, q_val):
    root = make_bst(arr)
    p_node = TreeNode(p_val)
    q_node = TreeNode(q_val)
    
    # Find lowest common ancestor in BST
    node = root
    while node:
        if p_val < node.val and q_val < node.val:
            node = node.left
        elif p_val > node.val and q_val > node.val:
            node = node.right
        else:
            return node.val
    return None
