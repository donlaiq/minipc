def solve(beginWord, endWord, wordList):
    from collections import deque
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    while queue:
        word, length = queue.popleft()
        if word == endWord:
            return length
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word not in visited and next_word in word_set:
                    if next_word == endWord:
                        return length + 1
                    visited.add(next_word)
                    queue.append((next_word, length + 1))
    return 0
