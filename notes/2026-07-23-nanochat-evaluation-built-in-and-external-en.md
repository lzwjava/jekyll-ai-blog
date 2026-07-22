---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Nanochat Evaluation: Built-in and External"
translated: false
type: note
---

Great news — nanochat already has **built-in task evaluation**! But there are also great external libraries. Here's the full picture.

---

## ✅ What You Already Have (Built-in)

**Script**: `python -m scripts.chat_eval`

| Task | Type | What it measures |
| ------ | ------ | ----------------- |
| **HumanEval** | Generative | Python function completion → run unit tests → pass@k |
| **MMLU** | Categorical | 57 subjects, multiple-choice knowledge |
| **ARC-Easy / ARC-Challenge** | Categorical | Grade-school science reasoning |
| **GSM8K** | Generative | Grade-school math word problems |
| **SpellingBee** | Generative | Letter counting & spelling |
| **SmolTalk** | (in chat_sft.py) | Conversational quality |
| **CustomJSON** | (in chat_sft.py) | Load your own JSONL eval |

**Usage** (for your SFT or base model):

```bash
cd /mnt/data/nanochat && source .venv/bin/activate

# Run HumanEval (code generation, runs unit tests)
python -m scripts.chat_eval --source=sft --model-tag=d12 --task-name=HumanEval

# Run all tasks
python -m scripts.chat_eval --source=sft --model-tag=d12

# Run specific tasks
python -m scripts.chat_eval --source=base --model-tag=d12 --task-name="ARC-Easy|GSM8K"
```

---

## 📦 External Eval Libraries to Add

Since your model is a **code model** (trained on Python), here are the most relevant ones:

### 1️⃣ [LM Eval Harness](https://github.com/EleutherAI/lm-evaluation-harness) (EleutherAI)

The industry standard. 100+ benchmarks out of the box.

```bash
pip install lm-eval
```

**Supports:** MMLU, HellaSwag, ARC, GSM8K, HumanEval, MATH, BigBench, etc.

**Usage with your model** — you'd need to either:

- Export your nanochat model to HuggingFace format (add a conversion script), or
- Use the `--model local-completion` interface to pipe prompts through your nanochat Engine

```bash
# If converted to HF format:
lm_eval --model hf --model_args pretrained=./my-model \
  --tasks mmlu,hellaswag,arc_challenge --device cuda:0
```

### 2️⃣ [HumanEval + MBPP](https://github.com/openai/human-eval) (direct)

You already have HumanEval integrated (nanochat/tasks/humaneval.py), but you could also run it standalone for more detailed reporting:

```bash
pip install human-eval
```

### 3️⃣ [BigCode Eval Harness](https://github.com/bigcode-project/bigcode-evaluation-harness)

Purpose-built for **code models**. Supports:

| Benchmark | Description |
| ----------- | ------------- |
| **HumanEval** | Python function completion |
| **MBPP** | ~1000 Python programming tasks |
| **HumanEval-X** | Multi-language (C++, Java, JS, Go, etc.) |
| **DS-1000** | Data science / numpy / pandas tasks |
| **APPS** | Competitive programming |
| **CodeContests** | Codeforces-level problems |

```bash
pip install bigcode-evaluation-harness
```

```bash
# Evaluate your converted model on code tasks
bigcode-eval-harness \
  --model hf \
  --model_args pretrained=./my-model \
  --tasks humaneval,mbpp --batch_size 8
```

### 4️⃣ [DeepEval](https://github.com/confident-ai/deep-eval)

Modern framework with LLM-as-judge evaluation. Good for conversational quality.

```bash
pip install deepeval
```

### 5️⃣ [HuggingFace `evaluate`](https://github.com/huggingface/evaluate)

Lightweight metrics — BLEU, ROUGE, perplexity, accuracy, F1. Good for quick stats.

```bash
pip install evaluate
```

```python
from evaluate import load
perplexity = load("perplexity", module_type="metric")
results = perplexity.compute(predictions=[...], model_id="...")
```

---

## 🧱 The Catch — Your Custom Tokenizer

Your nanochat model uses a **custom BPE tokenizer** (vocab_size=32768, trained on codeparrot code). External eval libraries expect **HuggingFace `transformers` models** with a `AutoTokenizer` / `AutoModelForCausalLM` interface.

**To use external libs, you'll need to add a HuggingFace export step.** A minimal exporter would:

1. Load your model via `checkpoint_manager.load_model()`
2. Convert the weights into `transformers` state dict
3. Save with `model.save_pretrained()` + tokenizer config

That's the one missing piece to unlock all external eval tools.

---

## TL;DR Recommendations

| What to Use | Why |
| ------------- | ----- |
| **Built-in `chat_eval.py`** | Already works, no setup needed |
| **Built-in `base_eval.py`** | BPB + CORE benchmark for base model |
| **Add BigCode Eval Harness** | Best for code-specific benchmarks (HumanEval, MBPP) |
| **Add LM Eval Harness** | Best for general LLM benchmarks (MMLU, ARC, GSM8K) |
| **Add a HF export script** | Required to use either of the above |

Want me to write a **HuggingFace export script** for your nanochat model so you can use all these external eval libraries?
