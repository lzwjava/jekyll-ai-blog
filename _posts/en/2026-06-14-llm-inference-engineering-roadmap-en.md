---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Inference Engineering Roadmap
translated: false
type: note
---

**Question:** What is the learning roadmap for LLM inference engineering?

**Answer:**

## Mental Model First

LLM inference has two phases with completely different bottlenecks:

```
Prefill:  prompt tokens → KV cache computed   → COMPUTE-bound (matmuls)
Decode:   one token at a time, KV cache read  → MEMORY BANDWIDTH-bound
```

Everything in inference optimization flows from this single insight. Keep it as your north star.

---

## Stage 1: Transformer Forward Pass from Scratch (Week 1-2)

You already trained GPT-2 — but can you write the inference forward pass in pure NumPy? That's the test.

```python
import numpy as np

def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / np.sqrt(d_k)  # [B, H, S, S]
    if mask is not None:
        scores += mask * -1e9
    weights = softmax(scores, axis=-1)
    return weights @ V  # [B, H, S, D]

def transformer_block(x, W_qkv, W_o, W_ff1, W_ff2, W_ln1, W_ln2):
    # LayerNorm → Attention → Residual → LayerNorm → FFN → Residual
    x_norm = layer_norm(x, W_ln1)
    qkv = x_norm @ W_qkv          # [B, S, 3*H*D]
    Q, K, V = np.split(qkv, 3, axis=-1)
    attn_out = attention(Q, K, V) @ W_o
    x = x + attn_out              # residual
    x = x + ffn(layer_norm(x, W_ln2), W_ff1, W_ff2)
    return x
```

**Key shapes to memorize:**

```
Input:        [B, S, D]          B=batch, S=seqlen, D=model_dim
Q/K/V:        [B, H, S, D//H]   H=heads
KV cache:     [L, 2, B, H, S, D//H]   L=layers, 2=(K,V)
```

**Resources:**

- `nanoGPT/model.py` — Karpathy's cleanest reference
- Annotated Transformer (Harvard NLP)

---

## Stage 2: KV Cache & Memory Math (Week 2-3)

This is the heart of inference systems.

```python
# KV cache memory calculation
def kv_cache_size(model, batch_size, seq_len, dtype_bytes=2):
    layers = model.n_layers          # e.g. 32 for 7B
    heads = model.n_kv_heads         # GQA: fewer than n_heads
    head_dim = model.d_model // model.n_heads

    # Per token: 2 (K+V) * layers * heads * head_dim * dtype
    per_token = 2 * layers * heads * head_dim * dtype_bytes
    total = per_token * batch_size * seq_len
    return total

# Llama-3 8B example:
# layers=32, kv_heads=8 (GQA), head_dim=128, bf16
per_token = 2 * 32 * 8 * 128 * 2  # = 131072 bytes = 128 KB per token
# 4096 seq_len, batch=1: 512 MB just for KV cache
```

**What to understand deeply:**

- Why decode is memory-bandwidth-bound: each token reads entire KV cache once
- GQA (Grouped Query Attention) — Llama 2/3 uses it, reduces KV cache by `n_heads/n_kv_heads`
- MLA (Multi-head Latent Attention) — DeepSeek's approach, compress KV into latent vectors

---

## Stage 3: Quantization (Week 3-4)

```
FP32 → FP16/BF16 → INT8 → INT4 → 2-bit
         free         SmoothQuant  GPTQ/AWQ  extreme
```

```python
# Naive INT8 quantization
def quantize_weight(W, bits=8):
    scale = W.abs().max() / (2**(bits-1) - 1)
    W_int = (W / scale).round().clamp(-128, 127).to(torch.int8)
    return W_int, scale

def dequantize(W_int, scale):
    return W_int.float() * scale

# GPTQ insight: minimize ||WX - W_q X||² per layer
# Uses Hessian of activation to find optimal quantization order
```

**Ladder to climb:**

1. **GGUF/llama.cpp** — start here, k-quants (Q4_K_M, Q5_K_S), easy to experiment
2. **GPTQ** — layer-wise quantization with calibration data
3. **AWQ** (Activation-aware Weight Quantization) — protect salient weights
4. **SmoothQuant** — migrate quantization difficulty from activations to weights

```bash
# Practical: quantize a model and measure perplexity
pip install llama-cpp-python
# Q4_K_M vs Q8_0 — measure perplexity on wikitext-2
python -c "
from llama_cpp import Llama
model = Llama('model-Q4_K_M.gguf', n_ctx=512)
# benchmark tokens/sec
"
```

---

## Stage 4: Batching & Scheduling (Week 4-5)

```
Static batching:    wait for batch to fill → bad GPU utilization
Dynamic batching:   group by length        → better
Continuous batching: add/remove sequences mid-flight → vLLM's key insight
```

```python
# Conceptual: continuous batching scheduler
class Scheduler:
    def __init__(self, max_tokens_in_flight):
        self.running = []   # sequences being decoded
        self.waiting = []   # sequences waiting for prefill
        self.max_tokens = max_tokens_in_flight

    def step(self):
        # Preempt if KV cache full (swap to CPU or recompute)
        self._preempt_if_needed()
        # Add new sequences if budget allows
        self._admit_from_waiting()
        # Return batch for this forward pass
        return self._build_batch()
```

**Read this code:**

```bash
git clone https://github.com/vllm-project/vllm
cat vllm/core/scheduler.py     # continuous batching
cat vllm/core/block_manager.py # PagedAttention memory
```

**PagedAttention in one sentence:** KV cache stored in non-contiguous blocks (like OS pages), mapped via block table — eliminates fragmentation, enables sharing prompt KV across requests.

---

## Stage 5: FlashAttention (Week 5-6)

The single most important kernel to understand.

```
Naive attention:    O(N²) HBM reads/writes  (slow)
FlashAttention:     O(N²) FLOPs, O(N) HBM  (fast)
```

```
Key trick: tile the QK^T computation into SRAM-sized blocks
           compute softmax incrementally (online softmax)
           never materialize full N×N attention matrix in HBM
```

```python
# Online softmax — the mathematical core of FlashAttention
def online_softmax(scores_block, running_max, running_sum):
    new_max = max(running_max, scores_block.max())
    # Rescale old sum
    running_sum = running_sum * exp(running_max - new_max)
    # Add new block
    running_sum += exp(scores_block - new_max).sum()
    running_max = new_max
    return running_max, running_sum
```

**Read:** FlashAttention-2 paper (Dao et al.), then `flash_attn/flash_attn_triton.py`

---

## Stage 6: Speculative Decoding (Week 6-7)

```
Problem:  decode is sequential, one token per forward pass → slow
Insight:  small draft model proposes k tokens, large model verifies in parallel

Speedup:  if acceptance rate α, speedup ≈ k·α / (1 + cost_of_draft)
Typical:  2-3x on code/repetitive text
```

```python
def speculative_decode(draft_model, target_model, prompt, k=4):
    draft_tokens = draft_model.generate(prompt, k)  # k tokens, cheap
    # Target model scores all k+1 positions in ONE forward pass
    target_logits = target_model(prompt + draft_tokens)

    accepted = []
    for i, token in enumerate(draft_tokens):
        p_target = softmax(target_logits[i])[token]
        p_draft  = draft_model.probs[i][token]
        # Accept with probability min(1, p_target/p_draft)
        if random() < min(1.0, p_target / p_draft):
            accepted.append(token)
        else:
            # Resample from corrected distribution
            accepted.append(sample_corrected(target_logits[i], p_draft))
            break
    return accepted
```

---

## Stage 7: Tensor Parallelism & Serving at Scale (Week 7-8)

```
Tensor Parallel:    split weight matrices across GPUs (Megatron-style)
Pipeline Parallel:  split layers across GPUs
Sequence Parallel:  split sequence dimension (for long context)
```

```python
# Tensor parallel: column-parallel linear
# W shape [D_in, D_out] split into N GPUs → each holds [D_in, D_out/N]
# Each GPU computes partial result, then AllReduce

# In vLLM: controlled by tensor_parallel_size argument
from vllm import LLM
llm = LLM("meta-llama/Llama-3-70b", tensor_parallel_size=4)
```

---

## Your Concrete Roadmap

```
Week 1-2:   Write GPT-2 forward pass from scratch (no PyTorch)
            Read nanoGPT model.py line by line
            Implement KV cache manually, verify output matches

Week 3:     llama.cpp deep dive
            Build from source, run with different quants
            Read ggml-cuda.cu — understand hand-written CUDA matmul

Week 4:     vLLM internals
            scheduler.py + block_manager.py
            Run vLLM on your 4070, benchmark throughput vs llama.cpp

Week 5:     FlashAttention
            Read FA2 paper
            Run flash_attn Triton kernel, compare to naive attention

Week 6:     SGLang + RadixAttention
            sglang/srt/managers/radix_cache.py
            Benchmark prefix caching benefit on repeated system prompts

Week 7:     Quantization experiments
            GGUF Q4_K_M vs Q8_0 perplexity on wikitext-2
            Try AWQ on a 7B model on your MI300X

Week 8:     Speculative decoding
            Implement toy version from scratch
            Profile where time is spent: prefill vs decode
```

---

## Key Papers (in order)

| Paper | Why |
| --- | --- |
| Attention Is All You Need | baseline |
| FlashAttention-2 (Dao 2023) | most important kernel |
| PagedAttention / vLLM (Kwon 2023) | memory management |
| Continuous Batching (Yu 2022) | scheduling |
| GQA (Ainslie 2023) | modern KV reduction |
| AWQ (Lin 2023) | best practical quantization |
| Speculative Decoding (Leviathan 2023) | latency reduction |
| DeepSeek-V2 MLA | future of KV compression |

---

## Your Unfair Advantage

You have MI300X with 192GB HBM3. Most inference researchers don't have that. Use it to:

- Run 70B models unquantized and profile memory bandwidth utilization
- Benchmark ROCm vs CUDA kernels (vLLM supports both)
- Experiment with batch sizes that don't fit on consumer GPUs

That's a real edge. Most people studying inference are bottlenecked by GPU memory — you're not.
