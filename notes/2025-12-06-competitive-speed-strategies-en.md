---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Competitive Programming Speed Strategies
translated: false
type: note
---

Question: What are good tricks and strategies for solving problems faster on Codeforces, AtCoder, LeetCode, or Competitive Programming in general (like starting with one example, making it work, then expanding)?

Answer:

Here are the most effective practical tricks that top competitive programmers actually use to solve problems quickly and correctly:

- **Start with one single example and hard-code it first**
  Copy one sample input, write the minimal code that outputs exactly the sample output (even if it’s completely hacked). Run it → it passes the sample. Now you have a working baseline in <2 minutes. This boosts confidence and gives you something to refactor.

- **Add one test case at a time (incremental development)**
  After the first sample works, add the second sample as a new test in your local code. Make it pass. Then add edge cases one by one (n=1, n=0, maximum constraints, all equal elements, etc.). This is basically TDD for CP and catches 90% of bugs early.

- **Solve for n=1 or smallest subproblem first**
  Many problems become trivial when n=1 or for the first few elements. Implement the solution for the tiny case, verify, then generalize step by step.

- **Brute-force first, optimize later**
  Write the slow O(n²) or O(2ⁿ) solution that obviously works. If it passes all your local tests (including near-maximum cases), submit it on platforms with loose constraints (many Codeforces Div2 A/B/C). You get AC instantly and can refactor to faster version only if needed.

- **Use “debug print” or visualizer aggressively**
  Print the state after every major step for your test cases. Many people use custom pretty-print functions or even draw the array/state on paper for one example.

- **Copy-paste the sample input into your code as a string and test locally**
  Saves time instead of running on the judge every time.

- **Write a stress-testing script early**
  Generate random test cases, run brute-force and your smart solution, compare outputs. If they differ → instant counter-test for debugging.

- **Think of the solution in terms of transformations on one example**
  Take the sample input, manually apply your idea step by step on paper or in comments, and see what the final state should be. Then translate those exact steps into code.

- **Edge-case checklist (memorize it)**
  Run these mentally or add them as tests:
  - n = 0 / empty input
  - n = 1
  - n = maximum
  - All elements equal
  - Already sorted / reverse sorted
  - Alternating values
  - Duplicates everywhere

- **Implement from the constraints**
  Look at constraints first → if n ≤ 20 → bitmask/dp, n ≤ 10⁵ → O(n log n) is safe, etc. Many people write the skeleton based only on constraints before reading the full problem.

- **“What if I sort it?” / greedy checklist**
  For many problems, trying the greedy approach on one sample manually reveals if it works.

- **Two-pointer / sliding window on one example**
  Take the array from sample, move left/right pointers manually on paper watching the condition → instantly see if the technique fits.

- **Binary search the answer (when possible)**
  Instead of finding the algorithm, assume the answer lies in some range and binary search it. Works surprisingly often and is easy to code after you verify on one example.

- **Read the problem → implement the absolute dumbest solution that could possibly work → submit → if TLE/WA, improve**
  This is faster than overthinking for 30 minutes and writing nothing.

These tricks combined let good contestants solve Div2 A/B/C in 5–15 minutes reliably because they focus on “make it work on samples + edges first” instead of perfect code from the beginning.

References:
- [Codeforces blog – How to practice efficiently](https://codeforces.com/blog/entry/17879)
- [Errichto – Debugging tips and common tricks (YouTube)](https://www.youtube.com/watch?v=O45fH0b7bUQ)
- [William Lin – Solving problems fast (stream highlights)](https://www.youtube.com/watch?v=6V3siDh2Buc)
