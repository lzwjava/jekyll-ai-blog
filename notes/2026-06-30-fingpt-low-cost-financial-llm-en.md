---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FinGPT: Low-Cost Financial LLM"
translated: false
type: note
---

Question: Explain what FinGPT (AI4Finance-Foundation/FinGPT) is.

Answer:

Let me fetch the actual repo state rather than answer from memory.Question: What is FinGPT (AI4Finance-Foundation/FinGPT) and how does it work?

Answer:

FinGPT is an open-source financial LLM project from the AI4Finance Foundation. The core thesis is a deliberate bet against the BloombergGPT approach: don't pretrain a finance LLM from scratch — instead, take strong open base models and cheaply adapt them with LoRA on financial instruction data. BloombergGPT cost ~$3M and ~53 days to train; FinGPT claims a fine-tune for under $300. The reasoning you'll appreciate: finance data is highly non-stationary, so the economically rational move is cheap, frequent re-adaptation rather than expensive full retraining.

## The actual mechanism

It's parameter-efficient fine-tuning, nothing exotic. Freeze the base model, inject low-rank adapters into the attention projections, train only those on financial instruction datasets. The math is the standard LoRA decomposition:

```
W' = W₀ + ΔW = W₀ + BA
```

where `W₀ ∈ ℝ^(d×k)` is frozen, `B ∈ ℝ^(d×r)`, `A ∈ ℝ^(r×k)`, and `r ≪ min(d,k)`. You train ~0.1% of parameters, which is why FinGPT v3.3 fine-tunes llama2-13b in 17.25 hours on a single RTX 3090 for ~$17. Minimal repro of what they're doing:

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-hf", load_in_8bit=True)
cfg = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj","v_proj"],
                 lora_dropout=0.05, task_type="CAUSAL_LM")
model = get_peft_model(base, cfg)
# train on instruction-formatted financial data, e.g. fingpt-sentiment-train (76.8K rows)
```

## What's in the repo

The project is structured as a five-layer "FinLLM stack": data source → data engineering → LLM (fine-tuning) → task → application. It releases multi-task LoRA adapters over many base models — Llama2-7b, falcon-7b, bloom-7b1, mpt-7b, chatglm2-6b, qwen-7b — plus single-task ones. The instruction datasets cover sentiment, financial relation extraction, headline classification, NER, and FiQA Q&A.

The headline claim worth scrutinizing: FinGPT v3.3 reports weighted-F1 of 0.882 on FPB and 0.903 on TFNS, beating GPT-4 (0.833 / 0.808) on those sentiment benchmarks. That's plausible — task-specific SFT on in-domain labels routinely beats a general zero-shot model on narrow classification. Don't read it as "FinGPT > GPT-4" broadly; it's a sentiment-classification result, not general reasoning.

## Notable products

- **FinGPT-Forecaster**: a robo-advisor demo — feed it a ticker, a date, and a lookback window of news, and it produces a company analysis plus a next-week price-movement prediction. Built as a LoRA on llama2-7b over Dow-30 news.
- **FinGPT-RAG**: retrieval-augmented framework for sentiment, pulling external context before predicting.
- **FinGPT-Benchmark**: their instruction-tuning evaluation harness (task-specific / multi-task / zero-shot).

## Honest assessment for your trajectory

The architecture is conservative — it predates the current MoE/RL-heavy frontier you're tracking (DeepSeek v4, GRPO). The repo is 83% Jupyter notebooks, which tells you it's research-demo-grade, not production infra. The value for you isn't the models — those base models (Llama2, falcon) are now dated — it's the **dataset engineering and instruction-formatting patterns** for financial NLP, which map directly to your banking domain. If you wanted to do something genuinely current, the move would be: take their instruction datasets, swap the base model for a 2025-era open model, and apply GRPO/DPO instead of plain SFT. Note there's a v1.0.0 "Open-Source Financial AI Platform" release dated April 2026, so the project has been refactored beyond the notebook-era code described in most of the README.

References:

- [FinGPT GitHub repo](https://github.com/AI4Finance-Foundation/FinGPT)
- [FinGPT: Open-Source Financial Large Language Models (arXiv 2306.06031)](https://arxiv.org/abs/2306.06031)
- [BloombergGPT (arXiv 2303.17564)](https://arxiv.org/abs/2303.17564)
