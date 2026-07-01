---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 LLM 回答保存为 Markdown 笔记
translated: true
type: note
---

Question: 如何使用 Safari 插件/扩展将 LLM（例如 Claude/ChatGPT）的回答保存为 Markdown 笔记到我的博客？

Answer:

根据您的设置（您已经在运行一个脚本，通过 git 将笔记拉取到 `blog-source` 并检查重复项），以下是从最简单到最自动化的几种方法：

---

## Option 1: Browser Extension — Export Claude Chat to Markdown

由于您在使用 Claude，最直接的工具是：

### **MarkDownload** (recommended, Safari supported)

MarkDownload 是一个支持 Safari、Chrome、Edge 和 Firefox 的浏览器扩展，允许您将网站下载为 Markdown 文本。只需点击浏览器工具栏中的图标，即会打开一个覆盖窗口，显示正确格式化的网页文本，并保留链接。

- 从 Safari Extension Gallery 安装（Safari 版本需支付少量费用）
- 在浏览器中打开您的 Claude 会话
- 点击 MarkDownload 图标 → 下载 `.md` 文件
- 将文件拖入您的 `blog-source` 文件夹 → 您现有的 git 脚本会自动拾取

### **claude-to-markdown** (open source WebExtension)

此 WebExtension 可自动将 Claude 对话记录导出为 Markdown。如果在扩展首选项中设置 GitHub token，您可以将生成的 Markdown 自动保存为 Gist。它不会将您的数据传输到任何第三方服务。

- GitHub: `legoktm/claude-to-markdown`
- 目前支持 Firefox；在 Safari 中手动加载需费一些功夫

### **AI Chat Exporter** (Chrome/Edge, not Safari natively)

AI Chat Exporter 支持以多种格式导出 Claude 会话，包括 PDF、Markdown、Text、JSON、CSV 和 Image。您可以仅下载会话中需要的特定部分。

> ⚠️ 此工具需要 Chrome/Edge，不直接支持 Safari。

---

## Option 2: DownMark Safari Extension (macOS)

DownMark 是一个专为 macOS 设计的 Safari 扩展，可更轻松地将网页内容转换为 Markdown 格式。只需点击 Safari 工具栏中的扩展图标，智能算法会自动识别核心内容区域，过滤掉广告、导航栏、侧边栏和其他干扰元素。

DownMark 输出标准化的 Markdown `.md` 文件（UTF-8 编码），所有处理均在设备上进行，不会将数据传输到外部服务器。

- Mac App Store 上售价 $4.99（一次性付费）
- 支持 Claude.ai、ChatGPT 和其他 LLM 网页界面
- 通过 Finder 直接保存到您指定的文件夹

---

## Option 3: Console Script (No Extension Needed)

您可以在浏览器中打开 Claude 会话，将 JavaScript 脚本复制到浏览器控制台，按 Enter 键，脚本会自动生成并下载以会话标题命名的 `.md` 文件。它使用 Claude 自带的复制功能，确保 Markdown 格式完美，支持表格、数学、代码块和其他复杂格式。

Script repo: `agarwalvishal/claude-chat-exporter` on GitHub。

---

## Option 4: Integrate with Your Existing Blog Pipeline

由于您的博客脚本已经：

- 在 `blog-source` 上运行 `git pull --rebase`
- 检查重复笔记

您可以添加一个 **watch folder** 步骤：

```bash
# Example: auto-move downloaded .md files into blog-source
WATCH_DIR=~/Downloads
BLOG_DIR=~/projects/blog-source/_notes

fswatch -o "$WATCH_DIR" | while read; do
  find "$WATCH_DIR" -name "*.md" -newer /tmp/.last_check | while read f; do
    mv "$f" "$BLOG_DIR/"
    echo "[info] Moved $f to blog"
  done
  touch /tmp/.last_check
done
```

然后您现有的 `ww note` 脚本会自动处理 git push 和重复检测。

---

## Recommended Workflow Summary

| 步骤 | 工具 |
| --- | --- |
| 保存 LLM 回答 | MarkDownload 或 DownMark Safari 扩展 |
| 输出格式 | `.md` 文件（带 front matter） |
| 放置位置 | 您的 `blog-source` 笔记文件夹 |
| 自动发布 | 您现有的 `ww note` git 脚本 |

最简洁的 Safari 原生方法是 **DownMark** ($4.99)（macOS）或 **MarkDownload**（免费/低价，跨浏览器支持）。

References:

- [MarkDownload on GitHub (deathau/markdownload)](https://github.com/deathau/markdownload)
- [DownMark Safari Extension](https://wanyi.dev/en/downmark/)
- [claude-to-markdown WebExtension (legoktm)](https://github.com/legoktm/claude-to-markdown)
- [claude-chat-exporter console script (agarwalvishal)](https://github.com/agarwalvishal/claude-chat-exporter)
- [AI Chat Exporter for Claude](https://www.claudexporter.com/en)
