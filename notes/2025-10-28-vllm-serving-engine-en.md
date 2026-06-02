---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: 'vLLM: Efficient LLM Serving Engine'
translated: false
type: note
---

### Invention of vLLM

vLLM (short for "virtual LLM") is an open-source library for high-throughput and memory-efficient inference and serving of large language models (LLMs). It was invented in early 2023 by researchers at the Sky Computing Lab in UC Berkeley's RISELab. The project began as a specialized inference engine optimized for NVIDIA A100 GPUs and a limited set of models, addressing key challenges in LLM serving like memory fragmentation and low throughput.

Key early milestones:
- **Mid-April 2023**: First public integration with FastChat, powering LMSYS's Vicuna and Chatbot Arena demos.
- **June 2023**: Official release and public GitHub repository launch.
- **September 12, 2023**: Foundational research paper, "Efficient Memory Management for Large Language Model Serving with PagedAttention," published on arXiv, introducing the core PagedAttention mechanism that enables continuous batching and near-zero KV cache waste.

The GitHub repository (vllm-project/vllm) was created around May–June 2023, aligning with the initial development push.

### Rise in Popularity

vLLM started gaining significant traction in 2024, evolving from a niche research tool into the de facto standard for open-source LLM serving. Its popularity exploded due to rapid feature additions (e.g., quantization, speculative decoding, multi-modal support), hardware expansions (NVIDIA, AMD, Google TPUs, etc.), and production adoptions by companies like Amazon (powering Rufus during Prime Day 2024) and LinkedIn.

Key growth indicators from 2024:
- **GitHub Stars**: Grew 2.3x from 14,000 (early 2024) to 32,600 (end of 2024).
- **Monthly Downloads**: Surged 4.5x from 6,000 to 27,000.
- **GPU Usage**: Increased ~10x in the second half of 2024.
- **Community**: Contributors rose 3.9x to 740, with bi-weekly office hours and partnerships (e.g., NVIDIA, IBM, AWS).

By mid-2024, it had ~20,000 stars and was frequently discussed in AI communities for outperforming alternatives in throughput. Momentum continued into 2025:
- Joined the PyTorch ecosystem in December 2024.
- Entered LF AI & Data incubation in October 2024.
- Reached 50,000 stars by June 2025.

Today (October 2025), it has over 55,000 stars and supports nearly 100 model architectures, making it a cornerstone for scalable AI deployments.

[arXiv Paper on PagedAttention](https://arxiv.org/abs/2309.06180)
[vLLM GitHub Repository](https://github.com/vllm-project/vllm)
[vLLM 2024 Retrospective Blog](https://blog.vllm.ai/2025/01/10/vllm-2024-wrapped-2025-vision.html)
[PyTorch Integration Announcement](https://pytorch.org/blog/vllm-joins-pytorch/)
