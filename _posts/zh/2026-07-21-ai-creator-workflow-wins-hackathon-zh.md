---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI创作者工作流赢得黑客马拉松
translated: true
type: note
---

问题：如何通过强有力的项目策略在 AMD Radeon 黑客马拉松赛道 1（多模态 AI）中获胜？

答案：

对于赛道 1，评委将 **80% 的分数分配给产品价值与创新**，仅 **20% 分配给 Radeon GPU 性能**。因此，不要构建“又一个 Stable Diffusion 界面”。获胜策略是：

> 构建一个能解决实际问题的完整 AI 创作者工作流，然后证明它在 AMD Radeon 上高效运行。

思考方向是 **AI 原生产品**，而非模型演示。

## 获胜项目思路：“面向创作者的 AI 视频工厂”

一个流水线：

```
创意 / 脚本
      |
      v
LLM 故事规划器
      |
      v
文本 -> 图像（场景生成）
      |
      v
图像 -> 视频（运动生成）
      |
      v
语音生成
      |
      v
自动字幕 + 剪辑
      |
      v
最终短视频 / Reels / TikTok 视频
```

一键操作：

```
“创建一个 30 秒的特斯拉 AI 新闻视频”
```

输出：

* 故事板
* 图像
* 动画视频
* 旁白
* 字幕
* 缩略图

这涵盖了：

* 文生图 ✅
* 图像编辑 ✅
* 图生视频 ✅
* 音频生成 ✅
* 创作者应用 ✅

---

## 为什么这能击败竞争对手

大多数黑客马拉松提交的作品将是：

* Stable Diffusion 封装
* 带图像生成的聊天机器人
* 简单的 ComfyUI 工作流

这些都是同质化的。

你的差异化：

### “AI 内容工厂”

目标用户：

* YouTuber
* TikTok 创作者
* 营销团队
* 独立创业者

痛点：

> 每天制作视频内容需要 3-5 小时。

解决方案：

> 从一个创意生成 10 条短视频/天。

---

# 架构

## 前端

简单：

```
React
 |
 |
FastAPI
 |
 |
工作流引擎
```

---

## AI 流水线

### 1. LLM 规划器

输入：

```
主题：
“解释 AMD MI300X”
```

输出：

```json
{
 "scenes":[
   {
    "duration":5,
    "image_prompt":
    "数据中心内的 AMD MI300X GPU"
   }
 ]
}
```

模型：

* Qwen
* Llama
* DeepSeek

---

### 2. 文生图

使用：

* Stable Diffusion XL
* FLUX
* SD3

示例：

```
提示词
 |
v
扩散模型
 |
v
1024x1024 图像
```

---

### 3. 图生视频

这是你的制胜点。

使用：

* Stable Video Diffusion
* AnimateDiff
* CogVideoX
* Wan2.1

流水线：

```
图像
 |
编码器
 |
时序 Transformer
 |
视频帧
```

生成：

```
1 张图像

↓

16-24 帧

↓

mp4
```

---

### 4. 音频

使用：

* Whisper
* XTTS
* CosyVoice

---

# Radeon 优化部分（20 分）

这一点很重要。

不要只说：

“可在 AMD 上运行”

要展示基准测试。

示例：

硬件：

```
RX 7900 XTX
24GB 显存
ROCm
```

测量：

```
模型              GPU       时间

SDXL               Radeon    18 秒/张

SDXL               CPU       4 分钟/张


视频生成：
SVD
24 帧
45 秒
```

创建仪表盘：

```
AMD Radeon AI 性能

显存：
18.2GB / 24GB

GPU 利用率：
96%

生成：
2.1 秒/帧
```

评委喜欢看得见的工程成果。

---

# 更进一步：构建一个智能体

而非固定工作流：

```
创作者智能体

用户：
“制作一个关于 Nvidia 与 AMD 对比的视频”


智能体：

1. 研究主题
2. 撰写脚本
3. 生成图像
4. 动画制作
5. 生成语音
6. 剪辑视频
7. 发布
```

这与当前的 AI 趋势相契合。

---

# 建议的技术栈

```
前端：
Next.js


后端：
FastAPI


智能体：
LangGraph / 自定义


图像：
Diffusers


视频：
ComfyUI 后端


音频：
XTTS


加速：
ROCm
PyTorch AMD 构建
ONNX Runtime
```

---

# 演示场景（非常重要）

不要演示：

“这是我的模型。”

要演示：

启动计时器：

```
输入：

“创建一个 30 秒的 AI 新闻视频：
AMD 发布新 GPU”


0 秒

智能体启动


20 秒

故事板就绪


60 秒

图像生成完毕


120 秒

视频生成完毕


180 秒

最终 MP4
```

然后播放输出。

评委记住的是结果。

---

# 加分项：利用你自己的优势

根据你的背景，我会把它做成：

## “AI 研究到视频工厂”

因为你已经拥有：

* 数千条 AI 笔记
* 博客流水线
* 视频生成工作流
* AI 实验

演示：

```
你的博客 markdown

        |
        v

AI 阅读文章

        |
        v

生成：

- YouTube 短视频
- Bilibili 视频
- 微信视频
- 缩略图
- 字幕
```

这是一个真正的产品，而不是黑客马拉松的玩具。

---

# 48 小时实施计划

## 第一天上午

构建：

```
Markdown
 |
LLM
 |
故事板 JSON
```

## 第一天下午

集成：

```
SDXL
+
AnimateDiff
```

## 第一天晚上

添加：

```
语音
字幕
视频合并
```

## 第二天

打磨：

* UI
* Radeon 基准测试
* 演示视频
* README

---

# 获胜阐述

标题：

> Radeon 创作者 AI 工作室：一个用于生成专业短视频的自主多模态智能体

一句话：

> “我们利用 AMD Radeon 加速的多模态 AI 模型，将一个创意转化为完整的、可发布的视频。”

---

参考资料：

* AMD ROCm 文档：[https://rocm.docs.amd.com/](https://rocm.docs.amd.com/)
* Hugging Face Diffusers：[https://huggingface.co/docs/diffusers](https://huggingface.co/docs/diffusers)
* ComfyUI：[https://github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)
* Stable Video Diffusion：[https://huggingface.co/docs/diffusers/en/using-diffusers/svd](https://huggingface.co/docs/diffusers/en/using-diffusers/svd)
* Luma AI：[https://lumalabs.ai/](https://lumalabs.ai/)
