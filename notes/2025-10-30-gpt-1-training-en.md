---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPT-1 Architecture and Training Overview
translated: false
type: note
---

### Overview of GPT-1 Architecture

GPT-1 (Generative Pre-trained Transformer 1) is the foundational model introduced by OpenAI in 2018. It pioneered the approach of pre-training a large language model on unlabeled text using a language modeling objective, followed by fine-tuning for downstream tasks. The architecture is a **decoder-only Transformer**, adapted from the original Transformer paper (Vaswani et al., 2017), but stripped down to only the decoder stack for autoregressive generation. This design enables the model to predict the next token in a sequence, making it suitable for tasks involving contiguous text.

Unlike bidirectional models like BERT, GPT-1 uses **masked self-attention** to ensure causality—each position can only attend to previous positions, preventing information leakage from future tokens.

### Key Components and Hyperparameters

- **Model Type**: Multi-layer Transformer decoder with masked multi-head self-attention and position-wise feed-forward networks.
- **Number of Layers**: 12 Transformer blocks (layers).
- **Attention Mechanism**: 12 attention heads per layer, with each head processing 64-dimensional states (total model dimension: 768).
- **Embedding Dimensions**:
  - Hidden size (d_model): 768.
  - Feed-forward inner dimension (d_ff): 3072 (4x the hidden size, standard for Transformers).
- **Positional Encoding**: Learned positional embeddings added to token embeddings (no sinusoidal encodings used).
- **Activation Function**: Gaussian Error Linear Units (GELU) in the feed-forward layers.
- **Vocabulary and Tokenization**: Byte-Pair Encoding (BPE) with 40,000 merges, trained on the corpus.
- **Total Parameters**: Approximately 117 million.
- **Sequence Length**: Trained on sequences of 512 tokens.
- **Regularization**:
  - Dropout: 0.1 on residuals, embeddings, and attention.
  - Weight decay: Modified L2 regularization (0.01) on non-bias/non-layer-norm weights.
- **Initialization**: Weights initialized from a normal distribution N(0, 0.02).

### Training Details

- **Pre-Training**:
  - **Dataset**: BooksCorpus, a collection of ~7,000 unpublished books (total ~800 million words) across genres like Fantasy, Romance, and Adventure. Text was cleaned (e.g., via ftfy library) and tokenized with spaCy.
  - **Objective**: Unsupervised language modeling (next-token prediction).
  - **Optimizer**: Adam with β1=0.9, β2=0.999, ε=1e-8.
  - **Learning Rate Schedule**: Linear warmup over 2,000 updates to a max of 2.5×10⁻⁴, then cosine annealing to 0.
  - **Batch Size**: 64 sequences per minibatch.
  - **Epochs**: 100.
  - **Performance Metric**: Achieved a perplexity of 18.4 on the training corpus.
- **Fine-Tuning**:
  - Minimal changes: Add a linear output layer for task-specific predictions and use delimiter tokens (e.g., <s>, <e>, $) to structure inputs as single sequences.
  - Auxiliary language modeling loss weighted at 0.5 during fine-tuning.
  - Hyperparameters: Lower learning rate (6.25×10⁻⁵), batch size 32, 3 epochs, with 0.2% warmup and linear decay.
  - This transfer learning approach allowed strong performance on tasks like textual entailment and question answering without task-specific architectures.

### Notable Innovations and Limitations

GPT-1 demonstrated that a single pre-trained model could transfer effectively to diverse NLP tasks via simple input formatting, outperforming some task-tuned models at the time. However, it was relatively small compared to modern LLMs (e.g., GPT-3 has 175B parameters) and limited to 512-token contexts. The architecture laid the groundwork for the entire GPT series, emphasizing scalability in pre-training.

[Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)
[GPT-1 - Wikipedia](https://en.wikipedia.org/wiki/GPT-1)
