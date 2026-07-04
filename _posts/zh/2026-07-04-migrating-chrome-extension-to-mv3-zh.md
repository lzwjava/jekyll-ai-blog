---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Chrome扩展迁移至MV3
translated: true
type: note
---

已完成。该扩展已从 MV2 迁移到 MV3。以下是变更内容：

**`manifest.json`** — MV2（`browser_action`、`background.page`）→ MV3（`action`、`background.service_worker`），移除了 `content_security_policy`（MV3 不允许使用 `unsafe-eval`，且当前也不再需要）

**`background.js`** — 原为基础页面形式的后台脚本，依赖 RequireJS + `background.html`。现改为 Service Worker，使用 `importScripts('js/lib/underscore.js')`，并将标签页管理器和设置逻辑直接内联。不再涉及 DOM、`window` 或 RequireJS。

**`popup.js`** — 将 `chrome.extension.getBackgroundPage().GlobalObject.settings.get()` 替换为直接的 `chrome.storage.sync.get/set` 调用，不再依赖后台页面。同时将 `_.template()` 替换为纯 jQuery DOM 构建（避免使用 `unsafe-eval`）。

**已移除** — `background.html`、`app.build.js`、`js/require.js`、`js/tabmanager.js`、`js/settings.js`（均为 MV3 中的无效代码）

现在在 Chromium 中加载：

1. 打开 `chrome://extensions` → 开启 **开发者模式**（右上角）→ 点击 **加载已解压的扩展程序**
2. 选择 `/home/lzw/projects/tab-killer/chrome-tab-killer`
3. 点击扩展图标即可设置最大标签页数和白名单