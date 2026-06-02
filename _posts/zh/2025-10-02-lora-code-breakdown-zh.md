---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: LoRA代码详解与解析
translated: true
type: note
---

我将把 LoRA 演示代码分解成关键部分，在进入下一部分之前详细解释每一部分。这将有助于清晰地展示 LoRA 的工作原理。这段代码基于之前的示例，使用 PyTorch 为简单线性层实现 LoRA。

### 代码片段 1：LoRA 层定义

```python
import torch
import torch.nn as nn

class LoRALayer(nn.Module):
    def __init__(self, in_features, out_features, rank=4):
        super(LoRALayer, self).__init__()
        # 原始冻结权重
        self.linear = nn.Linear(in_features, out_features)
        self.linear.weight.requires_grad = False  # 冻结原始权重
        # LoRA 参数：低秩矩阵 A 和 B
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.randn(rank, out_features))
        self.scaling = 1.0  # LoRA 更新的缩放因子
```

#### 解释

这段代码定义了实现 LoRA 技术的 `LoRALayer` 类：

- **导入和类设置**：我们导入 PyTorch（`torch`）及其神经网络模块（`nn`）。`LoRALayer` 类继承自 `nn.Module`，使其成为可以集成到更大模型中的 PyTorch 模块。
- **原始线性层**：`self.linear = nn.Linear(in_features, out_features)` 创建一个标准线性层（类似于神经网络中的全连接层），具有 `in_features` 个输入和 `out_features` 个输出。这代表我们想要适应的预训练权重。
- **冻结权重**：`self.linear.weight.requires_grad = False` 冻结线性层的原始权重，确保它们在训练期间不会更新。这是 LoRA 效率的关键，因为它避免了修改大型预训练模型。
- **LoRA 参数**：`self.lora_A` 和 `self.lora_B` 是低秩矩阵。`lora_A` 的形状为 `(in_features, rank)`，`lora_B` 的形状为 `(rank, out_features)`。`rank` 参数（默认=4）控制这些矩阵的大小，使其远小于原始权重矩阵（形状 `in_features x out_features`）。这些矩阵是可训练的（`nn.Parameter`）并使用随机值初始化（`torch.randn`）。
- **缩放因子**：`self.scaling = 1.0` 是一个超参数，用于缩放 LoRA 调整，允许微调适应的强度。

这种设置确保在训练期间只更新小的 `lora_A` 和 `lora_B` 矩阵，从而大幅减少可训练参数的数量。

---

### 代码片段 2：LoRA 前向传播

```python
    def forward(self, x):
        # 原始线性变换 + LoRA 调整
        original = self.linear(x)
        lora_adjustment = self.scaling * torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)
        return original + lora_adjustment
```

#### 解释

这段代码定义了 `LoRALayer` 的前向传播，计算层的输出：

- **输入**：输入 `x` 是一个形状为 `(batch_size, in_features)` 的张量，代表一批输入数据。
- **原始输出**：`original = self.linear(x)` 计算冻结线性层的输出，将预训练权重应用于输入。
- **LoRA 调整**：项 `torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)` 计算低秩适应。首先，`x` 乘以 `lora_A`（形状 `in_features x rank`），产生一个形状为 `(batch_size, rank)` 的张量。然后，将其乘以 `lora_B`（形状 `rank x out_features`），产生一个形状为 `(batch_size, out_features)` 的张量——与原始输出形状相同。此调整代表特定任务的更新。
- **缩放和组合**：调整通过 `self.scaling` 缩放并添加到原始输出，产生最终输出。这确保模型保留预训练知识的同时，融入特定任务的适应。

低秩结构（`rank` 很小，例如 4）确保调整在计算上比更新完整权重矩阵更廉价且参数效率更高。

---

### 代码片段 3：玩具数据集和训练

```python
def create_toy_dataset(n_samples=1000):
    X = torch.randn(n_samples, 64)  # 随机输入特征
    y = torch.randn(n_samples, 10)  # 随机目标输出
    return X, y

def train_model(model, X, y, epochs=10, lr=0.01):
    criterion = nn.MSELoss()
    optimizer = optim.Adam([param for param in model.parameters() if param.requires_grad], lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
```

#### 解释

这段代码创建一个玩具数据集并训练 LoRA 适应模型：

- **玩具数据集**：`create_toy_dataset` 函数生成用于演示的合成数据。`X` 是一个形状为 `(1000, 64)` 的张量（1000 个样本，64 个特征），`y` 是一个形状为 `(1000, 10)` 的张量（1000 个样本，10 个输出维度）。这些是随机张量，用于模拟输入-输出对。
- **训练函数**：`train_model` 函数设置一个简单的训练循环：
  - **损失函数**：`nn.MSELoss()` 将均方误差定义为损失，适用于这种类似回归的玩具任务。
  - **优化器**：`optim.Adam` 仅优化可训练参数（`param.requires_grad` 为 `True`），即 `lora_A` 和 `lora_B`。冻结的 `linear.weight` 被排除在外，确保效率。
  - **训练循环**：对于每个周期，模型计算输出，计算损失，执行反向传播（`loss.backward()`），并更新 LoRA 参数（`optimizer.step()`）。打印损失以监控训练进度。

这种设置展示了 LoRA 如何仅微调低秩矩阵，保持过程轻量。

---

### 代码片段 4：主执行和参数计数

```python
def main():
    # 设置随机种子以确保可重现性
    torch.manual_seed(42)

    # 创建玩具数据集
    X, y = create_toy_dataset()

    # 使用 LoRA 初始化模型
    model = LoRALayer(in_features=64, out_features=10, rank=4)

    # 计算可训练参数
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Trainable parameters: {trainable_params}")
    print(f"Total parameters: {total_params}")

    # 训练模型
    train_model(model, X, y)

if __name__ == "__main__":
    main()
```

#### 解释

这段代码将所有内容整合在一起，并突出显示 LoRA 的效率：

- **随机种子**：`torch.manual_seed(42)` 确保随机初始化的可重现性。
- **数据集和模型**：创建玩具数据集，并初始化一个 `LoRALayer`，其中 `in_features=64`、`out_features=10` 和 `rank=4`。
- **参数计数**：代码计算：
  - **可训练参数**：仅 `lora_A`（64 × 4 = 256）和 `lora_B`（4 × 10 = 40），总计 296 个参数。
  - **总参数**：包括冻结的 `linear.weight`（64 × 10 = 640）和 `linear.bias`（10），加上 LoRA 参数，总计 946。
  - 这显示了 LoRA 的效率：只有约 31%（296/946）的参数是可训练的，而在完全微调中为 100%。
- **训练**：调用 `train_model` 函数在玩具数据集上微调 LoRA 参数。

运行此代码时，您将看到可训练参数的数量远小于总参数，并且由于低秩更新，模型训练迅速。

---

### 运行代码

要运行此代码，您需要安装 PyTorch（`pip install torch`）。将完整代码保存为 `.py` 文件并执行。输出将显示参数数量和 10 个周期内的训练损失，展示 LoRA 在微调中的效率。

[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

如果您想深入了解任何部分或修改示例，请告诉我！
