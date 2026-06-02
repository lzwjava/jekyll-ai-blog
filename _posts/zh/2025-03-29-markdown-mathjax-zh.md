---
audio: false
generated: true
lang: zh
layout: post
title: 数学公式渲染方案：MathJax与KaTeX对比
translated: true
type: note
---

要在网页上结合 LaTeX 数学公式渲染与 **Markdown** 渲染，通常需要同时使用 JavaScript 库（如 **MathJax** 或 **KaTeX**）和能够处理标准 Markdown 语法的解析器。目标是让用户能在 Markdown 中编写 LaTeX 数学公式，并在页面上正确渲染。

以下是实现方法：

### 1. **使用 MathJax 或 KaTeX 进行 Markdown 渲染**

您可以使用 **Markdown 解析器**（如 **marked.js** 或 **remarkable.js**）渲染基础 Markdown 内容，然后在渲染完成后使用 MathJax 或 KaTeX 处理其中的 LaTeX 数学公式。

以下是具体实现步骤：

---

### **步骤 1：引入库文件**

需要在 HTML 文件中同时引入 **Markdown 解析器**和**数学公式渲染库**（MathJax 或 KaTeX）。

引入方式如下：

```html
<!-- 引入 KaTeX（或 MathJax）用于 LaTeX 渲染 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.15.3/contrib/auto-render.min.js"></script>

<!-- 引入 Markdown 解析器（如 marked.js） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.0.10/marked.min.js"></script>
```

如果更倾向于使用 **MathJax**，可以这样引入：

```html
<script type="text/javascript" async
  src="https://cdn
