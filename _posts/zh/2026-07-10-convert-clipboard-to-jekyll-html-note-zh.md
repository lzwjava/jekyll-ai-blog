---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将剪贴板转换为Jekyll HTML笔记
translated: true
type: note
---

以下是 `ww note html` 的完整说明。

---

## `ww note html` 的作用

读取剪贴板内容，将其转换为 **Jekyll 兼容的 HTML 页面**，并写入 `BASE_PATH/notes/` 目录 —— 与 markdown 笔记存放在同一目录 —— 但生成的是 `.html` 文件，能在浏览器中直接呈现富视觉内容。

## 两种工作模式

| 模式 | 命令 | 行为 |
|------|------|------|
| **直接** | `ww note html` | 立即在 `BASE_PATH/notes/` 中创建 HTML 文件 |
| **队列** | `ww note html --queue` | 将其加入 `~/.config/ww/note_queue.json`，类型为 `"html"`。随后由 `ww note process` 或 `ww note watch` 处理 |

队列路径与现有流程集成 —— `ww note watch` 会检测到新条目并自动处理，就像处理 markdown 笔记和日志一样。

## 处理流程（直接模式）

```
剪贴板内容
    ↓
1. clean_grok_tags()     — 去除 <grok:render> 标签
2. clean_content()        — 去除开头的 "# Title" 和多余的 ---
3. _generate_title()      — LLM：生成简短英文标题（≤6 个单词，≤60 字符）
4. _generate_slug()       — LLM：生成 URL 安全的 slug（连字符、小写、≤8 部分）
5. _content_to_html()     — LLM：转换为语义化的 HTML5
6. _format_front_matter() — Jekyll YAML 前置元数据
7. 写入文件               — {日期}-{slug}-en.html 存入 BASE_PATH/notes/
```

## HTML 输出格式

文件以 Jekyll 前置元数据开头（与 markdown 笔记相同的 layout/title/lang），后接 HTML 正文：

```yaml
---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Your Generated Title"
translated: false
type: note
---
```

然后是语义化的 HTML —— LLM 生成 `<h2>`、`<h3>`、`<p>`、`<pre><code class="language-xxx">`、`<ul>/<ol>`、`<blockquote>`、`<a>`、`<img>`、`<table>`、`<hr>` 等标签。代码块中的内容会被转义，避免 Liquid/Jekyll 因 `{{ }}` 或 `{% raw %}{% %}{% endraw %}` 模式而出错。

`layout: post` 前置元数据意味着 Jekyll 会使用与其他文章相同的主题/布局（页眉、页脚、侧边栏、CSS）来包裹内容，因此“可视化”效果既来自语义化的 HTML 结构，也来自 Jekyll 主题。

## 创建/修改的文件

| 文件 | 变更 | 说明 |
| ------ | ------ | ------ |
| `ww/note/create_note_html.py` | **+189** 新增 | 核心模块：标题生成、LLM→HTML 转换、Jekyll 前置元数据、文件写入 |
| `ww/main.py` | +7 | 添加 `elif subcmd == "html":` 分发逻辑，并在 `_print_help()` 中添加帮助文本 |
| `ww/note/note_queue.py` | +6 | 添加 `enqueue_html()` —— 读取剪贴板，以 `type: "html"` 入队 |
| `ww/note/note_queue_process.py` | +5 | 在 `process_queue` 中添加 `elif entry_type == "html":` —— 调用 `create_note_html()` 并跳过 markdown 专属的后处理 |
| `completions/_ww` | +1 | 在 `note_cmds` 数组中添加 `'html:Create a Jekyll HTML note (visual)'` |

## 错误处理

- **剪贴板为空** → `"Content is empty or invalid."`
- **文件已存在** → `"HTML note already exists: {path}"`（不覆盖文件）
- **LLM 失败** → 回退到基础 HTML 包装（`<p>` 加换行符和 HTML 转义内容）
- **推理模型噪声** → 标题超过 60 字符自动截断为 6 个单词；去掉尾部引号

## 使用示例

```bash
# 1. 复制内容
cmd+C 复制一些 markdown/文本/代码

# 2a. 立即创建 HTML 笔记
ww note html

# 2b. 或者加入队列，稍后处理
ww note html --queue
ww note process   # 稍后批量处理

# 文件生成在：
# ~/projects/jekyll-ai-blog/notes/2026-07-07-your-slug-en.html
```
