---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Training Completion Summary
translated: false
type: note
---

Training finished! Here's the final report:

**Done ✓** -- all 87,000 steps, ~30 hours (1,802 min) on RTX 4070 12GB

**Final stats:**

- **Val bpb: 0.372** -- solid for a 286M model on code
- Final loss band: ~1.06-1.13 (still bouncing)
- Peak VRAM: 6,240 MiB (only 52% of 12GB -- room to grow batch size)
- Checkpoint: `~/.cache/nanochat/base_checkpoints/d12/model_087000.pt`

**Sample outputs (base model, no SFT):**

```
The capital of France is the capital of France, and the capital of France is the capital of
The chemical symbol of gold is a number between 0 and 9.
The opposite of hot is a bit more complicated than it is.
If 5*x + 3 = 13, then x is 5*x + 3.
```

Classic base-model behavior -- recognizes the pattern structure but doesn't know facts. It's learned Python syntax and text structure (capitalize proper nouns, equation patterns, list enumerations), but it's a token predictor, not a Q&A bot. It needs SFT to turn this into a useful assistant.

**Script printed next steps:**

```
Evaluate: python -m scripts.base_eval --device-batch-size=8
Chat:     python -m scripts.chat_cli -p 'Write a Python function to reverse a linked list'
```

Want to run eval or try the chat CLI?
