---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adaptive Recurrent Depth with Parameter Reuse
translated: false
type: note
---

**Question:** What do you think about the idea of adaptive computation depth via hidden state-based per-token loop decisions — specifically training a ~100M parameter model that behaves like a 400M model through parameter reuse, and doing topic-wise comparisons?

**Answer:**

This is genuinely interesting research direction. Let me break down what your friend is proposing and where the real value is.

## The Core Idea: Adaptive Recurrent Depth

The paper they linked (arxiv 2604.21215) is almost certainly about **recurrent depth** — where instead of fixed L layers, you run the same layer block K times per token, but K is decided dynamically based on hidden state. This is the "looping" idea.

The key insight: **not all tokens need the same compute**. "The" needs 1 pass. "Therefore, given that the integral of e^x..." might need 8.

## Parameter Reuse → Effective Depth Amplification

The 100M → 400M equivalence math:

```
# Standard 400M model: 24 layers × ~16.7M params/layer
# Recurrent 100M model: 6 layers × 16.7M params/layer, looped up to 4x
# Per token: loop count K ∈ {1,2,3,4} decided by hidden state gate

class AdaptiveRecurrentBlock(nn.Module):
    def __init__(self, d_model=1024, max_loops=4):
        super().__init__()
        self.layer = TransformerBlock(d_model)  # shared weights
        self.halt_gate = nn.Linear(d_model, 1)  # per-token loop decision
        self.max_loops = max_loops

    def forward(self, x):
        # x: (B, T, D)
        halted = torch.zeros(x.shape[0], x.shape[1], device=x.device)
        out = x
        for k in range(self.max_loops):
            out = self.layer(out)
            # gate: should we stop?
            halt_prob = torch.sigmoid(self.halt_gate(out)).squeeze(-1)
            halted = halted + (1 - halted) * halt_prob  # ACT-style
            if halted.mean() > 0.99:
                break
        return out
```

This is basically **Universal Transformers** (Dehghani 2018) + **ACT (Adaptive Computation Time)** (Graves 2016), but applied with modern training tricks.

## Where Your Friend's Angle Gets Interesting

**Topic-wise comparison** is the genuinely novel contribution angle:

```python
# Hypothesis to test:
# - Code tokens → high loop depth (structured, requires planning)
# - Natural language → medium
# - Repetitive/formulaic text → low depth
# - Math reasoning → highest depth

topics = ["code", "math", "dialogue", "news", "poetry"]
for topic in topics:
    avg_depth = measure_avg_loop_depth(model, topic_dataset[topic])
    print(f"{topic}: {avg_depth:.2f} loops avg")
```

If you can show **empirically** that the model self-allocates depth in an interpretable, topic-consistent way — that's a publishable finding. It's mechanistic interpretability meets efficient inference.

## Practical Path on a Single GPU (RTX 4070 12GB)

100M recurrent model is very trainable:

```bash
# Rough compute budget
# 100M params, bfloat16 → ~200MB weights
# With optimizer states (AdamW) → ~800MB
# Activations for seq_len=512, batch=8 → ~2GB
# Total: fits in 12GB with headroom

python train.py \
  --n_layer 6 \
  --n_head 8 \
  --n_embd 1024 \
  --max_loops 4 \
  --halt_penalty 0.01 \  # penalize unnecessary compute
  --dataset openwebtext \
  --batch_size 8 \
  --compile  # torch.compile for speed
```

The `halt_penalty` coefficient is critical — too high and it always exits early (collapses to 1 loop), too low and it always runs max loops (no adaptation). This is the main hyperparameter to sweep.

## My Honest Assessment

**Strong parts of this idea:**

- Parameter efficiency story is real and measurable
- Topic-wise depth analysis is a clean, understandable experiment
- 100M scale is exactly right for one-GPU research
- The "swap one component" ablation structure maps well to a paper

**Risks:**

- Universal Transformers already exist — need to be clear about what's novel (the dynamic gating + topic analysis framing)
- Training stability: recurrent blocks with shared weights can have gradient issues (vanishing/exploding through loops). Use gradient clipping hard, maybe also loop-wise residual scaling
- The halt gate needs careful initialization — start biased toward "keep looping" or it never learns depth

**The strongest version of this project:**
Train on a diverse corpus, then do a **depth attribution map** — visualize which token positions in a sequence trigger high loop depth. If you can show that e.g. the verb in a complex sentence, or the `=` in a code assignment, triggers more loops — that's genuinely interpretable and interesting.

Worth doing. Start with nanoGPT base, add the recurrent block + ACT gate, train for a weekend, measure depth distributions per topic. That's a complete experiment.
