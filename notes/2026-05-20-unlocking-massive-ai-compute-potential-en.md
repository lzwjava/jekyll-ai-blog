---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unlocking Massive AI Compute Potential
translated: false
type: note
---

**Question:** What can you do with MI300X x8 (8x 192GB = 1.5TB VRAM total)? What models can you train/infer? How fast is Whisper transcription? What happens when compute becomes this cheap and abundant?

**Answer:**

This is exactly the right mental model to build. Let me go through it systematically.

---

## MI300X x8 — The Raw Numbers

| Resource | Value |
|---|---|
| GPUs | 8x AMD MI300X |
| VRAM | 8 × 192GB = **1.5TB total** |
| Memory Bandwidth | ~9.6 TB/s aggregate |
| BF16 TFLOPS | ~3,200 TFLOPS aggregate |
| Cost | $15.92/hr (~100 RMB/hr) |

---

## What Models Fit in 1.5TB VRAM?

### Inference (FP16/BF16)

| Model | VRAM Needed | Fits? |
|---|---|---|
| Llama 3 8B | ~16GB | ✅ trivially |
| Llama 3 70B | ~140GB | ✅ single GPU |
| Llama 3 405B | ~810GB | ✅ fits across 5 GPUs |
| DeepSeek V3 (671B) | ~1.3TB | ✅ fits! |
| DeepSeek R1 (671B) | ~1.3TB | ✅ fits! |
| GPT-4 scale (~1.8T est.) | ~3.6TB | ❌ need more |
| Llama 3 405B @ INT4 | ~200GB | ✅ 2 GPUs |

**DeepSeek R1 full precision, fully in VRAM, no offloading** — this is the key unlock. On H100 clusters people shard this across 16+ GPUs. Here it fits with headroom.

### Training

```
Model params (B) × 16 bytes (optimizer states, fp32 copy, gradients)
= rough VRAM for full fine-tune
```

| Model | Full Fine-tune | LoRA |
|---|---|---|
| Llama 3 8B | ~128GB | ~20GB |
| Llama 3 70B | ~1.1TB | ~150GB |
| Llama 3 405B | ~6.5TB | ~900GB |
| GPT-2 (1.5B) | ~24GB | ~5GB |

So with 1.5TB you can **full fine-tune Llama 70B** — no LoRA compromise. That's genuinely rare access.

---

## Whisper Transcription Speed

Whisper large-v3 on a single A100 80GB does ~200x realtime.
MI300X has ~2× the memory bandwidth of A100.

Rough estimate:

- **Whisper large-v3: ~300-400x realtime per GPU**
- With batching across 8 GPUs: **~2000-3000x realtime**

Meaning: **1 hour of audio → transcribed in ~1-2 seconds**

A podcast archive of 10,000 hours → done in ~3-5 hours, cost ~$50.

---

## What Can You Do With 100 RMB/hr?

### In 1 hour ($15.92)

- Fine-tune Llama 8B on your custom dataset (several epochs)
- Run 10,000+ inference calls on 70B model
- Transcribe ~50,000 hours of audio with Whisper
- Train nanoGPT-scale model from scratch, multiple runs
- Run full DeepSeek R1 671B for ~1hr of heavy reasoning tasks

### In 10 hours ($160, ~1000 RMB)

- Full fine-tune Llama 70B on domain data (e.g., financial/legal corpus)
- Train a 1B parameter model from scratch on custom data
- Process an entire company's document archive through an LLM pipeline

### In 100 hours ($1,600)

- Replicate most published LoRA/QLoRA research papers
- Build a production-grade specialized model (medical, legal, code)

---

## The Thought Experiment: Everyone Has 8x MI300X

This is the most interesting question. Let me think through it like Karpathy would.

### Phase 1: Democratized Inference

Right now, GPT-4 quality reasoning is gated behind API costs and rate limits. If everyone has 1.5TB VRAM:

- **Every developer runs frontier models locally**
- No data leaves your machine — privacy-preserving AI by default
- API companies lose moat unless they have better models

### Phase 2: Personalized Model Training

- Your model, trained on **your** data, your writing, your codebase
- Not fine-tuned for 30 min on 4-bit LoRA — **actually trained**, full weights
- Zhiwei's model trained on your 8,000 notes + 400 blog posts = a model that thinks like you

### Phase 3: Abundance Collapses Certain Markets

```
Current bottleneck: compute scarcity → API pricing → gatekeeping

If compute is abundant:
- Translation industry: gone (run NLLB-200 locally, free)
- Basic coding assistants: commoditized
- Voice transcription: free, instant
- Drug discovery: every lab runs protein folding continuously
- Scientific literature: every researcher has a personal RAG over all papers
```

### Phase 4: The Karpathy Vision

When everyone has H200×8 or MI300X×8:

> "The model is not the product. The data and the feedback loop are the product."

The constraint shifts from **compute** to **data quality** and **evaluation**. Whoever has the best:

- Domain-specific data
- RLHF/GRPO feedback pipelines
- Eval harnesses

...wins. Not whoever has the most GPUs.

---

## What Your Experiment Should Actually Test

Since you're getting trial access, here's a concrete plan:

```bash
# 1. Baseline: How fast is ROCm vs CUDA for your workloads?
python -c "import torch; print(torch.version.hip)"  # ROCm version

# 2. Run DeepSeek R1 671B — the thing you literally cannot do locally
pip install vllm
vllm serve deepseek-ai/DeepSeek-R1 --tensor-parallel-size 8

# 3. Benchmark Whisper at scale
pip install faster-whisper
# batch process, measure x-realtime factor

# 4. Try a full fine-tune of Llama 8B — not LoRA, full weights
torchrun --nproc_per_node=8 train.py \
  --model meta-llama/Llama-3-8B \
  --full_finetune True

# 5. Train something from scratch — your GPT-2 workflow but bigger
# On H200 you trained GPT-2 1.5B. Here try 3B-7B range.
```

---

## The Mental Model to Keep

The experiment gives you **intuition that compounds**:

> "I know what 1.5TB VRAM feels like. I know the ceiling. Now I can reason about what's possible at scale without guessing."

This is exactly how Karpathy talks about GPU intuition — you need to have **run the experiment** to have calibrated beliefs. Most people theorize. You'll have data.

The world where everyone has MI300X×8 is maybe 10-15 years away at current cost curves (GPU compute halves in cost roughly every 2-3 years). But the **mental model** — thinking from that future backward — is available to you right now, after this experiment.
