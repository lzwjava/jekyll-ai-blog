---
audio: false
generated: true
image: false
lang: en
layout: post
title: Simplest Qwen Inference Codebases
translated: false
type: note
---

**Question:** llama.cpp is too large to study. What's the simplest nanoGPT/nanochat-style codebase for *inference/serving* real models like Qwen?

**Answer:**

There are two clear winners depending on whether you want the Python/GPU path or the C/CPU path:

### 1. nano-vllm — the "nanoGPT of inference" (Python, ~1,200 lines)

This is the closest analog to nanoGPT for serving. It was created by a contributor to DeepSeek (name on the DeepSeek-V3/R1 technical reports), is ~1,200 lines of Python, and despite the minimal codebase implements prefix caching, tensor parallelism, CUDA graphs, and torch.compile — with throughput comparable to or slightly exceeding full vLLM. Benchmarks on an RTX 4070 Laptop GPU with Qwen3-0.6B show it matching or beating vLLM in offline inference — i.e., it'll run great on your 192.168.1.36 workstation.

```bash
pip install git+https://github.com/GeeeekExplorer/nano-vllm.git
huggingface-cli download Qwen/Qwen3-0.6B --local-dir ./Qwen3-0.6B
```

```python
from nanovllm import LLM, SamplingParams
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("./Qwen3-0.6B")
llm = LLM("./Qwen3-0.6B", enforce_eager=True, tensor_parallel_size=1)

prompts = [tok.apply_chat_template(
    [{"role": "user", "content": "explain KV cache in 3 sentences"}],
    tokenize=False, add_generation_prompt=True)]
out = llm.generate(prompts, SamplingParams(temperature=0.6, max_tokens=256))
print(out[0]["text"])
```

Why it's the right study target for you: it's literally a strip-down of vLLM's architecture. The scheduler is ~150 lines vs vLLM's thousands; the 98,800 lines between nano-vllm and vLLM are mostly production plumbing (timeouts, OOM recovery, metrics), and the model code in `models/qwen3.py` is a plain decoder-only transformer you can extend to other architectures. Read it in this order: `sequence.py` → `scheduler.py` → `block_manager.py` (paged KV cache) → `model_runner.py` → `models/qwen3.py`. That's the entire mental model of vLLM in an afternoon.

It's offline/batch by design — no HTTP server. Wrapping it in an OpenAI-compatible endpoint is ~30 lines of FastAPI, which is itself a good exercise (and there are community forks that already do it, e.g. the HF Inference Endpoints integration).

### 2. qwen3.c — the llama2.c successor (single-file C, ~1,000 lines, CPU)

If you want the Karpathy lineage directly: adriancable/qwen3.c started from Karpathy's llama2.c and runs Qwen3-architecture models in one dependency-free C file (~1,000 lines), with multi-core CPU support, Unicode, quantized checkpoints, and even reasoning mode — explicitly built as an up-to-date learning resource since the LLaMA 2 architecture is outdated.

```bash
git clone https://github.com/adriancable/qwen3.c && cd qwen3.c
python export.py Qwen3-4B.bin   # downloads + converts from HF, ~10 min
make
./run Qwen3-4B.bin -r 1          # -r 1 enables thinking mode
```

This runs fine on your M2 Air (no GPU needed). There's also a parallel project, gigit0000/qwen3.c, which loads GGUF directly with no conversion and adds multi-turn prefix caching, plus qwen3.cu — the same thing as a single pure-CUDA-C file, tokenization through CUDA kernels, no dependencies — the natural next step on the 4070 if you want to learn how the kernels themselves work below the PyTorch layer.

### How I'd sequence it given your goals

1. **nano-vllm on the 4070** — learn continuous batching, paged KV cache, scheduling. This is the serving-systems knowledge (directly transferable to understanding vLLM/SGLang internals).
2. **qwen3.c on the Air** — learn the raw forward pass: RMSNorm, RoPE, GQA, SwiGLU in plain C with no framework hiding anything.
3. **qwen3.cu** — bridge the two: hand-written attention/matmul kernels, the layer CUDA/HIP work lives at. Relevant prep for writing kernels on the MI300X too (port the kernels to HIP — it's mostly mechanical).

Note nanochat itself ships a minimal `Engine` with KV caching, but it only serves nanochat-trained checkpoints — it won't load Qwen weights, which is why nano-vllm/qwen3.c fill that gap.

**References:**

- [nano-vllm (GitHub, GeeeekExplorer)](https://github.com/GeeeekExplorer/nano-vllm)
- [Understanding LLM Inference Engines: Inside Nano-vLLM — Neutree](https://neutree.ai/blog/nano-vllm-part-1)
- [nano-vLLM architecture deep dive — morphllm](https://www.morphllm.com/nano-vllm)
- [qwen3.c (adriancable)](https://github.com/adriancable/qwen3.c)
- [qwen3.c GGUF variant (gigit0000)](https://github.com/gigit0000/qwen3.c)
- [qwen3.cu — single-file CUDA C](https://github.com/gigit0000/qwen3.cu)
