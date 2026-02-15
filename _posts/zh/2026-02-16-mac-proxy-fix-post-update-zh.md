---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新后 Mac 代理修复方案
translated: true
type: note
---

Question: 我的 MacBook Air M2 在重启后卡在显示“软件更新完成”界面，但我通过暂时禁用 Wi-Fi 解决了初始卡顿。现在启动过程中没有网络，系统更新/设置窗口要求选择 Ethernet 或不使用网络。我选择了不使用网络，随后进入了欢迎屏幕。在 Installer Log（通过 Options 查看）中，我看到了 fetch URL 错误，这证实了是一个网络 Proxy 问题，因为 Clash 设置了系统 Proxies 但尚未运行。

Answer:

好消息——你已经度过了最关键的卡顿点！通过选择“不使用网络”（或离线设置），macOS Tahoe 的设置程序会跳过需要互联网的部分（如 iCloud 登录、App Store 激活或最后的更新抓取），让你能够直接进入桌面/欢迎屏幕。当网络配置损坏时（在你这种情况下，是残留的 Clash 系统 Proxy 设置阻止了与 Apple 服务器的连接），这是一种标准的解决方法。

Installer Log 中的 fetch URL 错误完全符合我们的预期：在更新后阶段，macOS 会尝试从 mesu.apple.com、gdmf.apple.com 或 swcdn.apple.com 等域名下载小型配置文件、字体或完成数据，但无效的 Proxy（127.0.0.1:7890 或类似地址）导致了超时或连接被拒绝。

### 彻底解决并恢复正常网络的后续步骤

1. **离线完成设置**
   - 继续通过“欢迎 / 设置助理”屏幕（语言、地区、Apple ID 登录如果提示可以先跳过——选择“稍后设置”）。
   - 你应该很快就能到达桌面。

2. **进入桌面后 – 立即禁用所有系统 Proxies**
   打开 **System Settings** > **Network** > 选择 **Wi-Fi** (或你使用的接口) > **Details…** (或 Advanced…) > **Proxies** 选项卡：
   - 取消勾选 / 关闭以下所有选项：
     - Auto Proxy Discovery
     - Automatic Proxy Configuration
     - Web Proxy (HTTP)
     - Secure Web Proxy (HTTPS)
     - SOCKS Proxy
   - 点击 **OK** → **Apply**。

   这将移除导致正常网络阻塞的 Clash 残留 Proxy 设置。

   或者（更快速的方法），登录后立即打开 **Terminal** 并运行：
   ```bash
   networksetup -setwebproxystate "Wi-Fi" off
   networksetup -setsecurewebproxystate "Wi-Fi" off
   networksetup -setsocksfirewallproxystate "Wi-Fi" off
   networksetup -setautoproxystate "Wi-Fi" off
   ```
   （如果你的服务名称不同，请将 "Wi-Fi" 替换为实际名称——可以通过 `networksetup -listallnetworkservices` 查看。）

3. **重新开启 Wi-Fi**
   - 点击菜单栏中的 Wi-Fi 图标 → 开启 Wi-Fi → 连接到你的网络。
   - 现在它应该可以在没有 Proxy 干扰的情况下正常连接。

4. **让 macOS 完成任何挂起的更新**
   - 前往 **System Settings > General > Software Update**。
   - 系统可能会发现并安装之前被阻止的任何剩余小型更新或配置文件。
   - 如果有提示，请重启。

5. **预防 Clash 导致的未来问题**
   - 打开 Clash → 确保 **"Set as System Proxy"** 已关闭（或者在 macOS 更新期间永远不要启用它）。
   - 优先使用 **TUN mode**（如果你的 Clash 版本在 macOS 上支持）——它在更低层级路由流量，而不触碰系统 Proxy 设置。
   - 在进行重大 macOS 更新或重启之前，考虑完全退出 Clash。

你基本上已经完成了——离线设置绕过是一个完美的变通方案。在清除 Proxies 并重新连接后，所有功能（App Store、iCloud、Safari 等）都应恢复正常。如果执行第 2 步后仍看到抓取错误或无法连接，请在 Terminal 中运行此命令并分享输出：
```bash
scutil --proxy
```
这将显示系统范围内是否仍有任何 Proxy 处于活动状态。

你已经熬过了最困难的部分——排查做得很好！

References:

- 本解决方案基于标准 macOS Proxy 行为以及 Apple 论坛和 Reddit 上报告的常见 Clash 相关更新卡顿案例。