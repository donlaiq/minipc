def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i
        max_left_nums1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right_nums1 = float('inf') if i == m else nums1[i]
        max_left_nums2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right_nums2 = float('inf') if j == n else nums2[j]
        if max_left_nums1 <= min_right_nums2 and max_left_nums2 <= min_right_nums1:
            if (m + n) % 2 == 0:
                return (max(max_left_nums1, max_left_nums2) + min(min_right_nums1, min_right_nums2)) / 2
            else:
                return float(max(max_left_nums1, max_left_nums2))
        elif max_left_nums1 > min_right_nums2:
            right = i - 1
        else:
            left = i + 1

def solve(nums1, nums2):
    return findMedianSortedArrays(nums1, nums2)
