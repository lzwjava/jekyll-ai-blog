---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Talkie: A Vintage LM from 1930"
translated: false
type: note
---

**Question:** Give me an intro to talkie (<https://talkie-lm.com/introducing-talkie>).

**Answer:**

talkie is a 13B "vintage" language model trained on 260B tokens of pre-1931 English text, released April 2026 by Nick Levine, David Duvenaud, and Alec Radford. The core idea (term coined by Owain Evans): train an LM *only* on historical text so its knowledge cutoff is literally December 31, 1930 — a simulated conversation partner from the past, and more interestingly, a clean scientific instrument for studying LMs in general.

**Why it matters as research, not just a toy:**

1. **Contamination-free generalization tests.** Modern benchmarks are polluted by training-set leakage. A pre-1931 model has *zero* exposure to digital computers, so you can ask: can it learn Python purely in-context? On HumanEval with 100 samples and few-shot examples, vintage models dramatically underperform web-trained architectural twins, but improve steadily with scale — successful solutions are one-liners or small edits to in-context examples, e.g. inverting a rotation cipher by swapping `+` for `-`. That single-character edit implies some grasp of inverse functions with no code in pretraining.

2. **Forecasting evals.** They scored ~5,000 NYT historical event descriptions by bits-per-byte surprisal against the model; surprisal rises after the 1930 cutoff, peaks in the 1950s–60s, then plateaus — a quantitative way to measure how far an LM can "see" past its data.

3. **Data-diversity science.** Every modern model is downstream of the web (directly or via distillation). A web-free model lets you ask how much of "LM behavior" is about language in general vs. this one dataset.

**Engineering details worth knowing:**

- **Modern twin baseline:** same architecture trained on FineWeb at equal FLOPs. talkie underperforms on knowledge evals; filtering out anachronistic questions halves the gap, and core language understanding/numeracy are comparable.
- **Temporal leakage is the hard problem.** They use an n-gram anachronism classifier to filter the corpus, but it's imperfect — the model still knows about FDR's New Deal and some WWII/postwar facts. (Their 7B knew even more.)
- **OCR is the data bottleneck.** All pre-1931 text comes from scans. Conventional OCR transcriptions yield only 30% of the learning efficiency of human transcriptions; regex cleaning recovers it to 70%. Modern VLM OCR is more accurate but hallucinates modern facts into the corpus — so they're building a dedicated vintage OCR system.
- **Post-training without modern chat data:** SFT on instruction pairs mined from structurally regular historical texts (etiquette manuals, cookbooks, encyclopedias) → online DPO with Claude Sonnet 4.6 as judge (instruction-following rating went 2.0 → 3.4 on a 5-point scale) → final SFT on rejection-sampled Claude-talkie multi-turn chats. They note the RLAIF inevitably injects anachronism (the 7B started speaking in listicles), and want vintage-model-as-judge for a fully bootstrapped pipeline.

**Roadmap:** GPT-3-level vintage model this summer; corpus expansion to 1T+ tokens of historical text, which they estimate is enough for a GPT-3.5/ChatGPT-class model. Cutoff chosen as 1930 because that's the US public-domain boundary. Funded/computed in part by Coefficient Giving and Anthropic.

For your interests specifically: this is essentially nanoGPT-style methodology applied to a controlled-data experiment, and the base + IT checkpoints are on Hugging Face (`talkie-lm/talkie-1930-13b-base`, `-it`) with code on GitHub — very inspectable if you want to study how post-training behaves without web priors, or replicate the surprisal-vs-decade eval.

**References:**

- [Introducing talkie](https://talkie-lm.com/introducing-talkie)
- [talkie on GitHub](https://github.com/talkie-lm/talkie)
- [talkie-1930-13b-base on Hugging Face](https://huggingface.co/talkie-lm/talkie-1930-13b-base)
