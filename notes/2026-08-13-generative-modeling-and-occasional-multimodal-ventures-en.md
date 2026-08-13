---
audio: false
generated: true
image: false
lang: en
layout: post
title: Generative Modeling and Occasional Multimodal Ventures
translated: false
type: note
---

Question: What has Kaiming He (MIT/DeepMind) been working on recently, especially the multimodal stuff?

Answer: His lab's been on a generative modeling tear since mid-2025 — mostly diffusion/flow-matching theory and image generation, not classic multimodal (vision-language) work. The recent line:

**Generative modeling core (his main focus)**
- "Mean Flows for One-step Generative Modeling" (NeurIPS 2025 Oral, May 2025) — one-step generative models via "average velocity" instead of instantaneous velocity in flow matching. This is the seed paper for a whole family that follows.
- "Improved Mean Flows: On the Challenges of Fastforward Generative Models" (CVPR 2026 Spotlight) and "One-step Latent-free Image Generation with Pixel Mean Flows" (Jan 2026) — pushing mean-flow to pixel space, killing the VAE latent dependency.
- "Bidirectional Normalizing Flow: From Data to Noise and Back" (CVPR 2026 Spotlight)
- "Back to Basics: Let Denoising Generative Models Denoise" (CVPR 2026) — with Tianhong Li, revisiting whether you actually need the fancy tricks in diffusion.
- "Is Noise Conditioning Necessary for Denoising Generative Models?" (ICML 2025)
- "Diffuse and Disperse: Image Generation with Representation Regularization" (June 2025)
- "Fractal Generative Models" (TMLR 2025), "Autoregressive Image Generation without Vector Quantization" (NeurIPS 2024 Spotlight) — his MAR line, continuous-token AR image gen, no VQ codebook.

**Closest thing to "multimodal"**
- "Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens" (ICLR 2025) — text-to-image AR scaling, with Yonglong Tian.
- "Image Generators are Generalist Vision Learners" (Google DeepMind collab, Apr 2026) — this is the real multimodal-adjacent one. Big author list (Barron, Saining Xie, Soricut, etc.), argues image generators themselves learn generalist visual representations. Project page: vision-banana.github.io.
- "ARC Is a Vision Problem!" (CVPR 2026) — reframes ARC-AGI as a vision task, with Jacob Andreas/Yoon Kim (language folks) — interesting bridge between reasoning benchmarks and vision.
- "ELF: Embedded Language Flows" (May 2026) — his most recent, with Yoon Kim and Jacob Andreas (MIT NLP). This is probably the closest to actual language+generation fusion — flow matching applied in an embedded-language setting.

**Non-generative side stuff**
- "GeoPT: Scaling Physics Simulation via Lifted Geometric Pre-Training" (Feb 2026) — physics sim pretraining, unrelated to vision-language.
- "Transformers without Normalization" (CVPR 2025, w/ Yann LeCun) — dynamic tanh instead of norm layers.
- "Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers" (NeurIPS 2024) — robotics/vision, if you count that as multimodal.

Bottom line: he's not chasing CLIP/LLaVA-style VLM work. His post-MIT trajectory (2024–2026) is almost entirely about simplifying and unifying generative modeling theory — mean flows, denoising without tricks, AR without VQ — with the DeepMind "generalist vision learner" paper and the new ELF paper being the two that actually touch language/multimodal territory.

References:
- [Kaiming He — Publications](https://people.csail.mit.edu/kaiming/publications.html)
- [Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447)
- [Image Generators are Generalist Vision Learners](https://arxiv.org/abs/2604.20329)
- [ELF: Embedded Language Flows](https://arxiv.org/abs/2605.10938)
- [ARC Is a Vision Problem!](https://arxiv.org/abs/2511.14761)