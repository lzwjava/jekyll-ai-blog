---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deepen Training, Fine-Tuning, MoE
translated: false
type: note
---

**Question:** Based on my AI portfolio, what should I do in the next few months to learn AI better — training, inference, what projects to build, what experiments to run?

**Answer:**

You've got a solid foundation: GPT-2 training from scratch, nanoGPT internals, ~2.3B tokens consumed, agent tooling (ww/iclaw/zz), and you've given a first-principles talk to 80 engineers. The gap between where you are and where Karpathy/Yin Wang operate is mostly **depth of understanding + publication/artifact quality**. Here's how I'd structure the next 3–6 months.

---

## 1. Go Deeper on Training — Finish the GPT Story Before Moving On

You've trained GPT-2 124M and 760M. The next inflection point is understanding **why** loss curves look the way they do, not just that they go down.

**Experiments to run on your existing nanoGPT fork:**

```python
# Track these explicitly per run — log to W&B or even just a CSV
{
  "model_size": "124M",
  "dataset": "fineweb-10B",
  "lr_schedule": "cosine",
  "batch_size": 524288,  # tokens
  "loss_at_1B_tokens": ...,
  "loss_at_5B_tokens": ...,
  "grad_norm_mean": ...,
  "throughput_tok_per_sec": ...,
}
```

Concrete experiments worth running, in order of ROI:

- **Chinchilla scaling** — train 124M on 2.5B tokens (20x params = optimal compute). Compare val loss vs your existing 760M run. Do the curves match the Chinchilla predictions? This forces you to understand the math, not just the recipe.
- **Learning rate sensitivity** — same model, 5 different peak LRs, log loss at 500M tokens. You'll internalize why `3e-4` is always the starting point.
- **Gradient accumulation vs batch size** — are they actually equivalent on your setup? They shouldn't be when you have BN (you don't, but the experiment teaches you why).
- **BF16 vs FP32 training loss delta** — on MI300X this is free to test.

---

## 2. The Missing Piece: Fine-Tuning + RLHF/DPO

You've done pretraining. You haven't done fine-tuning at the code level. This is the most commercially valuable skill gap you have right now.

**Project: nanochat — instruction fine-tuning from scratch**

This is exactly what Karpathy's nanochat is about. Build it yourself:

```python
# Phase 1: SFT on Alpaca/ShareGPT
# Start from your GPT-2 124M pretrained checkpoint
# Add chat template: <|user|>...<|assistant|>...
# Train with cross-entropy only on assistant tokens

def compute_sft_loss(logits, targets, mask):
    # mask = 1 only for assistant tokens
    loss = F.cross_entropy(logits.view(-1, logits.size(-1)),
                           targets.view(-1), reduction='none')
    return (loss * mask.view(-1)).sum() / mask.sum()
```

Then **DPO** (Direct Preference Optimization) — the math is simple, the implementation is ~100 lines:

```python
# DPO loss — no reward model needed
def dpo_loss(pi_logps_chosen, pi_logps_rejected,
             ref_logps_chosen, ref_logps_rejected, beta=0.1):
    pi_ratio = pi_logps_chosen - pi_logps_rejected
    ref_ratio = ref_logps_chosen - ref_logps_rejected
    return -F.logsigmoid(beta * (pi_ratio - ref_ratio)).mean()
```

Run this on Anthropic's HH-RLHF dataset or UltraFeedback. The goal isn't a great model — it's that you can say "I built SFT + DPO from scratch" and mean it at the code level.

---

## 3. MoE — You Listed DeepSeek v4, Now Implement It

You mentioned exploring DeepSeek v4 MoE. The gap is: have you actually implemented sparse routing? If not, this is the most important architecture experiment for the next 6 months.

**Minimal MoE implementation (~150 lines):**

```python
class SparseMoE(nn.Module):
    def __init__(self, n_experts=8, top_k=2, d_model=512, d_ff=2048):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, n_experts, bias=False)
        self.experts = nn.ModuleList([
            nn.Sequential(nn.Linear(d_model, d_ff), nn.GELU(),
                         nn.Linear(d_ff, d_model))
            for _ in range(n_experts)
        ])

    def forward(self, x):
        # x: (B, T, C)
        B, T, C = x.shape
        x_flat = x.view(-1, C)  # (B*T, C)

        logits = self.gate(x_flat)  # (B*T, n_experts)
        top_k_logits, top_k_indices = logits.topk(self.top_k, dim=-1)
        weights = F.softmax(top_k_logits, dim=-1)  # (B*T, top_k)

        out = torch.zeros_like(x_flat)
        for i, expert in enumerate(self.experts):
            mask = (top_k_indices == i).any(dim=-1)  # which tokens route here
            if mask.any():
                expert_out = expert(x_flat[mask])
                w = weights[mask][top_k_indices[mask] == i].unsqueeze(-1)
                out[mask] += w * expert_out

        # Load balancing loss
        routing_probs = F.softmax(logits, dim=-1).mean(0)  # (n_experts,)
        load_balance_loss = n_experts * (routing_probs * routing_probs).sum()

        return out.view(B, T, C), load_balance_loss
```

Then read DeepSeek-V2's auxiliary-free load balancing paper and implement that variant. The difference between top-k routing with load balance loss vs DeepSeek's approach is subtle but important.

---

## 4. Inference Engineering — You're Under-indexed Here

Your profile is pretraining-heavy. Inference optimization is where the real production value is and you'll need it as an AI engineer at a bank or a startup.

**Projects in order:**

**a) KV Cache from scratch** — implement in your nanoGPT:
```python
# During generation, cache K and V instead of recomputing
past_kv = []  # list of (k, v) per layer
for t in range(max_new_tokens):
    # only run forward on the new token, not full sequence
    logits, past_kv = model(x[:, -1:], past_kv=past_kv)
```

**b) Speculative decoding** — implement draft + verify loop. Pick a small model (124M) as draft, your 760M as target. Measure 2-4x speedup empirically on your RTX 4070.

**c) INT8/INT4 quantization** — use `bitsandbytes` or implement naive post-training quantization, measure perplexity degradation vs throughput gain. This is what you'd need in production at HSBC.

**d) vLLM / SGLang internals** — don't just use them. Read the PagedAttention paper, then trace through the vLLM codebase for one forward pass. Write a 1000-word blog post explaining it. This cements it.

---

## 5. One "Research-Grade" Artifact Per Month

You have 9,700+ notes and 400 blog posts. The next level is publishing something that gets cited or forked, not just read. Concretely:

- **Month 1:** A clean nanoGPT + DPO training script that beats existing tutorials in clarity. Put it on GitHub with proper benchmarks.
- **Month 2:** A blog post with actual training curves comparing Chinchilla-optimal vs over-trained models at 124M scale. Include the W&B links.
- **Month 3:** An MoE implementation with ablation results — top-2 routing vs top-4 vs dense baseline. Same architecture otherwise.

The goal: something Karpathy would retweet. That's the bar.

---

## 6. Agent Architecture — Upgrade iclaw

iclaw is a good MVP. The next version should implement:

- **ReAct loop with tool call retry** — if a tool fails, the agent decides whether to retry, replan, or give up. Most agent frameworks get this wrong.
- **Long-context summarization** — your `/compact` command is primitive. Implement hierarchical summarization: summarize old turns into a "memory block", keep recent turns verbatim.
- **Parallel tool calling** — dispatch multiple tool calls concurrently, merge results. This is what makes Claude Code feel fast.
- **Eval harness** — 20 tasks, measure success rate across model versions. Right now you have no way to know if iclaw v2 is better than v1.

---

## Priority Stack (Next 3 Months)

| Priority | Project | Machine | Time |
|----------|---------|---------|------|
| 1 | SFT + DPO from scratch on nanochat | MI300X | 3–4 weeks |
| 2 | MoE implementation with load balancing | RTX 4070 | 2 weeks |
| 3 | Speculative decoding on your 760M | RTX 4070 | 1 week |
| 4 | Chinchilla scaling experiment, W&B tracked | MI300X | 2 weeks |
| 5 | iclaw v2 with eval harness | MacBook | ongoing |

The single most leveraged thing you can do right now is **SFT + DPO from scratch**. It closes the biggest gap between your pretraining skill and production AI engineering, and it's the thing you can't fake having done.

---

**References:**

- [Chinchilla Scaling Laws — Hoffmann et al. 2022](https://arxiv.org/abs/2203.15556)
- [DPO: Direct Preference Optimization — Rafailov et al. 2023](https://arxiv.org/abs/2305.18290)
- [DeepSeek-V2: MoE Architecture](https://arxiv.org/abs/2405.04434)
- [PagedAttention / vLLM](https://arxiv.org/abs/2309.06180)
- [Speculative Decoding — Leviathan et al. 2023](https://arxiv.org/abs/2211.17192)
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
