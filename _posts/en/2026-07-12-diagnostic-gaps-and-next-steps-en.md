---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnostic Gaps and Next Steps
translated: false
type: note
---

Question: Analyze the diagnostic conversation so far — the full reasoning chain, what's actually confirmed vs. what's assumed, and what that means for next steps.

Answer:

## Reconstructing the chain

| Step | Claim | Evidence type | Confidence |
|---|---|---|---|
| 1 | Not GPU | Direct swap test (AMD↔Nvidia) + removal test | **High** — two independent controlled experiments, both negative |
| 2 | Not fan/mechanical contact | Friend's suggestion → you moved on to "it's the motherboard" | **Unverified** — you never reported back on the actual eraser/visual/hand-spin check |
| 3 | It's the motherboard | Self-reported, method not stated | **Medium-low** — I explained *why* it's plausible, but I never confirmed *how* you determined this |
| 4 | It's "coil whine" specifically | My own framing, carried over from the PSU discussion | **Weakened** — see below |

Step 3 is the load-bearing claim in the whole conversation, and it's the one with the least rigor behind it. When you said "actually it is the motherboard," I jumped straight to explaining plausibility (VRM under 13900KF load, budget board tier, MSI Mortar forum reports) instead of asking how you localized it. That's a gap in my own reasoning, not yours — I should have asked whether you did a proximity test (ear near VRM heatsink vs. near PSU vs. near GPU slot), the pencil-eraser damping test, or something else. Those produce very different confidence levels:

```
localization_method = ?

if method == "proximity listening (moved ear around case)":
    confidence = MEDIUM   # case can resonate, sound travels along the chassis,
                           # false positives are common (see the AM5 thread I cited,
                           # where someone was sure it was "from the mobo" purely by ear)
elif method == "pencil eraser damping test on VRM inductors":
    confidence = HIGH      # direct mechanical confirmation
elif method == "swapped motherboard, noise persisted/disappeared":
    confidence = VERY_HIGH # same isolation logic as your GPU test
elif method == "just seemed obvious / process of elimination by exclusion":
    confidence = LOW       # exclusion of GPU + fan doesn't logically imply mobo;
                           # PSU is still untested and was never eliminated
```

That last branch matters: **you ruled out GPU and (implicitly) fan contact, but you never actually ruled out the PSU.** "Not GPU, not fan" → "therefore motherboard" skips a candidate. Unless you did a real isolation test on the PSU (the paperclip/external-load test from my first answer), the PSU is still mathematically in the running alongside the motherboard VRM.

## Why the terminology detour matters retroactively

This is the more interesting analytical point. When you asked "what does whine mean," it forced a distinction I'd been glossing over: **coil whine is a clean, high-pitched tonal sound; 滋滋 is closer to buzz/crackle — a lower, textured, electrical-sounding noise.**

That's not a cosmetic detail — it changes the hypothesis space:

- If it were a clean whine → near-certainly an inductor vibrating at its switching frequency (GPU/PSU/VRM), textbook case
- If it's genuinely a grainy buzz/crackle (滋滋) → still *could* be coil whine (case resonance can add texture to a pure tone, so don't over-update), but it also opens up:
  - A marginal/failing capacitor (electrolytic caps can produce a crackling sound as they degrade, distinct from inductor whine)
  - A loose connector or header making intermittent contact under vibration (a "buzz" more than a "whine")
  - Two separate switching frequencies beating against each other (VRM + PSU both active, slightly different switching rates → audible beat frequency, sounds textured/buzzy rather than a pure tone)

I stated the PSU (CX650F) recommendation in my first answer *before* this terminology distinction came up. In hindsight, that recommendation was reasonable given the evidence at the time, but it was built on an assumption (clean coil whine) that your own word choice doesn't cleanly support. Worth flagging rather than quietly carrying forward.

## Updated hypothesis ranking

Given all of the above, here's where I'd actually put confidence right now, low to high effort-to-verify:

1. **Motherboard VRM (coil whine or texture-added-by-case-resonance)** — plausible, matches budget-board-under-13900KF-load story, but *not independently confirmed* — only asserted
2. **PSU (CX650F)** — never actually eliminated; has documented history for this exact symptom class; untested in this conversation
3. **Beating frequency between MB VRM + PSU switching, both contributing** — would explain a "buzzy" rather than "pure tone" character, and would also explain why pressing on just the mobo VRM might only partially change the sound
4. **Component-level defect (capacitor/connector)** — lower prior, but not ruled out

## The one test that would actually collapse this

Everything so far has been correlational (GPU swap) or anecdotal (mobo "seems like" the source). The decisive test is the same isolation logic you already used successfully on the GPU, applied to the remaining two candidates:

```bash
# Definitive test — same rigor as your original GPU swap test:

# Step A: swap ONLY the motherboard (borrow one, or if you have the
#         old board from a previous rig, drop CPU/RAM/PSU onto it)
#   - noise persists  → NOT the motherboard, it's PSU or elsewhere
#   - noise disappears → CONFIRMED motherboard

# Step B (cheaper, do this first): swap ONLY the PSU
#   - borrow literally any other ATX PSU with enough wattage, even underpowered,
#     just for a 2-minute boot test
#   - noise persists  → NOT the PSU → strengthens motherboard hypothesis
#   - noise disappears → CONFIRMED PSU, motherboard was a red herring
```

Step B is strictly cheaper than Step A (PSUs are easier to swap than motherboards — no reseating CPU/cooler/RAM), so do it first. This gives you the same class of evidence you already have for the GPU — a controlled swap, not an inference from listening position.

## Bottom line

Your GPU elimination was rigorous. Everything after that (fan check, motherboard conclusion) has been faster and less rigorous, which is fine for a first pass but shouldn't be treated as equally confirmed. If you run the PSU swap test and it comes back negative (noise persists), then I'd upgrade my confidence in "motherboard VRM" from medium to high, and the earlier BIOS-tuning suggestions (C-states, LLC, VRM switching frequency) become the right next move. If you haven't done the fan/pencil tests yet either, doing all three swaps (fan check, PSU swap, mobo swap) in one sitting would let you nail this down with actual evidence rather than the current best-guess narrowing — worth knowing whether you've already done the PSU-swap-equivalent test and just didn't mention it, since that would change how much more digging is actually needed here.
