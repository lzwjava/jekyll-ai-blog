---
audio: false
generated: true
image: false
lang: en
layout: post
title: A/D Conversion in Source Encoding
translated: false
type: note
---

Question: A/D conversion involves sampling, quantization, and encoding; in which stage is this performed?

Answer: 

The process of Analog-to-Digital (A/D) conversion, which includes **sampling**, **quantization**, and **encoding**, is performed during the **Source Encoding** (or **信源编码**) stage in a digital communication system.

### Detailed Explanation:
1.  **Sampling**: This is the process of converting a continuous-time analog signal into a discrete-time signal by taking samples at regular intervals. According to the Nyquist-Shannon sampling theorem, the sampling rate must be at least twice the highest frequency component of the signal to avoid aliasing.
2.  **Quantization**: This step maps the continuous amplitude values of the sampled signal to a finite set of discrete levels. This introduces quantization error (noise) but is necessary for digital representation.
3.  **Encoding**: In this final step of A/D conversion, each quantized level is assigned a unique binary code (a sequence of bits).

In the context of a communication system model:
-   **Source Encoding** aims to convert the source information (which may be analog, like voice or video) into a digital bit stream efficiently. It often includes compression and the A/D conversion process itself if the source is analog.
-   **Channel Encoding** follows source encoding and adds redundancy to the bit stream to protect against errors during transmission (e.g., adding parity bits).
-   **Modulation** converts the digital baseband signal into a form suitable for transmission over the physical channel.

Therefore, since A/D conversion transforms the original analog source information into a digital format, it falls squarely under the domain of **Source Encoding**.

References:  

- [Analog-to-Digital Conversion - Wikipedia](https://en.wikipedia.org/wiki/Analog-to-digital_converter)
- [Source Coding - Britannica](https://www.britannica.com/technology/source-coding)