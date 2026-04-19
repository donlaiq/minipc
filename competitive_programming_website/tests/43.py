def solve(arr, k):
    if not arr or len(arr) <= 1 or k == 0:
        return arr
    length = len(arr)
    k = k % length
    if k == 0:
        return arr
    return arr[-k:] + arr[:-k]
