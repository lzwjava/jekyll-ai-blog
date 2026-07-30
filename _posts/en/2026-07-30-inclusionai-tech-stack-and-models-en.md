---
audio: false
generated: true
image: false
lang: en
layout: post
title: InclusionAI Tech Stack and Models
translated: false
type: note
---

Question: What is InclusionAI, and what's their tech stack / model lineup?

Answer:

**Who they are**

InclusionAI (IAI) is founded by Ant Group with researchers formerly at OpenAI, Google, and FAIR (Meta AI), positioning itself around open-source AGI built by and for everyone. Not a startup — Ant Group is Alibaba-affiliated fintech (Alipay parent), so this is a well-capitalized incumbent's AGI lab, similar in spirit to how DeepSeek emerged from a quant fund.

Key people (per an AI Wiki profile, take with normal skepticism on org wikis): Wu Yi (ex-OpenAI, Berkeley PhD), Le Zhenzhong (CMU grad, ex-Google AI), Cai Wei (Stanford, ex-Google, worked on Image Search/Cloud Vision API), Shen Chunhua (h-index 130+), Yang Ming (founding FAIR member), Zheng Da (Ant's graph computing lab), with Zhengyu He (Georgia Tech PhD, GPU max-flow algorithms) as Ant's CTO and executive sponsor of the AGI program.

**Model lineup you'd actually care about**

1. **Ling series** — flagship dense/MoE LLMs.
   - Ling-2.6-1T is a trillion-parameter model using a "Fast-Thinking" mechanism, distinct from long-CoT reasoning models, targeting agent-era execution: code edits, tool calls, complex instruction-following. It supports a 262.1k token context, 32.8k max output, is available via free API on OpenRouter, and open-sourcing is planned.
   - Predecessor Ling-1T got picked up in open-model roundups as one of the strong Chinese releases in late 2025.

2. **LLaDA2.0/2.X** — diffusion LLMs, not autoregressive. Features LLaDA2.0-mini (16B) and LLaDA2.0-flash (100B), both MoE, marking the first diffusion LM scaled to 100B params. LLaDA2.0-flash-CAP hits 535 tokens/s via parallel decoding — 2.1x over comparable AR models. Weights and training code for both sizes are fully open on Hugging Face. This is the interesting one for you if you're doing inference/serving work — parallel decoding at 100B MoE scale is a real systems achievement, not just a paper.

3. **Ming** — multimodal understanding/generation built on the Ling LLM backbone.

4. **ZwZ family** — ICML 2026 fine-grained perception model, paired with ZoomBench, a new perception benchmark.

5. **Ring-Zero** — research paper (arXiv, July 14 2026) pushing zero-RL (RL on raw base model, no human-labeled data) to 1T params on the Ling architecture. They document five emergent behaviors nobody explicitly engineered: self-verification, parallel reasoning, structured formatting, anthropomorphic narrative, and "context anxiety" — the model actively managing its own compute budget mid-inference. Worth reading if you're doing RL post-training — this is a genuine scaling-law result on emergent behavior, not marketing fluff.

**Infra you can actually use**

AReaL (Ant Reasoning RL) — open-source async RL training system for reasoning/agentic models, co-developed with Tsinghua IIIS. It decouples rollout generation from policy updates so GPU utilization stays continuous across inference and training workers, avoiding the sync-stall bottleneck of standard RL pipelines. Given you're already doing model training on MI300X clusters, this async rollout/policy decoupling is directly relevant if you're building or tuning your own RL loop — it's the same class of problem as OpenRLHF/veRL but Ant's framing emphasizes continuous GPU util as the headline metric.

Also: ABench (internal benchmark suite) and dInfer (inference framework built for diffusion LMs, shipped alongside Ling-1T).

**Caveat worth noting explicitly, not burying**: InclusionAI operates under Ant Group, headquartered in China, subject to China's National Intelligence Law (2017), Data Security Law (2021), and Cybersecurity Law (2017) — relevant if you're routing production traffic through their API/OpenRouter endpoint rather than self-hosting the open weights.

References:
- [InclusionAI GitHub org](https://github.com/inclusionAI)
- [LLaDA2.X repo](https://github.com/inclusionAI/LLaDA2.X)
- [Ling-2.6-1T announcement](https://phemex.com/news/article/ant-group-unveils-ling261t-a-trillionparameter-ai-model-76554)
- [Interconnects interview w/ Ant Ling & InclusionAI lead](https://www.interconnects.ai/p/inside-a-chinese-frontier-lab-inclusion)
- [Ring-Zero coverage](https://www.techtimes.com/articles/320677/20260716/trillion-parameters-no-human-labels-ant-group-documents-five-emergent-ai-behaviors.htm)
- [AI Wiki: InclusionAI](https://aiwiki.ai/wiki/inclusionai)