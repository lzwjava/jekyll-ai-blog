---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Evaluation Benchmark Guide
translated: false
type: note
---

Here's a comprehensive guide on evaluating LLMs with standard benchmarks, tailored to your project's setup:

---

## Popular Benchmarks for LLM Evaluation

### 1. **LM Evaluation Harness** (the standard tool)

Used by nearly every open LLM release (Llama, Qwen, Mistral, etc.). Supports 60+ benchmarks.

```bash
# Install
pip install lm-eval

# Run basic benchmarks on your fine-tuned model
lm_eval --model hf \
  --model_args pretrained=./finetune/lzw-notes-merged \
  --tasks mmlu,gsm8k,hellaswag,arc_easy,truthfulqa \
  --batch_size auto \
  --output_path ./eval_results
```

**Key tasks:**

| Benchmark | What it measures | Why it matters |
| ----------- | ----------------- | ---------------- |
| **MMLU** (57 subjects) | World knowledge, multi-task accuracy | Most cited LLM benchmark |
| **GSM8K** | Grade-school math reasoning | Tests chain-of-thought |
| **HumanEval** | Code generation (pass@1) | For code models |
| **HellaSwag** | Commonsense reasoning | Detects "stochastic parrot" |
| **ARC (Easy/Challenge)** | Science Q&A | Factual knowledge |
| **TruthfulQA** | Truthfulness | Adversarial for hallucinations |

### 2. **OpenCompass** (better for Chinese + English)

Since your dataset has both EN and ZH notes:

```bash
pip install opencompass
python run.py --models hf_lzw-notes-merged --datasets mmlu ceval cmmlu
```

- **C-Eval** / **CMMLU**: Chinese knowledge benchmarks
- **MMLU**: English multi-task

### 3. **For Code Models** (your codeparrot pipeline)

```bash
# BigCode Evaluation Harness (specifically for code)
pip install bigcode-evaluation-harness

# HumanEval + MBPP
accelerate launch main.py \
  --model codeparrot \
  --tasks humaneval \
  --n_samples 50 \
  --temperature 0.2 \
  --allow_code_execution
```

### 4. **Custom Eval → Benchmark Gap**

Your current `eval_sft.sh` and `finetune/eval.py` are **qualitative/manual** — good for sanity checks. To get numbers people trust, wrap them in **lm-eval** like this:

```python
# quick_bench.py — Stand on the shoulders of giants
import lm_eval
from lm_eval.models.huggingface import HFLM

model = HFLM(pretrained="./finetune/lzw-notes-merged")
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mmlu", "gsm8k", "hellaswag"],
    num_fewshot=5,
    batch_size="auto",
)
print(results["results"])
```

### 5. **Your Specific Models — Recommended Eval Plan**

| Model | Best Benchmarks | Setup |
| ------- | ---------------- | ------- |
| **lzw-notes-merged** (Qwen3-8B SFT) | MMLU, GSM8K, C-Eval | `lm_eval --model hf` |
| **CodeParrot** | HumanEval, MBPP | `bigcode-eval-harness` |
| **GPT-2 760M** (your pretrained) | HellaSwag, ARC-Easy, LAMBADA | `lm_eval` — models <1B aren't good at MMLU |

### 6. **VLLM Integration (fastest)**

Your `finetune/eval.py` already uses vLLM. Plugin lm-eval with vLLM backend:

```bash
lm_eval --model vllm \
  --model_args pretrained=./finetune/lzw-notes-merged,tensor_parallel_size=1 \
  --tasks mmlu,gsm8k \
  --batch_size auto
```

### 7. **Leaderboard Comparison**

Report results in a standard format so you can compare:

```json
{
  "model": "lzw-notes-merged",
  "base": "Qwen3-8B",
  "mmlu": 0.682,
  "gsm8k": 0.754,
  "hellaswag": 0.811,
  "ceval": 0.703
}
```

This is what people expect to see when you say "I fine-tuned a model."

---

**Quick start for your project:** Install `lm-eval` and run it on your merged model — you'll get MMLU/GSM8K/HellaSwag numbers in 10 minutes, which is what the community actually looks at.
