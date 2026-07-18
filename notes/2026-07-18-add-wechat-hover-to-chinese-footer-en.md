---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add WeChat hover to Chinese footer
translated: false
type: note
---

Pushed commit `fcf1c154c` to `origin/main`.

Regarding the WeChat QR hover:

It works on English pages, but **not on Chinese pages** — `_layouts/post.html:117-123` lists the Chinese footer as plain text:

```
微信：<strong>@lzwjava</strong>
```

while the English footer at line 124-130 uses the hover link:

```
WeChat: <a href="#" class="wechat-hover">@lzwjava<img src="/assets/images/contact/wechat.jpg" alt="WeChat QR"></a>
```

Want me to add the same `wechat-hover` QR to the Chinese footer too?
