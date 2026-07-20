---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新视频生成器
translated: true
type: note
---

全部完成。以下是所创建内容的摘要：

**`ww gen-video <file>`** — 根据 markdown 笔记生成竖屏短视频（9:16）。

**更改的文件：**
- `ww/gen_video/__init__.py` — 空包初始化文件
- `ww/gen_video/video.py` — 主模块（约 680 行）
- `ww/main.py` — 帮助文本 + 调度代码块 + 组查找
- `~/.zsh/completions/_ww` — zsh 补全条目

**处理流程：**
1. **LLM 脚本生成** — 读取 markdown，使用默认的 MODEL 生成解说脚本 + 每个场景 5-6 个图像提示
2. **Flux 图像生成** — 通过 OpenRouter 调用 `black-forest-labs/flux.2-pro` 为每个场景生成图像，处理 base64 数据 URL 和品牌名称审核
3. **TTS 解说** — 使用 macOS `say` 命令（Samantha/Tingting 语音），转换为 AAC 格式
4. **FFmpeg 合成** — 将图像拼接为 1080×1920 竖屏视频，并配上解说音频

**用法：**
```
ww gen-video /path/to/note.md
ww gen-video /path/to/note.md --output my_video.mp4 --voice Samantha
ww gen-video /path/to/note.md --audio existing_narration.aac
ww gen-video /path/to/note.md --image-model black-forest-labs/flux.2-pro
```

**已测试** 使用 Tesla P100 vs M60 文章 — 生成了一个 164 秒、3.9 MB、1080×1920 的视频，包含 5 张 Flux 生成的图像和配音。