---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tests Should Be Smart Not Dogmatic
translated: false
type: note
---

Question: What does the article at <https://www.yinwang.org/posts/tests> say?

Answer:

The article is titled **"On Tests"** by **Yin Wang** (王垠), a Chinese computer scientist known for his strong opinions about software engineering. The article argues against **test dogmatism** — the blind, excessive reliance on software testing as a measure of code quality. Here is a comprehensive summary:

---

## Core Thesis

The original purpose of testing was to improve code quality, but excessive, unnecessary, and unreliable testing not only fails to achieve that goal, but actually reduces code quality, increases workload, and greatly delays project progress.

Yin Wang's position is that **he does write tests**, but in a smarter, more selective way. He does not advocate for Test-Driven Development (TDD).

---

## The 11 Principles About Tests

**1. Attitudes and slogans don't improve code quality.**
Knowing terms like "unit test" and "integration test" does not mean you know programming well. The only feasible way to improve code quality is not to write tests, but to repeatedly refine one's own thinking and write simple and clear code.

**2. True programming masters are not bound by tests.**
Testing is like guardrails on a racetrack. A qualified driver will never focus on having guardrail protection — their safety only depends on their own skill, not the guardrails. People who advocate test-driven development are like third-rate drivers: no matter how many tests they write, they cannot produce reliable code.

**3. Don't write tests until the program and algorithm are finalized.**
Writing tests prematurely ties your hands and feet, preventing you from modifying code and algorithms freely. Only after the program no longer requires drastic changes is it time to gradually add tests.

**4. Don't change clear code just to accommodate tests.**
In order to meet "coverage" requirements or use mocks, many people change originally simple and clear code into a more complex and confusing form, even using a lot of reflection. This actually reduces the quality of the code.

**5. Don't test implementation details — only test essential properties.**
Tests should only describe the "basic properties" that the program needs to satisfy (such as `sqrt(4)` should equal `2`), rather than describe the "implementation details." Testing implementation details is essentially just writing the code twice.

**6. Not every bug fix requires a test.**
Before writing tests, you should think carefully: how likely is this bug to happen again in the same place? Once a low-level mistake is identified, it is unlikely to reappear in the same place. You shouldn't be writing tests for the bug, but for the nature of the code.

**7. Avoid using mocks, especially multi-layer mocks.**
Multi-layer mocks often cannot generate sufficiently diverse inputs and cannot cover various boundary conditions. If your code is modular enough, you shouldn't need multiple layers of mocks to test it.

**8. Don't neglect manual testing.**
Overemphasizing test automation not only delays the progress of the project but also loses the accuracy of manual testing. Changing the way of thinking, they only need to spend a few minutes to observe many in-depth problems manually.

**9. Avoid tests that are too long and time-consuming.**
Some people can test the required properties with a small input, but always like to give a large input, subconsciously thinking it is more reliable. As a result, the test consumes a lot of build time every time.

**10. Each test should test only one aspect.**
If a test only tests one aspect and does not test the same component repeatedly, then you can quickly find the problematic component and location based on the failed test.

**11. Avoid testing by comparing strings.**
Tests that compare formatted string output are very fragile, because the format often changes slightly. The correct approach is to perform a structured comparison.

---

## Case Studies

**Google (PySonar):**
Yin Wang created PySonar at Google without following his teammates' demands to write tests from the start. He organized the code in his own way, conducted precise thinking and reasoning, and completed a very elegant, correct, high-performance, and easy-to-maintain system within three months. PySonar is still the world's most advanced Python type inference and indexing system, adopted by many companies to process millions of Python codes.

**Shape Security:**
He built an advanced JavaScript obfuscator and improved a cluster management system. For the cluster system, the team decided to abandon the existing tests entirely and rely on strict code review, logical reasoning, and deliberation. The project was completed in less than two months.

**Coverity (Failure Case):**
Coverity's Java analysis team suffered from test dogmatism — requiring a test for every bug fix, even for trivially obvious mistakes. This made the progress of the project extremely painful and slow, while the product was still full of bugs.

---

## Conclusion

Because the vast majority of people have such a deep misunderstanding of testing and the prevalence of test dogmatism is so widespread, many excellent programmers have sunk into tedious test-driven development and cannot stretch their strengths. The hope is that everyone will treat tests rationally in the project, instead of writing tests blindly. Only in this way can the project be completed better and faster.

---

**In short:** Yin Wang's article is a sharp critique of blind test culture in software engineering. He advocates for **precision thinking, clean code, and selective testing** over mechanical adherence to TDD or coverage-driven testing dogma.

References:

- [On Tests - Yin Wang (Substack mirror)](https://yinwang0.substack.com/p/on-tests)
- [测试的道理 - yinwang.org (Original Chinese)](https://www.yinwang.org/blog-cn/2016/09/14/tests)
