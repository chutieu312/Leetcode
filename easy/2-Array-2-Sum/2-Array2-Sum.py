


from bisect import bisect_left

def two_array_two_sum(sorted_arr, unsorted_arr):
    n = len(sorted_arr)
    for j, val in enumerate(unsorted_arr):
        target = -val
        # binary search in sorted_arr
        idx = bisect_left(sorted_arr, target)
        if idx < n and sorted_arr[idx] == target:
            return [idx, j]
    return [-1, -1]
# Example usage:
sorted_arr = [-3, -1, 1, 2, 4]
unsorted_arr = [1, 2, 3, 4]
print(two_array_two_sum(sorted_arr, unsorted_arr))


# =================================================================


def binary_search(arr, target):
    """Return index of target in sorted arr, or -1 if not found."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_array_two_sum(sorted_arr, unsorted_arr):
    """
    Find indices [i, j] such that sorted_arr[i] + unsorted_arr[j] == 0.
    Return [-1, -1] if no such pair exists.

    Time:  O(m log n) where n = len(sorted_arr), m = len(unsorted_arr)
    Space: O(1) extra
    """
    for j, val in enumerate(unsorted_arr):
        target = -val
        i = binary_search(sorted_arr, target)
        if i != -1:
            return [i, j]
    return [-1, -1]


# --- Basic tests using the provided examples ---

def run_examples():
    # Example 1
    sorted_arr = [-5, -4, -1, 4, 6, 6, 7]
    unsorted_arr = [-3, 7, 18, 4, 6]
    print("Example 1 Output:", two_array_two_sum(sorted_arr, unsorted_arr))
    # One valid answer is [1, 3] (i.e., -4 + 4 == 0)

    # Example 2
    sorted_arr = [1, 2, 3]
    unsorted_arr = [1, 2, 3]
    print("Example 2 Output:", two_array_two_sum(sorted_arr, unsorted_arr))
    # Expected: [-1, -1]

    # Example 3
    sorted_arr = [-2, 0, 1, 2]
    unsorted_arr = [0, 2, -2, 4]
    print("Example 3 Output:", two_array_two_sum(sorted_arr, unsorted_arr))
    # One valid answer is [0, 1] (i.e., -2 + 2 == 0)


if __name__ == "__main__":
    run_examples()