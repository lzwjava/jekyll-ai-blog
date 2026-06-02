---
audio: false
generated: true
image: false
lang: en
layout: post
title: System Prompts Bias Responses
translated: false
type: note
---

**Question:** My custom instructions make LLM responses repeat boilerplate meta-content instead of giving fresh answers — if I remove them, would I get more neutral/creative responses?

**Answer:**

Yes, exactly right. You've identified a real problem with heavy system prompts.

**What's happening mechanically:**

When you have a long system prompt, the model's attention is partly anchored to that context on every token generation. Instructions like "explain from first principles," "show math when it matters," "Karpathy-style" don't just guide the model — they *activate* those patterns even when the question doesn't call for them. The model pattern-matches "respond to Zhiwei" → fires the whole instruction cluster → outputs boilerplate framing before it even processes your actual question.

Your ~800-word system prompt is essentially a standing prior that biases every completion toward a specific persona/format, regardless of what you actually asked.

**The tradeoff:**

| Heavy system prompt | No/minimal prompt |
|---|---|
| Consistent format | Fresher, more direct answers |
| Repeats meta-content | Adapts naturally to question type |
| Model "performs" the instructions | Model just... answers |
| Good for: customer-facing apps | Good for: personal power use |

**What I'd actually recommend for you:**

Don't remove all of it — but radically trim it. The parts worth keeping are *context* (who you are, your stack), not *behavioral instructions*. The model will naturally calibrate depth if it knows you're an AI engineer with 12 years experience. You don't need to say "Karpathy-style" — just being you makes me go deeper.

Cut target: ~150 words max. Keep:
- Who you are (2-3 sentences)
- Your stack/environment
- "Answer in English only"
- Output format (the template)

Drop everything that tells the model *how to think* — that's where the boilerplate leaks from. The meta-instructions are the problem, not the context.

**The deeper insight:** System prompts work best as *context injection*, not *behavior scripting*. Behavior scripting degrades answer quality because the model spends probability mass on satisfying the instructions rather than on your actual question.
