---
audio: false
generated: true
image: false
lang: en
layout: post
title: MTP Acceptance Rate Differences Explained
translated: false
type: note
---

**Question:** In the context of a tech discussion group, what does "MTP" mean, and is it normal that DSv4 + mtp_1 achieves ~90% acceptance rate with random inputs while GLM 5.2 + mtp_1 only reaches ~60%?

---

**Answer:**

**MTP = Multi-Token Prediction** — a speculative decoding technique where the model uses extra lightweight "draft heads" baked into its architecture to predict multiple future tokens per forward pass. Instead of generating one token at a time, MTP proposes the next 1–N tokens cheaply, which are then verified in parallel by the main model. The "mtp_1" in the message refers to using 1 speculative step (drafting 1 extra token ahead).

---

**Is the acceptance rate difference normal? Yes, and here's why:**

**1. DSv4's MTP was architecturally optimized for high acceptance rates.**
DeepSeek-V3's real-world practice data shows the MTP module achieves an acceptance rate of 80%–90% for predicting the next token, enabling 1.8x generation TPS improvement. DSv4 is built on the same lineage with continued MTP improvements.

**2. GLM 5.2 uses a different MTP design with different trade-offs.**
GLM-5.2 uses an MTP layer with KVShare speculative decoding that Z.ai reports raises draft-token acceptance length by up to 20% — but its baseline acceptance rate appears lower than DSv4's, especially on random/out-of-distribution inputs.

**3. Random inputs are a worst-case scenario that exposes architectural differences.**
The acceptance rate depends critically on how closely the draft model's token distribution approximates the target model's distribution. Random inputs have no coherent distribution, so models with tighter coupling between the MTP head and the main trunk will have a natural advantage.

**4. The underlying training strategy matters significantly.**
DeepSeek-V3 is trained with a single MTP layer but predicts 2 tokens at inference — this training-inference discrepancy reduces the acceptance rate of the second token. GLM-5 addresses this by sharing parameters of 3 MTP layers during training, keeping memory cost consistent with DeepSeek-V3 while increasing acceptance rate. GLM 5.2 inherits this lineage, but on *random* inputs (not realistic prompts), DSv4's raw acceptance rate for mtp_1 still dominates because its head was more aggressively optimized.

**5. 60% on mtp_1 is still within the normal/healthy range.**
Acceptance rates below 0.55 indicate a distribution mismatch; reducing num_speculative_tokens is recommended in that case. GLM 5.2 at 60% is above this threshold and functioning correctly — you'd still be getting a speedup.

---

**Summary table:**

| Model | MTP_1 Acceptance (random input) | Notes |
|---|---|---|
| DSv4 | ~90% | Highly optimized single MTP head |
| GLM 5.2 | ~60% | Different architecture; lower on random, better on real prompts |

On realistic prompts (code, chat, documents), the gap typically narrows because GLM 5.2's shared-parameter MTP design is more stable across longer speculation chains.

---

**References:**
- [DeepSeek-V3 MTP Architecture Deep Dive](https://arxiv.org/pdf/2505.09343)
- [GLM-5 MTP Parameter Sharing Design](https://arxiv.org/html/2602.15763v1)
- [MTP Deployment Guide (vLLM/SGLang)](https://www.spheron.network/blog/multi-token-prediction-mtp-gpu-cloud-deployment-guide/)
- [Nebius Fine-tuned MTP for DeepSeek-V3](https://huggingface.co/nebius/MTP-DeepSeek-V3-0324)