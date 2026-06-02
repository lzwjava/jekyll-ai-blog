---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: 提取最后十分钟音频
translated: true
type: note
---

要提取音频文件 `lobby-zh.ogg` 的最后10分钟内容，需要依据以下信息：

1.  **总时长：** 输入文件时长为 `00:33:34.40`。
2.  **目标片段时长：** 10分钟（即600秒）。
3.  **开始时间计算：** 需要计算文件结束前10分钟的时间点。

### 计算过程

*   总时长（秒）：
    $$(33 \times 60) + 34.40 = 1980 + 34.40 = 2014.40 \text{ 秒}$$
*   开始时间：
    $$2014.40 \text{ 秒} - 600 \text{ 秒} = 1414.40 \text{ 秒}$$

转换为 `时:分:秒.毫秒` 格式：
$$1414.40 \text{ 秒} = 23 \text{ 分 } 34.40 \text{ 秒} \quad (1414.40 / 60 = 23.5733\dots)$$
$$\text{开始时间} = 00:23:34.40$$

### FFmpeg 命令

使用 `-ss`（定位到指定位置）输入选项结合 `-t`（持续时间）选项。

1.  `-ss 00:23:34.40`：设置提取的起始位置。
2.  `-t 00:10:00`：设置输出片段的时长恰好为10分钟。

```bash
ffmpeg -i lobby-zh.ogg -ss 00:23:34.40 -t 00:10:00 last_10_minutes.ogg
```

**注意：** 若希望保持输出文件使用原始比特率/编解码器设置，可添加 `-c copy` 以加速处理：

```bash
ffmpeg -i lobby-zh.ogg -ss 00:23:34.40 -t 00:10:00 -c copy last_10_minutes_copy.ogg
```
