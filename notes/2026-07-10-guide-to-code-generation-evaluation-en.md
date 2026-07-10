---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guide to Code Generation Evaluation
translated: false
type: note
---

The file structure is straightforward — here's how to read it:

**Delimiters:**

```
======================================================================
```

That `=` line separates each sample. Each sample starts with `<|bos|>` which is the beginning-of-sequence token.

**Reading pattern:**

1. Scroll down past the log/init lines (lines 1-5)
2. Each block between `======` lines is one generated sample
3. Inside each block: the **input prompt** is everything you gave it, then the **model's continuation** follows

**Example:**

```
<|bos|>def fibonacci(n):     ← prompt (what you gave)
    if n == 0:              ← model's generation
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    ...
```

Total: **8 samples** (fibonacci, reverse_linked_list, sort_dict_by_value, Stack, numpy import, CSV comment, is_palindrome, binary_search). To quickly jump between samples from the terminal:

```bash
grep '^====' -n /mnt/data/zz/codeparrot/eval/results/python_samples.log
```

That prints line numbers of all separators:

```
6:  ======  ← sample 1: fibonacci
24: ======  ← sample 2: reverse_linked_list
48: ======  ← sample 3: sort_dict_by_value
68: ======  ← sample 4: Stack
94: ======  ← sample 5: numpy import
116: ====== ← sample 6: CSV comment
120: ====== ← ...wait that's only 1 line for CSV? Let me check
139: ====== ← sample 7: is_palindrome
175:        ← sample 8: binary_search (trailing, no ===== at end)
```

Then read a specific sample by line range:

```bash
sed -n '6,23p' /mnt/data/zz/codeparrot/eval/results/python_samples.log
```

To evaluate whether a generation is good:

- **Syntax correct?** Run it through `python3 -c "compile(open('/dev/stdin').read(), '<test>', 'exec')"` and paste the code
- **Semantically correct?** Read through — does the function actually solve the problem?
- **Hallucination?** Does it reference APIs that don't exist? (e.g. `head.is_linked()` — plausible but not real)
- **Loop/recursion termination?** Will it infinite-loop or terminate?
