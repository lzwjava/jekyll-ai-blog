---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 PyTorch 解释 Vision Transformer
translated: true
type: note
---

问题：Vision Transformer 是如何工作的？提供一些 PyTorch 示例。

答案：

Vision Transformer (ViT) 将最初为自然语言处理设计的 Transformer 架构应用于图像分类等计算机视觉任务。与使用卷积来捕获局部空间特征的卷积神经网络 (CNN) 不同，ViT 将图像视为补丁序列，并依靠自注意力来建模全局关系。

### ViT 工作原理的关键步骤

1.  **分块嵌入（Patch Embedding）**：
    *   输入图像（例如，形状为 `3 × H × W`）被分成固定大小的补丁（通常为 16×16 或 32×32 像素）。
    *   每个补丁被展平并线性投影到一个固定的嵌入维度 `D`（例如，768）。
    *   这会生成一个包含 `N = (H × W) / P²` 个补丁嵌入的序列，其中 `P` 是补丁大小。

2.  **添加分类 Token ([CLS])**：
    *   一个可学习的 `[CLS]` token 被前置到序列中。其在处理后的最终表示用于分类。

3.  **位置嵌入（Positional Embeddings）**：
    *   将可学习的（或固定的）位置嵌入添加到补丁嵌入中，以保留空间信息，因为自注意力是置换不变的。

4.  **Transformer 编码器（Transformer Encoder）**：
    *   序列（长度为 `N+1`）被输入到一堆 Transformer 块中。
    *   每个块包含：
        *   层归一化（Layer Normalization）
        *   多头自注意力（Multi-Head Self-Attention, MHSA）：全局计算所有补丁之间的注意力。
        *   层归一化（Layer Normalization）
        *   MLP（前馈网络）：两个线性层，带有 GELU 激活和 dropout。
        *   两个子层周围的残差连接。

5.  **分类头（Classification Head）**：
    *   与 `[CLS]` token 对应的输出通过一个线性层（或 MLP）生成类别 logits。

ViT 在使用大型数据集和预训练（例如，在 ImageNet 上）时表现出色，大规模训练时通常在可伸缩性和效率方面优于 CNN。

### 简单的 PyTorch 示例：使用 torchvision 的内置 ViT

PyTorch 在 `torchvision` 中提供了预训练的 ViT 实现。

```python
import torch
from torchvision import models, transforms
from PIL import Image

# 加载预训练的 ViT-B/16
model = models.vit_b_16(pretrained=True)
model.eval()

# 预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# 示例：加载图像并预测
img = Image.open("example_image.jpg")  # 替换为您的图像路径
input_tensor = preprocess(img).unsqueeze(0)  # 添加批次维度

with torch.no_grad():
    outputs = model(input_tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    # 获取最高预测（需要 ImageNet 类别列表）
```

### PyTorch 中最简化的自定义 ViT 实现

这是一个用于说明的简化版从头开始的 ViT（未进行生产优化）。

```python
import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        x = self.proj(x)  # (B, embed_dim, num_patches_h, num_patches_w)
        x = x.flatten(2).transpose(1, 2)  # (B, num_patches, embed_dim)
        return x

class ViT(nn.Module):
    def __init__(self, img_size=224, patch_size=16, num_classes=1000, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4):
        super().__init__()
        self.patch_embed = PatchEmbedding(img_size, patch_size, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches

        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))

        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dim_feedforward=embed_dim * mlp_ratio, activation='gelu')
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)

        self.mlp_head = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)

        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        x = x + self.pos_embed
        x = self.transformer(x)

        cls_output = x[:, 0]
        return self.mlp_head(cls_output)

# 使用方式
model = ViT(num_classes=10)  # 例如，用于 CIFAR-10
img = torch.randn(2, 3, 224, 224)
outputs = model(img)  # (2, 10)
```

这捕捉了核心机制；实际实现会添加 dropout、归一化细节等。

参考文献：

-   [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (原始 ViT 论文)](https://arxiv.org/abs/2010.11929)
-   [torchvision VisionTransformer 文档](https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html)
-   [维基百科: Vision Transformer](https://en.wikipedia.org/wiki/Vision_transformer)
-   [V7 Labs: Vision Transformer 指南](https://www.v7labs.com/blog/vision-transformer-guide)
-   [GeeksforGeeks: Vision Transformer 架构](https://www.geeksforgeeks.org/deep-learning/vision-transformer-vit-architecture/)
