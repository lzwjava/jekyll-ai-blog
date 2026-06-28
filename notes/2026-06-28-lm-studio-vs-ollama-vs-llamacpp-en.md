---
audio: false
generated: true
image: false
lang: en
layout: post
title: LM Studio vs. Ollama vs. llama.cpp
translated: false
type: note
---

Question: What is LM Studio (lmstudio.ai), and is it better than Ollama or llama.cpp?

Answer:

LM Studio is a closed-source desktop GUI app for running local LLMs. It wraps llama.cpp (and MLX on Apple Silicon) behind a polished interface — model discovery/download from Hugging Face, chat UI, and an OpenAI-compatible local server. It also ships a CLI (`lms`) and SDKs (Python/TypeScript). Free for personal use; recently free for commercial use too, but the app itself is not open source.

The stack hierarchy matters here because they're not really competitors at the same layer:

```
llama.cpp        ← the actual inference engine (C/C++, GGUF, CUDA/Metal/ROCm)
  │
  ├── Ollama     ← Go wrapper + model registry + daemon (uses llama.cpp under the hood)
  │
  └── LM Studio  ← GUI + llama.cpp + MLX backend (closed source)
```

So "better" depends on which layer you actually want to touch.

**For you specifically** — given your preferences (terminal-first, open-source bias, self-hosting, autonomy, building agents) — LM Studio is the wrong tool. It's a GUI-first, closed-source app. That conflicts with basically every axis you optimize for. You'd be putting a proprietary layer between yourself and an engine you should be reading the source of.

Quick comparison for your use case:

| | llama.cpp | Ollama | LM Studio |
|---|---|---|---|
| Open source | Yes (MIT) | Yes (MIT) | No |
| Interface | CLI/lib | CLI/daemon | GUI (+ CLI) |
| Control over flags | Full | Partial (Modelfile) | Limited (UI sliders) |
| OpenAI-compat server | `llama-server` | Yes | Yes |
| Apple MLX backend | No | No | Yes |
| Good for agents/scripting | Yes | Yes | Mediocre |
| Learning value | Highest | Medium | Lowest |

My actual recommendation for your trajectory:

**Use `llama.cpp` directly.** You're training GPT-2 from scratch and studying transformer internals — you should be running `llama-server` and `llama-cli` yourself, reading the KV cache and sampling code, understanding GGUF quantization (Q4_K_M, Q8_0, etc.). This compounds. LM Studio hides exactly the things you're trying to master.

```bash
# Build on your M2 (Metal auto-enabled)
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build -j

# Pull a GGUF and serve it OpenAI-style
./build/bin/llama-server \
  -hf bartowski/Qwen2.5-7B-Instruct-GGUF:Q4_K_M \
  --port 8080 -ngl 99 -c 8192

# Hit it like the OpenAI API
curl localhost:8080/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model":"local","messages":[{"role":"user","content":"hi"}]}'
```

**Use Ollama** when you just want zero-friction model management in scripts/agents and don't care about the GUI:

```bash
ollama serve &
ollama run qwen2.5:7b
# OpenAI-compat at localhost:11434/v1
```

The only genuine reason LM Studio wins: on Apple Silicon its **MLX** backend can outperform llama.cpp's Metal path for some models, and the model-discovery UX is smoother for non-technical users. Neither matters for you — your M2 Air has 16GB, you're memory-bound to ~7B Q4 models regardless, and you don't need discovery UX when you can `-hf` straight from Hugging Face.

Bottom line: LM Studio is a fine on-ramp for normal users. For someone reading nanoGPT and chasing llm internals, it's a layer of abstraction you should be removing, not adding. Go `llama.cpp` for depth, `ollama` for convenience, skip LM Studio.

References:

- [LM Studio](https://lmstudio.ai)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Ollama](https://github.com/ollama/ollama)
