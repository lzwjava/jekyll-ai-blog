---
audio: false
generated: true
image: false
lang: en
layout: post
title: One Feed-Forward Pipeline
translated: false
type: note
---

Here's the full synthesis of all four sources of evidence — your portfolio, your MoE note, your RL note, and the two comprehensive analyses you just received — into one coherent next-direction answer.

---

## Where You Actually Are Right Now

Reading across all your artifacts, your actual state is:

**Already proven:**

- GPT-2 124M from scratch on RTX 4070 (SEC filings, val loss 2.28, deployed chatbot)
- GPT-2 760M from scratch on MI300X (nanochat config)
- nanoGPT fork with 45 commits, 6 training configs, dataset pipelines
- Two-node DDP debugging (CPU gloo hang, learned torchrun mechanics)
- H200 nanochat runs (found device_batch=32 sweet spot for 1.38B model)
- SEC-EDGAR-GPT end-to-end in 3 days using Hermes Agent
- CLI agents: ww (255+ commits), iclaw (agent REPL with tool calling), zz (dataset/training pipeline)
- DeepSeek-V2-Lite inference scripts in zz
- 3B+ tokens/year API consumption across OpenRouter, Claude, Xiaomi MIMO
- ~70K monthly page views on blog, 10K+ posts, 9.7K+ AI answer notes

**Studied but not yet implemented in code:**

- MoE routing
- Multi-head Latent Attention (MLA)
- GRPO / RL post-training
- Distillation pipeline
- FlashAttention kernel-level mechanics

**Hardware in hand or incoming:**

- RTX 4070 12GB (active, daily driver)
- MI50 x2-3 at repair shop (ROCm status TBD, 16GB HBM2 each if healthy)
- RunPod H200 burst (10-hour sessions, occasional)

---

## The Core Tension You Need Resolved

Your July 13 "Focus on MoE Implementation" note says:

> **Skip RLHF/GRPO** — Poor hardware fit (needs reward model, multi-stage training). Learn later via distillation axis.

The comprehensive answer you just received says the opposite:

> **Agentic RL post-training is exactly what fits your hardware** — MI50s as cheap always-on inference for rollouts, 4070 for the dev loop, H200 burst for optimizer steps. This is the defensible research niche.

Which one is right?

The MoE note was written **before the MI50s entered your plan and without realizing iclaw/ww already constitutes an RL environment**. The comprehensive answer accounts for those two facts — and it's correct. An MI50 running `vllm-gfx906` serving a frozen reference policy + generating rollouts at near-zero marginal cost is exactly the piece that makes RL post-training viable on your hardware. Without that piece, RL on RTX 4070 alone is cramped (small models, slow iteration). With MI50s, the division of labor makes efficient sense.

So the comprehensive answer wins the strategic debate. But it doesn't mean you skip MoE — it means you **sequence MoE first, then RL, then merge them**.

---

## The Answer: One Feed-Forward Pipeline, Not Two Directions

Don't choose between MoE and RL. They are not separate projects — they are steps 1 and 2 of the same pipeline, and step 3 is the comparison between them, which is your paper.

### Phase 1 — Weeks 1-3: MoE from scratch into nanoGPT

**Why first:** Your MI50s are unconfirmed. You need a guaranteed output in weeks, not months. MoE in nanoGPT is ~150 lines of code — swap the dense FFN for an 8-expert top-2 router with load balancing loss. You can train it on RTX 4070 tonight. No hardware dependency.

**Concrete steps:**

1. Implement `class MoEFFN(nn.Module)` with `top_k=2`, `n_experts=8`, load balancing loss
2. Replace `MLP` in your nanoGPT with `MoEFFN` (gated by model config: `use_moe=True`)
3. Train GPT-2 124M config on RTX 4070 — compare dense vs MoE loss curves
4. Analyze expert utilization heatmaps, capacity factor, expert collapse
5. Publish one blog post: "Training Small MoE from Scratch"

This is **determinate** — you will have a working MoE in 3 weeks. No "waiting for hardware," no "if ROCm works."

### Phase 2 — Week 4: Hardware assessment breakpoint

By week 4 you'll know:

- Are the MI50s healthy? Does ROCm 6.4.3 + vllm-gfx906 work?
- If yes → you now have cheap always-on inference. This changes the RL plan's scope.
- If no → you still do RL on RTX 4070 alone. Smaller scale (124M), same algorithm, same learning.

### Phase 3 — Weeks 5-10: Agentic GRPO post-training

This follows the comprehensive answer's sequence exactly, but now your MoE model is available as the architecture variant:

1. **Reward + environment first**: Use iclaw's tool-calling loop. A broken shell command or failing Python snippet (from your zz dataset scripts) as the task. Reward = 1 if the model's tool call fixes it (test passes), 0 otherwise. You already have the harness — don't rebuild it.

2. **GRPO from scratch, no TRL library**: Write the loss yourself. The k3 KL estimator from DeepSeekMath (low-variance, unbiased MC estimate of KL divergence):

```python
def grpo_loss(logp_new, logp_old, logp_ref, advantages, mask, eps=0.2, beta=0.04):
    ratio = torch.exp(logp_new - logp_old)
    unclipped = ratio * advantages
    clipped = torch.clamp(ratio, 1 - eps, 1 + eps) * advantages
    pg_loss = -torch.min(unclipped, clipped)

    log_ratio_ref = logp_ref - logp_new
    kl = torch.exp(log_ratio_ref) - log_ratio_ref - 1

    per_token = (pg_loss + beta * kl) * mask
    return per_token.sum() / mask.sum()
```

3. **Default KL to β=0.04, but ablate it**: Recent open work (Open-Reasoner-Zero, TRL's β=0 default) shows KL isn't strictly required. That ablation (β=0 vs β=0.04 on your own 760M) is a better use of a week than reading five more papers about it.

4. **Online policy distillation**: Teacher=760M, student=124M, same reward signal. Falls out naturally from the same infra.

5. **The merge point — MoE vs dense**: Swap your MoE model in as the policy. Compare: does MoE help or hurt in GRPO? Does the routing pattern change under RL? This is your paper's Figure 3.

### Phase 4 — Week 10: H200 burst (one session)

Use a single H200 10-hour burst to run the 760M full GRPO backward pass — confirm your 4070-scale findings hold at larger model size. MoE vs dense on H200 is your paper's Figure 4.

### Phase 5 — Weeks 11-12: Write

One paper: **"Agentic RL Post-Training on Consumer Hardware: MoE vs Dense Policies with Your Own CLI Environment."**

Sections:

- Architecture: MoE implementation in nanoGPT
- Environment: CLI tool-calling tasks via iclaw
- Algorithm: GRPO with k3 KL ablation
- Results: Dense vs MoE GRPO, KL-on vs KL-off, 124M vs 760M scale
- Hardware mapping: MI50 as rollout server, RTX 4070 as dev loop, H200 for optimizer burst

---

## What to Deprioritize This Quarter

| Item | Why skip now |
| --- | --- |
| MLA from scratch | Do it after MoE + RL are done. MLA is a Day-2 architecture swap, the same pattern as MoE. |
| FlashAttention kernel | RTX 4070 doesn't need custom kernels — PyTorch SDPA works. Come back if you hit inference bottlenecks. |
| Rotary / Muon | Drop-in changes, not research. Add RoPE to nanoGPT in one afternoon. Swap AdamW→Muon as a config flag. |
| "Catch up on all post-2022 papers" | Pull the 5-10 papers you actually need as you hit each step above. Don't make reading a standalone activity. |
| NCP-GENL cert (Sept) | Credentialing, not research. Keep it as background, not a direction. |

---

## The Hardware Strategy (After MI50 Assessment)

Best case (MI50s healthy, ROCm works):

```
MI50 x2          → vllm-gfx906, GPTQ quantized
(vllm-gfx906)      → serves frozen reference policy (KL calc)
                   → generates rollouts (policy pi_old)
                   → serves reward/verifier model

RTX 4070         → dev loop, debug GRPO loss, 124M sanity runs
                   → fast iterate on reward hacking

H200 (burst)     → 760M full GRPO backward pass
                   → sync updated weights back to MI50 servers
```

Worst case (MI50s don't work):

```
RTX 4070 alone   → everything on one GPU, smaller scale (124M)
                   → slower iteration, same algorithm
                   → H200 for 760M when needed
```

You still learn the same things either way. The MI50s are a throughput multiplier, not a blocker.

---

## The One Sentence for Your Friends

> **"I'm building the full pipeline: MoE architecture in my own model → agentic GRPO post-training using my own CLI tools as the environment → the MoE-vs-dense comparison under RL as the paper — all sequenced as one feed-forward project, not two separate directions."**

Your previous research direction ("I train small efficient LLMs from scratch and understand every layer") upgrades to:

> **"I train small efficient LLMs from scratch and post-train them with RL using my own agent infrastructure."**

This is defensible because (a) the labs you're already a customer of — Xiaomi, MiniMax, DeepSeek-lineage — are hiring for exactly this skill, (b) you own the entire stack end-to-end which most people don't, and (c) cheap-hardware RL-loop engineering is the skill gap that well-funded labs never had to solve.
