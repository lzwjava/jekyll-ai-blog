---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fixing Runtime Error in Codeforces 2190A
translated: false
type: note
---

**Question:** Why does this code get a Runtime Error on test 1 for Codeforces problem 2190A?

**Answer:**

Your code gets **Runtime Error** on test 1 mainly because of this critical logical error:

```java
for (i = 0; i < n; i++) {
    char target;
    if (i < zero) {
        target = '0';
    } else {
        target = '1';
    }
    if (s.charAt(i) != target) {
        positions.add(i);
    }
}
```

This logic assumes that after sorting, the string should become:

- first `zero` characters = '0'
- remaining `one` characters = '1'

But this is **not** what the problem asks for.

The problem requires the **lexicographically smallest** string you can obtain by **at most one** swap of two characters.

That means the target sorted string is **always**:

All '0's come **before** all '1's  
→ `000...0111...1` (exactly `zero` zeros followed by `one` ones)

But your code is comparing the **current** string against this ideal sorted string and collecting **all** mismatch positions.

This is completely wrong for the purpose of the problem, because:

- The problem allows **at most one swap** (0 or 1 swap)
- You are supposed to output either:
  - "Bob" (if already sorted / no swap needed or impossible with 1 swap)
  - "Alice" + **exactly two positions** to swap (1-based)

Your code almost always outputs **more than two positions** (or zero), which leads to:

- Wrong output format → judge expects either:
  - single line "Bob"
  - or two lines: "Alice" followed by **exactly two numbers**
- When it prints many numbers or wrong count → **Runtime Error** or **Wrong Answer**

### Real reasons for Runtime Error on test 1

Most probably test 1 is one of these simple cases:

```
1
3
010
```

or

```
1
4
1100
```

or

```
1
1
0
```

In such cases your code:

- Counts `zero` and `one`
- If all same → prints "Bob" (ok)
- Otherwise → goes into the `positions` collection logic
- Prints "Alice" and then **many positions** (or none)
- Judge expects either "Bob" or "Alice\nx y" → your output format is invalid → **Runtime Error**

### Correct idea (very brief)

You only need to find **at most one misplaced '1' before a '0'**.

The string is already good (Bob) if it is non-decreasing (all 0s before 1s).

Otherwise, you usually need to swap **one '1' that appears too early** with **one '0' that appears too late**.

Most common pattern: find the **leftmost '1'** that should be '0', and the **rightmost '0'** that should be '1', and swap them.

But you must check if after this one swap the string becomes sorted.

### Quick correct approach

```java
Read t
For each test:
    Read n, s
    Count zeros = count of '0'
    
    // Check if already sorted (non-decreasing)
    boolean sorted = true;
    for (int i = 1; i < n; i++) {
        if (s.charAt(i) < s.charAt(i-1)) {
            sorted = false;
            break;
        }
    }
    
    if (sorted) {
        out.println("Bob");
        continue;
    }
    
    // Find leftmost position where we have '1' but should be '0'
    int left = -1;
    for (int i = 0; i < zeros; i++) {
        if (s.charAt(i) == '1') {
            left = i;
            break;
        }
    }
    
    // Find rightmost position where we have '0' but should be '1'
    int right = -1;
    for (int i = n-1; i >= zeros; i--) {
        if (s.charAt(i) == '0') {
            right = i;
            break;
        }
    }
    
    // If we found both → one swap fixes it
    if (left != -1 && right != -1) {
        out.println("Alice");
        out.println((left+1) + " " + (right+1));
    } else {
        out.println("Bob");  // impossible with one swap
    }
```

This is not 100% complete (some edge cases need careful check), but it explains the direction.

Your current code is trying to do something completely different from what the problem asks, which is why it fails very early (test 1).

**References:**

- [https://codeforces.com/contest/2190/problem/A](https://codeforces.com/contest/2190/problem/A)