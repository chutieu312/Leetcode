#
# @lc app=leetcode id=3 lang=python3
#
# [3] Longest Substring Without Repeating Characters
#

# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = [-1] * 128
        start = max_len = 0

        for i in range(len(s)):
            ch = ord(s[i])
            if last_seen[ch] >= start:
                start = last_seen[ch] + 1
            last_seen[ch] = i
            max_len = max(max_len, i - start + 1)

        return max_len
    
    
# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         currSub = []
#         maxSub = [s[0]] if s else []
#         left = 0
#         right = 1
#         currSub = list(s[left:right])
#         # maxSub = max(maxSub, currSub, key=len)
        
#         while right < len(s):
#             if s[right ] in currSub:
#                 for i in range(len(currSub)):
#                     if currSub[i] == s[right]:
#                         left += i + 1
#                         break
#                 right += 1
#                 currSub = list(s[left:right])
                
#             else:
#                 currSub.append(s[right])
#                 maxSub = max(maxSub, currSub, key=len)
#                 right += 1
                
#         return len(maxSub)






        
# @lc code=end
