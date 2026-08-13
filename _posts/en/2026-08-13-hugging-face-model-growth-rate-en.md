---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hugging Face Model Growth Rate
translated: false
type: note
---

Question: How fast is Hugging Face model count growing? Is it really adding ~1 million models in 1–2 months?

Answer:

Yes, the growth is extremely fast, but **"1 million models in 1–2 months" is probably too high** unless you count some unusual spikes or repository creation events. The real growth has been roughly:

| Time       |                  Hugging Face public models |
| ---------- | ------------------------------------------: |
| 2024 early |                               ~500k+ models |
| Jan 2025   |                    ~1.27M models ([DOI][1]) |
| Mar 2025   | crossed **1.5M models** ([Hugging Face][2]) |
| Mid 2025   |            ~1.8M models ([Hugging Face][3]) |
| Late 2025  |  crossed **2M+ models** ([Hugging Face][4]) |

So the approximate growth rate:

```
Jan 2025:
1.27M

Mar 2025:
1.50M

growth:
+230k / ~2 months
≈ 115k models/month
≈ 4k models/day
```

Later in 2025:

```
1.5M → 2.0M

+500k models

over several months
≈ 100k-200k/month
```

([Hugging Face][4])

The reason it feels like an explosion is that Hugging Face models are no longer only "new foundation models".

A huge percentage are:

```
Base model
    |
    +-- LoRA fine-tune
    |
    +-- QLoRA variant
    |
    +-- merged checkpoint
    |
    +-- quantized GGUF
    |
    +-- language/domain adaptation
    |
    +-- benchmark variant
```

Example:

```
meta-llama/Llama-3.1-8B
        |
        +-- 1000s of community versions
             |
             +-- roleplay
             +-- coding
             +-- Chinese
             +-- medical
             +-- 4-bit
             +-- 8-bit
             +-- long context
             +-- agent tuning
```

This creates an "AI GitHub effect":

* GitHub has millions of repos because people fork and modify.
* Hugging Face has millions of models because people fine-tune and publish derivatives.

The ecosystem is shifting from:

```
2018-2022:
"Who trained the biggest model?"
```

toward:

```
2024-2026:
"Who adapted the model best for this niche?"
```

Examples:

* a 7B model specialized for legal Chinese
* a 3B model for embedded devices
* a vision model for industrial inspection
* a Japanese bilingual model
* a coding agent model

These small models are useful because inference is cheap.

The interesting metric is not only model count. The distribution is very long-tail:

```
2M models

Top 0.01%
    dominate downloads

Most models:
    few downloads
    niche users
    experimental
```

Hugging Face itself reported that many models have very low usage, while a small number of popular models dominate downloads. ([Hugging Face][4])

So your intuition is right:

> HF diversity is crazy. There are many small, weird, specialized models.

The model zoo is becoming like a biological ecosystem:

```
Llama/Qwen/Mistral base models
          |
          |
     thousands of mutations
          |
          |
 millions of specialized models
```

The "one giant GPT model wins everything" era is probably moving toward a world with millions of specialized descendants. ([arxiv.org][5])

References:

* Hugging Face State of Open Source AI 2026: ([Hugging Face][4])
* Hugging Face crosses 1.5M models: ([Hugging Face][2])
* Hugging Face ecosystem overview: ([Hugging Face][3])
* Anatomy of 2M Hugging Face models: ([arxiv.org][5])

[1]: https://doi.org/10.1145/3755881.3755921?utm_source=chatgpt.com "Exploring Typo Squatting Threats in the Hugging Face Ecosystem | Proceedings of the 16th International Conference on Internetware"
[2]: https://huggingface.co/posts/clem/238420842235482?utm_source=chatgpt.com "@clem on Hugging Face: \"We just crossed 1,500,000 public models on Hugging Face (and 500k spaces, 330k…\""
[3]: https://huggingface.co/blog/evijit/hf-hub-ecosystem-overview?utm_source=chatgpt.com "What is the Hugging Face Community Building?"
[4]: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026?utm_source=chatgpt.com "State of Open Source on Hugging Face: Spring 2026"
[5]: https://arxiv.org/abs/2508.06811?utm_source=chatgpt.com "Anatomy of a Machine Learning Ecosystem: 2 Million Models on Hugging Face"
