---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transformers Are Not AGI
translated: false
type: note
---

**Question:** Is current transformer/LLM technology actually AGI, or is that hype?

**Answer:**

Current LLMs are not AGI—and calling them that conflates capability with generality in misleading ways. Here's the honest technical take:

## What transformers are actually good at

**Next-token prediction at scale.** That's it. Extremely good at it. With enough parameters, data, and compute, they learn to:

- Model language structure and encode semantic relationships
- Pattern-match across domains with some transfer capability
- Follow instructions and engage in multi-step reasoning (via in-context prompting)
- Generate plausible continuations of text distributions they've seen

This is *powerful* for text-based tasks. But it's a narrow capability dressed up as generality.

## Why it's not AGI

**Architectural limitations:**

1. **Stateless between requests** — No persistent memory, learning, or goal representation. Each chat restarts from scratch. A child learns to drive, remembers it, and improves. An LLM resets.

2. **Next-token prediction ≠ goal-directed behavior** — Transformers optimize for "what word comes next," not "achieve this objective." Planning requires explicit goal representation and causal reasoning. In-context prompting can *simulate* planning, but the model isn't actually reasoning about consequences—it's completing a pattern ("here's what planning-like text looks like").

3. **No causal intervention** — LLMs learn correlations. They can't reason counterfactually ("if I do X, then Y happens") without that exact pattern in training data. Real intelligence requires causal models.

4. **Brittleness on distribution shift** — Ask a transformer something slightly outside its training distribution and it hallucinates. Humans and animals generalize robustly. That's AGI-adjacent.

5. **Can't verify its own outputs** — A language model can't reliably tell you whether its answer is correct. It's predicting what comes next, not checking against ground truth.

6. **Learning efficiency** — Humans learn language in ~10,000 hours of exposure (~10^8 tokens). Transformers need 10^12+ tokens. That's a 10,000x inefficiency gap.

## The scaling question

Scaling laws have been remarkably predictable so far—no emergent jumps to "reasoning" or "understanding." Current observations:

- Loss scaling smoothly with compute (no phase transitions yet)
- Capability improvements correlate with dataset diversity and parameter count
- But fundamental limitations (context length, memory, causal reasoning) don't disappear with scale

Could scaling to 10^15 tokens change things? *Maybe*—but it's pure speculation. We don't have evidence that stacking more transformer blocks solves reasoning or goal-representation.

## What's actually needed for AGI

An architecture that combines:

- **Persistent memory** (not just context window)
- **Goal representation** (intrinsic objectives, not just next-token loss)
- **Causal models** (intervention, counterfactuals, planning)
- **Feedback integration** (real-time learning from outcomes, not just supervised training)
- **Grounding** (interaction with environment, verification against reality)

Current transformers have *none of these*. DeepSeek MoE and Claude Opus are incremental—better pattern matching, but no architectural shift.

## The honest framing

LLMs are:

- ✅ Remarkable at language understanding and generation
- ✅ Useful as tools (retrieval, summarization, code generation)
- ✅ Good enough to be economically significant
- ❌ Not general intelligence
- ❌ Not approaching AGI without fundamental architectural changes

Saying "current LLMs are AGI" is like saying "a really good chess engine is artificial general intelligence." It excels in one domain, but generality requires something different.

The marketing hype (OpenAI's "path to AGI," etc.) conflates "sophisticated pattern matching" with "understanding." They're not the same. Don't let investor messaging convince you otherwise.

**What should interest you:** The next architectures that *do* combine transformers with memory, causal reasoning, and goal-driven learning. That's where the real work is—and that's likely 3–5 years out at minimum, probably longer.
