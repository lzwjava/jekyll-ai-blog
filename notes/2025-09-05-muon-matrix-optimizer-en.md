---
audio: false
generated: true
image: false
lang: en
layout: post
title: 'Muon: Structure-Aware Matrix Optimizer'
translated: false
type: note
---

“Muon” in Kimi refers to an advanced optimizer—specifically a **structure-aware, matrix-orthogonalizing optimizer** used in training the Kimi K2 language model.

---

### What Is the Muon Optimizer?

1. **Matrix-Aware Optimization**
   Unlike AdamW or SGD, Muon treats weight matrices as geometric entities rather than independent scalar parameters. It applies **Newton–Schulz iterations** to orthogonalize the momentum-averaged gradient, yielding well-conditioned, balanced updates that respect both row and column structure of the matrix ([Medium][1], [kellerjordan.github.io][2]).

2. **Orthogonalization via Newton–Schulz**
   Rather than performing expensive Singular Value Decomposition (SVD), Muon uses a fast iterative method (Newton–Schulz) to approximate the nearest orthogonal matrix to the gradient. This keeps the update under **spectral norm constraints**, preserving energy and spreading learning across all directions equally ([Medium][1], [kellerjordan.github.io][2]).

3. **Pipeline Adjustment**
   The standard update flow—**Gradient → Momentum → Parameter Update**—is replaced by:
   **Gradient → Momentum → Newton–Schulz Orthogonalization → Parameter Update**.
   This modification enhances training efficiency and stability for 2D parameter matrices ([Medium][3], [kellerjordan.github.io][2]).

4. **Efficient in Practice**
   Despite adding a small computational overhead, Muon delivers significant speedups:

   * Records in NanoGPT speedrunning, improving training time by \~35% ([kellerjordan.github.io][2]).
   * Scales well in large language model training when combined with weight decay and per-parameter RMS adjustments ([arXiv][4]).

5. **Strong Theoretical Foundations**
   Recent research supports Muon’s convergence properties, benefits of weight decay, and optimal batch sizing. Studies confirm tighter theoretical bounds and efficiency across practical scenarios ([arXiv][5]).

---

### Role of Muon in **Kimi K2**

Kimi K2 is Moonshot AI’s **Mixture-of-Experts (MoE) model**, with **1 trillion total parameters** (32B activated) optimized for agentic capabilities. It achieved exceptional performance on knowledge, reasoning, and coding benchmarks thanks in part to training with Muon (and a variant termed **MuonClip**) ([Hugging Face][6], [Poe][7]).

* The **MuonClip optimizer** refers to applying Muon at massive scale while addressing stability challenges intrinsic to such large models ([Hugging Face][6], [Poe][7]).
* The optimizer was key to enabling **zero training instability** over a large token dataset (\~15.5 trillion tokens) and delivering state-of-the-art results ([Hugging Face][6]).

---

### In Summary (No Table, as Requested)

* **Muon** = “MomentUm Orthogonalized by Newton–Schulz”—an optimizer that replaces raw gradient updates with orthogonalized updates, improving learning dynamics for matrix parameters.
* It preserves structure, ensures balanced updates, and remains efficient through iterative orthogonalization instead of costly decompositions.
* **Kimi K2** leverages Muon (and MuonClip) to push the limits of large-scale MoE training, achieving top performance with stability and compute efficiency.

---

Let me know if you’d like a deeper dive—perhaps how Muon compares to AdamW in training trajectories, how MuonClip tweaks the algorithm for MoEs, or how the Newton–Schulz method works in code!

[1]: https://medium.com/%40gauritr01/the-truth-about-kimi-k2-pretraining-muon-optimizer-moe-unpacked-43554527d94a?utm_source=chatgpt.com "The Truth About KIMI K2 Pretraining: Muon Optimizer ..."
[2]: https://kellerjordan.github.io/posts/muon/?utm_source=chatgpt.com "Muon: An optimizer for hidden layers in neural networks"
[3]: https://medium.com/%40jenwei0312/going-beyond-adamw-a-practical-guide-to-the-muon-optimizer-93d90e91dbd3?utm_source=chatgpt.com "Going Beyond AdamW: A Practical Guide to the Muon ..."
[4]: https://arxiv.org/html/2502.16982v1?utm_source=chatgpt.com "Muon is Scalable for LLM Training"
[5]: https://arxiv.org/abs/2507.01598?utm_source=chatgpt.com "Convergence Bound and Critical Batch Size of Muon Optimizer"
[6]: https://huggingface.co/moonshotai/Kimi-K2-Base?utm_source=chatgpt.com "moonshotai/Kimi-K2-Base"
[7]: https://poe.com/Kimi-K2?utm_source=chatgpt.com "Kimi-K2"
