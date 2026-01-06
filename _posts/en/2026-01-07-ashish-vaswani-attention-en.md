---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: Ashish Vaswani on Self-Attention Mechanisms
translated: false
type: note
---

Question: What does the video "RAAIS 2019 - Ashish Vaswani, Senior Research Scientist at Google AI" discuss?

Answer: In this presentation from the **Research and Applied AI Summit (RAAIS) 2019**, Ashish Vaswani—one of the primary authors of the "Attention Is All You Need" paper—discusses the power and versatility of **self-attention mechanisms** as an inductive bias for various types of data.

The talk covers several key areas:

* **The Shift from RNNs to Transformers**: Vaswani explains that traditional Recurrent Neural Networks (RNNs) are limited by sequential computation and the difficulty of capturing long-distance relationships. Transformers solve this by allowing for parallel computation and linking any two distant positions in a single "hop" [[01:38](http://www.youtube.com/watch?v=bYmeuc5voUQ&t=98)].
* **Multi-Head Attention**: He describes how the "Transformer" model uses multiple attention layers in parallel to simulate the benefits of convolutions, allowing the model to learn complex relationships like "who did what to whom" in a sentence [[07:12](http://www.youtube.com/watch?v=bYmeuc5voUQ&t=432)].
* **Application to Images**: The presentation details how self-attention can be applied to image generation and classification. By replacing standard convolutions with self-attention layers, the researchers achieved state-of-the-art results with fewer parameters and lower computational costs [[15:04](http://www.youtube.com/watch?v=bYmeuc5voUQ&t=904)].
* **Music Generation**: Vaswani showcases "Music Transformer," which uses relative self-attention to capture timing and repeating motifs in music, enabling the generation of more coherent and expressive musical pieces [[19:34](http://www.youtube.com/watch?v=bYmeuc5voUQ&t=1174)].
* **Future Directions**: He concludes by suggesting that self-attention can be extended to other domains like graph modeling, molecule design, and video compression [[22:45](http://www.youtube.com/watch?v=bYmeuc5voUQ&t=1365)].

References:

* [RAAIS 2019 - Ashish Vaswani, Senior Research Scientist at Google AI](http://www.youtube.com/watch?v=bYmeuc5voUQ)