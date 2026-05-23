---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximizing AMD MI300X Developer Access
translated: false
type: note
---

Nice, congrats on joining the AMD AI Developer Program! That MI300X access is genuinely valuable — 192GB HBM3 is enough to run 70B models in full precision or do serious fine-tuning runs.

Here's how to make the most of it given your trajectory:

**Immediate priorities:**

1. **Claim your credits fast** — AMD Developer Cloud credits often have expiration windows. Log in to the member site now and screenshot/save everything.

2. **Check the DeepLearning.AI promo** — could be free access to courses like the new LLM fine-tuning or RL from Human Feedback courses. Worth grabbing even if you don't use them immediately.

**What to actually run on MI300X given your goals:**

```bash
# MI300X is ROCm-based, not CUDA — key difference
# Most PyTorch code works with minor changes:
pip install torch --index-url https://download.pytorch.org/whl/rocm6.0

# Check GPU visibility
rocm-smi
# vs nvidia-smi on your 4070

# HIP (AMD's CUDA equivalent)
hipcc --version
```

**High-value experiments for your AI engineering trajectory:**

```python
# 1. Full-precision 70B inference — impossible on your 4070 (12GB)
#    MI300X's 192GB HBM3 handles it natively
#    llama.cpp or vllm with ROCm backend

# 2. Full fine-tune (not LoRA) on mid-size models
#    GPT-2 XL, Mistral 7B — no quantization needed

# 3. Flash Attention on ROCm — compare perf vs CUDA
#    Good blog post material for lzwjava.github.io

# 4. Multi-GPU tensor parallelism experiments
#    MI300X often comes in multi-card configs on AMD cloud
```

**ROCm vs CUDA gotchas to know upfront:**

- `torch.cuda.*` still works — ROCm maps it transparently
- Custom CUDA kernels need HIP porting (`hipify-perl`)
- Some libraries lag (e.g., bitsandbytes ROCm support has historically been spotty)
- `PYTORCH_HIP_ALLOC_CONF` instead of `PYTORCH_CUDA_ALLOC_CONF`

**What I'd do first session:**

```bash
# Benchmark baseline — always know your hardware
git clone https://github.com/EleutherAI/lm-evaluation-harness
# Run a model, measure tokens/sec, compare to your 4070 numbers
# That delta = the story of HBM3 vs GDDR6X bandwidth
```

The MI300X is legitimately frontier hardware for an individual developer. Most people just run inference demos — you should be doing training runs and publishing the perf numbers on your blog. That's the kind of content that gets noticed in the AI engineering space.