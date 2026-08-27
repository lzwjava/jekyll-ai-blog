---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FreeToken: Edge MoE Serving System"
translated: false
type: note
---

**Question:** What is the paper at this arXiv link?

**Answer:**

This is a research paper titled **FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution**, published on arXiv on August 17, 2026, by a team from UC Berkeley (including Ion Stoica, Matei Zaharia, and Song Han, among others).

**What it's about:**

FreeToken is an edge-native serving system for Mixture-of-Experts (MoE) large language models. Rather than treating a personal machine as just a "small GPU," it treats it as a unified, elastic inference platform.

**The core problem it solves:**

Frontier open-weight AI models are increasingly available, but running them has largely still assumed datacenter-scale infrastructure. FreeToken brings that capability to personal hardware.

**Key technical contributions:**

FreeToken co-designs the full serving stack — covering model layout and loading, expert residency, CPU-GPU execution, agentic state reuse, and runtime memory management — around two key realities of local AI: agent workloads continuously shift their execution patterns, and edge hardware exposes heterogeneous resources that vary machine to machine. Instead of committing to a fixed offloading strategy, FreeToken dynamically maps computation onto whatever resources are actually available.

**Impressive results:**

It supports over 20 MoE models and real coding/tool-using agents, on hardware ranging from an 8GB laptop GPU to a single workstation GPU — enabling a 35B model on a laptop, a 284B model on a gaming desktop, and even the 753B GLM-5.2 on a single workstation GPU.

The system is released publicly at **flashml.ai**.

---

**References:**

- [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](https://arxiv.org/abs/2608.16157)
