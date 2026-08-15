---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting the Language Mix Ratio
translated: false
type: note
---

The language fraction is set at **data-mixing time** (before training), via `--zh-frac` in `mix_bilingual.py`. There's no runtime knob for the trained model — to change the balance you re-mix, re-prepare, and re-train.

## Where the current model's fraction came from

Your training corpus `mixed_sample_2gb.txt` was mixed at **73% Chinese docs** (127,507 en + 345,837 zh). That's why the model leans Chinese. The knob used was `--zh-frac 0.73`.

## Setting the fraction — the workflow

```bash
cd /mnt/data/bilingual-gpt

# 1. Mix with your desired ZH *doc* fraction (0..1)
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0

# 2. Measure the *token* fraction (this is what the model actually sees)
python3.12 -m scripts.measure_token_ratio --input mixed.txt --out ratios.json \
    --tok-prefix tok_mixed
#   look at "zh_token_frac" in ratios.json

# 3. Nudge --zh-frac until zh_token_frac matches your target, then:
python3.12 -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536
python3.12 -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
# 4. Re-train the nanoGPT model from scratch (corpus changed)
```

## The gotcha: doc-frac ≠ token-frac

`--zh-frac` is a **document sampling probability**, not a token ratio. Chinese text tokenizes into fewer tokens per doc, so a 50/50 doc split is ~47% zh tokens. From your repo's own measurements (smoke mix): `tokens_per_doc_en = 4245`, `tokens_per_doc_zh = 3919` (~92% of en). So:

| Want zh token frac | Set --zh-frac ≈ |
| --- | --- |
| 50% (balanced) | 0.51–0.52 |
| 60% | 0.62 |
| 71% (current model) | 0.73 |

Quick formula: `zh_token_frac ≈ 0.92·zh_frac / (0.92·zh_frac + 1 − zh_frac)`, verified by step 2.

## Alternative: continuous mix knob (needs different data)

There's also the code-switch path for a *continuous* ratio at generation time (`--mix-frac 0.75` with `<|mix_75|>` tags) — but it requires **sentence-aligned parallel data** (e.g. WMT zh-en) fed through `build_codeswitch.py`, and the model must be trained on those `<|mix_N|>` docs. Your current model was not trained on them, so it can't do this yet (that's why `codeswitch.txt` sits unused).

**Bottom line:** pick the token fraction you want (step 2 tells you the truth), set `--zh-frac` accordingly, and re-run mix → tokenizer → prepare → train. Want me to re-mix at a specific ratio (e.g. a true 50/50 token split) and kick off a retrain?
