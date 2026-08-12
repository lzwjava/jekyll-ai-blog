---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual Corpus Pipeline for nanoGPT
translated: false
type: note
---

This is a **Python** data-prep project (not Node). It's a bilingual EN/ZH corpus pipeline for nanoGPT/nanochat. Here are the commands to get it running:

**First, install dependencies:**
```bash
pip install -r requirements.txt
```

**Option A — smoke test (no downloads needed), the fastest way to verify it runs:**
```bash
python -m scripts.make_synthetic       --out_dir data/synthetic
python -m scripts.mix_bilingual        --en data/synthetic/en.jsonl --zh data/synthetic/zh.jsonl --zh-frac 0.5 --out mixed.txt --limit 2000
python -m scripts.train_tokenizer      --input mixed.txt --out-prefix tok_mixed --vocab-size 2048
python -m scripts.measure_token_ratio  --input mixed.txt --out ratios.json --tok-prefix tok_mixed
python -m scripts.prepare              --input mixed.txt --tok-prefix tok_mixed --out-dir data
```

**Option B — real pipeline.** Note you already have a 3.5GB `fineweb_edu_shard.jsonl` on disk, but `mixed.txt` is currently empty (0 bytes), so it hasn't been mixed yet. Run:

```bash
# 1. Grab ZH shard (you already have the EN shard)
python3.12 -m scripts.download_shards --source zh --out fineweb2_cmn_shard.jsonl

# 2. Mix EN/ZH with your language ratio knob
python -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0

# 3. Check real token ratio, then tune --zh-frac if needed
python -m scripts.measure_token_ratio --input mixed.txt --out ratios.json --tok-prefix tok_mixed

# 4. Train a joint bilingual BPE
python -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536

# 5. Tokenize -> binary train/val
python -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
```

**Once training is done, generate with language control:**
```bash
python -m scripts.generate --model out/ckpt.pt --tok-prefix tok_mixed --lang zh \
    --prompt "机器学习是什么？" --max-new-tokens 200
```

---

**Quick start recommendation:** start with **Option A** — the smoke test runs end-to-end in seconds and confirms the toolchain works before you spend time on the big 3.5GB shard. Then move to Option B for the real corpus. If you let me know your goal (e.g. "just verify it runs" vs "produce a tiny train.bin to train on"), I can give you a single combined command.