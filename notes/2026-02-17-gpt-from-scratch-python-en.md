---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT From Scratch in Pure Python
translated: false
type: note
---

Question: Explain the provided Python script by Andrej Karpathy that implements a GPT model from scratch without dependencies.

Answer: This script is a "pedagogical masterpiece" that strips a Large Language Model (LLM) down to its barest essentials. It implements a **Generative Pre-trained Transformer (GPT)** using only the Python Standard Library—no PyTorch, no NumPy, and no TensorFlow.

Here is a breakdown of the core components that make this work:

---

### 1. The "Micro-Autograd" Engine (`class Value`)

At the heart of any deep learning model is **Backpropagation**.

* **The Logic:** Since the script doesn't use PyTorch, it defines a `Value` class that stores a scalar (a single number) and its derivative (`grad`).
* **The Chain Rule:** Every mathematical operation (`+`, `*`, `exp`, `log`) is overloaded to build a "computation graph." When `loss.backward()` is called, the code traverses this graph in reverse order to calculate how much each parameter contributed to the error.

### 2. The GPT Architecture

The model follows the GPT-2 design but swaps some components for simpler versions (e.g., using **RMSNorm** instead of LayerNorm and **ReLU** instead of GeLU).

* **Embeddings:** It uses two lookup tables: `wte` (Token Embeddings) for character meanings and `wpe` (Positional Embeddings) so the model knows where a character sits in a string.
* **Multi-Head Attention:** This is the "brain" of the model. It allows the current character to "look back" at previous characters to determine context. It calculates **Query (Q)**, **Key (K)**, and **Value (V)** vectors for every step.
* **Feed-Forward Network (MLP):** A simple two-layer neural network that processes the information gathered by the attention heads.

### 3. Training & Optimization

The script trains the model on a dataset of names (`names.txt`).

* **Objective:** The model performs **Next-Token Prediction**. Given "A-N-D-R", it tries to predict "E".
* **Loss Function:** It uses **Cross-Entropy Loss** (calculated via `log` and `softmax`), which penalizes the model more heavily the further its prediction is from the actual next character.
* **Adam Optimizer:** It implements the Adam optimization algorithm manually to update the weights, including features like momentum and learning rate decay.

### 4. Inference (The "Babbling")

Once trained, the model generates new text. It starts with a special **BOS (Beginning of Sequence)** token and asks the model for a probability distribution of what comes next. It then "samples" from that distribution—influenced by a **temperature** setting—to create names that never existed in the original list.

---

### Summary Table: Hardware vs. Software

| Feature | This Script's Implementation | Industry Standard (e.g., GPT-4) |
| --- | --- | --- |
| **Math** | Pure Python loops (Slow) | GPU Kernels / CUDA (Fast) |
| **Data** | Single characters | Sub-word "Tokens" |
| **Scale** | ~7,000 parameters | Trillions of parameters |
| **Memory** | Python lists | Tensors (highly compressed) |

Would you like me to explain how the **Attention mechanism** specifically calculates the relationship between characters in this code?
