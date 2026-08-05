---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual GPT Pipeline Ready
translated: false
type: note
---

Done. I turned your Q&A answer into a runnable, tested prep-and-generation pipeline in `/mnt/data/bilingual-gpt`, committed to git.

## What's there

| File | Job |
| ------ | ----- |
| `scripts/mix_bilingual.py` | EN/ZH doc mixing with `--zh-frac` + `<\|lang_en\|>` / `<\|lang_zh\|>` control tokens |
| `scripts/measure_token_ratio.py` | tokenizes the corpus and reports the *real* token ratio (your "don't trust doc-count" point) |
| `scripts/train_tokenizer.py` | fresh joint byte-level BPE with control tokens registered as specials |
| `scripts/prepare.py` | nanoGPT-style `train.bin` / `val.bin` (auto uint16→uint32 if vocab >65536) |
| `scripts/generate.py` | generation-time `--lang` (binary) and `--mix-frac` (continuous) knobs |
| `scripts/build_codeswitch.py` | code-switched docs bucketed `<\|mix_0/25/50/75/100\|>` for the continuous knob |
| `scripts/make_synthetic.py` | synthetic EN/ZH/parallel data so you can smoke-test without downloading FineWeb |
| `README.md`, `requirements.txt`, `.gitignore` | docs + deps |

## Verified end-to-end

Ran the full chain on synthetic data: **50/50 doc split produced only ~38.8% ZH *token* ratio** — the exact insight from your answer, now measured automatically so you can nudge `--zh-frac` to hit a target.

## Bugs I caught while making it runnable

- `mix_bilingual.py` had a `KeyError` (yielded the expanded token string, then `main` re-indexed `LANG_TOK` by it).
- `measure_token_ratio.py` assumed control-token + text on one line, but the mixer writes them on separate lines — rewrote it as a structure-aware doc parser; also fixed a regex that matched `...\|` instead of the real `...\|>` ending, and a group that captured `lang_en` instead of `en`.
- `build_codeswitch.py`: `nearest_bucket()` treats input as a 0..1 fraction, but `main` passed it absolute buckets — everything non-zero collapsed to `<\|mix_100\|>`. Now builds the tag directly per explicit bucket.

## To run for real

```bash
pip install -r requirements.txt
python -m scripts.mix_bilingual --en fineweb_edu_shard.jsonl --zh fineweb2_cmn_shard.jsonl --zh-frac 0.5 --out mixed.txt
python -m scripts.measure_token_ratio --input mixed.txt --out ratios.json --tok-prefix tok_mixed   # iterate --zh-frac
python -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536
python -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
# then feed data/train.bin + data/val.bin into nanoGPT, or point nanochat's tok_train.py at mixed shards (add the control tokens to its special-token list)
```

Want me to wire in a minimal nanoGPT training loop that reads `data/train.bin` and imports the `generate.py` knob next?
