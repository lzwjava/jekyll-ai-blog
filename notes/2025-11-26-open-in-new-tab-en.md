---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: HTML Link Opening in New Tab
translated: false
type: note
---

Here is the complete minimal HTML code to create a hyperlink to <https://www.tsinghua.edu.cn> that opens in a new tab/window:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tsinghua University Link</title>
</head>
<body>
    <p>Visit <a href="https://www.tsinghua.edu.cn" target="_blank" rel="noopener noreferrer">Tsinghua University</a></p>
</body>
</html>
```

Key points:

- `target="_blank"` forces the link to open in a new tab/window
- `rel="noopener noreferrer"` is a security/best-practice addition when using `target="_blank"` to prevent the new page from gaining control over the original page

You can copy and paste this code into an `.html` file and open it in any browser.
