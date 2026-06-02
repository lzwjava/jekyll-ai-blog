---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 macOS 代理更新卡住的问题
translated: true
type: note
---

是的，Clash（如 ClashX、Clash for Windows 的 Mac 移植版或类似工具）在启用 "Set as System Proxy" 时，通常会设置系统级的 **HTTP**、**HTTPS** 和/或 **SOCKS** Proxy（通常指向 127.0.0.1 的 7890/7891 端口）。如果 App 崩溃、异常退出，或者在 macOS 更新/设置期间发生冲突，可能会残留这些 Proxy 设置——导致软件更新卡住，因为无法通过本地 Proxy 环回地址正常访问 Apple 的更新服务器。

既然你已经在 **Terminal** 中（考虑到卡在 "Software Update Complete" 界面，可能是在 macOS Recovery 或单用户模式下），我们可以通过内置的 `networksetup` 命令禁用所有 Proxy 设置。这是在没有 GUI 的情况下清除设置最干净的方法。

### Step 1: 查找你的 Network Service 名称

大多数 MacBook Air 使用 **Wi-Fi**（注意大小写！）。运行此命令确认：

```bash
networksetup -listallnetworkservices
```

- 寻找活动的名称（通常是 **Wi-Fi**，如果是主连接，旁边可能带有一个 *）。
- 如果是其他名称（较少见，如 "Thunderbolt Ethernet"），请在下面的命令中使用该名称。
- M2 Air 上的常用名称：**Wi-Fi**

### Step 2: 检查当前的 Proxy 设置（可选但推荐）

运行以下命令查看已设置的内容（根据需要替换 "Wi-Fi"）：

```bash
networksetup -getwebproxy "Wi-Fi"
networksetup -getsecurewebproxy "Wi-Fi"
networksetup -getsocksfirewallproxy "Wi-Fi"
networksetup -getautoproxyurl "Wi-Fi"
```

- 你可能会看到 HTTP/HTTPS/SOCKS 显示 Enabled: Yes 且 Server: 127.0.0.1 Port: 7890（或类似值）。

### Step 3: 禁用 / 清除所有 Proxy

逐条运行以下命令（如果要求输入密码请使用 `sudo`；在 Recovery 模式下通常不需要，或根据提示输入管理员密码）：

```bash
networksetup -setwebproxystate "Wi-Fi" off
networksetup -setsecurewebproxystate "Wi-Fi" off
networksetup -setsocksfirewallproxystate "Wi-Fi" off
networksetup -setautoproxystate "Wi-Fi" off
```

- 这些操作会关闭 **off** HTTP (Web Proxy)、HTTPS (Secure Web Proxy)、SOCKS 以及 Automatic Proxy Configuration (PAC URL)。
- 为了更加彻底（完全清除任何服务器/端口数值），你还可以运行：

```bash
networksetup -setwebproxy "Wi-Fi" "" 0
networksetup -setsecurewebproxy "Wi-Fi" "" 0
networksetup -setsocksfirewallproxy "Wi-Fi" "" 0
```

（空服务器和端口 0 会有效地清除它们。）

### Step 4: 验证是否已关闭

重新运行 Step 2 中的查询命令——现在它们应该显示 **Enabled: No**。

### Step 5: 退出并重试引导

- 输入 `exit`（或 `reboot`）退出 Terminal/Recovery。
- 从 Recovery 菜单中选择 **Restart**（或根据需要长按电源键强制重启）。
- 你的 Mac 现在应该在没有 Proxy 干扰的情况下启动，并有望跳过 "Software Update Complete" 界面以完成设置或进入桌面。

### 关于 Clash 的额提示

- 正常进入 macOS 后，在进行未来的更新前，请先打开 Clash → 关闭 **"Set as System Proxy"**（或完全退出 Clash）。
- 如果你在 Clash 中使用 TUN mode，它通常不会触动系统 Proxy——相比系统 Proxy 模式，更推荐使用该模式。
- 如果操作后仍然卡住，请回到 Recovery → Disk Utility → 对你的驱动器再次执行 First Aid，然后尝试 **Reinstall macOS**（非破坏性安装）。

如果 `networksetup -listallnetworkservices` 显示异常或任何命令报错，请告诉我——我可以进行调整！这可以解决绝大多数由 Proxy 引起的更新卡顿问题。
