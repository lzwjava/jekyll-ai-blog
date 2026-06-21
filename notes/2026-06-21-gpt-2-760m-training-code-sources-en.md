---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 760M Training Code Sources
translated: false
type: note
---

**Question:** Where to get the training code to train a GPT-2 760M scale model (like what I did on AMD MI300X)?

**Answer:**

BigCode is about code LLMs (StarCoder family), not GPT-2 pretraining. For GPT-2 760M scale training, here are the canonical codebases ranked by relevance to your setup:

---

## 1. nanoGPT — Karpathy's reference implementation (start here)

```bash
git clone https://github.com/karpathy/nanoGPT
```

This is the gold standard for GPT-2 scale pretraining from scratch. You've already used it on MI300X. Key files:

- `model.py` — GPT-2 architecture (CausalSelfAttention, MLP, Block, GPT)
- `train.py` — full DDP training loop with gradient accumulation, cosine LR, eval
- `config/train_gpt2.py` — configs for 124M, 355M, 774M, 1558M

For 760M specifically, `train_gpt2_medium.py` or just set:
```python
n_layer = 36
n_head = 20
n_embd = 1280
```
That's GPT-2 XL territory (~760M params).

---

## 2. Megatron-LM — production-grade, multi-GPU/multi-node

```bash
git clone https://github.com/NVIDIA/Megatron-LM
```

For MI300X you'd use the ROCm fork or AMD's own:
```bash
git clone https://github.com/ROCm/Megatron-LM
```

Supports tensor parallelism + pipeline parallelism. More complex but scales to 100B+. Overkill for 760M but worth knowing.

---

## 3. LitGPT — Lightning AI's clean multi-model trainer

```bash
git clone https://github.com/Lightning-AI/litgpt
```

Covers GPT-2, Llama, Mistral, Phi with a unified training interface. Cleaner than nanoGPT for production use, has LoRA/QLoRA built in.

---

## 4. BigCode's training repo — if you want code-specific pretraining

```bash
git clone https://github.com/bigcode-project/bigcode-dataset  # data pipeline
git clone https://github.com/bigcode-project/starcoder        # training scripts
```

StarCoder uses Megatron under the hood with FIM (Fill-in-Middle) objective. The Stack v2 is your data source.

---

## Quickstart for 760M on MI300X (nanoGPT path)

```bash
git clone https://github.com/karpathy/nanoGPT && cd nanoGPT

# Prepare FineWeb or OpenWebText
python data/openwebtext/prepare.py

# config/train_gpt2_760m.py
cat > config/train_gpt2_760m.py << 'EOF'
wandb_log = True
wandb_project = 'gpt2-760m'
dataset = 'openwebtext'

# 760M params
n_layer = 36
n_head = 20
n_embd = 1280
block_size = 1024
dropout = 0.0

# training
batch_size = 12
gradient_accumulation_steps = 40  # effective batch = 480 * 1024 tokens
max_iters = 600000
lr_decay_iters = 600000
learning_rate = 1e-4
min_lr = 1e-5
warmup_iters = 2000
EOF

# Launch with ROCm/HIP on MI300X
torchrun --nproc_per_node=1 train.py config/train_gpt2_760m.py
```

For multi-GPU on MI300X (it has 192GB HBM3 so you can fit this easily on 1 GPU):
```bash
# Single GPU, 760M fits in ~6GB weights + optimizer states ~24GB total
# MI300X has 192GB so you have massive headroom for bigger batch sizes
```

---

## Data options (better than OpenWebText)

| Dataset | Size | HF path |
|---------|------|---------|
| FineWeb | 15T tokens | `HuggingFaceFW/fineweb` |
| FineWeb-Edu | 1.3T edu tokens | `HuggingFaceFW/fineweb-edu` |
| OpenWebText | ~9B tokens | local via nanoGPT prepare script |
| The Stack v2 | 67.5TB code | `bigcode/the-stack-v2-dedup` |

FineWeb-Edu is the current best for a GPT-2 style language model if you want strong benchmarks.

---

## Summary

| Repo | Best for |
|------|---------|
| `karpathy/nanoGPT` | Learning, clean 760M training, single node |
| `ROCm/Megatron-LM` | Production, multi-node, tensor parallelism on MI300X |
| `Lightning-AI/litgpt` | Clean multi-model, LoRA, less boilerplate |
| `bigcode/starcoder` | Code-specific pretraining with FIM objective |

Since you're already familiar with nanoGPT from your MI300X run — the natural next step is either scaling data (FineWeb instead of OpenWebText) or switching to Megatron for tensor parallelism experiments.

**References:**

- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [ROCm/Megatron-LM](https://github.com/ROCm/Megatron-LM)
- [Lightning-AI/litgpt](https://github.com/Lightning-AI/litgpt)
- [FineWeb dataset](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [bigcode/starcoder training](https://github.com/bigcode-project/starcoder)
