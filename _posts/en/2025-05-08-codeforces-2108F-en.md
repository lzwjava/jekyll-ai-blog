---
audio: false
generated: true
lang: en
layout: post
title: Codeforces 2108F
translated: false
type: note
---

Let’s dive into why the provided Java code solves the "Fallen Towers" problem. The problem involves an array of \\( n \\) towers, each with a height \\( a_i \geq 0 \\). You can knock down the tower at position \\( i \\), which increases the heights of the next \\( a_i \\) towers by 1 (or fewer if there aren’t enough towers left), then sets \\( a_i \\) to 0. The goal is to knock down all \\( n \\) towers exactly once in any order, ensuring the final array is non-decreasing (i.e., for any \\( i < j \\), the height at position \\( i \\) is at most the height at position \\( j \\)). The output is the maximum MEX of the final array, where the MEX is the smallest non-negative integer not present in the array.

---

### Problem Analysis

1. **Operation Definition**:
   - Knocking down tower \\( i \\) with height \\( a_i \\):
     - Increases the heights of towers at positions \\( i+1, i+2, \dots, i+a_i \\) by 1 (if they exist).
     - Sets \\( a_i = 0 \\).
   - Each tower must be knocked down exactly once, in any order.
   - If \\( a_i = 0 \\), knocking down tower \\( i \\) has no effect on other towers.

2. **Non-Decreasing Final Array**:
   - After all operations, the final array \\( b_1, b_2, \dots, b_n \\) must satisfy \\( b_i \leq b_{i+1} \\) for all \\( i < n \\).

3. **MEX**:
   - The MEX of the final array is the smallest non-negative integer \\( m \\) not present in \\( \{b_1, b_2, \dots, b_n\} \\).
   - Since the array is non-decreasing, if the array contains values \\( 0, 1, 2, \dots, k-1 \\) (possibly with repetitions) but not \\( k \\), the MEX is \\( k \\).
   - The goal is to maximize this MEX.

4. **Interpretation of MEX**:
   - For the MEX to be \\( m \\), the final array must include all integers from 0 to \\( m-1 \\) at least once, and \\( m \\) must not appear.
   - Since the array is non-decreasing, achieving a MEX of \\( m \\) implies the final array has values like \\( 0, 0, \dots, 1, 1, \dots, m-1, m-1 \\), with each integer from 0 to \\( m-1 \\) appearing at least once, and no value \\( m \\) or higher.

5. **Key Insight**:
   - The MEX \\( m \\) corresponds to having at least one position with each value from 0 to \\( m-1 \\).
   - Equivalently, for a MEX of \\( m \\), we need at least \\( m \\) positions in the final array such that position \\( i \\) has a value at least \\( i - (n - m) \\), because:
     - The last \\( m \\) positions (from index \\( n-m+1 \\) to \\( n \\)) must cover values 0 to \\( m-1 \\).
     - Position \\( n-m+1 \\) should have value at least 0, position \\( n-m+2 \\) at least 1, ..., position \\( n \\) at least \\( m-1 \\).
   - This translates to requiring the final height at position \\( i \\) to be at least \\( \max(0, m - (n - i + 1)) = \max(0, m - n + i) \\).

---

### Solution Approach

The code uses a binary search to find the maximum possible MEX \\( m \\). For each candidate \\( m \\), it checks whether it’s possible to achieve a final non-decreasing array where each position \\( i \\) has a height at least \\( \max(0, m - n + i) \\). This ensures that the last \\( m \\) positions can cover values 0 to \\( m-1 \\), making the MEX at least \\( m \\).

#### Binary Search

- **Range**: The MEX \\( m \\) is at least 0 (empty array case) and at most \\( n \\) (since we need at least \\( m \\) positions to have values 0 to \\( m-1 \\)). Thus, search for \\( m \\) in \\( [0, n] \\).
- **Check Function**: For a given \\( m \\), determine if there exists an order to knock down the towers such that the final array satisfies:
  - \\( b_i \geq \max(0, m - n + i) \\) for all \\( i \\).
  - The array is non-decreasing.

#### Check Function

The check function simulates whether it’s possible to achieve the required heights using a difference array approach, assuming the towers can be knocked down in any order.

1. **Required Heights**:
   - For MEX \\( m \\), position \\( i \\) needs a final height \\( b_i \geq \text{need}_i \\), where:
     \\[
     \text{need}_i = \max(0, m - n + i)
     \\]
   - This ensures that positions \\( n-m+1 \\) to \\( n \\) have heights at least 0, 1, ..., \\( m-1 \\), respectively.

2. **Difference Array**:
   - The code uses a difference array \\( d \\) to track the cumulative effect of operations.
   - Initialize \\( d[i] = 0 \\) for all \\( i \\).
   - For each position \\( i \\):
     - Compute the cumulative sum: \\( d[i] += d[i-1] \\) (if \\( i > 0 \\)), representing the current number of extra blocks at position \\( i \\).
     - Check if \\( d[i] \geq \text{need}_i \\). If not, it’s impossible to achieve the required height, so return \\( false \\).
     - Compute the length of the range affected by knocking down tower \\( i \\):
       \\[
       \text{len} = d[i] - \text{need}_i + a_i
       \\]
       - \\( d[i] - \text{need}_i \\): Extra blocks available after meeting the minimum requirement.
       - \\( a_i \\): The number of blocks contributed by tower \\( i \\)’s height.
       - This \\( \text{len} \\) represents how many positions to the right of \\( i \\) can be incremented when tower \\( i \\) is knocked down.
     - Update the difference array:
       - Increment \\( d[i+1] \\) (if \\( i+1 < n \\)) to start the effect of knocking down tower \\( i \\).
       - Decrement \\( d[i + \text{len} + 1] \\) (if \\( i + \text{len} + 1 < n \\)) to end the effect after \\( \text{len} \\) positions.

3. **Feasibility**:
   - The difference array simulates the effect of knocking down tower \\( i \\) with a modified height based on the current state.
   - If the loop completes without returning \\( false \\), it’s possible to achieve the required heights for MEX \\( m \\).

4. **Why This Works**:
   - The check function doesn’t simulate the actual order of operations but verifies if there exists an order that satisfies the height requirements.
   - The difference array approach ensures that the number of blocks added to each position is consistent with some valid sequence of operations.
   - The non-decreasing condition is implicitly satisfied because the required heights \\( \text{need}_i = \max(0, m - n + i) \\) are non-decreasing (as \\( i \\) increases, \\( m - n + i \\) increases or stays 0).

#### Main Loop

- Read the number of test cases \\( t \\).
- For each test case:
  - Read \\( n \\) and the array \\( a \\).
  - Perform binary search on \\( m \\) from 0 to \\( n \\).
  - Use the check function to determine if MEX \\( m \\) is achievable.
  - Update \\( lo \\) (if achievable) or \\( hi \\) (if not).
- Output the maximum \\( m \\) (i.e., \\( lo \\)) for each test case.

---

### Why the Code Solves the Problem

1. **Correctness of Binary Search**:
   - The binary search finds the maximum \\( m \\) such that the check function returns \\( true \\).
   - Since the feasibility of MEX \\( m \\) implies feasibility for all smaller MEX values (lower \\( m \\) requires fewer positions with lower heights), the binary search correctly identifies the maximum possible MEX.

2. **Check Function Accuracy**:
   - The check function ensures that each position \\( i \\) can have at least \\( \max(0, m - n + i) \\) blocks after all operations.
   - The difference array simulates the cumulative effect of knocking down towers, accounting for the fact that each tower contributes \\( a_i \\) blocks to the next \\( a_i \\) positions.
   - By processing positions left to right and adjusting the difference array, it verifies if the initial heights \\( a_i \\) can be redistributed to meet the required heights.

3. **Handling Non-Decreasing Constraint**:
   - The required heights \\( \max(0, m - n + i) \\) are non-decreasing, which aligns with the problem’s requirement for a non-decreasing final array.
   - If the check function succeeds, the resulting array can be made non-decreasing by ensuring each position meets or exceeds the required height.

4. **Efficiency**:
   - **Binary Search**: \\( O(\log n) \\) iterations (since \\( m \leq n \\)).
   - **Check Function**: \\( O(n) \\) per call, as it processes each position once and updates the difference array in constant time per position.
   - **Total per Test Case**: \\( O(n \log n) \\).
   - **Total for All Test Cases**: Since \\( \sum n \leq 10^5 \\), the overall complexity is \\( O(t \cdot n \log n) \\), which fits within the 3-second time limit.

5. **Edge Cases**:
   - **\\( n = 1 \\)**: If \\( a_1 = 0 \\), MEX = 1 (array becomes [0]). If \\( a_1 > 0 \\), MEX = 0 (array becomes [0]). The code handles this correctly.
   - **Large \\( a_i \\)**: Since \\( a_i \leq 10^9 \\), but only the first \\( n-i \\) positions are affected, the code correctly bounds the effect using array limits.
   - **All \\( a_i = 0 \\)**: Final array is all zeros, MEX = 1. The check function confirms this.
   - **Mixed values**: The binary search and check function handle arbitrary \\( a_i \geq 0 \\).

---

### Java Code Specifics

The Java code adapts the C++ logic using `BufferedReader` and `PrintWriter` for efficient I/O, as requested. Key aspects:

1. **Input Handling**:
   - Uses `BufferedReader` to read lines and `StringTokenizer` to parse integers.
   - Reads \\( t \\), then for each test case, reads \\( n \\) and the array \\( a \\).

2. **Checker Class**:
   - Encapsulates the check logic to mimic the C++ lambda function.
   - Uses an array \\( d \\) to simulate the difference array approach.

3. **Output**:
   - Uses `PrintWriter` to output the result for each test case, with `out.flush()` to ensure all output is written.

4. **Performance**:
   - The Java code maintains the same \\( O(n \log n) \\) complexity per test case.
   - `BufferedReader` and `PrintWriter` ensure I/O is fast enough for \\( \sum n \leq 10^5 \\).

---

### Conclusion

The code solves the "Fallen Towers" problem by:

- Using binary search to find the maximum MEX \\( m \\).
- Employing a difference array-based check function to verify if the initial tower heights can be redistributed to achieve a non-decreasing array with the required heights.
- Ensuring correctness through the non-decreasing nature of the required heights and the feasibility of operation sequences.
- Handling all edge cases and fitting within the time and memory constraints.

The Java implementation faithfully translates the C++ logic, using efficient I/O to meet the problem’s requirements.
