---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ComfyUI：基于节点的生成式AI工作流
translated: true
type: note
---

问题：什么是ComfyUI？

答案：

ComfyUI 是一个**基于节点的图形界面，用于生成式 AI 图像/视频/音频工作流**，主要用于运行和构建围绕扩散模型（如 Stable Diffusion、FLUX、ControlNet、LoRA、IP-Adapter、AnimateDiff 等）的流水线。

你可以把它理解为**视觉 AI 领域的 PyTorch，但带有图形编辑器**。

不需要写：

```python
prompt
  -> text encoder
  -> diffusion model
  -> sampler
  -> VAE decoder
  -> image
```

而是以可视化方式构建相同的流水线：

```
[加载检查点]
        |
        v
[CLIP 文本编码] <--- 提示词
        |
        v
[KSampler]
        |
        v
[VAE 解码]
        |
        v
[保存图像]
```

每个方框都是一个节点。你可以在节点之间连接张量。

---

## 为什么人们使用 ComfyUI

### 1. 对推理图的完全控制

普通应用：

```
提示词 -> 图像
```

ComfyUI：

```
提示词
 |
CLIP
 |
正向条件
 |
ControlNet
 |
LoRA
 |
IP Adapter
 |
采样器
 |
调度器
 |
VAE
 |
图像
```

你可以修改每一步。

这与以下工具类似：

* TensorFlow 图模式
* Unreal Blueprint
* Blender 节点编辑器
* LangGraph（用于智能体）

---

## 2. 可重现的工作流

ComfyUI 的工作流就是 JSON。

示例：

```json
{
  "nodes": [
    {
      "type": "CheckpointLoader",
      "model": "flux-dev"
    },
    {
      "type": "KSampler",
      "steps": 30,
      "cfg": 4
    }
  ]
}
```

你可以分享这个 JSON，其他人就能得到相同的流水线。

这就是研究人员和创作者喜欢它的原因。

---

## 3. 本地运行

典型设置：

```
GPU
 |
CUDA / ROCm
 |
PyTorch
 |
ComfyUI
 |
模型
```

示例：

```bash
git clone https://github.com/comfyanonymous/ComfyUI

cd ComfyUI

pip install -r requirements.txt

python main.py
```

打开：

```
http://localhost:8188
```

---

## 硬件要求

大致如下：

| GPU             | 体验                              |
| --------------- | --------------------------------- |
| RTX 3060 12GB   | 还行                              |
| RTX 4070 12GB   | 良好                              |
| RTX 3090 24GB   | 优秀                              |
| RX 7900 XT 20GB | 可能可行 (ROCm)                   |
| MI50 16GB       | 技术上有趣但痛苦                  |
| H100            | 性能过剩                          |

你的 RTX 4070 + MI50 实验与此相关：

* RTX 4070 → 最简单的 ComfyUI 体验
* MI50 → ROCm 兼容性实验，不适合日常生成

---

## 流行工作流

### 文本 → 图像

```
提示词
 |
FLUX / SDXL
 |
KSampler
 |
图像
```

### 图像 → 图像

```
输入照片
 |
VAE 编码
 |
扩散
 |
VAE 解码
 |
新图像
```

### 角色一致性

```
参考图像
       |
IP Adapter
       |
LoRA
       |
FLUX/SDXL
       |
生成的角色
```

### 视频生成

```
文本
 |
AnimateDiff / Wan / CogVideo
 |
帧
 |
视频
```

---

## ComfyUI vs Automatic1111

|                     | ComfyUI   | Automatic1111 |
| ------------------- | --------- | ------------- |
| 对新手友好          | ❌         | ✅             |
| 控制                | ⭐⭐⭐⭐⭐     | ⭐⭐⭐           |
| 研究工作流          | ⭐⭐⭐⭐⭐     | ⭐⭐            |
| 自动化              | ⭐⭐⭐⭐⭐     | ⭐⭐            |
| API 使用            | 优秀       | 一般           |
| 复杂流水线          | 优秀       | 有限           |

对于工程师来说，ComfyUI 通常是更好的选择。

---

## 为什么它对 AI 工程师很重要

ComfyUI 本质上是一种**用于生成模型的视觉编程语言**。

核心概念：

LLM：

```
tokens
 ↓
Transformer
 ↓
tokens
```

扩散模型：

```
噪声
 ↓
UNet / DiT
 ↓
去噪后的潜变量
 ↓
图像
```

ComfyUI 暴露了整个前向传播过程。

对于从事模型训练/推理的人来说，它很有用，因为你可以尝试：

* 不同的采样器
* 条件方法
* LoRA 合并
* 量化模型
* ControlNet
* 图像/视频流水线

而无需编写整个应用。

---

鉴于你的背景（nanoGPT、ROCm、GPU 实验），ComfyUI 很可能值得一试。有趣的部分不是 UI，而是理解**扩散计算图**以及像交换 Transformer 块一样交换组件。