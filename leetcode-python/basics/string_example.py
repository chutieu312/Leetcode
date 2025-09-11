# %% 1 String Basics
my_string = "Hello, World!"
print(my_string[0])  # Output: H (first character)
print(my_string[-1])  # Output: ! (last character)

# Slicing
print(my_string[0:5])  # Output: Hello (substring from index 0 to 4)
print(my_string[:5])  # Output: Hello (start to index 4)
print(my_string[7:])  # Output: World! (index 7 to end)
print(my_string[::-1])  # Output: !dlroW ,olleH (reversed string)

# %% 2 join()
words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(sentence)  # Output: Python is awesome

# %% split()
sentence = "Python is awesome"
words = sentence.split()
print(words)  # Output: ['Python', 'is', 'awesome']

# %% replace()
text = "I love Python"
new_text = text.replace("Python", "coding")
print(new_text)  # Output: I love coding

import re

# %% 3 Match a Pattern
text = "The rain in Spain"
match = re.search(r"rain", text)
print(match.group())  # Output: rain

# %% Find All Matches
text = "The rain in Spain falls mainly in the plain"
matches = re.findall(r"in", text)
print(matches)  # Output: ['in', 'in', 'in', 'in']

# %% Replace Using Regular Expressions
text = "The rain in Spain"
new_text = re.sub(r"rain", "snow", text)
print(new_text)  # Output: The snow in Spain

# %% Extract Digits
text = "My phone number is 123-456-7890"
digits = re.findall(r"\d+", text)
print(digits)  # Output: ['123', '456', '7890']


#4. Practice Problems (15 Minutes)
# %%  Palindrome Check 
# Given a string, check if it is a palindrome (reads the same forwards and backwards).
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("A man a plan a canal Panama"))  # Output: True


# %% 2 Count Vowels
# Given a string, count the number of vowels (a, e, i, o, u).
def count_vowels(s):
    return len([char for char in s.lower() if char in "aeiou"])

print(count_vowels("Hello, World!"))  # Output: 3


# %%  3: Extract Hashtags 
# Given a string, extract all hashtags (words starting with #).
def extract_hashtags(s):
    return re.findall(r"#\w+", s)

print(extract_hashtags("I love #Python and #coding"))  # Output: ['#Python', '#coding']

