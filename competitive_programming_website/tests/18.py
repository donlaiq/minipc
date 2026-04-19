class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.end = True
    def search(self, word):
        node = self._search_prefix(word)
        return node and node.end if node else False
    def startsWith(self, prefix):
        return self._search_prefix(prefix) is not None
    def _search_prefix(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

def solve(operations=None):
    trie = Trie()
    results = []
    for op in (operations or []):
        if op["op"] == "insert":
            trie.insert(op["word"])
        elif op["op"] == "search":
            results.append(trie.search(op["word"]))
        elif op["op"] == "startsWith":
            results.append(trie.startsWith(op["prefix"]))
    return results if results else None
