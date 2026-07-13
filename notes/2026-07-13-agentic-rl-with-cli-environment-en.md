---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agentic RL with CLI Environment
translated: false
type: note
---

Question: Given my current portfolio (pretraining GPT-2 124M/760M from scratch, nanoGPT fork, DeepSeek-V2-Lite MoE inference, agent CLI tools ww/iclaw/zz, heavy production LLM usage), and my friend's framework (①reverse-engineer target company reqs, ②pick a frontier direction and find the company after) — how do I pick ONE research focus for the next quarter instead of scattering across MoE/KL/RL/MLA/Rotary/Muon/certs?

Answer:

Your two "friend" strategies aren't actually in tension for you — they converge on the same answer given what you've already built. Don't pick between them, find the intersection.

**The intersection: Agentic RL post-training, using your own pretrained model + your own CLI tools as the environment.**

Reasoning:

- Path ① (company-driven): Every Chinese lab you're already paying to use as an API customer (Xiaomi MIMO, MiniMax, DeepSeek-lineage) is hiring for post-training/RL, not pretraining. Pretraining headcount is nearly frozen industry-wide; RLHF/RLVR/agentic-RL teams are the ones scaling. Your token spend data literally shows you're already a power user of exactly the companies whose current hiring bottleneck is RL engineers who can debug reward hacking and KL blowup.
- Path ② (frontier-driven): the frontier direction in 2026 is agentic RL — training models to use tools correctly via RL rather than just SFT-imitating tool traces. You already built the environment for this without realizing it: `iclaw` and `ww` are literal tool-execution harnesses. That's 80% of an RL environment (env.step(), reward from exit code / test pass / diff correctness).

So: don't treat "MoE," "KL," "RL," "MLA," "Rotary/Muon" as five separate to-dos. Collapse them into one experiment: **run GRPO on your GPT-2 760M using your own agent's shell/tool-call tasks as the environment, with a KL-to-reference term.**

Concrete decision, not "it depends": spend the next 90 days shipping this, in order:

1. **Week 1-2 — reward + env first, not the algorithm.** Your model is too small/undertrained for real coding tasks, so pick a narrow verifiable task: given a broken shell command or a failing Python snippet (pull from your `zz` dataset scripts), reward = 1 if the model's tool call fixes it (test passes), 0 otherwise. Wire this to `iclaw`'s tool-calling loop directly — you already have the harness, don't rebuild it.

2. **Week 2-4 — GRPO with explicit KL, from scratch, not TRL.** Write the loss yourself so you actually understand it (Karpathy-style, no library magic):

```python
import torch, torch.nn.functional as F

def grpo_loss(logp_new, logp_old, logp_ref, advantages, mask, eps=0.2, beta=0.04):
    # logp_*: (B, T) per-token log-probs under current/old/ref policy
    # advantages: (B,) group-normalized reward, broadcast to (B, T)
    ratio = torch.exp(logp_new - logp_old)                     # (B, T)
    unclipped = ratio * advantages
    clipped = torch.clamp(ratio, 1 - eps, 1 + eps) * advantages
    pg_loss = -torch.min(unclipped, clipped)

    # k3 estimator (low-variance, unbiased KL approx), per-token
    log_ratio_ref = logp_ref - logp_new
    kl = torch.exp(log_ratio_ref) - log_ratio_ref - 1          # >= 0

    per_token_loss = (pg_loss + beta * kl) * mask
    return per_token_loss.sum() / mask.sum()

def group_advantages(rewards, group_size):
    r = rewards.view(-1, group_size)
    mean, std = r.mean(dim=1, keepdim=True), r.std(dim=1, keepdim=True) + 1e-4
    return ((r - mean) / std).view(-1)
```

The KL term here is exactly DeepSeekMath's k3 estimator — it's the unbiased low-variance MC estimator of KL(π_θ‖π_ref) you were about to go read papers about, so it acts as a low-variance, almost-unbiased Monte-Carlo estimator of KL divergence when the two policies are close. Worth noting: recent open work like Open-Reasoner-Zero has shown the KL term isn't strictly necessary for GRPO to work, and TRL now defaults β=0 — so treat KL as a stability knob to ablate, not a sacred term. That ablation (β=0 vs β=0.04 on your own 760M) is a better use of a week than reading five more papers about it.

3. **Week 4-8 — online policy distillation, which is item 2 on your list and falls out for free here.** Once GRPO runs, distill the RL-improved policy back into a smaller/faster student online (student samples, teacher scores/re-ranks, student updates) using the same reward signal. This is the same infra as step 2, just teacher=760M/student=124M.

4. **Only after that — MLA/MoE as an architecture swap, not a new project.** You already have DeepSeek-V2-Lite inference scripts in `zz`. Don't "learn MoE" abstractly — implement a minimal MLA + shared/routed-expert MoE block, swap it into your nanoGPT fork, retrain the 124M config, and diff perplexity/throughput vs vanilla attention. This is a 3-4 day exercise once you're not simultaneously context-switching to RL theory.

What to explicitly deprioritize this quarter: Rotary and Muon are drop-in — you can add RoPE to nanoGPT in an afternoon and swap AdamW→Muon as a config flag when you're bored, they don't deserve "focus" status. NCP-GENL cert (Sept) — keep it as a background task, not a research direction; it's credentialing, not research. "Catch up on all post-2022 papers" — stop doing this as a standalone activity; you'll pull the 5-10 papers you actually need (GRPO, DAPO, DeepSeek-V2 MLA, DeepSeek-V3 MoE routing) as you hit each step above.

The single sentence to answer your friend with: **"Agentic RL post-training with explicit KL control, using my own pretrained model and my own tool-calling agent as the environment — because it's what the labs I already use are hiring for, and it's the one frontier direction where I already own the entire stack instead of reimplementing someone else's."**

References:

- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO source paper)](https://arxiv.org/pdf/2402.03300)
- [Deep Dive into GRPO — implementation walkthrough](https://medium.com/@abhirupgupta123/deep-dive-into-grpo-03826359836c)
- [An unusual look at the KL-divergence term in DeepSeek R1 (k3 estimator explained)](https://aiwithmike.substack.com/p/an-unusual-look-of-the-kl-divergence)
- [TRL GRPO Trainer docs — β=0 default, KL ablation context](https://huggingface.co/docs/trl/main/en/grpo_trainer)
- [RLHF Book, ch. 6.3.6 — GRPO KL term derivation](https://arxiv.org/pdf/2504.12501)
- [Your own portfolio](https://lzwjava.github.io/ai-portfolio-en)
