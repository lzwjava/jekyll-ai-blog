---
audio: false
generated: true
image: false
lang: en
layout: post
title: AlphaFold Refutes the Bitter Lesson
translated: false
type: note
---

**Question:** Explain this article about John Jumper's retrospective on AlphaFold and his rejection of "the bitter lesson."

**Answer:**

This is a Chinese tech article summarizing a [Machine Learning Street Talk interview](https://www.youtube.com/watch?v=e3gBwLWAerw) with **John Jumper** (AlphaFold co-creator, 2024 Nobel laureate in Chemistry, now at Anthropic). The core thesis is contrarian: **AlphaFold's success was NOT a vindication of brute-force scaling — it was a refutation of the bitter lesson.**

## The problem AlphaFold solved

A protein starts as a 1D chain of amino acids (20 "letters") that self-assembles into a unique 3D shape, and that shape determines function. Jumper's analogy: an IKEA bookshelf that assembles itself the moment you open the box. Historically you got structures by crystallizing the protein and blasting it with synchrotron X-rays — years of work per structure. After decades, humanity had only ~200K structures (~140K when AlphaFold started).

AlphaFold's three breakthroughs: **accuracy** to ~atomic-radius error (rivaling experiment), **speed** from a year to 5–10 minutes, and **scale** — ~200M structures predicted, covering essentially every sequenced organism, released free.

## The Midnolin example (structure ≠ biology)

His point: having a structure is just the start. A study on protein recycling found ~hundreds of genes shut off during development, traced to a barely-studied protein, **Midnolin**, with no known mechanism. They ran AlphaFold jointly on Midnolin + ~500 affected proteins; ~40% showed a distinctive motif — the target protein pinned between two parts of Midnolin like pliers. Lab validation: delete the predicted binding site → degradation stops. 9/10 perfect; the 10th only partially weakened, so they rechecked and found AlphaFold had identified **two** binding sites. Remove both → degradation fully stops.

His framing of AlphaFold's value — the "$10,000 screw" story: turning the right screw costs $0.50; *knowing which screw* is worth the other $9,999.50. AlphaFold's value is its **narrowness** — it precisely predicts "what an experiment would show," then hands that machine to researchers. It deliberately isn't a general cell model.

## The anti-bitter-lesson argument (the technical core)

This is the part most relevant to you. Jumper traces the architecture evolution:

- **AlphaFold 1**: off-the-shelf CV CNN with protein-specific handling bolted on as an outer patch.
- **AlphaFold 2**: a science-first architecture built from scratch for folding. The **EvoFormer** backbone exploits that proteins evolve slowly (human proteins resemble yeast/E. coli ones), so you pull hundreds of evolutionarily-related sequences and bridge "geometric reasoning" and "evolutionary reasoning." This backbone = >90% of compute AND >90% of accuracy. Then the structure module — the "geometric engine" — with **IPA (Invariant Point Attention)** and the decisive **FAPE (Frame-Aligned Point Error)** loss.

The crowd attributed AF2's win to **SE(3) equivariance / geometric deep learning**. Jumper ran ablations and found: AF2 beats AF1 by ~30 GDT points; **removing invariance/equivariance costs only ~2–2.5 points.** He calls himself "an extremely cold empiricist." People kept worshipping equivariance and ignoring FAPE, which actually mattered. His view: global SE(3) symmetry is a weak, messy symmetry — nothing like the *permutation invariance over residues*, and it doesn't carry the law-deriving power symmetry has in physics.

More ablations: deleting all conv layers (mixing axial attention + conv in the pair stack) *improved* accuracy and reduced params; swapping raw MSA for pair correlations cost only 1–2 points. Interpretability showed most model capacity goes into **geometric refinement** — after the first few layers it's a "geometry engine," not an "evolution engine." These insights flowed into **AlphaFold 3**, which slashed EvoFormer depth for a simplified **Pairformer** and got *better*.

**The punchline against the bitter lesson:** AF2's custom architectural/training innovations bought a **~100× data-efficiency gain** — the AlQuraishi lab retrained AF2 on ~1% of the PDB (~1,500 structures) and *still beat AF1*. Architecture research isn't dead; it's a force multiplier on data.

## AlphaFold 3 ≠ "just a diffusion model"

Jumper resists the label the same way he resists "it's a Transformer so it works." AF3's real leap: from single proteins to ligands/lipids/drugs (small molecules, ~20–50 atoms) — answering "*where* does this drug bind," which AF2 couldn't.

The diffusion here is **unlike image diffusion**. AF3 has a huge run-once backbone (not diffusion) that likely *decides the structure*; diffusion plays the old structure-module role — a geometry engine taking precise constraints and solving micro-detail. Image diffusion generates color blobs first and assigns meaning late (you can re-run and reinterpret). Proteins are the opposite: the **large-scale macro structure is the hardest part**. AF2 worked *condensatively* (easy local fragments first, assemble up); AF3's diffusion must cross the "how do two proteins dock, what's the relative backbone position" threshold *first* via the backbone + first forward pass, then diffusion just samples remaining details. So despite being technically diffusion, its logic is closer to AF2.

## The deeper framing: prediction / control / understanding

Three things people conflate:

- **Prediction**: what value will appear on my instrument if I do X.
- **Control**: I want the measured value to be 17 — how do I intervene.
- **Understanding**: like prediction but with a human in the loop — you hold few facts, can predict, and can transmit it compactly to another human.

Machines give us prediction and control; **understanding still must be derived by humans.** AlphaFold's charm: the algorithm it ultimately learned is one we *can* understand and state in a few words — **continuous geometric refinement.**

His "two algorithms" point (relevant to your training work): there's the algorithm *you write* and the algorithm *you end up training*. ML is code meeting data, condensing into weights — the long debate is how much of the final skill is the code vs. the data in the weights.

## On AGI / representations

Jumper's closing, characteristically restrained: explicitly *specifying* representations matters far less than people thought 5 years ago. ML long indulged the temptation to hand-design a unit to name a concept and force disentangled intermediate representations — but many things once thought essential to "intelligence" emerge just from predicting the next token well. His line:

> They emerge not because you predict the next token, but because you push next-token prediction to the extreme.

The cost is the log-linear scaling relationship — exponential compute/data for linear capability gains. His open question: we *get* these representations, but how do we get them **cheaper**? Today we scaffold models externally (memory, goal reminders for agents); we don't yet know how to **distill** those external crutches back *into* the network so it doesn't need the scaffold.

The article's ending note: a system that just cracked a 50-year problem and earned its creator a Nobel — yet that creator refuses to deify it. Equivariance isn't magic, diffusion isn't magic, "understanding" itself remains unsolved. What Jumper cares about is the unglamorous grunt work, and the gap from prediction → control → human-built understanding.

**References:**

- [Machine Learning Street Talk — John Jumper interview](https://www.youtube.com/watch?v=e3gBwLWAerw)
