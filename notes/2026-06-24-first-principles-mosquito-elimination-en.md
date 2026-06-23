---
audio: false
generated: true
image: false
lang: en
layout: post
title: First-principles mosquito elimination
translated: false
type: note
---

**Question:** How would Yin Wang (王垠) approach a new research project: eliminating all mosquitoes in the house (not one left) and maintaining a mosquito-free state permanently?

**Answer:**

Yin Wang is famous for first-principles thinking, contrarianism toward accepted wisdom, and deep skepticism of "industry consensus." He'd approach this like he approaches programming language theory — strip away the conventional solutions, identify root causes, and derive an elegant minimal system.

Here's how I'd model his reasoning:

---

## Phase 1: Root Cause Analysis (not symptom treatment)

王垠 would immediately reject the standard approach (spray insecticide everywhere, buy a plug-in repeller, hang sticky traps). He'd say: **these are patches, not solutions.** They treat symptoms, not causes.

First-principles question: **Why are mosquitoes in the house at all?**

- Entry points: gaps in windows, doors, plumbing penetrations
- Breeding sites: standing water — plant saucers, AC drain pans, bathroom drain traps
- Attractants: CO₂, body heat, sweat, light at night near open gaps

He'd build a **causal graph** before touching any tool.

---

## Phase 2: Close the System (the 王垠 "type safety" move)

Just as he'd say a type-safe language prevents entire classes of bugs at compile time, he'd say: **seal the house so mosquitoes cannot enter.** Runtime bug-fixing (swatting) is for people who don't understand the system.

Concrete actions:
- Audit every penetration: windows → 20-mesh or finer screens, door sweeps, pipe gaps sealed with silicone
- Positive pressure HVAC: house maintained at slight positive pressure relative to outside → air flows *out*, insects can't drift *in*
- Eliminate *all* standing water within 50m (breeding radius for *Aedes albopictus* is ~50–100m)

This is the **static analysis** phase — make bad states unrepresentable.

---

## Phase 3: Eliminate the Existing Population (bounded problem)

Once the system is sealed, you have a **finite, non-replenishing population** inside. Now elimination is tractable.

His chosen tool would be **CO₂ traps** — he'd appreciate the elegance:
- Mimics a human host (CO₂ + warmth + octenol)
- No chemicals, no human intervention after setup
- Runs continuously, captures and kills

Recommended: **Mosquito Magnet** or similar propane/CO₂ lure trap placed strategically.

He'd probably also appreciate **ultrasonic + UV photocatalytic traps** as a secondary layer — not because he believes the marketing, but because he'd verify the mechanism himself (UV attracts, fan captures).

---

## Phase 4: Maintenance = Invariant Preservation

王垠 would define a **system invariant**: *zero standing water, zero entry points, trap running.*

He'd write a checklist (he's methodical) and check it weekly:
```
[ ] AC drain pan dry or flowing freely
[ ] All plant saucers empty
[ ] Window screens intact (no tears)
[ ] CO₂ trap CO₂ supply sufficient
[ ] No new gaps (after construction/repairs)
```

This is the equivalent of a CI pipeline — the invariant must hold at all times, not just at setup.

---

## What He Would NOT Do

- Insecticide sprays → "you're poisoning yourself and your family, not solving the problem"
- Mosquito coils → same objection, plus they don't scale
- Hiring pest control → "you're outsourcing your thinking to people who don't understand the system"
- Smart mosquito devices with apps → he'd call this marketing nonsense
- Any solution that requires ongoing manual effort per-mosquito → O(n) per bug is unacceptable when O(1) system design exists

---

## His Likely One-Liner Summary

> "蚊子进不来，就不需要消灭蚊子。这道题的前提本身就错了。"
> *(If mosquitoes can't get in, you don't need to eliminate them. The premise of the question is wrong.)*

Classic 王垠 — reject the framing, solve the meta-problem.

---

## Actual Practical Stack (what works in Guangzhou climate)

| Layer | Tool | Why |
|---|---|---|
| Entry sealing | 20-mesh fiberglass screens + door sweeps | Structural, permanent |
| Breeding elimination | Remove all standing water, treat drains with Bti (*Bacillus thuringiensis israelensis*) | Biological, non-toxic |
| Active capture | CO₂ lure trap (outdoor, near entry) | Intercepts before entry |
| Indoor backup | UV + photocatalytic trap | Catches stragglers |
| Monitoring | Weekly checklist | Invariant verification |

Bti is particularly elegant — it's a soil bacterium toxic only to mosquito larvae, used in organic farming. 王垠 would approve: targeted, no side effects, elegant mechanism.
