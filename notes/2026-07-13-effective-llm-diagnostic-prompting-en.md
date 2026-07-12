---
audio: false
generated: true
image: false
lang: en
layout: post
title: Effective LLM Diagnostic Prompting
translated: false
type: note
---

Question: Aside from the specific PSU/motherboard issue — is it actually important to fully describe what happened and write a good prompt before asking an LLM to diagnose something like this?

Answer: Yes, and here's the concrete mechanism why, not just "good practice" hand-waving.

**Why it matters specifically for hardware diagnosis:**

LLM diagnostic output is pattern completion over your input, not a lookup against your actual device. Two failure modes stack on top of each other when the prompt is thin:

1. **Under-specified prompt → interpolation across many possible causes.** "Motherboard buzzing after connecting GPU" matches training data for: coil whine (normal), PSU overcurrent, wrong cable insertion, capacitor failure, ground loop, PSU sag under load. Without the exact sequence of events (what was plugged, in what order, when the noise started, whether it powers on at all), the model picks the most *statistically likely* narrative across all those cases — which is why you got something that "sounds reasonable" (分析出来一篇看起来有道理的) rather than something *verified* against your actual wiring.

2. **No cross-checking with ground truth → confident-sounding hallucination.** The Corsair CPU/PCIe 8-pin pinout mismatch is real and documented — same female connector shape, different pin wiring, PSU-vendor specific. But whether *that specific failure* is what happened to your board is a separate claim the model can't verify from a text description alone. It's plausible, not confirmed.

**What actually fixes this — a better prompt template:**

```
Context:
- Hardware: [exact PSU model, exact GPU model, exact motherboard model]
- Sequence: [what you plugged, in exact order, with timestamps if possible]
- Symptom: [buzzing/no post/etc — exact sound, exact timing relative to power-on]
- What you already ruled out: [reseated cable? multimeter tested? swapped PSU cable?]

Ask:
1. List possible root causes ranked by likelihood given symptom
2. For each, name the specific test that would falsify it (not "check the cable" — "measure continuity on pin X vs pin Y with multimeter, expect Y, if Z then rule out")
3. Do not conclude — only next diagnostic step
```

This turns the LLM into a checklist generator instead of a narrator producing a plausible-sounding story you can't act on.

**On your friend's skepticism** — worth taking seriously, not dismissing: "if it fits it shouldn't matter" is wrong for Corsair modular PSUs specifically because the connector is keyed identically but wired differently between CPU and PCIe rails — that's Corsair's own documented warning, not LLM speculation. GPU *can* affect the motherboard if the miswired 12V rail backfeeds into a header expecting a different pinout, especially on non-ATX-spec adapters. But "PSU compatibility is that bad" is a fair pushback too — it's not that ATX is broken, it's that *modular cables are PSU-model-specific* and Corsair explicitly says don't mix cables across PSU models/generations even from the same brand. That's a real design footgun, not implausible.

Bottom line while the board's at repair: ask the shop for the actual root cause (they'll have a scope/multimeter), don't let the LLM's "looks reasonable" narrative become your accepted diagnosis until it's confirmed against a real measurement.

References:

- [Corsair Cable Compatibility Guide](https://www.corsair.com/us/en/explorer/diy/psus/why-you-should-only-use-corsair-modular-cables-with-corsair-power-supplies/)
- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
