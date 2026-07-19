---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3090 for CUDA Research
translated: false
type: note
---

Question: RX 7900 XT or RTX 3090 for local MoE/attention-architecture research, reproducing Kimi K2 Thinking techniques, and porting frontier tricks to smaller models — given RTX cards are pricier used (8-10k CNY)?

Answer: Buy the 3090. Not close, for your specific use cases.

**Why, concretely:**

1. **Every frontier repo you'll be reproducing ships CUDA-first.** Kimi K2 Thinking, DeepSeek-V3/R1 MoE kernels, any FlashAttention-3 variant, Mamba/linear-attention repos — all assume `torch.cuda`, custom CUDA kernels (often written in raw CUDA or Triton targeting NVIDIA), and `bitsandbytes`/`exllamav2` for quant. ROCm ports lag months behind and frequently just don't compile for research code (vs. production inference stacks like Ollama/vLLM which do get ported).

2. **NVLink matters for your MoE exploration.** Two 3090s give you ~112 GB/s NVLink vs PCIe-only ~32 GB/s on the AMD side 3090's NVLink versus 7900 XTX's PCIe-bound multi-GPU, since there's no cross-vendor tensor parallel and no NVLink equivalent on Radeon. For MoE-on-small-models experiments where you're doing expert-parallel or tensor-parallel across 2 cards, this is a real bottleneck difference, not a benchmark footnote.

3. **Ecosystem tools you'll actually reach for are CUDA-only.** No TensorRT-LLM, no ExLlamaV2 on the AMD side — you cannot use the fastest single-GPU INT4 inference path there. For "explore best-usable local model on scavenged hardware" (your point 4), ExLlamaV2 + GPTQ/AWQ on CUDA is still the fastest path per dollar.

4. **Where AMD would actually win — doesn't apply to you.** The MoE pattern (Qwen3-Coder, Gemma 4 style) plays well to a 24GB Radeon card because only a few billion params activate per token — this is a pure-inference argument. You're not doing pure inference; you're doing research reproduction and kernel-level experimentation, where CUDA's tooling maturity dominates.

5. **Price reality check against your CNY numbers:** used RTX 3090 at $749 (~5,400 CNY in the US market) is $100 cheaper than a used RX 7900 XTX and ~32% faster for inference in the US secondhand market. Your 8-10k CNY quote is China-market pricing (import/tariff premium on NVIDIA there), so the AMD-cheaper argument you're hearing doesn't hold as strongly as it looks — check actual local listings for both before assuming AMD's discount.

**Your "shallow ROCm understanding" framing is correct and not a bad thing** — ROCm's real value prop today is production *inference* serving (vLLM/Ollama) at lower $/GB-VRAM, not research reproduction. For goals 1, 2, 3, 5 in your list, you want the card the paper's code was written for. Goal 4 (old-card local-model scavenging) is the one place AMD is legitimately interesting to experiment with later, but don't make it your primary card.

**Practical move:** buy one 3090 now, verify with:

```bash
python -c "import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))"
nvidia-smi --query-gpu=name,memory.total,power.limit --format=csv
```

If your MoE/attention experiments need multi-GPU expert parallelism later, add a second 3090 for NVLink — still cheaper than one 4090 in most markets, and you keep the CUDA-native tooling for the whole stack you listed (Kimi verification, kernel porting, attention architecture comparison).

References:

- [ROCm vs CUDA for Local AI in 2026: The Software Gap](https://insiderllm.com/guides/rocm-vs-cuda-local-ai-2026/)
- [Radeon RX 7900 XTX for Local AI 2026 — Local AI Master](https://localaimaster.com/blog/radeon-7900-xtx-local-ai)
- [AMD vs NVIDIA for Local AI Inference in 2026 — GPU Hunter](https://www.gpuhunter.io/blog/amd-vs-nvidia-local-ai-2026)
