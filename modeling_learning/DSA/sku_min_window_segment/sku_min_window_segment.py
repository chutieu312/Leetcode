from collections import Counter  # For counting SKUs
from typing import List, Dict, Hashable  # Type hints

def shortest_cover_segment(scans: List[Hashable], required: Dict[Hashable, int]) -> List[int]:
    if not scans or not required:                  # Handle empty input
        return [-1, -1]                            # No valid segment

    need = Counter(required)                       # Required SKU counts
    need_total = len(need)                         # Number of distinct SKUs needed
    have = Counter()                               # Current window SKU counts (only for needed SKUs)
    left = satisfied = 0                           # Left pointer & satisfied count
    best = (-1, -1, float('inf'))                  # (start, end, length) of best window

    for right, sku in enumerate(scans):            # Expand window to the right
        if sku in need:                            # Count only SKUs we need
            have[sku] += 1                         # Add SKU to window
            if have[sku] == need[sku]:             # Just met required count for this SKU
                satisfied += 1                     # Increment satisfied count

        while satisfied == need_total:             # Window meets all requirements
            if right - left + 1 < best[2]:         # Found shorter window
                best = (left, right, right - left + 1)
            left_sku = scans[left]                 # SKU at left boundary
            if left_sku in need:                   # Only adjust counts we track
                have[left_sku] -= 1                # Remove leftmost SKU
                if have[left_sku] < need[left_sku]:# Broke requirement
                    satisfied -= 1                 # Decrement satisfied count
            left += 1                              # Move left pointer right

    return [best[0], best[1]] if best[2] != float('inf') else [-1, -1]  # Return best window or [-1, -1]

def _tests():
    print(shortest_cover_segment(
        ["A","D","B","C","A","B","C","A"],
        {"A":2,"B":1,"C":1}))  # [4, 7]

    print(shortest_cover_segment(
        ["x","y","z"],
        {"x":1,"y":1,"z":1}))  # [0, 2]

    print(shortest_cover_segment(
        ["p","q"],
        {"p":1,"q":2}))        # [-1, -1]

    print(shortest_cover_segment(
        ["a","b","a","b","c"],
        {"a":1,"c":1}))        # [2, 4]  (["a","b","c"])

    print(shortest_cover_segment(
        ["a","a","b","b","c","c"],
        {"a":2,"b":2,"c":2}))  # [0, 5]  (entire array)

_tests()



# BEST SOLUTION
# from collections import Counter  # For counting SKUs
# from typing import List, Dict, Hashable  # Type hints

# def shortest_cover_segment(scans: List[Hashable], required: Dict[Hashable, int]) -> List[int]:
#     if not scans or not required:                  # Handle empty input
#         return [-1, -1]                            # No valid segment

#     need = Counter(required)                       # Required SKU counts
#     need_total = len(need)                         # Distinct required SKUs
#     min_possible = sum(need.values())              # Lower bound on window length (optional)
#     have = Counter()                               # Current window counts (only for needed SKUs)
#     left = satisfied = 0                           # Left pointer & satisfied distinct count
#     best = (-1, -1, float('inf'))                  # (start, end, length) of best window

#     for right, sku in enumerate(scans):            # Expand window to the right
#         if sku in need:                            # Count only SKUs we need
#             have[sku] += 1                         # Add SKU to window
#             if have[sku] == need[sku]:             # Just met required count for this SKU
#                 satisfied += 1                     # Increment satisfied count

#         while satisfied == need_total:             # Window meets all requirements
#             curr_len = right - left + 1
#             if curr_len < best[2]:                 # Found shorter window
#                 best = (left, right, curr_len)
#                 if best[2] == min_possible:        # Can't beat the lower bound (optional)
#                     return [best[0], best[1]]

#             left_sku = scans[left]                 # SKU at left boundary
#             if left_sku in need:                   # Only touch counts we track
#                 have[left_sku] -= 1                # Remove leftmost needed SKU
#                 if have[left_sku] < need[left_sku]:# Broke requirement
#                     satisfied -= 1                 # Decrement satisfied count
#             left += 1                              # Move left pointer right

#     return [best[0], best[1]] if best[2] != float('inf') else [-1, -1]  # Best window or none
