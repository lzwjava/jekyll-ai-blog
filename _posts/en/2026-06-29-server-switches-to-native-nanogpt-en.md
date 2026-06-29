---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Switches to Native nanoGPT
translated: false
type: note
---

Done. Server now uses the native nanoGPT model — identical to the workstation sample.py.

== WHAT CHANGED ==

  server.py now loads ckpt.pt via nanoGPT's native GPT class (model.py),
  instead of the converted HF transformers model. Uses tiktoken for encoding.

  Files on RunPod (/workspace/model/):
    ckpt.pt          1.4GB  — original nanoGPT checkpoint (47k steps)
    model.py         8.6KB  — nanoGPT model definition
    server.py        4.6KB  — rewritten, no transformers dependency
    hf-model/        622MB  — old HF model (kept as backup)

== COMPARISON (same prompt, "The Company reported total revenue of") ==

  Before (transformers + top_p):
    "Our principal business is our principal executive office in San Francisco,
     California and is located in The San Francisco, California..."

  After (native nanoGPT + top_k=200):
    "$2.0 million during the year ended December 31, 2016, the Company
     recognized non-cash impairment charges of $0.1 million... bad debt
     expense. See Note 9 for further details."

  Workstation sample.py (reference):
    "$167.0 million for the year ended December 31, 2023... The following
     table shows the Company's net revenue by geographic location..."

  Both now produce proper SEC filing language with financial figures.

== STATUS ==

  Health:    <http://localhost:8888/health> -> ok
  Server:    native nanoGPT, top_k=200, temp=0.8
  Model:     124M params, vocab 50304, bias=False
  Checkpoint: 47k steps (val loss 2.2778)
  No transformers dependency — just torch + tiktoken + fastapi
