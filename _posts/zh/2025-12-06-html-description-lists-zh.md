---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: HTML描述列表标签详解
translated: true
type: note
---

问题：`dl`、`dt` 和 `dd` 在 HTML 中是什么意思？

回答：

在 HTML 中，`<dl>`、`<dt>` 和 `<dd>` 标签一起使用，用于创建**描述列表**（以前称为定义列表）。这是标记词汇表、元数据、问答对或任何每个项目都有一个**术语**和一个或多个**描述/详细信息**的列表的标准方法。

| 标签 | 含义               | 描述                                                                    |
|------|--------------------|-------------------------------------------------------------------------|
| `<dl>` | Description List   | 整个列表的容器元素。                                                    |
| `<dt>` | Description Term   | 被描述的术语、名称或标题（如词汇表中的单词或问题）。                    |
| `<dd>` | Description Details| 前一个 `<dt>` 的描述、定义或详细信息。一个 `<dt>` 可以有多个 `<dd>`。 |

### 示例

```html
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language – the standard language for creating web pages.</dd>

  <dt>CSS</dt>
  <dd>Cascading Style Sheets – used to style and layout web pages.</dd>
  <dd>Can be written inline, internally, or in external files.</dd>

  <dt>JavaScript</dt>
  <dd>A programming language that adds interactivity to websites.</dd>
</dl>
```

这会渲染成一个清晰、语义化的列表（浏览器通常会缩进 `<dd>` 内容）：

**HTML**
 HyperText Markup Language – the standard language for creating web pages.

**CSS**
 Cascading Style Sheets – used to style and layout web pages.
 Can be written inline, internally, or in external files.

**JavaScript**
 A programming language that adds interactivity to websites.

使用这些标签而不是普通的 `<ul>` 或 `<div>` 对于可访问性（屏幕阅读器将其宣布为定义列表）和 SEO 更好。
