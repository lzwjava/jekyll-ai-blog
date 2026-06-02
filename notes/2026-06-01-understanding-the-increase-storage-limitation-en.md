---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding The Increase Storage Limitation
translated: false
type: note
---

The answer is right there in the HTML:

```html
<input type="number" min="101" max="16384" step="1" value="101">
```

**`min="101"`** — the minimum allowed size is **101 GB**.

But `200 > 101`, so it should pass the HTML5 constraint. The "invalid size" error is likely because **your volume is already >= 200 GB**. This is an **"Increase storage size"** modal — it only allows values **greater than the current volume size**. You can't set it to 200 if the volume is already 200 or larger.

What's your current volume size? If it's already 200 GB, you'd need to enter at least 201.
