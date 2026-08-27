---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix ESM Requirement for QR Code
translated: false
type: note
---

Fixed. Because your `package.json` has `"type": "module"`, the file runs as an ES module where `require` isn't defined. I replaced it with a proper ESM import:

- `import qrcode from 'qrcode-terminal';` at the top
- Changed `require('qrcode-terminal').generate(...)` to `qrcode.generate(...)`

Now run it again with `node test.js`. It will show the QR code in the terminal so you can scan and log in.
