import unittest
from longest_substring import Solution

class TestLongestSubstring(unittest.TestCase):

    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("abcabcbb"), 3)
        self.assertEqual(self.sol.lengthOfLongestSubstring("bbbbb"), 1)
        self.assertEqual(self.sol.lengthOfLongestSubstring("pwwkew"), 3)

    def test_edge_cases(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring(""), 0)
        self.assertEqual(self.sol.lengthOfLongestSubstring("a"), 1)
        self.assertEqual(self.sol.lengthOfLongestSubstring(" "), 1)
        self.assertEqual(self.sol.lengthOfLongestSubstring("au"), 2)

    def test_special_cases(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("dvdf"), 3)
        self.assertEqual(self.sol.lengthOfLongestSubstring("abba"), 2)
        self.assertEqual(self.sol.lengthOfLongestSubstring("tmmzuxt"), 5)

if __name__ == '__main__':
    unittest.main()