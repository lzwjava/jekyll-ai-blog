---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何使用 Windows 11 远程桌面
translated: true
type: note
---

Question: 如何使用 Remote Desktop 连接到 Windows 11 PC？

Answer: 

Microsoft 的 Remote Desktop 功能允许你从另一台设备连接并控制一台 Windows 11 PC。请注意，**你要连接的 Windows 11 PC（主机）**必须运行 Pro、Enterprise 或 Education 版本——Windows 11 Home 版不支持作为 Remote Desktop 的宿主机。

### Step 1: 在 Windows 11 主机上启用 Remote Desktop

1. 打开 **Settings**（按 Windows 键 + I）。
2. 前往 **System** > **Remote Desktop**。
3. 将 **Enable Remote Desktop** 开关切换为 **On**，并确认弹窗提示。
4. 记下此页面显示的 **PC name**——你将需要它从另一台设备进行连接。
5. （可选）在 **Remote Desktop users** 下，添加任何需要远程访问权限的其他用户账号。

主机必须保持开机状态、连接到网络/互联网，且不能处于 sleep 模式，连接才能生效。

### Step 2: 从另一台 Windows PC（客户端）连接

1. 在客户端 PC 的开始菜单中搜索 **Remote Desktop Connection** 并打开它（或运行 `mstsc.exe`）。
2. 输入 Windows 11 主机的 **PC name** 或 **IP address**。
3. 点击 **Connect**。
4. 输入主机上已授权账号的 username 和 password。
5. 如果弹出证书提示，点击 **Yes** 继续。

现在你将拥有远程桌面会话的完全控制权。

### Step 3: 从 macOS, iOS, Android 或其他设备连接

- 从 App Store、Google Play 或 Microsoft Store 下载 **Windows App**（Microsoft 推荐）或 **Microsoft Remote Desktop** 应用。
- 通过输入主机的 PC name 或 IP address 添加新的 PC 连接。
- 保存并连接，然后在提示时提供登录凭据。

### Additional Tips

- 对于同一本地网络内的连接，使用 PC name。
- 对于通过互联网进行的连接，使用公网 IP address 或在路由器上设置端口转发（port 3389），或者为了安全性，建议统使用 VPN。由于潜在的攻击风险，直接将 RDP 暴露在互联网上是非常危险的——请务必使用强密码并考虑使用 Network Level Authentication（默认已启用）。
- Firewall：启用功能时 Windows 通常会自动允许 RDP 通过，但请确保没有第三方 firewall 对其进行拦截。
- Troubleshooting：如果连接失败，请检查主机是否处于唤醒状态、凭据是否正确，以及两台设备是否可以互相访问（尝试 ping 主机）。

References:  
- [How to use Remote Desktop - Microsoft Support](https://support.microsoft.com/en-us/windows/how-to-use-remote-desktop-5fe128d5-8fb1-7a23-3b8a-41e636865e8c)  
- [Enable Remote Desktop on your PC | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access)