---
audio: false
generated: true
image: false
lang: en
layout: post
title: Act as Agent's Remote Hands
translated: false
type: note
---

Question: For software bugs, agents like Claude Code can read the source directly, so a terse prompt works. For hardware/mechanical/daily-life issues, is the better approach to fully describe what happened (完整描述事情经过) and write a careful prompt, since the bot can't inspect anything itself?

Answer: Yes — and the reason is a first-principles one about **what tool the agent has access to**.

**Software case**: the agent has a read/write tool onto the exact state that's broken (the repo). It can `grep`, run the binary, check stack traces, bisect commits. Your prompt just needs to point it at the right entry point — the agent closes the information gap itself through iteration (read file → hypothesis → test → repeat). Low prompt cost per iteration, so front-loading isn't necessary.

**Hardware/mechanical/daily-life case**: the LLM has zero sensors. It cannot query dmesg on your fridge, can't measure voltage on your motherboard, can't see the crack in your bike frame. You are its only I/O device. That changes the optimal prompting strategy in two ways:

1. **Front-load everything measurable, in one shot** — because each round-trip costs you a real-world action (unscrew something, take a multimeter reading, wait for the noise to happen again), not a cheap tool call. So: symptom, exact timeline, environment (temp, humidity, load), what changed right before, error codes/photos/sounds, what you already tried and what happened when you tried it.

2. **But it should still be a diagnostic loop, not one giant prompt-and-pray** — the pattern isn't "write the perfect prompt once," it's "act as the agent's remote hands." Structure it like:
   - You give symptoms
   - Bot proposes 2-3 hypotheses ranked by likelihood + one cheap test to discriminate between them
   - You run that one test, report result
   - Repeat

This mirrors an actual diagnostic decision tree (like a mechanic or doctor), not a single retrieval query. The mistake people make is either (a) dumping everything and expecting one final answer with no follow-up, or (b) giving one vague symptom ("my laptop is slow") and expecting magic — both waste turns because the bot either drowns in irrelevant detail or has to ask 5 clarifying questions to even start.

Practical prompt template for hardware/physical issues:

```
Device/system: <exact model, e.g. "MacBook Pro M3 Max 2024">
Symptom: <precise, e.g. "fan spins at 100% within 30s of wake from sleep">
Timeline: <when it started, what changed>
Environment: <ambient temp, power source, load>
Already tried: <action -> result, for each>
Error codes/logs/photos: <paste raw, don't paraphrase>
Ask: give me the 2 most likely causes ranked, and the cheapest test to distinguish them
```

That last line is the key difference from a software prompt — you're explicitly asking for the *next physical action*, because the bot can't take it for you.

References:
- [Karpathy on LLMs as reasoning engines needing tool access](https://karpathy.ai)
- [Claude Code docs — agentic tool use](https://docs.claude.com/en/docs/claude-code)
