---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'TTT: 测试时训练解析'
translated: true
type: note
---

**Ilya Sutskever/新模型方向中的TTT是什么？**

答案：**TTT = 测试时训练**。其核心思想出乎意料地简单：

> **将模型的内部记忆从固定的向量/KV缓存，转变为一个小型可训练模型，并在读取测试序列时更新该模型。**

这是针对**超长上下文**的Transformer注意力机制的一个颇具前景的替代方案。

### 1. 标准Transformer

对于序列

```text
x1 x2 x3 ... xt
```

注意力机制实际上存储了：

```text
K = [k1, k2, ..., kt]
V = [v1, v2, ..., vt]
```

当前查询会搜索所有之前的token：

```python
attention(q_t, K, V)
    = softmax(q_t @ K.T / sqrt(d)) @ V
```

因此，记忆随着`t`增长。

大致来说：

```text
KV缓存：O(T)
注意力计算：O(T²)
```

TTT提出了一个问题：

> **为什么我需要保留所有之前的token？为什么不训练一个小模型来压缩我所看到的内容？**

这个小模型就成为了**隐藏状态**。

---

### 2. 关键的概念性转变

标准RNN：

```python
h_t = f(x_t, h_{t-1})
```

其中`h`只是一个向量/张量。

TTT：

```python
W_t = update(W_{t-1}, x_t)
```

其中**`W`本身是一个神经网络的权重**。

因此：

```text
RNN：
    记忆 = 向量

TTT：
    记忆 = 神经网络
```

这是一个非常重要的想法。

TTT论文精确描述了这一点：隐藏状态本身是一个机器学习模型，其更新是一个自监督学习步骤。([GitHub][1])

---

### 3. 一个最小化的数学示例

假设这个快速模型只是一个线性层：

```python
y = W @ x
```

当token `x_t`到达时，构建一个目标`z_t`并最小化：

```math
L_t(W) = ||W x_t - z_t||²
```

然后更新：

```math
W_{t+1}
=
W_t - η ∇_W L_t
```

对于均方误差：

```math
∇_W L
=
2(Wx-z)x^T
```

所以：

```math
W_{t+1}
=
W_t - 2η(W_t x_t-z_t)x_t^T
```

这就是你的**记忆更新**。

注意这里发生了什么：

```text
token x_t
   ↓
小型模型 W
   ↓
预测
   ↓
自监督损失
   ↓
梯度
   ↓
更新 W
```

这就是为什么它被称为**测试时训练**。

---

### 4. 为什么这对LLM很有吸引力

想象一下阅读一本包含100万个token的书。

Transformer：

```text
token 1 ─┐
token 2 ─┤
token 3 ─┤
   ...
token 1M ┘
      ↓
   KV缓存
```

你需要保留海量的token级别信息。

TTT：

```text
token流
     ↓
┌───────────────┐
│ 快速权重W     │
└───────────────┘
     ↑
     │ 梯度更新
     │
   新token
```

序列被**压缩到快速模型的权重中**。

这非常接近于：

> **学习而非记忆。**

2025年的TTT-E2E工作进一步推进了这一理念：一个带有滑动窗口注意力的Transformer在读取上下文时通过下一个token预测持续学习，有效地将上下文压缩到其权重中。他们的3B模型在上下文长度增加时推理延迟保持不变，据报道在**128K上下文下比全注意力机制快2.7倍**。([arXiv][2])

---

### 5. TTT vs KV缓存

这是最清晰的心智模型：

|                     | Transformer                | TTT                               |
| ------------------- | -------------------------- | --------------------------------- |
| 记忆                | K/V张量                    | 模型权重                          |
| 更新                | 追加token                  | 梯度更新                          |
| 查询                | 注意力机制                 | 运行快速模型                      |
| 记忆容量            | 大致 #tokens × 维度        | 快速模型的容量                    |
| 长上下文            | 昂贵                       | 潜在线性                          |
| 信息存储            | 显式的token表示             | 学习/压缩后的表示                 |

所以TTT不仅仅是：

> "让我们增加上下文长度。"

它更根本的是：

> **用学习到的记忆取代显式的token记忆。**

---

### 6. 一个重要的细微之处

不要把TTT理解为：

```python
# 每次与它对话时都重新训练整个7B LLM
```

这显然是荒谬的。

该架构将两者分开：

```text
慢速权重
    ↓
大型预训练模型
    ↓
大部分冻结

快速权重
    ↓
小型内部学习器
    ↓
推理时更新
```

概念上：

```python
慢速模型 = 预训练模型

快速状态 = 初始化()

for x in sequence:
    快速状态 = 快速状态 - 学习率 * 梯度(
        自监督损失(快速状态, x),
        快速状态
    )

    y = 慢速模型(x, 快速状态)
```

**快速权重是临时状态**。

这将TTT与更早的理念联系起来，例如**快速权重、在线学习、元学习和学习型记忆**。([测试时训练][3])

---

### 7. 为什么Ilya的方向很有趣

我不认为**Ilya本人等同于TTT**——TTT是由斯坦福/TTT研究小组开发的，并非SSI/Ilya架构的发明。但它与Ilya一直强调的更广泛方向高度相关：**未来的扩展可能会越来越多地来自推理过程中的计算/学习，而不仅仅是更多的静态预训练**。

Ilya在2024年明确表示，传统的预训练正面临数据限制，因为人类基本只有一个互联网，而未来的系统可能会越来越多地在推理时生成数据并进行推理/搜索。([路透社][4])

这在理念上与TTT非常兼容：

```text
旧范式：

预训练
     ↓
冻结模型
     ↓
推理


新范式：

预训练
     ↓
模型学习如何学习
     ↓
推理
     ↓
持续学习 / 搜索 / 推理
     ↓
更好的解决方案
```

而真正极端的扩展是**TTT-Discover**：模型不仅仅是将记忆适应到一个序列，还可以在测试时执行强化学习/搜索来解决特定问题。这更接近于"模型在解决问题的过程中持续学习"。([Reddit][5])

### 一句话直觉

**Transformer：** *"我记得我看到的一切。"*

**RNN：** *"我将我看到的一切压缩成一个状态向量。"*

**TTT：** *"我持续训练一个小模型来记住我看到的一切。"*

最后一个想法是有趣的。([GitHub][1])

参考文献：

* [Learning to (Learn at Test Time)](https://arxiv.org/abs/2407.04620?utm_source=chatgpt.com)
* [Official TTT PyTorch implementation](https://github.com/test-time-training/ttt-lm-pytorch?utm_source=chatgpt.com)
* [End-to-End Test-Time Training for Long Context](https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com)

[1]: https://github.com/test-time-training/ttt-lm-pytorch?utm_source=chatgpt.com "GitHub - test-time-training/ttt-lm-pytorch: Learning to (Learn at Test Time): 具有表达性隐藏状态的RNN的官方PyTorch实现 · GitHub"
[2]: https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com "面向长上下文的端到端测试时训练"
[3]: https://testtimetraining.com/?utm_source=chatgpt.com "测试时训练：跨越AI、医学影像和自主系统的推理时自适应学习"
[4]: https://www.reuters.com/technology/artificial-intelligence/ai-with-reasoning-power-will-be-less-predictable-ilya-sutskever-says-2024-12-14/?utm_source=chatgpt.com "Ilya Sutskever表示，具有推理能力的AI将更难预测"
[5]: https://www.reddit.com/r/singularity/comments/1ql39n9/learning_to_discover_at_test_time/?utm_source=chatgpt.com "测试时学会发现"