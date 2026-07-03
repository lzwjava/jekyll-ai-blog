---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing Qwen3-8B Via llama.cpp
translated: false
type: note
---

**Question:** Following up on the llama.cpp recommendation (over LM Studio/Ollama) — which model should I download to test it and then use daily?

**Answer:**

Two-stage answer: one tiny model to verify the build works, then a real daily driver sized to your hardware.

## Stage 1 — smoke test (30 seconds, no manual download)

llama.cpp can pull GGUF straight from HF with the `-hf` flag now — `llama-cli -hf ggml-org/gemma-3-1b-it-GGUF` runs a model directly from Hugging Face, and `llama-server -hf ggml-org/gemma-3-1b-it-GGUF` launches an OpenAI-compatible API server:

```bash
# Mac Air M2 (Metal auto-enabled)
brew install llama.cpp
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF

# or build from source on the 4070 box (better — you'll read the code anyway)
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j
./build/bin/llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

If tokens stream, the stack works. Gemma-3-1B is disposable — delete it after.

## Stage 2 — the actual model: Qwen3-8B Q4_K_M

For your two machines this is the consensus pick in 2026. Qwen3 8B is the recommendation for general use on constrained hardware — at Q4_K_M it uses about 5.5 GB of VRAM, leaving room for context, and it offers competitive quality across coding and general-purpose tasks. 5.5 GB fits comfortably in both your 4070's 12 GB (full GPU offload + long context) and the M2 Air's 16 GB unified memory (on Apple Silicon the full RAM pool is available to the GPU, so the VRAM distinction doesn't apply — but leave ~8 GB for macOS, so 8B Q4 is your practical ceiling on the Air).

```bash
llama-server -hf Qwen/Qwen3-8B-GGUF:Q4_K_M \
  --port 8080 -ngl 99 -c 16384 --flash-attn

# then point any OpenAI client at it
curl localhost:8080/v1/chat/completions -d '{
  "messages": [{"role":"user","content":"explain paged KV cache in 3 sentences"}]
}'
```

Qwen3 also has hybrid thinking mode (`/think` / `/no_think` in the prompt), which is worth poking at since you're studying sampling and reasoning-token behavior.

## Sizing map for your hardware

| Machine | Sweet spot | Ceiling | Notes |
|---|---|---|---|
| M2 Air 16 GB | Qwen3-4B Q4 | Qwen3-8B Q4 (~5.5 GB) | Watch swap; also try MLX — MLX gets 20–50% faster inference than llama.cpp on Apple Silicon |
| RTX 4070 12 GB | Qwen3-8B Q4 fully offloaded | Qwen3-14B Q4 (~9 GB, tight ctx) | This is your llama-server host |
| CPU-only fallback | Phi-4-mini 3.8B | — | ~3.5 GB at Q4_K_M, only viable option for 8 GB machines |

One rule worth internalizing: a larger Q4 model often beats a smaller Q8 model in the same memory budget — so prefer 8B-Q4 over 4B-Q8.

## Why not the others

- **DeepSeek-R1 distills** — good for reasoning-heavy tasks, but can be less steady than Qwen on strict XML tool-calling schemas in agent frameworks. Since you build CLI agents (iclaw), tool-call reliability matters more than raw reasoning benchmarks. Grab `deepseek-r1-distill-qwen-14b` later as a second model, not first.
- **Gemma 4 E4B/26B-A4B** — interesting MoE (E4B runs in as little as 3 GB VRAM, and the MoE setup keeps memory in check since only part of the model is active per token), worth studying for your DeepSeek-MoE learning track, but Qwen3 is stronger per byte for code.
- **Anything 30B+** — doesn't fit either machine at usable quality. When you want big-model experiments, that's what the MI300X droplet is for (and there you'd use vLLM, not llama.cpp — different layer, as we discussed).

Directly relevant to your study path: once Qwen3-8B is running under `llama-server`, diff its behavior against the same model under nano-vllm on the 4070. Same weights, two inference engines — that's the fastest way to make PagedAttention vs. GGUF-style KV cache concrete.

**References:**

- [llama.cpp (GitHub)](https://github.com/ggml-org/llama.cpp)
- [The Best Local LLM Models to Run in 2026 (daily.dev)](https://daily.dev/blog/best-local-llm-models-run/)
- [Local LLMs Are Getting Easier: The Complete Guide 2026 (SitePoint)](https://www.sitepoint.com/local-llms-are-getting-easier-the-complete-guide-2026/)
- [Best Local LLM Models 2026 — Developer Comparison (SitePoint)](https://www.sitepoint.com/best-local-llm-models-2026/)