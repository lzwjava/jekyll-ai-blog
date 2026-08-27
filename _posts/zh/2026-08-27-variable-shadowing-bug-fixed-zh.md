---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 变量遮蔽错误已修复
translated: true
type: note
---

已修复。实际问题是**变量影子**问题：`onScan(qrcode, status)` 参数中命名为 `qrcode` 的参数隐藏了同名的导入模块。在该函数内部，`qrcode` 指的是登录二维码字符串，因此 `qrcode.generate` 不存在。

我将模块导入重命名为 `qrcodeTerminal`，从而避免了冲突。重新运行：

```
node test.js
```

它将在终端中打印二维码，以便你扫码登录。