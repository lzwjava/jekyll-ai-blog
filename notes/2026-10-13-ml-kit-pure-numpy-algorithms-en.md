---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ML Kit: Pure NumPy Algorithms"
translated: false
type: note
---

All done. Here's what I built:

## `mlkit` — every algorithm from that table, implemented from scratch in pure NumPy

**`/home/lzw/projects/vv`** → 36 files, ~9,000 lines, one CLI (`mlkit` / `python -m mlkit`), zero ML dependencies (no scikit-learn, no PyTorch — only `numpy`).

### 🤖 Machine Learning — `mlkit ml <algo>` (20 algorithms + `bench`)

| Category | Implementations | Files |
|---|---|---|
| Regression | OLS (SVD), Ridge (closed form), Lasso & ElasticNet (coordinate descent with sklearn-style α) | `ml/linear.py` |
| Classification | Logistic (mini-batch GD), SVM (Pegasos subgradient + **Platt SMO** with RBF/poly kernels), k-NN, Gaussian & Multinomial Naive Bayes | `ml/logistic.py`, `svm.py`, `knn.py`, `naive_bayes.py` |
| Trees/Ensembles | CART (gini/entropy/mse), Random Forest (bagging + OOB score), Gradient Boosting (Friedman), **XGBoost** (Newton gain, λ/α, min_child_weight) | `ml/tree.py`, `boosting.py` |
| Clustering | K-Means++ , DBSCAN (grid bucketing), Hierarchical (**Lance-Williams** updates: single/complete/average/ward), GMM (full/diag EM) | `ml/cluster.py` |
| Dim. reduction | PCA (SVD), t-SNE (exact + early exaggeration), UMAP (fuzzy kNN graph + negative-sampling SGD), Fisher LDA | `ml/decomposition.py` |

### 🧠 Deep Learning — `mlkit dl <model>`

- **`dl/tensor.py`** — a reverse-mode **autograd engine** (broadcasting-aware, batched matmul, im2col conv/pool, fused cross-entropy, gather/dropout, iterative topo-sort) — **verified by `mlkit dl gradcheck`: 10/10 components match finite differences**
- **`dl/nn.py`** — Linear, Conv2d, LayerNorm, Embedding, Dropout, **RNN/GRU/LSTM**, scaled-dot-product + **multi-head attention** (causal mask, KV cache), Transformer blocks
- **`dl/optim.py`** — SGD (momentum/Nesterov), **Adam, AdamW, RMSProp** + grad clipping → demonstrated by `dl optim` (Rosenbrock curves)
- **`dl/train.py`** — MLP (spirals → 99% acc), CNN (shapes → 100%), sequence models (copy task, sine forecast R²≈0.95), **ViT** (100%), **GAN** (with a k-NN two-sample test), **VAE** (ELBO with correct reparameterisation + KL gradients), **DDPM diffusion** (linear & cosine schedules; samples match data moments)

### 🌐 LLMs — `mlkit llm <cmd>` (14 commands)

| Topic | Implementation & measured result |
|---|---|
| Tokenizers | Char + **BPE trained from scratch** (merge learning, ▁ word markers) — perfect round-trip |
| Pre-training | Decoder-only **Transformer**, both objectives: **CLM** (val ppl 33 → **1.8**) and **MLM** |
| Decoding | greedy, **temperature, top-k, top-p, beam search** (`llm generate --beam 4`) |
| **KV cache** | incremental decode: **3.6× faster, bit-identical outputs**; cache-growth table (`llm kv`) |
| **LoRA** | freeze base, train A/B on `c_attn`/`c_proj`: **1.92 % trainable params**, ppl 1.95 → 1.78, save/load/**merge** |
| **Quantization** | INT8 per-channel (**3.86×**, ppl unchanged) & INT4 group-wise (**7.11×**) |
| **Flash attention** | tiled online-softmax kernel, matches naive to **3.6e-7** |
| **Speculative decoding** | draft + target rejection sampling: acceptance 0.7, **target forwards 32 → 9** |
| **RAG** | chunking, TF-IDF/LM embedders, **Flat / IVF / HNSW** vector indexes, extractive + prompt-stuffed answers |
| Agents | **ReAct** (Thought→Action→Observation) & **CoT** loops with working calculator/convert/search tools |

### Verification
```
59/59 CLI commands pass   |   79/79 pytest tests pass   |   gradcheck 10/10
```

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
mlkit dl gradcheck                    # prove the autograd
mlkit bench --dataset circles         # algorithm comparison table
mlkit llm train --out ckpt/           # pre-train a Transformer
mlkit llm generate --ckpt ckpt/ --prompt "the " --top-p 0.9
```

Notable bugs caught during development (each caught by tests I wrote): a `is_leaf` predicate that made every tree node a leaf, swapped k-NN distance arguments, a flipped KL gradient that made the VAE diverge, a 1-off in speculative-decoding verification positions, conv-batch transpose error, and a duplicated class block in `cluster.py` — all fixed and now guarded by the test suite.