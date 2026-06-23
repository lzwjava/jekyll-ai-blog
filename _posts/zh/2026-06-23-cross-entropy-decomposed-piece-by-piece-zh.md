---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 逐项分解的交叉熵
translated: true
type: note
---

**问题：** 逐层分解交叉熵公式 H(p, q) = −Σₓ p(x) log q(x) = 𝔼_{x∼p}[−log q(x)]。

**答案：**

## 交叉熵：逐层解析

### 公式的含义

```
H(p, q) = −Σₓ p(x) log q(x)
```

你拥有**两个分布**：
- `p(x)` — **真实**分布（标签，真实情况）
- `q(x)` — **预测**分布（模型输出，softmax logits）

该公式问的是：**平均而言，使用针对 `q` 优化的编码，对从 `p` 中抽取的样本进行编码需要多少比特？**

---

### 逐项分解

**`−log q(x)`** — 在 `q` 下的惊讶度（自信息）

这是如果你假设 `q` 来设计编码本时，编码事件 `x` 的代价。如果你的模型说 `q(x) = 0.01` 但 `x` 实际发生了，你需要付出 `−log(0.01) = 6.64` 比特。如果 `q(x) = 0.99`，你几乎无需付出代价。

**`Σₓ p(x) · [−log q(x)]`** — 在真实分布上的加权平均

你并非均匀采样。你根据每个事件在 `p` 下**实际发生**的频率来加权其代价。即使模型预测错误，真正的稀有事件贡献也很小。真实频繁事件占据主导。

**`𝔼_{x∼p}[−log q(x)]`** — 同上，期望符号表示

完全等价。从真实世界（`p`）中抽取 `x`，然后测量你的模型（`q`）下的惊讶度。这是更清晰的解读方式：**模型 `q` 在现实 `p` 下的期望惊讶度**。

---

### 与 KL 散度的联系

```
H(p, q) = H(p) + D_KL(p || q)
```

其中：
- `H(p) = −Σₓ p(x) log p(x)` — 真实分布的熵（不可约减的代价）
- `D_KL(p || q) = Σₓ p(x) log [p(x)/q(x)]` — 使用错误模型带来的额外代价

在训练中最小化交叉熵损失时，`H(p)` 是常数（标签不变），因此你**纯粹在最小化 KL 散度**——推动 `q` 趋近于 `p`。

---

### 在分类中的具体情形

对于 one-hot 标签，`p` 是一个尖峰：`p(y=k) = 1`，其余为 0。求和退化为：

```
H(p, q) = −log q(y_true)
```

就这么简单。就是模型分配给正确类别的负对数概率。这就是为什么 PyTorch 的 `CrossEntropyLoss` 实现为：

```python
loss = -torch.log(softmax(logits)[true_class])
# 或者等价地：
loss = F.cross_entropy(logits, targets)  # 数值稳定性融合
```

---

### 数值稳定性说明（与你的 nanoGPT 工作相关）

切勿分两步计算 `log(softmax(x))`。应使用 `log_softmax`，它计算：

```python
log_softmax(x_i) = x_i - log(Σ exp(x_j))
# = x_i - (max_x + log(Σ exp(x_j - max_x)))  # logsumexp 技巧
```

在 nanoGPT 中，这正好是 `F.cross_entropy`，它内部通过 CUDA 核调用 `log_softmax` —— 不会因为 `exp(large_logit)` 而溢出。

---

### 一行直觉

> 交叉熵衡量的是，你的模型**平均而言**对实际发生的事件感到多么**惊讶**。最小化它 → 模型不再惊讶 → 模型已经学会了真实分布。