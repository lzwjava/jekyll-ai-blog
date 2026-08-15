---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual Generation End-to-End Verified
translated: false
type: note
---

Generation works end-to-end. Here's the full picture:

## How to generate from the checkpoint

I wrote `generate_bilingual.py` in `/mnt/data/nanoGPT/` (handles the `_orig_mod.` compile-prefix that the repo's `scripts/generate.py` would choke on, and uses the bilingual tokenizer + language knob):

```bash
cd /mnt/data/nanoGPT

# Chinese mode
./venv/bin/python generate_bilingual.py --lang zh --prompt "机器学习是什么？" --max-new-tokens 200

# English mode
./venv/bin/python generate_bilingual.py --lang en --prompt "Machine learning is" --max-new-tokens 200

# Tuning knobs
./venv/bin/python generate_bilingual.py --lang zh --prompt "如何学习编程？" \
    --temperature 0.9 --top-k 200 --num-samples 3 --seed 42
```

## What I verified before/during generation

- **Checkpoint**: iter 4500/5000, best val loss 4.368, 232M params, saved 17:12:56. ⚠️ **No training process is running now** — GPU is idle (10.6 GB free). It stopped before the ~19:40 ETA. If you want the last 500 iters, `./venv/bin/python train.py --init_from=resume --out_dir=out-bilingual` will pick up at 4500.
- **Consistency check (the important one)**: the control tokens are *not* single vocab entries — the special-token registry is lost when the tokenizer is saved as `vocab.json`+`merges.txt`, so `<|lang_zh|>` encodes to the byte-BPE fragment `[510, 730, 70, 1126, 509]`. I confirmed `train.bin` contains exactly those fragment sequences (320k zh + 127k en tags), so training and generation see *identical* ids → the knob works, just as a weaker 5-token signal instead of a single control token. If you ever retrain, fix this by saving the tokenizer with `save_pretrained()` (keeps special-token metadata).

## Sample outputs (all real, from iter-4500 checkpoint)

- **zh-tag + "机器学习是什么？"** → fluent Chinese Q&A ("机器学习是一个从无到有的过程…最终形成科学的知识体系…")
- **en-tag + "Machine learning is"** → coherent English essay on ML algorithms
- **Knob demo — same English prompt, both tags**: both continue in English (prompt language dominates), but zh-tag shifted to story/novel register while en-tag produced a tech-article. On Chinese prompts, the zh-tag yields fiction, en-tag yields article/marketing prose.
- The 2 GB corpus is zh-heavy (~2.7:1 tags), so ambiguous prompts lean Chinese.

**Bottom line**: the bilingual model generates coherent text in both languages with a working (if soft) language knob. The main loose ends are the truncated training run (4500/5000) and the tokenizer special-token bug for any future retrain.
