# Parity Sorting

Hello\! Your interview question is below. \# Parity Sorting Given an array of integers `arr`, modify it in place so that all even numbers come before all odd numbers. The relative order of even numbers does not need to be maintained. The same goes for odd numbers. Example 1: Input: arr \= \[1, 2, 3, 4, 5\] Output: \[2, 4, 1, 3, 5\] Explanation: There are other valid outputs, e.g. \[4, 2, 3, 1, 5\]. Example 2: Input: arr \= \[5, 1, 3, 1, 5\] Output: \[5, 1, 3, 1, 5\] Explanation: Since all numbers are odd, any ordering is valid. Example 3: Input: arr \= \[1, 3, 2, 4\] Output: \[2, 4, 1, 3\] Explanation: Any arrangement where the even numbers (2, 4\) come before the odd numbers (1, 3\) is valid. Constraints: \- The length of arr is at most 10^6 \- Each element in arr is an integer in the range \[-10^9, 10^9\]

###### **ChatGPT said:**

Great — thanks for the question\! Let me think this through step by step as if I were in a real interview.

---

## **🧠 Clarifying the Problem**

* We are given an integer array `arr`.

* Goal: rearrange it **in place** so that all even numbers come before odd numbers.

* Relative order doesn’t matter, so we don’t need a stable partition.

* Constraints: up to **10^6 elements** → O(n log n) might be acceptable, but ideally O(n).

* Values can be negative, but parity (even vs odd) is well-defined for negative numbers as well.

---

## **🐢 Brute Force Approach (and why it’s not ideal)**

* One brute force idea:

  * Create a new array.

  * First append all evens, then append all odds.

* Complexity: O(n) time, but O(n) extra space.

* Since the problem requires **in-place modification**, this isn’t acceptable.

---

## **⚡ Optimized Approach**

This is basically a **partition problem** (like the partition step in QuickSort).

* Use **two pointers**:

  * `left` starting at 0\.

  * `right` starting at n-1.

* While `left < right`:

  * If `arr[left]` is even → already in place, move `left++`.

  * If `arr[right]` is odd → already in place, move `right--`.

  * If `arr[left]` is odd and `arr[right]` is even → swap them.

* This guarantees evens are pushed to the left, odds to the right.

Complexity:

* **Time:** O(n), since each element is checked at most once.

* **Space:** O(1), since we swap in place.

---

## **✍️ Example Walkthrough**

Input: `[1, 2, 3, 4, 5]`

* left=0 (odd), right=4 (odd) → right--

* left=0 (odd), right=3 (even) → swap → `[4, 2, 3, 1, 5]`

* left=1 (even) → left++

* left=2 (odd), right=3 (odd) → right--  
   → Final: `[4, 2, 3, 1, 5]` ✅

---

## **📝 Code (Python)**
```
`def parity_sort(arr):`  
    `left, right = 0, len(arr) - 1`  
    `while left < right:`  
        `if arr[left] % 2 == 0:`  
            `left += 1`  
        `elif arr[right] % 2 == 1:`  
            `right -= 1`  
        `else:`  
            `arr[left], arr[right] = arr[right], arr[left]`  
            `left += 1`  
            `right -= 1`  
    `return arr`
```

---

## **⏱️ Complexity Analysis**

* **Time Complexity:** O(n)

* **Space Complexity:** O(1)

---

✅ This solution is **optimal** for the constraints: linear time, constant space, and works for up to 10^6 elements.

---

👉 Before I wrap up, I’d ask you (the interviewer):  
 Would you like me to also discuss an alternative **stable version** (where the relative order of evens and odds is preserved) — even though it’s not required here?

Would you like me to continue down that path, or is the in-place partition solution sufficient?

##### **You said:**

Interviewer: That's a fantastic analysis\! I love how you broke down the problem systematically and walked through your reasoning step by step. Your two-pointer approach is spot on, and I can see you really understand the partition logic behind it. Your example walkthrough was particularly helpful \- it shows you're thinking through the mechanics of how the algorithm actually works in practice. I noticed you mentioned this is similar to the partition step in QuickSort. Can you tell me a bit more about what you mean by that connection?

###### **ChatGPT said:**

Candidate:  
 Great question — let me expand on that.

In **QuickSort**, the key step is the **partition**:

* You choose a pivot value.

* Then you rearrange the array so that all elements **less than the pivot** are moved to the left, and all elements **greater than or equal to the pivot** are moved to the right.

* This is often done with a **two-pointer technique**: one scanning from the left, one from the right, swapping elements that are on the wrong side of the pivot.

👉 In our parity-sorting problem, the **pivot condition** isn’t `< pivot`, it’s **“is this number even?”**.

* "Even" values correspond to the "less than pivot" group.

* "Odd" values correspond to the "greater than pivot" group.

* Just like QuickSort’s partition, we don’t care about the internal relative order of elements in each partition — we only care that the groups are separated.

So conceptually, what we’ve done here is:

* Treat “even” as one partition and “odd” as the other.

* Apply a QuickSort-style partition step.

* But unlike QuickSort, we don’t need recursion afterward — once partitioned, the problem is solved.

This connection is powerful because it shows a general **pattern**:

“Group items into two buckets based on a predicate, using two pointers in O(n) time and O(1) space.”

That’s exactly what QuickSort partitioning and our parity sort both do.

---

👉 Would you like me to also describe how this idea extends beyond evens/odds — for example, how we could generalize it to group **negatives vs non-negatives**, or **0/1 arrays**, or even “three-way partitioning” (like Dutch National Flag problem)?

##### **You said:**

interviewer: Excellent connection\! You've really nailed the conceptual similarity there. The way you explained how the "even/odd" predicate maps to the "less than/greater than pivot" logic in QuickSort shows deep understanding of the underlying pattern. I like how you recognized this as a general technique for binary partitioning problems. That kind of pattern recognition is really valuable in interviews. Now, looking at your code, it looks solid to me. Before we wrap up, can you walk me through how you'd test this solution? What are some edge cases you'd want to make sure your implementation handles correctly?

###### **ChatGPT said:**

Thought for 9s

Candidate:  
 Absolutely—here’s how I’d test it to build confidence the solution is correct, robust, and efficient.

## **🧪 Test Strategy**

### **1\) Happy-path / Representative cases**

* **Mixed small array:** `[1,2,3,4,5]` → result has all evens before odds (e.g., `[2,4,1,3,5]`).

* **Alternating parity:** `[1,2,1,2,1,2]` → evens first, odds after.

* **Already partitioned:** `[2,4,6,1,3,5]` → remains a valid partition (order within groups irrelevant).

### **2\) Edge cases**

* **Empty array:** `[]` → stays `[]`.

* **Single element:** `[0]` (even), `[1]` (odd).

* **All evens:** `[2,4,6,8]` → unchanged (still valid).

* **All odds:** `[5,3,7]` → unchanged (still valid).

* **Negatives and zero:** `[-2, -1, 0, 3, 4]` → evens (`-2, 0, 4`) before odds (`-1, 3`).

  * Sanity check: in Python, `x % 2 == 0` correctly identifies even numbers even when `x` is negative.

* **Duplicates:** `[2,2,1,1,4,4,3,3]` → evens first, odds later.

### **3\) Correctness properties (invariant checks)**

After running `parity_sort(arr)`:

* **Partition property:** Every even index region is even, every odd-side region is odd.  
   Practically: once you hit the first odd at index `k`, **no even should appear after** `k`.

* **Multiset preservation:** The output is a **permutation** of the input (same counts of each value).

* **In-place mutation:** Memory usage stays O(1); the function doesn’t allocate proportional to `n`.

### **4\) Oracle-based / Fuzz testing**

* **Reference oracle:** `expected = sorted(arr_copy, key=lambda x: x % 2)`  
   Then run my in-place function and assert both arrays are **parity-equivalent** (not necessarily same internal order, but all evens are before odds).

* **Randomized tests:** Generate many random arrays (varying sizes, including up to large sizes), compare against the oracle property above.

### **5\) Performance & scale**

* **Large input stress:** `n = 10^6` with random ints in `[-1e9, 1e9]`.

  * Expect linear time and no memory blow-up.

  * Confirm it completes within reasonable time bounds on typical interview hardware.

### **6\) Adversarial distributions**

* **Worst “swap-heavy” pattern:** All odds on the left, all evens on the right (e.g., `[1,3,5,..., 2,4,6,...]`). Ensures our two-pointer loop handles many swaps correctly.

* **Already good pattern:** All evens on left, odds on right (should do minimal work).

* **Many zeros:** `[0,0,0,1,1]` (zeros are even—ensure they stay in the even partition).

## **✅ Example (lightweight) Python test scaffolding**

`def is_valid_partition(a):`  
    `# finds first odd index; ensures no even after that`  
    `seen_odd = False`  
    `for x in a:`  
        `if x % 2 == 0:`  
            `if seen_odd:`  
                `return False`  
        `else:`  
            `seen_odd = True`  
    `return True`

`def multiset_equal(a, b):`  
    `from collections import Counter`  
    `return Counter(a) == Counter(b)`

`def test_basic():`  
    `for arr in ([1,2,3,4,5], [], [0], [1], [2,4,6], [5,3,7],`  
                `[-2,-1,0,3,4], [2,2,1,1,4,4,3,3], [1,2,1,2,1,2]):`  
        `original = arr[:]`  
        `parity_sort(arr)`  
        `assert is_valid_partition(arr)`  
        `assert multiset_equal(arr, original)`

`def test_oracle_random():`  
    `import random`  
    `for _ in range(200):`  
        `n = random.randint(0, 2000)`  
        `arr = [random.randint(-10**9, 10**9) for _ in range(n)]`  
        `copy = arr[:]`  
        `parity_sort(arr)`  
        `oracle = sorted(copy, key=lambda x: x % 2)`  
        `# we don't require same internal order; just require partition validity and multiset preservation`  
        `assert is_valid_partition(arr)`  
        `assert multiset_equal(arr, oracle)`

## **🧩 Possible micro-improvements to the code**

* In Python, `x & 1` is a tiny bit faster than `x % 2`, but `% 2` is perfectly fine and more explicit in interviews.

* Guard for empty arrays (the loop already handles it).

* Unit-test the predicate for negative values to avoid language-specific surprises (good hygiene across languages).

If you’d like, I can also show a **stable** O(n) time / O(n) space version (preserving relative order) and discuss why it’s not required here but occasionally requested in variants.

##### **You said:**

interviewr: Wow, that's an incredibly thorough testing strategy\! I'm really impressed by how systematically you've thought about this. Your approach covers all the bases \- from basic functionality to edge cases to performance validation. I particularly like how you defined the correctness properties with the partition invariant and multiset preservation. That shows you're thinking like a software engineer, not just solving the immediate problem. Your oracle-based testing approach is smart too \- using the sorted version with the parity key as a reference point for validation. One quick question about your implementation: you mentioned that in Python, x & 1 might be slightly faster than x % 2 for checking parity. Do you think that kind of micro-optimization would be worth mentioning or implementing in an interview setting?

###### **ChatGPT said:**

Thought for 14s

Candidate:  
 Great question. Short answer: I’d **mention it briefly**, but I’d **keep `% 2` in the final code** unless the interviewer explicitly cares about micro-optimizations.

Here’s why:

* **Readability first (interview bias):** `x % 2 == 0` is immediately clear to everyone. `x & 1` is correct but a bit more “bit-twiddly.” In interviews, I optimize for clarity unless performance is truly at risk.

* **Performance impact is negligible:** The algorithm is **memory-bound and O(n)**. The parity check is not the bottleneck; swapping/traversal dominates. Any speedup from `&` vs `%` is dwarfed by overall costs.

* **Correctness across languages:**

  * In **Python**, both work for negatives (e.g., `-3 % 2 == 1`, `-3 & 1 == 1`).

  * In **Java/C++**, `%` on negatives can bite you if you write `x % 2 == 1` for “odd.” Safer checks are `x % 2 != 0` **or** `((x & 1) != 0)`. If I were coding in those languages, I’d call this out to avoid sign pitfalls.

**What I’d do in an interview:**

* Use `% 2 == 0` in Python for clarity.

* Add a one-liner: “If we were in Java/C++, I’d either use `x % 2 != 0` or `x & 1` to avoid negative-mod traps.”

* If you ask for the micro-opt, I can switch to `x & 1` and add a small comment like `# parity check (bitwise, faster but less explicit)`.

So I’d acknowledge the micro-opt, demonstrate awareness, but default to the **clean, obvious** version unless there’s a concrete reason to squeeze cycles.

##### **You said:**

Interviews reward clarity and correctness over micro-optimizations, unless you're explicitly asked about performance tuning. The fact that I know both approaches and their trade-offs is what matters\!

###### **ChatGPT said:**

Candidate:  
 Exactly\! 🎯 You summed it up perfectly. In an interview, the priorities are:

1. **Correctness** – solve the problem as stated.

2. **Clarity** – write code that the interviewer can read and reason about quickly.

3. **Efficiency at the right level** – choose the right algorithm and data structures; micro-optimizations are secondary.

The fact that I can say:

* *“Here’s the clean `% 2` solution I’d actually use in Python for clarity.”*

* *“Here’s the alternative `& 1` approach, which is slightly faster and safer in some languages, but harder to read.”*

…shows that I understand the **trade-offs** and can adapt to context. That’s usually what interviewers are really testing: can you recognize the options and explain *why* you made your choice.

