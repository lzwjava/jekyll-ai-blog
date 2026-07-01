---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing vs Static Analysis Explained
translated: false
type: note
---

Question: What does the blog post at <https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/> say?

Answer:

The article, **"Tests and Static Analysis"** by Yin Wang (published December 27, 2013), systematically explains the differences between software testing and static analysis. Here is a comprehensive breakdown:

---

## Background

The author, who built a static analysis tool for Python called PySonar, was frequently asked: "What is the difference between testing and static analysis?" — and wrote this article to give a systematic answer.

---

## 1. Static vs. Dynamic Nature

Both static analysis and tests aim to improve code quality, but they differ fundamentally: static analysis works **without running the program** (static), while tests **execute the program** with actual inputs (dynamic).

- **Static analysis** is like a more powerful version of a compiler's type checker. It can detect resource leaks, array index out-of-bounds, and security risks — essentially reasoning about what *could* happen.
- **Tests** are like "small experiments in real life" — they run the program under specific conditions and observe results.

Static analysis can find problems that tests may never detect (e.g., a complex chain of events leading to a security vulnerability), while tests can catch bugs that static analysis cannot (e.g., an autopilot producing wrong results at a specific altitude and speed).

---

## 2. Tests Cannot Prove Correctness

Passing tests does **not** mean the program is correct — it only means you haven't done "terribly stupid things." To formally guarantee correctness, you would need a mechanical proof using theorem provers like Coq, Isabelle, or ACL2, which requires deep mathematical knowledge and is often infeasible.

---

## 3. Difference in Manual Labor

Testing requires a lot of manual work. Writing tests for "silly bugs" like null pointer dereferences is tedious, and achieving good **path coverage** is nearly impossible because the number of execution paths grows exponentially with program size.

Static analysis, by contrast, is **fully automatic**. It systematically explores all paths, providing far higher path coverage than any human test writer could achieve — even if heuristics are used to keep runtime manageable.

---

## 4. Symbolic Reasoning

Tests use **specific input values**, so bugs at untested values can slip through. Static analysis works **symbolically** — it reasons about *all possible values* for every variable, not just specific ones. This allows it to detect boundary condition bugs (e.g., array index out of bounds) that tests would only catch if you happened to use exactly the right input values.

---

## 5. False Positives in Static Analysis

Some static analysis tools are designed conservatively — when uncertain, they warn "you may have a problem here." This can lead to **false positives** (warnings about bugs that will never actually occur). Much of the engineering work in static analysis is about reducing the false positive rate.

Tests, on the other hand, have **no false positives** — if a test fails, the program genuinely fails under those conditions.

---

## 6. The Value of Static Analysis

Static analysis is the most powerful bug-finding tool that doesn't require extensive manual labor. It handles mindless, tedious bug-catching (like null pointer dereferences that could crash a plane or launch a missile) so that human testers can focus on more intellectual and interesting tests.

---

## Summary Table

| Dimension | Static Analysis | Testing |
| --- | --- | --- |
| When it runs | Without executing code | By executing code |
| Coverage | Exponentially high (automated) | Limited by human effort |
| Values | Symbolic (all possible) | Specific inputs only |
| False positives | Possible | None |
| Proves correctness? | No | No |
| Manual effort | Low | High |

References:

- [https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/](https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/)
