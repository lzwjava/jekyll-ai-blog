---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 一个建造者三个项目
translated: true
type: note
---

完成。您的 Marp 演示文稿已准备就绪——完全由代码/Markdown 驱动，可完全编辑。

## 📊 演示文稿 (Marp Markdown)

**源文件：`deck.md`** — 纯 Markdown 文件，可在任意编辑器中编辑并重新导出。

**6 张幻灯片 · 中英双语 · 与视频匹配的暗色主题**（背景色 #0a0a0b + 金色 #e3b341）：

1. **封面** — Three Projects, One Builder / 三个项目 · 一位建造者
2. **议程** — 01 Truth Lab · 02 Truth Software · 03 lzwjava.com
3. **Truth Lab 求真实验室** — 从头训练语言模型 · 52GB 集群 · 诚实实验 → truthlab.cc
4. **Truth Software 求真软件** — 40 余款产品 · 每日处理超 10 亿 token → truthsoft.dev
5. **lzwjava.com** — AI 博客 · AI 与软件作品集 → 作品链接
6. **行动号召** — 构建诚实之物 · 所有网址 · 联系方式 · 基于 token 的定价

**导出至 `output/` 目录：**

- `announcement.pdf`（6 页，16:9 比例，已验证中文渲染正常）
- `announcement.html`（浏览器视图）
- `announcement.pptx`（PowerPoint 格式）
- `previews/slide-1..6.png`（快速缩略图）

## 如何调整

```bash
marp deck.md -o output/announcement.html          # 生成 HTML
marp deck.md -o output/announcement.pdf --pdf     # 生成 PDF（通过 Chrome）
marp deck.md -o output/announcement.pptx         # 生成 PPTX
```

演示文稿与视频（`announcement.mp4`，时长 55 秒）现在共享相同的内容与外观——分别由 `deck.md` 和 `scenes.json` 驱动。所有文件均位于 `/Users/lzwjava/projects/video-factory` 目录下，其中包含一份 README 文件概述了构建命令。

是否需要我将演示文稿完全翻译为中文（仅限中文，面向中国观众）、为每张幻灯片添加演讲者备注页面，或者将真实的作品截图（位于 `truth-software` 目录下的 `images/` 文件夹中）嵌入到幻灯片中？
