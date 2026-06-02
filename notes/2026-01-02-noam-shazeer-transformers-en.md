---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Noam Shazeer on Transformers and Attention
translated: false
type: note
---

Question: How does Noam Shazeer comment on the Transformer and attention mechanism, based on his YouTube videos, interviews, and papers? Provide a comprehensive explanation using his own words and tone where possible.

Answer:

Noam Shazeer, one of the key inventors behind the Transformer architecture, has a casual, enthusiastic, and straightforward tone when discussing it—often sounding like an excited engineer who's thrilled by practical breakthroughs rather than hype. He frequently uses phrases like "Heck yeah!" to express excitement and describes ideas in simple, relatable terms.

### Origins and Motivation

Shazeer traces the Transformer's birth to frustration with recurrent neural networks (RNNs), particularly LSTMs, which were the state-of-the-art for language tasks before 2017.

He said: "I’d been working with LSTMs, the state-of-the-art language architecture before transformer... Filling up memory with all those activations limits the size of your model and the length of the sequences you can process. Transformers can solve those problems because you process the entire sequence simultaneously."

The spark came casually: "I heard a few of my colleagues in the hallway saying, 'Let’s replace LSTMs with attention.' I said, 'Heck yeah!'"

In interviews, he explains RNNs vs. Transformers simply: "The recurrent neural network is the sequential computation where every word you read the next word and you kind of compute your current state of your brain based on the old state... So you have this very long sequence of computations that has to be executed in order... The magic of transformer kind of like convolutions is that you get to process the whole sequence at once."

This parallelism was a game-changer for training speed and scalability.

### Key Contributions to Attention

In the "Attention Is All You Need" paper acknowledgments, it's noted that Shazeer "proposed scaled dot-product attention, multi-head attention and the parameter-free position representation and became the other person involved in nearly every detail." He developed the multi-headed self-attention mechanism, which became core to the architecture.

He describes attention intuitively: "Attention itself... It's kind of like you're creating this big key value associative memory where you're like building this big table like with one entry for every word in the sequence... The insight here was hey, you can use the same attention thing to like look back at the past of this sequence that you're trying to produce."

Inspired by machine translation (like Google Translate), attention acts as a "soft lookup into an index" or memory.

### Impact and Reflections

Shazeer views the Transformer as fundamentally superior for language: "Transformer is a better tool for understanding language. That’s very exciting, and it’s going to affect a lot of applications."

He was surprised by its broader success, especially transfer learning: "I’ve been very pleasantly surprised by transfer learning for transformers, which really kicked off with BERT. The fact that you could spend a lot of computation and train a model once, and very cheaply use that to solve all sorts of problems."

On scaling: "According to the papers OpenAI has been publishing, they haven’t seen any signs that the quality improvements plateau as they make the models bigger."

Overall, his tone is optimistic and understated—he calls the origin a "bright idea" to ditch "annoying" RNNs, and he's "pleasantly surprised" by how far it went, from translation to modern LLMs.

The Transformer replaced recurrence with pure attention for better parallelism, longer contexts, and superior performance, laying the foundation for today's AI boom.

References:

- [Attention Is All You Need paper (arXiv)](https://arxiv.org/abs/1706.03762)
- [DeepLearning.ai Interview with Noam Shazeer](https://www.deeplearning.ai/the-batch/ai-transformed/)
- [No Priors Podcast Transcript with Noam Shazeer](https://sarahguo.com/blog/noamshazeer)
- [Good Times Podcast Notes on Noam Shazeer](https://kevinhabits.com/ai/podcast-notes-noam-shazeer-character-ai-attention-is-all-you-need-on-good-times-w-aarthi-and-sriram)
- [No Priors YouTube Video](https://www.youtube.com/watch?v=emCoG-hA7AE)
