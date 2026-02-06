---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Mastering llama.cpp CLI Options
translated: false
type: note
---

**Question:** Provide a comprehensive introduction to llama.cpp command line options.

**Answer:**

llama.cpp is a highly efficient C/C++ library for running large language models (LLMs) locally, with several main executables that share most parameters but have different purposes:

- **llama-cli** — interactive chat / text generation in terminal (most commonly used for testing)
- **llama-server** — OpenAI-compatible HTTP API server + simple web UI
- **llama-bench** — performance benchmarking
- others (llama-perplexity, llama-embedding, llama-eval-callbacks, …)

The vast majority of important options are **common** to llama-cli and llama-server.

### 1. Model Loading – Most Important Flags

- `-m, --model FNAME`  
  Path to GGUF model file (`.gguf`)

- `-hf, --hf-repo REPO` + `--hf-file FILE`  
  Download model directly from Hugging Face (e.g. `-hf bartowski/Llama-3.1-8B-Instruct-GGUF --hf-file Llama-3.1-8B-Instruct-Q5_K_M.gguf`)

- `--mmproj FNAME`  
  Path to multimodal projector (for vision/language models like llava, bakllava, obsidian, …)

### 2. Context & KV Cache Control

- `-c, --ctx-size N` / `--context-length N`  
  Maximum context length in tokens (default usually 4096 or 8192, 0 = model default)

- `--no-context-shift`  
  Disable context shifting when context is full (newer models often prefer this)

- `--rope-scaling yarn` / `--rope-scale N` / `--rope-freq-base` / `--rope-freq-scale`  
  Advanced RoPE scaling (important for context > original training length)

### 3. GPU / Acceleration Layers

- `-ngl, --n-gpu-layers N`  
  Number of layers to put on GPU (very important for speed)  
  - `999` / `-1` = try to put everything on GPU  
  - `0` = CPU only

- `-fa, --flash-attn`  
  Enable Flash Attention (usually faster & lower VRAM usage on modern GPUs)

- `-sm row` / `-sm block`  
  Split mode for model layers on multiple GPUs (row / block / layer)

- `--main-gpu INDEX` / `--tensor-split "0,0.5,0.5,…"`  
  Multi-GPU splitting control

- `--rpc-tensors` / `--no-rpc-tensors`  
  Offload tensors via RPC to another machine

### 4. Performance / Threading

- `-t, --threads N`  
  Number of CPU threads for generation (default ≈ all physical cores)

- `-tb, --threads-batch N`  
  Threads used for prompt processing / batch (often same as `-t` or slightly higher)

- `-b, --batch-size N`  
  Logical batch size (default 2048, 512–4096 common)

- `-ub, --ubatch-size N`  
  Physical micro-batch size (often 512–1024, important for very large prompts)

- `--cont-batching` / `--no-cont-batching`  
  Enable continuous batching (usually faster for server / parallel requests)

- `--no-mmap`  
  Disable memory mapping (sometimes needed on certain file systems or WSL)

### 5. Sampling – Controls creativity & quality

- `--temp N`  
  Temperature (0.0 = deterministic, 0.7–1.2 = creative, default ~0.8)

- `--top-k N`  
  Keep only top K tokens (20–50 common)

- `--top-p N`  
  Cumulative probability threshold (0.9–0.95 common)

- `--min-p N`  
  Minimum probability relative to the most likely token (0.05–0.1 very popular 2025+)

- `--tfs N` / `--typical N` / `--mirostat 2 --mirostat-tau 5.0 --mirostat-et 0.1`  
  Advanced samplers (mirostat v2 is very good default in 2025–2026)

- `--repeat-penalty N` / `--presence-penalty` / `--frequency-penalty`  
  Discourage repetition

- `--dry` family (dry-multipliers, dry-base, dry-sequence-breakers)  
  Newer repetition penalty method (2025+)

### 6. Prompt & Chat Control (especially llama-cli)

- `-cnv, --color --no-display-prompt --simple-io`  
  Pretty terminal chat mode

- `--chat-template TEMPLATE` / `--chat-template-file FILE`  
  Choose/alter chat template (chatml, llama-3, mistral, gemma, …)

- `-s, --simple-io`  
  Raw input/output (no fancy formatting)

- `--reverse-prompt STR` / `--in-prefix` / `--in-suffix`  
  Custom stop strings / prompt wrapping

- `-p, --prompt TEXT` / `-f, --file FILE`  
  Initial non-interactive prompt

- `-n, --n-predict N` / `-c, --ctx-size N`  
  How many tokens to generate (-1 = infinite until stop)

### 7. llama-server Specific (OpenAI compatible API)

- `--host 0.0.0.0 --port 8080`  
  Listen address/port

- `--path PREFIX`  
  API base path (default /v1)

- `--slots` / `--parallel N`  
  Maximum concurrent requests / slots

- `--embedding`  
  Enable embedding endpoint

- `--reasoning-format deepseek` / `--jinja`  
  Special handling for reasoning models / full jinja templates

- `--api-key-file` / `--ssl-key-file` / `--ssl-cert-file`  
  Authentication & HTTPS

### 8. Quick Reference – Popular 2025–2026 Combinations

**Fast local chat (good GPU):**

```bash
./llama-cli -m model-Q5_K_M.gguf -ngl 99 -fa --temp 0.7 --min-p 0.05 --top-k 40 --top-p 0.9 -c 32768 --color -cnv
```

**Max speed server (RTX 4090 / 5090 class):**

```bash
./llama-server -m model-Q6_K.gguf --n-gpu-layers 999 -fa --flash-attn --ubatch-size 1024 -c 32768 --temp 0.6 --min-p 0.1 --cont-batching --host 0.0.0.0
```

**Very long context CPU-only:**

```bash
./llama-cli -m model-Q4_K_M.gguf -ngl 0 -c 131072 --rope-scaling yarn --rope-scale 16 --no-mmap --threads 24
```

Options evolve quickly — always run `./llama-cli --help` or `./llama-server --help` for the most up-to-date list on your build.

**References:**

- [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp)
- [llama-cli comprehensive guide discussion](https://github.com/ggml-org/llama.cpp/discussions/15709)
- [llama-server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [Qwen llama.cpp usage examples](https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html)
- [llama.cpp manpage (Debian)](https://manpages.debian.org/testing/llama.cpp-tools/llama-cli.1.en.html)