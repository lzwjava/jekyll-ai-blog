---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复ESM对二维码的要求
translated: true
type: note
---

已修复。因为你的 `package.json` 中设置了 `"type": "module"`，文件会作为 ES 模块运行，此时 `require` 未定义。我已将其替换为正确的 ESM 导入方式：

- 在文件顶部添加 `import qrcode from 'qrcode-terminal';`  
- 将 `require('qrcode-terminal').generate(...)` 改为 `qrcode.generate(...)`  

现在重新用 `node test.js` 运行。它会将二维码显示在终端中，供你扫码登录。
