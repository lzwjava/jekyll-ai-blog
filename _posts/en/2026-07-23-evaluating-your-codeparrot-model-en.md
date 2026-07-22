---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evaluating Your Codeparrot Model
translated: false
type: note
---

Apologies for the mixed language earlier. Here's the full picture in English.

---

## Project Overview

You're training a **nanochat-based GPT model** (286M params, depth=12) on the `codeparrot-clean` dataset (Python code). Checkpoints are stored via MLflow in `~/.cache/nanochat/base_checkpoints/d12/`.

---

## Recent Eval-Related Commits

| Commit | Description |
| -------- | ------------- |
| `9538f8b` | `eval_long`: Markdown output with syntax-highlighted code blocks |
| `1df37d3` | `eval_long`: add PROMPT/OUTPUT separator in log output |
| `efa3c1f` | add eval and eval_long: codeparrot-d12 evaluation scripts and results |

These are all in `zz/codeparrot/eval/` and `zz/codeparrot/eval_long/`.

---

## How to Evaluate Your Trained Model

### 1️⃣ BPB + Sampling + Python Code Gen (Quantitative)

**Script**: `zz/codeparrot/eval/run_eval.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate

python -m scripts.base_eval \
    --model-tag d12 \
    --eval bpb,sample \
    --device-batch-size=8 \
    --split-tokens=1048576
```

This runs:

- **bpb** – Bits-per-byte on train/val splits (measures loss)
- **sample** – Generates text from built-in prompts to qualitatively check output

The script also has an inline Python section that tests 8 Python code prompts (fibonacci, reverse linked list, etc.) using the nanochat Engine directly.

### 2️⃣ Long-Prompt Evaluation (Code Generation)

**Script**: `zz/codeparrot/eval_long/run_eval_long.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate
bash zz/codeparrot/eval_long/run_eval_long.sh
```

This runs `eval_long.py` which tests 8 complex Python prompts (BST, LCS, decorators, file I/O, etc.) and writes a nicely formatted Markdown file with syntax-highlighted code blocks to `zz/codeparrot/eval_long/results/long_prompt_results.md`.

### 3️⃣ Quick Interactive Chat / Single Prompt

**Scripts**: `zz/eval_sft.sh` and `zz/eval_sft_extra.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate

# Test base model with a single prompt
python -m scripts.chat_cli \
    --source=base \
    --model-tag=d12 \
    --temperature=0.3 \
    --top-k=50 \
    --prompt="Write a Python function to check if a string is a palindrome"
```

Or for interactive mode:

```bash
python -m scripts.chat_cli --source=base --model-tag=d12
```

### 4️⃣ Full CORE Benchmark (ICL Accuracy)

If you want to evaluate on few-shot NLP tasks:

```bash
python -m scripts.base_eval \
    --model-tag d12 \
    --eval core \
    --max-per-task=100
```

This downloads an eval bundle (~1GB) and runs accuracy on multiple-choice / completion tasks, scoring a "CORE metric" (centered accuracy).

---

## Key Files Summary

| File | What it does |
| ------ | ------------- |
| `zz/codeparrot/eval/run_eval.sh` | Full eval: BPB + samples + Python code gen |
| `zz/codeparrot/eval_long/run_eval_long.sh` | Long-context code generation eval |
| `zz/codeparrot/eval_long/eval_long.py` | Python logic for long-prompt eval |
| `zz/eval_sft.sh` | SFT checkpoint eval (5 general prompts) |
| `zz/eval_sft_extra.sh` | More SFT prompts (math, reasoning, SQL) |
| `zz/finetune/eval.py` | vLLM/transformers eval for fine-tuned LoRA checkpoints |
| `/mnt/data/nanochat/scripts/base_eval.py` | Main eval CLI: `core`, `bpb`, `sample` |
| `/mnt/data/nanochat/scripts/chat_cli.py` | Interactive chat or single-prompt inference |

---

## Quick Start to Eval Your Latest Checkpoint

**For BPB + sampling:**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
NANOCHAT_DATA_DIR="/mnt/data/zz/datasets/codeparrot-clean-nanochat" \
python -m scripts.base_eval --model-tag d12 --eval bpb,sample --device-batch-size=8
```

**For long-prompt code eval:**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
bash /mnt/data/zz/codeparrot/eval_long/run_eval_long.sh
```

Results go to `~/.cache/nanochat/base_eval/` (for `base_eval.py`) and `zz/codeparrot/eval_long/results/long_prompt_results.md` (for long-prompt).
