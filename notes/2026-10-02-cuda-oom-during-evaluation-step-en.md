---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA OOM During Evaluation Step
translated: false
type: note
---

Found it. There's no tmux session named `a` (your sessions are `0` = mihomo proxy and `1` = the training shell), but the error is in **session 1** — the training run **crashed with a CUDA Out-Of-Memory error during evaluation**.

## The error

```
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.51 GiB.
GPU 0 has a total capacity of 11.56 GiB of which 1.16 GiB is free.
...
File ".../nanochat/gpt.py", line 515, in forward
    logits = softcap * torch.tanh(logits / softcap)   # squash the logits
```

## What happened

1. Training itself was fine — it reached **step ~116** with healthy decreasing loss (~4.12).
2. Then a periodic **core evaluation** kicked in. It completed `coqa` and `boolq` fine.
3. During `bigbench_language_identification (10-shot)`, the eval ran a **forward pass on a long/batched input** and OOM'd right at the logits-squash line in `gpt.py:515`.
4. The process died and dropped back to the shell prompt (`lzw@to:/mnt/data/nanochat$`).

## Memory breakdown (GPU 0 = 11.56 GiB total)

- PyTorch allocated: 7.81 GiB
- PyTorch reserved but unallocated: 1.34 GiB (fragmentation)
- Only 1.16 GiB free when it tried to allocate another 1.51 GiB

## Likely fixes

1. **Reduce memory fragmentation** (what the error itself suggests):
   ```bash
   export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
   ```
2. **Reduce eval memory** — e.g. limit `max_per_task` (the `--core_metric_max_per_task` flag), reduce eval batch size, or use gradient/activation offloading for eval.
3. **Free memory before eval** — the training state (optimizer/activations) is still resident when eval runs; eval should run under `torch.no_grad()` (it does) but the model weights + training buffers may be competing. Consider running eval on CPU or a separate process.

Want me to look at `base_train.py` / `core_eval.py` to find the cleanest fix (e.g. cap the eval batch length or add `expandable_segments`)?