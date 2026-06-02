---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wisdom of Programming by Wang Yin
translated: false
type: note
---

**Question:** What does the article at https://www.infoq.cn/article/wisdom-of-programming say?

**Answer:**

The article is titled **"编程的智慧" (The Wisdom of Programming)**, written by **Wang Yin (王垠)** and published on **August 29, 2016** on InfoQ China. It is approximately a 70-minute read (~21,000 Chinese characters). Wang Yin is a well-known and opinionated Chinese programmer/blogger. The article shares his personal philosophy and hard-won lessons on writing high-quality code. Here is a comprehensive summary of all the major topics covered:

---

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

**References:**

- [https://www.infoq.cn/article/wisdom-of-programming](https://www.infoq.cn/article/wisdom-of-programming)
