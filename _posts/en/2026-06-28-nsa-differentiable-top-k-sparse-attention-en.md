---
audio: false
generated: true
image: false
lang: en
layout: post
title: "NSA: Differentiable Top-K Sparse Attention"
translated: false
type: note
---

Question: Give a deeper intro to Native Sparse Attention (NSA) — the DeepSeek paper (arXiv 2502.11089), how its three branches work, how it makes top-k selection trainable, and why it's the key prior art for a trainable-selection sparse attention method like ERSA.

Answer:

NSA is the cleanest existing answer to a problem you've already bumped into: **how do you make "pick the top-k tokens to attend to" differentiable and fast enough to train end-to-end, not just bolt onto a frozen model at inference?** Most sparse-attention work (and a lot of KV-cache eviction work) is inference-only — you train dense, then sparsify. NSA's thesis is that this is leaving performance on the table, and that *native* (train-from-scratch sparse) attention can match or beat full attention while being dramatically cheaper.

Let me search for the specifics so I'm citing the actual mechanism rather than my memory of it.Now let me give you the full mechanistic picture.

## The core problem NSA solves

Standard attention is O(n²). Every sparse-attention method tries to make each query attend to only a subset of keys. The hard part is the **selection step**: "which keys matter for this query?" is a `top-k` operation, and `top-k` has **zero gradient almost everywhere** (it's a hard, discrete pick — perturb the scores infinitesimally and the selected set doesn't move, so ∂loss/∂score is 0). That's why nearly every prior method (H2O, StreamingLLM, SampleAttention, Quest) is **inference-only**: you train dense, then sparsify at decode time. The model never *learns* its own sparsity pattern, so there's a train/inference mismatch and a performance ceiling.

NSA's claim: make sparsity **native** — present during pretraining, fully differentiable, and trained end-to-end. NSA's pretraining loss curve is stable and smooth, and consistently outperforms the Full Attention baseline. That last part is the headline: sparse beats dense, not just approximates it.

## The three branches

For each query, NSA computes three separate attention outputs over the same K/V sequence and **gates** them together. The three sparse mechanisms are compression attention, selection attention, and sliding window attention.

**Branch 1 — Compression (coarse global).** Compress the key matrix into a lower-dimensional representation using an MLP. Concretely: chunk the sequence into blocks of size `l=32`, run a small learnable MLP (plus intra-block positional encoding) over each block of keys/values to produce **one compressed K and one compressed V per block**. The query attends over these `n/32` compressed tokens. This is cheap and gives every query a coarse view of the *entire* context. Critically, the attention scores against these compressed blocks double as **importance scores** for the next branch.

**Branch 2 — Selection (fine-grained, the trainable top-k).** This is the branch that matters for ERSA. Use the importance score computed in the compression step — the α value from compression attention — to find the top-k blocks. Then fetch the original uncompressed version of the selected top-k blocks from the original input, apply attention over only those selected blocks, and get the output. Block size here is `l'=64`, and `n=16` blocks are selected (including 1 fixed initial + 2 local blocks). So roughly: *compression scores tell you which 64-token chunks are worth looking at in full resolution, then you pull those chunks back at full fidelity.*

**Branch 3 — Sliding window (local).** Use the original key-value vectors, apply a sliding window, and obtain the attention. Window `w=512`. This is a dedicated path for recent/local tokens. The reason it's *separate* is subtle and important: local patterns are so strong and easy to learn that, without isolation, they dominate gradients and the other two branches never learn to do their job. Giving local context its own branch lets compression/selection specialize on long-range retrieval.

**Gating.** Gated outputs from compressed, selected, and sliding attentions are integrated. A small MLP on the query produces three sigmoid gate weights; the final output is the gated sum of the three branch outputs. This is MoE-style routing applied *inside the attention op* — which should resonate given your DeepSeek-v4 MoE interest.

## How the top-k becomes trainable (the key trick)

This is the crux. NSA doesn't make `top-k` itself differentiable — that's not the move. Instead:

1. **The selection scores are reused compression-attention scores**, which *are* differentiable (they're softmax outputs over the compression branch). So gradient flows into "how important is each block" through the compression path, even though the discrete pick is hard.
2. **Blockwise selection** (not per-token) is what makes it hardware-efficient. Per-token gather is memory-scatter hell on a GPU. By selecting contiguous 64-token blocks, NSA does coalesced loads that map onto Tensor Cores. NSA achieves speeds comparable to FlashAttention-2 with far fewer operations, supports end-to-end training, and uses hardware-friendly Triton kernels.
3. The gate MLP and compression MLP carry the learnable signal; the gradient to "select better blocks next time" arrives through the compression branch's scores, not through the argmax.

So the design sidesteps the non-differentiable `top-k` rather than patching it. **This is exactly why it's the prior art that dominates ERSA.** ERSA's contribution — using BCE-over-softmax (the eq-5 trick) to push gradient through `torch.topk` — is a *direct, cruder attack on the same gradient-zero problem.* NSA's paper explicitly frames inefficient back-propagation through selection as the thing to avoid, and its answer (reuse-compression-scores + blockwise + custom kernel) is both more principled and validated at scale. If Zeyu's framing is "we made trainable selection work," NSA got there first, at pretraining scale, from Liang Wenfeng's team, and won ACL Best Paper for it. That's not a citable-in-passing reference — it's the baseline the method has to beat or differentiate from.

## A minimal mental-model implementation

Not the real kernel (that's Triton), but the differentiable skeleton so the gradient path is concrete:

```python
import torch, torch.nn as nn, torch.nn.functional as F

class NSAttention(nn.Module):
    def __init__(self, d, l=32, l_sel=64, n_sel=16, w=512):
        super().__init__()
        self.l, self.l_sel, self.n_sel, self.w = l, l_sel, n_sel, w
        self.k_cmp = nn.Linear(l * d, d)   # compress a block of keys -> 1 key
        self.v_cmp = nn.Linear(l * d, d)
        self.gate  = nn.Linear(d, 3)       # per-query gate over 3 branches

    def forward(self, q, k, v):            # q,k,v: (T, d), causal
        T, d = q.shape

        # --- Branch 1: compression (coarse, global) ---
        nb = T // self.l
        kb = k[:nb*self.l].view(nb, self.l*d)
        vb = v[:nb*self.l].view(nb, self.l*d)
        k_c, v_c = self.k_cmp(kb), self.v_cmp(vb)        # (nb, d) each
        s_cmp = q @ k_c.T / d**0.5                       # (T, nb) importance scores
        a_cmp = s_cmp.softmax(-1)
        o_cmp = a_cmp @ v_c                              # (T, d)

        # --- Branch 2: selection (fine, uses s_cmp as importance) ---
        # map compression-block scores -> selection-block scores, pick top-k
        topk = s_cmp.topk(self.n_sel, dim=-1).indices    # hard pick (no grad here)
        # gradient reaches selection via s_cmp/a_cmp above, NOT via this argmax
        o_sel = gather_and_attend(q, k, v, topk, self.l_sel)  # full-res on chosen blocks

        # --- Branch 3: sliding window (local) ---
        o_win = sliding_window_attend(q, k, v, self.w)

        # --- Gated combine (MoE-style) ---
        g = self.gate(q).sigmoid()                       # (T, 3)
        return g[:,0:1]*o_cmp + g[:,1:2]*o_sel + g[:,2:3]*o_win
```

The thing to stare at: **gradient never needs to flow through `s_cmp.topk(...)`.** It flows through `a_cmp @ v_c` (compression output is a normal softmax-weighted sum) and through the gate. The selected-block output `o_sel` is differentiable *inside* the chosen blocks; the *choice* of blocks rides on compression scores that are already being trained by branch 1. That coupling — selection scores parasitic on a differentiable compression branch — is the whole insight, and it's what ERSA's BCE trick is independently (and more expensively) reinventing.

References:

- [Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089)](https://arxiv.org/abs/2502.11089)
- [NSA full text (HTML)](https://arxiv.org/html/2502.11089v1)
- [But why Deepseek — Native Sparse Attention? (selection-branch walkthrough)](https://medium.com/@anuragupperwal/but-why-deepseek-native-sparse-attention-d3ca8a099809)
- [NSA Surpasses Full Attention — math of token compression](https://medium.com/@ligtleyang/native-sparse-attention-surpasses-full-attention-in-performance-at-lightning-speed-0dc9af7c3f95)
