---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: MuonClip Optimizer for Kimi K2
translated: false
type: note
---

### Overview of Muon Optimizer

The Muon Optimizer is a cutting-edge optimization algorithm mentioned by Zhiling Yang (also known as Yang Zhilin), the founder and CEO of Moonshot AI, in the context of developing their large language model, Kimi K2[1][2][3]. It is a second-order-inspired optimizer that uses high-rank updates to better adapt to the geometry of the loss surface during model training[2]. However, it has issues with training instability, which Moonshot AI addressed by creating an enhanced version called MuonClip[1][4].

### Key Characteristics
- **Efficiency and Design**: Muon aims for token efficiency, meaning it processes fewer tokens than traditional optimizers like AdamW while achieving comparable or better performance. It draws inspiration from second-order methods (e.g., Newton's method) but adapts to large-scale deep learning scenarios[2][3].
- **Stability Issues**: The base Muon optimizer can cause instability during long training runs, such as loss spikes, because it's prone to divergence in certain conditions[2][1].
- **MuonClip Enhancement**: Moonshot AI introduced MuonClip by integrating Muon with a "QK-Clip" technique, which clips query-key interactions in the attention mechanism to prevent instability. This allowed stable, spike-free training of Kimi K2 on 15.5 trillion tokens[1][4][5].

### Application in Kimi K2
MuonClip was pivotal in pre-training Kimi K2, a 1 trillion total parameter Mixture-of-Experts (32 billion activated parameters) model. The optimizer enabled Moonshot AI to achieve state-of-the-art results in benchmarks like Tau2-Bench (66.1), ACEBench (76.5), and SWE-Bench Verified (65.8) without extended thinking[4][6]. Yang highlighted this as a breakthrough for open-source AI development, emphasizing its role in making large-scale training more efficient and stable[7][8].

For technical details, refer to the Kimi K2 paper on arXiv[1][4]. Zhiling Yang discussed this in interviews and announcements around the model's release in July 2025[2][7].

Citations:
[1] https://arxiv.org/pdf/2507.20534?
[2] https://artificialintelligencemadesimple.substack.com/p/kimi-k2-is-the-most-important-model?utm_source=post-email-title&publication_id=1315074&post_id=169438943&utm_campaign=email-post-title&isFreemail=true&r=36rt3&triedRedirect=true&utm_medium=email
[3] https://composio.dev/blog/notes-on-kimi-k2
[4] https://arxiv.org/abs/2507.20534
[5] https://www.hpcwire.com/2025/07/16/chinas-moonshot-ai-releases-trillion-parameter-model-kimi-k2/
[6] https://intuitionlabs.ai/pdfs/analysis-of-the-kimi-k2-open-weight-language-model.pdf
[7] https://www.chinatalk.media/p/kimi-k2-the-open-source-way
[8] https://github.com/MoonshotAI/Kimi-K2
