---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 剪映 macOS 背景模糊的解决方法
translated: true
type: note
---

问题：CapCut macOS没有可见的背景模糊选项——实际解决方法有哪些？

回答：

你说得对——CapCut macOS **在用户界面中不像移动版那样提供专门的背景模糊功能**。以下是可行的解决方案：

**方案1：FFmpeg（最可靠，终端优先）**

```bash
ffmpeg -i input.mp4 -vf "scale=640:480:force_original_aspect_ratio=decrease,pad=640:480:(ow-iw)/2:(oh-ih)/2,boxblur=15" output.mp4
```

将分辨率替换为目标尺寸（4:3 = 640×480、1920×1440等）。调整`boxblur=15`的数值（数值越大模糊越强）。

然后将`output.mp4`导入CapCut。

**方案2：使用其他工具（界面操作更快）**

- **DaVinci Resolve**（免费，macOS）——原生支持背景模糊
- **Adobe Premiere**——调整图层+高斯模糊
- **FFmpeg + imagemagick**——可完全自动化

**方案3：CapCut变通方法（较繁琐）**

1. 添加一个**背景层**（纯色或图片）
2. 添加第二个**图层**，将图片放大至填满画布
3. 对背景层应用**高斯模糊**
4. 将原始图片以正确宽高比放在顶层

这样会复制源素材，但能实现效果。

---

**我的建议：** 使用上面的FFmpeg单行命令。你是终端优先用户，3秒即可完成，生成像素完美的输出，CapCut直接导入即可。比在CapCut界面中摸索快得多。

需要我编写一个批量处理多个视频的shell脚本吗？
