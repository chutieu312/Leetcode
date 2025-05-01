FILTER

1. Filter Even Numbers from a List

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Output: [2, 4, 6, 8, 10]

Explanation: The lambda function checks if a number is divisible by 2. filter() keeps only the even numbers.

2. Remove Empty Strings from a List

strings = ["apple", "", "banana", " ", "cherry", ""]
non_empty_strings = list(filter(lambda x: x.strip() != "", strings))
print(non_empty_strings)  # Output: ['apple', 'banana', 'cherry']

Explanation: The lambda function removes strings that are empty or contain only whitespace.

3. Filter Words Starting with a Specific Letter

words = ["apple", "banana", "cherry", "apricot", "blueberry"]
words_starting_with_a = list(filter(lambda x: x.startswith('a'), words))
print(words_starting_with_a)  # Output: ['apple', 'apricot']

Explanation: The lambda function checks if a word starts with the letter 'a'.

4. Filter Positive Numbers from a List

numbers = [-10, -5, 0, 5, 10, 15]
positive_numbers = list(filter(lambda x: x > 0, numbers))
print(positive_numbers)  # Output: [5, 10, 15]

Explanation: The lambda function keeps only numbers greater than 0.

5. Filter Alphabetic Characters from a String

text = "H3ll0 W0rld!"
alphabetic_chars = ''.join(filter(str.isalpha, text))
print(alphabetic_chars)  # Output: "HllWrld"

Explanation: The str.isalpha method filters out non-alphabetic characters.

6. Filter Palindromes from a List of Words

words = ["level", "world", "radar", "python", "madam"]
palindromes = list(filter(lambda x: x == x[::-1], words))
print(palindromes)  # Output: ['level', 'radar', 'madam']

Explanation: The lambda function checks if a word is the same when reversed.

7. Filter Numbers Divisible by 3

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
divisible_by_3 = list(filter(lambda x: x % 3 == 0, numbers))
print(divisible_by_3)  # Output: [3, 6, 9]

Explanation: The lambda function keeps numbers divisible by 3.

8. Filter Out Non-Digits from a String

text = "Phone: 123-456-7890"
digits = ''.join(filter(str.isdigit, text))
print(digits)  # Output: "1234567890"

Explanation: The str.isdigit method filters out non-digit characters.

9. Filter Names Longer Than 5 Characters

names = ["Alice", "Bob", "Catherine", "David", "Eve"]
long_names = list(filter(lambda x: len(x) > 5, names))
print(long_names)  # Output: ['Catherine']

Explanation: The lambda function keeps names with more than 5 characters.

10. Filter Prime Numbers

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

numbers = range(1, 20)
prime_numbers = list(filter(is_prime, numbers))
print(prime_numbers)  # Output: [2, 3, 5, 7, 11, 13, 17, 19]

Explanation: The is_prime function checks if a number is prime, and filter() keeps only the prime numbers.

11. Filtering Custom Objects

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# List of Person objects
people = [
    Person("Alice", 30),
    Person("Bob", 17),
    Person("Charlie", 25),
    Person("Diana", 15)
]

# Filter to get only adults (age >= 18)
adults = list(filter(lambda p: p.age >= 18, people))

# Print the names of adults
print([p.name for p in adults])  # Output: ['Alice', 'Charlie']





