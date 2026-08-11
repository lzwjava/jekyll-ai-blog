---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Installed and Ready
translated: false
type: note
---

Done! ✅ WeChat is installed and ready to use.

**Summary:**

- **Package:** `wechat` version **4.1.1.8** installed via dpkg
- **Missing dependencies fixed:** Installed `libxcb-icccm4`, `libxcb-image0`, `libxcb-render-util0`, `libxcb-keysyms1` (Qt xcb libraries needed by WeChat)
- **Verify:** `dpkg -s wechat` shows `install ok installed`, and all libraries resolve

You can launch it with:

```bash
wechat
```

or from your application launcher (search for "微信" / WeChat).
