
# %%  
def arrayManipulation1(n, queries):
    # Write your code here
    
    arr = [0] * (n +2)
    max_value = 0
    
    for a, b, k in queries:
        for i in range(a, b + 1):
            arr[i] += k
            if arr[i] > max_value:
                max_value = arr[i]
            
    return max_value

# %% 
def arrayManipulation2(n, queries):
    # Write your code here
    
    # def interval_overlap(a, b):
    #     # a and b are intervals like [start, end]
    #     start = max(a[0], b[0])
    #     end = min(a[1], b[1])
    #     if start <= end:
    #         return [start, end]  # Overlap exists
    #     else:
    #         return None  
    
    
    # queries.sort(key=lambda x: (x[0], x[1]))
    
    # max_value = queries[0][2]
    # max_interval = [queries[0][0],queries[0][1]]
    
    # overlap_interval = max_interval
    # overlap_value = max_value
    # prev_interval = max_interval
    # prev_value = max_value
    
    # for a, b, k in queries[1:]:
    #     overlap_interval = interval_overlap(overlap_interval, [a,b])
        
    #     if overlap_interval:
    #         overlap_value += k
    #         max_value = max(max_value, overlap_value)
    #         prev_interval =  [a,b]
    #     elif interval_overlap(prev_interval, [a,b]):
    #         prev_value += k
    #         overlap_interval = interval_overlap(prev_interval, [a,b])
    #         prev_interval =  [a,b]
    #         max_value = max(max_value, overlap_value, prev_value)
            
    #     else:   
    #         prev_value = k
    #         max_value = max(max_value, overlap_value, prev_value)
    #         prev_interval = [a, b]
            
    # print(f"max value: {max_value}")
            
    # return max_value
    
    arr = [0] * (n + 2)

    for a, b, k in queries:
        arr[a] += k
        arr[b + 1] -= k

    max_val = 0
    current = 0
    for val in arr:
        current += val
        max_val = max(max_val, current)

    return max_val
    
    
n = 40
queries = [
    [29, 40, 787],
    [9, 26, 219],
    [21, 31, 214],
    [8, 22, 719],
    [15, 23, 102],
    [11, 24, 83],
    [14, 22, 321],
    [5, 22, 300],
    [11, 30, 832],
    [5, 25, 29],
    [16, 24, 577],
    [3, 10, 905],
    [15, 22, 335],
    [29, 35, 254],
    [9, 20, 20],
    [33, 34, 351],
    [30, 38, 564],
    [11, 31, 969],
    [3, 32, 11],
    [29, 35, 267],
    [4, 24, 531],
    [1, 38, 892],
    [12, 18, 825],
    [25, 32, 99],
    [3, 39, 107],
    [12, 37, 131],
    [3, 26, 640],
    [8, 39, 483],
    [8, 11, 194],
    [12, 37, 502]
]

# queries.sort(key=lambda x: (x[0], x[1]))
# for query in queries:
#     print(query)
#     print("\n")



result2 = arrayManipulation2(n, queries)
print("Result2:", result2)

result1 = arrayManipulation1(n, queries)
print("Result1:", result1)
    
# correct result is 8628

# %%
