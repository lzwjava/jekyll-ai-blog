---
audio: false
generated: true
lang: zh
layout: post
title: 在Jekyll中使用KaTeX
translated: true
type: note
---

要在当前 Jekyll 设置中使用 KaTeX 替代 MathJax，您需要替换 MathJax 脚本并调整 Jekyll 配置。KaTeX 比 MathJax 更轻量快速，但实现方式有所不同（例如，公式自动编号需要手动处理）。以下是将 Jekyll 站点切换至 KaTeX 的完整步骤：

### 1. 更新 Jekyll 配置
修改 `_config.yml` 中的 kramdown 配置段：

```yaml
kramdown:
  math_engine: katex
  input: GFM
  syntax_highlighter: rouge
```

该配置会指示 Kramdown 使用 KaTeX 渲染 LaTeX 数学公式。

### 2. 引入 KaTeX 资源
在 Jekyll 布局文件（如 `_layouts/default.html`）的 `<head>` 段中移除 MathJax 脚本，替换为以下 KaTeX 资源：

```html
<!-- KaTeX CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" integrity="sha384-nB0miv6/jRmo5SLY8cTjmnkA3wC7o1L0jOey4Cki5N3kdjdPD/mW59G1Qsxa8c3y" crossorigin="anonymous">

<!-- KaTeX JS -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" integrity="sha384-7zkKLzPD3M4y9W8FWsN4Z0yO5eLu8qUn0QHY6hZ2r3fDzqjk0McYc3vJrmE2h6cZ" crossorigin="anonymous"></script>

<!-- 自动渲染扩展（可选功能） -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" integrity="sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTL0xF3iS9Ho94fSc31UyUyIDgWvB4" crossorigin="anonymous"></script>

<!-- 自动渲染配置 -->
<script>
  document.addEventListener("DOMContentLoaded", function() {
    renderMathInElement(document.body, {
      delimiters: [
        {left: "$$", right: "$$", display: true}, // 块级公式
        {left: "\\[", right: "\\]", display: true}, // 块级公式
        {left: "\\(", right: "\\)", display: false}, // 行内公式
        {left: "$", right: "$", display: false} // 行内公式
      ],
      throwOnError: false
    });
  });
</script>
```

### 3. 移除 MathJax 配置
删除布局文件中所有 MathJax 相关代码，包括 `<script type="text/x-mathjax-config">` 配置块和 MathJax CDN 脚本。KaTeX 通过上述自动渲染脚本实现类似功能。

### 4. 在 Markdown 中编写数学公式
配置完成后，您可以使用原有分隔符编写 LaTeX 公式：

- **行内公式**：使用 `$...$` 或 `\(...\)`（示例：`$E=mc^2$` 或 `\(E=mc^2\)`）
- **块级公式**：使用 `$$...$$` 或 `\[...\]`（示例：`$$E=mc^2$$` 或 `\[E=mc^2\]`）

示例如下：

```markdown
行内公式：$E=mc^2$ 或 \(E=mc^2\)

块级公式：
$$E=mc^2$$

或

\[E=mc^2\]
```

Kramdown 会配合 KaTeX 引擎将这些公式转换为可渲染的 HTML 结构。

### 5. KaTeX 与 MathJax 差异说明
- **公式自动编号**：KaTeX 不支持类似 MathJax 的 `autoNumber: "AMS"` 自动编号。如需编号，须在 LaTeX 代码中手动添加 `\tag{}`（示例：`$$E=mc^2 \tag{1}$$`）
- **性能表现**：KaTeX 渲染速度显著优于 MathJax，特别适合静态站点
- **功能支持**：KaTeX 支持的 LaTeX 命令少于 MathJax，请查阅 [KaTeX 支持列表](https://katex.org/docs/supported.html) 确认兼容性
- **渲染机制**：上述自动渲染脚本通过配置的分隔符数组模拟 MathJax 的自动渲染行为，可根据需要调整 `delimiters` 参数

### 6. 测试配置
通过 `jekyll serve` 本地运行站点，验证公式渲染效果。若遇到问题：
- 检查浏览器控制台的 KaTeX 报错信息
- 确认使用的 KaTeX CDN 链接为最新版本（当前示例为 0.16.11）
- 确保 Markdown 中的 LaTeX 语法符合 KaTeX 规范

### 7. 可选：本地部署 KaTeX
若需避免 CDN 依赖，可本地部署 KaTeX：
1. 从 [KaTeX 发布页](https://github.com/KaTeX/KaTeX/releases) 下载 `katex.min.css`、`katex.min.js` 和 `auto-render.min.js`
2. 将文件放置于资源目录（如 `assets/katex/`）
3. 更新资源链接指向本地文件（示例：`/assets/katex/katex.min.css`）

### 8. 故障排除
- **公式未渲染**：检查 KaTeX 脚本是否正常加载，并确认 `kramdown.math_engine` 设置为 `katex`
- **分隔符异常**：核对自动渲染脚本中的分隔符配置与 Markdown 使用是否一致
- **命令不支持**：若某些 LaTeX 命令失效，请查阅 KaTeX 文档或重构表达式

如需针对特定数学表达式或配置获得进一步帮助，请提供具体细节，我将为您提供定制化指导！
