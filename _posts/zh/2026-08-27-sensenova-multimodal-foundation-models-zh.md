---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SenseNova 多模态基础模型
translated: true
type: note
---

问题：SenseNova（Hugging Face 组织）简介

回答：

商汤科技的 SenseNova 是其基础模型系列。Hugging Face 组织 `sensenova` 发布了多模态 AI、视觉语言模型、图像生成和智能体系统方面的开源模型。（[Hugging Face][1]）

可以把 SenseNova 看作是中国对标 **GPT-4o / Gemini 风格的多模态基础模型栈** 的尝试：

```
SenseNova
├── 语言模型
│   └── 推理 / 对话 / 智能体
│
├── 视觉语言模型
│   └── 理解图像 + 文本
│
├── 统一多模态模型
│   └── 输入：文本/图像
│   └── 输出：文本/图像/混合生成
│
├── 图像生成
│   └── 文本 → 图像
│   └── 图像编辑
│
└── 智能体生态系统
    └── 工具 + 工作流
```

（[Sensenova][2]）

## 公司背景

SenseNova 来自商汤科技（SenseTime），成立于 2014 年。商汤最初以计算机视觉闻名：

* 人脸识别
* 自动驾驶感知
* 智慧城市摄像头
* 工业视觉

在 ChatGPT（2022）之后，他们大力转向基础模型：

```
旧商汤科技：
计算机视觉
       ↓
深度学习感知模型
       ↓
行业 AI

新商汤科技：
大规模计算
       ↓
基础模型
       ↓
多模态智能体
       ↓
企业级 AI
```

（[SenseTime][3]）

---

## 有趣的 Hugging Face 模型

该 HF 组织目前包含以下模型：（[Hugging Face][1]）

### 1. SenseNova-U1

示例：

```
sensenova/SenseNova-U1-8B-MoT
```

这是他们的统一多模态模型。

MoT = Mixture of Tokens（令牌混合）。

其理念：

传统方式：

```
图像
 ↓
视觉编码器
 ↓
LLM
 ↓
文本回答
```

统一模型：

```
图像令牌
文本令牌
音频/视频令牌
       ↓
 Transformer
       ↓
文本令牌
图像令牌
```

与以下方向类似：

* GPT-4o
* Gemini
* Chameleon
* BAGEL
* NEO-unify

商汤将 U1 描述为使用其 NEO-unify 架构的统一理解与生成模型。（[SenseTime][4]）

---

### 2. SenseNova-Vision

视觉语言模型：

```
图像 + 问题
        ↓
SenseNova-Vision
        ↓
答案
```

示例：

输入：

```
<image>
这是什么 GPU？
```

输出：

```
这看起来像是一块 NVIDIA RTX 4090...
```

类似类别：

* Qwen2.5-VL
* InternVL
* LLaVA
* GPT-4V

---

### 3. SenseNova-SI

空间智能模型。

这很有趣，因为它从：

```
"图像里有什么？"
```

转变为：

```
"物体的 3D 关系是什么？"
```

示例：

```
机器人摄像头图像

→
杯子在哪里？
距离多远？
机器人能抓住它吗？
```

这与具身 AI 相关联。

---

### 4. SenseNova-MARS

面向推理的多模态模型。

方向：

```
视觉
+
语言
+
推理
```

类似趋势：

* OpenAI o 系列
* DeepSeek-R1
* Gemini 思考模型

---

## 为什么 SenseNova 在技术上有趣

重要的转变：

以前：

```
独立模型

CLIP
 +
LLM
 +
Diffusion
 +
语音模型
```

现在：

```
一个基础模型

          Transformer
        /     |      \
    文本    图像    动作
```

行业正朝着**原生多模态模型**发展。

你之前的实验，例如：

* nanoGPT
* GPT-2 训练
* FLUX
* Qwen-VL

恰好触及了这个方向。

---

## 如何运行/研究它

例如：

```bash
git clone https://huggingface.co/sensenova/SenseNova-U1-8B-MoT

pip install transformers accelerate

python inference.py
```

概念上：

```python
image = load_image("gpu.jpg")

tokens = processor(
    text="识别这个 GPU",
    image=image
)

output = model.generate(tokens)

print(output)
```

有趣的工程部分：

1. 多模态分词

```
图像
 ↓
块嵌入
 ↓
视觉令牌
```

2. transformer 注意力机制

```
[文本令牌]
      +
[图像令牌]

      ↓

 自注意力

      ↓

推理
```

3. 统一生成

```
输出：
"文本"
或
"图像令牌"
```

---

## 与 Qwen / DeepSeek 的比较

粗略对比图：

| 模型系列   | 主要优势                         |
| ---------- | -------------------------------- |
| Qwen       | 开放通用 LLM + 多模态            |
| DeepSeek   | 推理 + 高效训练                  |
| SenseNova  | 视觉 + 多模态 + 企业级 AI        |
| InternVL   | 强大的视觉语言研究               |
| GPT-4o     | 闭源多模态产品                   |

SenseNova 的历史优势是**计算机视觉**，因此他们的赌注是：

```
视觉 AI 专业知识
        +
大型语言模型
        +
智能体
        =
物理世界 AI
```

（[SenseTime][5]）

对于像你这样喜欢 **GPU 维修 + 硬件 + AI** 的人来说，SenseNova 的方向实际上非常相关：未来的"AI 工程师"技术栈很可能不仅仅包括训练 transformer，还会连接：

```
摄像头
 ↓
多模态模型
 ↓
推理
 ↓
机器人/工具/动作
 ↓
物理世界
```

参考：

* SenseNova Hugging Face 模型：([Hugging Face][1])
* 商汤科技概览：([SenseTime][3])
* SenseNova 模型平台：([Sensenova][6])

[1]: https://huggingface.co/sensenova/models?utm_source=chatgpt.com "sensenova (SenseNova)"
[2]: https://www.sensenova.ai/models?utm_source=chatgpt.com "模型 — SenseNova 多模态 AI 模型平台"
[3]: https://www.sensetime.com/en/about-index?utm_source=chatgpt.com "关于商汤科技 | SenseTime"
[4]: https://sensetime.com/en/news/51170625/?utm_source=chatgpt.com "商汤科技全面开源 SenseNova U1：统一理解与生成模型 | SenseTime"
[5]: https://sensetime.com/en/?utm_source=chatgpt.com "商汤科技 | SenseNova 多模态 LLM 与 AI 解决方案"
[6]: https://www.sensenova.ai/?utm_source=chatgpt.com "SenseNova - 多模态 AI 模型平台"
