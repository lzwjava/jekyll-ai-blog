---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FinGPT on RTX 4070: Issues & Fixes"
translated: false
type: note
---

Here's the full picture:

---

## GPU Status

```
RTX 4070  |  12GB VRAM (12,282 MiB)  |  230MiB used  |  CUDA 13.0
```

Plenty of headroom, only Xorg using it.

---

## The Code — What It Does

FinGPT is a **LoRA fine-tuning framework** for financial LLMs. It wraps HuggingFace `Trainer` + PEFT + DeepSpeed. Key sub-projects:

| Sub-project | What it does |
|---|---|
| **FinGPT_Benchmark** | Multi-task training (sentiment, NER, headline IE, relation extraction, ConvFinQA) on 7B models |
| **FinGPT_Forecaster** | Stock movement prediction from news — Llama-2-7B, max_length 4096 |
| **FinGPT_Sentiment_Analysis** | Financial sentiment classifier |
| **FinGPT_RAG / MultiAgentsRAG** | RAG pipelines for financial QA |
| **FinGPT_FinancialReportAnalysis** | PDF report analysis |

Model sizes supported:

| Model | Size (fp16) | 8-bit | 4-bit |
|---|---|---|---|
| ChatGLM2-6B / Falcon-7B / Qwen-7B / Llama-2-7B | ~13-14 GB | ~6.5 GB | ~3.5 GB |
| Llama-2-13B | ~26 GB | ~13 GB | ~7 GB |

Training uses **LoRA** (not full fine-tune) — adapter weights are tiny (~few MB).

---

## Issues I See

**1. `load_in_8bit=True` is commented out** (line 50 in both `train_lora.py` files)

```python
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # load_in_8bit=True,       <-- commented out
    # device_map="auto",
    trust_remote_code=True
)
```

This means the model loads in full fp16 — **13GB for a 7B model won't fit in 12GB VRAM**. You WILL get CUDA OOM unless you uncomment this or use 4-bit.

**2. Designed for 4 GPUs, not 1**

- Forecaster `train.sh` does `--include localhost:2,3` — hardcoded for GPUs 2-3 on a multi-GPU box
- DeepSpeed config uses **ZeRO stage 0** (no sharding) — it helps with optimizer memory but doesn't split the model
- Original paper says training costs <$300 per run, but they assume 4× A100 or similar

**3. Needs model files locally**

- `from_remote=False` by default → looks for models at local `base_models/Llama-2-7b-hf` etc.
- Would need to either download models first or set `--from_remote` (and have HF token for gated models like Llama-2)

**4. Dated dependencies**

- Uses `prepare_model_for_int8_training` from PEFT — deprecated in newer versions, replaced by `prepare_model_for_kbit_training`
- No flash attention, no gradient checkpointing, no QLoRA (4-bit NF4)

---

## What You Can Actually Do on RTX 4070 12GB

### ✅ EASILY fits — comfortable

| Task | Setup |
|---|---|
| **Sentiment / NER / Headline** fine-tune on **7B** | 4-bit QLoRA, batch_size 4, max_length 512 → ~5-6 GB |
| **Forecaster** on **7B** | 4-bit, batch_size 1, max_length 4096 → ~6-7 GB |
| **Inference** on any **7B** model | fp16 or 8-bit, fits easily |
| **Inference** on **13B** | 4-bit quantization → ~7-8 GB |

### ⚠️ Fits with work — needs tuning

| Task | Setup |
|---|---|
| **Forecaster** on **7B** with 8-bit | Batch_size 1, grad_accum 16 (like the original), max_length 2048 |
| **13B** fine-tune with LoRA | 4-bit QLoRA only, tiny batch_size 1, max_length 512 |

### ❌ Won't work

| Task | Why |
|---|---|
| Full fp16 fine-tune of any 7B+ model | 13GB > 12GB |
| 13B model in 8-bit | ~13GB barely over 12GB, no headroom for activations |
| Anything requiring fp32 (without mixed precision) | 26GB+ per 7B model |

---

## Quick Fix to Get Running

Uncomment `load_in_8bit=True` and add `device_map="auto"` in `train_lora.py`. Or better, upgrade to 4-bit QLoRA:

```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
```

Then drop DeepSpeed (overkill for 1 GPU) and use HuggingFace Trainer directly. For the Forecaster, also enable gradient checkpointing and set `batch_size=1`, `gradient_accumulation_steps=16`.

Want me to make these changes and set up a test run?
