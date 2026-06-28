---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Weights vs Open Source
translated: false
type: note
---

You're right on the substance, and the distinction you're drawing is the one that matters.

The "you can't see inside the model" framing conflates two different things:

**Open weights** — you get the trained parameters. You can run it locally, inspect activations, probe it, fine-tune it, quantize it. GLM, Llama, Qwen, DeepSeek, etc. You literally *can* see "inside" in the mechanistic sense — every weight, every attention head, the full forward pass. Claude's weights you cannot see; that part of Dario's claim holds only for closed models like Claude itself.

**Open source (full)** — weights *plus* the training data, data-mixing/curation pipeline, training code, and recipe. This is what lets you actually reproduce and understand *why* the model is the way it is. Nemotron (NVIDIA released training data + recipes), OLMo (AI2, fully open including dolma dataset + training logs), and Pythia are the canonical examples. This is the real analogue to "seeing the source."

So the precise rebuttal to the open-source-vs-open-weights gotcha:

- Open weights ≠ open source — the OSI even published a formal Open Source AI Definition (OSAID) in late 2024 partly to police exactly this. Most "open" models (Llama, GLM) are weights-available, often under non-OSI licenses with use restrictions.
- But "you can't see inside the model" is still wrong for any open-weights model. The weights *are* the model. Interpretability research (SAEs, probing, activation patching) runs on exactly these. Closedness is about access, not some inherent opacity.
- The fully-reproducible tier (OLMo, Nemotron data releases, Pythia) is where "see the source" becomes literal — you can rerun the pipeline and get a comparable model.

The cleaner way to put it: closed models hide the artifact, open-weights models hide the *production process* but expose the artifact, and fully-open models expose both. Dario's analogy fails because for open weights the "binary" and the "running internals" are both fully available — what's missing is the build system, not the source-you-can-inspect.

One caveat worth noting: even with full weights + data + code, "understanding" the model is still bounded by interpretability being unsolved — you can see every weight and still not know what a given circuit computes. So "see the source" in the software sense (readable, intentional logic) never fully transfers to neural nets regardless of openness. That's a fair point *neither* side usually makes.
