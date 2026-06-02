---
audio: false
generated: true
image: false
lang: en
layout: post
title: CSS Last of Type Explained
translated: false
type: note
---

**Question:** What does :last-of-type mean in CSS?

**Answer:**

The `:last-of-type` pseudo-class in CSS selects **the last element of its type** (its tag name) among its siblings inside the same parent.

### Key characteristics
- It looks at the **element type** (like `p`, `div`, `li`, `article`, etc.), **not** the class or any other attribute.
- It selects **only one element** per parent — the very last child that matches that particular tag name.
- It **ignores** other element types that come after it.

### Visual examples

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

→ Only "Last paragraph" becomes red + bold

### More common real-world examples

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

### :last-of-type vs :last-child — important difference

| Selector          | Selects the last child …                             | Cares about tag name? | Example that gets selected                     |
|-------------------|-------------------------------------------------------|-----------------------|------------------------------------------------|
| `:last-child`     | … regardless of its tag name                         | No                    | The very last element in the parent            |
| `:last-of-type`   | … but only if it is the last of **its own tag type** | Yes                   | Last element of that specific tag among siblings |

```html
<section>
  <h2>Title</h2>
  <p>Text</p>
  <p>Text</p>           ← p:last-of-type selects this
  <div>Footer</div>     ← div:last-of-type selects this
                         :last-child would select this div
</section>
```

### Summary — when to use `:last-of-type`

Use it when you want to target the **last occurrence of a specific element type** inside a container, especially when:
- There are mixed element types as siblings
- You cannot rely on `:last-child` because the last element might not be the type you want
- You are styling repeating elements like paragraphs, list items, articles, table cells, etc.

**References:**

- [MDN Web Docs: :last-of-type](https://developer.mozilla.org/en-US/docs/Web/CSS/:last-of-type)
- [CSS Tricks: :nth-child and :nth-of-type explained](https://css-tricks.com/how-nth-child-works/)
