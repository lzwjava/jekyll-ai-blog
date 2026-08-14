---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Justin Gilmer: Theoretical Machine Learning Researcher"
translated: false
type: note
---

Question: **Who is Justin Gilmer, the Google research scientist, and what is he known for?**

Answer:

**Justin Gilmer** is a mathematician / machine-learning researcher who has worked at **Google Brain / Google Research**, with a research background unusually close to the intersection of **theoretical mathematics, deep learning optimization, robustness, and empirical ML**.

His background is particularly interesting if you're studying neural networks from first principles.

### 1. His background

Gilmer did his PhD at **Rutgers University (2009–2015)**, focusing on **combinatorics and theoretical computer science**. His own public profile describes his mathematical specialization as **discrete mathematics, probability theory, and theoretical CS**. ([LinkedIn][1])

So he's not primarily the "build another application with transformers" type of researcher. His work often asks:

> **What is actually happening mathematically inside deep neural networks?**

That makes some of his older papers still surprisingly relevant today.

---

## 2. The paper you should absolutely know: Deep Information Propagation

One of his most important papers is:

**Deep Information Propagation** — Samuel Schoenholz, Justin Gilmer, Surya Ganguli, Jascha Sohl-Dickstein.

It appeared at ICLR 2017 and became an important foundation for understanding **signal propagation and initialization in very deep networks**. Google lists it among its ICLR 2017 research. ([Google Research][2])

The central question is roughly:

> If I repeatedly apply random nonlinear transformations, what happens to the distribution of activations and gradients as depth → ∞?

Consider a simplified network:

[
h^{l+1} = \phi(W^l h^l)
]

As depth increases, you can track quantities such as

[
q_l = \mathbb E[(h_i^l)^2]
]

and the correlation between two inputs:

[
c_l =
\frac{\mathbb E[h_i^l(x)h_i^l(x')]}
{\sqrt{q_l(x)q_l(x')}}.
]

They derive recursive dynamics for these quantities.

The key insight is that deep networks have different regimes:

```text
ordered regime
      ↓
signals become correlated
gradients can vanish
      ↓
critical regime
      ↓
information propagates deeply
gradients remain usable
      ↓
chaotic regime
      ↓
small differences explode
```

This eventually connects to the idea of **edge of chaos / critical initialization**.

That's one of the mathematical roots behind why initialization, normalization, activation functions, etc. matter so much for deep networks.

---

## 3. He also worked on adversarial examples

Another notable direction is **adversarial robustness**.

For example:

**Adversarial Spheres** — Justin Gilmer, Luke Metz, Fartash Faghri.

Google Research publications include this work under Justin Gilmer's publications. ([Google Research][3])

The interesting thing is that Gilmer wasn't merely asking:

> "How do I make adversarial examples?"

He was asking a deeper question:

> **What does adversarial vulnerability actually tell us about the geometry of learned classifiers?**

A useful mental model is:

```text
high-dimensional input space

        decision boundary
              /
             /
   x -------/------ x + δ
            ↑
        tiny perturbation
```

In high-dimensional spaces, a perturbation that looks tiny in Euclidean norm can nevertheless cross a decision boundary.

This is connected to geometry, concentration of measure, margins, and dimensionality—not simply a weird "bug" in neural networks.

---

## 4. TCAV / interpretability

Gilmer also appears on work around **interpreting neural-network representations**, including **TCAV (Testing with Concept Activation Vectors)**.

The basic idea is beautiful:

Instead of asking:

> "Which neuron represents a zebra?"

define a human concept direction in representation space.

Suppose a layer produces

[
h(x)\in\mathbb R^d.
]

Collect examples corresponding to a concept such as "stripes", then learn a concept direction

[
v_{\text{stripe}}\in\mathbb R^d.
]

Now measure how sensitive the model's output is to movement in that direction:

[
S(x) =
\nabla_h f(x)\cdot v_{\text{stripe}}.
]

That gives you something closer to:

> "How important is the concept of stripes to this prediction?"

rather than:

> "Which individual neuron fires?"

This line of thinking became influential in modern representation interpretability. Google Research's publication pages list Gilmer on this work. ([Google Research][3])

---

## 5. His work also reached production ML

An interesting detail is that Gilmer's work isn't purely theoretical.

He's also an author on Google's work around **YouTube recommendation ranking**, including:

**Improving Training Stability for Multitask Ranking Models in Recommender Systems** (KDD 2023).

The paper studies a real multitask ranking system for YouTube recommendations and training stability. ([Google Research][4])

So there is an interesting trajectory:

```text
mathematics
   ↓
theory of neural-network dynamics
   ↓
deep learning optimization
   ↓
robustness / interpretability
   ↓
large-scale production ML
```

That's a very "Google Research" style research career.

---

# Why I think Gilmer is especially worth studying for you

Given that you're currently going through things like **matrix rank, Q/K projections, DeepSeek MLA, initialization, Transformer internals**, I'd put Gilmer in a particularly useful category:

```text
Karpathy
    ↓
implementation / systems intuition

Schoenholz + Gilmer
    ↓
mathematical dynamics of neural nets

Saxe / Pennington / Ganguli
    ↓
linear algebra + signal propagation

DeepSeek / modern LLM papers
    ↓
architectural engineering
```

The connection is that **modern Transformer research still has the same fundamental problem**:

[
x
\rightarrow W_1
\rightarrow \phi
\rightarrow W_2
\rightarrow \cdots
\rightarrow W_L
]

How does information, variance, correlation, and gradient flow through a huge composition of transformations?

That's exactly the kind of question Gilmer/Schoenholz studied.

And when you start thinking about MLA, residual streams, normalization, Q/K projections, rank, information loss, etc., this mathematical perspective becomes very useful.

### A good reading order

I'd go:

1. **Deep Information Propagation** — understand signal/gradient propagation.
2. **Adversarial Spheres** — understand high-dimensional geometry.
3. **TCAV** — understand representation-space geometry.
4. Then move into **Saxe / Pennington / Ganguli** work on deep-network dynamics.
5. Finally connect this to **Transformer/LLM architectures**.

The first paper is the one I'd prioritize. It's much more foundational than his name recognition might suggest.

References:

* [Justin Gilmer — Google Research publications/search ecosystem](https://research.google/people/?utm_source=chatgpt.com)
* [Deep Information Propagation — Google Research / ICLR 2017](https://research.google/blog/research-at-google-and-iclr-2017/?utm_source=chatgpt.com)
* [Google Research publications](https://research.google/pubs/?utm_source=chatgpt.com)
* [Justin Gilmer — LinkedIn profile](https://www.linkedin.com/in/jmgilmer?utm_source=chatgpt.com)

[1]: https://www.linkedin.com/in/jmgilmer?utm_source=chatgpt.com "Justin Gilmer - Research Scientist at Google Brain"
[2]: https://research.google/blog/research-at-google-and-iclr-2017/?utm_source=chatgpt.com "Research at Google and ICLR 2017"
[3]: https://research.google/people/martinwattenberg/?utm_source=chatgpt.com "Martin Wattenberg"
[4]: https://research.google/people/darylchang/?utm_source=chatgpt.com "Daryl Chang"
