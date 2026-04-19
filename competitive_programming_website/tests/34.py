class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i, num in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + num
    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]

def solve(nums):
    result = NumArray(nums)
    return str(type(result).__name__)
