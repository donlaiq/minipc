def solve(arr, k):
    if not arr or k <= 1:
        return arr
    length = len(arr)
    k = k % length
    if k == 0:
        return arr
    
    result = []
    for i in range(0, length, k):
        chunk = arr[i:i+k]
        if len(chunk) == k:
            result.extend(chunk[::-1])
        else:
            result.extend(chunk)
    return result
