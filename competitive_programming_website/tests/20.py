class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def make_tree(arr):
    if not arr:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while i < len(arr):
        node = queue.pop(0)
        if arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr):
            if arr[i] is not None:
                node.right = TreeNode(arr[i])
                queue.append(node.right)
            i += 1
    return root

def solve(tree_arr):
    root = make_tree(tree_arr) if tree_arr else None
    if not root:
        return 0
    return 1 + max(solve_list_to_tree(root.left) if hasattr(root, 'left') else solve(root.left),
                   solve_list_to_tree(root.right) if hasattr(root, 'right') else solve(root.right)) if root else 0

def solve_list_to_tree(node):
    if not node:
        return 0
    return 1 + max(solve_list_to_tree(node.left), solve_list_to_tree(node.right))

def solve(tree_arr):
    root = make_tree(tree_arr) if tree_arr else None
    if not root:
        return 0
    return 1 + max(solve_list_to_tree(root.left), solve_list_to_tree(root.right))

def solve_list_to_tree(node):
    if not node:
        return 0
    return 1 + max(solve_list_to_tree(node.left), solve_list_to_tree(node.right))
