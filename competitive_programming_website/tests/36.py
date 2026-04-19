def solve(nums):
    if len(nums) < 2:
        return 0
    min_val, max_val = min(nums), max(nums)
    if min_val == max_val:
        return 0
    gap = max(1, (max_val - min_val) // (len(nums) - 1))
    size = (max_val - min_val) // gap + 1
    buckets = [[None, None] for _ in range(size)]
    for num in nums:
        idx = (num - min_val) // gap
        if buckets[idx][0] is None:
            buckets[idx][0] = buckets[idx][1] = num
        else:
            buckets[idx][0] = min(buckets[idx][0], num)
            buckets[idx][1] = max(buckets[idx][1], num)
    max_gap = 0
    prev_max = min_val
    for i in range(size):
        if buckets[i][0] is None:
            continue
        max_gap = max(max_gap, buckets[i][0] - prev_max)
        prev_max = buckets[i][1]
    return max_gap
