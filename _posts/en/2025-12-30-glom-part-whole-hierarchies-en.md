---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: GLOM for Part-Whole Hierarchies
translated: false
type: note
---

**Question**: What did Geoffrey Hinton say in his Stanford CS25 lecture?

**Answer**:

Geoffrey Hinton gave a guest lecture in Stanford's CS25: Transformers United course (specifically in an earlier version of the seminar series). The talk was titled "Representing Part-Whole Hierarchies in a Neural Network" and focused on his proposed architecture called **GLOM**.

### Key Points from Hinton's Lecture:
- Hinton introduced **GLOM** as an imaginative neural network system designed to better represent **part-whole hierarchies** (e.g., how parts of an object form wholes, like features in a face forming the face itself) in visual perception.
- He argued that current Transformer-based systems, while powerful, struggle with parsing scenes into coherent part-whole structures and interpreting representations intuitively.
- GLOM combines ideas from several research advances:
  - Transformers (for attention mechanisms)
  - Capsules (his earlier work on dynamic routing)
  - Neural fields
  - Contrastive representation learning
  - Distillation techniques
- The core idea is to use **island-like distributed representations** where similar vectors cluster ("islands") over time to represent entities at different levels of hierarchy, improving interpretability especially in vision tasks.
- If successful, GLOM could make representations in Transformer-like models (applied to vision or language) much more interpretable for humans.
- Hinton emphasized that this could address limitations in how modern deep learning models handle compositional structures compared to human perception.

This talk was a special/guest lecture, not part of the regular instructor series, and was released on YouTube in August 2022 (recorded earlier). It reflects Hinton's ongoing thinking on improving neural networks beyond standard Transformers, tying into his broader views on AI representation and understanding.

References:

- [Stanford CS25: Represent part-whole hierarchies in a neural network, Geoff Hinton (YouTube Video)](https://www.youtube.com/watch?v=CYaju6aCMoQ)
- [CS25 Course Website (mentions Hinton as a past speaker)](https://web.stanford.edu/class/cs25/)
- [Speaker Deck Summary of CS25 Lectures (includes Hinton's GLOM talk)](https://speakerdeck.com/sadahry/cs25-transformers-united-2785d644-be02-4be6-8812-e8d9c93790ae)
