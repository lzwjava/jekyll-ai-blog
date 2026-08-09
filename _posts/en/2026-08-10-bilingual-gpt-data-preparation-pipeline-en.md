---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual GPT Data Preparation Pipeline
translated: false
type: note
---

This is a **data-prep pipeline for training a bilingual (English/Chinese) GPT from scratch**. Here's how it works, end to end:

## The core idea

You can't just train on a pile of mixed EN+ZH text and expect to control *which language the model speaks at generation time*. This repo's trick: **tag every document with a control token** (the same trick as CTRL control codes / NLLB language tokens), so the language choice becomes a *conditional* the model learns.

```
<|lang_zh|>
{text}
<|endoftext|>
```

Then at inference, you simply prepend `<|lang_zh|>` to the prompt and the model stays in Chinese; `<|lang_en|>` and it stays in English.

## The pipeline (each script is one stage)

```
en.jsonl ─┐
          ├→ mixed.txt ─→ tok_mixed/* ─→ data/train.bin / val.bin
zh.jsonl ─┘     (docs     (fresh joint  (tokens, nanoGPT
                wrapped    byte-level     .bin format)
                in tags)   BPE)
```

1. **`download_shards.py`** — Pulls one shard each from HuggingFace: `fineweb-edu` (EN) and `fineweb-2`'s `cmn_Hani` (ZH, Mandarin, simplified), and normalizes both to a `{"text": ...}` jsonl so one mixer handles either.

2. **`mix_bilingual.py`** — The language-ratio knob. For each doc, it flips a coin: with probability `--zh-frac` it draws from the ZH shard, else EN. It writes each doc wrapped in `<|lang_zh|>`/`<|lang_en|>` + `<|endoftext|>`.

3. **`measure_token_ratio.py`** — *Important gotcha*: `--zh-frac` is a **doc** ratio, not a **token** ratio. Chinese tokenizes to fewer tokens per byte of text, so a 50/50 doc split might be ~39% ZH by tokens (which is exactly what your `ratios.json` shows: `zh_doc_frac = 0.50` but `zh_token_frac = 0.39`). This script tokenizes the corpus and reports the real token breakdown so you can nudge `--zh-frac` until the *token* balance matches.

4. **`train_tokenizer.py`** — Trains a **fresh joint byte-level BPE** with the control tokens registered as special tokens (so they never get split). This is deliberate: GPT-2's tokenizer fragments Chinese into ~3 tokens/char, wasting context; a fresh BPE on the mixed corpus learns real Chinese merges.

5. **`prepare.py`** — nanoGPT's classic step: tokenize everything once, split 90/10, write `train.bin`/`val.bin` of `uint16` ids (switches to `uint32` if vocab > 65536). These are trainable directly by [nanoGPT](https://github.com/karpathy/nanoGPT).

6. **`generate.py`** — The payoff. Loads a trained nanoGPT checkpoint + tokenizer, prepends the language tag (or a `--mix-frac` knob), and samples.

## The optional second knob (continuous mixing)

`build_codeswitch.py` goes beyond pure EN/pure ZH. Given a **sentence-aligned parallel corpus** (e.g. WMT zh-en), it interleaves EN and ZH sentences at a target ratio `r` and tags the doc `<|mix_0|>` … `<|mix_100|>`. Then `--mix-frac 0.75` tells the model "~75% Chinese here" — it produces genuinely code-switched output. The README notes the real constraint is the data (sentence-aligned parallel text), not the model.

## Current state of the repo

- A full 3.5 GB `fineweb_edu_shard.jsonl` EN shard is downloaded and sitting in the repo root (`ratios.json` shows you did a smoke-test run with synthetic data: 2000 docs, ~28k tokens).
- `data/train.bin` + `val.bin` and a `tok_mixed/` tokenizer (vocab 2048) exist from that smoke test.
- The `config/` dir is empty — no training config has been written yet, and nothing has been trained (that's the next step: point a nanoGPT config at `data/` and run the training loop).

Want me to walk through any specific part in more detail, or should I run the synthetic smoke test to show the pipeline working end to end?
