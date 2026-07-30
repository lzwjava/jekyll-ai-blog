---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reading a Scheduler Trace
translated: false
type: note
---

Now I have the full picture. Let me explain every field in that trace.

---

## How to Read the Scheduler Trace

Each line during **DECODE** (or **PRE-FILL**) looks like:

```
seq[  7] prompt_len=    6 total_len=   65 blocks=  1 cached=   64 scheduled=   1 blocks=[7]
```

Here's what every field means:

### `seq[7]`

The sequence ID. Each request gets one. IDs are assigned in order of `add_request()`.

### `prompt_len=6`

**Number of prompt (input) tokens** — never changes for a given sequence.

### `total_len=65`

**Total tokens in this sequence right now** (prompt + generated so far). Grows by 1 each decode step as a new token is appended.

### `blocks=1`

**Number of physical KV cache blocks allocated** to this sequence. With `block_size=256`, the formula is:

```
blocks = ceil(total_len / 256)
```

So for `total_len=65` → `ceil(65/256) = 1` block. Even for `total_len=211` → `ceil(211/256) = 1` block.
That's why you see `blocks=1` even with 211 tokens — they all fit in one 256-slot block.

### `cached=64`

**Number of tokens that have already been consumed as input by the model.** Think of this as "how many tokens have been processed/forward-passed so far." It counts all tokens the model has already seen — both prompt tokens AND previously generated tokens that were fed back as input.

### `scheduled=1`

**Tokens to be processed in this step.** During decode, this is always 1 (generate the next token). During prefill, this can be >1 (the remaining prompt tokens to process in one shot, or a chunk if chunked prefill is happening).

---

## Why `cached` > `prompt_len` — The Key Confusion

This is the most important thing to understand. For `seq[7]` with `prompt_len=6`:

```
Step     cached     total_len     What happened
──────────────────────────────────────────────────
Prefill      6            7      Model processes all 6 prompt tokens, appends 1 generated token
Decode 1     7            8      Model takes the 7 tokens as input, appends 1 more
Decode 2     8            9      ...
Decode n     n+6          n+7    (after n decode steps)
```

So when you see `cached=64, total_len=65`:

| Field | Value | Meaning |
| --- | --- | --- |
| `prompt_len` | 6 | Original prompt tokens |
| `cached` | 64 | 6 prompt + 58 previous outputs the model has already consumed as input |
| `total_len` | 65 | 6 prompt + 59 generated tokens exist in the buffer |
| `scheduled` | 1 | The model is about to process token #64 as input to produce token #65 |

**`cached` = tokens the model has already seen for this sequence (as input).**
**`total_len` = tokens currently stored in the sequence buffer (prompt + all generations).**
**The 1-token gap** (total_len - cached = 1) is the **most recently generated token** that hasn't been fed back as input yet — it will be consumed on the next decode step.

---

## The Full Trace Walkthrough for seq[7]

```
DECODE: seq[7] total_len=65 cached=64 scheduled=1   ← model consumed 64 tokens, produces #65
DECODE: seq[7] total_len=66 cached=65 scheduled=1   ← model consumed 65 tokens, produces #66
DECODE: seq[7] total_len=67 cached=66 scheduled=1
DECODE: seq[7] total_len=68 cached=67 scheduled=1
DECODE: seq[7] total_len=69 cached=68 scheduled=1
FINISHED: seq[7] prompt=6 + generated=64 = 70 total
```

The finished line confirms: `6 prompt + 64 generated = 70 total`. After the last decode step (total_len=69 → becomes 70 after appending), the sequence hits `max_tokens=64` and finishes.

---

## Why `blocks=1` Seems Suspicious

With `block_size=256`, the sequence only crosses into a **second block** when `total_len > 256`. For these short sequences (70 tokens max), they all fit in a single block. This is expected — small models with small prompts don't need many KV cache blocks.

The "PagedAttention" advantage really shines when sequences are **long** (thousands of tokens) and their KV caches would normally waste memory due to fragmentation. Here the sequences are tiny, so you only see 1 block per sequence.
