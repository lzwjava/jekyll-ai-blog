---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run DeepSeek-V3 on H200 or MI300X
translated: false
type: note
---

**Question:** What if we have H200 or AMD MI300X — can we run the full DeepSeek-V3/V4 (671B) model on those?

**Answer:**

## Running DeepSeek-V3/V4 on H200 or AMD MI300X

Let's do the math properly first, then the setup.

---

## Memory Math

### DeepSeek-V3 (671B parameters, the latest open-weights model)

| Precision | VRAM needed | Notes |
| ----------- | ------------ | ------- |
| FP8 | ~380 GB | Recommended for inference |
| BF16 | ~1.34 TB | Way too much for single node |
| INT4 (GPTQ/AWQ) | ~190 GB | Lossy but viable |

### Your hardware

| GPU | VRAM | Notes |
| ----- | ------ | ------- |
| H200 SXM (single) | 141 GB HBM3e | Not enough solo |
| H200 SXM (2x) | 282 GB | Tight for FP8, doable with offload |
| **AMD MI300X (single)** | **192 GB HBM3** | **Best single-GPU option — barely fits FP8** |
| MI300X (2x) | 384 GB | Comfortable for FP8, possible BF16 |

**The MI300X 192GB is actually the sweet spot for running DeepSeek-V3 solo in FP8.**

---

## Option 1: AMD MI300X — DeepSeek-V3 Full Model (FP8)

DeepSeek officially supports this. Their repo targets exactly this config.

### Setup (ROCm path)

```bash
# On your AMD Dev Cloud instance ($2/hr — ~$3-4/hr for MI300X nodes)
# Check what you have
rocm-smi
rocminfo | grep "gfx"  # Should be gfx942 for MI300X

# Clone DeepSeek-V3 inference repo
git clone https://github.com/deepseek-ai/DeepSeek-V3.git
cd DeepSeek-V3/inference

# Install deps (ROCm-compatible)
pip install torch --index-url https://download.pytorch.org/whl/rocm6.1
pip install transformers accelerate safetensors
pip install flashinfer  # may need ROCm build

# Download model (FP8 checkpoint ~380GB)
# From HuggingFace — needs HF_TOKEN
pip install huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='deepseek-ai/DeepSeek-V3',
    local_dir='/mnt/data/deepseek-v3',
    ignore_patterns=['*.pt'],  # prefer safetensors
)
"
```

### Run inference (single MI300X, FP8)

```bash
# Using their official inference script
cd DeepSeek-V3/inference

python generate.py \
    --ckpt-path /mnt/data/deepseek-v3 \
    --config configs/config_671B.json \
    --interactive \
    --max-new-tokens 512 \
    --temperature 0.7
```

### vLLM path (recommended for serving)

```bash
# vLLM has first-class MI300X support as of v0.4+
pip install vllm

vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype fp8 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.92 \
    --tensor-parallel-size 1  # single MI300X
```

---

## Option 2: H200 — Multi-GPU Setup

Single H200 (141GB) can't fit V3 in FP8 (needs ~380GB). You need tensor parallelism.

### 2x H200 = 282GB — tight but works

```bash
# Using vLLM with tensor parallelism
vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype fp8 \
    --tensor-parallel-size 2 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.90

# Or with their native inference (fp8, tp=2)
python generate.py \
    --ckpt-path /mnt/data/deepseek-v3 \
    --tp 2 \
    --dtype fp8 \
    --interactive
```

### 4x H200 = 564GB — comfortable, can do BF16 MoE layers

```bash
vllm serve deepseek-ai/DeepSeek-V3 \
    --dtype bfloat16 \
    --tensor-parallel-size 4 \
    --max-model-len 32768  # full context now viable
```

---

## Option 3: SGLang (Best for DeepSeek MLA Architecture)

SGLang has specific optimizations for DeepSeek's **MLA (Multi-head Latent Attention)** — the KV cache compression trick that makes V3/V4 memory-efficient. Better than vLLM for this arch.

```bash
pip install sglang[all]

# Single MI300X
python -m sglang.launch_server \
    --model-path deepseek-ai/DeepSeek-V3 \
    --tp 1 \
    --dtype fp8 \
    --port 30000 \
    --mem-fraction-static 0.88 \
    --enable-mla  # MLA-specific KV cache optimization

# Client
python -c "
import sglang as sgl

@sgl.function
def pipeline(s, prompt):
    s += sgl.user(prompt)
    s += sgl.assistant(sgl.gen('response', max_new_tokens=512))

sgl.set_default_backend(sgl.RuntimeEndpoint('http://localhost:30000'))
state = pipeline.run(prompt='Explain transformer attention from scratch')
print(state['response'])
"
```

---

## Architecture Reminder: Why MLA Matters on These GPUs

DeepSeek-V3 uses **Multi-head Latent Attention** — it compresses KV cache by projecting keys/values into a low-rank latent space:

```
Standard MHA KV cache: 2 × n_heads × d_head × seq_len × bytes
MLA KV cache:          d_c × seq_len × bytes   # d_c << n_heads × d_head
```

For V3: `d_c = 512` vs `n_heads × d_head = 128 × 128 = 16384` — that's **32x KV cache reduction**. This is why V3 can serve long contexts on MI300X that would OOM on equivalent VRAM with standard MHA.

---

## Recommendation for Your Setup

| Goal | Best Option |
| ------ | ------------ |
| Quick experiment, single GPU | **MI300X + SGLang + FP8** |
| Production serving | **2x MI300X + SGLang TP=2** |
| H200 access | **4x H200 + vLLM TP=4 + FP8** |
| Budget-conscious | **MI300X 1x, $2-4/hr, FP8 only** |

**Your AMD Dev Cloud MI300X is the right machine for this.** Single node, single GPU, FP8 — DeepSeek-V3 fits (barely, ~92% utilization) and SGLang's MLA optimization means you get decent throughput. Start there.

---

## References

- [DeepSeek-V3 GitHub](https://github.com/deepseek-ai/DeepSeek-V3)
- [SGLang MLA optimization](https://github.com/sgl-project/sglang)
- [vLLM AMD ROCm support](https://docs.vllm.ai/en/latest/getting_started/amd-installation.html)
- [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)
