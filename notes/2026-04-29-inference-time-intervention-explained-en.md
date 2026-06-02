---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inference-Time Intervention Explained
translated: false
type: note
---

Question: What does “ITI” mean in the context of improving instruction following with a model architecture plugin?

Answer:

In most recent LLM research contexts, **ITI usually refers to *Inference-Time Intervention***.

It’s a technique where you **modify or steer a model’s internal activations during inference (not training)** to improve behavior such as instruction following, truthfulness, safety, or style control.

### What ITI typically means (in your context)

If you are building a plugin around instruction-following optimization, ITI likely means:

**Inference-Time Intervention = controlling model behavior by intervening in hidden states at runtime**

### How it works conceptually

Instead of retraining the model, ITI methods:

* Identify internal representations (e.g., attention heads, MLP activations, residual stream)
* Detect features correlated with desired behavior (e.g., “following instructions”, “refusing”, “hallucinating”)
* Apply **additive or projection-based edits** to activations during forward pass

So the pipeline becomes:

> prompt → forward pass → intervene on activations → continue generation

### Why it helps instruction following

Instruction-following failures often come from:

* competing internal “prior habits” (pretraining bias)
* weak instruction signal propagation across layers
* shallow alignment in certain heads

ITI tries to:

* amplify instruction-relevant features
* suppress conflicting directions
* steer generation trajectory without full fine-tuning

### Related ideas (for positioning your work)

Depending on your implementation, ITI is close to:

* **Activation steering / representation engineering**
* **Logit lens / hidden state editing**
* **Control vectors (e.g., refusal/safety steering vectors)**
* **Test-time adaptation without gradient updates**

### Important distinction

* **SFT / RLHF** → changes weights permanently
* **LoRA / adapters** → adds trainable parameters
* **ITI** → *no weight change, only runtime activation manipulation*

---

If you want, you can describe your plugin design (e.g., where you inject signals—attention, residual stream, or MLP), and I can map it to known ITI-style methods or suggest improvements.
