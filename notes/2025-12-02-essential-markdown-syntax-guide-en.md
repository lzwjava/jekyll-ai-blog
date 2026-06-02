---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Essential Markdown Syntax Guide
translated: false
type: note
---

Question: Can you provide a guide to the most common Markdown syntax?

Answer:

Markdown is a lightweight markup language that lets you format text easily. Here's a practical guide to the most commonly used syntax (works on GitHub, Reddit, Notion, Obsidian, etc.).

### Headings

```markdown
# H1 - Largest heading
## H2
### H3
#### H4
##### H5
###### H6 - Smallest heading
```

### Text Styling

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
~~strikethrough~~
`inline code`
```

### Lists

**Unordered lists**

```markdown
- Item 1
- Item 2
  - Sub-item (2 spaces or tab)
  - Sub-item
```

**Ordered lists**

```markdown
1. First item
2. Second item
   1. Sub-item
   2. Sub-item
```

### Links & Images

```markdown
[Link text](https://example.com)

[Link with title](https://example.com "Hover text")

![Alt text for image](https://example.com/image.jpg)

![Alt text](https://example.com/image.jpg "Optional title")
```

### Blockquotes

```markdown
> This is a blockquote
>
> Can span multiple lines
>> Nested blockquote
```

### Code Blocks

Inline: `` `code` ``

Fenced code block (recommended):
    ```markdown
    ```python
    print("Hello, world!")
    x = 42
    ```
    ```

Or without language:
    ```markdown
    ```
    Plain text code block
    ```
    ```

### Horizontal Rule

```markdown
---
***
- - -
```

### Tables

```markdown
| Header 1   | Header 2   | Header 3      |
|------------|:----------:|--------------:|
| Left       |  Center    |         Right |
| Normal     |   Bold     |     *Italic*  |
```

### Task Lists (supported on GitHub, Notion, etc.)

```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another one
```

### Escaping Characters

To display a literal character that would otherwise be interpreted:

```markdown
\*literal asterisks\*
\`backtick\`
```

### Quick Reference Table

| Feature          | Syntax                              | Result                    |
|------------------|-------------------------------------|-----------------------------------|
| Bold             | `**text**` or `__text__`            | **text**                  |
| Italic           | `*text*` or `_text_`                | *text*                    |
| Strikethrough    | `~~text~~`                          | ~~text~~                  |
| Inline code      | `` `code` ``                        | `code`                    |
| Link             | `[text](url)`                       | [text](url)               |
| Image            | `![alt](url)`                       | (image)                   |
| Heading 1        | `# Heading`                         | Huge heading            |
| Blockquote       | `> text`                            | > text                    |
| Code block       | ```language:disable-run

That's 95% of what most people use daily! Different platforms support slight variations (e.g., GitHub adds footnotes, emojis :smile:, and mermaid diagrams), but the above works almost everywhere.

* [Mastering Markdown · GitHub Guides](https://guides.github.com/features/mastering-markdown/)
* [Markdown Guide by Matt Cone](https://www.markdownguide.org/basic-syntax/)

```
