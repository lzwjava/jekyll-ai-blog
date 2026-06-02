---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 macOS 上的 WhatsApp 摄像头权限
translated: true
type: note
---

这是一个常见的 macOS 权限问题。当一个应用没有出现在 Privacy & Security 设置中时，意味着它尚未请求该权限。以下是解决方法：

## 强制 WhatsApp 请求 camera 权限：

1. **完全退出 WhatsApp**（使用 Cmd+Q，而不仅仅是关闭窗口）

2. **重置 WhatsApp 的 TCC database**（这将清除其权限状态）：
   ```bash
   tccutil reset Camera com.whatsapp.WhatsApp
   ```

3. **重新启动 WhatsApp** 并尝试再次扫描 QR code。现在应该会弹出请求 camera 权限的提示。

## 如果上述方法不起作用：

**手动编辑 TCC database**（高级）：
```bash
# 打开 TCC database
sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceCamera','com.whatsapp.WhatsApp',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1687910000);"
```

然后重新启动 WhatsApp。

## 备选方案：改用 WhatsApp Web

如果 camera 权限问题仍然存在，你可以完全跳过它：
1. 在手机上打开 WhatsApp
2. 前往 Settings > Linked Devices > Link a Device
3. 在 Mac 上，在浏览器中打开 https://web.whatsapp.com
4. 用手机扫描 QR code（而不是使用 Mac camera）

这样你就是在使用手机的 camera 进行扫描，从而完全避开了 Mac 的权限问题。

请先尝试执行 `tccutil reset` 命令 —— 这通常能解决问题。
