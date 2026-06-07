---
audio: false
generated: true
image: false
lang: en
layout: post
title: MPS Model Performance Summary
translated: false
type: note
---

Both models run perfectly on MPS. Here's a summary:

```
RESULTS
=======

1. Shakespeare char-level model (0.80M params)
   - Checkpoint: out-shakespeare-char/ckpt.pt (9.7 MB)
   - Device: MPS, dtype=float32
   - Output: Pseudo-Shakespeare with character names, dialogue format
   - "Forstan deefff, here the be dofenink you..."

2. GPT-2 from HuggingFace (123.65M params)
   - Loaded via: init_from=gpt2 (downloads weights automatically)
   - Device: MPS, dtype=float32
   - Prompt: "The future of AI is"
   - Output: Coherent, on-topic paragraphs about AI

MPS BENCHMARK
  100x matmul 1024x1024: 0.136s
  MPS available: True
  torch 2.11.0 via python3.14
```

Key notes for running on Mac:

- Use `python3.14` (has torch 2.11.0 with MPS) or `python3.13` (torch 2.6.0)
- `--device=mps --dtype=float32` (MPS doesn't support bfloat16 well)
- The model.py has debug prints enabled — you'll see tensor shapes for every layer during forward pass. Handy for learning, noisy for production.

Want me to try a larger model (gpt2-medium/large/xl), or try training something small on MPS?
