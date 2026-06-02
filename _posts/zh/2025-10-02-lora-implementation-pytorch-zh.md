---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 使用PyTorch实现LoRA的示例
translated: true
type: note
---

以下是一个Python代码示例，演示如何使用PyTorch实现LoRA（低秩自适应）来微调简单神经网络。该示例重点展示了如何使用LoRA适配预训练的线性层，保持原始权重冻结的同时引入低秩更新矩阵。代码包含基础设置、玩具数据集和最小化训练循环，以阐明核心概念。

<xaiArtifact artifact_id="1327e99b-24b5-4b0d-9ffd-5b4c2d1472af" artifact_version_id="4053525d-2225-4913-a3b9-b7d66b48daea" title="lora_demo.py" contentType="text/python">
import torch
import torch.nn as nn
import torch.optim as optim

# 定义LoRA层
class LoRALayer(nn.Module):
    def __init__(self, in_features, out_features, rank=4):
        super(LoRALayer, self).__init__()
        # 原始冻结权重
        self.linear = nn.Linear(in_features, out_features)
        self.linear.weight.requires_grad = False  # 冻结原始权重
        # LoRA参数：低秩矩阵A和B
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.randn(rank, out_features))
        self.scaling = 1.0  # LoRA更新的缩放因子

    def forward(self, x):
        # 原始线性变换 + LoRA调整
        original = self.linear(x)
        lora_adjustment = self.scaling * torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)
        return original + lora_adjustment

# 用于演示的玩具数据集
def create_toy_dataset(n_samples=1000):
    X = torch.randn(n_samples, 64)  # 随机输入特征
    y = torch.randn(n_samples, 10)  # 随机目标输出
    return X, y

# 训练函数
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

# 主执行函数
def main():
    # 设置随机种子保证可复现性
    torch.manual_seed(42)

    # 创建玩具数据集
    X, y = create_toy_dataset()

    # 初始化带LoRA的模型
    model = LoRALayer(in_features=64, out_features=10, rank=4)

    # 统计可训练参数
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"可训练参数: {trainable_params}")
    print(f"总参数: {total_params}")

    # 训练模型
    train_model(model, X, y)

if __name__ == "__main__":
    main()
</xaiArtifact>

此代码定义了一个`LoRALayer`，该层通过低秩自适应矩阵（`lora_A`和`lora_B`）封装标准线性层。原始权重被冻结，仅LoRA参数在训练过程中更新。通过玩具数据集和训练循环，展示了LoRA如何在保持微调能力的同时减少可训练参数数量。安装PyTorch后运行此代码，可观察训练过程及参数效率表现。

[LoRA: 大语言模型的低秩自适应](https://arxiv.org/abs/2106.09685)
