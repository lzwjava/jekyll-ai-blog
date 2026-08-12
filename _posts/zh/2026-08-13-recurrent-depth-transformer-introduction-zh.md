---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 循环深度Transformer介绍
translated: true
type: note
---

## 问题：OpenMythos 简介

## 答案

[OpenMythos GitHub 仓库](https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com) 是 Kye Gomez 的一个有趣实验项目，试图从第一性原理**重构一种可能的下一代 Transformer 架构**。它**并非官方的 Claude 实现**；作者明确表示，这是基于公开研究和推测进行的独立理论重构。([GitHub][1])

核心思想：

> 与其通过堆叠更多不同的层来加深 Transformer，不如在一次前向传播中多次复用某些层。

这被称为**递归深度 Transformer (Recurrent-Depth Transformer, RDT)** 或**循环 Transformer (Looped Transformer)**。([GitHub][2])

---

## 1. 普通 Transformer vs OpenMythos

普通的 LLM：

```
x
 ↓
Transformer Block 1
 ↓
Transformer Block 2
 ↓
Transformer Block 3
 ↓
...
 ↓
Transformer Block N
 ↓
logits
```

每一层有不同的参数：

```
Layer1: W1
Layer2: W2
Layer3: W3
...
LayerN: WN
```

深度 = 层数。

---

OpenMythos：

```
x
 ↓
Prelude
 ↓
Recurrent Block
      ↻
      ↻
      ↻
 ↓
Coda
 ↓
logits
```

中间的块被复用：

```
h1 = Block(h0)
h2 = Block(h1)
h3 = Block(h2)
...
hT = Block(hT-1)
```

相同的权重：

```
Block parameters = W

apply:
W(h0)
W(h1)
W(h2)
...
```

因此，不再是：

```
96 个不同的层
```

你可以拥有：

```
12 层
+
8 次递归迭代
=
96 有效计算深度
```

但参数更少。

---

## 2. 为什么要这样做？

直觉：

人类解决问题，并不总是需要更多的“知识”。

有时需要更多的**思考步骤**。

传统 Transformer：

```
更多推理能力
        |
        v
更多层
        |
        v
更多参数
```

OpenMythos 假设：

```
更多推理能力
        |
        v
更多计算步骤
        |
        v
复用现有网络
```

这关联到：

* Universal Transformers
* Deep Equilibrium Models
* 自适应计算时间 (Adaptive Computation Time, ACT)
* 循环神经网络 (recurrent neural networks)

---

## 3. 前向传播

来自仓库：

```
Input token IDs
      |
Embedding
      |
Prelude Transformer
      |
Recurrent Block
      |
Coda Transformer
      |
RMSNorm
      |
LM Head
```

递归更新：

[
h_{t+1}=A h_t + B e + Transformer(h_t,e)
]

其中：

* `h_t`：当前隐藏状态
* `e`：原始编码输入
* `A`, `B`：可学习参数

输入注入很重要。

如果没有它：

```
h0
 ↓
Block
 ↓
h1
 ↓
Block
 ↓
h2
```

多次循环后，信息可能会漂移。

有注入：

```
h0 + input signal
      |
      v
Block
      |
      v
h1 + input signal
      |
      v
Block
```

模型保持对原始表示的访问。([GitHub][3])

---

## 4. 它结合了多个现代 LLM 思想

OpenMythos 基本上是一个“研究游乐场”，结合了：

### Attention

支持：

### GQA

分组查询注意力 (Grouped Query Attention)：

```
许多 Q 头

共享较少的 KV 头
```

目标：

减少 KV 缓存。

---

### MLA

来自 DeepSeek 的多潜在注意力 (Multi-Latent Attention)：

不再使用：

```
缓存：

K:
seq × heads × head_dim

V:
seq × heads × head_dim
```

而是压缩：

```
潜变量 KV：

seq × low_rank_dim
```

然后重构。

这减少了推理时的内存占用。

---

### MoE

不再使用单个巨大的 MLP：

```
token
 |
 |
MLP
```

而是使用专家：

```
token
 |
router
 |
+---- Expert 1
|
+---- Expert 2
|
+---- Expert 3
```

只激活部分专家。

该仓库实现了带有路由专家和共享专家的稀疏 MoE。([GitHub][2])

---

## 5. 与当前 LLM 研究的关系

有趣的部分不在于代码规模，而在于方向。

Transformer 的扩展配方：

```
更多数据
更多参数
更多 GPU
```

代价高昂。

研究人员正在探索：

### 1. 更好的参数效率

示例：

```
MoE
MLA
LoRA
权重共享
```

### 2. 更好的推理时扩展

不再：

```
训练更大的模型
```

而是：

```
相同模型
思考更长时间
```

示例：

```
o1 风格的推理
测试时计算
递归深度
```

OpenMythos 属于这一家族。

---

## 6. 简单的 PyTorch 版本

核心思想仅此而已：

```python
class LoopedTransformer(nn.Module):
    def __init__(self, block, loops):
        super().__init__()
        self.block = block
        self.loops = loops

    def forward(self, x):
        for _ in range(self.loops):
            x = self.block(x)
        return x
```

对比：

普通：

```python
layers = [
    Block(),
    Block(),
    Block(),
    Block()
]
```

参数：

```
4 × block_parameters
```

循环：

```python
block = Block()

for i in range(4):
    x = block(x)
```

参数：

```
1 × block_parameters
```

计算深度相似，参数量更少。

---

## 我的看法

这里最有趣的想法不是“Claude 重构”。更深层的想法是：

> Transformer 层可能更接近迭代算法，而不是固定深度的前馈网络。

Transformer 层是一个可学习的更新规则：

[
h_{t+1}=f_\theta(h_t)
]

今天：

```
应用 f1, f2, f3...
```

未来：

```
重复应用 f 直到足够计算
```

这连接了 LLM 与经典迭代优化：

* 梯度下降
* 数值求解器
* 循环系统

OpenMythos 本质上在问：

**语言模型能否学习其自身的内部推理循环，而不是在架构设计时就将推理深度固定？**

这才是重要的研究方向。([GitHub][2])

参考文献：

* [OpenMythos GitHub](https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com)
* [OpenMythos 文档](https://github.com/kyegomez/OpenMythos/blob/main/docs/open_mythos.md?utm_source=chatgpt.com)
* [OpenMythos PyPI](https://pypi.org/project/open-mythos/?utm_source=chatgpt.com)

[1]: https://github.com/kyegomez/OpenMythos/blob/main/README.md?utm_source=chatgpt.com "OpenMythos/README.md at main · kyegomez/OpenMythos · GitHub"
[2]: https://github.com/kyegomez/OpenMythos?utm_source=chatgpt.com "GitHub - kyegomez/OpenMythos: A theoretical reconstruction of the Claude Mythos architecture, built from first principles using the available research literature. · GitHub"
[3]: https://github.com/kyegomez/OpenMythos/blob/main/docs/open_mythos.md?utm_source=chatgpt.com "OpenMythos/docs/open_mythos.md at main · kyegomez/OpenMythos · GitHub"
