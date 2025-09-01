


import heapq
from typing import List

def min_average_turnaround(arrival: List[int], duration: List[int]) -> int:
    """
    Compute floor(average turnaround) on a single non-preemptive machine.

    Turnaround(i) = completion_time(i) - arrival[i]
    Strategy: Shortest-Job-First among jobs that have arrived.
              Use a min-heap keyed by duration to pick the next job.

    Assumptions for this interview:
      - arrival is already sorted ascending.
      - arrival and duration are aligned by index (job i is (arrival[i], duration[i])).
    """

    n = len(arrival)
    if n == 0:
        return 0  # no jobs => average turnaround is 0 by convention

    i = 0                    # pointer over (arrival, duration)
    time = 0                 # current machine time
    total = 0                # sum of all turnaround times
    pq = []                  # min-heap of (duration, arrival) for available jobs

    # Process until all jobs are scheduled (i == n) and heap is empty
    while i < n or pq:
        # If no available jobs, jump time forward to the next arrival
        if not pq and i < n and time < arrival[i]:
            time = arrival[i]  # idle → fast-forward to next job arrival

        # Enqueue every job that has arrived by 'time'
        # Since arrival is sorted, this loop advances 'i' monotonically.
        while i < n and arrival[i] <= time:
            heapq.heappush(pq, (duration[i], arrival[i]))
            i += 1

        # If we have any available job, run the shortest duration next.
        if pq:
            d, a = heapq.heappop(pq)  # pick the job with smallest duration
            time += d                  # advance time by its duration
            total += (time - a)        # add its turnaround = completion - arrival

    # Return the floored average turnaround
    return total // n



def _test():
    print(min_average_turnaround([0, 1, 2], [3, 9, 6]))     # 9
    print(min_average_turnaround([0, 0, 0], [2, 2, 2]))     # 4
    print(min_average_turnaround([5], [7]))                 # 7  (finishes at 12)
    print(min_average_turnaround([0, 10, 20], [10, 1, 1]))  # 4
    print(min_average_turnaround([0, 2, 4], [100, 2, 2]))   # 64 
    
_test()