---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.2
title: Solving Codeforces Problem B1 Sub-RBS Easy
translated: false
type: note
---

Question: How to solve the Codeforces problem “B1. Sub-RBS (Easy Version)”?

Answer:

This problem asks for the **longest regular bracket subsequence** `t` of a given regular bracket sequence `s` such that `t` is **lexicographically better** than `s` under a custom definition.

Let’s break it down step by step.

---

## 1. Understanding “better than”

A bracket sequence `t` is **better than** `s` if:

1. `s` is a prefix of `t` and `t ≠ s`, **or**
2. At the first position where they differ, `t[i] = '('` and `s[i] = ')'`.

Since `t` is a **subsequence** of `s`, the first case is impossible (a subsequence cannot be longer and still have `s` as a prefix).

So only the **second rule matters**:

> At the first differing position, `t` must have `'('` while `s` has `')'`.

---

## 2. Key observation

To be better than `s`, the subsequence `t` must:

* Match `s` for some prefix,
* Then **skip a `')'` in `s` and instead use a later `'('`**.

That means:
👉 There must exist a position where `s[i] = ')'`, but later in the string there is an unused `'('` that we can pick.

---

## 3. Strategy

We want the **maximum length** valid subsequence `t`.

To achieve this:

1. **Remove a prefix** of `s` ending at some `')'`
2. From the remaining suffix, take the **longest possible regular bracket subsequence**

The optimal choice is:

* Remove the **shortest prefix ending at a `')'`** such that the remaining suffix still contains a regular bracket sequence.

Why?

* Shorter removal → longer remaining subsequence
* Skipping a `')'` immediately guarantees `t` is better than `s`

---

## 4. When is it impossible?

If **every prefix ending at `')'` leaves an invalid suffix**, then:

* No subsequence can be better than `s`
* Output `-1`

This happens when `s` is already lexicographically minimal, like:

* `()`
* `(())()`

---

## 5. Practical solution approach

For each test case:

1. Traverse the string from left to right.
2. Track balance of brackets.
3. Find the **first position `i` where `s[i] = ')'`** such that:

   * The suffix `s[i+1 ... n]` contains at least one valid RBS
4. Compute the length of the **longest RBS subsequence** in that suffix:

   * This is `2 × min(number of '(' , number of ')')`
5. Output that length.
6. If no such position exists → output `-1`.

---

## 6. Example walkthrough

### Example 1

```
s = ()
```

* Only valid subsequence is itself
* No way to be better
  ✅ Output: `-1`

---

### Example 2

```
s = (()(()))
```

* Skip the `')'` at position 3
* Remaining string can form `((()))`
* Length = 6
  ✅ Output: `6`

---

### Example 3

```
s = (())()
```

* Any skipped `')'` breaks validity of the suffix
* No better subsequence
  ✅ Output: `-1`

---

## 7. Time complexity

* Each test case is processed in **O(n)**
* Total complexity across all test cases is **O(Σn)** ≤ 2 × 10⁵
* Fully acceptable within constraints

---

## 8. Final takeaway

✔ You are not constructing the subsequence explicitly
✔ You are finding the **best possible suffix** after skipping one crucial `')'`
✔ If such a suffix exists → compute its maximum RBS length
✔ Otherwise → `-1`

This greedy observation is the core idea behind solving the problem efficiently.