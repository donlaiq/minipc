from collections import defaultdict

def solve(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    result = list(groups.values())
    # Sort by the last occurrence of any element in the original list (descending)
    def last_idx(g):
        return max(strs.index(x) for x in g)
    result.sort(key=last_idx, reverse=True)
    return result
