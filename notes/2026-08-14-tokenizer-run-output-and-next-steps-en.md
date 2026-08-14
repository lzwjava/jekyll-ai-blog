---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenizer Run Output and Next Steps
translated: false
type: note
---

The tokenizer worked perfectly. Here's how to read that run and what comes next.

## 1. How to read the run output

```
training on 1 file(s)
streaming, capped at ~200000000 bytes     ← your --max-bytes took effect

[00:00:04] Pre-processing sequences   …  0 / 0
[00:00:06] Tokenize words             …  3,192,137 / 3,192,137   ← 3.19M unique words found
[00:00:04] Count pairs               …  3,192,137 / 3,192,137
[00:00:48] Compute merges            …  65,272 / 65,272         ← learned 65,272 BPE merges
saved tokenizer -> tok_mixed/
  vocab size = 65536
```

What each stage means:

- **Pre-processing sequences** — scanning the 200 MB stream, splitting into words.
- **Tokenize words** (3,192,137) — that's the count of **unique words** the trainer saw (each becomes a starting symbol). Huge because Chinese has no spaces, so many distinct character-sequences.
- **Count pairs** — counting which adjacent byte-pairs occur most often (drives which merges win).
- **Compute merges** (65,272) — repeatedly merge the most frequent pair until vocab reaches 65,536. This took ~48s (the slow part).
- **vocab size = 65536** — final vocab, and your 8 special tokens (`<|lang_en|>`, `<|lang_zh|>`, `<|mix_*|>`) occupy ids 0–7, verified in `vocab.json`.

The total wall time was ~58 s and peak RAM ~9 GB — safe. The earlier freeze is fully avoided.

## 2. What to do next (pipeline order)

You're now at step 3 of the README's "Real usage" flow. The remaining steps are:

**Step 4 — Measure the real token ratio** (sanity-check language balance):

```bash
python3.12 -m scripts.measure_token_ratio \
  --input mixed_sample_2gb.txt --out ratios.json --tok-prefix tok_mixed
```

Checks whether the EN/ZH *token* split matches what you want (doc-count ≠ token-count). If `zh_token_frac` is off, re-run `mix_bilingual.py` with a nudged `--zh-frac`.

**Step 5 — Tokenize → binary train/val** (`prepare.py`):

```bash
python3.12 -m scripts.prepare \
  --input mixed_sample_2gb.txt --tok-prefix tok_mixed --out-dir data --val-frac 0.1
```

This writes `data/train.bin` + `data/val.bin` (uint16 ids) that nanoGPT/nanochat consume.

⚠️ **Heads-up — `prepare.py` has the same memory trap we just fixed.** Look at its core:

```python
with open(a.input, "r", encoding="utf-8") as f:
    text = f.read()                      # ← loads the WHOLE file into RAM
ids = tok.encode(text).ids               # ← + another full copy of token ids
```

For the 2 GB sample that's ~2 GB text + ~2–4 GB of ids ≈ 6–8 GB → **ok on your 62 GB**. But if you ever point it at the full 11.5 GB `mixed.txt`, it'll need ~20–30 GB+ and could OOM again.

Want me to also patch `prepare.py` to **stream in chunks** (encode line-by-line / fixed blocks and append to the `.bin` files) so it's safe on any size corpus — same treatment as the tokenizer? That would make the whole pipeline safe for the full 11 GB `mixed.txt`.
