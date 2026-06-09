---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH隧道到本地端口5001
translated: true
type: note
---

端口5001可用。在终端中运行以下命令（前台运行，保持打开直到按Ctrl+C）：

```
ssh -L 5001:127.0.0.1:5001 amd-cloud -N
```

然后在浏览器中打开 <http://localhost:5001。完成后按> `Ctrl+C` 关闭隧道。
