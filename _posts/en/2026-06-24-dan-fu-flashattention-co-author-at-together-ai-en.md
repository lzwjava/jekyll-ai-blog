---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Dan Fu: FlashAttention Co-Author at Together AI"
translated: false
type: note
---

**Question:** Who is Dan Fu, the VP of Kernels at Together AI?

**Answer:**

Dan Fu is essentially Tri Dao's close collaborator and the person running Together AI's low-level GPU engineering. Here's the breakdown:

**Who he is:**

Assistant Professor at UCSD (CSE department), leading the SandyResearch Lab, and VP of Kernels at Together AI — building a world-class team focused on low-level performance engineering and GPU kernels.

His research develops efficient algorithms for machine learning, with a focus on solutions that are both theoretically efficient and practically fast on modern hardware.

**His key work:**

- Co-author on **FlashAttention** with Tri Dao (Stanford PhD, same advisor Chris Ré)
- **H3** — a hybrid SSM/attention architecture (only 2 attention layers, ICLR 2023 spotlight, co-authored with Tri Dao)
- **ThunderKittens** — a library for fast GPU kernel development. Within one week of getting access to NVIDIA Blackwell GPUs, his team shipped some of the fastest FP4 and FP8 GEMM kernels available, with up to 2x speedups over cuBLAS on H100s.

**The model he operates under:**

Dan Fu runs a lab at UCSD focused on higher-risk fundamental research, including his personal passion project on FFT algorithms. Together AI co-founder Tri Dao is at Princeton. The model is symbiotic: de-risk ideas in academia, productionize them at Together AI. PhD students join the company, Together AI interns work on longer-term research in academic labs.

So the Together AI kernels org is essentially a Stanford/Princeton systems mafia productionizing their own research — FlashAttention, Mamba, H3, ThunderKittens — all flowing from academia directly into the inference stack. Very similar to how DeepSeek operates: research-first, implementation depth as the moat.

**References:**

- [Dan Fu's homepage - danfu.org](https://danfu.org/)
- [Inside the Together AI kernels team](https://www.together.ai/blog/inside-the-together-ai-kernels-team)
