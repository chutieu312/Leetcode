
# %% 1. Basics of Dictionaries (5 Minutes)
# Create and Access Dictionaries
my_dict = {"a": 1, "b": 2, "c": 3}
print(my_dict["a"])  # Access value by key: Output: 1

# Add or Update Key-Value Pairs
my_dict["d"] = 4  # Add a new key-value pair
my_dict["a"] = 10  # Update an existing key
print(my_dict)  # Output: {'a': 10, 'b': 2, 'c': 3, 'd': 4}

# Check if a Key Exists
print("a" in my_dict)  # Output: True
print("z" in my_dict)  # Output: False



# %% 2. Dictionary Methods (10 Minutes)
# Common Dictionary Methods
my_dict = {"a": 1, "b": 2, "c": 3}

# Get Keys, Values, and Items
print(my_dict.keys())  # Output: dict_keys(['a', 'b', 'c'])
print(my_dict.values())  # Output: dict_values([1, 2, 3])
print(my_dict.items())  # Output: dict_items([('a', 1), ('b', 2), ('c', 3)])

# Remove a Key
my_dict.pop("b")  # Removes key 'b' and returns its value
print(my_dict)  # Output: {'a': 1, 'c': 3}

# Get a Value with Default
print(my_dict.get("a", 0))  # Output: 1
print(my_dict.get("z", 0))  # Output: 0

# Clear the Dictionary
my_dict.clear()
print(my_dict)  # Output: {}



# %% 3. Iterating Over Dictionaries (10 Minutes)
my_dict = {"a": 1, "b": 2, "c": 3}

# Iterate Over Keys
for key in my_dict:
    print(key)  # Output: a, b, c

# Iterate Over Values
for value in my_dict.values():
    print(value)  # Output: 1, 2, 3

# Iterate Over Key-Value Pairs
for key, value in my_dict.items():
    print(f"{key}: {value}")  # Output: a: 1, b: 2, c: 3



# %% 4. Dictionary Comprehensions (10 Minutes)
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter a Dictionary
filtered_dict = {k: v for k, v in squares.items() if v > 10}
print(filtered_dict)  # Output: {4: 16, 5: 25}



# %% 5. Advanced Dictionary Operations (10 Minutes)
# Merge Two Dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged_dict = {**dict1, **dict2}  # Python 3.9+: dict1 | dict2
print(merged_dict)  # Output: {'a': 1, 'b': 3, 'c': 4}

# Use defaultdict
from collections import defaultdict
dd = defaultdict(list)
dd["a"].append(1)
dd["a"].append(2)
print(dd)  # Output: defaultdict(<class 'list'>, {'a': [1, 2]})

# Use Counter
from collections import Counter
counter = Counter("aabbcc")
print(counter)  # Output: Counter({'a': 2, 'b': 2, 'c': 2})

# 6. Practice Problems (15 Minutes)
# Problem 1: Count Word Frequencies
# Given a list of words, count the frequency of each word and return a dictionary.
# %%
def count_words(words):
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

print(count_words(["apple", "banana", "apple", "orange", "banana", "apple"]))
# Output: {'apple': 3, 'banana': 2, 'orange': 1}

# Problem 2: Group Anagrams
# Write a function to group anagrams together.
# %%
from collections import defaultdict

def group_anagrams(words):
    anagrams = defaultdict(list)
    for word in words:
        signature = ''.join(sorted(word))
        anagrams[signature].append(word)
    return list(anagrams.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

# Problem 3: Invert a Dictionary
# Write a function to invert a dictionary (swap keys and values).
# %%
def invert_dict(d):
    return {v: k for k, v in d.items()}

print(invert_dict({"a": 1, "b": 2, "c": 3}))
# Output: {1: 'a', 2: 'b', 3: 'c'}
