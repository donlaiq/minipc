def solve(k, n):
    result = []
    def backtrack(start, current):
        if len(current) == k:
            result.append(list(current))
            return
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    backtrack(1, [])
    return result
