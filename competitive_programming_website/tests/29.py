class MyQueue:
    def __init__(self):
        self.in_s = []
        self.out_s = []
    def push(self, x):
        self.in_s.append(x)
    def pop(self):
        if not self.out_s:
            while self.in_s:
                self.out_s.append(self.in_s.pop())
        if self.out_s:
            return self.out_s.pop()
        return None
    def peek(self):
        if not self.out_s:
            while self.in_s:
                self.out_s.append(self.in_s.pop())
        return self.out_s[-1] if self.out_s else None
    def empty(self):
        return not self.in_s and not self.out_s

def solve(operations):
    q = MyQueue()
    results = []
    for op in operations:
        if op["op"] == "push":
            q.push(op["x"])
            results.append(None)
        elif op["op"] == "pop":
            results.append(q.pop())
        elif op["op"] == "peek":
            results.append(q.peek())
        elif op["op"] == "empty":
            results.append(q.empty())
    return results
