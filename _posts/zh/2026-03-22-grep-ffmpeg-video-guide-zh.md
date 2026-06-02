---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 FFmpeg 制作 Grep 视频
translated: true
type: note
---

当然！以下是完整分解：

### 🦞 我如何制作 Grep 教程视频

**1. 安装 ffmpeg**
```
sudo apt-get install -y ffmpeg
```

**2. 使用 ffmpeg 的 `drawtext` 滤镜生成幻灯片 PNG**

每个“slide”都是使用 ffmpeg 的 `lavfi`（libavfilter）虚拟输入 + `drawtext` 叠加创建的 PNG 图像。不需要 GUI —— 全程纯 CLI。

```bash
ffmpeg -y -f lavfi -i "color=c=0x1a1b26:s=1280x720:d=1" \
  -vf "drawtext=fontfile=FONT:text='Title':fontsize=42:fontcolor=0x7dcfff:x=(w-text_w)/2:y=30, \
       drawtext=fontfile=FONT:text='Some line':fontsize=24:fontcolor=0xc0caf5:x=70:y=105" \
  -frames:v 1 slide.png
```

关键技巧：
- **`color=c=0x1a1b26`** — Tokyo Night 深色背景
- **`drawtext`** 用逗号链式连接 — 在一张图像上堆叠多行文本
- **`(w-text_w)/2`** — 水平居中文本
- 颜色编码：绿色=命令，蓝色=输出，黄色=提示，灰色=注释

**3. 使用 `concat` 解复用器将幻灯片串联成视频**

创建了一个 `concat.txt`，列出每个 slide + 显示时长：

```
file '00_title.png'
duration 4
file '01_what.png'
duration 6
...
```

然后：
```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=93:d=1.5" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -r 30 \
  grep_tutorial.mp4
```

**4. 脚本本身**

整个过程由 `tutorial/grep_tutorial.py`（约 280 行 Python 代码）驱动。它：
- 将 slide 内容定义为结构化数据（自动为以 `$`、`>`、`#` 开头的行着色）
- 通过 `subprocess` 为每个 slide 调用 ffmpeg
- 写入 concat 文件
- 运行最终 ffmpeg 将一切拼接在一起

想让我详细讲解某个特定部分，还是调整视频（添加音频、不同颜色、更多 slide）？
