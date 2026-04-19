class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def count_nodes(node):
    if not node: return 0
    visited = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if n.val in visited: continue
        visited.add(n.val)
        for nb in n.neighbors:
            if nb.val not in visited:
                stack.append(nb)
    return len(visited)

def solve(adj_list):
    if not adj_list:
        return None
    
    # Create nodes
    nodes = {}
    for i in range(len(adj_list)):
        nodes[i] = Node(i + 1)
    
    for i in range(len(adj_list)):
        for neighbor_idx in adj_list[i]:
            nodes[i].neighbors.append(nodes[neighbor_idx - 1])
    
    # Clone using DFS
    clones = {}
    def dfs(node):
        if node.val in clones:
            return clones[node.val]
        clone = Node(node.val)
        clones[node.val] = clone
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        return clone
    
    cloned = dfs(nodes[0])
    
    return {"nodes": len(adj_list), "cloned_nodes": count_nodes(cloned) if cloned else 0}
