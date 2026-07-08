---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning Concentrates in Early Phases
translated: false
type: note
---

Question: Is it true that most of what you learn from training a model happens in the early experimentation/setup phase (not the long 10-hour/7-day/month-long training run itself), and that iterating on someone else's existing checkpoint is a lower-cost way to keep learning?

Answer:

Mostly right, but you're underweighting one category of signal that *only* shows up in long runs, and that category happens to be your moat.

### Where the learning actually concentrates

Split a training run into three phases by information-per-wall-clock-hour:

**Phase A — first minutes to ~1hr (highest density of learning)**
This is where you catch: tokenizer bugs, dataloader shuffling bugs, wrong attention mask, loss not decreasing, wrong LR scale, gradient explosion at init, wrong dtype (bf16 vs fp32 accumulation), OOM at your target batch size. Almost all of your *correctness* learning happens here. This is exactly why nanoGPT/nanochat "speedrun" configs exist — Karpathy's own workflow is: get a tiny model training correctly in minutes, then scale the same recipe up, rather than debugging at scale.

```python
# minimal sanity-check harness before committing to a long run
import torch, time

def sanity_check(model, get_batch, steps=50):
    model.train()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)
    losses = []
    t0 = time.time()
    for i in range(steps):
        x, y = get_batch()
        logits = model(x)
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, logits.size(-1)), y.view(-1)
        )
        loss.backward()
        gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad()
        losses.append(loss.item())
        if i % 10 == 0:
            print(f"step {i:3d} loss {loss.item():.3f} gnorm {gnorm:.3f}")
    dt = time.time() - t0
    assert losses[-1] < losses[0], "loss not decreasing — stop, don't scale up yet"
    print(f"{steps} steps in {dt:.1f}s -> tokens/sec estimate for full run")
```

If this doesn't pass, a 7-day run just burns compute reproducing the same bug slower. So yes — cheap, fast iteration on small scale captures the majority of *debugging* signal.

**Phase B — hours to a few days (scaling-law signal)**
This is where you learn whether your recipe is *chinchilla-consistent* — does loss follow the expected power-law curve as you scale tokens/params, does your LR warmup+cosine schedule interact badly with your batch size, does MoE router load-balancing actually converge (this is DeepSeek-v4-relevant for you) or does it collapse into a few dead experts after enough steps. None of this shows up in a 50-step sanity check. You need enough steps to see the *shape* of the curve, not just the sign of the first derivative.

**Phase C — days to weeks (the part people skip discussing)**
This is where the actually rare, hard-to-fake learning lives, and it's *not* about the model — it's about **infra**:
- NCCL timeouts / stragglers in multi-node training
- checkpoint/resume correctness after a node dies at hour 130 of 168
- loss spikes that appear only after N tokens (data ordering, a bad shard, optimizer state corruption)
- thermal throttling / driver issues on long-duration MI300X or H100 runs
- disk I/O bottlenecks that only manifest once you've burned through cache

Nobody debugs this in a 50-step test. This is the stuff that separates "I ran a training script" from "I can be trusted to run *your* training job without it silently failing at 3am." For a consulting business selling Tinker-level infra expertise, this phase-C experience is disproportionately valuable *precisely because* it's expensive to acquire and most API-wrapper consultants have never sat through it.

### On "take someone else's checkpoint, it's cheaper"

Also correct, and it's the right default for **client revenue work** — LoRA/PEFT on an existing checkpoint gives you:
- iteration loop in minutes, not days
- inherits someone else's pretraining compute spend
- most consulting asks (domain adaptation, instruction tuning, RLHF/GRPO on top of a base model) don't require touching the pretraining loop at all

But it doesn't teach you optimizer dynamics at pretraining scale, MoE routing collapse/recovery, or the phase-C infra failure modes above — because those only exist *during* pretraining of a model from scratch. Fine-tuning existing checkpoints and running your own from-scratch pretrains (GPT-2 760M on MI300X, your DeepSeek-v4-MoE work) are complementary, not substitutes: one funds the business today, the other is the credibility asset that lets you charge Tinker-level rates instead of "another LangChain consultant" rates.

**Practical rule for your situation**: run Phase A/B cheaply and often (small scale, few $ each) to validate every new recipe/architecture idea fast — that's where "$20 out" experiments belong. Reserve full Phase C long runs for the ones where you specifically need to prove/observe scaling behavior or infra robustness you'll later sell as expertise, not for routine idea validation.
