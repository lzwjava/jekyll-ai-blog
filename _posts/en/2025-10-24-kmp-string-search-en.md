---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: KMP Algorithm Efficient String Search
translated: false
type: note
---

### Understanding the Knuth-Morris-Pratt (KMP) Algorithm

You're spot on with your intuition: KMP is all about **not wasting partial matches** during string searching. When you're looking for a pattern (like "abc") in a longer text (like "ababcabc"), the naive approach restarts from scratch every time there's a mismatch, which is inefficient. KMP smartly "remembers" how much of the pattern you've already matched and jumps ahead, avoiding redundant comparisons. This makes it super fast—linear time, O(n + m), where n is text length and m is pattern length.

I'll break it down step-by-step with a simple example. We'll search for the pattern `P = "abab"` in the text `T = "ababababc"`. (It appears at positions 0 and 2.)

#### Step 1: The Problem and Naive Approach

- **Goal**: Find all starting positions where `P` fully matches in `T`.
- **Naive way**: Slide `P` over `T`, comparing character by character. If mismatch at position i in `P`, shift `P` by 1 and retry from the beginning of `P`.
  - For our example:
    - Start at T[0]: "a"=="a" (match), "b"=="b" (match), "a"=="a" (match), "b"=="b" (match) → Found at 0.
    - Shift to T[1]: "b"=="a"? No → Restart `P` at beginning. Waste!
    - T[2]: "a"=="a", "b"=="b", "a"=="a", "b"=="b" → Found at 2.
    - T[3]: "a"=="a", "b"=="b", "a"=="a", "b"=="a"? No → Restart.
    - And so on. Lots of backtracking to char 0 of `P`.

This can be O(n*m) in the worst case (e.g., searching "aaaaa...a" for "aaa...ab").

#### Step 2: KMP's Key Idea – The Prefix Table (or "Failure Function")

KMP precomputes a table `π` (pi) for the pattern `P`. This table tells you, for each position i in `P`, **the longest proper prefix of `P[0..i]` that is also a suffix**. In other words: "If we mismatch here, how much of the partial match can we reuse by jumping to this overlapping prefix?"

- **Proper prefix/suffix**: A prefix/suffix that isn't the whole string (e.g., for "aba", prefix "a" matches suffix "a").
- Why? It lets you "slide" the pattern by more than 1 on mismatch, reusing the overlap instead of restarting.

For `P = "abab"`:

- Build `π` step by step (we'll code this soon).

| Position i | P[0..i] | Longest proper prefix = suffix | π[i] |
|------------|---------|--------------------------------|------|
| 0          | "a"     | None (single char)             | 0    |
| 1          | "ab"    | None                           | 0    |
| 2          | "aba"   | "a" (prefix "a" == suffix "a") | 1    |
| 3          | "abab"  | "ab" (prefix "ab" == suffix "ab") | 2  |

- π[2] = 1 means: If you matched "aba" but mismatch on next char, pretend you matched the prefix "a" (length 1) so far.
- π[3] = 2 means: For full "abab", overlap of "ab".

#### Step 3: Building the Prefix Table (π)

This is done in O(m) time. It's like searching `P` against itself, using a similar logic.

Pseudocode:

```
def compute_prefix_function(P):
    m = len(P)
    pi = [0] * m
    k = 0  # Length of current prefix-suffix match
    for i in range(1, m):
        while k > 0 and P[k] != P[i]:
            k = pi[k-1]  # Jump to previous overlap (reuse!)
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi
```

- Start with π[0] = 0.
- For each i=1 to m-1:
  - Try to extend the current match length k.
  - If mismatch, fall back to π[k-1] (don't waste—reuse prior overlap).
  - If match, k++.

For "abab":

- i=1: P[0]='a' != P[1]='b' → k=0, π[1]=0.
- i=2: P[0]='a' == P[2]='a' → k=1, π[2]=1.
- i=3: P[1]='b' == P[3]='b' → k=2, π[3]=2.

#### Step 4: Searching with the Prefix Table

Now search `T` with `P` and `π`:

- Keep a variable `q` = current state (length of matched prefix so far).
- For each char in `T`:
  - While mismatch and q>0, set q = π[q-1] (jump back smartly).
  - If match, q++.
  - If q == m, found! Then q = π[q-1] to continue for overlaps.

Pseudocode:

```
def kmp_search(T, P):
    n, m = len(T), len(P)
    if m == 0: return []
    pi = compute_prefix_function(P)
    q = 0
    matches = []
    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q-1]
        if P[q] == T[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)  # Starting position
            q = pi[q-1]  # Overlap for next search
    return matches
```

For `T = "ababababc"`, `P = "abab"`:

- i=0: 'a'=='a' → q=1
- i=1: 'b'=='b' → q=2
- i=2: 'a'=='a' → q=3
- i=3: 'b'=='b' → q=4 == m → Match at 0, q=π[3]=2
- i=4: Now q=2, T[4]='a' == P[2]='a' → q=3
- i=5: 'b'=='b' → q=4 == m → Match at 2, q=2
- i=6: q=2, 'a'=='a' → q=3
- i=7: q=3, 'b' != P[3]='b'? Wait, 'b'=='b' → q=4 == m? But T[7]='b', wait no: T="ababababc", i=6='a' (q=3), i=7='b'==P[3]='b' → q=4, but i=8='c' next.
- Actually: After second match at i=5 (pos 2), q=2, i=6='a'==P[2]='a' q=3, i=7='b'==P[3]='b' q=4 → Match at 4? Wait, let's trace fully.

Wait, correction on trace (full run yields matches at 0 and 2; at i=7: after q=4 at i=7? No:

- Up to i=3: match, q=2
- i=4: T[4]='a' (after "ababa"), P[2]='a' yes q=3
- i=5: T[5]='b' P[3]='b' q=4 → match at 2 (5-4+1=2), q=π[3]=2
- i=6: T[6]='a' P[2]='a' q=3
- i=7: T[7]='b' P[3]='b' q=4 → would be match at 4, but T[4:8]="abab" yes! Wait, T="a b a b a b a b c" positions 0-8.
- T[4:8] = "abab" yes, but in my T="ababababc", yes positions 4-7: a(4)b(5)a(6)b(7) = "abab" → third match at 4.
- Then i=8: 'c' != P[4]? But m=4, after match q=2, but since end, no more.

Wait, actually for this T, matches at 0,2,4. Yes!

See? On mismatches (like if there was one), it jumps q=π[q-1] instead of q=0.

#### Why It Feels Magical

- No backtracking in `T`—you only move forward.
- The "while" loop for mismatches runs amortized O(1) times total, because each jump decreases q, and q increases at most n times.

#### Try It Yourself: Simple Python Code

```python
def compute_prefix_function(P):
    m = len(P)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and P[k] != P[i]:
            k = pi[k - 1]
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi

def kmp_search(T, P):
    n, m = len(T), len(P)
    if m == 0: return []
    pi = compute_prefix_function(P)
    q = 0
    matches = []
    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q - 1]
        if P[q] == T[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q - 1]
    return matches

# Test
T = "ababababc"
P = "abab"
print(kmp_search(T, P))  # Output: [0, 2, 4]
```

Run this—tweak P/T to see jumps in action (add prints for q).

#### Common Pitfalls & Tips

- π[0] always 0.
- For patterns without self-overlaps (e.g., "abc"), π is all 0s—falls back to naive.
- Great for DNA sequences or code autocomplete.
- If still fuzzy, visualize the π as a "state machine": each state is matched length, transitions on match/mismatch.

This should click now—it's just smart skipping via precomputed overlaps. If you have a specific example that's tripping you up, share it!

[GeeksforGeeks: KMP Algorithm](https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/)
[Wikipedia: Knuth–Morris–Pratt Algorithm](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
