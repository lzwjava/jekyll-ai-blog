---
audio: false
generated: true
image: false
lang: en
layout: post
title: Undercorrection and Myopia Reversal
translated: false
type: note
---

**Question:** Is the following myopia reversal theory correct? Humans are born hyperopic (far-sighted). Looking at near objects causes light to focus behind the retina, which signals the eye to elongate. Over time this causes myopia. Wearing full-prescription glasses while doing near work again pushes the focal point behind the retina, worsening myopia. Wearing -1.50D undercorrection puts the image exactly on the retina for near work. Wearing -1.75D undercorrection pushes the image in *front* of the retina, which signals the eye to shorten axially, reversing myopia. Is this right?

**Answer:**

Your model is mostly correct in mechanism, but the last step (−1.75D pushing image *in front* → axial shortening) is where the theory gets ahead of the evidence. Let me go layer by layer.

---

## The Emmetropization Framework (What You Got Right)

This is real, well-established biology called **emmetropization** — the eye's active servo loop for focal length.

```
Signal:            image behind retina → grow longer (myopic shift)
                   image in front of retina → grow shorter (hyperopic shift)
                   image ON retina → stabilize

Sensor:            retinal blur detection, primarily in peripheral retina
                   (not just foveal — this is critical)

Actuator:          scleral remodeling → axial length change
                   (choroidal thickness changes faster, hours-scale)
```

Animal models (chick, tree shrew, monkey) prove this conclusively. You can induce myopia with a minus lens, reverse it with a plus lens — axial length tracks the defocus signal faithfully. This is **not controversial**.

---

## The "Undercorrection for Near Work" Step

Your specific claim:

> Full Rx while reading → image behind retina → eye elongates → myopia worsens
> Reduced Rx (−1.50D under) → image on retina → stable
> Further reduced (−1.75D under) → image in front → eye shortens → reversal

The **first two steps** are mechanistically plausible. The **third step** has a problem.

### Why Undercorrection Doesn't Reliably Reverse (or even slow) Myopia

**Clinical RCTs say undercorrection is neutral-to-harmful:**

The COMET study and multiple Asian RCTs tested undercorrection directly. Result: undercorrection does **not** slow myopia progression — in several studies it *accelerated* it slightly.

Why? Because of **peripheral defocus**. The fovea isn't the only signal. When you undercorrect, the *peripheral* retina (which has stronger emmetropization signal weight in many models) sees hyperopic defocus → drives axial growth.

---

## What Actually Works: The Peripheral Defocus Insight

The real mechanism that **does** work in clinical practice:

| Intervention | Mechanism | Evidence |
|---|---|---|
| Orthokeratology (OK lenses) | Flattens cornea center → peripheral retina gets *myopic* defocus | ~50% slowdown, strong RCT evidence |
| Multifocal soft contacts (e.g. MiSight) | Peripheral plus power → myopic peripheral defocus | FDA-approved, ~59% slowdown |
| Atropine 0.01% | Blocks muscarinic receptors, mechanism debated | ~50-77% slowdown |
| Outdoor time (2hr/day) | Dopamine release from bright light inhibits axial growth | Epidemiological + some RCT |

The key is **peripheral retinal signal**, not foveal.

---

## Can Myopia Be *Reversed* (Axial Shortening)?

This is where your theory is most optimistic and where evidence is weakest.

**Axial shortening in adults is extremely rare.** The sclera in adults is largely non-remodeling compared to children. What changes:

- **Choroidal thickness**: Can thicken within hours under myopic defocus (measured by OCT). This is real but small (~10–20μm), transient, and doesn't represent true reversal.
- **Axial length**: In children during OK lens treatment, *slowed growth* is measurable. True *shortening* in adults — almost no robust evidence.

**The honest answer**: The emmetropization servo works well during development (childhood, teens). In adults, the sclera hardens. You can slow progression in kids significantly. You can probably stabilize. True reversal of established adult myopia via optical defocus alone — not convincingly demonstrated in humans.

---

## Your Theory vs. Reality

| Claim | Verdict |
|---|---|
| Born hyperopic, eye elongates with near work | ✅ Correct |
| Full Rx near work → image behind retina → worsens myopia | ⚠️ Plausible but oversimplified (peripheral defocus dominates) |
| −1.50D under → image on retina for near → stable | ⚠️ Foveally correct, peripherally wrong |
| −1.75D under → image in front → axial shortening | ❌ Not supported by RCT; undercorrection ≠ myopic peripheral defocus |

---

## What the Endmyopia / Jake Steiner Community Gets Wrong

This framework (which your description resembles) is popular online. The **mechanism** they describe for the eye isn't wrong. The **intervention** (print pushing, undercorrection) doesn't match what the mechanism actually requires, because:

1. They treat the eye as a fovea-only system
2. They ignore peripheral defocus geometry
3. Anecdotal "reversal" is mostly measurement noise + accommodation relaxation (ciliary muscle, not axial length)

---

## TL;DR

You have the biology right (emmetropization is real, defocus drives axial length). The intervention logic has the right intuition but wrong geometry. To actually drive axial shortening you need **myopic peripheral defocus** — which is what OK lenses and multifocal contacts engineer precisely. Simple undercorrection doesn't deliver that signal correctly. And in adults, even correct signals produce minimal axial shortening because scleral plasticity is largely gone.

**References:**

- [Flitcroft DI — The complex interactions of retinal, optical and environmental factors in myopia aetiology (2012)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3487423/)
- [COMET Group — Myopia stabilization and associated factors (2013)](https://pubmed.ncbi.nlm.nih.gov/23266438/)
- [Walline JJ et al. — MiSight 3-year myopia control (2019)](https://pubmed.ncbi.nlm.nih.gov/31233061/)
- [Cho P, Cheung SW — ROMIO orthokeratology study](https://pubmed.ncbi.nlm.nih.gov/22772737/)
- [Troilo D et al. — IMI — Report on Experimental Models of Emmetropization and Myopia (2019)](https://pubmed.ncbi.nlm.nih.gov/30817317/)
