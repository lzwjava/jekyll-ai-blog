---
audio: false
generated: true
image: false
lang: en
layout: post
title: Variable Shadowing Bug Fixed
translated: false
type: note
---

Fixed. The real problem was a **variable shadowing** issue: the `onScan(qrcode, status)` parameter named `qrcode` was hiding the imported module of the same name. Inside that function, `qrcode` referred to the login QR string, so `qrcode.generate` didn't exist.

I renamed the module import to `qrcodeTerminal` so there's no conflict. Run it again:

```
node test.js
```

It should print the QR code in the terminal so you can scan and log in.
