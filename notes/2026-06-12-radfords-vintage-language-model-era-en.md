---
audio: false
generated: true
image: false
lang: en
layout: post
title: Radford's Vintage Language Model Era
translated: false
type: note
---

**Question:** What has Alec Radford (the former OpenAI researcher) been doing in recent years?

**Answer:**

Quick recap of why he matters: Radford was the lead author on GPT-1, GPT-2, CLIP, and Whisper, and a core contributor to DALL-E — a technical IC who never ran a team in the executive sense but kept shipping the field forward, with his name first on the papers that defined the modern era. Here's the recent timeline:

**December 2024 — Left OpenAI.** He told colleagues he was leaving to pursue research independently, and said he planned to collaborate with OpenAI and other AI developers. No new lab, no startup — just independent research, which is very on-brand for him.

**March–April 2025 — Advisor at Thinking Machines Lab.** He joined Mira Murati's Thinking Machines Lab as an advisor, alongside Bob McGrew, OpenAI's former chief research officer. Advisory role only, not full-time.

**April 28, 2026 — Released Talkie, a "vintage language model."** This is the most interesting one for you, given your nanoGPT/training interests. Radford, with Nick Levine and David Duvenaud, trained a 13B-parameter model on 260 billion tokens of English text all predating January 1, 1931 — historical books, newspapers, scientific journals, patents, and case law. No web crawl, no Wikipedia, no modern code. Key technical details:

- Two checkpoints released under Apache 2.0: talkie-1930-13b-base and an instruction-tuned -it variant fine-tuned on instruction-response pairs extracted from pre-1931 reference works
- The 1930 cutoff was chosen because works published in the US in 1930 entered the public domain on January 1, 2026 — so the whole corpus is copyright-clean
- It's a non-profit team effort with compute support from Anthropic
- The research motivation is serious: it's a clean testbed for generalization vs. memorization. Benchmark contamination — test questions leaking into training data — is one of AI's most stubborn problems, and a model that physically cannot have seen post-1930 text sidesteps it. It also breaks the shared web-data lineage of every modern LLM, letting researchers study which behaviors are universal to language modeling versus artifacts of training on the contemporary web
- The team says it's the largest vintage language model so far and plans to keep scaling significantly
- One related open question they cite: could a model trained only on pre-1911 text independently derive general relativity, as Demis Hassabis has suggested? Larger vintage models could reveal those scaling trends

If you want to play with it hands-on: weights are on Hugging Face (Apache 2.0, base is ~53 GB so it fits comfortably on your MI300X, and a quantized -it would run on the 4070), inference library on GitHub, live chat at talkie-lm.com. Given that you're training GPT-2-scale models from scratch, the dataset engineering side of Talkie (OCR pipelines, temporal leakage filtering — misdated documents or old texts with anachronistic editorial introductions can compromise historical fidelity) is probably the most instructive part to dig into.

**References:**

- [Simon Willison — Introducing talkie](https://simonwillison.net/2026/Apr/28/talkie/)
- [The Decoder — LLM that knows nothing after 1930](https://the-decoder.com/here-is-what-an-llm-that-knows-nothing-after-1930-thinks-our-world-looks-like-in-2026/)
- [MarkTechPost — Talkie-1930 technical overview](https://www.marktechpost.com/2026/04/27/meet-talkie-1930-a-13b-open-weight-llm-trained-on-pre-1931-english-text-for-historical-reasoning-and-generalization-research/)
- [Wikipedia — Alec Radford](https://en.wikipedia.org/wiki/Alec_Radford)
