---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yifan Zhou's Diffusion Blog
translated: false
type: note
---

**Question:** Introduce the blog at https://zhouyifan.net and its author.

**Answer:**

## The Author: Yifan Zhou (周弈帆)

Yifan Zhou is a Ph.D. student at the School of Computer Science and Engineering, Nanyang Technological University (Singapore), a member of NTU MMLab (affiliated with NTU S-Lab), supervised by Professor Xingang Pan. Before the Ph.D., he worked as a research engineer at NTU S-Lab and at Shanghai AI Lab, and got his bachelor's degree in CS at Beijing Institute of Technology. His research focus is image and video generation — diffusion models, DiT architectures, and attention efficiency.

Career highlights worth knowing:

- At Shanghai AI Lab (2021–2022), he was a core developer and maintainer of MMDeploy, the open-source model deployment library in the OpenMMLab ecosystem.
- Competitive programming background: 1 ACM-ICPC Gold Medal, 5 Silver Medals, plus 2 CCPC Silver Medals. GitHub handle: SingleZombie.
- Publications include Rerender A Video (SIGGRAPH Asia 2023), FRESCO and DiffMorpher (both CVPR 2024), Alias-free Latent Diffusion Models (CVPR 2025 Oral), and his latest first-author work, Trainable Log-linear Sparse Attention for Efficient Diffusion Transformers — accepted as a CVPR 2026 Highlight.
- His stated long-term ambition is unusual for an ML researcher: he openly says game design is his true dream, and that he's pursuing AI research success first to fund an eventual "AI + game design" venture. He plans research, dev tooling, and game products around AI-driven gameplay design, in a solo-founder-ish working mode after finishing his academic career.

## The Blog (周弈帆的博客)

Hexo-powered, running since ~2019, with 158 posts across 21 categories, mostly in Chinese (an English mirror exists at /blog-en). This is one of the best Chinese-language deep-dive blogs on diffusion models and attention mechanisms — directly relevant to your nanoGPT/MoE/sparse-attention track. The signature style: paper walkthroughs that start from first principles, with math, complexity analysis, and honest critique sections (he critiques his own papers' weaknesses publicly, which is rare).

Representative recent content:

- **LLSA (his own paper)** — a first-person explainer of Log-linear Sparse Attention, which reduces sparse attention from O(N²) to O(N log N) via hierarchical Top-K selection, KV enrichment, and KV reweighting, with an open-sourced high-performance Triton implementation (github.com/SingleZombie/LLSA) — validated on VAE-free, patchification-free pixel DiT at up to 512×512 pixel sequences. This competes with MoBA (Kimi) and NSA (DeepSeek), which don't actually reduce asymptotic complexity — their runtime still grows O(N²).
- **Pixel DiT series** — comparative analysis of JiT (Kaiming He's team), DiP, DeCo, and PixelDiT, dissecting why large-patch DiTs are hard to train and how pixel-level decoders replace unpatchify.
- **FlashAttention tutorial** — "FlashAttention explained without needing CUDA knowledge", plus his Triton GPU programming notes (sparse index transposition for efficient backward passes, Q-major → K-major index conversion).

He's also a personality: at CVPR 2026 in Denver, alongside his poster session he cosplayed Togawa Sakiko from BanG Dream! — admittedly as a publicity stunt, inspired by the Frieren coser at CVPR 2024. His self-intro claims, tongue-in-cheek, that his coding ability is "king-tier among all humans."

**Why it's relevant to you:** his LLSA Triton kernels are exactly the kind of attention-internals + GPU-programming material you're building toward (NSA/MoBA-adjacent, open source, drop-in attention replacement). The FlashAttention and sparse-attention posts pair well with your nanoGPT/DeepSeek-v4 MoE study — and his code runs fine on a single H200-class budget, i.e., the MI300X territory you already rent.

**References:**

- [周弈帆的博客 (homepage)](https://zhouyifan.net)
- [About / CV page](https://zhouyifan.net/about/)
- [LLSA paper explainer](https://zhouyifan.net/2025/12/18/20251211-llsa-1/)
- [LLSA on arXiv](https://arxiv.org/abs/2512.16615)
- [LLSA GitHub](https://github.com/SingleZombie/LLSA)
