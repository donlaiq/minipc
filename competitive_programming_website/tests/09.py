def solve(s):
    if not s or len(s) < 1:
        return ""
    start = 0
    max_len = 0
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1
    for i in range(len(s)):
        l1, r1 = expand_around_center(i, i)
        l2, r2 = expand_around_center(i, i + 1)
        if r1 > max_len:
            start, max_len = l1, r1
        if r2 > max_len:
            start, max_len = l2, r2
    return s[start: start + max_len]
