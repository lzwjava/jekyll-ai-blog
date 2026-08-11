---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Schmidhuber: LSTM Creator's Life and Legacy"
translated: false
type: note
---

Question: How is the life story of the LSTM author, Julien xxx?

Answer:

I think you mean **Jürgen Schmidhuber**, one of the key people behind LSTM, not "Julien". LSTM was created by **Sepp Hochreiter and Jürgen Schmidhuber** in the 1990s. ([Wikipedia][1])

Jürgen Schmidhuber has a very unusual AI researcher life story.

### Early life

* Born in 1963 in Munich, Germany.
* As a child, he was fascinated by the idea of creating an artificial intelligence that could improve itself.
* Unlike many researchers who entered AI through traditional computer science, he was strongly influenced by **self-improving machines and artificial curiosity**.

His early thinking was not just "solve a task", but:

> Can we build a machine that discovers better algorithms by itself?

This theme continued through his career.

### Academic path

He studied computer science at the Technical University of Munich.

His PhD work focused on neural networks and learning algorithms. During this period, he worked with Sepp Hochreiter, whose thesis studied the **vanishing gradient problem** in recurrent neural networks. That work became the foundation for LSTM. ([Wikipedia][1])

### LSTM invention (1990s)

Traditional RNNs had a major problem:

When training:

```
h_t = f(W_h h_(t-1) + W_x x_t)
```

the gradient:

```
∂Loss / ∂h_t
```

would repeatedly multiply through many time steps.

If values were smaller than 1:

```
0.9^100 ≈ 0.000026
```

The model "forgot" long-term information.

Hochreiter and Schmidhuber introduced LSTM:

```
forget gate
input gate
output gate
memory cell
```

The key idea:

Instead of forcing information through repeated nonlinear transformations, create a controlled memory highway:

```
c_t = f_t * c_(t-1) + i_t * g_t
```

where:

* `f_t` decides what to forget
* `i_t` decides what new information enters
* `c_t` stores long-term memory

The first LSTM paper appeared in the mid-1990s, with later versions adding the forget gate that became standard. ([Wikipedia][1])

### Career after LSTM

Schmidhuber continued researching:

* meta-learning
* neural architecture search
* artificial curiosity
* self-improving AI
* compression as intelligence

He founded the AI research lab IDSIA in Switzerland and became known for predicting many directions of modern deep learning.

His students and collaborators influenced many later AI systems.

### Personality and philosophy

He is a very "first-principles" researcher.

A recurring idea:

> Intelligence is compression + prediction + self-improvement.

He often argues that a sufficiently powerful learning system should discover patterns and improve itself.

This is similar in spirit to modern LLM scaling:

```
more data
+
larger models
+
better optimization
=
emergent capability
```

### Comparison with modern AI founders

Interesting contrast:

| Person      | Main contribution                                  |
| ----------- | -------------------------------------------------- |
| Schmidhuber | Learning algorithms, LSTM, self-improving AI ideas |
| Hinton      | Deep neural networks, representation learning      |
| LeCun       | CNNs, self-supervised learning                     |
| Bengio      | Deep learning theory, representation learning      |
| Karpathy    | Making AI systems understandable and practical     |

Schmidhuber is closer to a "theoretical inventor" type.

### A lesson from his career

One interesting pattern:

LSTM was invented around **1995–1997**, but its huge impact came almost 15 years later.

Timeline:

```
1995
 |
 | LSTM invented
 |
2000s
 |
 | limited adoption
 |
2014
 |
 | Google seq2seq, speech recognition, translation
 |
2017
 |
 | Transformer replaces LSTM for many NLP tasks
```

([arXiv][2])

This is a good example of how important ideas can arrive much earlier than the ecosystem is ready for them.

For an engineer building AI systems today, the LSTM story is a reminder: **deep technical ideas often need hardware, data, and engineering ecosystems before they become revolutionary.**

References:

* ([Wikipedia][1])
* ([arXiv][3])
* ([arXiv][2])

[1]: https://en.wikipedia.org/wiki/Long_short-term_memory?utm_source=chatgpt.com "Long short-term memory"
[2]: https://arxiv.org/abs/1409.3215?utm_source=chatgpt.com "Sequence to Sequence Learning with Neural Networks"
[3]: https://arxiv.org/abs/1503.04069?utm_source=chatgpt.com "LSTM: A Search Space Odyssey"