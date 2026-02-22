---
audio: false
generated: true
image: false
lang: en
layout: post
title: HTML Text Wrapping Rules Explained
translated: false
type: note
---

Question: In HTML, if no line break tags are used, when does the text wrap to a new line?

Answer: 

In standard HTML rendering, if no explicit line break markers (such as the `<br>` tag) or block-level elements are used within a paragraph of text, the browser automatically handles line wrapping based on the **width of the containing element** (the viewport or the parent container).

The text will continue on the same line until it reaches the **boundary of the window** (or the specific container's width). Once the text hits this boundary, the browser automatically wraps the remaining content to the next line to ensure it fits within the visible area. This behavior is known as "word wrapping."

Therefore, the statement that line breaks only occur when encountering the window boundary (in the absence of manual markers) is **correct**.

References:  

- [https://developer.mozilla.org/en-US/docs/Web/CSS/white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)
- [https://www.w3.org/TR/CSS2/text.html#white-space-prop](https://www.w3.org/TR/CSS2/text.html#white-space-prop)