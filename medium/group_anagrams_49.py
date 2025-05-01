#
# @lc app=leetcode id=49 lang=python3
#
# [49] Group Anagrams
#
from typing import List
from collections import defaultdict
# @lc code=start
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
            # Dictionary to group anagrams
        anagrams = defaultdict(list)
        
        for word in strs:
            # Sort the word to create a signature
            signature = ''.join(sorted(word))
            # Group words with the same signature
            anagrams[signature].append(word)
        
        # Return the grouped anagrams as a list of lists
        return list(anagrams.values())

        
# @lc code=end

