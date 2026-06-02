---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Responsive Flexbox Layout Control
translated: false
type: note
---

The correct answer is **A. flex-direction**

To make a flex container switch from a row layout on large screens to a column layout on small screens, you change the `flex-direction` property inside a **media query**.

Example:

```css
.container {
  display: flex;
  flex-direction: row; /* default on large screens */
}

@media (max-width: 768px) {
  .container {
    flex-direction: column; /* switches to column on small screens */
  }
}
```

Explanation of why the others are wrong:

- **B. flex-wrap** – controls whether items wrap onto multiple lines, not the main direction (row vs column)
- **C. media query** – this is the *technique* used to apply changes at different screen sizes, but it’s not a CSS *property*. The actual property you change is `flex-direction`.
- **D. grid-template** – this belongs to CSS Grid, not Flexbox

So even though you need a media query (C) to trigger the change, the **property** that actually arranges items in a row or column is **flex-direction (A)**.

Correct answer: **A**
