---
audio: false
generated: true
image: false
lang: en
layout: post
title: Triton Compiler Lead Update
translated: false
type: note
---

Let me search for current information on this.**Question:** What is Philippe Tillet (the author of Triton) doing now?

**Answer:**

Philippe Tillet is still at OpenAI as a Member of Technical Staff, leading the Triton compiler effort. He's based in San Diego, with ~13 years of experience in high-performance ML systems, compiler engineering, and GPU kernel optimization. Quick recap of his trajectory and current focus:

**Background.** He started with GPUs in 2011 as a ViennaCL contributor, got his B.S. from Telecom SudParis (2012), M.S. from NCTU Taiwan (2014), and his Ph.D. from Harvard in 2020 with a dissertation on compilers for blocked algorithms on GPUs. He joined OpenAI full-time in 2020 to pursue Triton, a project he started in 2018 out of frustration with writing auto-tuners for matmuls in CUDA.

**Current work — what's notable for you:**

1. **Triton on custom silicon.** This is the most interesting recent signal. He's expanding the Triton Compiler group at OpenAI and hiring engineers to push performance on OpenAI's custom 1P (first-party) accelerators. That confirms OpenAI is targeting Triton as the kernel-authoring layer for their own chips (the Broadcom-partnered hardware), not just NVIDIA — a hardware-portability play that matters a lot if you're thinking about where the MoE/inference-optimization stack is heading.

2. **Blackwell support.** He presented "Blackwell Programming for the Masses with OpenAI Triton" (early 2025), covering the CUDA-C++ vs. XLA/Torch trade-off space and new TMA-style APIs like `tl.make_tensor_descriptor` for tiled GEMM on Blackwell. The talk gets into real hardware constraints — e.g. on H100, `wgmma.sync` doesn't distinguish between QK and PV MMAs, so they can't be pipelined independently (directly relevant to FlashAttention kernel scheduling).

3. **Research output.** He has an ICML 2025 paper (ELMO) with PhD students Nasib Ullah, Jinbin Zhang, and Erik Schultheis on pure 16-bit and 8-bit training for large-output-space models, using fused Triton kernels to cut peak GPU memory from ~40GB to ~6GB on a 3M-item recommendation dataset.

**Why this matters for your trajectory:** The Triton-on-custom-accelerators angle is the thread worth pulling. If you're moving toward inference optimization and GPU compute, Triton is increasingly the portable kernel IR layer — and the fact that OpenAI is betting it onto their own ASICs (the same way AMD already maintains a [ROCm Triton fork](https://github.com/ROCm/triton), which you'd use on your MI300X) means kernel skills written in Triton compound across hardware vendors in a way CUDA doesn't. Worth checking the Triton tutorials directly against your MI300X to see how the ROCm backend codegen differs from the NVIDIA path.

**References:**

- [Philippe Tillet — LinkedIn](https://www.linkedin.com/in/philippe-tillet-809b5536/)
- [Author: Philippe Tillet — NVIDIA Technical Blog](https://developer.nvidia.com/blog/author/philopenai/)
- [Blackwell Programming for the Masses with OpenAI Triton (slides PDF)](https://semianalysis.com/wp-content/uploads/2025/03/Blackwell-Programming-for-the-Masses-With-OpenAI-Triton-Phil-Tillet.pdf)
- [getprog.ai profile — Philippe Tillet](https://getprog.ai/profile/614788)
- [ptillet — GitHub](https://github.com/ptillet)
