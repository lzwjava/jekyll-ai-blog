---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 Claude Code 调试 WhatsApp
translated: true
type: note
---

问题：我们可以使用 Claude Code 来检查和调试笔记本电脑上的本地应用程序（如 WhatsApp.app）吗？

回答：

是的，你可以使用 Claude Code 来检查本地应用程序目录并协助调试问题 —— 包括 WhatsApp 的 QR code 可能无法加载的原因。以下是详细说明：

## Claude Code 如何实现这一点

Claude Code 在你的 terminal 中运行，并具有访问本地 filesystem 的权限。当你运行以下命令时：

```bash
claude --dangerously-skip-permissions
```

它会给予 Claude Code 提升的权限来读取文件、列出目录、运行命令等。因此，它**可以**执行如下操作：

```bash
ls /Applications/WhatsApp.app/Contents/
cat /Applications/WhatsApp.app/Contents/Info.plist
```

这使得 Claude Code 能够检查 app bundle、核对版本、读取 config files，并可能识别出问题所在。

---

## 为什么 WhatsApp QR Code 可能会失效

QR code 无法加载或扫描的常见原因：

| 原因 | 详情 |
|---|---|
| **Network/Proxy 问题** | WhatsApp Web QR 需要出站 WebSocket 连接 |
| **App 版本过旧** | 旧版本的 WhatsApp 会被 Meta 的服务器屏蔽 |
| **App bundle 损坏** | `.app` 内部文件缺失或损坏 |
| **macOS 权限** | Camera 或网络访问在 System Settings 中被禁用 |
| **Firewall/VPN 拦截** | 公司或个人 VPN 可能会屏蔽 WhatsApp 的 endpoints |

---

## Claude Code 在此场景下能做什么

```bash
# 检查 app 版本
defaults read /Applications/WhatsApp.app/Contents/Info.plist CFBundleShortVersionString

# 检查 app bundle 是否完整
ls /Applications/WhatsApp.app/Contents/MacOS/

# 检查与 WhatsApp 服务器的网络连通性
curl -I https://web.whatsapp.com
```

Claude Code 可以为你运行所有这些命令并解释结果。

---

## 需要注意的限制

`--dangerously-skip-permissions` 标志会跳过 Claude Code 通常的安全提示。对于本地调试来说这是可以的，但在处理敏感项目或通过 `@file` 引用注入不受信任的 prompts 时请务必小心。

所以，是的 —— Claude Code 是调试此类本地 app 问题的合法且强大的工具！
