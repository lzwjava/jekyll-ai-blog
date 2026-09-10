---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT的交叉熵目标
translated: true
type: note
---

问题：为什么 GPT 使用 cross-entropy loss？

答案：

因为 GPT 从根本上就是作为 **next-token probability model** 训练的：

$$
P(x_t \mid x_1,\ldots,x_{t-1})
$$

在每个位置，GPT 都会在词表上输出一个概率分布：

```text
context: "The capital of France is"

logits
   ↓
softmax
   ↓
P(token)
   ↓
[Paris: 0.82, London: 0.03, Berlin: 0.01, ...]
```

训练数据会给出真实的 next token，例如：

```text
target = "Paris"
```

cross-entropy 询问的是：

> **模型把多少概率分配给了正确的 token？**

对于单个 token：

$$
L=-\log P_\theta(x_t\mid x_{<t})
$$

所以如果 GPT 预测：

```text
P(Paris) = 0.82
```

那么

$$
L=-\log(0.82)\approx0.20
$$

预测好 → loss 小。

如果：

```text
P(Paris) = 0.001
```

那么

$$
L=-\log(0.001)\approx6.91
$$

预测很差 → loss 巨大。

### 为什么偏偏是 cross-entropy？

这背后有更深层的原因。

假设真实数据分布是 \(p(x)\)，GPT 学习到的是 \(q_\theta(x)\)。

期望 cross-entropy 为：

$$
H(p,q)=-\mathbb E_{x\sim p}[\log q_\theta(x)]
$$

并且：

$$
H(p,q)=H(p)+D_{KL}(p\|q)
$$

由于 \(H(p)\) 不依赖模型：

$$
\arg\min_\theta H(p,q_\theta)
=
\arg\min_\theta D_{KL}(p\|q_\theta)
$$

所以最小化 cross-entropy 本质上就是让 GPT 的预测分布 \(q_\theta\) 去逼近生成训练文本的那个分布。

---

### 为什么不用 MSE？

假设目标是：

```text
Paris = 1
London = 0
Berlin = 0
...
```

你 *可以* 用 MSE：

$$
\sum_i (q_i-y_i)^2
$$

但分类问题本质上是一个 **概率分布**，而 cross-entropy 的行为要好得多。

对于 softmax + cross-entropy，有一个特别漂亮的 gradient。

令：

$$
z_i = \text{logit}_i
$$

$$
p_i=\operatorname{softmax}(z)_i
$$

且目标 \(y_i\) 是 one-hot。

那么：

$$
L=-\sum_i y_i\log p_i
$$

导数很简单：

$$
\boxed{\frac{\partial L}{\partial z_i}=p_i-y_i}
$$

这极其方便。

例如：

```text
prediction: [0.1, 0.7, 0.2]
target:     [0,   1,   0]

gradient:   [0.1, -0.3, 0.2]
```

模型会收到一个直接信号：

* 概率太高 → 把它往下推
* 概率太低 → 把它往上推
* 正确的 token → gradient 反映它的概率离 1 还有多远

---

### 而这正是 GPT 所做的

对于序列：

```text
The cat sat on the mat
```

GPT 会构造训练样本：

```text
"The"              → "cat"
"The cat"           → "sat"
"The cat sat"       → "on"
"The cat sat on"    → "the"
"The cat sat on the" → "mat"
```

然后：

$$
L=
-\frac1T
\sum_{t=1}^{T}
\log P_\theta(x_t|x_{<t})
$$

在代码中，概念上是：

```python
logits = model(tokens[:, :-1])

loss = F.cross_entropy(
    logits.reshape(-1, vocab_size),
    tokens[:, 1:].reshape(-1),
)
```

然后：

```python
loss.backward()
optimizer.step()
```

这就是 GPT 训练循环的核心。

**cross-entropy 并不是随意选的。** GPT 的任务是估计 next token 的 categorical probability distribution，而 negative log-likelihood / cross-entropy 正是学习该分布时自然的 maximum-likelihood objective。