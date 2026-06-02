---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Mihomo 修复 WhatsApp 二维码登录问题
translated: true
type: note
---

Question: 如何修复在使用 Mihomo proxy 时 WhatsApp macOS 版 QR code 无法加载的问题？

Answer:

根据你的对话日志，根本原因是你的 **Mihomo proxy 干扰了 WhatsApp 与其服务器的连接**。以下是完整的逐步修复方案：

---

## Step 1 — 修复 Mihomo Config (正确路由 WhatsApp)

你的 config 中已经包含 WhatsApp 规则，但它们在 `DIRECT` 和 `Proxy` 之间切换。正确的选择取决于你的网络状况：

**方案 A：通过 proxy 路由 WhatsApp（如果你的地区限制直接访问互联网，推荐此方案）**

编辑 `~/.config/mihomo/config.yaml`，并确保以下行出现在 `RULE-SET,Global` 行**之前**：

```yaml
- DOMAIN-SUFFIX,whatsapp.com,Proxy
- DOMAIN-SUFFIX,whatsapp.net,Proxy
- DOMAIN-SUFFIX,wa.me,Proxy
```

**方案 B：直接路由 WhatsApp（绕过 proxy）**

```yaml
- DOMAIN-SUFFIX,whatsapp.com,DIRECT
- DOMAIN-SUFFIX,whatsapp.net,DIRECT
- DOMAIN-SUFFIX,wa.me,DIRECT
```

---

## Step 2 — 正确重启 Mihomo

会话日志显示 mihomo 在执行命令中途被终止。请干净地执行重启：

```bash
# 终止现有的 mihomo 进程
pkill -f mihomo

# 等待片刻
sleep 2

# 重启 mihomo (请根据你的实际 binary 路径调整)
nohup /Users/lzwjava/projects/mihomo-darwin-amd64-v1-alpha-3035ae8 \
  -d /Users/lzwjava/.config/mihomo > /tmp/mihomo.log 2>&1 &

# 验证其是否正在运行
ps aux | grep -i mihomo | grep -v grep
```

---

## Step 3 — 重置 WhatsApp Camera 权限

对话日志还显示 Camera 权限使用了错误的 bundle ID 进行重置。正确的 ID 如下：

```bash
tccutil reset Camera net.whatsapp.WhatsApp
```

---

## Step 4 — 重启 WhatsApp

```bash
# 完全退出 WhatsApp
osascript -e 'quit app "WhatsApp"'
sleep 2

# 重新打开
open -a WhatsApp
```

当 WhatsApp 打开时，现在应该会提示 Camera 权限请求 —— 点击 **Allow**。

---

## Step 5 — 验证连通性

测试 WhatsApp 服务器是否可以通过你的 proxy 访问：

```bash
curl -I --proxy http://127.0.0.1:7890 https://web.whatsapp.com
```

如果你收到 HTTP `301` 或 `200` 响应，说明 proxy 路由工作正常。

---

## 备选方案 — 使用手机 Camera (无需 Mac Camera)

如果 QR code 仍然没有出现，你可以在浏览器中使用 WhatsApp Web —— 访问 `web.whatsapp.com`，然后通过手机上的 WhatsApp App 扫描 QR code：Settings > Linked Devices > Link a Device。这可以完全绕过 Mac 的 Camera 权限问题。

---

## 日志中发现的根本原因总结

| Issue | Status | Fix |
|---|---|---|
| 错误的 bundle ID (`com.whatsapp.WhatsApp`) | ✅ Fixed | 使用 `net.whatsapp.WhatsApp` |
| WhatsApp domains 未包含在 proxy rules 中 | ✅ Fixed | 已添加到 config |
| Mihomo 未正常重启 | ⚠️ Incomplete | 使用 `pkill -f mihomo` 后重启 |
| 未授予 Camera 权限 | ⚠️ Pending | 重置 + 重新打开 WhatsApp |

References:

- [How to fix WhatsApp not working on Mac - MacPaw](https://macpaw.com/how-to/fix-whatsapp-not-working-on-mac)
- [WhatsApp Web QR Code Not Working - TechViral](https://techviral.net/whatsapp-web-qr-code-not-working/)
- [WhatsApp Web QR Code Fix - HelpDeskGeek](https://helpdeskgeek.com/whatsapp-web-qr-code-not-working-8-fixes-to-try/)
