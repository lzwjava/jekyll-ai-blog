---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CSS :last-of-type 详解
translated: true
type: note
---

**问题：** CSS 中的 :last-of-type 是什么意思？

**答案：**

CSS 中的 `:last-of-type` 伪类选择同一父元素内其同胞元素中**最后一种类型的元素**（其标签名）。

### 关键特性

- 它关注**元素类型**（如 `p`、`div`、`li`、`article` 等），**不**关注类或其他属性。
- 每个父元素**只选择一个元素**——匹配该特定标签名的最后一个子元素。
- 它**忽略**其后出现的其他元素类型。

### 视觉示例

```html
<div class="container">
  <p>First paragraph</p>
  <p>Second paragraph</p>
  <div>Some div</div>
  <p>Last paragraph</p>     ← this one is selected by p:last-of-type
  <div>Another div</div>
</div>
```

```css
p:last-of-type {
  color: red;
  font-weight: bold;
}
```

→ 只有“Last paragraph”变为红色 + 粗体

### 更常见的真实世界示例

```css
/* Last <li> in any <ul> or <ol> */
li:last-of-type {
  border-bottom: none;
}

/* Last article inside a section (very common pattern) */
article:last-of-type {
  margin-bottom: 0;
}

/* Last <td> in every table row */
tr td:last-of-type {
  text-align: right;
}

/* Last <p> inside an .entry-content (blog post style) */
.entry-content p:last-of-type {
  margin-bottom: 1.8em;
}
```

### :last-of-type 与 :last-child 的区别——重要差异

| 选择器             | 选择最后一个子元素……                                 | 是否关心标签名？ | 示例中被选中的元素                             |
|--------------------|-------------------------------------------------------|-------------------|------------------------------------------------|
| `:last-child`      | …无论其标签名是什么                                   | 否                | 父元素中的最后一个元素                         |
| `:last-of-type`    | …但仅限于**其自身标签类型的最后一个**                 | 是                | 同胞元素中该特定标签的最后一个元素             |

```html
<section>
  <h2>Title</h2>
  <p>Text</p>
  <p>Text</p>           ← p:last-of-type 选择这个
  <div>Footer</div>     ← div:last-of-type 选择这个
                         :last-child 会选择这个 div
</section>
```

### 总结——何时使用 `:last-of-type`

当你想针对容器内**特定元素类型的最后一次出现**时使用它，特别是当：
- 同胞元素中有混合的元素类型
- 不能依赖 `:last-child`，因为最后一个元素可能不是你想要的类型
- 你正在样式化重复元素，如段落、列表项、文章、表格单元格等。

**参考资料：**  

- [MDN Web Docs: :last-of-type](https://developer.mozilla.org/en-US/docs/Web/CSS/:last-of-type)  
- [CSS Tricks: :nth-child and :nth-of-type explained](https://css-tricks.com/how-nth-child-works/)