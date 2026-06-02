---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Critiques of Backpropagation in Neural Networks
translated: false
type: note
---

Question: What are some unpopular or controversial opinions about backpropagation in neural networks?

Answer:

Here are several genuinely unpopular or minority opinions about backpropagation (backprop) that you’ll rarely hear praised in mainstream deep-learning circles:

- **Backpropagation is biologically implausible and holding neuroscience-inspired AI back**
  Most neuroscientists and some ML researchers (e.g., Geoffrey Hinton in recent years, David Marr’s heirs, Tai Sing Lee, Blake Richards) argue that backprop is nothing like what brains do: no symmetric feedback weights, no locked forward/backward phases, no global error signal transported backward. The unpopular take is that continuing to rely on backprop is wasting time and we should abandon it entirely for local, Hebbian, or predictive-coding-style learning rules.

- **Backpropagation is a dead end for scaling laws and AGI**
  A growing minority (François Chollet, some people in the “bitter lesson” counter-movement) claim that the spectacular gains we’ve seen since 2012 are mostly from scale + data, not from backprop being magically good. If we switched to evolution strategies, random search, or hypernetwork weight generation, or synthetic gradients at sufficient scale, we would get similar or better results with less headache (credit assignment vanishing/exploding, etc.).

- **The credit-assignment justification for backprop is overrated**
  Some researchers (e.g., Timothy Lillicrap with “sign symmetry” or “feedback alignment, Subutai Ahmad at Numenta) argue that you don’t actually need precise gradients—random feedback weights, sign-sign agreement, or even zero feedback often work almost as well. The unpopular conclusion: the chain-rule derivative part of backprop is mostly theater; the real magic is just “nudging layers in vaguely the right direction.”

- **Backprop makes models brittle and non-robust on purpose**
  Critics like Ali Rahimi (“alchemy” talk), Chris Olah’s circuits thread skeptics, and adversarial-example researchers sometimes claim that backprop’s extreme efficiency at minimizing loss on i.i.d. data necessarily produces sharp minima and overconfidence. Alternatives (Bayesian methods, energy-based models, diffusion) that don’t use backprop are inherently more robust.

- **We could replace backprop with forward-only methods and lose almost nothing**
  Extreme version promoted by Max Welling (forward-forward algorithm), Hinton again recently, and some equilibrium-prop papers: train two forward passes (positive and negative phase) instead of forward+backward. The unpopular claim is that classic backprop will look like “using a crane to move a pebble” in ten years.

- **Backprop is the reason we have no continual/learning-to-learn abilities**
  Strong opinion in lifelong-learning community (e.g., German I. Parisi, Vincenzo Lomonaco): catastrophic forgetting is baked into backprop because it globally overwrites weights with SGD. Local learning rules or explicit memory replay are the only real solution, not more backprop tricks (EWC, SI, etc.).

These opinions are definitely minority views—most practitioners love backprop because it just works and is insanely efficient on GPUs—but they are held by respected researchers and are gaining more traction as the field starts questioning whether the 1986 recipe can carry us all the way to AGI.

References:
- [Geoffrey Hinton’s Forward-Forward Algorithm (2022)](https://www.cs.toronto.edu/~hinton/FFA13.pdf)
- [Feedback Alignment works almost as well as backprop (Lillicrap et al., 2016)](https://www.nature.com/articles/ncomms13276)
- [Chollet’s “On the Measure of Intelligence” (2020) critiquing pure scaling](https://arxiv.org/abs/1911.01547)
- [Rahimi’s “Test of Time” NIPS 2017 talk (“Machine Learning has become Alchemy”)] (https://www.youtube.com/watch?v=Qi1Yry33eDU)
