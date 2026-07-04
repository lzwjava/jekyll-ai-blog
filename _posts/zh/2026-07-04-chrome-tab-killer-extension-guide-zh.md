---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chrome标签页杀手扩展指南
translated: true
type: note
---

你说得对。`chrome-tab-killer/` 才是正确的——它只是 Chrome 扩展，没有 Safari Xcode 外壳（`safari-tab-killer/` 同时包含两者）。

```
/home/lzw/projects/tab-killer/chrome-tab-killer/
├── manifest.json
├── background.js / background.html
├── popup.html / popup.js
├── js/tabmanager.js
├── js/settings.js
├── css/popup.css
└── img/
```

在 Chromium 中加载此扩展：

1. 打开 `chrome://extensions`
2. 启用 **开发者模式**
3. 点击 **加载已解压的扩展程序** → 选择 `/home/lzw/projects/tab-killer/chrome-tab-killer`

扩展会立即启动。点击它的图标即可设置最大标签页限制和白名单。

需要我打开 Chromium 和你一起操作，还是直接交给你处理？