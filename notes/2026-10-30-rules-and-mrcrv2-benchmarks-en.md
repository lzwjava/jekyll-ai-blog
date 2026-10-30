---
audio: false
generated: true
image: false
lang: en
layout: post
title: RULES and MRCRv2 Benchmarks
translated: false
type: note
---

**Question:** What are RULES and MRCRv2 attention tests for LLMs?

**Answer:**

---

## RULES (Rule-Following Language Evaluation Scenarios)

RULES is a programmatic benchmark designed to evaluate Large Language Models' ability to reliably follow simple, explicit rules. Each scenario includes a programmatic evaluation function that automatically detects rule violations using string comparison and regular expressions — eliminating the need for subjective human judgment.

Key findings:

- Alignment fine-tuning (as in Llama-2 Chat and Gemma IT) surprisingly **decreases** rule-following performance on this benchmark.
- Harmless rule scores show near-zero correlation with other existing benchmarks, indicating RULES measures a **fundamentally different** capability in LLMs.
- The evaluation covers proprietary models (GPT-4, Claude, Gemini) and over 100 open-weight models.

---

## MRCRv2 (Multi-Round Coreference Resolution v2)

MRCRv2 is an enhanced version of the synthetic long-context reasoning task. It extends the original MRCR framework with improved evaluation criteria and additional complexity for testing models' ability to **maintain attention and reasoning across extended contexts**.

The core idea is a "Latent Structure Queries" (LSQ) framework — tasks that require a model to "chisel away" irrelevant information in the context to reveal a latent structure, then query the model for details of that structure. This provides a stronger signal of long-context language model capabilities.

Key variants:

- **MRCR v2 (8-needle)**: Retrieves 8 needle items from long contexts. Meta's Muse Spark 1.3 currently leads with a score of 0.985.
- **MRCR v2 (8-needle, 512K–1M)**: Evaluated on contexts from 512K to 1 million tokens, currently led by OpenAI models.
- MRCRv2 carries significant weight in benchmark scoring systems — contributing 20% of the Reasoning category score.

---

**In short:**

| Benchmark | Tests | Key Challenge |
| --- | --- | --- |
| **RULES** | Rule-following obedience | LLMs often violate explicit instructions |
| **MRCRv2** | Long-context attention & retrieval | Tracking multiple items across 512K–1M token contexts |

**References:**

- [RULES Paper (arXiv)](https://arxiv.org/abs/2311.04235)
- [MRCRv2 Paper (arXiv)](https://arxiv.org/abs/2409.12640)
- [MRCRv2 Leaderboard - LLM Stats](https://llm-stats.com/benchmarks/mrcr-v2)
