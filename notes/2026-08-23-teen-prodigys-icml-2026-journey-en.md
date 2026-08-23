---
audio: false
generated: true
image: false
lang: en
layout: post
title: Teen Prodigy's ICML 2026 Journey
translated: false
type: note
---

**Question:** What is the story behind these three links — the ICML 2026 poster, the podcast episode, and the arXiv paper?

**Answer:**

These three links all tell the same remarkable story: a 17-year-old high school student named **Jonathan Su (苏庭灏)**, born in 2009, who independently conducted pretraining research and got his paper accepted at ICML 2026 — one of the most prestigious machine learning conferences in the world.

---

### 1. The Paper — *ExoFormer* (arXiv + ICML)

The paper is titled **"Attention Projection Mixing with Exogenous Anchors"** and was accepted as a poster at **ICML 2026** (presented July 7, 2026).

The core problem it addresses: cross-layer reuse of early attention projections can improve optimization and data efficiency, but it creates a structural conflict — the first layer must simultaneously act as a stable, reusable anchor for all deeper layers and as an effective computational block.

Jonathan's solution is **ExoFormer**: instead of using the first layer as the anchor, ExoFormer learns *exogenous* anchor projections outside the sequential layer stack — dedicated weight matrices that project from the input embeddings and are blended into every subsequent layer via learnable, normalized mixing coefficients.

The results are significant: the dynamic ExoFormer variant achieves approximately 1.5 downstream accuracy points while matching validation loss using about 1.5× fewer tokens than Gated Attention — a meaningful gain in data efficiency.

He explains this via the **Offloading Hypothesis**: external anchors preserve essential token identity, allowing the sequential layers to specialize exclusively in feature transformation rather than also having to maintain identity signals.

Notably, the author's affiliation is listed simply as "Independent Researcher," with a correspondence email at a high school domain (gsis.edu.hk).

---

### 2. The Podcast — *Xiaoyuzhou Episode 151*

The episode is titled **"The 17-year-old whose paper was accepted by ICML 2026: I bet I'm happy! Happy! Happy!"** — an interview on the podcast *张小珺Jùn｜商业访谈录* (Zhang Xiaojun Business Interviews), a Chinese deep-dive interview show.

The host Zhang Xiaojun notes this is the first time she opened up a high schooler's AI world on the show, having previously interviewed many mature AI researchers.

In the conversation, Jonathan talks about:

- How he independently conducted pretraining research, describing pretraining as "a bit magical"
- Losing ¥1,500 on a mistake during experiments, which made him very upset and brought him to tears
- His view that AI has made classmates feel a loss of meaning — "no matter what you do, AI might do it better" — though he worked through this emotionally
- His philosophy: happiness is the foundation of humanity — since AI's trajectory is uncontrollable, don't overthink it; just talk more with the people you like
- After returning from ICML in Korea, he immediately went to a rural area to volunteer as a teaching aide — a completely different, slower world of catching insects and playing Werewolf

---

### The Big Picture

Together, these three sources form a portrait of an extraordinary teenager: a high school student who taught himself ML, ran GPU experiments on his own (reportedly spending ~¥30,000 total on compute, supported by his parents), published a technically solid Transformer architecture paper accepted at a top venue, attended ICML in Seoul, and then went off to teach rural children — all before turning 18. The contrast between the cutting-edge research and his grounded, cheerful personality is what makes the story so compelling.

---

**References:**

- [ICML 2026 Poster — ExoFormer](https://icml.cc/virtual/2026/poster/61175)
- [Podcast Episode — Xiaoyuzhou](https://xiaoyuzhoufm.com/episode/6a8472b95aeb2a5712e8de78)
- [arXiv Paper — 2601.08131v4](https://arxiv.org/html/2601.08131v4)
- [GitHub Code — ExoFormer](https://github.com/jon123boss/ExoFormer)
