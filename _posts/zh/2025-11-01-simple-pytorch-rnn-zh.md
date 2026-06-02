---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 简单PyTorch循环神经网络示例
translated: true
type: note
---

### PyTorch 简单 RNN 示例

循环神经网络（RNN）非常适合处理时间序列或文本等序列数据。以下是一个使用 PyTorch 构建简单 RNN 进行序列分类的基础示例（例如对随机序列进行二元分类）。假设已安装 PyTorch（需导入 `import torch` 和 `import torch.nn as nn`）。

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 超参数
input_size = 1      # 特征维度（如单变量时间序列）
hidden_size = 32    # 隐藏状态维度
output_size = 1     # 二元输出（使用 sigmoid 激活函数）
sequence_length = 10  # 序列长度
batch_size = 32
num_epochs = 10

# 生成虚拟数据：长度为10的序列，根据序列和生成二元标签
def generate_data(num_samples):
    X = torch.randn(num_samples, sequence_length, input_size)
    y = (torch.sum(X, dim=1) > 0).float().unsqueeze(1)
    return X, y

# 简单 RNN 模型
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x 形状: (batch, seq_len, input_size)
        h0 = torch.zeros(1, x.size(0), self.hidden_size)  # 初始隐藏状态
        out, _ = self.rnn(x, h0)
        # 取最后时间步的输出进行分类
        out = self.fc(out[:, -1, :])  # 末时间步
        return self.sigmoid(out)

# 初始化模型、损失函数、优化器
model = SimpleRNN(input_size, hidden_size, output_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 训练循环
num_samples = 1000
X, y = generate_data(num_samples)
dataset = torch.utils.data.TensorDataset(X, y)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

for epoch in range(num_epochs):
    for batch_X, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 推理示例
test_seq = torch.randn(1, sequence_length, input_size)
prediction = model(test_seq)
print(f'Prediction: {prediction.item():.4f}')
```

#### 实现原理：
- **数据生成**：创建长度为10的随机序列，根据序列和是否大于0生成二元标签
- **模型结构**：使用 `nn.RNN`（基础RNN单元）。前向传播逐步处理序列，最终隐藏状态用于输出
- **训练过程**：标准 PyTorch 训练循环，使用二元交叉熵损失函数
- **输出结果**：Sigmoid 激活函数输出0-1之间的概率值

此为基础RNN实现。若需处理长序列，建议使用 LSTM 或 GRU 变体（例如将 `nn.RNN` 替换为 `nn.LSTM`）。

### LSTM 变体（快速扩展）
为解决梯度消失问题，可替换为 LSTM：

```python
# 在模型类中替换为：
self.rnn = nn.LSTM(input_size, hidden_size, batch_first=True)

# 前向传播中调整为：
h0 = torch.zeros(1, x.size(0), self.hidden_size)
c0 = torch.zeros(1, x.size(0), self.hidden_size)  # LSTM 需要细胞状态
out, (hn, cn) = self.rnn(x, (h0, c0))
```

请在 PyTorch 环境中运行此代码进行实验！

[PyTorch RNN 文档](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html)
[PyTorch LSTM 文档](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)
