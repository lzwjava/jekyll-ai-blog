---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Training as Egg Checking
translated: false
type: note
---

Question: Is the "shake an egg to check if it's cooked" analogy a good mental model for LLM training — checkpoint frequently, monitor progress, terminate early if needed?

Answer:

Exactly right. The analogy maps cleanly:

| Egg check | LLM training equivalent |
| ----------- | ------------------------ |
| Shake to feel if yolk is set | Eval on checkpoint — loss, perplexity, downstream task |
| Don't wait until you crack it open | Don't wait until full training ends to discover divergence |
| Overcooking wastes energy | Unnecessary training steps waste GPU-hours ($$$) |

**The core principle: observable intermediate state → early decision.**

In nanoGPT terms:

```python
# Every N steps, checkpoint + eval
if step % eval_interval == 0:
    losses = estimate_loss()
    print(f"step {step}: train {losses['train']:.4f}, val {losses['val']:.4f}")

    if losses['val'] < best_val_loss:
        best_val_loss = losses['val']
        torch.save(checkpoint, 'ckpt.pt')

    # Early stop if val loss diverging from train loss (overfitting)
    if losses['val'] > losses['train'] * 1.3:
        print("Overfitting detected — stopping")
        break
```

**Training and inference as two processes** — yes, this works cleanly for scripts (unlike Java services with port conflicts). Common pattern:

```bash
# Terminal 1 — training
python train.py --out_dir=out/

# Terminal 2 — inference on latest checkpoint (polling)
watch -n 60 'python sample.py --checkpoint=out/ckpt.pt --prompt="test"'
```

No port conflict because both just do file I/O on the checkpoint. The inference process reads what training writes.

**The job market check = same principle.** Periodic signal sampling on an external system (industry demand) to calibrate your trajectory. DeepSeek MoE, inference optimization, agent frameworks — check what's actually being hired for every few weeks, not once a year.

The meta-lesson: **any long-running process with a goal needs intermediate checkpoints.** Training runs, career moves, startup pivots. The cost of not checking is always higher than the cost of the check itself.
