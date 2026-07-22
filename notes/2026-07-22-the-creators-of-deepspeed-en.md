---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Creators of DeepSpeed
translated: false
type: note
---

Question: Who invented DeepSpeed?

Answer:

DeepSpeed was **created by the Microsoft Research AI at Scale team**, not by a single individual. It was open-sourced in **May 2020** as a PyTorch optimization library for training and serving very large neural networks. ([Wikipedia][1])

The key people behind the original DeepSpeed project include:

* Jeff Rasley
* Samyam Rajbhandari
* Olatunji Ruwase
* Yuxiong He

These four authors wrote the original **ZeRO (Zero Redundancy Optimizer)** paper, which is the core innovation that made DeepSpeed famous. ZeRO partitions optimizer states, gradients, and parameters across GPUs, dramatically reducing memory usage while preserving the same model semantics. Most of DeepSpeed's later features (ZeRO-Offload, ZeRO-Infinity, Ulysses, MoE support, etc.) build on this foundation. ([Microsoft][2])

### Leadership

The researcher most closely associated with the overall vision of DeepSpeed is **Yuxiong He**. He leads the Microsoft Research AI at Scale effort and is a senior author on many of the major DeepSpeed papers, including:

* ZeRO
* ZeRO-Offload
* ZeRO-Infinity
* DeepSpeed-MoE
* DeepSpeed Inference
* ZeRO++

### Timeline

| Year      | Milestone                                                                         |
| --------- | --------------------------------------------------------------------------------- |
| 2020      | DeepSpeed open sourced by Microsoft Research                                      |
| 2020      | ZeRO optimizer introduced                                                         |
| 2021      | ZeRO-Offload and ZeRO-Infinity                                                    |
| 2022      | DeepSpeed Inference and DeepSpeed-MoE                                             |
| 2023–2024 | Ulysses, ZeRO++, Universal Checkpointing, Domino, and other scaling optimizations |

Today, DeepSpeed remains one of the three dominant distributed training frameworks for PyTorch, alongside:

* PyTorch Distributed
* NVIDIA Megatron-LM
* DeepSpeed

References:

* [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed?utm_source=chatgpt.com)
* [Microsoft Research DeepSpeed project](https://www.microsoft.com/en-us/research/project/deepspeed/people/?utm_source=chatgpt.com)
* ([Microsoft][3])

[1]: https://en.wikipedia.org/wiki/DeepSpeed?utm_source=chatgpt.com "DeepSpeed"
[2]: https://www.microsoft.com/en-us/research/project/deepspeed/publications/?utm_source=chatgpt.com "DeepSpeed - Microsoft Research: Publications"
[3]: https://www.microsoft.com/en-us/research/project/deepspeed/people/?utm_source=chatgpt.com "DeepSpeed - Microsoft Research: People"
