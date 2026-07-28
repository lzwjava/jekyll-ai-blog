---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫耳墨斯视频代理概念
translated: true
type: note
---

问题：构建 `hermes-video-agent` 怎么样？一个类似 Hermes/pi-agent 风格的编码代理，但专门用于通过提示词 + ffmpeg 进行视频编辑和生成。

回答：

我认为这个想法比构建一个完整的 TikTok 平台**更聚焦、技术上更有趣**。

关键洞察：

> 不要构建“AI 视频编辑器 UI”。构建一个**视频原生代理**。

类似于：

* Anthropic Claude Code → 软件工程代理
* pi-agent → 轻量级代理运行时
* Hermes → 你自己的代理工作流

那么：

```
hermes-video-agent

用户：
"把这个视频变得更像 YouTube Short"

代理：
- 检查视频
- 理解时间线
- 剪掉无聊部分
- 添加字幕
- 添加音乐
- 生成 B 卷
- 用 ffmpeg 渲染
```

---

## 核心想法

当前视频工具：

```
人类
 |
 | 点击按钮
 |
Premiere / CapCut / DaVinci
```

你的想法：

```
人类
 |
 | 自然语言
 |
hermes-video-agent
 |
 +-- ffprobe
 +-- whisper
 +-- 视觉模型
 +-- ffmpeg
 +-- 图像/视频生成
 |
output.mp4
```

代理拥有时间线。

---

## 将“文件系统作为记忆”模型

类似于编码代理：

编码代理：

```
repo/
 ├── main.py
 ├── tests/
 └── package.json
```

视频代理：

```
project/
 |
 ├── input.mp4
 ├── transcript.json
 ├── scenes.json
 ├── assets/
 │    ├── broll01.mp4
 │    └── image01.png
 |
 ├── edit_plan.json
 └── output.mp4
```

代理编辑文件。

---

## 示例会话

用户：

```
hermes-video edit interview.mp4

把它做成一个 60 秒的 AI 新闻短片。
去掉静音。
添加字幕。
高亮重要句子。
```

代理：

```
正在分析视频...

时长：48 分钟

转录：
- 12000 个词

正在寻找高亮...

已选择：
03:21-04:05
12:44-13:20
27:10-27:55

正在创建编辑计划...
```

生成：

```json
{
 "cuts":[
   ["03:21","04:05"],
   ["12:44","13:20"]
 ],
 "captions":true,
 "style":"youtube-short"
}
```

然后：

```bash
ffmpeg \
-i input.mp4 \
-filter_complex script.txt \
output.mp4
```

---

## 杀手锏：将 ffmpeg 暴露为工具

代理工具：

```python
tools = [
    ffprobe,
    extract_audio,
    transcribe,
    detect_scene,
    cut_video,
    merge_video,
    add_caption,
    add_music,
    generate_image,
    generate_video
]
```

示例：

```
用户：
"做一段 Elon Musk 风格的开场"

代理：

1. 生成开场图像
2. 创建运动效果
3. 合并
4. 渲染
```

---

## 架构

最小化：

```
                 LLM
                  |
                  |
          hermes-video-agent
                  |
     +------------+-------------+
     |            |             |
  视觉        音频          编辑
     |            |             |
 GPT-4.1     Whisper       ffmpeg
 Qwen-VL                  MoviePy
                           Remotion
```

---

## 为什么 ffmpeg 很重要

大多数 AI 视频初创公司隐藏了 ffmpeg。

我会让 ffmpeg 成为“汇编语言”。

示例：

代理创建：

`edit.sh`

```bash
ffmpeg \
-i input.mp4 \
-vf "
scale=1080:1920,
subtitles=sub.srt,
drawtext=text='AI NEWS'
" \
-c:a copy \
output.mp4
```

LLM 本质上是一个编译器：

```
提示词
  |
  v
编辑计划
  |
  v
ffmpeg 程序
  |
  v
视频
```

非常类似于：

```
自然语言
       |
       v
代码
       |
       v
机器
```

---

## 大机会：视频 MCP 服务器

我会构建：

```
video-mcp-server
```

这样每个代理都能使用视频能力。

工具：

```
video.inspect()
video.cut()
video.caption()
video.translate()
video.generate()
video.render()
```

然后：

Claude Code：

```
"把这个演示变成发布视频"
```

Cursor：

```
"根据 README 创建教程视频"
```

你自己的代理：

```
"生成每日 AI 新闻视频"
```

---

## 我会构建的 MVP

不要从生成开始。

从编辑开始。

因为生成成本高且不稳定。

第一阶段：

```
输入：
mp4

命令：

"去掉静音"
"制作短片"
"添加字幕"
"翻译字幕"
"剪切高亮"

输出：
mp4
```

技术栈：

```
Python
FastAPI
ffmpeg
Whisper
Qwen-VL / Gemini vision
LLM 规划器
```

大概 1-2 周。

---

第二阶段：

添加生成：

```
"解释 CUDA"

代理：

生成：
 - 图表
 - 图像
 - B 卷
 - 旁白

组装视频
```

---

有趣的定位：

不是：

> "AI 视频生成器"

太拥挤了。

而是：

> "用于视频的 Claude Code。"

一个终端优先的自主视频工程师。

`hermes-video-agent` 实际上是你 `ww` 生态系统的很自然扩展。同样的代理循环：

```
观察
 -> 规划
 -> 执行工具
 -> 验证输出
 -> 迭代
```

但产物是：

```
软件 -> 视频
```

这是一个更清晰的产品边界。
