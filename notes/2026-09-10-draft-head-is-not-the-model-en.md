---
audio: false
generated: true
image: false
lang: en
layout: post
title: Draft Head Is Not The Model
translated: false
type: note
---

Build is done. But there's a hard blocker I need to make clear, and I verified it empirically:

## `Qwen3.8-27B-Uncensored-draft-Q8_0.gguf` is **not** the model

It's the **MTP draft head** (3.2 GB), a speculative-decoding sidecar for a 27B target. Proof:

```
$ ./build/bin/llama-server -m models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf
loading model 'models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf'
timeout: the monitored command dumped core     <-- no transformer blocks to run
```

Its metadata says `qwen35.block_count = 65` but the file only contains **18 tensors**, all of them `blk.64.*` plus `blk.64.nextn.*`:

```
qwen35.nextn_predict_layers = 1
  blk.64.attn_q.weight          Q8_0  [5120, 12288]
  blk.64.nextn.eh_proj.weight   Q8_0  [10240, 5120]   <- MTP fusion projection
  blk.64.nextn.enorm.weight     F32   [5120]
  blk.64.nextn.hnorm.weight     F32   [5120]
  output.weight / token_embd.weight ...
```

Blocks 0-63 are missing. Alone it cannot produce a single token. Your file comes from **`JonathanColetti/Qwen3.8-27B-Uncensored-GGUF`**, and the real model sits next to it.

## Build result (done)

`/mnt/data/llama.cpp/build/bin/llama-server` — CUDA 13.2, sm_89 (Ada), 2m44s.

## What you need next

Two options, both from that same repo. Your 12 GB RTX 4070 (~9.4 GB free) is the constraint; `-ngl auto --fit on` handles the split automatically.

**Option A - fused (simpler, MTP head is inline, 16.8 GB):**
```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-Q4_K_M.gguf --local-dir /mnt/data/llama.cpp/models

./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on --host 127.0.0.1 --port 8080
```

**Option B - reuse the draft file you already have (16.5 + 3.2 GB):**
```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-noMTP-Q4_K_M.gguf --local-dir /mnt/data/llama.cpp/models

./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-noMTP-Q4_K_M.gguf \
  -md models/Qwen3.8-27B-Uncensored-draft-Q8_0.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on --host 127.0.0.1 --port 8080
```

Then open `http://127.0.0.1:8080` for the web UI.

Note: this build has `LLAMA_CURL=OFF` (no libcurl dev headers on your box), so the server's `-hf` flag is unavailable - use the `hf` CLI for downloads as shown.

Want me to start the 16.8 GB download of Option A now? Say the word and I'll fetch it and launch the server.