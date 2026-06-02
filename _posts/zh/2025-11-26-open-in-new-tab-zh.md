---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: HTML链接在新标签页中打开
translated: true
type: note
---

以下是创建指向 <https://www.tsinghua.edu.cn> 的超链接（在新标签页/窗口中打开）的完整最小 HTML 代码：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>清华大学链接</title>
</head>
<body>
    <p>访问 <a href="https://www.tsinghua.edu.cn" target="_blank" rel="noopener noreferrer">清华大学</a></p>
</body>
</html>
```

关键要点：

- `target="_blank"` 强制链接在新标签页/窗口中打开
- `rel="noopener noreferrer"` 是在使用 `target="_blank"` 时的安全/最佳实践补充，可防止新页面获得对原始页面的控制权

您可以将此代码复制并粘贴到 `.html` 文件中，并在任何浏览器中打开。
