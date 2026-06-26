---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AICAS 2026: Silicon-Model Boundary Conference"
translated: false
type: note
---

I'll fetch the page to give you accurate details.Question: Give me an intro to the IEEE AICAS 2026 conference (<https://2026.ieee-aicas.org>).

Answer:

**AICAS** is the **IEEE International Conference on Artificial Intelligence Circuits and Systems** — the flagship AI-hardware conference of the IEEE Circuits and Systems Society (CASS). The 2026 edition is the **8th**, held **September 16–18, 2026 in Ha Long Bay, Vietnam**, organized jointly by IEEE CASS Vietnam and China chapters.

**The angle that matters for you:** This is *not* an algorithms/ML-theory venue like NeurIPS or ICML. AICAS sits at the **silicon ↔ model boundary** — it's where the people building the chips your models run on publish. If your trajectory is model training + inference optimization + CUDA/GPU compute, this is the conference that explains *why* the hardware behaves the way it does.

The topics map directly onto your stated interests:

- **In-memory computing / Compute-in-Memory (CIM)** — moving MAC operations into the memory array to kill the von Neumann bottleneck. Directly relevant to why KV-cache bandwidth dominates LLM inference.
- **Circuits/architecture for neural-network language modeling** — i.e., transformer accelerators, attention-specific datapaths, quantization-aware silicon.
- **HW/SW co-design and design automation for AI** — the LoRA/quantization/sparsity tricks you use, but pushed down to the hardware contract.
- **Neuromorphic / bioinspired** — spiking nets, event-driven compute (further from your current LLM focus).
- **Inference for edge → cloud**, hardware security, privacy-preserving ML.

**Logistics / current state (as of the page today):**

- Full-paper submission **closed April 5, 2026**. You can't submit a regular paper anymore.
- **Acceptance notifications go out ~June 28, 2026** (slipped twice from June 18 → 25 → 28).
- **Live Demo papers still open — deadline June 30, 2026** (via EDAS, `edas.info/N34921`). This is the one open door if you wanted to present something.
- Camera-ready + advance registration: **July 10, 2026**.
- Format: max 5 pages (4 technical + 1 references). Proceedings go to **IEEE Xplore**; selected papers get recommended to **TCAS-AI** or **TVLSI** special sections.
- Diamond sponsors: **T-Head** (Alibaba's RISC-V/chip arm) and **RingConn**; Platinum: **Cadence** (EDA). The sponsor list tells you the room is RISC-V + EDA + edge-AI hardware people.

**Honest fit assessment for your goals:** Your self-described frontier is *model training, agent architectures, LLM internals, AI-native tooling* — that's the **software/algorithm** side. AICAS is the **hardware/circuits** side of the same coin. It's adjacent and genuinely useful for the *inference-optimization and CUDA/GPU* slice of your roadmap, but it won't teach you MoE routing or GRPO. If you want to go deeper on the silicon that makes your 2B-token/year habit possible, this is high-signal. If you're optimizing for shipping AI products fast, MLSys, NeurIPS-Systems, or GTC are closer to your daily work.

References:

- [IEEE AICAS 2026 home](https://2026.ieee-aicas.org/)
- [Call for Demos (open until June 30)](https://2026.ieee-aicas.org/call-for-demos/)
- [Paper submission / EDAS](https://edas.info/N34921)
