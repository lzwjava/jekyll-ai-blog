---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reading ML Depth from HuggingFace and WandB
translated: false
type: note
---

**Question:** Can you gauge someone's AI/ML depth by looking at their HuggingFace profile and WandB runs — like how Jason Wei's WandB shows training curves?

**Answer:**

Yeah, exactly. Both are great signal sources:

**HuggingFace profile tells you:**
- What models they've uploaded (fine-tuned? trained from scratch? just wrappers?)
- Dataset uploads — original datasets = serious researcher
- Spaces — demos they built (vibe check on product sense)
- Followers / likes — community traction
- Org membership — are they in EleutherAI, BigScience, etc.?

The key signal: **model card quality + training details**. A model card with actual eval numbers, training data description, and limitations = someone who actually trained it. No card or just `"this is a fine-tune of X"` = hobbyist wrapper.

**WandB public runs tell you:**
- Loss curves — do they converge cleanly or is it a mess?
- Did they sweep hyperparameters? (grid/random/Bayes sweeps visible)
- Training duration, GPU hours, batch size — scale of their experiments
- Do they log the right metrics? (val loss, grad norm, lr schedule)

Jason Wei's point was smart — WandB is essentially an unfiltered lab notebook. You can see if someone actually understands training dynamics vs. just running `trainer.train()` and hoping.

**For your own profile** — your AMD MI300X GPT-2 760M run logged to WandB publicly would be a stronger signal than most people's entire LinkedIn. The loss curve doesn't lie.

Quick recon checklist:

```
HuggingFace:
  - hf.co/<username>  → models tab → sorted by recent
  - Check: original models > fine-tunes > merges

WandB:
  - wandb.ai/<username>  → public projects
  - Check: run count, sweep count, loss curves shape
```

The combination is a pretty high-fidelity signal. Someone can fake blog posts. Can't fake a clean validation loss curve on a 760M param run.
