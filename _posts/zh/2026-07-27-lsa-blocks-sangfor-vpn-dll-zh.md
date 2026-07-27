---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LSA阻止深信服VPN DLL
translated: true
type: note
---

这是一个关于 Windows 安全机制的极好问题。让我详细解释为什么 **sangfornspx64.dll**（深信服 VPN/网络访问组件）会被 Windows 的 **本地安全机构 (LSA)** 拦截。

## 核心原因：LSA 保护 (RunAsPPL)

从 Windows 8.1/10 开始，Windows LSA（具体来说是 `lsass.exe`）会强制实施 **受保护进程轻量级 (PPL)** 保护。这是一种安全强化机制，旨在通过以下方式防止凭据盗窃（例如 Mimikatz）：

- 阻止非 Microsoft 签名的 DLL 加载 **到** LSA 进程中
- 阻止不受信任的代码访问 LSA 的受保护内存空间

**Sangfornspx64.dll** 可能尝试加载到 LSA 进程或与之交互（例如作为 **安全支持提供程序 (SSP)** 或 **身份验证包**），以便将深信服的 VPN 身份验证与 Windows 登录集成。然而，在 LSA 保护下：

1. **没有 Microsoft 签名** → 该 DLL 被阻止加载到 LSASS 中
2. **不在批准的列表中** → 只允许 Microsoft 签名的 DLL 或来自 **Microsoft 专属白名单**（例如某些 McAfee、Symantec、SentinelOne 组件）的 DLL

## 你将会看到的 Windows 事件

```
日志名称: System
来源: Microsoft-Windows-Security-Mitigations/Kernel Mode
事件 ID: 12
描述: "Windows LSA 已阻止加载不受信任的 DLL: C:\Program Files\Sangfor\...\sangfornspx64.dll"
```

## 解决方案（如果你需要它正常工作）

| 方法 | 作用 | 安全风险 |
|--------|-------------|---------------|
| **禁用 LSA 保护** | 将 `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\RunAsPPL` 设置为 `0` | **高** — 使 LSASS 暴露于凭据盗窃风险 |
| **联系深信服** | 请求提供经过正确签名且 Microsoft 批准的 DLL 版本 | 无（最佳方案） |
| **使用其他 VPN 客户端** | 切换到与 LSA 兼容的客户端（例如 OpenVPN、WireGuard） | 无 |

## 快速检查

你可以通过以下命令验证 LSA 保护状态：

```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL"
```

值为 `2` 表示已强制实施 PPL（会阻止深信服的 DLL）。值为 `0` 则允许加载——但从安全角度不推荐。

**结论：** 拦截是 Windows 防御机制按设计正常工作。深信服需要将其 DLL 提交给 Microsoft 进行签名/白名单认证，才能与现代 LSA 保护兼容。