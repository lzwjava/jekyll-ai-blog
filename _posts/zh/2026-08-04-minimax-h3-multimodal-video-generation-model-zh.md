---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniMax H3：多模态视频生成模型
translated: true
type: note
---

**问题：什么是 MiniMax H3？**

**答案：**

MiniMax H3 是 MiniMax 推出的 **新型多模态生成式 AI 模型**。它主要是一个 **视频生成模型**，而非像 MiniMax M2/M3 那样的文本 LLM。它与字节跳动的 Seedance 和快手的 Kling 等模型竞争。([Reuters][1])

简单来说：

> **H3 = GPT-4o 风格的多模态理解 + Sora 风格的视频生成 + 原生音频生成。**

它可以接受：

```
文本
图像
视频
音频
        ↓
     H3 模型
        ↓
视频 + 立体声
```

能力：

* 文本 → 视频
* 图像 → 视频
* 视频 → 视频编辑
* 参考图像/视频控制
* 运动迁移
* 原生立体声生成
* 最高 2K 分辨率
* 最长 15 秒视频片段 ([Reuters][1])

示例：

输入：

```
一辆特斯拉在夜晚的东京街道上行驶，
雨水倒影，
电影级镜头运动，
日本街道的声音
```

输出：

```
15秒 2K 视频
+
引擎声
+
雨声氛围
+
立体声
```

---

## 架构直觉

H3 不是像 Stable Diffusion 那样的普通扩散模型。

简化的流程：

```
             文本编码器
                  |
图像编码器 ----+
                  |
视频编码器 ----+
                  |
音频编码器 ----+
                  |
            全能 Transformer
                  |
              视频 Token
                  |
              H3 VAE 解码器
                  |
          帧 + 音频波形
```

关键概念：

### 1. 统一的多模态表示

不再是：

```
文本模型
图像模型
音频模型
视频模型

（全部独立）
```

H3 尝试：

```
          多模态上下文

文本
图像
视频
音频

      ↓

共享表示

      ↓

生成
```

这与以下方向类似：

* GPT-4o
* Gemini
* Claude 多模态模型

---

## 人们为何兴奋

有趣的部分在于 **开放权重**。

MiniMax 公开了 H3 权重，这对于前沿视频模型来说并不常见。([Reddit][2])

过去：

```
Sora
Runway
Kling
Veo

仅限 API
```

现在：

```
MiniMax H3

下载权重
↓
本地运行
↓
微调
↓
研究
```

---

## 硬件

这对你来说很有意思。

与 LLM 相比：

```
Qwen3-32B：
~64GB BF16

视频模型：
重得多
```

但 H3 似乎有针对性的优化变体。

社区测试报告称，某些工作流可在 ~12-32GB VRAM 下运行，尽管生成速度可能较慢。([Reddit][3])

你的 RTX 4070 12GB：

可能可行：

```
✔ 实验
✔ 低分辨率
✔ 量化模型

可能：
每分钟数帧
```

不可行：

```
实时视频生成
```

MI300X / A100 级别的机器会是不同的体验。

---

## 与你当前的 FLUX 工作流对比

你一直在玩：

```
FLUX.1-schnell GGUF
stable-diffusion.cpp
```

那是：

```
文本
 ↓
图像
```

H3：

```
文本/图像/视频/音频
 ↓
视频 + 音频
```

这是一个大得多的飞跃。

想想：

```
Stable Diffusion
    |
    v
FLUX
    |
    v
H3
```

从静态图像生成 → 世界模拟。

---

## MiniMax 发布此模型的意义

AI 格局正在演变：

2023：

```
LLM 竞赛
GPT vs Llama
```

2025：

```
推理模型
DeepSeek-R1
o1
```

2026：

```
多模态世界模型

文本
图像
视频
音频
动作
```

H3 是这一转变的一部分。

对于构建 AI 智能体的人来说，有趣的部分不仅仅是视频生成。更大的趋势是：

```
智能体
 |
 |-- LLM 大脑
 |
 |-- 视觉模型
 |
 |-- 视频模型
 |
 |-- 音频模型
 |
 |-- 模拟器
```

H3 更接近"模拟器"组件。

参考文献：

* MiniMax H3 讨论与发布详情 ([Reddit][4])
* MiniMax 官方 Hugging Face 模型 ([huggingface.co][5])
* Reuters：MiniMax H3 视频模型发布 ([Reuters][1])

[1]: https://www.reuters.com/world/china/chinas-minimax-releases-h3-video-model-2026-07-31/?utm_source=chatgpt.com "中国 MiniMax 发布 H3 视频模型"
[2]: https://www.reddit.com/r/LovingOpenSourceAI/comments/1ve5pav/minimax_minimaxh3_is_now_publicly_available/?utm_source=chatgpt.com "MiniMax \"MiniMax-H3 Is Now Publicly Available\" ➡️ MiniMax H3 刚刚发布，附带公开权重，支持本地 768p 视频生成和同步立体声——这个看起来真的很好玩！🚀"
[3]: https://www.reddit.com/r/LocalLLaMA/comments/1ve1mvh/minimaxh3_now_on_huggingface/?utm_source=chatgpt.com "MiniMax-H3 现已登陆 huggingface"
[4]: https://www.reddit.com/r/LocalLLaMA/comments/1vbdsmz/minimaxh3_video_model_released_open_weights/?utm_source=chatgpt.com "MiniMax-H3 视频模型发布，开放权重将在未来几天内推出"
[5]: https://huggingface.co/MiniMaxAI/models?utm_source=chatgpt.com "MiniMaxAI (MiniMax)"
