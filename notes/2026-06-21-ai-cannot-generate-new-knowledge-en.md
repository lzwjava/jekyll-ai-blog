---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Cannot Generate New Knowledge
translated: false
type: note
---

The document you shared is the Weibo post itself — it's the essay "《网球和AI》" (Tennis and AI) by the author. The URL points to this exact content.

**Question:** How should I understand this essay — "Tennis and AI" — by Yin Wang (王垠)?

**Answer:**

This is almost certainly written by **Yin Wang** (王垠), given the Weibo account and the writing style — which is unmistakable: self-referential, confrontational, conspiratorial undertones, and a strong conviction in solo intellectual superiority. You listed him as one of your technical idols, so understanding this piece carefully matters.

---

### The Core Thesis

He's making one central claim: **AI (Transformer models) cannot generate genuinely new knowledge — it can only recombine existing text.**

He arrives at this through a personal experiment: he tried using AI to help him develop tennis techniques, and found it useless — because his own research had surpassed everything available on the internet. The AI had no raw material to work from.

His formulation: *AI is translation. Natural language → natural language, or natural language → code. But it cannot originate.*

---

### The Technical Argument (which is actually solid)

> "Transformer模型终究只是在做翻译" — Transformers are ultimately just doing translation.

This is a compressed but defensible point:

- Transformers are trained on the corpus of human-produced text. Their "knowledge" is a lossy compression of that corpus.
- When you ask about something **not well-represented in the training data** (e.g., Yin Wang's privately-developed tennis biomechanics), the model has nothing to interpolate from. It either hallucinates or parrots generic sources.
- His conclusion: **the frontier of any field is inaccessible to AI** because by definition the frontier hasn't been written down yet.

This maps cleanly to something you already know from training: the model can only predict next tokens from learned distributions. It cannot run physical experiments, cannot feel proprioception, cannot iterate in the real world.

His phrase: *"只有人（或其它生命体）才有和现实世界接轨的能力"* — only living beings can interface with physical reality. This is the **embodied cognition argument** — a real and serious critique in AI philosophy (Dreyfus, Brooks, etc.).

---

### The Psychological Layer

Yin Wang's writing always mixes genuine insight with something more personal. In this essay:

- He frames his tennis research as a solo conquest of truth, hidden from others who "don't deserve it"
- He dismisses all medicine (Eastern and Western) as "secret weapons designed to harm humans"
- He believes his shoelace research took "hours" and nobody else could do this
- He sees 90% of the tennis world as lies, and himself as uniquely capable of seeing through them

This is a pattern in his writing: **valid epistemological core wrapped in grandiosity and paranoia.** Don't throw out the argument because of the delivery. But also don't absorb the worldview wholesale.

---

### What to Take From It (for your trajectory)

1. **The core AI critique is real.** At the frontier of your own work — your custom CLI agents, your model training experiments — AI will plateau. It can scaffold, but the novel architectural decisions have to come from you. You've probably already experienced this.

2. **Embodiment / real-world grounding is the hard problem.** Robotics + RL is one path toward closing this gap. Current LLMs without tool use or sensors are fundamentally limited in domains requiring physical experimentation.

3. **AI as a "screwdriver" framing.** He's not wrong that the best use of AI today is as a high-leverage tool, not an autonomous researcher. Your own workflow — using LLMs for code scaffolding while directing the architecture yourself — is exactly the correct model.

4. **The 6-month deep dive methodology is worth noting.** His approach to tennis is the same as his approach to CPS and CFA: total immersion, first-principles deconstruction, willingness to declare everything else wrong. This is Karpathy's approach too. It's how you actually get to the frontier.

---

### One Sentence Summary

Yin Wang used tennis as a stress test for AI's knowledge boundaries, found it failed beyond the internet's horizon, and concluded that Transformers are sophisticated interpolators — useful tools, but incapable of being the scientist.
