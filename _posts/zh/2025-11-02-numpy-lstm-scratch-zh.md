---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 从零实现NumPy长短期记忆网络
translated: true
type: note
---

这是一个基于 NumPy 的长短期记忆网络基础实现，灵感来源于 Christopher Olah 博客文章《理解 LSTM 网络》中的概念。该实现包含核心门控机制（遗忘门、输入门、候选细胞状态和输出门），主要聚焦于前向传播过程。类通过 `forward()` 方法处理单个时间步，通过 `forward_sequence()` 方法处理完整序列。

权重采用随机初始化（实际应用中建议使用 Xavier/Glorot 等更好的初始化方法）。此处未包含反向传播或训练功能——可通过扩展实现基于时间的反向传播算法。

```python
import numpy as np

class LSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        # 初始化遗忘门、输入门、细胞状态和输出门的权重与偏置
        self.Wf = np.random.randn(hidden_size, hidden_size + input_size)
        self.Wi = np.random.randn(hidden_size, hidden_size + input_size)
        self.WC = np.random.randn(hidden_size, hidden_size + input_size)
        self.Wo = np.random.randn(hidden_size, hidden_size + input_size)
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bC = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def tanh(self, z):
        return np.tanh(z)

    def forward(self, x, h_prev, C_prev):
        # x: (input_size, 1), h_prev 和 C_prev: (hidden_size, 1)
        # 拼接隐藏状态与输入
        concat = np.vstack((h_prev, x))
        # 遗忘门
        f_t = self.sigmoid(np.dot(self.Wf, concat) + self.bf)
        # 输入门
        i_t = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
        C_tilda = self.tanh(np.dot(self.WC, concat) + self.bC)
        # 细胞状态更新
        C_t = f_t * C_prev + i_t * C_tilda
        # 输出门
        o_t = self.sigmoid(np.dot(self.Wo, concat) + self.bo)
        # 隐藏状态更新
        h_t = o_t * self.tanh(C_t)
        return h_t, C_t

    def forward_sequence(self, X):
        # X: (seq_len, input_size)
        h = np.zeros((self.hidden_size, 1))
        C = np.zeros((self.hidden_size, 1))
        outputs = []
        for x in X:
            h, C = self.forward(x.reshape(-1, 1), h, C)
            outputs.append(h)
        return np.hstack(outputs).T  # 返回 (seq_len, hidden_size)

# 使用示例
input_size = 3
hidden_size = 5
lstm = LSTM(input_size, hidden_size)

# 单步处理
x_t = np.random.randn(input_size, 1)
h_prev = np.zeros((hidden_size, 1))
C_prev = np.zeros((hidden_size, 1))
h_t, C_t = lstm.forward(x_t, h_prev, C_prev)
print("单步处理 - 隐藏状态维度:", h_t.shape)

# 序列处理
X = np.random.randn(4, input_size)  # 序列长度=4
outputs = lstm.forward_sequence(X)
print("序列输出维度:", outputs.shape)
```

### 核心机制解析
- **初始化**：权重矩阵连接拼接后的输入（前一隐藏状态 + 当前输入）与各个门控，偏置项初始化为零
- **门控机制**：
  - **遗忘门** (`f_t`)：决定从先前细胞状态中遗忘哪些信息（sigmoid 输出 0-1）
  - **输入门** (`i_t`) 与 **候选细胞状态** (`C_tilda`)：决定添加哪些新信息（sigmoid + tanh 组合）
  - **输出门** (`o_t`)：过滤细胞状态生成隐藏状态（sigmoid + 细胞状态 tanh 变换）
- **细胞状态** (`C_t`)：通过线性流动与加法更新实现长期记忆保持
- **使用方式**：处理序列时循环遍历时间步，逐步更新隐藏状态与细胞状态

本实现完美复现了 Colah 博客中描述的 LSTM 架构：细胞状态作为由门控机制调控的"信息高速公路"。

[理解LSTM：从零开始实现](https://medium.com/@samina.amin/understanding-lstms-lstm-implementation-from-scratch-18965a150eca)
