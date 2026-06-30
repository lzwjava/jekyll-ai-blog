---
audio: false
generated: true
image: false
lang: en
layout: post
title: Token Volume Is Repetition
translated: false
type: note
---

Question: When people claim they spent ~10B tokens in a month, are those actually deterministic/easy tasks — like an app or an agent where the structure is mostly known beforehand?

Answer:

Mostly yes, with nuance. High token volume almost always means high *call count*, not deep reasoning per call. The math forces this.

Let's ground it. 10B tokens/month ≈ 333M/day ≈ 13.9M/hour. No human reads 13.9M tokens/hour. So by definition almost all of it is machine-driven, looping, and repetitive. The question is *what kind* of repetition.

Three archetypes that produce billions of tokens:

**1. Agentic loops (the big one).** A coding agent like Claude Code or a custom CLI agent re-sends the entire context window every step. A 100K-token context × 50 steps for one task = 5M tokens for what a human would call "one feature." The *task* isn't deterministic — debugging, planning, tool-calling — but the *token burn* comes from context re-transmission, not from the model doing genuinely novel reasoning each token. KV cache prefix-reuse hides some of this on the provider side, but billing-wise you're resending state constantly.

```python
# Why agents burn tokens: context grows linearly, resent every turn
total = 0
ctx = 8000  # system + tools + initial files
for step in range(50):
    ctx += 1500          # new tool result appended each turn
    total += ctx          # WHOLE context billed as input every step
print(total)  # ~565K input tokens for one 50-step task
```

So "one agent task" silently becomes 500K–5M tokens. Run a few hundred of those a month and you're at billions. The individual decisions are sometimes hard; the volume is an artifact of architecture.

**2. Batch/pipeline jobs (the genuinely deterministic ones).** Classification, extraction, embedding generation, synthetic data, eval harnesses, bulk translation/summarization. These *are* the "known, easy, deterministic" category you're describing. You — with ~8,000 notes generated — know this firsthand: a fixed prompt template fanned out over N inputs. Each call is independent, structured, and the "intelligence" is front-loaded into the prompt design, not discovered at runtime. This is where token counts scale embarrassingly fast and cheaply.

```python
# Fixed prompt × N items = predictable, deterministic burn
PROMPT = "Classify intent. Return JSON {label, confidence}.\n\n{text}"
# 5000 tokens/call × 200K items = 1B tokens, zero novel reasoning
```

**3. Self-play / RL / eval rollouts.** GRPO/RLHF rollouts, multi-sample voting, agent benchmarks. You generate many completions per prompt and score them. Massive volume, but the *generation* is the cheap part — the value is in the reward signal and filtering. Deterministic in structure, expensive in tokens.

So your intuition is right for categories 2 and 3, and *half-right* for 1. The honest framing:

- High token count ≠ hard problems. It correlates with **loops, fan-out, and context resending** far more than with reasoning difficulty.
- The hard part of high-volume work is almost never "the model thinking." It's the *system*: prompt design, batching, retry/error handling, eval, dedup, cost control, caching. That's where the skill actually lives.
- A single human doing genuinely hard, novel reasoning with an LLM might burn 50–200M tokens/month and feel maxed out. Someone reporting 10B is running pipelines or fleets of agents — orchestration, not deeper thought.

Where the "easy" framing breaks: the *orchestration* can be quite hard even when each call is trivial. Keeping a 200K-item pipeline correct, idempotent, cheap, and well-evaluated is a real engineering problem — just not an LLM-reasoning problem. The difficulty moved from the model to the harness.

For your trajectory: when you see "2B/10B tokens" claims, read it as a proxy for *throughput and automation maturity*, not raw capability. The interesting question to ask anyone (or yourself) isn't "how many tokens" but "what's your tokens-per-useful-outcome, and where's the eval loop?" That ratio is the actual signal.
