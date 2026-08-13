---
audio: false
generated: true
image: false
lang: en
layout: post
title: "False alarm: uint16 fits 65536 vocab"
translated: false
type: note
---

That warning is a **false alarm — it's stale and doesn't match reality**. Here's the full story:

## What the warning *claims*
It says your model has >65535 tokens, so `prepare.py` would have to use `uint32`, making the `.bin` files twice as big (4 bytes/token instead of 2).

## Why it's actually wrong
`vocab_size = 65536` means token **ids run from 0 to 65535** — the highest id is exactly `65535`. And `numpy.uint16`'s max value is exactly `65535`. So everything fits comfortably in `uint16`.

`prepare.py` (the file that actually writes the `.bin`s) knows this — look at its logic:

```python
# numpy uint16 caps at 65535; the tokenizer top bound is 65536.
# If vocab_size is exactly 65536 we still fit in uint16 (max id 65535),
# but be safe once it exceeds that.
dtype = np.uint16 if vocab_size <= 65536 else np.uint32
```

So with your `--vocab-size 65536`:
- `prepare.py` **will use `uint16`** (compact, 2 bytes/token)
- your `train.bin` stays small
- **no uint32, no larger files**

The `WARNING` in `train_tokenizer.py` was written with an off-by-one (`> 65535` instead of `> 65536`) and contradicts `prepare.py`. It's purely cosmetic — you can ignore it.

Want me to fix the stale warning in `scripts/train_tokenizer.py` so it matches `prepare.py` (i.e. only warn when vocab actually exceeds 65536)? One-line change:

```python
if tok.get_vocab_size() > 65536:   # instead of > 65535
```

Say the word and I'll patch it.