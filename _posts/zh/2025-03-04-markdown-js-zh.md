---
audio: false
generated: true
lang: zh
layout: post
title: Markdown的JavaScript库
translated: true
type: note
---

看起来您是在询问如何使用 `marked` 库的 `^0.3.6` 版本——这是一个用于解析 Markdown 文本并将其转换为 HTML 的 JavaScript 库。由于您通过 `^0.3.6` 表示法（可能来自 Node.js 项目中的 `package.json` 文件）引用了特定版本，我将指导您使用这个旧版本的 `marked`。请注意，`0.3.6` 版本相当老旧（大约在 2016 年发布），此后该库已有了显著发展。不过，我将遵循适用于该版本的方法。

### 步骤 1：安装

如果您在 Node.js 环境中工作，可以使用 npm 安装 `marked` 的 `0.3.6` 版本：

```bash
npm install marked@0.3.6
```

`package.json` 中的 `^0.3.6` 表示它将安装 `0.3.6` 或任何兼容的补丁更新（例如 `0.3.7`），但为了清晰起见，上面的命令将其锁定为确切的 `0.3.6`。

### 步骤 2：基本用法

以下是在不同环境中使用 `marked` 版本 `0.3.6` 的方法：

#### 在 Node.js 中

1. **引入库**：
   创建一个文件（例如 `index.js`）并添加以下内容：

   ```javascript
   var marked = require('marked');
   ```

2. **将 Markdown 转换为 HTML**：
   通过将 Markdown 字符串传递给 `marked()` 函数来使用它。例如：

   ```javascript
   var markdownString = '# Hello World\n这是**粗体**文本。';
   var html = marked(markdownString);
   console.log(html);
   ```

   **输出**：

   ```html
   <h1>Hello World</h1>
   <p>这是 <strong>粗体</strong> 文本。</p>
   ```

#### 在浏览器中

1. **包含库**：
   您可以使用 CDN 或下载 `marked@0.3.6` 并通过 `<script>` 标签包含它。例如，使用历史 CDN 链接（如果可用）或本地文件：

   ```html
   <script src="https://cdn.jsdelivr.net/npm/marked@0.3.6"></script>
   ```

2. **在 JavaScript 中使用**：
   包含脚本后，`marked` 将在全局可用：

   ```html
   <script>
     var markdownString = '# Hello World\n这是**粗体**文本。';
     var html = marked(markdownString);
     console.log(html);
   </script>
   ```

### 步骤 3：选项（适用于 0.3.6 版本）

`0.3.6` 版本支持一些自定义选项。您可以将选项对象作为第二个参数传递给 `marked()`。以下是一个示例：

```javascript
var markdownString = '# Hello\n这是带有 *文本* 和 `代码` 的内容。';
var html = marked(markdownString, {
  gfm: true,         // 启用 GitHub 风味 Markdown
  tables: true,      // 启用 GFM 表格
  breaks: false,     // 如果为 true，在单行换行处添加 <br>
  pedantic: false,   // 如果为 true，遵循严格的 Markdown 规范
  sanitize: false,   // 如果为 true，出于安全考虑会剥离 HTML 标签
  smartLists: true,  // 改进列表渲染
  smartypants: false // 如果为 true，使用“智能”排版（例如，弯引号）
});
console.log(html);
```

### 0.3.6 版本的主要特性

- **基本 Markdown**：支持标题（`#`）、粗体（`**`）、斜体（`*`）、列表、代码块（```）等。
- **GFM 支持**：如果设置了 `gfm: true`，则可以使用 GitHub 风味 Markdown（如表格和任务列表）。
- **无渲染器自定义**：与新版本不同，`0.3.6` 不支持自定义渲染器，因此您只能使用其默认输出。

### 包含更多 Markdown 的示例

以下是 Node.js 中的一个更完整的示例：

```javascript
var marked = require('marked');

var markdown = `
# 我的标题
## 副标题

- 项目 1
- 项目 2

\`\`\`
console.log("Hello");
\`\`\`

| 姓名  | 年龄 |
|-------|-----|
| Alice | 25  |
| Bob   | 30  |
`;

var html = marked(markdown, { gfm: true, tables: true });
console.log(html);
```

**输出**：

```html
<h1>我的标题</h1>
<h2>副标题</h2>
<ul>
<li>项目 1</li>
<li>项目 2</li>
</ul>
<pre><code>console.log("Hello");
</code></pre>
<table>
<thead>
<tr>
<th>姓名</th>
<th>年龄</th>
</tr>
</thead>
<tbody>
<tr>
<td>Alice</td>
<td>25</td>
</tr>
<tr>
<td>Bob</td>
<td>30</td>
</tr>
</tbody>
</table>
```

### 注意事项

- **清理**：如果要渲染用户输入，请设置 `sanitize: true` 以剥离原始 HTML 以确保安全（例如 `<script>` 标签）。然而，这在 `0.3.6` 中是基本功能，不如现代替代方案健壮。
- **限制**：此版本缺少后续版本中添加的功能（例如异步解析、自定义分词器），因此如果您需要更多功能，请考虑升级到较新版本，如 `5.x`。
- **调试**：如果无法正常工作，请确保正确加载了库并检查 Markdown 语法。
