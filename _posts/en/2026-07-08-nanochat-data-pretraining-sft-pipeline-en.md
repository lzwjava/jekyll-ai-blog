---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NanoChat: Data Pretraining SFT Pipeline"
translated: false
type: note
---

Here's the full pipeline breakdown:

---

## Pipeline Overview

```
prepare_data.sh  →  fineweb-code-sec-gpt.sh  →  sft_code_sec.sh
   (data)                (pretrain)                (SFT)
```

---

## 1. Data Pipeline (`prepare_data.sh`)

**Sources** (3.2B total tokens):

| Source | Size | Content |
| -------- | ------ | --------- |
| github-code | 38 shards, ~3.9M files | Python, Go, SQL, JS, etc. |
| fineweb-edu | 8 train + 1 val shards | ~4.3B tokens CommonCrawl (filtered) |
| sec-edgar | 17 parquet files | 10-K filings text |

**Tokenizer**: BPE trained on 2B chars of mixed data, vocab=32768

**Data split**: last fineweb shard is validation, everything else is train. All symlinked into `nanochat-mixed/`.

---

## 2. Pretraining (`fineweb-code-sec-gpt.sh`)

**Architecture (d12)**:

| Param | Value |
| ------- | ------- |
| Layers | 12 |
| n_embd | 768 (depth × 64) |
| Heads | 6 (n_kv_head=6, MHA) |
| Vocab | 32,768 |
| Sequence | 2,048 |
| Window | L (sliding window, all layers) |
| **Total params** | **~110M** (embedding 25M + 12 blocks × 7M + final LN) |

The script header says "286M" but that's a stale estimate — actual is ~110M (embedding + 12 transformer blocks of ~7M each + tied LM head).

**Training config**:

| Setting | Value |
| --------- | ------- |
| Steps | 50,000 |
| Batch | 65,536 tokens/step |
| Device batch | 8 (grad_accum = 4) |
| Total tokens | 50k × 65K = **3.28B** |
| Data:param ratio | 29.8x (above Chinchilla 20x) |
| Duration | ~16.5h on RTX 4070 |
| Metric | val_bpb ~1.418 (from memory) |

**Sampling**: `--sample-every=5000`, `--save-every=5000`, `--eval-every=2000`

---

## 3. SFT (`sft_code_sec.sh`)

**Starting from**: pretrained d12 checkpoint at step 50,000

**SFT data**: SmolTalk (~460K general chat) + 1000 custom code/SEC examples + MMLU + GSM8K + SpellingBee

**Custom SFT examples** (`prepare_sft_data.py`): 14 generators, randomly sampled 1000 times:

- 5 code generators: Python (fib, quicksort, merge sort, API), Go (HTTP server), SQL (top customers), React (DataFetcher)
- 4 SEC generators: financial analysis, risk factors, revenue MD&A, financial ratios
- 3 general knowledge: compound interest, photosynthesis, water cycle

**SFT config**:

| Setting | Value |
| --------- | ------- |
| Steps | 8,985 (dataset exhausted, `num_iterations=-1`) |
| Batch | 65,536 tokens/step |
| Device batch | 4 |
| LR schedule | cosine: init_lr_frac=0.8, warmdown_ratio=0.5, final_lr_frac=0.0 |
| Duration | 184.7 min (~3h) |
| Eval | every 500 steps |
| **Val bpb** | **0.4053** (from 0.9536 at step 7) |

---

## 4. Inference Results in Context

Given the ~110M param scale and 3h SFT training, looking at the results again:

| Prompt | Verdict | Analysis |
| -------- | --------- | ---------- |
| **Palindrome code** | PASS | SFT data had 3 code generators with similar patterns. High probability continuation in code distribution. |
| **Capital of France** | PASS | Extremely common fact in web data. Small models memorize high-frequency n-grams. |
| **Gradient descent** | FAIL | ~110M can't store concept-level knowledge. Only high-frequency facts survive. |
| **2+2** | FAIL | Arithmetic requires working memory in activations. Transformer at this scale can't maintain state. |
| **Fibonacci** | FAIL | Pattern recognition requires multi-step reasoning. |
| **SQL query (2023)** | FAIL | The SFT SQL example uses `ORDER BY ... LIMIT` pattern, but the model didn't generalize to `YEAR(hire_date)`. |
| **Poem** | REPETITION | Softmax head gets stuck. Common at this scale — needs repetition penalty during inference. |
| **Average speed** | PARTIAL | Structured reasoning started correctly. The model knows the *form* of a math solution but loses one number. |

**Bottom line**: The SFT successfully taught chat format + code patterns. The ~110M param cap is the bottleneck — not the training. For the compute budget (3h SFT on RTX 4070), the result is exactly where it should be.
