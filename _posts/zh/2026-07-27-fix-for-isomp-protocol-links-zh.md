---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复isomp://协议链接
translated: true
type: note
---

## 🔍 解码后的 `isomp://` URI

Base64 负载解码后得到：

```
[GATEWAY_IP] 12025 mstsc [UUID] rdp [TARGET_IP]
```

| 字段 | 值 |
| ------- | ------- |
| SSO 网关 | `xxx.xxx.x.xx` |
| 网关端口 | `12025` |
| 协议 | **RDP**（远程桌面 / mstsc） |
| 会话 UUID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| 目标服务器 | `xxx.xxx.x.xxx` |

---

## ❌ 问题

`isomp://` 协议处理程序在 **Windows 注册表中缺失**，因此点击任何 `isomp://` 链接均无反应。IsompSSO 客户端 (`sso.exe`) 无法自动启动。

---

## ✅ 已应用的修复

在 Windows 注册表中注册了 `isomp://` 协议：

**创建的 `.reg` 文件位于：** `C:\Program Files\IsompSSO\register_isomp.reg`

**已添加的注册表项：**

- `HKCR\isomp` → `URL:IsompSSO Protocol`
- `HKCR\isomp\shell\open\command` → `"C:\Program Files\IsompSSO\sso.exe" "%1"`

这将告诉 Windows 将所有 `isomp://` URL 传递给 `sso.exe`。

---

## 🔧 RDP 文件调整

在已保存的 `Default.rdp` 文件中，将以下内容更改：

| 之前 | 之后 |
|--------|-------|
| `prompt for credentials:i:0` | `prompt for credentials:i:1` |

这样，当自动认证失败时，将允许显示凭据对话框。

---

## ✅ 结果

注册协议后，`sso.exe` 成功：

1. 接收到 `isomp://` URL
2. 解码了 base64 负载
3. 使用会话 UUID 通过 SSO 网关进行认证
4. 启动了 **mstsc.exe**（远程桌面）以连接到目标服务器

所有 `isomp://` 链接今后将自动正常工作。
