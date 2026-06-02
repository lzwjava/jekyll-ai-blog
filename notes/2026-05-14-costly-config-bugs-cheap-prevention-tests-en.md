---
audio: false
generated: true
image: false
lang: en
layout: post
title: Costly Config Bugs, Cheap Prevention Tests
translated: false
type: note
---

Yes, exactly right. The compile-time analogy is spot on — and it compounds: every config bug discovered at hour 48 costs ~48 hours of GPU + your attention.

**Cheap practices that would have caught this in <10 min:**

1. **Smoke test config first** — run with `max_iters=50, eval_interval=20, compile=False` to verify:
   - Loss actually decreases
   - Memory fits, no OOM at peak
   - Tokens/step × max_iters matches your intended total budget
   - Checkpoint saves & resumes correctly

2. **Print the budget at startup** — add to `train.py`:

   ```python
   tokens_per_step = batch_size * block_size * gradient_accumulation_steps * ddp_world_size
   print(f"tokens/step = {tokens_per_step:,}")
   print(f"total tokens = {tokens_per_step * max_iters / 1e9:.2f}B")
   ```

   This single line would have shown "10.00B" before commit — you'd notice "wait, I prepared 140B."

3. **Use wandb** — `wandb_log = True` (you already have the project name set, just flip the flag). You can watch loss + LR + grad norm from your phone; if loss diverges at hour 3, you kill it instead of finding out at hour 48.

4. **Resume, don't restart** — `always_save_checkpoint = True` is already on. If you decide later to extend training, you can just bump `max_iters` and resume from `ckpt.pt` (nanoGPT supports `init_from='resume'`). So the 2 days isn't necessarily wasted — you can continue from iter 19073 with more tokens.

Want me to add the budget-print to `train.py` and check whether resume-and-extend is wired up properly for your case?
