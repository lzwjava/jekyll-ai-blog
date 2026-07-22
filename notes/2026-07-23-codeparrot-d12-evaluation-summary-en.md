---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codeparrot-d12 Evaluation Summary
translated: false
type: note
---

Here's the full evaluation report for your **codeparrot-d12 model**:

---

## 📊 Model Evaluation Results

### Model Info

| Property | Value |
|----------|-------|
| Architecture | GPT (286M params, depth=12, dim=768, heads=6) |
| Training Data | codeparrot-clean (Python code, 24.7B tokens) |
| Base Model Step | **87,000** (final) |
| SFT Model Step | **8,985** |
| val_bpb | **0.3723** |
| Tokenizer | Custom BPE (vocab_size=32,768, trained on Python code) |

---

### Base Model — Code Generation

**✅ Good**: Generates syntactically valid Python — license headers, imports, function definitions, class structures all look realistic.

**❌ Not so good**: Logic is often wrong. The model knows *shapes* of code but not *semantics*:

| Prompt | Output Quality |
|--------|---------------|
| `def is_palindrome(s):` | ✅ Gets `s[::-1]` right, but repeats with is_palindrome2, is_palindrome3... |
| `class BinarySearchTree: insert(self, val):` | ❌ Inserts to both left AND right |
| `async def fetch_url(...)` | ✅ Async/await syntax correct, but loops infinitely with `fetch_json_async_async_async...` |
| Unconditioned generation | ✅ Generates full Python files (SickRage, pvlib, PyQt4, etc.) |

**Bottom line**: It learned Python syntax well but not algorithmic correctness.

---

### SFT Model — Chat Evaluation

| Task | Accuracy | Random Baseline | Verdict |
|------|----------|-----------------|---------|
| **ARC-Easy** (200 probs) | **25.50%** | 25.00% | 🟡 At chance |
| **ARC-Challenge** (100 probs) | **28.00%** | 25.00% | 🟡 Slightly above chance |
| **MMLU** (20 probs) | **15.00%** | 25.00% | 🔴 Below random |
| **GSM8K** (20 probs) | **0.00%** | 0.00% | 🔴 Can't do math |
| **HumanEval** (5 probs) | **0.00%** | 0.00% | 🔴 No correct Python function |
| **SpellingBee** (10 probs) | **0.00%** | 0.00% | 🔴 Can't count letters |

**All results logged via nanochat's report system.**

---

### Key Takeaways

1. **The base model** is a decent **Python code language model** — it generates syntactically correct Python with appropriate imports, docstrings, and structure. It just doesn't *understand* logic well (it's only 286M params, trained on raw code without instruction tuning).

2. **The SFT model** barely improves over random — likely because **8,985 steps is too few** for SFT. It was probably still in early training (learning the chat format tokens like `<|user_start|>`, `<|assistant_start|>`).

3. **Built-in eval works great.** You can run all tasks with:
   ```bash
   cd /mnt/data/nanochat && source .venv/bin/activate
   PYTORCH_ALLOC_CONF=expandable_segments:True \
     python -m scripts.chat_eval --source=sft --model-tag=d12 --step=8985
   ```

Want me to:
- **Train the SFT model longer** and re-evaluate?
- **Write a script** that evaluates all checkpoints (5k, 10k, 15k, ... 87k) to see the learning curve?
- **Export to HuggingFace format** so you can use LM Eval Harness / BigCode Eval?