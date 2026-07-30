---
audio: false
generated: true
image: false
lang: en
layout: post
title: tqdm in PyTorch Training Loops
translated: false
type: note
---

Question: What does tqdm do in a PyTorch/LLM training loop?

Answer: `tqdm` is just a progress bar wrapper around any iterable. In training loops it wraps the dataloader (or range of steps) so you get iteration speed, ETA, and a live-updating postfix for loss/lr/grad-norm — nothing more, no framework magic.

```python
from tqdm import tqdm

for epoch in range(epochs):
    pbar = tqdm(train_loader, desc=f"epoch {epoch}")
    for batch in pbar:
        x, y = batch
        optimizer.zero_grad()
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()

        pbar.set_postfix(loss=loss.item(), lr=optimizer.param_groups[0]['lr'])
```

Key mechanics:
- `tqdm(iterable)` returns a generator wrapper — it calls `len()` on the iterable up front if available (dataloader has `__len__` via `len(dataset)/batch_size`) to compute the total for the bar and ETA.
- `set_postfix(**kwargs)` updates the trailing `{...}` dict on the bar without a new line — this is what you use for live loss/lr/tokens-per-sec.
- `set_description(str)` updates the leading label (e.g. `f"loss {loss:.4f}"`).
- Refresh is throttled internally (`mininterval=0.1s` default) so it doesn't spam stdout on fast loops — matters when you're doing thousands of micro-batches/sec on H100/MI300X, otherwise stdout flushing itself becomes a bottleneck.
- In multi-GPU/distributed (DDP), you gate `tqdm` behind `if rank == 0:` — every rank writing its own bar is a mess.
- Nested bars: `tqdm(range(epochs))` outer + `tqdm(train_loader, leave=False)` inner — `leave=False` clears the inner bar so it doesn't stack per epoch.
- For token-throughput style logging (common in your GPT-2 pretraining runs), people compute `tokens/sec` manually and shove it into `set_postfix` — tqdm itself only tracks `it/s`, not domain-specific throughput.

It's purely cosmetic/observability — has zero effect on gradients, on distributed comms, or on the actual training math. If it's slowing you down at high step-rate (rare, but happens on very fast H100 loops with tiny batches), disable with `disable=True` or bump `mininterval`.

References:
- [tqdm docs](https://tqdm.github.io/)
- [tqdm GitHub](https://github.com/tqdm/tqdm)