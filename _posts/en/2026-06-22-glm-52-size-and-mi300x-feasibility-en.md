---
audio: false
generated: true
image: false
lang: en
layout: post
title: GLM-5.2 Size and MI300X Feasibility
translated: false
type: note
---

**Question:** How large is GLM-5.2, and how do you run it? Is AMD MI300X sufficient?

**Answer:**

## Model Size

**753B parameters**, BF16/F32 tensors. At BF16 (2 bytes/param), that's roughly **~1.5 TB** of raw weights. It's a MoE model though (like DeepSeek), so active parameters per token are much smaller — but you still need to load all expert weights.

For practical deployment:

- **BF16 full precision**: ~1.5 TB VRAM — not feasible on a single MI300X
- **FP8 / INT8 quantized**: ~750 GB — still needs multiple GPUs
- **INT4 quantized (GGUF)**: ~380 GB — borderline on 2× MI300X or a single node

## AMD MI300X Feasibility

MI300X has 192 GB HBM3. **Single card: not enough** for BF16 or even FP8. Your options:

| Config | VRAM needed | Feasible on MI300X? |
|---|---|---|
| BF16 full | ~1.5 TB | Need 8× MI300X |
| FP8 | ~750 GB | Need 4× MI300X |
| INT4 (GGUF) | ~380 GB | Need 2× MI300X |
| INT4 + offload | ~100–150 GB active | Single MI300X (slow) |

The AMD Dev Cloud typically gives you **1 node = 1× MI300X** unless you request multi-GPU. Check if you can get a 4-GPU or 8-GPU node.

## How to Run It

### Option 1: vLLM (recommended for MI300X / ROCm)

```bash
pip install vllm

# BF16 on multi-GPU
vllm serve "zai-org/GLM-5.2" \
  --tensor-parallel-size 8 \
  --dtype bfloat16 \
  --max-model-len 32768

# Or FP8 quantized on fewer GPUs
vllm serve "zai-org/GLM-5.2" \
  --tensor-parallel-size 4 \
  --quantization fp8
```

For ROCm specifically:

```bash
pip install vllm --extra-index-url https://download.pytorch.org/whl/rocm6.1
```

### Option 2: SGLang (also supports ROCm)

```bash
pip install sglang

python3 -m sglang.launch_server \
  --model-path "zai-org/GLM-5.2" \
  --tp 4 \
  --host 0.0.0.0 \
  --port 30000
```

SGLang has a [GLM-5.2 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2) — use that.

### Option 3: INT4 quantized via llama.cpp / KTransformers (single MI300X)

KTransformers v0.5.12+ supports GLM-5.2. For a single 192 GB card with offloading:

```bash
# First grab a GGUF quantized version
huggingface-cli download \
  <some-user>/GLM-5.2-GGUF \
  --local-dir ./glm52-gguf

# Or build from source weights
python convert_hf_to_gguf.py zai-org/GLM-5.2 --outtype q4_k_m
```

Check [quantized models](https://huggingface.co/models?other=base_model:quantized:zai-org/GLM-5.2) — there are 24 quantized variants available.

### Inference via API after serving

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")

response = client.chat.completions.create(
    model="zai-org/GLM-5.2",
    messages=[{"role": "user", "content": "Explain MoE routing"}],
    max_tokens=1000,
)
print(response.choices[0].message.content)
```

## Key Architecture Notes

GLM-5.2 uses **IndexShare** — reuses the same indexer across every 4 sparse attention layers, cutting per-token FLOPs by 2.9× at 1M context. It also improves MTP (multi-token prediction) layers for speculative decoding, increasing acceptance length by up to 20%. This makes it more efficient than naive MoE at long contexts.

## Bottom Line

Your **single MI300X (192 GB) can run GLM-5.2 INT4** (~380 GB) only with aggressive CPU offloading via KTransformers, which will be slow (1–5 tok/s). For real throughput you need **2–4 MI300X nodes** — worth requesting a multi-GPU allocation on AMD Dev Cloud if you want to benchmark it seriously.

**References:**

- [GLM-5.2 HuggingFace](https://huggingface.co/zai-org/GLM-5.2)
- [GLM-5 Technical Report (arxiv 2602.15763)](https://arxiv.org/abs/2602.15763)
- [IndexShare paper (arxiv 2603.12201)](https://arxiv.org/abs/2603.12201)
- [SGLang GLM-5.2 Cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.2)
- [KTransformers GLM-5.2 Tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5.2-Tutorial.md)
