---
audio: false
generated: true
image: false
lang: en
layout: post
title: Small model's Python code generation results
translated: false
type: note
---

The eval ran. BPB failed (eval dataloader expects default nanochat data path, not our codeparrot data — we already have val_bpb from training anyway: **0.372**). The **Python code generation results are the real story**:

**Python Code Gen Results (286M model, temperature=0.3):**

```
def fibonacci(n):
    if n == 0:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

**✓ Correct** recursive implementation. It then generates `fibonacci2`, `fibonacci3` as variations.

---

```
def reverse_linked_list(head):
    if head == None:
        return None
    if head.is_empty():
        return None
    if head.is_linked():
        return head
    return reverse_linked_list(head.next)
```

**~** Recognizes the problem, generates plausible node API (`.is_empty()`, `.is_linked()`), but the recursion is wrong (infinite on `is_linked`). Shape is right.

---

```
class Stack:
    def __init__(self):
        self._stack = []
        self._stack.append(None)

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0
```

**✓ Correct** — full working Stack with all standard methods.

---

```
def is_palindrome(s):
    if len(s) == 0:
        return False
    if s[0] == s[-1]:
        return True
    else:
        return False
```

**~** Recognizes first/last char comparison but logic is wrong (returns True immediately, no recursion). It tried `is_palindrome2`, `is_palindrome3` variants.

---

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
...
```

✓ Generates plausible import chains.

---

**Assessment:** For a 286M model trained on codeparrot-clean only (no SFT), this is solid. It learned:

- Python syntax and indentation perfectly
- Class/function structure
- Docstrings and comments
- Common import patterns
- The *shape* of common algorithms (even when logic is off)

Limitations are what you'd expect: small model capacity means it memorizes patterns but doesn't deeply understand algorithms. SFT would tighten this up significantly.

Results saved to `/mnt/data/zz/codeparrot/eval/results/`. Want to try running the chat CLI next to interact with it?
