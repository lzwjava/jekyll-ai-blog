---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-pro-preview
title: Codeforces Sorting Game Solution Guide
translated: false
type: note
---

Question: How can one solve the Codeforces problem "Sorting Game," where Alice and Bob take turns rearranging non-increasing subsequences of a binary string into non-decreasing order?

Answer:

### **Problem Analysis**

The game is played on a binary string  of length .

1. **Valid Move**: A player chooses a **non-increasing** subsequence (e.g., `1, 1, 0, 0`) and sorts it into **non-decreasing** order (e.g., `0, 0, 1, 1`). This move must strictly change the string.
2. **Losing Condition**: The player who cannot make a valid move loses (Normal Play Convention).
3. **Terminal State**: A string is in a terminal state (no moves possible) if and only if it is already **sorted** (all `0`s come before all `1`s). If a string is sorted, any non-increasing subsequence would consist of only all `0`s or only all `1`s, and sorting them would not change the string.

### **Winning Strategy**

Alice wins if she can transform the string into a sorted state in a single move. Because the game ends as soon as a player is presented with a sorted string, if Alice can sort the string on her first turn, Bob will immediately lose.

**Can Alice always sort the string in one move?**
Yes, if the string is not already sorted. To do this, Alice needs to identify all characters that are "out of place" compared to the final sorted version of the string.

1. Let  be the total number of zeros in the string .
2. In a sorted string of length  with  zeros, the first  characters must be `0` and the remaining  characters must be `1`.
3. Alice can pick the set of indices  where the characters are currently incorrect:
* Any index  where .
* Any index  where .


4. **Validity Check**:
* The characters at indices  (where ) always appear before the indices  (where ).
* Therefore, the subsequence chosen is always a series of `1`s followed by a series of `0`s, which is **non-increasing**.
* Sorting this subsequence swaps the `1`s to the back and the `0`s to the front, making the entire string sorted.
* If the string is unsorted, this set  will contain at least one `1` and one `0`, making the move valid.



### **Algorithm**

1. Count the total number of zeros () in the string.
2. Check if the string is already sorted (i.e., all characters from index  to  are `'0'`).
3. If the string is already sorted, output **Bob**.
4. Otherwise, output **Alice**.
5. To provide the move:
* Find all indices  where .
* Find all indices  where .
* Combine these indices, sort them, and output them as Alice's first move.



### **Complexity**

* **Time**:  per test case to count zeros and identify indices.
* **Space**:  to store the indices of the move.

References:

* [Codeforces Problem 2190A - Sorting Game](https://codeforces.com/contest/2190/problem/A) (Note: Ensure the contest ID is correct as per your source.)