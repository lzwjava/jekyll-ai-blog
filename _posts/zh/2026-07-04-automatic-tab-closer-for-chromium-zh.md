---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chromium自动标签关闭器
translated: true
type: note
---

这个项目**可以**在 Chromium 上提供帮助。它是在 `safari-tab-killer/` 目录下的一个 Chrome 扩展——Chromium 原生支持 Chrome 扩展。Safari 的 Xcode 部分只是同一扩展逻辑的 macOS 封装。

**功能说明：** 当标签页数量超过设定的 `maxTabs` 上限时，自动关闭最旧的标签页。受保护的 URL 可通过白名单设置。通过弹出式 UI 进行配置。

**如何加载到 Chromium（在本机上）：**

```bash
chromium-browser
```

然后在 Chromium 中：

1. 导航到 `chrome://extensions`
2. 启用 **开发者模式**（右上角开关）
3. 点击 **加载已解压的扩展程序**
4. 选择 `/home/lzw/projects/tab-killer/safari-tab-killer/`

这样就完成了。扩展程序将开始运行。默认的最大标签页数可能未定义（需要在弹出窗口中设置）。点击扩展图标进行配置：

- **最大标签页数** — 达到此数量时标签页杀手开始工作
- **白名单** — 永不自动关闭的 URL 模式（例如 `github.com`、`mail.google.com`）

需要我同时检查当前已安装的 Chromium 扩展，或者直接打开并加载该扩展吗？
