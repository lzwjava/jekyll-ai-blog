---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ML Kit：纯NumPy算法
translated: true
type: note
---

全部完成。以下是我构建的内容：

## `mlkit` — 该表格中的每个算法，均使用纯 NumPy 从零实现

**`/home/lzw/projects/vv`** → 36 个文件、约 9,000 行、一个 CLI（`mlkit` / `python -m mlkit`）、零 ML 依赖（没有 scikit-learn、没有 PyTorch——只有 `numpy`）。

### 🤖 机器学习 — `mlkit ml <algo>`（20 个算法 + `bench`）

| 类别 | 实现 | 文件 |
| --- | --- | --- |
| 回归 | OLS（SVD）、Ridge（闭式解）、Lasso 和 ElasticNet（坐标下降，sklearn 风格 α） | `ml/linear.py` |
| 分类 | Logistic（小批量梯度下降）、SVM（Pegasos 次梯度 + **Platt SMO**，带 RBF/多项式核）、k-NN、高斯朴素贝叶斯与多项式朴素贝叶斯 | `ml/logistic.py`, `svm.py`, `knn.py`, `naive_bayes.py` |
| 树/集成 | CART（gini/entropy/mse）、随机森林（bagging + OOB 分数）、梯度提升（Friedman）、**XGBoost**（Newton gain、λ/α、min_child_weight） | `ml/tree.py`, `boosting.py` |
| 聚类 | K-Means++、DBSCAN（网格分桶）、层次聚类（**Lance-Williams** 更新：single/complete/average/ward）、GMM（full/diag EM） | `ml/cluster.py` |
| 降维 | PCA（SVD）、t-SNE（exact + early exaggeration）、UMAP（模糊 kNN 图 + 负采样 SGD）、Fisher LDA | `ml/decomposition.py` |

### 🧠 深度学习 — `mlkit dl <model>`

- **`dl/tensor.py`** — 一个反向模式 **autograd 引擎**（支持 broadcasting、批量 matmul、im2col 卷积/池化、融合交叉熵、gather/dropout、迭代拓扑排序）——**由 `mlkit dl gradcheck` 验证：10/10 组件与有限差分一致**
- **`dl/nn.py`** — Linear、Conv2d、LayerNorm、Embedding、Dropout、**RNN/GRU/LSTM**、缩放点积 + **多头注意力**（因果掩码、KV cache）、Transformer 块
- **`dl/optim.py`** — SGD（momentum/Nesterov）、**Adam、AdamW、RMSProp** + 梯度裁剪 → 由 `dl optim` 演示（Rosenbrock 曲线）
- **`dl/train.py`** — MLP（螺旋数据 → 99% 准确率）、CNN（形状数据 → 100%）、序列模型（复制任务、正弦预测 R²≈0.95）、**ViT**（100%）、**GAN**（带 k-NN 双样本检验）、**VAE**（正确重参数化 + KL 梯度的 ELBO）、**DDPM 扩散**（线性与余弦调度；样本与数据矩匹配）

### 🌐 LLM — `mlkit llm <cmd>`（14 个命令）

| 主题 | 实现与实测结果 |
| --- | --- |
| Tokenizers | Char + **从零训练的 BPE**（学习合并、▁ 词标记）——完美往返 |
| 预训练 | 仅解码器 **Transformer**，两个目标：**CLM**（验证 ppl 33 → **1.8**）和 **MLM** |
| 解码 | 贪心、**temperature、top-k、top-p、beam search**（`llm generate --beam 4`） |
| **KV cache** | 增量解码：**快 3.6×，输出逐位一致**；缓存增长表（`llm kv`） |
| **LoRA** | 冻结基础模型，在 `c_attn`/`c_proj` 上训练 A/B：**1.92% 可训练参数**，ppl 1.95 → 1.78，保存/加载/**合并** |
| **Quantization** | INT8 逐通道（**3.86×**，ppl 不变）和 INT4 分组（**7.11×**） |
| **Flash attention** | tiled online-softmax kernel，与朴素实现匹配至 **3.6e-7** |
| **Speculative decoding** | draft + target rejection sampling：接受率 0.7，**目标模型前向次数 32 → 9** |
| **RAG** | 分块、TF-IDF/LM embedders、**Flat / IVF / HNSW** 向量索引、抽取式 + prompt 填充式回答 |
| Agents | **ReAct**（Thought→Action→Observation）和 **CoT** 循环，带有可用的 calculator/convert/search 工具 |

### 验证

```
59/59 CLI commands pass   |   79/79 pytest tests pass   |   gradcheck 10/10
```

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
mlkit dl gradcheck                    # 验证 autograd
mlkit bench --dataset circles         # 算法对比表
mlkit llm train --out ckpt/           # 预训练一个 Transformer
mlkit llm generate --ckpt ckpt/ --prompt "the " --top-p 0.9
```

开发过程中捕获的值得注意的 bug（每一个都由我编写的测试捕获）：一个 `is_leaf` 谓词导致每个树节点都成为叶子，k-NN 距离参数被交换，一个翻转的 KL 梯度导致 VAE 发散，speculative-decoding 验证位置差 1（off-by-one），conv-batch 转置错误，以及 `cluster.py` 中重复的类块——全部已修复，现在由测试套件覆盖。
