def solve(s):
    if not s:
        return 0
    char_index = {}
    start = 0
    max_len = 0
    for end, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= start:
            start = char_index[ch] + 1
        char_index[ch] = end
        max_len = max(max_len, end - start + 1)
    return max_len
