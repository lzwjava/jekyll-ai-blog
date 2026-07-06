---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新的ww笔记HTML命令
translated: true
type: note
---

以下是已完成内容的摘要：

---

**`ww note html` — 新命令**

读取剪贴板内容，创建一个兼容 Jekyll 的 `.html` 视觉笔记。

**用法：**
```
ww note html                   # 直接在 BASE_PATH/notes/ 中创建 HTML 笔记
ww note html --queue           # 加入队列，供后续通过 `ww note process` 处理
ww note html --dir /path       # 自定义输出目录
```

**生成的内容：**

在 `~/projects/jekyll-ai-blog/notes/` 中生成类似 `2026-07-07-slug-en.html` 的文件，包含：

- **Jekyll 前置元数据**（layout: post, title, lang, type）
- **语义化的 HTML 正文** — 由 LLM 将剪贴板内容转换而来，包含适当的 `<h2>`、`<pre><code class="language-xxx">`、`<ul>`、`<blockquote>` 等
- **转义后的代码块** — 对 Jekyll/Liquid 渲染安全

**文件变更：**

| 文件 | 变更 |
|------|------|
| `ww/note/create_note_html.py` | **新增** — 模块：标题生成、slug 生成、LLM→HTML 转换、Jekyll 前置元数据 |
| `ww/main.py` | 添加了 `ww note html` 子命令分发 + 帮助文本 |
| `ww/note/note_queue.py` | 添加了用于基于队列工作流的 `enqueue_html()` |
| `ww/note/note_queue_process.py` | 在处理循环中添加了 `entry_type == "html"` 处理器 |
| `completions/_ww` | 添加了 `html` 补全条目 |

**队列集成：** `ww note html --queue` → `ww note watch` 自动处理，或 `ww note process` 将其排空。工作方式与 `ww note log` 完全相同，但生成的是 Jekyll HTML 而非纯文本日志。