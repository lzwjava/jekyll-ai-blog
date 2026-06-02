## 1. Repeatedly Refine Your Code

Wang Yin argues that the most effective way to improve programming skill is to **repeatedly revise and polish code**, not just write more of it. He compares this to a writer who discards more than they publish — great programmers delete more code than they keep. You cannot write perfect code in one shot; insights come gradually over time.

---

## 2. Write Elegant Code

Elegant code has two key structural characteristics:

- **Box-like structure**: Code is neatly nested and organized, like labeled compartments in a drawer.
- **Tree-like structure**: Logic branches clearly like a tree. He notes that his `if` statements almost always have **two branches** (if + else), making logic explicit and exhaustive.

---

## 3. Write Modular Code

True modularity is **logical, not physical**. Splitting code into many files/directories does not make it modular. The real tool for modularity is the **function** — functions have well-defined inputs (parameters) and outputs (return values). He recommends:

- **Keep functions short** (under ~40 lines, so it fits in one screen without scrolling).
- **Create small helper functions** — even 2-line helpers can drastically simplify the main logic.
- **Each function should do one simple thing** — avoid multi-purpose functions with internal branching based on conditions.
- **Avoid using global variables or class members to pass data between functions** — use local variables and parameters instead.

---

## 4. Write Readable Code

Truly elegant code **barely needs comments**. Over-commenting is actually harmful — comments get outdated and clutter the code. Instead, make the code self-explanatory through:

- **Meaningful function and variable names** — the name should describe the logic.
- **Keep local variables close to where they are used** — don't declare everything at the top of a function.
- **Keep local variable names short** — when the variable is used nearby, the context makes a short name sufficient.
- **Don't reuse local variables** — define a new variable for each distinct value; it clarifies scope and intent.
- **Extract complex logic into helper functions** — replace a block of cryptic code with a well-named function call.
- **Extract complex expressions into intermediate variables** — avoid deeply nested function calls.
- **Break lines at logical boundaries** — don't rely on the IDE's automatic line-wrapping, which breaks lines at arbitrary positions.

He warns against making code look like natural language (e.g., the Chai.js assertion style), which actually reduces clarity.

---

## 5. Write Simple Code

Don't blindly use every language feature. Stick to a reliable, battle-tested subset. Specific rules:

- **Avoid `i++` / `++i` / `i--` / `--i`** — these mix read and write operations and are a historical design mistake. Replace with explicit two-step operations (e.g., `int t = i; i += 1; foo(t);`), except in simple `for` loop update expressions.
- **Never omit curly braces** — even single-line `if` bodies should always have `{}` to avoid "optical illusion" bugs when adding new lines later.
- **Use parentheses to clarify operator precedence** — don't rely on readers knowing obscure precedence rules (e.g., bitshift `<<` has lower precedence than `+`).
- **Avoid `continue` and `break` in loops** — they make loop termination conditions complex. Eliminate them by:
  - Inverting the condition of `continue` into an `if` block.
  - Merging `break` conditions into the `while` header.
  - Replacing `break` with `return`.
  - Extracting complex loop bodies into helper functions.

---

## 6. Write Direct/Intuitive Code

Choose the clearer, more explicit approach even if it appears longer. For example, avoid abusing short-circuit evaluation (`&&`, `||`) as a replacement for `if` statements. This is confusing because logical OR/AND were designed for efficiency, not for control flow readability.

Instead of:

```javascript
if (action1() || action2() && action3()) { ... }
```

Write the explicit version:

```java
if (!action1()) {
  if (action2()) {
    action3();
  }
}
```

---

## 7. Write Bulletproof Code

Always have **two branches in every `if` statement** to force yourself to think about all cases. Don't omit the `else` branch and rely on "fall-through" control flow — this creates spaghetti logic that is hard to verify as correct. Explicitly handle every possible outcome.

---

## 8. Correctly Handle Errors

- Don't ignore return values from functions (e.g., Unix `read()` returning `-1`).
- Don't use overly broad `catch (Exception e) {}` — this silently swallows unexpected errors.
- Catch the **specific** exception type you expect.
- Keep `try` blocks small — one try/catch per function call where possible, to pinpoint which call failed.
- Handle errors at the point where they occur, not by re-throwing them endlessly upward.

---

## 9. Correctly Handle Null Pointers

- **Minimize producing nulls** — use exceptions (e.g., `NotFoundException`) instead of returning null for "not found."
- **Never catch `NullPointerException`** — fix the root cause instead.
- **Never put null into collections** (List, Map, Set) — it causes hard-to-trace bugs.
- **Check for null immediately** at the point where a nullable value is received, and handle it meaningfully rather than passing the null upstream.
- **Function authors should reject null parameters aggressively** — use `Objects.requireNonNull()` to crash immediately on null input.
- Use **`@NotNull` / `@Nullable` annotations** (IntelliJ) for static analysis.
- Use **`Optional` types** (Java 8 / Swift) carefully — the benefit comes only when you use the "atomic" pattern (check + unwrap in one operation), not when you call `isPresent()` + `get()` separately (which is just null-checking under a different name).

---

## 10. Prevent Over-Engineering

Signs of over-engineering:

- Thinking too far into the future before solving the present problem.
- Obsessing over "code reuse" before you have working code.
- Excessive test scaffolding that makes simple code complex.

His principles:

- **Solve the problem at hand first**, then consider future extensibility.
- **Write working code first**, then consider reuse.
- **Write simple, obviously-correct code first**, then consider testing.

He distinguishes between "code with no obvious bugs" (complex code + lots of tests) and "obviously bug-free code" (simple, direct code), and advocates for the latter.

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
