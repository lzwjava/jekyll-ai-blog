---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vision-Language Models' Mathematical Blind Spot
translated: false
type: note
---

Question: Are current models very strong at mathematical reasoning in text, but still struggle with mathematical constraints embedded within images?

Answer:

Yes, exactly right. This is a precise and insightful observation.

## The Gap in One Sentence

> Models can solve IMO-level text math, but fail to "see" that a triangle's angles must sum to 180° when looking at a diagram.

---

## Why Text Math Is Now Strong

- DeepSeek-R1, o3, Gemini 2.5 Pro can solve competition math (AIME, AMC) at near-human or superhuman level
- Chain-of-thought + RL post-training has pushed text math reasoning very far
- The symbolic reasoning engine is mature

---

## Why Image Math Constraints Are Still Hard

### 1. **Perception vs. Reasoning Decoupling**

The vision encoder extracts *approximate* features. It doesn't enforce:

- Geometric constraints (parallel lines, right angles, congruence)
- Algebraic constraints embedded in a figure (labeled lengths must be consistent)
- Topological relationships (which region is inside/outside)

The model **reasons correctly** given what it *thinks* it sees — but what it sees is already wrong or imprecise.

### 2. **No Formal Grounding**

Text math: `a² + b² = c²` is exact, discrete, unambiguous.
Image math: a right triangle drawn in a figure — the model must *infer* the right angle exists, and that inference can fail.

There is no hard constraint forcing the model to respect geometric consistency across the image.

### 3. **Generation Side Is Even Worse**

When generating images with math constraints:

- T2I models cannot enforce that generated angles are geometrically valid
- A "generated" equation image may look correct but have wrong symbols
- The model has no internal "math checker" during pixel generation

This is exactly MathGen's point — **visual plausibility ≠ mathematical correctness**.

### 4. **Evaluation Confirms This**

Benchmarks like:

- **MathVista** — VLMs drop significantly on geometry vs. pure algebra
- **GeoQA / Geometry3K** — models struggle with constraint-based geometric reasoning
- **We-Math** — fine-grained visual measurement is the weakest category across all tested models

---

## The Core Asymmetry

| Dimension | Status |
|---|---|
| Text math reasoning | ✅ Very strong (near-superhuman on benchmarks) |
| Math in image → understand | ⚠️ Partial — depends on clarity and type |
| Geometric/algebraic constraints in image | ❌ Still weak |
| Generating images with valid math constraints | ❌ Very weak |

---

## What Would Fix This?

The real solution likely requires:

1. **Formal geometry engines** integrated with VLMs (like a symbolic solver verifying visual outputs)
2. **Structured intermediate representations** — converting image → constraint graph → then reasoning
3. **Specialized training data** pairing images with explicit mathematical constraint annotations

Right now, models are essentially doing **pattern matching on visual math**, not **constraint satisfaction**. That is the fundamental gap you identified.
