---
audio: false
generated: true
image: false
lang: en
layout: post
title: Downloading and Running Gemma Models
translated: false
type: note
---

Yes! **llama.cpp fully supports Gemma models** (Gemma 1, Gemma 2, and the newer Gemma 3). I can see `ggml-vocab-gemma-4.gguf` in your models folder, confirming support is built in.

You don't have a Gemma model downloaded yet though. To run one:

**Option 1: Download a GGUF from Hugging Face**

For example, Gemma 2 9B (instruct):

```bash
cd ~/projects/llama.cpp
wget -O models/gemma-2-9b-it-Q4_K_M.gguf \
  https://huggingface.co/bartowski/gemma-2-9b-it-GGUF/resolve/main/gemma-2-9b-it-Q4_K_M.gguf
```

**Option 2: Convert from original Gemma (if you have it)**

If you already have the original Gemma model from Kaggle/Google:

```bash
python convert_hf_to_gguf.py --outfile models/gemma-2-9b.gguf /path/to/gemma-model/
./build/bin/llama-quantize models/gemma-2-9b.gguf models/gemma-2-9b-Q4_K_M.gguf Q4_K_M
```

**Then run it with llama-server:**

```bash
./build/bin/llama-server -m models/gemma-2-9b-it-Q4_K_M.gguf --port 8080
```

**Smaller option** — Gemma 2 2B runs on less VRAM (~2GB with Q4):

```bash
wget -O models/gemma-2-2b-it-Q4_K_M.gguf \
  https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf
```

Your GPU has ~24GB VRAM (from the 2099MiB usage shown), so Gemma 2 9B at Q4 (~6-7GB) would run comfortably. Want me to help download and start one?
