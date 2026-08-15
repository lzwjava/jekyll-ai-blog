---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'MiniMax-H3: 统一视频基础模型'
translated: true
type: note
---

## 问题：MiniMax-H3 有多好？

## 答案

简短版：**MiniMax-H3 是向“世界模拟器”风格模型迈出的非常令人印象深刻的一步，尤其来自中国 AI 实验室。它不仅仅是一个更好的视频生成器，其有趣之处在于统一的多模态架构。** ([MiniMax][1])

我会将其重要性排序如下：

```
LLM 时代：
GPT-3 → GPT-4 → Claude → DeepSeek

图像时代：
DALL-E → Stable Diffusion → Midjourney

视频时代：
Sora → Veo → Kling → MiniMax-H3
```

H3 是最后一类中的严肃前沿尝试之一。 ([MiniMax][1])

---

## 1. 令人印象深刻的部分：它更接近“视频基础模型”

旧流程：

```
文本 LLM
   |
   v
提示理解

+

视频扩散模型
   |
   v
帧

+

音频模型
```

许多系统是拼接在一起的。

H3 尝试：

```
文本
图像
视频
音频

      |
      v

全能 Transformer

      |
      v

视频 + 立体声
```

MiniMax 表示 H3 使用统一的多模态表示，可以生成带有原生立体声的视频，最高可达 2K 分辨率和 15 秒。 ([MiniMax][1])

这很重要。

---

## 2. 为什么视频比 LLM 难得多

对于 LLM：

```
token1 token2 token3 token4
```

模型学习：

```
P(下一个 token | 之前的 token)
```

对于视频：

```
帧1
帧2
帧3
...
帧300
```

模型需要：

### 物体恒存性

示例：

```
一个女性走进房间。

帧1：
女性穿红色夹克

帧100：
仍然是红色夹克
同一张脸
同一个身体
```

### 物理

```
球落下

不是：

球随机瞬移
```

### 摄像机理解

```
放大
向左平移
摄像机抖动
景深
```

### 音频同步

```
嘴巴动作
      +
声音
      +
环境音
```

这更接近于学习一个简化的物理模拟器。

---

## 3. H3 看起来最强的方面

### A. 可控性

这可能最重要。

随机生成漂亮的视频很容易。

可控的视频很难。

示例：

提示：

```
一辆特斯拉在东京街道上行驶。

摄像机：
慢速推轨镜头

天气：
雨

音频：
交通声 + 雨声 + 引擎声
```

模型需要遵守所有约束。

MiniMax 强调指令遵循、文本/标志渲染、视频到视频运动迁移和可控编辑等领域。 ([MiniMax][1])

---

### B. 参考视频编辑

这非常强大：

```
输入：

你孩子的画作

+

提示：

将其变成皮克斯风格的动画
```

或：

```
输入：

一个跳舞的人

输出：

同一个人
不同的环境
不同的风格
```

这就是视频 AI 对创作者变得有用的地方。

---

## 4. 与 Sora / Veo / Kling 相比

我的大致看法：

| 模型       | 优势                              |
| ---------- | --------------------------------- |
| OpenAI Sora | 世界模拟，电影级质量              |
| Google Veo  | 逼真度，制作级视频                |
| Kling       | 消费者创作者生态系统              |
| MiniMax-H3  | 开放生态系统 + 多模态控制         |

H3 最大的优势是开放性和开发者生态系统。已经有社区集成，如 ComfyUI 工作流。 ([Reddit][2])

---

## 5. 研究意义

对于 AI 工程师来说，有趣的问题是：

“未来的模型还会是 LLM 吗？”

也许不是。

轨迹：

```
2017 Transformer

        ↓

2020 GPT

        ↓

2023 多模态 GPT-4

        ↓

2024 视频生成

        ↓

2026 全能世界模型
```

下一个前沿：

```
模型理解：

语言
视觉
音频
运动
空间
物理

并能生成后果。
```

这就是为什么像 Yann LeCun 这样的人谈论世界模型。

---

## 6. 弱点

它不是 AGI。

当前的视频模型仍然存在问题：

* 长期一致性
* 复杂推理
* 精确物理
* 交互环境
* 持久记忆

示例：

生成：

```
一个人在 10 年内建造一座房子。
```

当前模型无法维持：

```
同一个人
同一个房屋结构
同一时间线
```

对于长时间跨度。

---

## 7. 对于作为 LLM 工程师的你

我认为 H3 实际上比另一个 400B 的 LLM 更有趣。

下一个技能栈可能变成：

```
Transformer
+
LLM 训练
+
扩散 / 流匹配
+
VAE
+
多模态分词
+
视频 Transformer
+
GPU 优化
```

核心思想仍然相似：

```
token → Transformer → 预测
```

但现在 token 是：

```
文本 token
图像 token
视频潜变量 token
音频 token
```

“下一个 GPT” 可能不仅仅写代码。

它可能模拟一个世界，并同时生成代码、视频、UI 和环境。

参考文献：

* MiniMax H3 公告：([MiniMax][1])
* MiniMax Hugging Face 组织：([huggingface.co][3])
* MiniMax H3 社区 ComfyUI 集成：([Reddit][2])

[1]: https://minimaxi.com/blog/minimax-h3?utm_source=chatgpt.com "MiniMax H3：打破任务和模态的边界 - MiniMax Research | MiniMax"
[2]: https://www.reddit.com/r/StableDiffusion/comments/1ve1756/day_0_minimax_support_for_comfyui/?utm_source=chatgpt.com "Day 0 MiniMax 对 ComfyUI 的支持"
[3]: https://huggingface.co/MiniMaxAI?utm_source=chatgpt.com "MiniMaxAI (MiniMax)"
