---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLIP模型训练基础
translated: true
type: note
---

问题：如何训练一个 CLIP（图像-文本对比学习）模型？

答案：

CLIP 训练的核心是学习一个**共享的嵌入空间，使得含义相同的图像和文本在空间中靠近，而不匹配的图像-文本对则相互远离**。它是现代多模态大语言模型的关键基础组件之一。

---

## 1. CLIP 的核心思想

CLIP 包含两个编码器：

* **图像编码器**：ViT / ResNet
* **文本编码器**：Transformer（类似 GPT 的编码器风格）

两者输出相同维度的向量：

```
image → f_img → vector (d)
text  → f_txt → vector (d)
```

然后使用余弦相似度进行比较。

---

## 2. 训练目标（关键部分）

使用 **(图像，文本) 对** 进行训练。

对于一个包含 N 个对的批次：

* 每张图像应与正确的文本匹配
* 所有其他文本均作为负样本
* 所有其他图像均作为负样本

---

### 相似度矩阵

对于批次大小 N：

```
S_ij = cosine_similarity(image_i, text_j)
```

得到一个 N×N 的矩阵。

---

### 损失函数（对称交叉熵）

从两个方向进行计算：

#### (1) 图像 → 文本

正确文本位于对角线：

```
Loss_img = CE(S / temperature, target = [0,1,2,...])
```

#### (2) 文本 → 图像

```
Loss_txt = CE(S^T / temperature, target = [0,1,2,...])
```

最终损失：

```
Loss = (Loss_img + Loss_txt) / 2
```

---

## 3. 温度参数

CLIP 使用一个可学习的缩放因子：

```
logits = S * exp(t)
```

用于控制相似度分布的尖锐程度。

---

## 4. 所需数据

需要 **数百万到数十亿个（图像，文本）对**：

常用数据集：

* LAION-400M / LAION-5B
* Conceptual Captions (CC3M / CC12M)
* 网络爬取的 alt-text 数据

重要提示：

> 数据质量比模型大小更重要。

---

## 5. 模型架构（标准设置）

### 图像编码器

* ViT-B/32（快速基准）
* ViT-L/14（性能强劲）

### 文本编码器

* Transformer（类似 GPT 编码器堆栈）
* 最大长度通常为 77 个 token（CLIP 标准）

---

## 6. 训练流程

### 步骤 1：数据预处理

每个样本：

```
(image, text caption)
```

对图像进行归一化，对文本进行分词。

---

### 步骤 2：前向传播

```python
img_emb = image_encoder(image)      # [B, d]
txt_emb = text_encoder(text)        # [B, d]
```

归一化：

```python
img_emb = img_emb / ||img_emb||
txt_emb = txt_emb / ||txt_emb||
```

---

### 步骤 3：相似度矩阵

```python
logits = img_emb @ txt_emb.T
logits *= exp(logit_scale)
```

---

### 步骤 4：计算损失

```python
labels = torch.arange(batch_size)

loss_i = cross_entropy(logits, labels)
loss_t = cross_entropy(logits.T, labels)

loss = (loss_i + loss_t) / 2
```

---

## 7. 最小 PyTorch 风格代码

```python id="clip_train_min"
import torch
import torch.nn.functional as F

def clip_loss(image_features, text_features, logit_scale):
    # 归一化
    image_features = F.normalize(image_features, dim=-1)
    text_features  = F.normalize(text_features, dim=-1)

    # 相似度矩阵
    logits = logit_scale * image_features @ text_features.T

    labels = torch.arange(logits.size(0), device=logits.device)

    loss_i = F.cross_entropy(logits, labels)
    loss_t = F.cross_entropy(logits.T, labels)

    return (loss_i + loss_t) / 2
```

---

## 8. 训练技巧（非常重要）

### (1) 大批量大小至关重要

CLIP 高度依赖负样本：

* 256 → 效果弱
* 4096+ → 效果好
* 32k → 达到前沿水平

使用：

* 梯度累积
* 分布式训练（DDP / FSDP）

---

### (2) 困难负样本提升质量

随机负样本太简单 → 学习效果差。

更好的做法：

* 最近邻负样本
* 相同类别图像

---

### (3) 使用强图像编码器

ViT-L/14 是一个折中优选。

---

### (4) 混合精度

使用 FP16 / BF16 加速训练。

---

## 9. 为什么 CLIP 效果如此好

因为它学习到了：

* 语义对齐（而非像素级别）
* 通用视觉概念
* 开放词汇检索

因此现代系统将其用于：

* 图像搜索
* 多模态大语言模型 grounding
* 图像上的 RAG

---

## 10. 如果你想更进一步

我可以向你展示：

* 如何在 **RTX 4070（小规模版本）** 上训练 CLIP
* 如何将 CLIP 扩展为 **SigLIP / 现代对比损失**
* 或者 CLIP 如何成为 **LLaVA / GPT-4V 风格模型的视觉前端**