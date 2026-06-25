---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whitespace Collapse Overwhelms Context
translated: false
type: note
---

Here's what the 613-token context produced. Let me break down just the continuation (after the prompt ends):

**Sample 1:**
```
free(classroom[i]->name);
                             data(s, &n, &n,->n1);
```
Then ~250 chars of pure whitespace.

**Sample 2:**
```
free(classroom[i]->name);
          if(p->size() == 1)
```
Then ~250 chars of pure whitespace.

**Sample 3:**
```
free(classroom[i]->name);
              = 1;
              m[i - i] + 1] + 1_t;
```
Then ~200 chars of pure whitespace.

### What's happening

**The good news still holds.** With 613 tokens of context, the model produces actual C/C++ tokens — `data(s, &n, &n,->n1)`, `if(p->size() == 1)`, `m[i - i] + 1]` — these are syntactically plausible fragments. It even tries to stay in the right *register*: after a `free()` call inside a loop, it generates more C statements. That's context conditioning working.

**But three clear problems remain visible:**

1. **It can't complete the trivially obvious next line.** The prompt ends at `free(classroom[i]->name);` — any human would write `free(classroom[i]); }` next. The model can't. It generates something syntactically adjacent but semantically wrong (`data(s, &n, &n,->n1)`). This is the 124M + PPL 32 symptom: it has enough local statistics to produce *a* C statement, but not enough to produce *the right* C statement.

2. **It collapses to whitespace after ~10 tokens of continuation.** All three samples generate a single line of pseudo-C, then pad with 200+ whitespace characters. This is the model's **whitespace prior** reasserting itself. It has enough context to "start" a continuation, but after 10 tokens the context signal fades and it falls back to the dominant pattern in the training data: whitespace and indentation. This is directly from the data quality problem — github-code has massive whitespace runs (license headers, blank lines, indentation), and the model's strongest prior is "when uncertain, emit whitespace."

3. **The `_`-soup is milder now but still present.** `_t` in sample 3, `->n1` in sample 1. These are BPE-shredded identifier fragments. Less dominant than with a 3-token context, but still visible.

### Diagnosis update

The 613-token test confirms the earlier answer's diagnosis, with one refinement:

- **"Living, undertrained, badly-tokenized"** — confirmed. The model is clearly conditioning on context (C tokens after C prompt, not `<div>` tags), but can't sustain it.
- **The whitespace collapse** is worse than the earlier answer suggested. Even with 613 tokens of context, the model generates ~10 tokens of pseudo-code and then falls into a whitespace hole. This means the whitespace problem is NOT just a short-context artifact — it's a **data distribution problem** that persists at any context length. The model has learned "whitespace is the most common thing to emit" and it can't escape that prior even with rich context. This makes the data cleaning lever even more important than the earlier answer ranked it.

### Revised priority ranking

| Rank | Lever | Why |
|------|-------|-----|
| 1 | **Data cleanup** | The whitespace collapse at 613 tokens proves data quality is the #1 problem. Whitespace-heavy training data → whitespace-prior model. |
| 2 | **Tokenizer** | Still matters — `_t`, `->n1` are BPE artifacts. But less critical than the data problem. |
| 3 | **Train longer** | Only useful after #1 and #2 are fixed. |

### One more thing to try

Run with `temperature=0.0` (greedy) on this same prompt. If greedy also collapses to whitespace after 10 tokens, it's definitely the data/weights problem (the model *assigns highest probability* to whitespace). If greedy produces a full function, then it's a sampling problem and the weights are better than they look.
