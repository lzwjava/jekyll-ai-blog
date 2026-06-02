---
audio: false
generated: true
lang: en
layout: post
title: Autoregressive Model Generation
translated: false
type: note
---

In the context of models like GPT (Generative Pre-trained Transformer), the term "autoregressive" refers to the method by which the model generates output sequences. Specifically, it means that the model generates each item in a sequence one at a time, using its previous outputs as additional input context for generating the next item.

Here's a breakdown of how the autoregressive process works in such models:

1. **Sequential Generation**: The model generates text in a sequential manner. It starts with an initial input (often called a prompt) and generates one token (which can be a word, part of a word, or a character) at a time.

2. **Dependency on Previous Tokens**: For each new token it generates, the model considers all the previously generated tokens. This means that the output at each step is dependent on the outputs of all previous steps.

3. **Feedback Loop**: The model uses a feedback loop where the output of the model at time step \\( t \\) is fed back as input at time step \\( t+1 \\). This allows the model to maintain coherence and context over longer sequences.

4. **Probability Distribution**: At each step, the model generates a probability distribution over the possible next tokens and selects one based on this distribution (often using techniques like sampling or selecting the most likely token).

In summary, "autoregressive" in the context of GPT and similar models means that the model generates sequences step-by-step, with each step depending on the previous ones, allowing it to produce coherent and contextually relevant text.
