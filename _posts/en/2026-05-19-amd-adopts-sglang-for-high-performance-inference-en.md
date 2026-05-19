---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Adopts SGLang for High-Performance Inference
translated: false
type: note
---

Question: What is SGLang, and why does it appear on the AMD Developer Cloud?

Answer:

## What is SGLang?

**SGLang** (short for **Structured Generation Language**) is an open-source, high-performance serving framework for large language models (LLMs) and multimodal models. Developed by UC Berkeley and hosted by the LMSYS organization, it combines a Python-embedded frontend language with a highly optimized backend runtime.

---

## Core Architecture

SGLang is built on two fundamental pillars:

**1. Backend — RadixAttention**

Unlike traditional inference approaches that waste 60–80% of GPU memory on KV cache allocation, SGLang introduces **RadixAttention** — a radix tree-based prefix caching system that automatically discovers and reuses shared prefixes across requests. This dramatically improves memory efficiency and throughput.

**2. Frontend — Structured Programming Language (DSL)**

The flexible frontend language provides intuitive and powerful LLM programming interfaces, supporting chainable generation calls, advanced prompt engineering, complex control flow, multimodal input, parallel execution, and external system interaction.

---

## Key Features

SGLang's fast runtime provides efficient serving with RadixAttention for prefix caching, a zero-overhead CPU scheduler, prefill-decode disaggregation, speculative decoding, continuous batching, paged attention, tensor/pipeline/expert/data parallelism, structured outputs, chunked prefill, quantization (FP4/FP8/INT4/AWQ/GPTQ), and multi-LoRA batching.

It also has extensive hardware support, running on NVIDIA GPUs (GB200/B300/H100/A100), AMD GPUs (MI355/MI300), Intel Xeon CPUs, Google TPUs, Ascend NPUs, and more.

---

## Model Support

SGLang supports mainstream generative models such as Llama, Gemma, Mistral, Qwen, DeepSeek, and LLaVA, as well as embedding models and reward models, with a simple mechanism for extending to new models.

---

## Industry Scale & Adoption

SGLang has been deployed at large scale, generating trillions of tokens in production each day. It is trusted by a wide range of leading enterprises and institutions, including xAI, AMD, NVIDIA, Intel, LinkedIn, Cursor, Oracle Cloud, Google Cloud, Microsoft Azure, AWS, Stanford, UC Berkeley, and Tsinghua University. It is currently running on over 400,000 GPUs worldwide.

---

## Why Does It Appear on AMD Developer Cloud?

AMD has deeply integrated SGLang as a **first-class inference framework** on their platform:

- The AMD Developer Cloud offers **Quick Start Packages** including SGLang — pre-built Docker containers where Jupyter is launched inside the container to give users direct access to the SGLang AI/ML software stack, with example notebooks included to help you get started quickly.

- AMD's ROCm 7 introduces distributed inference in collaboration with the open-source ecosystem including SGLang, vLLM, and llm-d. AMD embraces an open strategy, co-developing shared interfaces and primitives to enable efficient distributed inference on AMD platforms.

- AMD provides SGLang-based Docker containers optimized for the MI300X GPU, which developers can use to serve models like Qwen 3.5 with minimal setup on AMD Developer Cloud droplets.

- AMD Developer Cloud gives developers raw access to AMD Instinct GPUs to run inference, training, fine-tuning, or any custom workload using frameworks they already know — including vLLM, SGLang, PyTorch, and more.

---

## Performance Comparison

SGLang delivers 29% higher throughput on H100 GPUs compared to vLLM (16,215 vs 12,553 tokens/second) with lower latency (79ms vs 103ms time-to-first-token). Organizations deploying DeepSeek R1 or V3 achieve 2–3x better throughput on SGLang compared to generic inference engines.

---

## Summary Table

| Aspect | Detail |
|---|---|
| **Full Name** | Structured Generation Language |
| **Origin** | UC Berkeley / LMSYS |
| **Primary Use** | LLM & multimodal model inference serving |
| **Key Innovation** | RadixAttention (prefix caching) |
| **Hardware** | NVIDIA, AMD, Intel, TPU, and more |
| **AMD Integration** | Pre-built Docker Quick Start on AMD Developer Cloud |
| **License** | Open Source |

References:

- [SGLang GitHub Repository](https://github.com/sgl-project/sglang)
- [SGLang Official Documentation](https://sgl-project.github.io/)
- [SGLang on AMD Instinct GPUs — ROCm Blogs](https://rocm.blogs.amd.com/artificial-intelligence/sglang/README.html)
- [How to Get Started on the AMD Developer Cloud](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD ROCm AI Developer Hub](https://www.amd.com/en/developer/resources/rocm-hub/dev-ai.html)
- [SGLang Complete Guide — Inference.net](https://inference.net/content/sglang-complete-guide/)