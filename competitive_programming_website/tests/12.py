def solve(board):
    rows = [{} for _ in range(9)]
    cols = [{} for _ in range(9)]
    boxes = [{} for _ in range(9)]
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue
            box_index = (r // 3) * 3 + (c // 3)
            if val in rows[r]:
                return False
            rows[r][val] = True
            if val in cols[c]:
                return False
            cols[c][val] = True
            if val in boxes[box_index]:
                return False
            boxes[box_index][val] = True
    return True
