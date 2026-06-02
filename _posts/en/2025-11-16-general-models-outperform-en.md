---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: General Models Outperform Domain Specific AI
translated: false
type: note
---

You're raising a very good and timely question. The pendulum in the AI industry has indeed swung back toward **general-purpose foundation models** being more reasonable (and economically dominant) than narrow domain-specific models for most use cases. Here’s why the “BloombergGPT / Med-PaLM / FinanceGPT / LawGPT” style approach has become less attractive in 2024–2025:

### 1. Data contamination and overlap is massive

Modern pre-training corpora (RefinedWeb, FineWeb, Dolma, RedPajama v2, etc.) already contain huge amounts of finance, law, medical, and code text. For example:

- Common Crawl alone has billions of SEC filings, court documents, GitHub repos, arXiv papers, financial news, etc.
- A general model trained on 10–30T tokens sees almost as much high-quality finance/law/code data as a “domain-specific” model trained on 1T tokens of hand-curated domain data.

Result: The performance gap between a 100B–400B general model and a 100B “FinanceGPT” has shrunk dramatically. BloombergGPT (2023) beat general models by ~10–20% on finance tasks, but Llama 3.1 405B or Qwen2.5 72B today often match or exceed BloombergGPT’s numbers with zero domain-specific training.

### 2. Domain boundaries are blurry and moving

You already pointed this out perfectly: finance + AI, crypto + law, biotech + finance, programming + math + physics, etc. Knowledge is heavily entangled now.

- A pure “finance” model will fail on DeFi/smart-contract questions because it never saw enough code.
- A pure “law” model will struggle with AI-regulation cases that require understanding transformers and training data.
- A pure “programming” model will be bad at writing trading algorithms that need market microstructure knowledge.

General models handle these compound domains naturally because they saw everything mixed together—just like the real world.

### 3. MoE makes specialization almost free

Mixture-of-Experts (Mixtral, DeepSeek-V3, Qwen2.5-MoE, Grok-1.5, etc.) already does lightweight domain routing internally. Some experts learn to fire more on code, some on finance, some on biomedical text, etc., without anyone having to explicitly separate the data. You get most of the benefit of domain-specific routing with zero extra engineering or sales effort.

### 4. Economics and distribution have changed

2023 thinking: “Train a 50B FinanceGPT on proprietary data → sell API access to banks at $50–200 per million tokens.”
2025 reality:

- Banks can just use Claude 3.5 / GPT-4o / Llama 405B + RAG on their internal documents and get 95–98% of the performance for 1/50th the cost.
- Open-source frontier models (Llama 3.1 405B, Qwen2.5 72B, DeepSeek-V3) are now good enough that most companies prefer fine-tuning or context injection rather than paying a huge premium for a closed domain model.
- Hosting and inference cost for a dedicated 70B–400B domain model is very high if your customer base is small.

### 5. Post-training (SFT + RL) closes almost the entire remaining gap

Even if a general model is slightly behind on pure domain knowledge after pre-training, 500–5000 high-quality synthetic or human-written examples in supervised fine-tuning + DPO/RLHF aligned to that domain will push it to state-of-the-art anyway. This is 100× cheaper and faster than collecting and cleaning terabytes of domain pre-training data.

### When domain-specific models still make sense (the few remaining cases)

- Extremely regulated or security-sensitive environments where you literally cannot send data to OpenAI/Anthropic/Meta (some defense, some central banks, some healthcare systems).
- When you have massive proprietary data that is truly not on the public internet (e.g., trillions of private trade records, decades of internal legal memos) and you can prove the general models are missing signal.
- Tiny models that run on-device or in air-gapped systems (e.g., legal co-pilot that runs entirely inside a law firm’s firewall with <7B parameters).

For 95%+ of commercial use cases in 2025, though, the answer is:
General frontier model (open or closed) + domain-specific post-training / RAG / tool use >> dedicated domain pre-trained model.

So yes — you’re exactly right: the essence of the transformer is predicting text, regardless of domain, and the data mixing problem + scaling laws + MoE + cheap post-training have made purely domain-specific models mostly a 2022–2023 phenomenon.
