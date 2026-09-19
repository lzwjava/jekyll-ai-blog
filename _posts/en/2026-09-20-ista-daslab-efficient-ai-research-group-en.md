---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ISTA-DASLab: Efficient AI Research Group"
translated: false
type: note
---

**Question:** What is ISTA-DASLab on Hugging Face, and what do they do?

**Answer:**

**ISTA-DASLab** stands for the **IST Austria Distributed Algorithms and Systems Lab** (Deep Algorithms and Systems Lab), a research group based at the [Institute of Science and Technology Austria (ISTA)](https://ist.ac.at).

**Leadership:** The group is led by Professor **Dan Alistarh**, who has been a professor at ISTA since 2022. His background spans a postdoc at MIT, research at Microsoft Research Cambridge, and a PhD from EPFL.

**Mission:** The Alistarh group works to remove barriers to the democratization of AI by creating training and inference algorithms that are significantly more efficient than conventional ones. Their core concern is that the computation required to train and deploy state-of-the-art AI models has been rising exponentially, potentially hindering innovation and leading to inequalities in expertise and economic benefit.

**Research Focus:** Their current projects span efficient training and inference for massive AI models, large-scale distributed machine learning, adaptive concurrent data structures, and fundamental limits of distributed computation. They develop new algorithms for learning over compressed representations — such as sparse or quantized models — as well as efficient systems implementations that can leverage compression gains in practice.

**What They Publish on Hugging Face:** The lab hosts 164 models and 2 datasets on Hugging Face, with 19 team members contributing. Their most prominent recent work includes:
- **GSQ** (Gumbel-Softmax quantization) — highly accurate low-precision scalar quantization for LLMs
- **GSQ-RCO-GGUF** — non-uniform GGUF quantizations using per-tensor mixed precision in standard GGUF format
- Quantized versions of popular large models like Qwen3, Kimi-K2, and Llama 3.1 (at 2-bit and 3-bit precision)

In short, DASLab is a leading academic research group pushing the frontier of **LLM compression and efficient inference**, making large models smaller and faster without sacrificing quality.

**References:**
- [ISTA-DASLab on Hugging Face](https://huggingface.co/ISTA-DASLab)
- [Alistarh Group — ISTA](https://ist.ac.at/en/research/alistarh-group/)