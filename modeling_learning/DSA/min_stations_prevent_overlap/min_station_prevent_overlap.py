

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
