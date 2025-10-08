#
# @lc app=leetcode id=1 lang=python3
#
# [1] Two Sum
#
# @lc code=start
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        index = 0
        remain = {}
        return_list = []
        
        for num in nums: 
            if num in remain:
                return_list.append(remain[num])
                return_list.append(index)
                return return_list
            else:
                remain[target - num] = index
            index += 1
            
# @lc code=end

