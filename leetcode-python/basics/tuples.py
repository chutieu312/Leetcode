# %% 1 Create and Access Tuples
my_tuple = (1, 2, 3, 4, 5)
print(my_tuple)  # Output: (1, 2, 3, 4, 5)

# Access Elements
print(my_tuple[0])  # Output: 1
print(my_tuple[-1])  # Output: 5

# Tuples Can Contain Mixed Data Types
mixed_tuple = (1, "hello", 3.14)
print(mixed_tuple)  # Output: (1, 'hello', 3.14)

# Tuples Can Contain Duplicates
duplicate_tuple = (1, 2, 2, 3)
print(duplicate_tuple)  # Output: (1, 2, 2, 3)

# %% 2 Tuples Are Immutable
my_tuple = (1, 2, 3)

# Attempting to Modify a Tuple Will Raise an Error
# my_tuple[0] = 10  # Uncommenting this will raise a TypeError

# However, You Can Reassign the Entire Tuple
my_tuple = (4, 5, 6)
print(my_tuple)  # Output: (4, 5, 6)

# %% 3 Common Tuple Methods
my_tuple = (1, 2, 3, 2, 4, 2)

# Count the Occurrences of an Element
print(my_tuple.count(2))  # Output: 3

# Find the Index of an Element
print(my_tuple.index(3))  # Output: 2

# %% 4 Iterating Over a Tuple
my_tuple = (1, 2, 3, 4, 5)

for item in my_tuple:
    print(item)  # Output: 1 2 3 4 5
    
    
# %% 5 Tuple Packing
packed_tuple = 1, 2, 3
print(packed_tuple)  # Output: (1, 2, 3)

# Tuple Unpacking
a, b, c = packed_tuple
print(a, b, c)  # Output: 1 2 3

# Unpacking with *
my_tuple = (1, 2, 3, 4, 5)
a, *b, c = my_tuple
print(a)  # Output: 1
print(b)  # Output: [2, 3, 4]
print(c)  # Output: 5

# %% 6 Nested Tuples
nested_tuple = ((1, 2), (3, 4), (5, 6))
print(nested_tuple[0])  # Output: (1, 2)
print(nested_tuple[0][1])  # Output: 2


# 7. Practice Problems (15 Minutes)
# %% 1 Swap Two Variables
# Swapping Variables
a, b = 5, 10
a, b = b, a
print(a, b)  # Output: 10 5

# %% Return Multiple Values
# Write a function that returns multiple values as a tuple.
def min_max(lst):
    return min(lst), max(lst)

print(min_max([1, 2, 3, 4, 5]))  # Output: (1, 5)

# %% 3 Sort a List of Tuples
# Given a list of tuples, sort them based on the second element of each tuple.
def sort_tuples(lst):
    return sorted(lst, key=lambda x: x[1])

print(sort_tuples([(1, 3), (2, 2), (3, 1)]))  # Output: [(3, 1), (2, 2), (1, 3)]

