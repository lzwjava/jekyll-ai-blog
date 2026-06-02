---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: The CSS Box Model Explained
translated: false
type: note
---

The CSS box model describes how every element in a webpage is rendered as a rectangular box. It consists of **four** layers (not three), but people sometimes group them into three when they combine padding + border + margin as "spacing". The precise and correct order, however, has **four distinct parts**.

Here is the correct structure, from the **inside** (center) to the **outside**:

1. **Content**
   The innermost part: the actual text, image, or other content of the element.
   Controlled by properties like `width`, `height`, `font-size`, etc.

2. **Padding**
   The space **inside** the element, between the content and the border.
   It is transparent (takes the background of the element).
   Controlled by `padding`, `padding-top`, `padding-right`, etc.

3. **Border**
   The line that surrounds the padding (and content).
   Controlled by `border`, `border-width`, `border-style`, `border-color`, etc.

4. **Margin**
   The outermost layer: transparent space **outside** the border, used to separate the element from neighboring elements.
   Controlled by `margin`, `margin-top`, etc.
   Can be negative and can cause margin collapsing.

### Visual order from inside → outside:

```
Margin (outside)
└─ Border
   └─ Padding
      └─ Content (text/image/etc.)
```

Or as a simple diagram:

```
+---------------------------+  ← Margin
|        Border             |
|  +---------------------+  |  ← Border
|  |      Padding        |  |
|  |  +---------------+  |  |
|  |  |   Content     |  |  |
|  |  +---------------+  |  |
|  |                     |  |
|  +---------------------+  |
|                           |
+---------------------------+
```

### Common "three-part" misconception
Some tutorials simplify it as:
1. Content
2. Padding/Border (grouped as "inner spacing + edge")
3. Margin

But technically and according to the official CSS specification, there are **four** parts in this exact order:
**content → padding → border → margin**

This order is critical when calculating the total space an element occupies (especially with `box-sizing: content-box` vs `box-sizing: border-box`).
