---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: FFmpeg 命令选项详解
translated: true
type: note
---

这是一份关于 FFmpeg 命令选项的全面介绍，旨在帮助你有效地理解和使用这个强大的工具：

---

### 1. **什么是 FFmpeg？**
FFmpeg 是一个免费、开源的命令行工具包，用于处理视频、音频以及其他多媒体文件和 Stream。它支持极广泛的 Codec、格式（Format）和协议（Protocol），是处理媒体任务的首选解决方案。

---

### 2. **基础命令结构**
FFmpeg 命令的通用语法如下：
```bash
ffmpeg [global_options] [input_file_options] -i input_file [output_file_options] output_file
```
- **顺序很重要**：选项通常应用于其后紧跟的文件。你可以为不同的输入/输出重复设置选项。
- **Global options**（例如：`-y` 用于覆盖输出文件）应用于整个命令。

---

### 3. **核心命令选项**

#### **输入/输出选项**
- `-i input_file`：指定输入文件。
- `-f fmt`：强制指定输入或输出文件格式（例如：`-f mp4`）。
- `-y`：直接覆盖输出文件而不询问。
- `-n`：从不覆盖输出文件。

#### **Stream 选择**
- `-map`：选择哪些 Stream（视频、音频、字幕）包含在输出中。
- `-vn`：禁用视频。
- `-an`：禁用音频。
- `-sn`：禁用字幕。

#### **Encoding/Decoding**
- `-c[:stream_specifier] codec`：为 Stream 设置 Codec（例如：`-c:v libx264` 用于 H.264 视频）。
- `-c copy`：Stream copy（不进行重新编码，保留质量并加快处理速度）。
- `-b:v bitrate`：设置视频 Bitrate（例如：`-b:v 1M` 表示 1 Mbps）。
- `-r fps`：设置 Frame rate（例如：`-r 30` 表示 30 fps）。

#### **Filtering**
- `-vf filtergraph`：应用视频 Filter（例如：`-vf "scale=640:480"` 用于调整尺寸）。
- `-af filtergraph`：应用音频 Filter（例如：`-af "volume=2"` 用于将音量加倍）。

#### **裁剪与剪辑**
- `-ss position`：定位到特定时间（例如：`-ss 00:01:30`）。
- `-t duration`：记录或转码特定时长（例如：`-t 10` 表示 10 秒）。
- `-to position`：在特定时间停止。

#### **Metadata 及其他**
- `-metadata key=value`：设置 Metadata（例如：`-metadata title="My Video"`）。
- `-preset`：调节编码速度与压缩率的平衡（例如：`-preset fast`）。

---

### 4. **示例**
- **转换视频格式：**
  ```bash
  ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
  ```
- **提取音频：**
  ```bash
  ffmpeg -i input.mp4 -vn -c:a copy output.aac
  ```
- **调整视频尺寸：**
  ```bash
  ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4
  ```
- **裁剪视频：**
  ```bash
  ffmpeg -i input.mp4 -ss 00:01:30 -t 10 -c copy output.mp4
  ```

---

### 5. **高级功能**
- **Complex filtergraphs**：链接多个 Filter 以实现高级特效。
- **Streaming**：使用 FFmpeg 推流至 YouTube 或 RTMP 服务器等平台。
- **批量处理**：编写 FFmpeg 命令脚本以实现自动化。

---

### 6. **进一步学习的资源**
- [Official FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)：最权威、最新的参考文档。
- [FFmpeg Cheat Sheet](https://gist.github.com/steven2358/ba153c642fe2bb1e47485962df07c730)：常用命令的快速查询表。
- [Detailed Explanation of Common FFmpeg Commands](https://www.oreateai.com/blog/detailed-explanation-of-common-ffmpeg-commands-and-functions/45e0c1f86c8859751366c58d67c34a8b)：包含示例的深入指南。

---

**提示：** 由于 FFmpeg 会持续更新，请务必查看官方文档以获取最新的选项和功能。

你是否想深入了解 FFmpeg 的某个特定方面，例如 Filtering、Streaming 或批量处理？
