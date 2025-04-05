import math

# Basic Input/Output
name = input("Enter your name: ")  # Input
print(f"Hello, {name}!")           # Output

# Variables and Data Types
x = 5               # Integer
y = 3.14            # Float
z = "Hello"         # String
is_valid = True     # Boolean
nums = [1, 2, 3]    # List
info = {"key": "value"}  # Dictionary

# Loops
for i in range(5):  # For loop
    print(i)  # Output: 0, 1, 2, 3, 4

while x > 0:        # While loop
    print(x)  # Output: 5, 4, 3, 2, 1
    x -= 1

# Conditionals
if x > y:
    print("x is greater")  # Output: (depends on x and y values)
elif x == y:
    print("x equals y")    # Output: (depends on x and y values)
else:
    print("x is smaller")  # Output: (depends on x and y values)

# Functions
def add(a, b):
    return a + b

result = add(2, 3)
# print(result)  # Output: 5

# String Manipulation
s = "leetcode"
# print(s[::-1])  # Output: "edocteel" (Reverse string)
# print(s.upper())  # Output: "LEETCODE" (Uppercase)

# List Operations
nums.append(4)  # Add element
nums.pop()      # Remove last element
nums.sort()     # Sort list

# Dictionary Operations
info["new_key"] = "new_value"  # Add key-value pair
del info["key"]               # Delete key-value pair

# List Comprehension
squares = [i * i for i in range(5)]
# print(squares)  # Output: [0, 1, 4, 9, 16]

# Set Operations
unique = set([1, 2, 2, 3])  # Remove duplicates
# print(unique)  # Output: {1, 2, 3}

# Tuples
t = (1, 2, 3)  # Immutable list
# print(t)  # Output: (1, 2, 3)

# Enumerate
names = ["Alice", "Bob", "Charlie"]
for index, name in enumerate(names):
    print(f"{index}: {name}")  # Using f-string: Output: 0: Alice, 1: Bob, 2: Charlie

# Without using f-string
for index, name in enumerate(names):
    print("{}: {}".format(index, name))  # Using str.format(): Output: 0: Alice, 1: Bob, 2: Charlie

# Zip
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
zipped = zip(list1, list2)
for item in zipped:
    print(item)  # Output: (1, 'a'), (2, 'b'), (3, 'c')

# Classes
class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

# Exception Handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")  # Output: "Cannot divide by zero"

# Importing Modules
# print(math.sqrt(16))  # Output: 4.0

# Algorithms
# Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1




# Recursion
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Sorting
arr = [3, 1, 4, 1, 5]
arr.sort()  # In-place sort
# print(arr)  # Output: [1, 1, 3, 4, 5]
sorted_arr = sorted(arr)  # Returns a new sorted list
# print(sorted_arr)  # Output: [1, 1, 3, 4, 5]