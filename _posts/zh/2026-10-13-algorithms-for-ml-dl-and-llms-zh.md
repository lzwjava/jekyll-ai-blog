---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器学习、深度学习与大型语言模型算法
translated: true
type: note
---

机器学习和深度学习以及大型语言模型（LLMs）中常用的典型算法有哪些？

## 🤖 机器学习（传统）

| 类别 | 算法 |
| --- | --- |
| **回归** | Linear Regression, Ridge, Lasso, ElasticNet |
| **分类** | Logistic Regression, SVM, k-NN, Naive Bayes, Decision Tree |
| **集成学习** | Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost) |
| **聚类** | K-Means, DBSCAN, Hierarchical Clustering, GMM |
| **降维** | PCA, t-SNE, UMAP, LDA |

---

## 🧠 深度学习

| 类别 | 算法 / 架构 |
| --- | --- |
| **前馈** | MLP (Multi-Layer Perceptron) |
| **卷积** | CNN, ResNet, VGG, EfficientNet, Vision Transformer (ViT) |
| **循环** | RNN, LSTM, GRU |
| **生成模型** | GAN (Generative Adversarial Network), VAE (Variational Autoencoder), Diffusion Models |
| **注意力** | Self-Attention, Multi-Head Attention, Cross-Attention |
| **优化** | SGD, Adam, AdamW, RMSProp |

---

## 🌐 大型语言模型（LLMs）

| 类别 | 关键概念 / 技术 |
| --- | --- |
| **核心架构** | Transformer (Encoder-Decoder, Decoder-only) |
| **预训练** | Next Token Prediction (CLM), Masked Language Modeling (MLM) |
| **微调** | Supervised Fine-Tuning (SFT), RLHF, DPO, LoRA, QLoRA |
| **推理** | Greedy Decoding, Beam Search, Top-k / Top-p Sampling, Temperature |
| **检索** | RAG (Retrieval-Augmented Generation), Vector Search (FAISS, HNSW) |
| **效率优化** | Quantization (INT4/INT8), Flash Attention, KV Cache, Speculative Decoding |
| **智能体** | Tool use, Chain-of-Thought (CoT), ReAct, Planning |

---

## 📊 快速参考 —— 何时使用什么

```
Tabular data     → XGBoost / LightGBM
Image tasks      → CNN / ViT / Diffusion
Sequential/NLP   → Transformer / LLM
Clustering       → K-Means / DBSCAN
Small dataset    → SVM / Random Forest
Generative       → GAN / VAE / LLM
```

参考链接：

- [Scikit-learn: Choosing the right estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/)
- [Deep Learning Book – Goodfellow et al.](https://www.deeplearningbook.org/)
- [Attention Is All You Need (Transformer paper)](https://arxiv.org/abs/1706.03762)
- [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course)
- [Sebastian Raschka: ML Algorithm Overview](https://sebastianraschka.com/blog/)
