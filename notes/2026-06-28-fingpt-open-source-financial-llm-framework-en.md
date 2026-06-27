---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FinGPT: Open-Source Financial LLM Framework"
translated: false
type: note
---

**Question:** Introduce FinGPT (Yang, Liu, Wang, 2023, arXiv:2306.06031) — the open-source financial LLM framework.

**Answer:**

FinGPT is the open-source counterpunch to BloombergGPT. Where Bloomberg spent ~1.3M GPU-hours and $1M+ training a 50B model from scratch on a proprietary corpus, FinGPT's thesis is the opposite: **don't train from scratch — the financial data shifts too fast, and a strong open base + cheap adapters gets you there for ~$300 per fine-tune.** It's less a single model than a *framework* (data pipeline + LoRA fine-tuning + RL alignment) built on top of open bases like Llama, ChatGLM, Falcon, etc.

**The core argument — why from-scratch is wrong for finance.** Financial markets are non-stationary. News, sentiment drivers, and market regimes change weekly. A model frozen at training time decays fast. BloombergGPT's $1M run is a sunk cost you'd have to repeat to stay current. FinGPT's answer: build a **lightweight data-centric pipeline** that ingests fresh financial text continuously, and use **LoRA** to cheaply re-adapt a frozen open base. The moat moves from "who has the biggest one-time corpus" to "who has the best automated data refresh + adaptation loop."

**The four-layer architecture (the actual paper structure):**

1. **Data source layer** — scrapes news (Reuters, Yahoo, Seeking Alpha), social (Twitter/Reddit), filings, company announcements across markets (US + China). Real-time ingestion is the point.
2. **Data engineering layer** — cleaning, tokenization, alignment. This is where they spend their epistemic energy: financial text is noisy and time-sensitive, so they emphasize cheap, reproducible pipelines over curation perfectionism.
3. **LLM layer** — frozen open base + LoRA adapters. They also explored **RLHF / RL with stock-price feedback (RLSP)** — using market reaction as a reward signal instead of human labels, which is a clever domain-specific substitute for expensive human preference data.
4. **Application layer** — robo-advising, algorithmic trading signals, sentiment analysis, low-code development.

**The LoRA economics — the part worth internalizing.** This is the whole pitch in one number. LoRA freezes the base weights `W ∈ ℝ^{d×k}` and learns a low-rank update:

```
W' = W + ΔW = W + B·A,   where B ∈ ℝ^{d×r}, A ∈ ℝ^{r×k}, r ≪ min(d,k)
```

For a `d=k=4096` layer with `r=8`, you train `2·d·r = 65,536` params instead of `d·k = 16.7M` — a **~256x** reduction per layer. Across the model FinGPT fine-tunes ~roughly millions of params instead of billions. That's why a fine-tune costs **<$300 and runs on a single GPU** vs Bloomberg's $1M+. Concretely, for financial sentiment they took a base model from a weak F1 to competitive-with-BloombergGPT performance for the price of a dinner.

Minimal mental model of what the fine-tune actually does:

```python
# conceptual: FinGPT-style sentiment fine-tune
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")  # frozen
cfg = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj","v_proj"],
                 lora_dropout=0.05, task_type="CAUSAL_LM")
model = get_peft_model(base, cfg)   # only A,B matrices are trainable
# train on instruction pairs: ("headline X about TSLA", "negative")
# adapter is ~tens of MB, swappable, re-trainable weekly as data refreshes
```

The instruction-tuning data is the real product: they frame financial sentiment as instruction pairs (headline → label) rather than raw next-token prediction, which is why a 7B base can match a 50B from-scratch model on the *narrow* task. This is the standard lesson — task-specific instruction tuning on a strong base beats scale-from-scratch on narrow benchmarks.

**Honest limits.** FinGPT "beating" BloombergGPT is benchmark-specific — sentiment classification, FPB, FiQA. It's not a general financial reasoning win; it's "for the tasks people actually deploy, adapters on an open base are 3000x cheaper and good enough." The from-scratch model still had broader latent financial knowledge from its 363B-token FinPile. But for your purposes the verdict is clear: the FinGPT approach (open base + LoRA + fresh-data pipeline) is what actually won the industry, and it's the template you'd use if you built a financial-domain model today given your bank background and GPU access.

**For your trajectory.** This pairs directly with your nanoGPT/LoRA work. The reproducible exercise: take Qwen or Llama-3-8B, build a small instruction set from financial headlines, LoRA-tune on your RTX 4070 (7B in 4-bit fits in 12GB with QLoRA), and you've replicated the core FinGPT result on your own hardware for ~free. That's a concrete portfolio piece that maps your banking domain knowledge onto your AI-engineering transition — exactly the kind of project that compounds.

**References:**

- [FinGPT: Open-Source Financial Large Language Models (arXiv:2306.06031)](https://arxiv.org/abs/2306.06031)
- [FinGPT GitHub (AI4Finance-Foundation)](https://github.com/AI4Finance-Foundation/FinGPT)
- [LoRA: Low-Rank Adaptation of Large Language Models (arXiv:2106.09685)](https://arxiv.org/abs/2106.09685)
- [QLoRA: Efficient Finetuning of Quantized LLMs (arXiv:2305.14314)](https://arxiv.org/abs/2305.14314)
