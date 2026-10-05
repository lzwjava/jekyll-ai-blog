---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Vision-Language Models Work
translated: false
type: note
---

Question: How do vision-language models (VLMs) work?

Answer: A vision-language model takes images (and sometimes video) together with text and produces text, such as captions, answers to questions about a picture, or descriptions of a chart. Most modern VLMs have three main parts.

**1. Vision encoder.** The image is split into small patches (e.g., 14×14 or 16×16 pixels). A Vision Transformer (ViT) turns each patch into a vector and processes them with self-attention, producing a sequence of visual feature vectors. The encoder is usually pretrained, often with a contrastive method like CLIP, which learns to place an image and its matching caption close together in the same embedding space.

**2. Connector (projector).** The visual features live in a different "space" than the language model's word embeddings, so a bridge is needed. It can be a simple linear layer or small MLP (as in LLaVA), or a more elaborate module such as cross-attention or a Q-Former (as in Flamingo and BLIP-2) that compresses the image into a fixed number of "visual tokens."

**3. Large language model (LLM).** The visual tokens are placed in the LLM's input sequence alongside the text tokens of the prompt. The LLM then generates the answer one token at a time, attending to both the image tokens and the text. To the LLM, the image is effectively a sequence of extra "words."

**Training** usually happens in stages:
- *Alignment pretraining:* train on large sets of image-caption pairs so the connector learns to translate visual features into something the LLM understands. The encoder and LLM are often frozen at this point.
- *Instruction tuning:* fine-tune on image-based conversations, question answering, OCR, charts, and reasoning tasks so the model follows instructions about images.
- *Optional preference tuning (RLHF or similar):* reduces hallucinations and improves helpfulness.

**Example flow:** you upload a photo of a dog and ask "What breed is this?" → the image is encoded into, say, a few hundred visual tokens → they are projected into the LLM's embedding space → the LLM reads those tokens plus your question → it generates "This looks like a golden retriever."

**Common limitations:** VLMs can hallucinate details that aren't in the image, struggle with fine spatial reasoning and counting, and may miss small text when high-resolution images are downscaled (newer models tile images or use dynamic resolution to help with this).

References:
- [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)
- [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)](https://arxiv.org/abs/2010.11929)
- [Flamingo: a Visual Language Model for Few-Shot Learning](https://arxiv.org/abs/2204.14198)
- [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and LLMs](https://arxiv.org/abs/2301.12597)
- [Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485)