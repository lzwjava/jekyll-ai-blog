---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多模态大语言模型训练流水线
translated: true
type: note
---

问题：如何为大型语言模型（LLM）训练一个多模态模型？

答案：

训练一个多模态 LLM（例如，文本+图像，或文本+音频+视频）基本上是**将一个预训练的模态编码器与一个语言模型连接起来，并训练它们在共享表示空间中对齐**。

以下是现代系统中使用的实用管线，如 GPT-4V 风格模型、LLaVA、Flamingo 等。

---

## 1. 整体架构

典型的多模态 LLM 包含三个部分：

### (1) 模态编码器（冻结或轻量训练）

* 图像：ViT (Vision Transformer)、CLIP-ViT
* 音频：Whisper 编码器 / wav2vec
* 视频：TimeSformer / VideoViT

示例：

* `image → ViT → 1024-d embeddings`

---

### (2) 投影 / 适配层

该层将模态嵌入映射到 LLM 的嵌入空间。

常见设计：

* 线性层
* MLP（2–3 层）
* Perceiver Resampler（Flamingo 风格）
* Q-Former（BLIP-2 风格）

示例：

```
vision_features (2048) → projector → 4096 (LLM hidden size)
```

---

### (3) 语言模型（解码器）

* LLaMA / Qwen / Mistral / GPT 风格的解码器-only Transformer
* 通常预训练，初期部分冻结

---

## 2. 训练阶段

### 阶段 A：对齐预训练（最重要）

目标：教会模型“连接视觉/音频 → 文本 token”

在配对数据上训练：

* image → caption
* image + question → answer
* video → description

损失函数：

* 标准下一个 token 预测（交叉熵）

示例：

```
输入: <image> "What is in the image?"
目标: "A dog running in a park"
```

---

### 阶段 B：多模态指令微调

现在让它具备对话能力：

数据集：

* LLaVA-Instruct
* MiniGPT-4 数据
* ShareGPT 风格的多模态问答
* 合成的 GPT 生成字幕 + 问答

目标：

* 遵循涉及图像/音频的指令

---

### 阶段 C：可选强化学习（RLHF / DPO）

* 提升推理质量
* 减少幻觉
* 使回答与人类偏好对齐

---

## 3. 数据需求

你需要大规模配对数据集：

### 视觉-语言

* LAION-5B（过滤后）
* COCO captions
* CC3M / CC12M
* 合成的 GPT 字幕生成

### 指令数据

* GPT 生成的图像问答对
* 人工标注的 VQA 数据集

关键点：

> 在指令微调阶段，质量比数量更重要。

---

## 4. 常见训练方案（现代实践）

### 方案 1：LLaVA 风格（最简单）

* 冻结视觉编码器
* 冻结 LLM（或部分 LoRA）
* 先只训练投影层
* 然后进行指令微调整个系统

---

### 方案 2：BLIP-2 风格

* 冻结视觉编码器
* 训练 Q-Former（桥接模块）
* 冻结 LLM

对于有限的计算资源非常高效。

---

### 方案 3：Flamingo 风格

* 在 LLM 中插入交叉注意力块
* 训练门控交叉注意力层
* 性能强但更复杂

---

## 5. 损失函数

主要损失：

* 下一个 token 预测（因果 LM 损失）

可选：

* 对比损失（类似 CLIP 的图像-文本对齐）
* 排序损失（用于 VQA 正确性）
* 偏好损失（DPO/RLHF）

---

## 6. 最小 PyTorch 概念

高级流程：

```python
image_features = vision_encoder(image)
projected = projector(image_features)

text_embeddings = tokenizer(text)

inputs = concat(projected, text_embeddings)

loss = language_model(inputs, labels)
loss.backward()
```

---

## 7. 关键工程挑战

### (1) 对齐不稳定性

* 如果投影器太弱，视觉嵌入会坍塌

### (2) Tokenization 不匹配

* 需要特殊的“图像 token”或前缀嵌入

### (3) 对字幕过拟合

* 模型变成“字幕机器人”而非推理

### (4) 计算成本

* 多模态训练内存开销大（尤其是视频）

---

## 8. 推荐起步技术栈（实用）

如果你想自己搭建：

* 视觉编码器：`openai/clip-vit-large-patch14`
* LLM：`LLaMA 3 / Qwen2.5`
* 框架：

  * HuggingFace Transformers
  * DeepSpeed / FSDP
  * LLaVA 仓库（最佳参考基线）

---

## 9. 最佳学习路径

1. 训练 CLIP（图像-文本对比）
2. 训练字幕生成模型
3. 构建 LLaVA 风格 VQA 系统
4. 添加指令微调
5. 扩展到多图像 / 视频

---

如果你需要，我还可以展示：

* **一个最小可运行的 LLaVA 训练代码**
* 如何在 **1× RTX 4070** 上完成
* 或者 GPT 风格模型如何**内部注入图像 token**
