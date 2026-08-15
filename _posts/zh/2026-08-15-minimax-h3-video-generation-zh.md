---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniMax-H3 视频生成
translated: true
type: note
---

## 问题：MiniMaxAI/MiniMax-H3 介绍

## 回答

MiniMax 的 **MiniMax-H3** 是一个专注于**视频生成**的**大规模全模态生成式 AI 模型**，它将**文本、图像、视频和音频的理解/生成**整合在同一系统中。这是中国前沿的多模态模型之一，与 OpenAI Sora、Google DeepMind Veo、字节跳动/快手视频模型等竞争。（[MiniMax][1]）

![Image](https://images.openai.com/static-rsc-4/veZv0LvNq-Uou8CSgSCOijkTOwig-VT9wbJN2R7hwacN_w_iICw1OEmVStwfb4QrASvWgB6fK46NoJhcW9Yh18tuhAekyp_pxBIWFcHPYB1cV3-yLjSBoZThgKJE55-TbPyTktbEWI5Fkp1WxYZQoZsGqQrKb88migs0BmmbDrEyv1HaH6MHPsA0cnQN61lw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yrap5FMEREyvKvufuDJzMGgCCdmRQEtmcRjTgP8L-c0NLN5DDxHxhlan4bql1036yKy8JyTaszoeiAaonv6ZwseD2FwSRJYPMygcugVxoz2J14kD16083ja22i2GcJ8jSx5fDvQIDCk_iFrtD9EEW1KJcrDnk0U2tiIPLwIsQfWRpU7owRLM1MYFL_7jVGcp?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0VYGhrav5Xacr-tjW0ttCRj_Mr3c11kLEtP5GNs-diE9uhEAw3MUeuYAd0kmtIZ_Rf2FtooOUNNvB7f7k9653VyiOM940mvh7fES_3KzkY8poFMDX734HhdSu7qFp8zgzLAttDYbkneyLxDAHBIDRmNgLHWoyNz48QkNyaN-UacGnc5LkwQDdceBtnQkoBN1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2cPwQukpqvafkulf6dxJNa0R5H8ypCsohHfFMo7rN2hXowlCPmu6lGWEkjvmumc7BP0scuMLJ_4MJkWm-CGTRpCIo78AqKVlIhlq-DA_hvoMzN3FiFst1O-t4-OUDk3cwxysYbDOOp_IgWeporf--zc9X-bALMJVji6MVdOqWcwF8RDJ1H5nHwp_QNIy3n65?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/y5weH9t8rR4kRKzophsAkKo8w17fgZJxWgae6eIeN4Yz80nW8OWDzgoHo09KyapNWqUuAi1wQDxuAaXGCc62RiC7JlS9FTgJqh9invsGwBPPaOJDusGhpWjiGg3zJkTWOdC4l2oTqus28NtnBAlzN7kRlAMEUUaD44bymkx992yvVoUr8RZdwGP0_In4Bh4o?purpose=fullsize)

### 1. H3 是什么？

H3 并非像 Qwen/DeepSeek/MiniMax-M3 那样的 LLM，它更接近于一个**视频基础模型**。

目标：

```
输入：
  文本提示
  图像
  视频
  音频

        ↓

   MiniMax-H3

        ↓

输出：
  视频 + 原生立体声
```

它可以做到：

* 文本 → 视频（T2V）
* 图像 → 视频（I2V）
* 参考视频 → 新视频
* 视频编辑
* 运动迁移
* 多模态指令跟随

它支持生成最高**2K 分辨率、约 15 秒**的视频，包括原生立体声生成。（[MiniMax][1]）

---

## 2. 架构思路（高层）

像 H3 这样的现代视频模型通常由几个组件构建而成：

```
文本编码器
      |
      v
多模态表示
      |
      v
视频潜在表示
      |
      v
视频 Transformer / 扩散 Transformer
      |
      v
VAE 解码器
      |
      v
视频帧 + 音频
```

类似家族：

```
Stable Diffusion:
 文本 → 潜在图像扩散 → 图像

Sora / H3:
 文本 + 视频 token → 时空 Transformer → 视频 token
```

困难之处不在于生成一张图像。

视频是：

```
帧：

F1 F2 F3 F4 ... Fn

每帧：
H × W × RGB

加上：

时间一致性
运动
物理
物体身份
音频同步
```

一个 10 秒 24fps 的视频：

```
10 × 24 = 240 帧
```

模型必须保持：

* 同一人物身份
* 一致的光照
* 真实的运动
* 摄像机移动
* 物体交互

---

## 3. 为什么 H3 在技术上值得关注

### A. 统一的多模态上下文

传统流程：

```
文本模型
   +
图像模型
   +
音频模型
   +
视频模型

分离的系统
```

H3 尝试：

```
文本
图像
视频
音频

       ↓

一个多模态表示
```

MiniMax 将这一方向描述为统一的多模态生成架构。（[MiniMax][1]）

---

### B. 原生音频生成

许多视频系统这样做：

```
生成视频

+

事后添加音频
```

H3 尝试：

```
视频生成
        +
音频生成

联合进行
```

意味着：

```
人物说话

嘴部运动
        +
声音
        +
背景音

同步对齐
```

（[Kylon][2]）

---

## 4. 与 MiniMax 其他模型的关系

MiniMax 有多个模型系列：

```
MiniMax
│
├── M 系列
│     ├── MiniMax-M1
│     ├── MiniMax-M2
│     └── MiniMax-M3
│
└── H 系列
      └── MiniMax-H3
```

M 系列：

```
LLM
代码
推理
智能体
```

H3：

```
视频生成
多模态创造力
```

Hugging Face 上的 MiniMax 组织目前托管了包括 M 系列模型在内的多个模型家族。（[Hugging Face][3]）

---

## 5. 开放权重的重要性

H3 之所以引起关注，是因为 MiniMax 开始发布模型权重/提供开放访问，而不仅仅是 API 访问。这一点很重要，因为视频模型通常是封闭的。

开放模型使得：

```
研究人员：
    ↓
微调
    ↓
专用视频模型

公司：
    ↓
私有化部署

开发者：
    ↓
ComfyUI 工作流
```

社区集成迅速出现，包括 ComfyUI 支持。（[Reddit][4]）

---

## 6. 硬件直觉

视频生成比 LLM 推理重得多。

比较：

### Qwen/DeepSeek LLM

```
token：

hello world ...
```

### 视频模型

```
token：

帧1：
xxxxxxxx

帧2：
xxxxxxxx

帧3：
xxxxxxxx

...
```

时间维度导致内存爆炸。

粗略预期：

* 16GB GPU: 困难
* 24GB GPU: 通过优化可能运行
* 32GB+ GPU: 好得多
* 多 GPU: 生产环境

社区报告显示，根据设置，较小的工作流可以在约 20GB 左右运行，但高分辨率生成成本高昂。（[Reddit][5]）

---

## 7. 为什么这对 AI 工程师重要

从研究角度看，H3 代表了下一个转型：

```
2018：
GPT
（仅文本）

2020：
DALL-E
（文本 → 图像）

2023：
扩散视频

2025+：
全模态模型

（文本 + 图像 + 视频 + 音频）
```

前沿正在从：

> “预测下一个 token”

转向：

> “学习一个世界模拟器”

视频模型之所以有趣，是因为它们迫使模型学习：

* 物理
* 因果
* 3D 结构
* 人体运动
* 环境动态

对于从事 LLM 基础设施的人来说，H3 是下一代架构的一个好例子：**Transformer + 多模态 tokenization + 潜在世界建模**。

参考文献：

* [MiniMax H3 公告](https://minimaxi.com/blog/minimax-h3?utm_source=chatgpt.com)
* [MiniMax Hugging Face 组织](https://huggingface.co/MiniMaxAI?utm_source=chatgpt.com)
* [MiniMax H3 实践指南](https://kylon.io/blog/minimax-h3-guide-2026?utm_source=chatgpt.com)

[1]: https://minimaxi.com/blog/minimax-h3?utm_source=chatgpt.com "MiniMax H3：打破任务和模态的边界 - MiniMax Research | MiniMax"
[2]: https://kylon.io/blog/minimax-h3-guide-2026?utm_source=chatgpt.com "MiniMax H3 Guide: Open-Weight Multimodal Video, API, and License"
[3]: https://huggingface.co/MiniMaxAI?utm_source=chatgpt.com "MiniMaxAI (MiniMax)"
[4]: https://www.reddit.com/r/StableDiffusion/comments/1ve1756/day_0_minimax_support_for_comfyui/?utm_source=chatgpt.com "Day 0 MiniMax Support for ComfyUI"
[5]: https://www.reddit.com/r/LocalLLaMA/comments/1ve1mvh/minimaxh3_now_on_huggingface/?utm_source=chatgpt.com "MiniMax-H3 now on huggingface"
