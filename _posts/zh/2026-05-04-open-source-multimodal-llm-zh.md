---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源多模态大语言模型项目
translated: true
type: note
---

以下是**精心挑选且实用的真实开源项目清单**，可用于学习、克隆并构建小型多模态LLM系统（图像/视频+语言）。我已按**学习 → 训练 → 扩展**的实用价值进行分类。

---

# 🧠 1. 最佳入门级多模态LLM（图像+文本）

## 🔹 LLaVA（必学项目）

* GitHub: [https://github.com/haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA)
* 核心思路：视觉编码器 + LLM + 投影层
* 你能学到：

  * GPT-4V 风格模型的构建方法
  * 如何使用 LoRA 进行微调
  * 图像特征如何与LLM词元连接

👉 这是**多模态LLM的“Hello World”**

---

## 🔹 BLIP-2 / InstructBLIP

* 图像 → 文本推理的强大基线
* 采用冻结视觉编码器 + 冻结LLM + Q-former桥接

为什么重要：

* 训练方案非常稳定
* 计算需求远低于全参数微调

---

# 🎥 2. 最佳开源视频LLM项目（你的主要关注点）

## 🔹 Video-LLaVA（强烈推荐）

* 仓库: [https://github.com/PKU-YuanGroup/Video-LLaVA](https://github.com/PKU-YuanGroup/Video-LLaVA) ([SourcePulse][1])
* 论文风格：EMNLP 2024 风格系统

功能特点：

* 将LLaVA扩展至视频
* 对齐视频帧 → LLM推理

优点：

* 架构清晰
* 适用于视频问答/描述生成
* 适合小规模训练实验

---

## 🔹 LLaMA-VID

* 仓库: [https://github.com/dvlab-research/LLaMA-VID](https://github.com/dvlab-research/LLaMA-VID) ([SourcePulse][2])

核心思路：

* 将长视频压缩为“上下文词元”
* 支持长达数小时的视频推理

实用价值：

* 学习长上下文多模态设计
* 探索“视频记忆”研究方向的优质案例

---

## 🔹 PLLaVA（轻量级视频扩展）

* 仓库: [https://github.com/magic-research/PLLaVA](https://github.com/magic-research/PLLaVA) ([Hugging Face][3])

核心思路：

* 图像LLaVA的“免参数”视频扩展
* 从图像模型到视频模型的高效适配

为什么重要：

* 极低计算需求，极具实用性
* 适合在1-2块GPU上进行实验

---

# 🧱 3. 强大的视频基础模型（用于特征提取）

这些并非小型训练项目，但作为骨干模型极具价值：

## 🔹 InternVideo（非常重要的生态系统）

* 仓库: [https://github.com/OpenGVLab/InternVideo](https://github.com/OpenGVLab/InternVideo) ([GitHub][4])

提供资源：

* 视频编码器（基于ViT）
* 预训练的视频表征
* 大规模数据集 + 预训练模型

为什么值得关注：

* 可冻结此模型并基于其构建自己的LLM
* 相当于“视频领域的CLIP”

---

## 🔹 InternVideo2 / InternVid数据集

* 700万+视频，超大规模数据集 ([InternVideo][5])

重要性：

* 相当于“视频领域的FineWeb”
* 为数据集工程提供灵感

---

# 🧪 4. 极简/可快速修改的多模态框架

## 🔹 nanoVLM（非常适合学习）

* 轻量级VLM（约750行概念代码）
* 可在Colab级别GPU上运行

重要性：

* 以最小代码展示完整流程
* 适合“构建自己的多模态LLM”学习

---

# 🧠 5. 最佳“实战训练栈”（建议采用方案）

如果你的目标是**小型多模态LLM训练项目**，最佳组合如下：

### ⭐ 推荐技术栈

* 视觉编码器：CLIP / SigLIP / InternVideo特征
* LLM：LLaMA 3 / Qwen 2.5（小版本）
* 连接器：MLP投影器或Q-former
* 训练方法：LoRA / QLoRA
* 数据集：

  * WebVid
  * MSR-VTT
  * COCO captions

---

# 🚀 6. 基于这些仓库的最佳项目创意

如果你想进行“可实际构建的项目”：

### 1. 视频问答助手

使用：

* Video-LLaVA + LoRA

### 2. “视频版FineWeb”

构建：

* 数据集爬虫 + 过滤 + 去重流程

### 3. 长视频记忆模型

使用：

* LLaMA-VID风格的压缩思路

### 4. 轻量级多模态聊天机器人

使用：

* LLaVA + 小型LoRA微调

---

# ⚡ 关键洞察（重要提示）

实际上你无需**“从头训练视频LLM”**。

现代成功公式是：

> **冻结的预训练编码器 + 小型可训练适配器 + 高质量数据集工程**

这正是 Video-LLaVA、InternVideo2 和 PLLaVA 等系统的工作原理。

---

如需下一步指导，我可为你设计：

* **一周构建计划**
* 精确的**GPU成本估算**
* 或首个多模态视频LLM的**最小仓库架构（目录结构 + 代码骨架）**

随时告诉我需求 👍

[1]: https://www.sourcepulse.org/projects/1853092?utm_source=chatgpt.com "Video-LLaVA by PKU-YuanGroup - SourcePulse"
[2]: https://www.sourcepulse.org/projects/1842220?utm_source=chatgpt.com "LLaMA-VID by dvlab-research - SourcePulse"
[3]: https://huggingface.co/ermu2001/pllava-7b?utm_source=chatgpt.com "ermu2001/pllava-7b · Hugging Face"
[4]: https://github.com/opengvlab/internvideo?utm_source=chatgpt.com "GitHub - OpenGVLab/InternVideo: [ECCV2024] Video Foundation Models & Data for Multimodal Understanding · GitHub"
[5]: https://internvideo.github.io/?utm_source=chatgpt.com "InternVideo"
