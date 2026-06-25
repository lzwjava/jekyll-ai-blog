---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Complete — GPT-2 Done
translated: false
type: note
---

🎉 **Training COMPLETE!** Congrats!

The checkpoint confirms it:

  - **iter_num: 427,000** / max_iters: 427,000 — hit the full target
  - **best_val_loss: 3.466** — that's your final validation loss
  - GPT-2 124M (12 layers, 12 heads, 768 embd) trained on github-code
  - ~14B tokens processed (427k iters × batch 4 × accum 8 × block 1024)

The "train" tmux session is gone — it exited cleanly after finishing all 427k iterations and saving the final checkpoint. GPU is idle now (0% util, 43°C, 10W).

The model is sitting at:
  /mnt/data/nanoGPT/out-github-code-124m/ckpt.pt  (1.4 GB)

Want to do anything with it? Like converting to GGUF for llama.cpp, running some code generation samples, or pushing to HuggingFace?
