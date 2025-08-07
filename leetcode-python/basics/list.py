

# %% 1. Create and Access Lists
my_list = [1, 2, 3, 4, 5]
print(my_list[0])  # Access first element: Output: 1
print(my_list[-1])  # Access last element: Output: 5

# %% Modify Lists
my_list[2] = 10  # Change the third element
print(my_list)  # Output: [1, 2, 10, 4, 5]

# %% Add Elements
my_list.append(6)  # Add to the end
print(my_list)  # Output: [1, 2, 10, 4, 5, 6]

# %% Remove Elements
my_list.pop()  # Remove the last element
print(my_list)  # Output: [1, 2, 10, 4, 5]

# %% 2. Slicing Lists
my_list = [1, 2, 3, 4, 5, 6, 7]
print(my_list[1:4])  # Output: [2, 3, 4]
print(my_list[:3])  # Output: [1, 2, 3]
print(my_list[3:])  # Output: [4, 5, 6, 7]
print(my_list[::2])  # Output: [1, 3, 5, 7]
print(my_list[::-2])
my_list = my_list[::-1]  # Reverse the list
print(my_list)  # Output: [7, 6, 5, 4, 3, 2, 1]
print(my_list[::-1])  # Output: [1, 2, 3, 4, 5, 6, 7]

# %% 3. Basic List Comprehension
squares = [x**2 for x in range(1, 6)]
print(squares)  # Output: [1, 4, 9, 16, 25]

# %% Conditional List Comprehension
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)  # Output: [4, 16, 36, 64, 100]

# %% Nested List Comprehension
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)  # Output: [[1, 2, 3], [2, 4, 6], [3, 6, 9]]


print([ x**3 for x in range(1, 11) ])  # Output: [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
print([ x for x in range(1, 21) if x % 3 == 0 ])  # Output: [3, 6, 9, 12, 15, 18]

# %% 4. List Methods
my_list = [3, 1, 4, 1, 5, 9]

# Append and Extend
my_list.append(2)
print(my_list)  # Output: [3, 1, 4, 1, 5, 9, 2]

my_list.extend([6, 5])
print(my_list)  # Output: [3, 1, 4, 1, 5, 9, 2, 6, 5]

# Insert
my_list.insert(2, 10)  # Insert 10 at index 2
print(my_list)  # Output: [3, 1, 10, 4, 1, 5, 9, 2, 6, 5]

# Remove and Pop
my_list.remove(1)  # Remove the first occurrence of 1
print(my_list)  # Output: [3, 10, 4, 1, 5, 9, 2, 6, 5]

my_list.pop(3)  # Remove the element at index 3
print(my_list)  # Output: [3, 10, 4, 5, 9, 2, 6, 5]

# Sort and Reverse
my_list.sort()
print(my_list)  # Output: [2, 3, 4, 5, 5, 6, 9]

my_list.reverse()
print(my_list)  # Output: [9, 6, 5, 5, 4, 3, 2]

my_list.append(6)  # Add 6 to the end
print(my_list)  # Output: [9, 6, 5, 5, 4, 3, 2, 6]
my_list = [x for x in my_list if x != 6]  # Remove all occurrences of 6
print(my_list)  # Output: [9, 5, 5, 4, 3, 2]

# %% Iterating with a For Loop
my_list = [1, 2, 3, 4, 5]
for num in my_list:
    print(num) # Output: 1 2 3 4 5

# %% Enumerate
for index, value in enumerate(my_list):
    print(f"Index: {index}, Value: {value}") # Output: Index: 0, Value: 1 ... Index: 4, Value: 5

# %% Using List Comprehension for Iteration
squared = [x**2 for x in my_list]
print(squared)  # Output: [1, 4, 9, 16, 25]

# %% 5. Iterating with a For Loop
my_list = [1, 2, 3, 4, 5]
for num in my_list:
    print(num)

# %% Enumerate
for index, value in enumerate(my_list):
    print(f"Index: {index}, Value: {value}")

# %% Using List Comprehension for Iteration
squared = [x**2 for x in my_list]
print(squared)  # Output: [1, 4, 9, 16, 25]
# %%

# %% 6. Zip Two Lists
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
zipped = list(zip(list1, list2))
print(zipped)  # Output: [(1, 'a'), (2, 'b'), (3, 'c')]

# %% Unzip a List of Tuples
# The * operator is used to unpack the zipped list of tuples into individual elements.
unzipped = list(zip(*zipped))
print(unzipped)  # Output: [(1, 2, 3), ('a', 'b', 'c')]

# %% Flatten a Nested List
nested_list = [[1, 2], [3, 4], [5, 6]]
flattened = [item for sublist in nested_list for item in sublist]
print(flattened)  # Output: [1, 2, 3, 4, 5, 6]


# %% 7. Practice Problems 
def second_largest(lst):
    unique = list(set(lst))
    unique.sort()
    return unique[-2]

print(second_largest([1, 2, 3, 4, 5]))  # Output: 4

# %%
def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

print(remove_duplicates([1, 2, 2, 3, 4, 4, 5]))  # Output: [1, 2, 3, 4, 5]


def rotate_list(lst, k):
    k = k % len(lst)
    return lst[-k:] + lst[:-k]

print(rotate_list([1, 2, 3, 4, 5], 2))  # Output: [4, 5, 1, 2, 3]

