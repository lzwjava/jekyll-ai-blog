---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mapping the AI Stack for Positioning
translated: false
type: note
---

**Question:** How should I systematically explore the AI value chain — from NVIDIA to AMD, open source models, local inference, chips, and tooling — then revisit in 3–6 months to spot which niches are moving and where to position myself? AI as a tool for both depth and breadth — right?

**Answer:**

Yes, exactly right. This is the correct meta-strategy: *survey the full stack, run experiments, let time reveal which bets compound.* Here's a structured map of the AI value chain with concrete things you can actually run and measure.

---

## The AI Value Chain, Layer by Layer

```
┌─────────────────────────────────────────┐
│           Applications / Agents          │  ← you build here now
├─────────────────────────────────────────┤
│        Models (open weights)             │  ← Llama, Qwen, Mistral, DeepSeek
├─────────────────────────────────────────┤
│     Inference Runtimes & Frameworks      │  ← vLLM, llama.cpp, MLX, ROCm
├─────────────────────────────────────────┤
│          Training Frameworks             │  ← PyTorch, FSDP, Megatron
├─────────────────────────────────────────┤
│            Hardware (GPU/NPU)            │  ← NVIDIA H100, AMD MI300X, Apple M2
├─────────────────────────────────────────┤
│        Chip Design & Compilers           │  ← CUDA, ROCm/HIP, Metal, Triton
└─────────────────────────────────────────┘
```

---

## Layer-by-Layer: What to Run + What to Watch

### 1. Hardware — NVIDIA vs AMD vs Apple

**You already have all three.** This is rare and valuable.

| Platform | Your Hardware | Key Stack |
|----------|--------------|-----------|
| NVIDIA | AMD Dev Cloud MI300X | ROCm + HIP |
| AMD | RTX 4070 (workstation) | CUDA 12.x |
| Apple | M2 Air | Metal + MLX |

**Run this week:**

```bash
# On M2 — MLX is Apple's answer to CUDA
pip install mlx mlx-lm
python -m mlx_lm.generate --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --prompt "Explain KV cache in one paragraph"

# On RTX 4070 — llama.cpp with CUDA
git clone https://github.com/ggml-org/llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j8
./build/bin/llama-cli -m qwen2.5-7b-q4_k_m.gguf -p "KV cache explanation"

# On MI300X — ROCm baseline
rocm-smi  # check device
pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

**What to benchmark:** tokens/sec per watt, VRAM headroom at different quant levels, time-to-first-token.

**Insight to track:** AMD MI300X has 192GB HBM3 — that's the single biggest moat right now for large model inference. Watch if ROCm software catches up to CUDA in 6 months.

---

### 2. Open Models — The Real Disruption

The open weight ecosystem is compressing commercial model lead times from years → months → weeks.

**Models worth running right now:**

```
Qwen3-235B (MoE)     — Alibaba, beats GPT-4o on many benchmarks
DeepSeek-R1          — reasoning, MIT license, runnable locally
Llama-3.3-70B        — Meta, best open dense model at 70B class
Gemma-3-27B          — Google, strong at coding
Mistral Small 3.1    — 24B, fast, Apache 2.0
```

**Experiment to run — model quality vs size tradeoff:**

```python
import subprocess, time

models = [
    "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b"  # via ollama
]
prompt = "Implement attention from scratch in numpy, with comments."

for m in models:
    t0 = time.time()
    result = subprocess.run(
        ["ollama", "run", m, prompt],
        capture_output=True, text=True
    )
    elapsed = time.time() - t0
    print(f"{m}: {elapsed:.1f}s, {len(result.stdout)} chars")
```

**What to watch in 6 months:** Does Qwen4 / Llama-4 close the gap with Claude/GPT-4.5 on agentic tasks? Does model size continue to shrink for same capability?

---

### 3. Inference Runtime — The Unsexy Moat

This layer is underrated. Whoever wins inference runtime wins developer mindshare.

| Runtime | Target | Key Feature |
|---------|--------|-------------|
| `llama.cpp` | CPU/GPU local | GGUF quant, universal |
| `vLLM` | GPU server | PagedAttention, high throughput |
| `MLX` | Apple Silicon | unified memory, fast on M-series |
| `ollama` | local DX | docker-like UX for models |
| `SGLang` | serving | structured generation, fast |
| `TensorRT-LLM` | NVIDIA production | max perf, NVIDIA-only |

**Run vLLM on your workstation:**

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --gpu-memory-utilization 0.85 \
  --max-model-len 8192

# Then hit it like OpenAI API
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen2.5-7B-Instruct","messages":[{"role":"user","content":"hello"}]}'
```

**What to watch:** Does SGLang overtake vLLM? Does llama.cpp get Vulkan/Metal performance parity with CUDA? Is there a runtime that abstracts CUDA vs ROCm cleanly?

---

### 4. Training & Fine-tuning — Your Existing Edge

You've trained GPT-2 from scratch. Next moves:

```bash
# LoRA fine-tune on your RTX 4070 (12GB is enough for 7B)
pip install unsloth
# Unsloth makes LoRA 2x faster, 60% less VRAM

from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen2.5-7B-Instruct",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16)
```

**What to watch:** Does GRPO (DeepSeek's RL method) become the standard over PPO/DPO for reasoning? Can you fine-tune a small model to outperform a large one on your specific bank domain tasks?

---

### 5. The Chip Layer — Understand Without Building

You don't need to design chips. But understanding the compute primitives makes you a better ML engineer.

**Key concepts to internalize:**

```
FLOPS        → raw compute (H100: 989 TFLOPS BF16)
Memory BW    → how fast weights move (H100: 3.35 TB/s HBM3)
Arithmetic Intensity → FLOPs / bytes = where your op is bottlenecked
Roofline model → visualizes compute vs memory bound
```

**Quick roofline intuition in code:**

```python
# Is your operation compute-bound or memory-bound?
# Matrix multiply A(M,K) @ B(K,N)
M, K, N = 4096, 4096, 4096

flops = 2 * M * K * N          # multiply-add
bytes = (M*K + K*N + M*N) * 2  # fp16, read inputs + write output
arithmetic_intensity = flops / bytes

# H100 peak: 989 TFLOPS compute, 3350 GB/s memory
ridge_point = 989e12 / 3350e9  # ~295 FLOPs/byte

print(f"Arithmetic intensity: {arithmetic_intensity:.1f} FLOPs/byte")
print(f"H100 ridge point: {ridge_point:.1f} FLOPs/byte")
print("Compute-bound" if arithmetic_intensity > ridge_point else "Memory-bound")
```

**What to watch:** Cerebras, Groq (LPU), Tenstorrent — any of these crack the inference latency problem at scale? Does AMD's MI400 close the gap with H100 successor?

---

## Your 3/6-Month Review Framework

Set a reminder. Come back and answer these:

```markdown
## AI Value Chain Snapshot — [DATE]

### Hardware
- [ ] NVIDIA market share in inference vs training: changed?
- [ ] AMD ROCm: is it usable without pain now?
- [ ] Apple MLX: did it reach serious model sizes (70B+)?

### Open Models
- [ ] What's the best open 7B / 70B model now?
- [ ] Has open source closed gap with GPT-5/Claude 4?
- [ ] Any new architecture beyond transformer?

### Inference
- [ ] vLLM vs SGLang vs llama.cpp: who won mindshare?
- [ ] Is there a unified CUDA/ROCm/Metal runtime yet?

### Training
- [ ] Is GRPO the new standard training method?
- [ ] Can I fine-tune a 7B to beat GPT-4 on my domain?

### Chips
- [ ] Groq / Cerebras: any real production deployment?
- [ ] TSMC 2nm yields: who gets allocation?

### Ecosystem niches to bet on
- [ ] Where is the unsexy infrastructure gap?
- [ ] What did every company start buying that nobody anticipated?
```

---

## Where to Position — Strategic Take

Given your profile (AI engineer at bank, agent builder, model trainer):

**Short-term (now–3mo):** Own the inference + agent layer. You can already build. Focus on: routing across models, fine-tuning small models for specific tasks, building evals.

**Medium-term (3–6mo):** Go deeper on ROCm. If AMD MI300X + ROCm becomes viable (huge "if"), being one of the few engineers who can navigate both CUDA and ROCm is a real moat. Right now almost nobody can.

**Long-term signal to watch:** Whoever wins the *agentic infrastructure* layer — task memory, multi-agent orchestration, tool use at scale — that's where the next platform emerges. You're already building there with your CLI agents.

---

**Yes, AI makes you both深入 (deep) and博识 (broadly knowledgeable)** — that's the compounding return. Each layer informs the others. Understanding roofline models makes you write better kernels, which makes you understand why vLLM's PagedAttention matters, which makes you build better agents. It's a virtuous cycle. Run the experiments, take notes, let 6 months of evidence tell you where the real leverage is.
