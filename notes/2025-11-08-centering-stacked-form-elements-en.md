---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Centering Stacked Form Elements with Flexbox
translated: false
type: note
---

```css
.sort-container {
    display: flex;
    flex-direction: column; /* Add this to stack items vertically */
    align-items: center; /* Centers items horizontally in the column */
    justify-content: center; /* Centers the column vertically */
    gap: 10px;
    margin-bottom: 1rem;
}

.sort-container select {
    padding: 5px;
    font-size: 16px;
}

.sort-container .post-number {
    font-size: 16px;
}
```

### Explanation
- **flex-direction: column**: Changes the main axis from horizontal (row) to vertical, stacking the `select` and `.post-number` elements top-to-bottom.
- **align-items: center**: Keeps horizontal centering of child elements.
- **justify-content: center**: Centers the entire vertical stack within the container.
- I also fixed the nested selector syntax (moved `select` and `.post-number` outside the main block for better practice, assuming they are direct children—adjust if needed). The `gap` now applies vertically between items.
