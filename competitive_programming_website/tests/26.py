def solve(nums):
    result = []
    n = len(nums)
    for i in range(1 << n):
        subset = [nums[j] for j in range(n) if i & (1 << j)]
        result.append(subset)
    return result
