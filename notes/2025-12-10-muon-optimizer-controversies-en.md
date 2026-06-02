---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Muon Optimizer Controversies and Criticisms
translated: false
type: note
---

Question: What are some unpopular opinions about the Muon optimizer?

Answer:

The Muon optimizer (MomentUm Orthogonalized by Newton-Schulz) is a relatively new neural network optimization technique introduced in late 2024, primarily for hidden layers in models like transformers. It applies Newton-Schulz iterations to orthogonalize momentum-based updates, aiming for more efficient training with lower computational overhead (under 1% FLOPs extra) and better sample efficiency than AdamW. While it's gained hype for setting speed records in tasks like CIFAR-10 and NanoGPT training, and powering models like Moonlight (a 3B/16B MoE LLM), it's not without controversy. Below are some unpopular opinions drawn from discussions in ML communities (e.g., Reddit's r/MachineLearning and X posts). These views challenge the enthusiasm, often emphasizing practical limitations over theoretical gains.

### Unpopular Opinions on Muon:
- **The speedup is overhyped and mostly due to other tweaks, not Muon itself**: In speedrun benchmarks (e.g., training a 120M GPT model in 3 minutes), Muon contributes only about 10% of the total speedup— the bulk comes from architecture changes, data efficiency, or implementation optimizations. When baselines like AdamW are properly tuned (e.g., with optimal learning rates), Muon offers just a modest 10% edge, not the revolutionary 2x efficiency claimed in papers.

- **It's not truly second-order or geometrically superior— that's just math-washing for hype**: Despite claims of "steepest descent under spectral norm" or manifold optimization, Muon is fundamentally a first-order method (no second-order stats like Hessians). The fancy geometric framing (orthogonal updates preserving "energy" in matrix space) is seen as unnecessary intimidation tactics to impress VCs or non-experts, with no real superiority over well-tuned Adam variants. One researcher called it "irrelevant" and promised a PSA debunking the math.

- **Switching to Muon mid-training (e.g., for fine-tuning) hurts more than it helps**: Models pretrained with AdamW don't transfer well to Muon due to differing inductive biases—Muon's orthogonal constraints create "different minds" or structures that clash, leading to mixed or worse fine-tuning results (e.g., in SFT tasks). Sticking with AdamW throughout is simpler and more reliable, especially for dense vs. MoE architectures.

- **AdamW is actually the underrated workhorse—Muon is the fleeting "optimizer-of-the-month"**: If roles were reversed (Muon as the 2015 default and AdamW arriving in 2025), labs would flock to AdamW for its "free scaling" across 1M-GPU clusters, no extra comms/compute, and plug-and-play reliability on weird architectures. Muon's niche (e.g., 2D hidden weights only) makes it less universal, slowing research by complicating comparisons.

- **It produces "minimalist" solutions that might be too restrictive**: By orthogonalizing updates (effectively "restricting to spheres" in parameter space), Muon favors compact, esoteric knowledge absorption (e.g., why Kimi K2 "knows so much" despite being smaller than GPT-4). But this could limit creativity or broad generalization, making models overly precise in narrow domains at the cost of robustness—essentially trading expressiveness for efficiency.

- **Overhead and instability make it impractical at frontier scales**: Early versions caused exploding logits in large LLMs, requiring hacks like MuonClip. Even with fixes, it's dead at massive scales (e.g., >10% better only in small models), and the Newton-Schulz steps add subtle bugs or tuning hassles. Adam remains "really good if you tune your baseline well," per rare rigorous ablation studies.

Overall, these opinions highlight a divide: Muon shines in controlled speedruns but struggles with the messiness of real-world scaling and integration. Enthusiasts praise its theoretical elegance, but skeptics see it as evolutionary, not revolutionary—echoing debates around past optimizers like Lion or Shampoo.

References:
- [Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/)
- [Muon is Scalable for LLM Training (arXiv)](https://arxiv.org/abs/2502.16982)
- [r/MachineLearning: [P] Understanding Muon](https://www.reddit.com/r/MachineLearning/comments/1m2y23l/p_understanding_muon_a_revolutionary_neural/)
- [r/LocalLLaMA: Kimi.ai released Moonlight](https://www.reddit.com/r/LocalLLaMA/comments/1ivrprb/kimiai_released_moonlight_a_3b16b_moe_model/)
- [r/MachineLearning: [R] Muon is Scalable](https://www.reddit.com/r/MachineLearning/comments/1ixzj26/r_muon_is_scalable_for_llm_training/)
- [X Post: Jason Lee on Muon not being second-order](https://x.com/jasondeanlee/status/1986102152574767308)
- [X Post: Simo Ryu on Adam vs. Muon](https://x.com/cloneofsimo/status/1963670853574705413)
- [X Post: James MMatrix on lab adoption](https://x.com/JamesWhate89993/status/1998190303669342530)
