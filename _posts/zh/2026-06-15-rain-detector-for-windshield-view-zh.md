---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 挡风玻璃视野雨水检测器
translated: true
type: note
---

以下是翻译后的中文内容：

**新文件：** `ww/weather/rain.py`
- 通过 ffmpeg（avfoundation）从网络摄像头录制 3 秒视频
- 提取 5 帧（每秒一帧）
- 通过 OpenRouter 将所有帧发送给视觉模型（使用 `.env` 中的 `VISION_MODEL` 或 `MODEL`）
- 将降雨强度评为 0-5 级，并提供详细描述和建议
- 专为车内使用设计：提示词告知模型网络摄像头正对挡风玻璃，车窗可能关闭

**使用方法：**
```
ww rain              # 录制 3 秒视频，分析降雨
ww rain --seconds 5  # 录制更长时间
ww rain --keep       # 保留视频文件
ww rain --debug      # 显示模型/请求信息
ww weather rain      # 同样有效
```

**修改的文件：**
- `ww/main.py` — 为 `ww rain`（顶级命令）和 `ww weather rain` 添加路由、帮助文本和 all_groups
- `~/.zsh/completions/_ww` — 在顶级命令中添加 `rain`，并在 `weather_cmds` 数组中添加降雨子命令

**在车内的使用方式：** 将笔记本电脑摄像头对准挡风玻璃。运行 `ww rain`。它会录制一小段视频、提取帧，并告诉您降雨强度（0=晴朗，5=暴雨），同时提供实用的建议，例如"关闭车窗"或"可以稍微打开车窗"。