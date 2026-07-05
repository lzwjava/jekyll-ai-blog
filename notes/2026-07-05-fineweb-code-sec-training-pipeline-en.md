---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fineweb-Code-SEC Training Pipeline
translated: false
type: note
---

## Comprehensive Summary — code-sec-fineweb Project

### What We Built

A complete training pipeline: raw data → pretrained model → SFT fine-tuning.

### Phase 1: Data Pipeline — `/mnt/data/zz/prepare_data.sh`

| Dataset | Source | Format | Size | Purpose |
| --- | --- | --- | --- | --- |
| **github-code** | `codeparrot/github-code` (38 of 1126 shards) | Parquet, `content` col → converted to `text` col | 11 GB | Code understanding (Python, JS, Go, etc.) |
| **sec-edgar** | SEC 10-K filings (17 files) | Parquet, extracted `text` column | 2.6 GB | Financial document understanding |
| **fineweb-edu** | `HuggingFaceFW/fineweb-edu` (9 shards) | Parquet, `text` column | 20 GB | General web text knowledge |
| **Merged** | All 3 datasets symlinked into one dir | 64 parquet files (63 train + 1 val) | 34 GB | Mixed training data |

Conversion scripts:

- `scripts/extract/convert_github_code_for_nanochat.py` — renames `content`→`text` col
- `scripts/extract/convert_sec_edgar_for_nanochat.py` — extracts `text` column
- Tokenizer trained on mixed data: `python -m scripts.tok_train` (32k vocab, 2B chars)

### Phase 2: Pretraining — 16.5 hours on RTX 4070

```
bash /mnt/data/zz/fineweb-code-sec-gpt.sh
```

**Model:** d12 (286M params), n_embd=768, n_head=6, seq_len=2048, window=L

**Training progression:**

```
Step   5000 | val_bpb: 1.680 | loss: 1.397 | 1.6h
Step  25000 | val_bpb: 1.568 | loss: 1.136 | 8.2h
Step  50000 | val_bpb: 1.418 | loss: 1.062 | 16.5h
```

Checkpoints: `/home/lzw/.cache/nanochat/base_checkpoints/d12/` (5k intervals, 793MB each)

### Phase 3: SFT Fine-tuning — Running Now

```
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh
```

**Base model:** d12 step 50k → fine-tuned on chat conversations

**SFT data mixture (1,071,759 rows):**

| Dataset | Rows | Purpose |
| --- | --- | --- |
| **SmolTalk** | 460K | General chat conversations |
| **MMLU** x3 | 300K | Multiple choice reasoning |
| **SimpleSpelling** | 200K | Spelling tasks |
| **SpellingBee** | 80K | Counting letters |
| **GSM8K** x4 | 32K | Math word problems |
| **Identity** | 1K | Model identity/persona |
| **Custom code+SEC** | **1K** | Our curated code + SEC conversations |

Custom data format (`prepare_sft_data.py`):

```python
# Each line in JSONL:
[{"role":"user","content":"Write a Python function..."},
 {"role":"assistant","content":"def fibonacci(n):..."}]
```

SFT uses loss masking — only trains on **assistant tokens** (mask=1), user/BOS/tool outputs are ignored (mask=0). Chat format uses special tokens: `<|user_start|>`, `<|user_end|>`, `<|assistant_start|>`, `<|assistant_end|>`.

**SFT status: Step 1,591 / ~9,000 (17.7%)**

```
Loss: 1.47 (down from 2.4 → shows model is learning chat format)
Speed: 51,450 tok/s, 1.27s/step
Runtime: 33 min elapsed, ~2.5h remaining for epoch
```

First validation eval at step 500 (not hit yet — eval-every=500). Checkpoints save to `~/.cache/nanochat/chatsft_checkpoints/d12/`.

### What's Left

1. **SFT completion** — full epoch will finish in ~2.5h
2. **Test generation** — run `run_prompts.py --step=<sft_step>` to compare pretrained vs SFT quality
3. **GGUF export** — convert to GGUF for llama.cpp serving

### Scripts in `/mnt/data/zz/`

```
fineweb-code-sec-gpt.sh        # pretraining (50k steps)
prepare_data.sh                # full data pipeline
train_log.sh                   # monitoring utility

fineweb-code-sec-gpt/
  prepare_sft_data.py          # creates 1000 code+SEC chat JSONL
  sft_code_sec.sh              # SFT fine-tuning
  run_prompts.py               # generate samples from any checkpoint
  prompt_*.txt                 # 13 test prompts (code/SEC/general)
  results.txt                  # generation results (pretrained model)
```
