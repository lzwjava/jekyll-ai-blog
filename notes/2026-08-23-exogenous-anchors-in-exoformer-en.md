---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exogenous Anchors in ExoFormer
translated: false
type: note
---

**Question:** What does "Exogenous" mean in the context of ExoFormer?

**Answer:**

"Exogenous" comes from Greek — *exo* (outside) + *genous* (origin) — meaning **"coming from outside the system."** Its opposite is *endogenous* (generated from within).

In ExoFormer, it refers specifically to where the **anchor projections** come from:

- **Endogenous / Internal anchor** (the old approach, called NuResFormer): the anchor is taken from the **first layer of the network itself** — a layer that already has its own job to do (compute features for the next layer). This forces the first layer to serve two conflicting roles at once.

- **Exogenous / External anchor** (ExoFormer): the anchor is produced by a **dedicated set of weight matrices that sit entirely outside the main layer stack**, projecting directly from the raw input embeddings. These weights have *one job only* — to produce a stable, high-fidelity reference signal that gets blended into every layer.

A useful analogy: imagine a building under construction. In the endogenous design, you ask one of the workers on the 1st floor to also serve as the foreman for all upper floors — he's pulled in two directions and does both jobs worse. In the exogenous design, you hire a separate site supervisor who stands outside the building, has no floors to build himself, and exists purely to give guidance to every floor. That separation is what makes the whole system work better.

In the paper's terms, this is the **Offloading Hypothesis** — by externalizing identity preservation to a dedicated external module, the internal sequential layers are freed to specialize entirely in feature transformation.
