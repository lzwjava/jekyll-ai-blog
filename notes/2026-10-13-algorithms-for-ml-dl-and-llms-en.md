---
audio: false
generated: true
image: false
lang: en
layout: post
title: Algorithms for ML, DL, and LLMs
translated: false
type: note
---

Question: What are the typical algorithms used in machine learning, deep learning, and large language models (LLMs)?

Answer:

## 🤖 Machine Learning (Traditional)

| Category | Algorithms |
|---|---|
| **Regression** | Linear Regression, Ridge, Lasso, ElasticNet |
| **Classification** | Logistic Regression, SVM, k-NN, Naive Bayes, Decision Tree |
| **Ensemble** | Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost) |
| **Clustering** | K-Means, DBSCAN, Hierarchical Clustering, GMM |
| **Dimensionality Reduction** | PCA, t-SNE, UMAP, LDA |

---

## 🧠 Deep Learning

| Category | Algorithms / Architectures |
|---|---|
| **Feedforward** | MLP (Multi-Layer Perceptron) |
| **Convolutional** | CNN, ResNet, VGG, EfficientNet, Vision Transformer (ViT) |
| **Recurrent** | RNN, LSTM, GRU |
| **Generative** | GAN (Generative Adversarial Network), VAE (Variational Autoencoder), Diffusion Models |
| **Attention** | Self-Attention, Multi-Head Attention, Cross-Attention |
| **Optimization** | SGD, Adam, AdamW, RMSProp |

---

## 🌐 Large Language Models (LLMs)

| Category | Key Concepts / Techniques |
|---|---|
| **Core Architecture** | Transformer (Encoder-Decoder, Decoder-only) |
| **Pre-training** | Next Token Prediction (CLM), Masked Language Modeling (MLM) |
| **Fine-tuning** | Supervised Fine-Tuning (SFT), RLHF, DPO, LoRA, QLoRA |
| **Inference** | Greedy Decoding, Beam Search, Top-k / Top-p Sampling, Temperature |
| **Retrieval** | RAG (Retrieval-Augmented Generation), Vector Search (FAISS, HNSW) |
| **Efficiency** | Quantization (INT4/INT8), Flash Attention, KV Cache, Speculative Decoding |
| **Agents** | Tool use, Chain-of-Thought (CoT), ReAct, Planning |

---

## 📊 Quick Reference — When to Use What

```
Tabular data     → XGBoost / LightGBM
Image tasks      → CNN / ViT / Diffusion
Sequential/NLP   → Transformer / LLM
Clustering       → K-Means / DBSCAN
Small dataset    → SVM / Random Forest
Generative       → GAN / VAE / LLM
```

References:
- [Scikit-learn: Choosing the right estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/)
- [Deep Learning Book – Goodfellow et al.](https://www.deeplearningbook.org/)
- [Attention Is All You Need (Transformer paper)](https://arxiv.org/abs/1706.03762)
- [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course)
- [Sebastian Raschka: ML Algorithm Overview](https://sebastianraschka.com/blog/)