---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learningto Replicate Expert Judgment
translated: false
type: note
---

**Question:** How did Thinking Machines Lab and Bridgewater collaborate using the Tinker API — what was the project, the training recipe, and the results?

**Answer:**

This is the "Learning to Replicate Expert Judgment in Financial Tasks" work, published June 30, 2026 by Sarah Su, Kevin Zhu, Emily Xiao, Rohan Alur (Thinking Machines) and Daniel Kang (Bridgewater AIA Labs). It's the strongest public case study of Tinker in production so far, and it's directly relevant to your Phase 1 consulting thesis.

**The problem.** They evaluated models on six information-filtering tasks drawn from investors' daily workflows — e.g., given a financial article, classify whether it's relevant to a C-suite investment professional; given a central bank document, classify whether it signals the direction of future interest rate changes. The catch: relevance decisions were hard to automate because a correct answer often depended on Bridgewater's private workflow rather than public web knowledge — Gemini, Claude, and GPT variants averaged roughly 50% accuracy given only task descriptions. Expert-written prompts (including a smart label reframing: relevant-and-interesting / relevant-but-uninteresting / irrelevant) boosted frontier models from a coin flip to the mid-70s, and automatic prompt optimization added nothing further. Best prompted frontier models still stayed under the 80% accuracy threshold investors required for trust.

**The model and platform.** They fine-tuned Qwen3-235B (the MoE) via Tinker, which uses LoRA adapters so the customer's data stays tied to the customer's model, and exposes forward-backward, optimizer-step, sampling, and save-state primitives. Tinker handled the infrastructure side, letting the team iterate rapidly without managing GPU clusters directly.

**The training recipe** — this is the interesting part for you:

The method combined expert-labeled fine-tuning data with GRPO, interleaved batching (+12.1%), CISPO loss with asymmetric clipping (+10.1%), and on-policy distillation with dynamically promoted teacher models (+3.1%). In the on-policy distillation setup, a student model learns from its own attempted outputs while stronger teachers grade them. Note the recipe is basically what's in the tinker-cookbook already — SFT → RL with a GRPO-family objective → on-policy distillation — but with two non-obvious tricks (interleaved batching and asymmetric CISPO clipping) doing most of the lifting. Contractor labels were not enough on their own — expert labels were the real dataset moat.

**Results.** The custom model reached 84.7% vs. 78.2% for the best expert-prompted frontier baseline — 29.8% fewer errors, and significantly cheaper to operate — 13.8x cheaper inference per call. Caveat worth keeping: these are company-run measurements on an internal six-task evaluation, so treat the exact numbers as marketing-adjacent even if the direction is credible.

**The strategic frame.** They call it "differentiated intelligence" — custom models tuned to specific organizational needs outperforming frontier models. Tinker is the commercial product being validated here; every institution with proprietary expert-labeled data is a potential Tinker customer.

**Why this matters for you specifically:** this is literally the playbook you wrote in your Phase 1 plan — "Tinker-level skills as moat," high-end clients, fine-tuning on proprietary judgment data. The Bridgewater result is the sales deck you can point Greater Bay Area / HK financial clients to: frontier API + prompting caps out below deployment threshold; expert labels + LoRA fine-tune on an open MoE breaks through it at 1/14th inference cost. The reproducible parts (GRPO, on-policy distillation, LoRA on Qwen MoE) are all in the open tinker-cookbook — worth replicating a mini version on a public dataset as a portfolio piece. Also note the cookbook now ships Claude Code skills that teach Claude the Tinker API (`/plugin marketplace add thinking-machines-lab/tinker-cookbook`), which fits your agent-first workflow.

**References:**

- [Learning to Replicate Expert Judgment in Financial Tasks — Thinking Machines Lab](https://thinkingmachines.ai/news/learning-to-replicate-expert-judgment-in-financial-tasks/)
- [Bridgewater test says GPT, Claude lag tuned Qwen model — WinBuzzer](https://winbuzzer.com/2026/07/04/bridgewater-test-says-gpt-claude-lag-tuned-qwen-model-xcxwbn/)
- [TML × Bridgewater analysis — FourWeekMBA](https://fourweekmba.com/ai-thinking-machines-lab-bridgewater-custom-model-beats-frontie/)
- [tinker-cookbook — GitHub](https://github.com/thinking-machines-lab/tinker-cookbook)
