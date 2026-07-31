---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nano codebase internalization workflow
translated: false
type: note
---

Question: What's the right workflow for internalizing a "nano" codebase (nanoGPT, nanochat, nano-vllm) — clone, run, debug, log, read line-by-line, use an agent, experiment?

Answer: Yes, your instinct is right. Here's the actual sequence I'd use, in order of ROI:

**1. Run it before reading anything**

Don't open the code cold. Get a green run first — that gives you a ground truth to diff against later.

```bash
git clone https://github.com/karpathy/nanochat
cd nanochat
uv sync  # or pip install -e .
bash speedrun.sh  # or a scaled-down variant, see below
```

For nanoGPT/nano-vllm, always find the smallest possible config first — shrink `n_layer`, `n_embd`, `block_size`, batch size — so one iteration takes seconds not minutes. You want a fast inner loop, not a real training run.

```python
# nanoGPT: override in a scratch config
n_layer=2; n_head=2; n_embd=32
block_size=64; batch_size=4
max_iters=20; eval_interval=5
```

**2. Trace one tensor's full lifecycle, not the whole repo**

Reading top-to-bottom wastes time. Pick one tensor (e.g. `idx` -> logits) and grep/follow only its path:

```bash
grep -n "def forward" nanochat/gpt.py
python -c "
import torch
from nanochat.gpt import GPT, GPTConfig
cfg = GPTConfig(n_layer=2, n_head=2, n_embd=32, block_size=64, vocab_size=1000)
m = GPT(cfg)
x = torch.randint(0, 1000, (2, 8))
out = m(x)
print(out.shape if not isinstance(out, tuple) else [o.shape for o in out])
"
```

This forces you through attention, MLP, and the loss computation without reading config parsing, checkpointing, or distributed setup — save those for later passes.

**3. Instrument instead of just reading**

Add `print(x.shape, x.mean().item(), x.std().item())` after every major op, or use `torch.autograd.set_detect_anomaly` / hooks if you want gradient flow. For a repo like nano-vllm, instrument the scheduler/KV-cache path specifically — that's the actual novel content, everything else is standard transformer plumbing.

```python
def hook(name):
    def fn(module, inp, out):
        print(f"{name}: {out.shape if torch.is_tensor(out) else type(out)}")
    return fn

for name, module in model.named_modules():
    module.register_forward_hook(hook(name))
```

**4. Use an agent as a targeted debugger, not a summarizer**

Don't ask "explain this repo" — that gives you a shallow essay. Instead:

```bash
# with claude code / your own ww agent, cd into the repo and ask targeted diffs:
"trace how KV cache blocks are allocated and reused between nano-vllm's scheduler.py and block_manager.py, show me the actual function call chain for one decode step"
```

Agents are much better at "find every call site of X and explain why" than "explain the architecture." Use them to answer questions you already have from step 2/3, not to replace reading.

**5. Break it on purpose**

Change one hyperparameter, one line, and predict the effect before running:
- nanoGPT: kill weight tying (`lm_head.weight = wte.weight`), watch loss/param count
- nanochat: change `depth` and confirm width/heads/lr auto-scale as claimed the depth of the transformer is the single dial that automatically determines all other hyperparameters
- nano-vllm: shrink `max_num_seqs` or block size, watch scheduler behavior under contention

**6. Diff against the "real" version**

Karpathy explicitly built nanochat's `speedrun.sh` as the reference path — the runs/speedrun.sh script always reflects the reference way to train GPT-2 grade model and talk to it. If you fork and modify, always keep speedrun.sh runnable so you have a baseline to diff against.

For repo-specific questions (not "how to learn code" in general), Karpathy also points people to using DeepWiki from Devin/Cognition to ask questions about the repo, or the Discussions tab, or the #nanochat Discord channel — worth using DeepWiki as a second-opinion agent alongside your own.

One thing I'd add to your list: **write the test before you read the fix**. When something breaks (loss NaN, wrong shape), write a minimal repro script first, then read code — you'll read with a specific question in mind instead of scanning.

References:
- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [nanochat Discussion #1 — speedrun walkthrough](https://github.com/karpathy/nanochat/discussions/1)
- [nanochat Discussion #420 — depth/miniseries scaling](https://github.com/karpathy/nanochat/discussions/420)
- [nanochat/gpt.py](https://github.com/karpathy/nanochat/blob/master/nanochat/gpt.py)
