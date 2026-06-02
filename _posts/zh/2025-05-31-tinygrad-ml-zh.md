---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: TinyGrad轻量级机器学习库
translated: true
type: note
---

### TinyGrad 简介
TinyGrad 是一个轻量级、极简主义的 Python 机器学习和深度学习库，专为教育性和简洁性而设计。它实现了类似 PyTorch 的自动微分功能，但代码量要小得多——大约只有 1000 行。它非常适合学习机器学习概念或构建小型模型，无需大型库的开销。它支持张量、神经网络和基本操作，包括通过 PyTorch 或 Metal 实现的 GPU 加速。

你可以在以下位置找到官方仓库：[tinygrad GitHub](https://github.com/geohot/tinygrad)。注意：它是实验性的，在生产使用中不如 PyTorch 或 TensorFlow 稳定。

### 安装
通过 pip 安装 TinyGrad：

```bash
pip install tinygrad
```

它依赖项极少，但可选地使用 PyTorch 作为某些后端。如需 GPU 支持，请确保已安装 PyTorch。

### 基本用法
首先导入并设置上下文（TinyGrad 要求指定是训练还是推理，因为梯度计算方式不同）。

#### 导入与上下文设置
```python
from tinygrad import Tensor
from tinygrad.nn import Linear, BatchNorm2d  # 用于神经网络

# 设置上下文：训练（用于梯度计算）或推理
Tensor.training = True  # 启用梯度追踪
```

#### 创建与操作张量
张量是核心数据结构，类似于 NumPy 数组或 PyTorch 张量。

```python
# 通过列表、NumPy 数组或形状创建张量
a = Tensor([1, 2, 3])          # 从列表创建
b = Tensor.zeros(3)            # 形状为 (3,) 的零张量
c = Tensor.rand(2, 3)          # 形状为 (2, 3) 的随机张量

# 基本运算
d = a + b                      # 逐元素加法
e = d * 2                      # 标量乘法
f = a @ Tensor([[1], [2], [3]])  # 矩阵乘法（a 是一维张量，隐式转置）

print(e.numpy())               # 转换为 NumPy 以打印或进一步使用
```

#### 自动微分（反向传播）
TinyGrad 使用链式法则自动计算梯度。

```python
# 启用梯度追踪
Tensor.training = True

x = Tensor([1.0, 2.0, 3.0])
y = (x * 2).sum()             # 某些操作；y 是标量

y.backward()                  # 计算梯度
print(x.grad.numpy())         # x 的梯度：应为 [2, 2, 2]
```

导出到 NumPy 时使用 `.numpy()`——除非重置，否则梯度会累积。

#### 神经网络与训练
TinyGrad 包含基本层和优化器。以下是一个简单的 MLP 示例：

```python
from tinygrad.nn import Linear, optim

# 定义简单模型（例如线性层）
model = Linear(3, 1)          # 输入 3，输出 1

# 虚拟数据
x = Tensor.rand(4, 3)         # 4 个样本批次，3 个特征
y_true = Tensor.rand(4, 1)    # 目标值

# 前向传播
pred = model(x).sigmoid()      # 假设为二分类

# 损失（例如均方误差）
loss = ((pred - y_true) ** 2).mean()

# 反向传播与优化
loss.backward()
optim.Adam([model], lr=0.01).step()
```

对于卷积网络，使用 `tinygrad.nn` 中的 `Conv2d`。

### 高级功能
- **损失函数与激活函数**：在 `tinygrad.nn` 中可用（例如 `sigmoid`、`relu`、`cross_entropy`）。
- **优化器**：`tinygrad.nn.optim` 中的 `SGD`、`Adam`。
- **层**：`Linear`、`Conv2d`、`BatchNorm` 等。
- **保存/加载**：模型可以保存为状态字典（类似于 PyTorch）。
- **GPU/加速**：TinyGrad 可以通过 PyTorch 后端在 GPU 上运行：`TESOR_SET_DEVICE='cuda:0'`。它还支持 macOS 上的 Metal。
- **视觉/去噪示例**：仓库中包含在 MNIST 上训练 ResNet 等示例。

完整示例请查看 GitHub 仓库中的 `examples/` 文件夹，例如图像分类或强化学习。

### 示例：训练神经网络
以下是一个完整的简单脚本，用于在 XOR 问题上训练网络：

```python
from tinygrad import Tensor
from tinygrad.nn import Linear, optim

# 数据
X = Tensor([[0,0], [0,1], [1,0], [1,1]])
Y = Tensor([[0], [1], [1], [0]])

# 模型
model = Linear(2, 1)
opt = optim.Adam([model], lr=0.1)

Tensor.training = True

for epoch in range(1000):
    pred = model(X).sigmoid()
    loss = ((pred - Y) ** 2).mean()
    loss.backward()
    opt.step()
    opt.zero_grad()

# 测试
print(model(Tensor([[0,0]])))  # 应接近 0
```

### 提示与注意事项
- **模式切换**：训练时始终设置 `Tensor.training = True`；推理时切换到 `False` 以避免梯度计算。
- **形状处理**：张量遵循 NumPy 风格的广播规则，但在小型模型中注意溢出问题。
- **调试**：使用 `.numpy()` 检查值。如果失败，请检查形状不匹配。
- **性能**：对于大型模型较慢——生产环境请使用 PyTorch。
- **更新**：TinyGrad 发展迅速；请查看仓库获取最新版本。

更多详情，请访问 [文档/README.md](https://github.com/geohot/tinygrad/blob/master/README.md) 或在本地运行示例。如果你有特定用例，请提供更多细节以获得针对性建议！
