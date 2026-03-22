---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 排除 WhatsApp 二维码问题故障
translated: true
type: note
---

该应用程序本身看起来正常（版本 26.11.21，与您的 macOS 26.3.1 兼容）。QR code 问题可能是由以下原因之一引起的：

**最常见的原因：**

1. **Camera 权限被拒绝** — 前往 `System Settings > Privacy & Security > Camera` 并确保 WhatsApp 已启用。

2. **Network 问题** — 生成 QR code 需要网络连接。请检查网络是否正常工作。

3. **App 缓存过旧** — 尝试完全退出 WhatsApp（`Cmd+Q`）并重新启动。

4. **macOS 26 beta 兼容性** — 您正在运行 macOS 26.3.1（非常新/测试版）。WhatsApp 的 DTPlatformVersion 也是 26.2，因此它应该是兼容的，但测试版 OS 可能会导致意外的 UI bugs。

**可以尝试的快速修复方法：**

```bash
# Force quit WhatsApp
killall WhatsApp

# Clear WhatsApp cache
rm -rf ~/Library/Caches/net.whatsapp.WhatsApp
```

然后重新启动 WhatsApp。如果 QR code 仍然不显示，请检查 `System Settings > Privacy & Security > Camera`。

您能否更具体地描述一下发生了什么 —— 是 QR code 完全没有出现，还是出现了但扫描失败？