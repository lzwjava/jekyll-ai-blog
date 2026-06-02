---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: HTML Description List Tags Explained
translated: false
type: note
---

Question: What does `<dl>`, `<dt>`, and `<dd>` mean in HTML?

Answer:

In HTML, `<dl>`, `<dt>`, and `<dd>` are tags used together to create a **description list** (formerly called a definition list). This is the standard way to mark up glossaries, metadata, question-and-answer pairs, or any list where each item has a **term** and one or more **descriptions/details**.

| Tag   | Meaning                  | Description                                                                 |
|-------|--------------------------|-----------------------------------------------------------------------------|
| `<dl>`| Description List         | The container element for the entire list.                                  |
| `<dt>`| Description Term         | The term, name, or title being described (like a glossary word or question).|
| `<dd>`| Description Details      | The description, definition, or details for the preceding `<dt>`. You can have multiple `<dd>` for one `<dt>`. |

### Example

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

This renders as a clean, semantic list (browsers usually indent the `<dd>` content):

**HTML**
 HyperText Markup Language – the standard language for creating web pages.

**CSS**
 Cascading Style Sheets – used to style and layout web pages.
 Can be written inline, internally, or in external files.

**JavaScript**
 A programming language that adds interactivity to websites.

Using these tags instead of plain `<ul>` or `<div>`s is better for accessibility (screen readers announce them as definition lists) and SEO.
