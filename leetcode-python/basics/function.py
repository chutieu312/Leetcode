# %% 1 Define and Call a Function
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Output: Hello, Alice!

# Function with Default Arguments
def greet_with_default(name="World"):
    return f"Hello, {name}!"

print(greet_with_default())  # Output: Hello, World!
print(greet_with_default("Bob"))  # Output: Hello, Bob


# %% Lambda Functions
square = lambda x: x**2
print(square(5))  # Output: 25

# Lambda with Multiple Arguments
add = lambda x, y: x + y
print(add(3, 4))  # Output: 7


# %% Using map() to Apply a Function to a List
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, nums))
print(squared)  # Output: [1, 4, 9, 16, 25]


# %% Using filter() to Filter a List
nums = [1, 2, 3, 4, 5]
even_nums = list(filter(lambda x: x % 2 == 0, nums))
print(even_nums)  # Output: [2, 4]


from functools import reduce

# %% Using reduce() to Compute a Sum
nums = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, nums)
print(total)  # Output: 15

# Using reduce() to Compute a Product
product = reduce(lambda x, y: x * y, nums)
print(product)  # Output: 120


# %% Reusable Function to Calculate Factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # Output: 120

# Reusable Function to Check if a Number is Prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(7))  # Output: True
print(is_prime(10))  # Output: False




# 7. Practice Problems (15 Minutes)
# %% Filter Even Numbers from a List
# Given a list of numbers, return a new list containing only the even numbers.
def filter_even(nums):
    return list(filter(lambda x: x % 2 == 0, nums))

print(filter_even([1, 2, 3, 4, 5, 6]))  # Output: [2, 4, 6]

# %% Map to Square Numbers
# Given a list of numbers, return a new list containing the squares of the numbers.
def square_numbers(nums):
    return list(map(lambda x: x**2, nums))

print(square_numbers([1, 2, 3, 4, 5]))  # Output: [1, 4, 9, 16, 25]

# %% Find the product of a List
# Given a list of numbers, return the product of all the numbers.
def product_of_list(nums):
    return reduce(lambda x, y: x * y, nums)

print(product_of_list([1, 2, 3, 4]))  # Output: 24


# %% N-Queens
def solve_n_queens(n):
    results = []
    board = [['.'] * n for _ in range(n)]
    def is_valid(row, col):
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        # Check diagonal /
        for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
            if board[i][j] == 'Q':
                return False
        # Check diagonal \
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i][j] == 'Q':
                return False
        return True
    def backtrack(row):
        if row == n:
            # Found a valid solution
            results.append([''.join(r) for r in board])
            return
        for col in range(n):
            if is_valid(row, col):
                # Place queen
                board[row][col] = 'Q'
                # Backtracking step: move to next row
                backtrack(row + 1)
                # Undo the choice (backtrack)
                board[row][col] = '.'
    backtrack(0)
    return results

print(solve_n_queens(4))
# Output: All valid board arrangements for 4-Queens
# %%
