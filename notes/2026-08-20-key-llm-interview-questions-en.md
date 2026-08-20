---
audio: false
generated: true
image: false
lang: en
layout: post
title: Key LLM Interview Questions
translated: false
type: note
---

Here are key LLM interview questions organized by topic:

---

## Models & Architecture

- What is the Transformer architecture and how does self-attention work?
- Explain multi-head attention vs single-head attention.
- What is positional encoding and why is it needed?
- What are the differences between encoder-only, decoder-only, and encoder-decoder models? Give examples.
- What is the difference between GPT, BERT, and T5 architectures?
- What is Flash Attention and why does it matter?
- What is Mixture of Experts (MoE) and how does it improve efficiency?
- Explain KV cache — what it is and why it's critical for inference.

---

## Training

- What is pretraining vs fine-tuning vs RLHF?
- Explain the difference between SFT (Supervised Fine-Tuning) and DPO (Direct Preference Optimization).
- What is gradient checkpointing and when would you use it?
- What are the differences between data parallelism, tensor parallelism, and pipeline parallelism?
- What is mixed-precision training (FP16/BF16)? What are the tradeoffs?
- What is the role of learning rate warmup and cosine decay schedules?
- What is catastrophic forgetting and how do you mitigate it?
- How does ZeRO optimization (DeepSpeed) work?
- What is LoRA and how does it reduce trainable parameters?
- What is the difference between LoRA, QLoRA, and full fine-tuning?

---

## Inference & Serving

- What is the difference between greedy decoding, beam search, top-k, and top-p (nucleus) sampling?
- What is speculative decoding and how does it speed up inference?
- What is quantization (INT8, INT4, GPTQ, AWQ)? What do you lose?
- What is model distillation?
- What is continuous batching and why does it outperform static batching?
- How does tensor parallelism work during inference?
- What is prefill vs decode phase in LLM inference?
- What is PagedAttention (used in vLLM) and what problem does it solve?
- How do you measure inference latency vs throughput, and what's the tradeoff?
- What are the bottlenecks in serving a large LLM at scale?

---

## Evaluation & Alignment

- What metrics are used to evaluate LLMs? (Perplexity, BLEU, ROUGE, MMLU, HumanEval, etc.)
- What is hallucination and what techniques reduce it?
- What is RLHF and what are its weaknesses?
- What is Constitutional AI (CAI)?
- How do you evaluate an LLM for production readiness?

---

## Practical / System Design

- How would you design an LLM serving system for 1M requests/day?
- How do you handle context window limits at inference time? (chunking, RAG, sliding window)
- What is RAG (Retrieval-Augmented Generation) and when is it better than fine-tuning?
- How do you reduce GPU memory during inference?
- How would you debug a model that produces repetitive or degenerate output?
