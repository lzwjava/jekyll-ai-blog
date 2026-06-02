---
audio: false
generated: true
lang: en
layout: post
title: Typical Advice and Patterns in Benjamin Qi’s C++ Files
translated: false
type: note
---

Benjamin Qi, known as "Benq" in competitive programming circles, is a top-rated programmer on platforms like Codeforces and a prominent figure in the USACO community. His advice and coding practices, particularly in C++, are well-regarded for their efficiency and clarity in the context of competitive programming. While specific comments in his C++ files may vary depending on the problem, his general approach and the reminders he includes in his code (often as comments) reflect best practices for competitive programming. Below is an overview of the typical advice and patterns in his C++ files, including the kinds of comments he might use to remind himself of key considerations, based on his contributions, resources, and community insights.

### Typical Advice and Patterns in Benjamin Qi’s C++ Files

Benjamin Qi’s C++ code is optimized for speed (both in writing and execution), correctness, and minimal debugging during contests. His files often include comments that serve as reminders to avoid common pitfalls or to enforce good habits. Here are the key aspects of his approach:

1. **Minimal but Clear Code Structure**:
   - **Advice**: Qi emphasizes writing concise code that is just readable enough for the contest duration, as competitive programming prioritizes speed over maintainability. Comments are sparse but strategic, focusing on critical logic or potential error points.
   - **Typical Comments**:
     - `// check bounds` or `// array size`: Reminders to verify array indices or sizes to avoid out-of-bounds errors, a common issue in C++.
     - `// int overflow?`: A prompt to consider whether integer operations might exceed `int` limits (e.g., 2^31 - 1), often suggesting the use of `long long`.
     - `// mod arithmetic`: A note to ensure modular arithmetic is handled correctly, especially in problems involving large numbers.

2. **Use of Macros and Templates**:
   - **Advice**: Qi advocates for using macros and templates to reduce typing and speed up coding, but he warns against overuse to maintain readability. His files often include a pre-written template with common utilities (e.g., loops, data structures).
   - **Typical Comments**:
     - `// #define FOR(i,a,b) ...`: Defining a loop macro like `FOR(i,a,b)` for iterating from `a` to `b`, with a comment to clarify its purpose or warn against misuse.
     - `// careful with macro args`: A reminder to avoid side effects in macro arguments (e.g., `i++` in a macro).
     - `// template for min/max`: Comments above template functions like `chmin` or `chmax` to remind him of their usage for updating minimum/maximum values efficiently.

3. **Focus on Avoiding Bugs**:
   - **Advice**: Qi’s code includes checks for common competitive programming errors, such as off-by-one errors, uninitialized variables, or incorrect input handling. His comments often highlight these potential issues.
   - **Typical Comments**:
     - `// 0-based or 1-based?`: A reminder to confirm whether the problem uses 0-based or 1-based indexing, especially for graph or array problems.
     - `// init variables`: A note to ensure all variables are initialized, particularly for arrays or accumulators.
     - `// edge cases`: A prompt to consider special cases, like empty inputs, single-element cases, or extreme values (e.g., `n = 1` or `n = 10^5`).

4. **Efficient Input/Output**:
   - **Advice**: Qi uses fast I/O techniques to avoid time limit exceeded (TLE) errors, such as `ios::sync_with_stdio(0)` and `cin.tie(0)`. He may comment on these to remind himself of their necessity.
   - **Typical Comments**:
     - `// fast I/O`: Above the I/O optimization lines to confirm they’re included.
     - `// endl vs \n`: A reminder to use `\n` instead of `endl` for faster output.
     - `// read carefully`: A note to ensure the input format (e.g., number of test cases, whitespace) is correctly handled.

5. **Modular and Reusable Code**:
   - **Advice**: Qi’s files often include reusable components like modular arithmetic functions, graph algorithms, or data structures (e.g., segment trees). Comments help him quickly adapt these for specific problems.
   - **Typical Comments**:
     - `// mod = 1e9+7`: A note specifying the modulus for arithmetic operations, common in combinatorial problems.
     - `// precompute`: A reminder to precompute values (e.g., factorials, inverses) for efficiency.
     - `// copy-paste from library`: A comment indicating a block of code reused from his personal library, ensuring he verifies its applicability.

6. **Time and Space Complexity Awareness**:
   - **Advice**: Qi is meticulous about ensuring his solutions meet time and space constraints. His comments often reflect calculations or reminders about complexity.
   - **Typical Comments**:
     - `// O(n log n)`: A note on the expected time complexity of the algorithm.
     - `// memory limit`: A reminder to check if the space used (e.g., large arrays) fits within problem constraints.
     - `// bottleneck`: A comment identifying the slowest part of the code that might need optimization.

7. **Debugging and Testing**:
   - **Advice**: While competitive programming doesn’t allow extensive debugging during contests, Qi includes comments to facilitate quick checks or to mark areas for verification.
   - **Typical Comments**:
     - `// debug`: Above a temporary print statement (e.g., `cerr`) used to inspect variable values.
     - `// test small cases`: A reminder to mentally or manually verify the code on small inputs.
     - `// check sample`: A note to compare output against the problem’s sample cases.

### Example of a Benjamin Qi C++ File with Comments

Below is a hypothetical example of how Qi’s C++ file might look for a competitive programming problem, incorporating his typical advice and comment style (inspired by his GitHub repository and USACO Guide contributions):

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// fast I/O
#define FOR(i,a,b) for (int i = (a); i < (b); ++i)
const ll MOD = 1e9 + 7; // mod = 1e9+7

int main() {
    ios::sync_with_stdio(0); cin.tie(0); // fast I/O
    int t; cin >> t; // read carefully
    while (t--) {
        int n; cin >> n;
        vector<ll> a(n); // check bounds
        FOR(i,0,n) cin >> a[i];

        // init variables
        ll sum = 0;
        FOR(i,0,n) {
            sum = (sum + a[i]) % MOD; // mod arithmetic
            // int overflow?
            if (sum < 0) sum += MOD; // edge cases
        }

        // O(n) complexity
        cout << sum << '\n'; // endl vs \n
        // check sample
    }
    return 0;
}
```

### Specific Insights from Benjamin Qi’s Resources

- **USACO Guide (Contributor)**: Qi co-authored the USACO Guide, which emphasizes practical C++ tips for competitive programming. He advises using `bits/stdc++.h` for quick access to standard libraries, despite it being non-standard, and includes comments like `// non-portable` to acknowledge this. He also recommends `auto` for type deduction to reduce code length, with comments like `// auto for readability` in his templates.[](https://usaco.guide/general/intro-cp)[](https://usaco.guide/general/generic-code)
- **GitHub Repository (cp-notebook)**: In his `cp-notebook` repository, Qi’s files often start with a standard template including macros and typedefs. Comments like `// adjust for problem` or `// verify constraints` remind him to tweak the template for specific problem requirements.[](https://github.com/bqi343/cp-notebook)
- **Codeforces Style Guide**: Qi follows a competitive programming-specific C++ style guide, advocating for minimal spacing (e.g., `int* ptr` instead of `int *ptr`) and comments like `// style: pointer spacing` to enforce consistency. He also uses `const` over `#define` for constants, with comments like `// const for type safety`.[](https://codeforces.com/blog/entry/64218)

### Common Reminders in Comments

Qi’s comments are concise and problem-focused, often addressing:

- **Correctness**: `// check if sorted`, `// handle negative numbers`.
- **Efficiency**: `// reduce to O(n)`, `// avoid TLE`.
- **Problem-Specific Nuances**: `// multiple test cases?`, `// undirected graph?`.
- **Personal Habits**: `// don’t rush`, `// think before coding`, reflecting his disciplined approach to avoiding hasty mistakes.

### Why These Comments Matter

In competitive programming, where time is critical, Qi’s comments serve as quick mental checkpoints to prevent errors that could cost valuable points. They reflect his experience with common pitfalls (e.g., missing edge cases, misinterpreting input) and his focus on staying organized under pressure. His advice, as seen in forums like Codeforces and Reddit, emphasizes practicing with problems on platforms like USACO, Codeforces, and LeetCode to internalize these checks, reducing the need for explicit comments over time.[](https://codeforces.com/blog/entry/90103)[](https://www.reddit.com/r/cpp_questions/comments/1fh8wrm/c_for_competitive_programming/)

### Conclusion

Benjamin Qi’s typical advice in his C++ files for competitive programming revolves around writing fast, correct, and minimally readable code, with comments acting as reminders for bounds checking, overflow prevention, input/output optimization, and complexity awareness. His comments are succinct, targeting potential errors like `// check bounds`, `// int overflow?`, or `// edge cases`, and are often paired with a pre-written template to streamline coding. For those looking to emulate his approach, studying his USACO Guide modules, GitHub repository, and Codeforces submissions can provide deeper insights into his coding style and comment habits.[](https://github.com/bqi343/cp-notebook)[](https://github.com/bqi343)[](https://cphof.org/profile/topcoder:bqi343)

If you’d like me to search for specific examples from Qi’s public code or analyze a particular problem’s file, let me know!
