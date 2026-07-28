---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 视频智能体空间仍不成熟
translated: true
type: note
---

问题：是否存在一个 `hermes-video-agent`（基于 Claude Code/pi-agent 风格的视频编辑代理，使用 ffmpeg）？

答案：

**是的，部分存在。但这一领域仍然非常不成熟。**

你的想法本质上是：

> Claude Code 用于视频。

这个确切方向正在兴起。（[Claude][1]）

最接近的项目：

---

## 1. Vex — 可能是最接近的匹配

[Vex GitHub 仓库](https://github.com/AKMessi/vex?utm_source=chatgpt.com)

Vex 自称：

> "终端优先的 AI 视频编辑，由纯英语驱动"

它做的事情：

```
用户提示
    |
    v
LLM 代理
    |
    +-- FFmpeg
    +-- MoviePy
    +-- 转录分析
    +-- 生成视觉元素
    |
    v
编辑后的视频
```

示例：

```
"移除尴尬的开场"

"制作成 YouTube 短视频"

"添加字幕"

"剪掉无聊的部分"
```

与你的 Hermes 想法非常接近。（[GitHub][2]）

---

## 2. video-use — Claude Code 风格

[video-use GitHub 仓库](https://github.com/browser-use/video-use?utm_source=chatgpt.com)

概念：

```
原始素材文件夹

        |
        v

Claude Code

        |
        v

final.mp4
```

它将视频编辑视为编码：

* 文件
* 脚本
* 工具
* 迭代

基本上就是：

```
Claude Code
      |
      +-- edit.py
      +-- ffmpeg
      +-- assets
      +-- output.mp4
```

（[GitHub][3]）

---

## 3. 研究方向：VideoAgent

还有一些学术系统正在朝这个方向发展：

VideoAgent：视频理解与编辑的全能框架

思路：

```
LLM
 |
 +-- 镜头规划代理
 +-- 编辑代理
 +-- 检索代理
 +-- 渲染管线
```

它更接近一个多智能体视频编辑器。（[arXiv][4]）

---

## 但你的想法有一个不同的角度

目前大多数项目：

```
输入视频
    |
    v
编辑视频
```

你的 Hermes 想法可以是：

```
意图
 |
 v
视频工程师代理
 |
 +-- 理解
 +-- 创建
 +-- 编辑
 +-- 发布
 +-- 学习
```

更像是：

```
Claude Code
      +
Midjourney
      +
FFmpeg
      +
YouTube 自动化
```

---

## 缺失的部分

当前工具通常缺少以下内容：

### 1. 长期记忆

示例：

```
hermes-video-agent/

memory/
   my_channel_style.md
   subtitle_style.json
   favorite_music.json
   audience.json
```

经过 100 个视频后：

```
Agent:
"我了解你的风格。"
```

---

### 2. 视频项目状态

需要类似 git 的东西：

```
video-project/

main.mp4

timeline.json

versions/

v1/
v2/
v3/
```

而不是：

```
随机的 ffmpeg 命令
```

而是：

```
视频提交历史
```

示例：

```bash
hermes-video commit -m "缩短开场"

hermes-video rollback v2
```

---

### 3. 自我评估循环

编码代理有测试：

```
代码
 |
测试
 |
修复
```

视频代理需要：

```
渲染
 |
观看
 |
评判模型
 |
修复
```

示例：

```
Critic:

- 前 5 秒太慢
- 字幕太小
- 没有钩子

Agent:
重新生成
```

---

## 我的看法

我不会与以下产品竞争：

* CapCut
* Runway
* Pika
* Kling

它们优化的是**一次性生成**。

你更好的定位：

```
hermes-video-agent

"AI 视频创作者的操作系统"
```

从 CLI 开始：

```bash
hermes video edit input.mp4 \
"把这个变成一个病毒式 AI 短视频"
```

然后稍后：

```bash
hermes channel run \
--topic "AI 新闻"
--daily
```

自然的演进是：

```
pi-agent
   |
   +-- 编码代理
   |
   +-- 研究代理
   |
   +-- 视频代理
```

所以，是的，其他人正在开始这个方向，但 "AI 视频编辑器" 和 "自主视频工程师" 之间仍有很大差距。你的想法正好处于这个差距之中。

[1]: https://code.claude.com/docs/en/overview?utm_source=chatgpt.com "Claude Code 概述 - Claude Code 文档"
[2]: https://github.com/AKMessi/vex?utm_source=chatgpt.com "GitHub - AKMessi/vex: claude code for video editing · GitHub"
[3]: https://github.com/browser-use/video-use?utm_source=chatgpt.com "GitHub - browser-use/video-use: Edit videos with coding agents · GitHub"
[4]: https://arxiv.org/abs/2606.23327?utm_source=chatgpt.com "VideoAgent: 视频理解与编辑的全能框架"