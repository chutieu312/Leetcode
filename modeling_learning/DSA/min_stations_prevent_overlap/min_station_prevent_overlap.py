

import heapq
from typing import List

def min_stations(intervals: List[List[int]]) -> int:
    if not intervals: return 0                              # No bookings → no stations

    heap: List[int] = []                                    # Min-heap of end times
    max_stations = 0                                        # Peak concurrent usage

    for start, end in intervals:                            # Process bookings (already sorted)
        while heap and heap[0] <= start:                    # Free all stations that ended
            heapq.heappop(heap)
        heapq.heappush(heap, end)                           # Occupy a station with this booking
        max_stations = max(max_stations, len(heap))         # Track peak usage

    return max_stations                                     # Minimum stations required


def _test():
    print(min_stations([[0,30],[5,10],[15,20]]))         # 2
    print(min_stations([[7,10],[10,12]]))                # 1
    print(min_stations([[0,5],[0,6],[0,7],[8,9]]))       # 3
    print(min_stations([[0,10],[10,20],[20,30]]))        # 1
    print(min_stations([[1,3],[2,4],[3,5],[4,6]]))       # 2
    print(min_stations([]))                               # 0
    
    
_test()


from typing import List

def subarray_sum(nums: List[int], k: int) -> int:
    prefix_count = {0: 1}                               # prefix value -> frequency; empty prefix sum 0 seen once
    total = 0                                           # running prefix sum
    count = 0                                           # number of valid subarrays

    for x in nums:                                      # scan each element
        total += x                                      # extend prefix sum
        need = total - k                                # we need a previous prefix equal to (total - k)
        if need in prefix_count:                        # if such a prefix was seen
            count += prefix_count[need]                 # add its frequency
        prefix_count[total] = prefix_count.get(total, 0) + 1  # record current prefix sum

    return count                                        # total subarrays summing to k
