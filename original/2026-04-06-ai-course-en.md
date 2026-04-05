---
audio: false
generated: false
image: false
lang: en
layout: post
title: "My AI Course: 10 Lessons from Neural Networks to GPT"
translated: false
---

I'm offering a 10-lesson AI course. 3000 RMB total, spread over three months. That's about 3 days of work salary — a simple way to earn some living expenses while sharing what I've learned.

## My Background

I completed the Machine Learning Specialization (by DeepLearning.AI and Stanford University) and the Deep Learning Specialization (by DeepLearning.AI) — both Andrew Ng's courses. I basically finished them. To be honest, I was a bit impatient with the assignments at the time and referenced others' solutions more than I should have. But I went back later and filled in the gaps myself.

After writing the article [Zen and the Art of Machine Learning](https://lzwjava.github.io/zen-neural-en), I found that I still didn't understand neural networks deeply enough. Understanding is a relative thing, as Feynman said. So I figured out a way — copy a few lines of code, run it, print every variable. That's how I really learned.

Later I spent about two years mulling over transformers. I first read about the KQV mechanism around end of 2023 but didn't understand much. By mid-2025, it clicked. I wrote about that journey in [Neural Network, Transformer and GPT](https://lzwjava.github.io/kqv-transformers-en).

The key project in my learning was Karpathy's [nanoGPT](https://github.com/karpathy/nanoGPT). A lot of my knowledge came from studying that codebase.

I've also done hands-on GPU work. I used a DigitalOcean H200 GPU droplet to run inference on Qwen3.5-35B, and I've done GPT-2 124M training experiments with nanoGPT. So this course isn't just theory — I have the infrastructure to walk you through real training and inference.

## Course Philosophy

Inspired by Yin Wang's [CS video course](https://www.yinwang.org/posts/cs-video-course) and his [CS course principles](https://www.yinwang.org/posts/cs3), I believe in:

* Print variables to understand — not just read about it
* Read real code (nanoGPT, not just textbooks)
* Train small models yourself
* Build systems, not just theory
* Iterate like training an LLM — you don't get it right the first time

## The 10 Lessons

We do three months. Month 1 is foundations, Month 2 is GPT and nanoGPT, Month 3 is agents and building your own system.

### Lesson 1 — Neural Networks from First Principles

Understand what a neural network really computes. Scalar, vector, matrix computation. Forward propagation step by step. Backpropagation intuition with manual derivatives. Activation functions, loss functions.

Practice: Print every variable (Zen neural style). Implement a 2-layer NN in pure Python. Train on MNIST.

After this, you understand every number inside a neural network.

### Lesson 2 — From Neural Networks to Deep Learning

Gradient descent, learning rate, convergence. Overfitting vs generalization. Regularization, dropout, batch/mini-batch/SGD.

Practice: Train a 3-layer classifier. Visualize the loss curve. Implement dropout manually.

After this, you understand how deep learning actually trains.

### Lesson 3 — PyTorch Minimal Framework

Tensor fundamentals, autograd, nn.Module design, optimizer mechanics, Dataset and DataLoader.

Practice: Rebuild MLP in PyTorch. Train a CIFAR classifier. Inspect gradients.

After this, you can read any PyTorch model.

### Lesson 4 — Language Modeling Fundamentals

Tokenization (BPE), n-gram models, RNN/LSTM intuition, next token prediction, cross-entropy for language.

Practice: Build a character-level language model. Train on tiny Shakespeare. Generate text.

After this, you understand what GPT predicts.

### Lesson 5 — Transformer Architecture

Self-attention, Q K V explained, multi-head attention, positional encoding, feed-forward blocks, residual connections.

Practice: Implement single-head attention. Build a mini transformer. Visualize attention.

After this, you understand the GPT architecture.

### Lesson 6 — nanoGPT Deep Dive

This is the key lesson. nanoGPT training loop, GPT model architecture, weight initialization, data pipeline, sampling.

Practice: Train nanoGPT on a small dataset. Modify model size. Train on a Chinese corpus. Change the tokenizer.

After this, you can train your own GPT.

### Lesson 7 — GPT Training Engineering

GPU memory optimization, gradient accumulation, mixed precision, checkpointing, multi-GPU training, dataset scaling.

Practice: Train a 100M parameter model. Resume training. Fine-tune a model.

After this, you can run real GPT training.

### Lesson 8 — Instruction Tuning and Alignment

SFT fine-tuning, instruction datasets, RLHF overview, reward model concept, LoRA fine-tuning.

Practice: Fine-tune nanoGPT with a chat format dataset. Build an instruction-following model.

After this, you can build a chat model.

### Lesson 9 — LLM Agents (Claude Code / OpenClaw)

Tool calling, agent loop, planning and execution, memory systems, CLI agent design.

Practice: Build a coding agent. Build a CLI automation agent. Build a multi-step reasoning agent.

After this, you can build an OpenClaw-style system.

### Lesson 10 — Personal AI System (Capstone)

Local model deployment, retrieval (RAG), long context memory, multi-agent systems, CLI toolkit integration.

Final project options: Personal coding AI, research assistant, CLI AI toolkit, or autonomous dev agent.

After this, you have your own AI system.

## What You'll Be Able to Do

After these 10 lessons, you'll understand neural networks deeply, understand transformers, train GPT from scratch, modify nanoGPT, fine-tune models, build AI agents, and build an OpenClaw-like platform.

From math to GPT to AI system. That's the path.

## Details

* 10 lessons, 3 months
* 3000 RMB
* Month 1 (Lessons 1–4): Foundations
* Month 2 (Lessons 5–7): GPT + nanoGPT
* Month 3 (Lessons 8–10): Agents + System

Reach out if you're interested.
