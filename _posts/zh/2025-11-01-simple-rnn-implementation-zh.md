---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 从零实现简单循环神经网络
translated: true
type: note
---

### 使用 NumPy 从零实现简单 RNN 示例

通过 NumPy 从零实现 RNN 是理解其机制的好方法：循环隐藏状态、前向传播和随时间反向传播（BPTT）。以下是一个针对随机序列（类似先前 PyTorch 版本）进行二元分类的基础示例，使用单变量时间序列数据（input_size=1），隐藏层维度为 32，序列长度为 10。

代码包含：

- 数据生成
- RNN 前向传播（隐藏状态使用 tanh 激活函数）
- 反向传播（使用简单梯度下降的 BPTT）
- 训练循环

注意：这是基础 RNN，长序列可能出现梯度消失/爆炸问题。实际应用中建议考虑梯度裁剪或使用 LSTM 逻辑。

```python
import numpy as np

# 超参数
input_size = 1      # 特征维度（单变量）
hidden_size = 32    # 隐藏状态维度
output_size = 1     # 二元输出
sequence_length = 10  # 序列长度
num_samples = 1000
num_epochs = 10
learning_rate = 0.01

# 生成虚拟数据：长度为10的序列，标签基于求和结果（二元分类）
def generate_data(num_samples):
    X = np.random.randn(num_samples, sequence_length, input_size)
    y = (np.sum(X, axis=1) > 0).astype(float).reshape(num_samples, 1)
    return X, y

# 简单RNN类（从零实现）
class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # 初始化权重（Xavier初始化）
        self.Wxh = np.random.randn(hidden_size, input_size) * np.sqrt(1. / input_size)
        self.Whh = np.random.randn(hidden_size, hidden_size) * np.sqrt(1. / hidden_size)
        self.Why = np.random.randn(output_size, hidden_size) * np.sqrt(1. / hidden_size)

        # 偏置项
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))

    def forward(self, x):
        # x 形状：（序列长度, 输入维度, 1）单样本处理
        self.x = x  # 存储用于反向传播
        self.h = np.zeros((self.hidden_size, 1))  # 初始隐藏状态

        # 时间步前向传播
        self.hs = np.zeros((self.hidden_size, sequence_length + 1))  # 隐藏状态（包含初始状态）
        self.hs[:, 0] = self.h.flatten()

        for t in range(sequence_length):
            self.h = np.tanh(np.dot(self.Wxh, x[t]) + np.dot(self.Whh, self.h) + self.bh)
            self.hs[:, t+1] = self.h.flatten()

        # 最终隐藏状态输出
        self.y_pred = np.dot(self.Why, self.h) + self.by
        return self.sigmoid(self.y_pred)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -250, 250)))  # 数值稳定性裁剪

    def backward(self, y_true):
        # 随时间反向传播（简化版）
        dWhy = np.dot((self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred), self.hs[-1:, :].T)
        dby = (self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred)

        # 隐藏层和输出层权重梯度
        dWhh = np.zeros_like(self.Whh)
        dWxh = np.zeros_like(self.Wxh)
        dbh = np.zeros_like(self.bh)

        dh_next = np.zeros_like(self.h)
        for t in reversed(range(sequence_length)):
            dh = np.dot(self.Why.T, (self.y_pred - y_true) * self.sigmoid_deriv(self.y_pred)) + dh_next
            dh_raw = (1 - self.h**2) * dh  # Tanh导数
            dWxh += np.dot(dh_raw, self.x[t].T)
            dWhh += np.dot(dh_raw, self.hs[:, t:t+2].T[:, 0:1])  # 简化处理；完整BPTT需精确累积
            dbh += dh_raw
            dh_next = np.dot(self.Whh.T, dh_raw)

        # 权重更新
        self.Wxh -= learning_rate * dWxh
        self.Whh -= learning_rate * dWhh
        self.Why -= learning_rate * dWhy
        self.bh -= learning_rate * dbh
        self.by -= learning_rate * dby

    def sigmoid_deriv(self, z):
        s = self.sigmoid(z)
        return s * (1 - s)

# 训练流程
X, y = generate_data(num_samples)

# 重塑为单样本处理（简化版 batch_size=1）
X = X.reshape(num_samples, sequence_length, input_size, 1)  # 添加批次维度
y = y.reshape(num_samples, 1, 1)

model = SimpleRNN(input_size, hidden_size, output_size)

for epoch in range(num_epochs):
    total_loss = 0
    for i in range(num_samples):
        pred = model.forward(X[i])
        loss = -np.mean(y[i] * np.log(pred + 1e-8) + (1 - y[i]) * np.log(1 - pred + 1e-8))  # 二元交叉熵
        total_loss += loss
        model.backward(y[i])

    avg_loss = total_loss / num_samples
    print(f'Epoch [{epoch+1}/{num_epochs}], Avg Loss: {avg_loss:.4f}')

# 推理示例
test_seq = np.random.randn(sequence_length, input_size, 1)
prediction = model.forward(test_seq)
print(f'Prediction: {prediction.flatten()[0]:.4f}')
```

#### 实现原理

- **数据生成**：随机序列，基于求和结果的二元标签
- **前向传播**：按时间步处理序列，更新隐藏状态 `h_t = tanh(Wxh * x_t + Whh * h_{t-1} + bh)`，最终隐藏状态通过 sigmoid 输出
- **反向传播**：BPTT 计算所有时间步梯度，通过简单梯度下降更新权重（注：这是最小化实现；完整版本需处理更精确的梯度累积）
- **训练**：遍历样本，计算二元交叉熵损失并更新参数
- **输出**：Sigmoid 输出概率值（0-1）

使用默认参数在标准机器上运行约需 10-20 秒。可增加 `num_samples` 或 `num_epochs` 观察学习效果。如需批量处理，需将循环向量化。

扩展阅读：
[理解 LSTM 网络（Colah 博客）](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
[NumPy RNN 教程](https://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/)
