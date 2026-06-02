---
audio: true
generated: false
image: true
lang: zh
layout: post
title: Markdown 问题：Kramdown 和 XeLaTeX
translated: true
type: post
---

为了将 Markdown 内容生成 PDF 文件并同时兼容 Jekyll 博客的 HTML 渲染和 XeLaTeX 的 PDF 渲染，可以采用以下方法。以下是我生成 PDF 使用的 Pandoc 命令：

```python
command = [
    'pandoc',
    input_markdown_path,
    '-o', output_pdf_path,
    '-f', 'markdown',
    '--pdf-engine', 'xelatex',
    '--resource-path=.:assets',
    '-V', f'CJKmainfont={CJK_FONT}',
    '-V', f'CJKsansfont={CJK_FONT}',
    '-V', f'CJKmonofont={CJK_FONT}',
    '-V', f'geometry:{GEOMETRY}',
    '-V', 'classoption=16pt',
    '-V', 'CJKoptions=Scale=1.1',
    '-V', 'linestretch=1.5'
]
```

同时支持 Kramdown 和 XeLaTeX 的注意事项

在 Markdown 中同时兼容 kramdown（Jekyll 用于生成 HTML）和 XeLaTeX（用于 Pandoc 的 PDF 生成），需要注意以下几点：

1. 图片路径的兼容性
	•	Kramdown（HTML）: 通常使用以 / 开头的路径来引用资源。
	•	XeLaTeX（PDF）: 要求使用相对路径，不应以 / 开头。

解决方案：统一使用相对路径，这样能兼容两种格式：

```
![](assets/images/chatgpt/block.jpg)
```

2. 处理 Kramdown 特定属性
	•	{:.responsive} 是 Kramdown 支持的属性，用于 HTML 样式控制。
	•	XeLaTeX 不支持这些属性，保留会导致错误。

解决方案：移除 PDF 生成时不支持的 Kramdown 特定属性。例如：

<!-- Kramdown-specific -->
```
![](assets/images/chatgpt/block.jpg){: .responsive }
```

<!-- Compatible with both -->
```
![](assets/images/chatgpt/block.jpg)
```

如果 {:.responsive} 对 HTML 输出至关重要，可以仅在生成 HTML 时添加，而在 PDF 输出中省略。

双格式兼容的工作流

1.	编写 Markdown 时尽量避免依赖 Kramdown 的特定功能。
2.	如果需要为 HTML 添加样式，建议将 CSS 类 应用到 Jekyll 模板中，而不是直接在 Markdown 中定义。
3.	使用 Pandoc 参数控制 PDF 的格式化，确保 Markdown 的跨平台兼容性。

通过这些方法，可以让 Markdown 内容在 Jekyll 的 HTML 渲染 和 XeLaTeX 的 PDF 渲染 中兼容无误，从而实现多格式发布的无缝工作流。
