---
audio: false
generated: true
image: false
lang: en
layout: post
title: June 2026 Hugging Face Top Models
translated: false
type: note
---

**Question:** What are the hot/trending models on Hugging Face right now (June 2026)?

**Answer:**

DeepSeek V4.1 Flash took the #1 trending slot within one week of its release, and Chinese open-weight models now hold five of the top ten slots — the highest concentration ever recorded on HF.

Here's the full top 20 snapshot:

| Rank | Model | Vendor | License | Notes |
| ------ | ------- | -------- | --------- | ------- |
| 1 | **DeepSeek V4.1 Flash** | DeepSeek | DeepSeek License | MoE, ~71B active |
| 2 | **Qwen 3.7** (flagship) | Alibaba | Qwen License | |
| 3 | **Gemma 4** (31B Dense) | Google | Apache 2.0 | Permissive commercial |
| 4 | **Llama 4.5 Maverick** | Meta | Llama Community | |
| 5 | **GLM-6** (flagship MoE) | Zhipu AI | MIT-modified | |
| 6 | DeepSeek V4.1 smaller variants | DeepSeek | DeepSeek License | |
| 7 | Llama 4.5 Scout | Meta | Llama Community | |
| 8 | **Qwen 3.7 Coder** | Alibaba | Qwen License | |
| 9 | **Qwen 3.7 VL** (vision) | Alibaba | Qwen License | |
| 10 | **Kimi K2.6** | Moonshot AI | MIT-modified | |
| 11 | Mistral Small 3.x | Mistral AI | Apache 2.0 | |
| 12 | Hunyuan Large 3 | Tencent | Custom open | |
| 13 | Yi-Lightning 2 | 01.AI | Apache 2.0 | |
| 14 | Phi-4 series | Microsoft | MIT | |
| 15 | FLUX 1.1 Pro | Black Forest Labs | Custom commercial | Image gen |
| 16 | Stable Diffusion 4 | Stability AI | Custom open | Image gen |
| 17 | Whisper v3 Turbo | OpenAI | MIT | Audio |
| 18 | Sentence-Transformers v3 | Multiple | Apache 2.0 | Embeddings |
| 19 | NV-Embed v3 | NVIDIA | — | Embeddings |

**Key signals for you:**

- The June 2026 Chinese frontier wave shipped six competitive releases within two weeks — Qwen 3.7, DeepSeek V4.1, Hunyuan Large 3, ERNIE 5.1, Doubao Pro, GLM-6 — open-weight releases from that wave drove the trending concentration.
- Gemma 4 holds strong at #3 largely due to Apache 2.0 commercial clarity.
- Embedding models (NV-Embed, BGE-M3, Sentence-Transformers) dominate the long-tail of downloads even if not top-10 in velocity.

**For your use case** — you're already on deepseek-v4-flash (basically #1 here). Kimi K2.6 is worth watching if you haven't tried it (Moonshot AI, MIT-ish license). GLM-6 is Zhipu's MoE flagship and has been strong on Chinese benchmarks but also competitive on code. Qwen 3.7 Coder at #8 is relevant if you're building coding agents.

**References:**

- [Hugging Face Trending Models June 2026 — Presenc AI](https://presenc.ai/research/huggingface-trending-models-june-2026)
