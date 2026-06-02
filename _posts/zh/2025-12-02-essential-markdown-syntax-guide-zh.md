---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Markdown基本语法指南
translated: true
type: note
---

问题：您能提供一份最常见的 Markdown 语法指南吗？

回答：

Markdown 是一种轻量级标记语言，可让您轻松格式化文本。以下是最常用语法的实用指南（适用于 GitHub、Reddit、Notion、Obsidian 等）。

### 标题

```markdown
# H1 - 最大标题
## H2
### H3
#### H4
##### H5
###### H6 - 最小标题
```

### 文本样式

```markdown
*斜体* 或 _斜体_
**粗体** 或 __粗体__
***粗斜体*** 或 ___粗斜体___
~~删除线~~
`行内代码`
```

### 列表

**无序列表**

```markdown
- 项目 1
- 项目 2
  - 子项目（2 个空格或 Tab 键）
  - 子项目
```

**有序列表**

```markdown
1. 第一项
2. 第二项
   1. 子项目
   2. 子项目
```

### 链接和图片

```markdown
[链接文本](https://example.com)

[带标题的链接](https://example.com "悬停文本")

![图片的 Alt 文本](https://example.com/image.jpg)

![Alt 文本](https://example.com/image.jpg "可选标题")
```

### 块引用

```markdown
> 这是一个块引用
>
> 可以跨多行
>> 嵌套块引用
```

### 代码块

行内：`` `code` ``

围栏代码块（推荐）：
    ```markdown
    ```python
    print("Hello, world!")
    x = 42
    ```
    ```

或不带语言：
    ```markdown
    ```
    纯文本代码块
    ```
    ```

### 水平线

```markdown
---
***
- - -
```

### 表格

```markdown
| 标题 1   | 标题 2   | 标题 3      |
|------------|:----------:|--------------:|
| 左对齐     |   居中     |         右对齐 |
| 普通文本   |   **粗体**  |     *斜体*    |
```

### 任务列表（GitHub、Notion 等支持）

```markdown
- [x] 已完成任务
- [ ] 未完成任务
- [ ] 另一个
```

### 转义字符

若要显示一个原本会被解释为语法的字面字符：

```markdown
\*字面星号\*
\`反引号\`
```

### 速查表

| 特性          | 语法                              | 结果                    |
|------------------|-------------------------------------|-----------------------------------|
| 粗体             | `**text**` 或 `__text__`            | **text**                  |
| 斜体           | `*text*` 或 `_text_`                | *text*                    |
| 删除线    | `~~text~~`                          | ~~text~~                  |
| 行内代码      | `` `code` ``                        | `code`                    |
| 链接             | `[text](url)`                       | [text](url)               |
| 图片            | `![alt](url)`                       | (image)                   |
| 标题 1        | `# Heading`                         | 巨大的标题            |
| 块引用       | `> text`                            | > text                    |
| 代码块       | ```language:disable-run

这涵盖了大多数人日常使用的 95%！不同的平台支持细微的变体（例如，GitHub 添加了脚注、表情符号 :smile: 和美人鱼图表），但上述内容几乎适用于所有地方。

* [Mastering Markdown · GitHub Guides](https://guides.github.com/features/mastering-markdown/)
* [Markdown Guide by Matt Cone](https://www.markdownguide.org/basic-syntax/)

```
