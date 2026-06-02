---
audio: false
generated: true
image: false
lang: en
layout: post
title: Overview of Huawei Pangu Ultra 135B
translated: false
type: note
---

Question: What is the Pangu 135B V3 model from Huawei?

Answer:

## Huawei Pangu 135B V3 ("Pangu Ultra")

The **135B V3** refers to the third-version, 135-billion-parameter dense large language model developed by Huawei's **Noah's Ark Lab** as part of the Pangu AI program. It is officially branded as **Pangu Ultra**.

---

### Technical Specifications

Pangu Ultra is a dense LLM with **135 billion parameters** and a **128K context window**, trained on **13.2 trillion tokens** using **8,192 Ascend 910B NPUs** (Huawei's custom AI chips).

The model features **94 neural layers** and uses a three-phase training regimen: Phase 1 covers 12 trillion tokens of general knowledge, Phase 2 adds 0.8 trillion tokens for reasoning (math and code), and Phase 3 uses curriculum learning with complex Q&A pairs.

To address training instability at such depth, Huawei introduced **Depth-Scaled Sandwich Normalization (DSSN)** and **TinyInit**, which reduced training loss spikes by 78% compared to Meta's Llama 3 approach.

It achieved strong benchmark results, surpassing models like LLaMA-3 (405B dense) and Qwen2.5 (72B), and was competitive with DeepSeek-R1 (671B MoE), despite being a smaller, purely dense model.

---

### The "V3" Significance — Context from the Whistleblower Scandal

The **V3** label is especially significant due to a major internal controversy that came to light in mid-2025. According to a whistleblower from Huawei's Noah's Ark Lab:

- **135B V1 and V2** were allegedly built through "shelling" — repackaging competitor models (particularly Alibaba's Qwen-110B), making superficial changes, and presenting them as proprietary developments.

- **135B V3**, however, was the exception. The core team fully trained the 135B V3 "Pangu Ultra" model from scratch on Ascend hardware — no shortcuts, no stolen code — with stable training, no spikes in loss, and reliable performance matching competitor benchmarks.

- The whistleblower called it the team's genuine point of pride, writing that they were "willing to guarantee the authenticity of this model's training with our lives and honor," describing a grueling process with countless rollbacks to ensure stability.

- Unlike the allegedly plagiarized V2, the 135B V3 used a refined tokenizer and improved training pipeline — described as the "true product of blood, sweat, and sacrifice" — delivering clean training with no loss spikes.

---

### Why It Matters

The 135B V3 was seen internally as Huawei's first truly competitive, honest effort, demonstrating that Huawei's Ascend chips could genuinely train a large-scale model from scratch, without relying on NVIDIA hardware — a significant geopolitical and technical statement given ongoing US sanctions.

Huawei also applied DSSN and TinyInit to help the model achieve over 52% MFU (Model FLOP Utilization) on Ascend chips, which is a notable hardware efficiency result.

---

### Summary Table

| Attribute | Detail |
|---|---|
| Model Name | Pangu Ultra (135B V3) |
| Parameters | 135 billion (dense) |
| Context Window | 128K tokens |
| Training Tokens | 13.2 trillion |
| Hardware | 8,192 Ascend 910B NPUs |
| Key Techniques | DSSN, TinyInit, NPU Fusion Attention |
| Status | Genuinely trained from scratch (per whistleblower) |

References:

- [The Pangu Illusion – Open Source Ward](https://www.open-source-ward.com/the-pangu-illusion-how-huaweis-star-ai-model-was-built-on-burnout-betrayal-and-open-source-theft/)
- [Huawei PanGu – Wikipedia](https://en.wikipedia.org/wiki/Huawei_PanGu)
- [The Latest Huawei AI Scandal – Medium](https://medium.com/@PlanB./the-latest-huawei-ai-scandal-unlocking-the-secret-fraud-behind-pangus-fall-e171cce1f075)
- [Pangu Ultra Technical Overview – zqg8.com](https://www.zqg8.com/post/383.html)
- [Whistleblower: Huawei cloned Qwen and DeepSeek – Dilemma Works](https://dilemmaworks.substack.com/p/whistleblower-huawei-cloned-and-renamed)
- [How Huawei Trains LLMs Using Ascend Chips – Recode China AI](https://recodechinaai.substack.com/p/how-huawei-trains-deepseek-r1-class)
- [Whistleblower Exposes Alleged Fraud – CTOL Digital Solutions](https://www.ctol.digital/news/whistleblower-exposes-alleged-fraud-misconduct-huawei-flagship-ai-program/)
