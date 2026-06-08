---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoGPT块架构
translated: true
type: note
---

## 问题

解释 nanoGPT 中的 Block 类——它如何结合层归一化、注意力机制和 MLP。

## 答案

这是一个**Transformer 解码器模块**——堆叠形成整个语言模型的可重复单元。下面我将逐步讲解前向传播过程及其架构选择。

### 前向传播

```python
def forward(self, x):
    x = x + self.attn(self.ln_1(x))           # 路径1：注意力 + 残差
    x = x + self.mlp(self.ln_2(x))            # 路径2：MLP + 残差
    return x
```

**逐步解析：**

1. **`self.ln_1(x)`** — 对输入应用层归一化
2. **`self.attn(...)`** — 将归一化后的激活值传入因果自注意力（仅关注之前的 token）
3. **`x + ...`** — 添加残差连接：`x_out = x + Attn(LayerNorm(x))`
4. **`self.ln_2(x_out)`** — 再次应用层归一化
5. **`self.mlp(...)`** — 通过前馈网络（全连接 → 激活 → 全连接）
6. **`x + ...`** — 添加另一个残差：`x_final = x_out + MLP(LayerNorm(x_out))`

### 为什么采用 Pre-Norm 架构？

这里使用的是**pre-norm**（在子层前归一化），而非 post-norm（在子层后归一化）。区别如下：

```python
# Pre-norm（本代码）
x = x + SubLayer(LayerNorm(x))

# Post-norm（旧式风格）
x = LayerNorm(x + SubLayer(x))
```

**Pre-norm 的优势：**

- **更好的梯度流动** — 梯度直接通过残差连接传递，不会被层归一化压缩
- **训练更快** — 深层模型更稳定（nanoGPT 采用此方式是有充分理由的）
- **无需热身阶段** — Post-norm 需要学习率预热，pre-norm 则不需要

### 残差连接：恒等捷径

`x + ...` 至关重要。没有它的情形：

```python
# 无残差
x = self.attn(self.ln_1(x))  # x 经过多层后可能消失或爆炸
x = self.mlp(self.ln_2(x))
```

**有残差时：**

```python
x = x + self.attn(self.ln_1(x))
```

网络学习的是对 x 的**加性更新**，而非替换。数学表达式为：

```
x_l+1 = x_l + f_l(x_l)
```

这实现了：

- **深层网络** — 梯度直接流动：∂L/∂x_l = ∂L/∂x_l+1 · (1 + ∂f/∂x_l)
- **安全初始化** — f 初始时接近零（小权重），因此训练早期 x_l ≈ x_0
- **信息旁路** — 注意力/MLP 学习修改 x 而非重建 x

### 注意力与 MLP 的交互方式

```
Block(x) 其中 dim(x) = [batch, seq_len, n_embd]

→ Attn: "哪些过去的 token 是相关的？"（上下文聚合）
→ MLP: "给定关注的上下文，会出现哪些模式？"（特征变换）
```

MLP 是按位置操作的（对每个 token 独立应用）：

```python
# MLP 内部结构（大致）
def forward(self, x):
    x = x @ W1 + b1      # [batch, seq, n_embd] → [batch, seq, 4*n_embd]
    x = gelu(x)          # 激活函数
    x = x @ W2 + b2      # [batch, seq, 4*n_embd] → [batch, seq, n_embd]
    return x
```

因此每个模块完成：

1. **注意力** — token 间的通信（在序列上混合信息）
2. **MLP** — 逐 token 的非线性变换（特征精炼）

### 完整模块示意图

```
输入 x
  ↓
[层归一化] → [因果自注意力] → [+ 残差] → x'
  ↓
[层归一化] → [MLP] → [+ 残差] → 输出
```

### 堆叠模块

nanoGPT 堆叠 N 个这样的模块（通常为 12 或 24 层）。每一层都在处理逐渐高层次的特征：

```python
x = embedding(input_ids)  # [batch, seq, n_embd]
for _ in range(num_layers):
    x = Block(config)(x)   # 重复精炼
x = final_layer_norm(x)
logits = x @ token_embedding.T  # 预测下一个 token
```

早期模块学习低级语法（空格、标点）。后期模块学习语义关系。

### 核心洞见

该模块**精简而优雅**：

- 此处无 dropout（nanoGPT 规模小，过拟合并非主要问题）
- 无学习缩放因子（层归一化已处理方差）
- Pre-norm + 残差 = 无需技巧即可稳定训练深层网络

这正是其有效的原因：**简单组件 + 优良残差结构 = 可训练的深层网络**。
