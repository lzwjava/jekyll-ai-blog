---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smoke test passed with Python 3.12
translated: false
type: note
---

Smoke test ran successfully end-to-end with system Python 3.12. ✅

**Results:**
- **make_synthetic** → `data/synthetic/{en,zh,aligned}.jsonl`
- **mix_bilingual** → 2000 docs, EN 50% / ZH 50% → `mixed.txt`
- **train_tokenizer** → joint tokenizer, vocab=357, control tokens added → `tok_mixed/`
- **measure_token_ratio** → wrote `ratios.json` (ZH ≈ 38.8% of tokens — confirms the README gotcha that doc-ratio ≠ token-ratio)
- **prepare** → `data/train.bin` (90KB) + `data/val.bin` (10KB)

I used the same Python 3.12 invocation (`python3.12 -m scripts.<name>`) that the project's own pycache files (`cpython-312`) expect. The full pipeline is working.

**Note:** this overwrote `mixed.txt` (now ~100KB of synthetic data instead of empty) and the synthetic tokenizer in `tok_mixed/`. When you move to the real 3.5GB `fineweb_edu_shard.jsonl`, you'll want to re-run the real pipeline (download the ZH shard, mix at large scale, train a full 65536-vocab tokenizer). Want me to spin that up too, or run the generation step?