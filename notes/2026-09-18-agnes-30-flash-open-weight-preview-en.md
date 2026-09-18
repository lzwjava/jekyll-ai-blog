---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agnes-3.0-Flash Open-Weight Preview
translated: false
type: note
---

**Question:** What is Agnes-3.0-Flash on Hugging Face?

**Answer:**

Agnes-3.0-Flash Preview is an open-weights multimodal AI model by Agnes AI, released in September 2026. Here's a breakdown:

**What it is**

It is an open-weights multimodal preview model (33B parameters) built for "flagship-class reasoning without flagship-class hardware," supporting text, image, and video understanding with a 262,144-token context window.

**Important Clarification**

This repository contains an earlier open-weight **Preview checkpoint**, distinct from the newer **production/API checkpoint**. The production model uses a different configuration with a 1M-token context window — its benchmark results should not be attributed to the Preview weights released here.

**Architecture Highlights**

It uses a hybrid-attention decoder: 3 out of every 4 layers run a gated delta rule (recurrent), and only 1 in 4 runs standard global attention. This means only 18 of 72 layers hold a KV cache that grows with context length — making it more memory-efficient for long sequences.

**Key Capabilities**

| Feature | Detail |
|---|---|
| Parameters | 33B |
| Context window | 262,144 tokens |
| Modalities | Text, image, video |
| Reasoning effort | High / Medium / Low (adjustable) |
| Tool calling | Yes |
| License | Apache 2.0 |

**Hardware Requirements**

It requires approximately 66 GB on disk for the bf16 checkpoint and is recommended to run on 1× NVIDIA H200 141 GB or H100 80 GB GPU, with 128 GB or more of host memory.

**Benchmark Performance**

On GPQA Diamond (a graduate-level science reasoning benchmark), the Preview checkpoint scores 85.05, which is competitive with models like Qwen3.5-27B (85.8), though behind larger or API-only models like Gemini 3.5 Flash (92.2).

**References:**
- [Agnes-AI/Agnes-3.0-Flash on Hugging Face](https://huggingface.co/Agnes-AI/Agnes-3.0-Flash)
- [Agnes AI Website](https://agnes-ai.com/)
