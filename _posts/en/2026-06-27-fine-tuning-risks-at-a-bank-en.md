---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-tuning Risks at a Bank
translated: false
type: note
---

**Question:** Is it a good idea to fine-tune GLM-5.2 or DeepSeek V4 as a base model on the bank's finance data, then run it on public RunPod from a personal laptop while sharing the result internally over company channels (Teams, etc.)?

**Answer:**

The *modeling* idea is sound. The *data-handling plan* as described would likely get you walked out of the bank. Let me separate the two cleanly, because they have very different risk profiles.

### 1. The technical idea — yes, this is the right shape

Fine-tuning an open-weight base (GLM or DeepSeek V4) on domain finance data is exactly how you build a defensible internal asset. A few sharpenings:

- **Don't full-fine-tune a 600B+ MoE.** DeepSeek V4 is a large MoE; full FT is infeasible on RunPod budget and unnecessary. Use **LoRA/QLoRA on the active experts + attention**, or better, treat the base as frozen and do **continued-pretraining-lite on domain corpus → SFT on instruction pairs → optional DPO** on preference data from your analysts. For a bank, the highest-ROI move is usually **RAG over fine-tune** for factual finance knowledge (regulations, internal docs change constantly — you don't want them baked into weights). Fine-tune for *behavior and format* (how to answer, tone, structured output), RAG for *facts*.
- **GLM-5.2 vs DeepSeek V4 as base:** pick by license first, not benchmark. Check the commercial-use and redistribution terms — a bank's legal will care more about the license than your eval scores. DeepSeek's MoE gives you better cost/perf at inference if you can host it; GLM dense-ish variants are easier to LoRA and serve on modest hardware.
- **Eval is the actual product.** Before any of this, build a finance eval set (real questions, graded answers). Without it you can't prove the fine-tune beats base+RAG, and you can't sell it internally.

### 2. The data + infra plan — this is the part to stop and rethink

Here's the problem, stated directly:

> bank finance data → personal laptop → public RunPod → shared back over company Teams

That pipeline moves regulated customer/financial data **off the bank's controlled environment onto third-party GPUs via your personal machine.** At a global bank this is almost certainly a breach of:

- Data residency / cross-border transfer rules (your contract is Guangzhou, RunPod GPUs are wherever — instant cross-border issue)
- Customer data confidentiality + banking secrecy law
- The bank's third-party / cloud vendor approval process (RunPod is not an approved processor)
- Your contractor agreement's IP and data clauses — anything you train on bank data, the bank likely owns, and you've now copied it to infra they don't control

As a contractor with no promotion path, you have the *least* protection if this goes wrong. This is a "tax to pay" task that could end the salary, not a learning-ground task. The asymmetry is brutal: upside is a cool internal demo, downside is termination + legal exposure.

### What I'd actually do instead

**Split into two tracks:**

**Track A — the bank version (compliant, boring, real):**
- Propose it *through the channel*. Banks have internal GPU/AI platforms now (or sanctioned cloud — Azure OpenAI-style private deployments). Get the idea funded as a sanctioned project. "I can build a finance-tuned assistant on our approved infra" is a strong contractor pitch that raises your leverage.
- Use **synthetic / de-identified data** for any experimentation that touches your own machine. Never raw PII/financial records off-prem.
- If they won't sanction it, that's your answer: don't do it covertly.

**Track B — your version (your IP, your career):**
- Build the *exact same pipeline* on **public finance datasets** — SEC EDGAR filings, FinQA, ConvFinQA, FiQA, financial news corpora. Same architecture, same LoRA recipe, same eval harness, on RunPod or your MI300X.
- This is the one you blog, open-source, and put in your notes. It's portable, it's yours, and it demonstrates the exact capability without the legal landmine. *This* is the startup-optionality asset; the bank-internal version never leaves the bank.

You get the skill, the artifact, and the credibility from Track B — and the leverage/salary upside from Track A — without ever putting raw bank data on a personal laptop and a public GPU host.

The instinct (one engineer + AI-native pipeline builds what a team used to) is right. Just point it at data you're allowed to move.

**References:**
- [DeepSeek V3/V4 model & license](https://github.com/deepseek-ai/DeepSeek-V3)
- [GLM model family](https://github.com/THUDM/GLM-4)
- [FinQA dataset](https://github.com/czyssrs/FinQA)
- [ConvFinQA](https://github.com/czyssrs/ConvFinQA)
- [SEC EDGAR full-text filings](https://www.sec.gov/edgar/searchedgar/companysearch)
