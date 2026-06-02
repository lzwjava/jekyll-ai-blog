---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 下拉列表的 HTML 元素
translated: true
type: note
---

Question: 哪一个 HTML element 用于在 form 中创建 dropdown list？

Answer:

在 form 中创建 dropdown list（也称为 select menu）的正确 HTML element 是 **`<select>`**，它通常与用于定义具体选项的 `<option>` elements 配合使用。

### Explanation:

- `<select>` element 定义了 dropdown list 本身。
- 在其内部，多个 `<option>` elements 指定了可供选择的项目。
- Example:

```html
<label for="cars">Choose a car:</label>
<select id="cars" name="cars">
  <option value="volvo">Volvo</option>
  <option value="saab">Saab</option>
  <option value="mercedes">Mercedes</option>
  <option value="audi">Audi</option>
</select>
```

由于提供的选项（A) B) C) D)）似乎不完整，且其中一个列出的 `<dropdown>` **不是有效的 HTML element**，因此标准且正确的答案是 **`<select>`**。

References:
- [MDN Web Docs - <select> element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select)
- [W3Schools - HTML <select> Tag](https://www.w3schools.com/tags/tag_select.asp)
