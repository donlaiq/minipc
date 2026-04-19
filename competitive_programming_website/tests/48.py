def solve(numRows, s):
    if numRows == 1 or numRows >= len(s):
        return s
    rows = [''] * numRows
    cur = 0
    going_down = False
    for ch in s:
        rows[cur] += ch
        if cur == 0 or cur == numRows - 1:
            going_down = not going_down
        cur += 1 if going_down else -1
    return ''.join(rows)
