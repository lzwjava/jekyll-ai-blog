---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Recurrent Neural Networks Surprising Power
translated: false
type: note
---

This 2015 blog post by Andrej Karpathy is a classic introduction to Recurrent Neural Networks (RNNs), highlighting their surprising power in handling sequences like text generation. Karpathy shares his enthusiasm after training RNNs for tasks like image captioning, which produced coherent outputs with minimal tuning. He releases open-source code for character-level language models using LSTMs (a type of RNN) and demonstrates their "magic" through various text-generation experiments. Below is a structured summary of the key sections.

## Introduction
Karpathy describes RNNs as "unreasonably effective" for sequential data, contrasting them with traditional feedforward networks that handle fixed-size inputs/outputs. He trains simple RNNs on text corpora to predict and generate characters, questioning how they capture language patterns so well. The post includes code on GitHub for replicating the demos.

## Key Concepts: How RNNs Work
RNNs excel at sequences (e.g., sentences, videos) by maintaining an internal "state" (hidden vector) that carries information across time steps. Unlike static networks, they apply the same transformation repeatedly:

- **Input/Output Types**: Fixed input to sequence output (e.g., image to caption); sequence to fixed output (e.g., sentence to sentiment); sequence-to-sequence (e.g., translation).
- **Core Mechanism**: At each step, new state \\( h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t) \\), where \\( x_t \\) is input, and output \\( y_t \\) is derived from the state. Trained via backpropagation through time (BPTT).
- **Depth and Variants**: Stack layers for depth; use LSTMs to handle long-term dependencies better than vanilla RNNs.
- **Philosophical Note**: RNNs are Turing-complete, essentially "learning programs" rather than just functions.

A simple Python snippet illustrates the step function:
```python
def step(self, x):
    self.h = np.tanh(np.dot(self.W_hh, self.h) + np.dot(self.W_xh, x))
    y = np.dot(self.W_hy, self.h)
    return y
```

## Character-Level Language Modeling
The core example: Train on text to predict the next character (one-hot encoded), building probability distributions over a vocabulary (e.g., 65 chars for English). Generation works by sampling from predictions and feeding back. It learns context via recurrent connections—e.g., predicting 'l' after "hel" vs. "he". Trained with mini-batch SGD and optimizers like RMSProp.

## Demonstrations: RNN-Generated Text
All use the author's char-rnn code on single text files, showing progression from gibberish to coherent output.

- **Paul Graham Essays** (~1MB): Mimics startup advice style. Sample: "The surprised in investors weren’t going to raise money... Don’t work at first member to see the way kids will seem in advance of a bad successful startup."
- **Shakespeare** (4.4MB): Produces play-like dialogues. Sample: "PANDARUS: Alas, I think he shall be come approached and the day When little srain would be attain'd into being never fed..."
- **Wikipedia** (96MB): Generates article-like text with markdown, links, and lists. Sample: "Naturalism and decision for the majority of Arab countries' capitalide was grounded by the Irish language by [[John Clair]]..."
- **Algebraic Geometry LaTeX** (16MB): Outputs near-compilable math proofs. Sample: "\begin{proof} We may assume that $\mathcal{I}$ is an abelian sheaf on $\mathcal{C}$..."
- **Linux Kernel C Code** (474MB): Realistic functions with comments and syntax. Sample: "static int indicate_policy(void) { ... if (ss->segment < mem_total) unblock_graph_and_set_blocked(); ... }"
- **Baby Names** (8K names): Novel inventions like "Rudi Levette" or "Hany Mareanne".

" Temperature" controls sampling: Low for repetitive but safe text; high for creative but erratic.

## Challenges and Limitations
- Long-term dependencies: Forgets early context (e.g., mismatched LaTeX tags).
- Memorization over generalization: Good at syntax/structure but hallucinates content.
- Compute-intensive: Needs GPUs; vanilla RNNs unstable without LSTMs.
- Future fixes: External memory (Neural Turing Machines), attention mechanisms.

## Conclusion
RNNs shine in NLP (translation, speech), vision (captioning), and beyond, evolving from nonsense to structured generation. Karpathy visualizes activations (e.g., neurons detecting quotes) and teases an RNN trained on the post itself, outputting meta-text like "I've the RNN with and works...". He recommends further reading and code resources, predicting RNNs' role in smarter AI.

[The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
