def solve(nums):
    result = []
    nums.sort()
    def backtrack(current, used):
        if len(current) == len(nums):
            result.append(list(current))
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            current.append(nums[i])
            backtrack(current, used)
            current.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
