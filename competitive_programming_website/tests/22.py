def solve(arr):
    if not arr:
        return True
    return arr == arr[::-1]
