def solve(nums):
    result = []
    def backtrack(current, used):
        if len(current) == len(nums):
            result.append(list(current))
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack(current, used)
                current.pop()
                used[i] = False
    backtrack([], [False] * len(nums))
    return sorted(result, key=lambda x: (len(x), x))
