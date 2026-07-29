---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Qwen Model Outputs
translated: false
type: note
---

The output is structured like this (broken down for clarity):

---

### 1️⃣ The progress bar

```
Generating: 100% | ... | 2/2 [00:47<00:00, 23.84s/it, Prefill=535tok/s, Decode=4tok/s]
```

- `2/2` — 2 prompts processed ✅
- `Prefill=535tok/s` — prompt encoding speed (fast)
- `Decode=4tok/s` — generation speed (slow, typical for CPU/limited GPU)

### 2️⃣ The two completions (separated by `---`)

#### Completion 1 — "introduce yourself"

```
---
Completion: <think>
...introduces itself...
</think>

Hello! I'm a language model...
---
```

- The model is using **chain-of-thought reasoning** inside `<think>...</think>` tags (a feature of Qwen models).
- The actual **final answer** comes **after** `</think>`.

#### Completion 2 — "list all prime numbers within 100"

```
---
Completion: <think>
Okay, so I need to list all the prime numbers between 100. Let me start...
...
```

- This output appears **cut off / truncated**. The model started reasoning but didn't finish generating — likely because `max_tokens=256` was hit or the output was clipped by the terminal.

---

### ❓ The `flash_attn` error

```
ModuleNotFoundError: No module named 'flash_attn'
```

- `flash_attn` is an **optional** CUDA kernel for faster attention. It's not required.
- Since you set `enforce_eager=True`, the model runs fine **without it**, just slower.

---

### 💡 How to read the answers

| Part | Meaning |
| --- | --- |
| `<think>...</think>` | Model's internal reasoning (like a scratchpad) |
| Text **after** `</think>` | The **final answer** the model outputs to the user |

To get **clean output** (strip the thinking), you could modify the script:

```python
text = output['text']
if '</think>' in text:
    text = text.split('</think>', 1)[-1].strip()
print(f"Completion (clean): {text}")
```

Want me to apply that change?
