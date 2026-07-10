---
audio: false
generated: true
image: false
lang: en
layout: post
title: Long Prompt Code Generation Analysis
translated: false
type: note
---

Results in `/mnt/data/zz/codeparrot/eval_long/results/long_prompt_results.log`. Here's the breakdown:

**Sample 1 — BinarySearchTree**
Generated `insert`, `search`, `delete`, `__str__`, `__repr__`, `__len__`, `__iter__`, `__getitem__` — impressive dunder coverage. The `insert()` is wrong (inserts to both left + right child), but it knew to create `TreeNode(val)` and check `self.root is None`. The shape is there, the logic is not.

**Sample 2 — longest_common_subsequence**
Recognized DP, created the 2D table. But the recurrence `dp[i][j] = max(dp[i][j], dp[i][j + 1])` is wrong — no character comparison. Then it degenerated into repeating the same function with longer names.

**Sample 3 — timer_decorator — ✓ Correct**

```
def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print("Execution time: %.2f seconds" % (end - start))
    return result
return wrapper
```

Then repeats itself 5 more times with slight name variations.

**Sample 4 — load_json_data — ✓ Mostly correct**
Proper `try/except` with `FileNotFoundError` + `json.decoder.JSONDecodeError` handling. Then degenerate into `load_csv_data`, `load_csv_data_from_json`, etc.

**Sample 5 — is_prime — ✓ Correct**, `prime_factors` — ✗ wrong

**Sample 6 — APIClient — ✓ Best sample**
Generated `get`, `post`, `put`, `delete` methods all with consistent error handling pattern. Nearly identical method bodies (copy-paste pattern). Recognized `requests.Session()`, headers, `response.json()`.

**Sample 7 — clean_and_transform**
Started well: `drop_duplicates()`, numeric column selection. Then degenerated into `apply(lambda x: x.lower().strip())` on numeric columns — nonsense.

**Sample 8 — fetch_url — ✓ Correct**
`async with session.get(url)`, `await response.json()`. Then degenerated into `fetch_json_async_async_async_async...`.

**Summary pattern across all 8:**

- First **50-100 tokens** of continuation are often reasonable or correct
- Then **degeneration** kicks in — repeating the first successful pattern with slight variations
- The model learned **code structure** well (indentation, imports, class/method patterns, try/except, decorators, async)
- But **semantic correctness** degrades rapidly with length — capacity bottleneck at 286M params
- The degeneration is exaggerated by greedy sampling (temperature=0.3) — deterministic mode amplifies repetition loops
