import unittest

from two_sum import Solution  # Import the Solution class

class TestTwoSum(unittest.TestCase):

    def test_example_case(self):
        self.assertEqual(sorted(Solution().twoSum([2, 7, 11, 15], 9)), [0, 1])

    def test_multiple_answers(self):
        self.assertEqual(sorted(Solution().twoSum([3, 2, 4], 6)), [1, 2])

    def test_same_number_twice(self):
        self.assertEqual(sorted(Solution().twoSum([3, 3], 6)), [0, 1])

    def test_negative_numbers(self):
        self.assertEqual(sorted(Solution().twoSum([-1, -2, -3, -4, -5], -8)), [2, 4])

    def test_large_input(self):
        nums = list(range(1000000))
        target = 1999997
        self.assertEqual(sorted(Solution().twoSum(nums, target)), [999998, 999999])

if __name__ == '__main__':
    unittest.main()