---
audio: false
generated: true
image: false
lang: en
layout: post
title: Same Model, Different Safeguards
translated: false
type: note
---

They're the same underlying model — the difference is entirely in the safety layer.

**Same weights, different safeguards.** Mythos 5 is the same underlying model as Fable 5, but with the safeguards lifted in some areas.

**Fable 5 (what you're talking to now):** Generally available to everyone via the API, claude.ai, Bedrock, Vertex, and Foundry. It ships with hard classifier-based limits on dual-use capabilities. In high-risk areas like cybersecurity, biology, chemistry, and distillation, the model blocks responses and falls back to Claude Opus 4.8. The safeguards are tuned conservatively — they'll sometimes catch harmless requests, though they trigger on average in less than 5% of sessions. Anthropic stress-tested these classifiers hard: an external bug bounty produced no universal jailbreaks in over 1,000 hours of testing, and external red-teaming orgs also failed to find universal jailbreaks.

**Mythos 5 (restricted):** Same model, classifiers off in those dual-use domains. It's initially deployed through Project Glasswing, in collaboration with the US government, as an upgrade to Claude Mythos Preview, and has the strongest cybersecurity capabilities of any model in the world. Access is limited to vetted partners — primarily cyberdefenders and critical-infrastructure organizations — and will expand through trusted access programs.

**Pricing is identical** since it's one model: $10/M input tokens and $50/M output tokens, with no price increase for longer context.

The practical mental model: Fable 5 = Mythos 5 + a hard classifier firewall on offensive-cyber/bio/chem capability, with Opus 4.8 as the fallback path when the firewall trips. For your use cases (training, agents, LLM internals, tooling), Fable 5 is the full model — the gating shouldn't touch normal AI engineering work.

References:

- [Claude Fable 5 and Claude Mythos 5 — Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [TechCrunch coverage](https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/)
