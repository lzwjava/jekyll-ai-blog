---
audio: false
generated: true
image: false
lang: en
layout: post
title: Profile of AI Researcher Lvmin Zhang
translated: false
type: note
---

**Question:** Who is Lvmin Zhang (lllyasviel)?

**Answer:**

Lvmin Zhang is one of the most impactful applied AI researchers in the generative image/video space right now. Here's the quick profile:

**Identity:**
- PhD candidate in CS at Stanford, advised by Maneesh Agrawala. Previously a research assistant at CUHK under Tien-Tsin Wong. B.Eng. from Soochow University (2021).

**Why you've definitely used his work:**

- **ControlNet** — ICCV 2023 Best Paper (Marr Prize). The architecture that adds spatial conditioning (edges, depth, pose) to frozen text-to-image diffusion models via trainable copy + zero convolutions. This is the paper that made Stable Diffusion controllable and is used by essentially every image generation pipeline today.

- **FramePack** — NeurIPS 2025 Spotlight (top 3%). A next-frame video prediction architecture that compresses input frames by importance to pack longer contexts into fixed length, with drift prevention to reduce error accumulation.

- **IC-Light** — ICLR 2025 Oral (top 1%). Diffusion-based relighting that imposes consistent light transport principles for scalable in-the-wild training.

- **LayerDiffuse** — SIGGRAPH 2024. Transparent image generation with latent diffusion by encoding alpha channel as a latent offset ("latent transparency").

**Background that makes him unusual:**
He worked with digital painting artists for years and funded Style2Paints Research. Before college he was a game developer and pro YGO player who built YGOPro2. He also has anonymous activities in cracking communities (mainly Denuvo and VMs).

**The pattern:** He consistently finds elegant architectural ideas — ControlNet's zero convolutions, FramePack's importance-based compression — that solve hard practical problems in generative models. He ships real code, runs it in community (his GitHub `lllyasviel` is extremely active), and publishes top-venue papers simultaneously. Very much a builder-researcher hybrid in the Karpathy mold, but focused on controllable diffusion and video generation.

His recent 2026 output (2 ICML, 1 SIGGRAPH, 1 CVPR) shows he's not slowing down.

**References:**

- [Lvmin Zhang's homepage](https://lllyasviel.github.io/lvmin_zhang/)
- [ControlNet paper](https://arxiv.org/abs/2302.05543)
- [FramePack](https://lllyasviel.github.io/frame_pack_gitpage/)
- [IC-Light code](https://github.com/lllyasviel/IC-Light)