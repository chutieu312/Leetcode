# %% 1 Create and Access Sets
my_set = {1, 2, 3, 4, 5}
print(my_set)  # Output: {1, 2, 3, 4, 5}

# Add Elements
my_set.add(6)
print(my_set)  # Output: {1, 2, 3, 4, 5, 6}

# Remove Elements
my_set.remove(3)  # Removes 3 from the set
print(my_set)  # Output: {1, 2, 4, 5, 6}

# Check Membership
print(4 in my_set)  # Output: True
print(10 in my_set)  # Output: False

# %% 2 Union, Intersection, Difference, and Symmetric Difference
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

# Union
print(set1 | set2)  # Output: {1, 2, 3, 4, 5, 6}

# Intersection
print(set1 & set2)  # Output: {3, 4}

# Difference
print(set1 - set2)  # Output: {1, 2}

# Symmetric Difference
print(set1 ^ set2)  # Output: {1, 2, 5, 6}

# %% 3 Common Set Methods
my_set = {1, 2, 3}

# Add Elements
my_set.add(4)
print(my_set)  # Output: {1, 2, 3, 4}

# Update with Multiple Elements
my_set.update([5, 6])
print(my_set)  # Output: {1, 2, 3, 4, 5, 6}

# Remove Elements
my_set.discard(2)  # Removes 2 if it exists
print(my_set)  # Output: {1, 3, 4, 5, 6}

# Clear the Set
my_set.clear()
print(my_set)  # Output: set()

# %% 4 Iterating Over a Set
my_set = {1, 2, 3, 4, 5}

for item in my_set:
    print(item)  # Output: 1 2 3 4 5 (order may vary)
    
    
# %% 5 Create a Set Using Comprehension
squared_set = {x**2 for x in range(1, 6)}
print(squared_set)  # Output: {1, 4, 9, 16, 25}

# Filter a Set
filtered_set = {x for x in range(10) if x % 2 == 0}
print(filtered_set)  # Output: {0, 2, 4, 6, 8}

# %% 6 Subset and Superset
set1 = {1, 2, 3}
set2 = {1, 2, 3, 4, 5}

# Check if set1 is a subset of set2
print(set1.issubset(set2))  # Output: True

# Check if set2 is a superset of set1
print(set2.issuperset(set1))  # Output: True

# Check if two sets are disjoint
set3 = {6, 7, 8}
print(set1.isdisjoint(set3))  # Output: True


# 7 Practice Problems (15 Minutes)
# %% 1 Remove Duplicates from a List
# Given a list, remove duplicates and return a new list.
def remove_duplicates(lst):
    return list(set(lst))

print(remove_duplicates([1, 2, 2, 3, 4, 4, 5]))  # Output: [1, 2, 3, 4, 5]

# %% 2 Find the Intersection of Two Sets
# Given two lists, return a list of common elements.
def find_common(lst1, lst2):
    return list(set(lst1) & set(lst2))

print(find_common([1, 2, 3], [2, 3, 4]))  # Output: [2, 3]

# %% 3 Find the Union of Two Sets
# Given two lists, return a list of all unique elements.
def find_unique(lst1, lst2):
    return list(set(lst1) ^ set(lst2))

print(find_unique([1, 2, 3], [2, 3, 4]))  # Output: [1, 4]