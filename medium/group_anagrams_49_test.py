import unittest
from collections import defaultdict
from typing import List
from group_anagrams_49 import Solution  # Adjust the import path as needed

class TestGroupAnagrams(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_group_anagrams(self):
        # Test case 1: Basic example
        input_data = ["eat", "tea", "tan", "ate", "nat", "bat"]
        expected_output = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        result = self.solution.groupAnagrams(input_data)
        self.assertCountEqual(result, expected_output)

    def test_empty_list(self):
        # Test case 2: Empty input
        input_data = []
        expected_output = []
        result = self.solution.groupAnagrams(input_data)
        self.assertEqual(result, expected_output)

    def test_single_word(self):
        # Test case 3: Single word
        input_data = ["word"]
        expected_output = [["word"]]
        result = self.solution.groupAnagrams(input_data)
        self.assertEqual(result, expected_output)

    def test_identical_words(self):
        # Test case 4: Identical words
        input_data = ["aaa", "aaa", "aaa"]
        expected_output = [["aaa", "aaa", "aaa"]]
        result = self.solution.groupAnagrams(input_data)
        self.assertEqual(result, expected_output)

    def test_anagrams_with_repeated_letters(self):
        # Test case 5: Anagrams with repeated letters
        input_data = ["ana", "naa", "aann", "nana", "naan"]
        expected_output = [["ana", "naa"], ["aann", "nana", "naan"]]
        result = self.solution.groupAnagrams(input_data)
        self.assertCountEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()