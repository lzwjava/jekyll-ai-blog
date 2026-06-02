---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Compute Drives AI's Future
translated: false
type: note
---

In Stanford CS25 (a course on Transformer architectures), Hyung Won Chung, a Research Scientist at OpenAI, gave a guest lecture titled "Shaping the Future of AI" (part of the V4 series). He discusses the importance of identifying the "dominant driving force" behind major changes in any field to predict its future trajectory effectively.

### Key Points from His Discussion

- **The Pen Drop Analogy**: To illustrate, Chung uses a simple physics example: If you drop a pen, its path is predictable because we understand the **dominant force**—gravity—which overrides minor factors like air resistance. By focusing on this dominant force, we simplify complex systems and make reliable predictions. He argues we should apply the same lens to AI.

- **The Dominant Force in AI**: For AI research, the dominant driving force is the **exponential decrease in compute costs** (i.e., cheaper and more abundant computational power). This has been the key enabler of rapid progress, allowing models to scale with more data and parameters. Chung emphasizes that understanding this force shifts focus toward building scalable, general methods rather than over-engineered, bias-heavy designs.

- **Connection to the "Bitter Lesson"**: He references Rich Sutton's "Bitter Lesson" essay, which argues that AI advances come from leveraging more compute and data with simpler, learning-based approaches (like Transformers) rather than human-crafted inductive biases. With compute as the dominant force, architectures should prioritize scalability—e.g., favoring decoder-only Transformers over more complex encoder-decoder setups, as extra structure becomes unnecessary with abundant resources.

- **Broader Implications**: Chung shows historical plots of compute growth vs. AI performance, noting that past trends (like Moore's Law) suggest continued scaling will drive future breakthroughs. His advice: "When we talk about something into the future, the best place to get advice is to look into the history."

This framework helps explain why recent AI models (e.g., those from OpenAI) emphasize massive scaling over fine-tuned tweaks.

[Stanford CS25: V4 - Shaping the Future of AI with Hyung Won Chung](https://www.linkedin.com/pulse/stanford-cs25-v4-shaping-future-ai-hyung-won-chung-tarazona-md-lf9pe)
[Full Lecture Video on YouTube](https://www.youtube.com/watch?v=orDKvo8h71o)
