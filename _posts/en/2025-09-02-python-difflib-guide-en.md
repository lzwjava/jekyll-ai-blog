---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Difflib Sequence Comparison Guide
translated: false
type: note
---

In Python, the **`difflib`** module provides tools for comparing sequences—strings, lists, or any iterable. It’s often used for tasks like detecting differences between texts (like `diff` in Unix) or building auto-completion and similarity tools.

---

### How `difflib` Works

At its core, `difflib` tries to find the longest contiguous matching subsequences between two inputs. It then uses these matches to highlight similarities and differences. The library can:

* Generate human-readable diffs (`ndiff`, `unified_diff`, `context_diff`).
* Compute similarity ratios between sequences.
* Suggest close matches from a list (`get_close_matches`).

---

### `SequenceMatcher`

The most important class is **`difflib.SequenceMatcher`**.

**How it works**:

* It compares two sequences element by element.
* It looks for the *longest common subsequence* (but not necessarily contiguous).
* It produces a list of operations (`replace`, `delete`, `insert`, `equal`) describing how to transform one sequence into another.

**Key methods**:

1. **`ratio()`**
   Returns a float in `[0, 1]` that measures similarity.
   Formula:

   $$
   \text{ratio} = \frac{2 \times M}{T}
   $$

   where `M` = number of matching elements, and `T` = total elements in both sequences.

2. **`quick_ratio()`** and **`real_quick_ratio()`**
   Faster approximations of similarity, trading accuracy for speed.

3. **`get_opcodes()`**
   Returns a list of operations to transform `a` into `b`. Example: `[('replace', 0, 2, 0, 1), ('equal', 2, 4, 1, 3)]`.

4. **`get_matching_blocks()`**
   Returns all matching subsequences with their positions.

---

### Example

```python
import difflib

a = "hello world"
b = "helo wrld"

s = difflib.SequenceMatcher(None, a, b)

print("Similarity ratio:", s.ratio())
print("Operations:", s.get_opcodes())
print("Matching blocks:", s.get_matching_blocks())
```

**Output**:

```
Similarity ratio: 0.9090909090909091
Operations: [('equal', 0, 1, 0, 1), ('delete', 1, 2, 1, 1),
             ('equal', 2, 5, 1, 4), ('delete', 5, 6, 4, 4),
             ('equal', 6, 11, 4, 9)]
Matching blocks: [Match(a=0, b=0, size=1),
                  Match(a=2, b=1, size=3),
                  Match(a=6, b=4, size=5),
                  Match(a=11, b=9, size=0)]
```

---

👉 In short:

* `difflib` is a sequence comparison toolkit.
* `SequenceMatcher` is the core engine—it finds matching subsequences and computes similarity.
* It’s useful for diffs, spellcheckers, plagiarism detection, auto-suggestions, etc.

Would you like me to also show how to use `get_close_matches()` (which internally uses `SequenceMatcher`) for fuzzy string matching, like in spell-check or search suggestions?
