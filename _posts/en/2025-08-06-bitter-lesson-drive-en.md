---
audio: false
generated: true
image: false
lang: en
layout: post
title: '"Bitter Lesson" Drives Transformer Evolution'
translated: false
type: note
---

In his talk at the Stanford CS25 event, Hyung Won Chung provides a detailed historical and predictive analysis of **Transformer architectures**, arguing that understanding the driving forces behind their evolution is key to anticipating the future of AI. The core of his argument is centered on "The Bitter Lesson" of AI development, which he illustrates through the evolution of Transformer models.

***

### The Driving Force of AI Progress

Chung posits that the most significant factor propelling AI research is the **exponentially decreasing cost of compute**, which has enabled a corresponding increase in the scale of models and data. He argues that to understand the rapid pace of change in the field, one must focus on this dominant driving force rather than getting lost in the details of individual architectural innovations.

He introduces **"The Bitter Lesson,"** a concept that suggests long-term AI progress favors simpler, more general methods with fewer built-in assumptions (inductive biases). While highly structured, domain-specific models might offer short-term gains, they ultimately become bottlenecks as compute and data scale. He encourages researchers to constantly question and simplify their models' underlying structures.

***

### The Evolution of Transformer Architectures

Chung uses three major Transformer architectures to exemplify his points:

1.  **Encoder-Decoder (Original Transformer):** This architecture, originally used for tasks like machine translation, has more inherent structure. It uses separate parameters for the encoder and decoder and specific cross-attention patterns. While effective for distinct input/output tasks, this structure is becoming less relevant in the age of large, general-purpose models.

2.  **Encoder-Only (e.g., BERT):** A simpler architecture that forgoes generation, focusing on tasks like classification. While powerful for specific benchmarks, its narrow focus makes it less generalizable for a wide range of modern applications.

3.  **Decoder-Only (e.g., GPT-3):** This is the most general and least structured of the three. It uses a single stack of layers and shared parameters, making it highly suitable for modern large language models that handle diverse tasks, learn general knowledge, and perform long-form generation.

***

### Key Takeaways and Predictions

According to Chung, the trend is clear: AI is moving toward **simpler, more general architectures with less imposed structure**. This allows models the freedom to learn complex patterns and relationships from vast amounts of data without being constrained by fixed assumptions.

He suggests that the next bottleneck in AI might not be architecture itself but the **learning objective**. He views methods like Reinforcement Learning from Human Feedback (RLHF) as a step toward less structured, learned objective functions that are better suited for open-ended and complex generation tasks. He encourages the audience to think critically about these principles to help shape the future of AI.

You can watch the full talk at [https://www.youtube.com/watch?v=3gb-ZkVRemQ&pp=0gcJCfwAo7VqN5tD](https://www.youtube.com/watch?v=3gb-ZkVRemQ&pp=0gcJCfwAo7VqN5tD).
