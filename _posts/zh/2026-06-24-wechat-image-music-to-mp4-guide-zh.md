---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信图片音乐转MP4指南
translated: true
type: note
---

**问题：** 在微信中分享带背景音乐的图片，这是微信特有的格式吗？而上传到 YouTube Shorts 需要实际视频，那么如何将该“图片+音乐”格式转换为合适的视频文件？

**回答：**

是的，微信的“图片+音乐”分享格式是微信生态系统特有的。当你在微信中创建“视频动态”或通过视频号分享静态图片加背景音乐时，微信会在内部将其存储为复合帖子，而非标准视频文件。你无法直接将其导出为 `.mp4` 格式。

对于 YouTube Shorts，你需要一个真正的视频文件（H.264/MP4，竖屏 9:16，建议 ≥1080x1920）。

**使用 ffmpeg 将图片+音频转换为 MP4（这里正确的工具）：**

```bash
ffmpeg -loop 1 -i input.jpg \
       -i music.mp3 \
       -c:v libx264 \
       -t 30 \
       -pix_fmt yuv420p \
       -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
       -c:a aac -b:a 192k \
       -shortest \
       output.mp4
```

关键参数：

- `-loop 1` — 将静态图片循环作为视频帧
- `-t 30` — 视频时长（秒）（Shorts 最长 60 秒）
- `scale + pad` — 添加黑边（letterbox/pillarbox）以适配 9:16 而不裁剪
- `-pix_fmt yuv420p` — 确保广泛兼容性（YouTube、微信等）
- `-shortest` — 当音频结束时停止

**如果你需要先从微信中提取音乐**，那会更棘手——微信不提供干净导出的方式。可选方法：

- 用另一台设备录制手机播放的音频，或屏幕录制带音频
- 如果你原本就有音频文件，直接使用即可
- 在已 root 的 Android 设备上，微信缓存位于 `/data/data/com.tencent.mm/` 但经过混淆

**快速测试用的单行命令（使用纯色背景代替图片）：**

```bash
ffmpeg -f lavfi -i color=c=black:s=1080x1920:r=30 \
       -i music.mp3 -t 30 \
       -c:v libx264 -pix_fmt yuv420p -c:a aac \
       -shortest output.mp4
```

结论：微信的图片+音乐不是标准格式，而是平台特性。跨平台使用时，`ffmpeg -loop 1` 是你的好帮手。
