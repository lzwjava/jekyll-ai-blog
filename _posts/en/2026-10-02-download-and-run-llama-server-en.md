---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download and Run Llama Server
translated: false
type: note
---

```bash
cd ~/projects/llama.cpp && wget -O models/Qwen3.8-27B-UD-IQ1_M.gguf https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-IQ1_M.gguf
```

Then run:

```bash
./build/bin/llama-server -m models/Qwen3.8-27B-UD-IQ1_M.gguf --port 8080
```

Open `http://localhost:8080` in browser.

Note: This is a **27B model at IQ1 (1-bit quantization)**, so it'll be small in size but quality may be impacted. If you have enough VRAM (~16GB), a Q4 or Q3 version would give much better results. Want me to find a higher quality GGUF for this model?
